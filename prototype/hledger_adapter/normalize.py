from __future__ import annotations

from decimal import Decimal
from typing import Any

from .errors import AdapterError, EXIT_HLEDGER_EXECUTION
from .models import CategoryMap, EngineReports, LoadedTransactions, SourceTransaction


CENT = Decimal("0.01")


def normalize_transactions_and_accounts(
    reports: EngineReports,
    transactions: LoadedTransactions,
    category_map: CategoryMap,
) -> dict[str, Any]:
    source_by_id = {record.transaction_id: record for record in transactions.records}
    if len(source_by_id) != len(transactions.records):
        _invariant_failed("Validated source transactions contain duplicate IDs")

    normalized_transactions: list[dict[str, Any]] = []
    account_totals: dict[str, Decimal] = {}
    category_source_totals: dict[str, Decimal] = {}
    seen_ids: set[str] = set()
    posting_count = 0

    if not isinstance(reports.print_json, list):
        _schema_mismatch("hledger print JSON must be a transaction list")

    for raw_transaction in reports.print_json:
        if not isinstance(raw_transaction, dict):
            _schema_mismatch("hledger print transaction must be an object")
        transaction_id = raw_transaction.get("tcode")
        if not isinstance(transaction_id, str) or not transaction_id:
            _schema_mismatch("hledger print transaction is missing tcode")
        if transaction_id in seen_ids:
            _invariant_failed("hledger print JSON contains a duplicate transaction ID", transaction_id)
        source = source_by_id.get(transaction_id)
        if source is None:
            _invariant_failed("hledger print JSON contains an unexpected transaction ID", transaction_id)
        seen_ids.add(transaction_id)

        if raw_transaction.get("tdate") != source.date:
            _invariant_failed("hledger transaction date did not match source CSV", transaction_id)
        _validate_tags(raw_transaction, source)

        postings = raw_transaction.get("tpostings")
        if not isinstance(postings, list) or len(postings) != 2:
            _invariant_failed("hledger transaction must contain exactly two postings", transaction_id)
        decoded_postings = [_decode_posting(posting, category_map, transaction_id) for posting in postings]
        posting_count += len(decoded_postings)

        accounts = {posting["account"] for posting in decoded_postings}
        if accounts != {category_map.primary_account, source.category}:
            _invariant_failed("hledger posting accounts did not match source account/category", transaction_id)

        source_posting = _single_posting(decoded_postings, category_map.primary_account, transaction_id)
        category_posting = _single_posting(decoded_postings, source.category, transaction_id)
        if source_posting["amount"] != source.amount_usd:
            _invariant_failed("hledger source-account amount did not match source CSV", transaction_id)
        if category_posting["amount"] != -source.amount_usd:
            _invariant_failed("hledger category amount was not equal and opposite", transaction_id)
        if source_posting["amount"] + category_posting["amount"] != Decimal("0.00"):
            _invariant_failed("hledger postings did not sum to zero", transaction_id)

        for posting in decoded_postings:
            account_totals[posting["account"]] = account_totals.get(posting["account"], Decimal("0.00")) + posting["amount"]
        category_source_totals[source.category] = category_source_totals.get(source.category, Decimal("0.00")) + source.amount_usd

        normalized_transactions.append(_transaction_payload(source))

    expected_ids = set(source_by_id)
    if seen_ids != expected_ids:
        missing = sorted(expected_ids - seen_ids)
        extra = sorted(seen_ids - expected_ids)
        detail = ", ".join([*(f"missing:{value}" for value in missing[:3]), *(f"extra:{value}" for value in extra[:3])])
        _invariant_failed(f"hledger transaction IDs did not match source CSV ({detail})")

    accounts = _normalize_balance_json(reports.balance_json, category_map)
    expected_accounts = {category_map.primary_account, *(record.category for record in transactions.records)}
    balance_accounts = {account["name"] for account in accounts}
    if balance_accounts != expected_accounts:
        _invariant_failed("hledger account list did not match accounts implied by source CSV")

    balance_by_account = {account["name"]: Decimal(account["ledger_balance"]) for account in accounts}
    for account_name in expected_accounts:
        posting_total = account_totals.get(account_name, Decimal("0.00"))
        balance_total = balance_by_account.get(account_name)
        if balance_total != posting_total:
            _invariant_failed(f"hledger balance did not match reconciled postings for {account_name}")

    for category, source_total in category_source_totals.items():
        if balance_by_account[category] != -source_total:
            _invariant_failed(f"hledger category balance did not match source amounts for {category}")

    checking_balance = balance_by_account.get(category_map.primary_account, Decimal("0.00"))
    source_posting_total = account_totals.get(category_map.primary_account, Decimal("0.00"))
    if checking_balance != source_posting_total:
        _invariant_failed("checking balance did not match source-account postings")

    return {
        "transactions": normalized_transactions,
        "accounts": accounts,
        "counts": {
            "input_files": len(transactions.files),
            "transactions": len(normalized_transactions),
            "postings": posting_count,
            "accounts": len(accounts),
        },
        "reconciliation": {
            "status": "passed",
            "checks": [
                "transaction_ids_exact",
                "two_balanced_usd_postings_per_transaction",
                "source_account_amounts_match_csv",
                "category_postings_equal_and_opposite",
                "accounts_match_input_categories",
                "account_balances_match_reconciled_postings",
                "checking_balance_matches_source_postings",
            ],
            "checking_balance": _format_money(checking_balance),
        },
    }


def _decode_posting(posting: Any, category_map: CategoryMap, transaction_id: str) -> dict[str, Any]:
    if not isinstance(posting, dict):
        _schema_mismatch("hledger posting must be an object", transaction_id)
    account = posting.get("paccount")
    if not isinstance(account, str) or not account:
        _schema_mismatch("hledger posting account must be a string", transaction_id)
    if posting.get("ptype") != "RegularPosting":
        _invariant_failed("hledger posting was not regular", transaction_id)
    return {
        "account": account,
        "amount": _decode_amount_list(posting.get("pamount"), category_map, transaction_id),
    }


def _decode_amount_list(raw_amounts: Any, category_map: CategoryMap, transaction_id: str | None = None) -> Decimal:
    if not isinstance(raw_amounts, list) or len(raw_amounts) != 1:
        _schema_mismatch("hledger amount list must contain exactly one amount", transaction_id)
    return _decode_amount(raw_amounts[0], category_map, transaction_id)


def _decode_amount(raw_amount: Any, category_map: CategoryMap, transaction_id: str | None = None) -> Decimal:
    if not isinstance(raw_amount, dict):
        _schema_mismatch("hledger amount must be an object", transaction_id)
    if raw_amount.get("acommodity") != category_map.currency:
        _invariant_failed("hledger amount commodity was not USD", transaction_id)
    if raw_amount.get("acost") is not None or raw_amount.get("acostbasis") is not None:
        _invariant_failed("hledger amount unexpectedly included cost conversion", transaction_id)
    quantity = raw_amount.get("aquantity")
    if not isinstance(quantity, dict):
        _schema_mismatch("hledger amount quantity must be an object", transaction_id)
    mantissa = quantity.get("decimalMantissa")
    places = quantity.get("decimalPlaces")
    if type(mantissa) is not int or type(places) is not int:
        _schema_mismatch("hledger decimal amount must use integer mantissa and places", transaction_id)
    amount = Decimal(mantissa).scaleb(-places)
    if amount.quantize(CENT) != amount:
        _invariant_failed("hledger amount was not representable as cents", transaction_id)
    return amount


def _normalize_balance_json(raw_balance: Any, category_map: CategoryMap) -> list[dict[str, Any]]:
    if not isinstance(raw_balance, list) or len(raw_balance) != 2:
        _schema_mismatch("hledger balance JSON must contain account rows and a total")
    rows, total_amounts = raw_balance
    if not isinstance(rows, list):
        _schema_mismatch("hledger balance account rows must be a list")
    total = _decode_amount_list(total_amounts, category_map)
    if total != Decimal("0.00"):
        _invariant_failed("full hledger balance total did not sum to zero")

    accounts: list[dict[str, Any]] = []
    seen_accounts: set[str] = set()
    for row in rows:
        if not isinstance(row, list) or len(row) != 4:
            _schema_mismatch("hledger balance row shape was unexpected")
        account_name = row[0]
        if not isinstance(account_name, str) or not account_name:
            _schema_mismatch("hledger balance account name must be a string")
        if account_name in seen_accounts:
            _invariant_failed(f"hledger balance duplicated account {account_name}")
        seen_accounts.add(account_name)
        accounts.append(
            {
                "name": account_name,
                "ledger_balance": _format_money(_decode_amount_list(row[3], category_map)),
            }
        )
    return accounts


def _single_posting(decoded_postings: list[dict[str, Any]], account_name: str, transaction_id: str) -> dict[str, Any]:
    matches = [posting for posting in decoded_postings if posting["account"] == account_name]
    if len(matches) != 1:
        _invariant_failed(f"expected exactly one posting for {account_name}", transaction_id)
    return matches[0]


def _validate_tags(raw_transaction: dict[str, Any], source: SourceTransaction) -> None:
    raw_tags = raw_transaction.get("ttags")
    if not isinstance(raw_tags, list):
        _schema_mismatch("hledger transaction tags must be a list", source.transaction_id)
    tags: dict[str, str] = {}
    for item in raw_tags:
        if not isinstance(item, list) or len(item) != 2 or not all(isinstance(value, str) for value in item):
            _schema_mismatch("hledger transaction tag shape was unexpected", source.transaction_id)
        tags[item[0]] = item[1]
    if tags.get("tax_hint") != source.tax_hint or tags.get("memo") != source.memo:
        _invariant_failed("hledger tax_hint/memo tags did not match source CSV", source.transaction_id)


def _transaction_payload(source: SourceTransaction) -> dict[str, Any]:
    return {
        "id": source.transaction_id,
        "date": source.date,
        "payee": source.payee,
        "description": source.description,
        "source_account": source.source_account,
        "category": source.category,
        "source_amount": _format_money(source.amount_usd),
        "tax_hint": source.tax_hint,
        "source_cleared": source.cleared,
        "memo": source.memo,
    }


def _format_money(amount: Decimal) -> str:
    quantized = amount.quantize(CENT)
    if quantized == Decimal("-0.00"):
        quantized = Decimal("0.00")
    return format(quantized, "f")


def _schema_mismatch(message: str, transaction_id: str | None = None) -> None:
    detail = {"transaction_id": transaction_id} if transaction_id else None
    raise AdapterError("ENGINE_OUTPUT_SCHEMA_MISMATCH", message, exit_code=EXIT_HLEDGER_EXECUTION, detail=detail)


def _invariant_failed(message: str, transaction_id: str | None = None) -> None:
    detail = {"transaction_id": transaction_id} if transaction_id else None
    raise AdapterError("ACCOUNTING_INVARIANT_FAILED", message, exit_code=EXIT_HLEDGER_EXECUTION, detail=detail)
