from __future__ import annotations

from decimal import Decimal
from typing import Any

from .errors import AdapterError, EXIT_HLEDGER_EXECUTION
from .models import CategoryMap, ContextSummary, EngineReports
from .normalize import _decode_amount_list, _format_money


ZERO = Decimal("0.00")

UNSUPPORTED_CAPABILITIES = [
    "tax_liability_calculation",
    "deductibility_determination",
    "form_1040_generation",
    "schedule_generation",
    "refund_calculation",
    "return_validation",
    "efile_submission",
]

BASE_WARNINGS = [
    {
        "code": "NOT_TAX_CALCULATION",
        "message": "Results are bookkeeping summaries and non-authoritative tax-adjacent labels.",
    },
    {
        "code": "TAX_HINTS_NON_AUTHORITATIVE",
        "message": "Tax hints are controlled synthetic labels, not tax treatment.",
    },
]


def build_financial_summary(
    normalized: dict[str, Any],
    reports: EngineReports,
    category_map: CategoryMap,
    context: ContextSummary,
) -> dict[str, Any]:
    account_balances = _account_balances(normalized)
    category_amounts = _category_magnitudes(normalized, category_map, account_balances)
    grouped = _group_category_amounts(category_amounts, category_map)

    opening_balance = grouped["ledger.opening_balance"].get("opening_balance", ZERO)
    gross_receipts = _sum_values(grouped["schedule_c_style.gross_receipts"])
    cash_expenses = _sum_values(grouped["schedule_c_style.cash_expenses"])
    interest_income = _sum_values(grouped["tax_adjacent.interest_income"])
    cash_charity = _sum_values(grouped["tax_adjacent.cash_charitable_contributions"])
    estimated_payments = _sum_values(grouped["tax_adjacent.federal_estimated_payments"])
    checking_balance = account_balances.get(category_map.primary_account)
    if checking_balance is None:
        _invariant_failed("primary checking account was missing from normalized accounts")

    income_statement = _decode_income_statement(reports.income_statement_json, category_map)
    expected_revenue = gross_receipts + interest_income
    expected_expenses = cash_expenses + cash_charity
    expected_net = expected_revenue - expected_expenses
    if income_statement["revenue"] != expected_revenue:
        _invariant_failed("income-statement revenue did not match mapped revenue buckets")
    if income_statement["expenses"] != expected_expenses:
        _invariant_failed("income-statement expenses did not match mapped expense buckets")
    if income_statement["net"] != expected_net:
        _invariant_failed("income-statement net did not equal revenue minus expenses")
    expected_checking = opening_balance + income_statement["net"] - estimated_payments
    if checking_balance != expected_checking:
        _invariant_failed("checking balance did not match opening plus net income minus tracked tax payments")

    schedule_c_net = gross_receipts - cash_expenses
    tax_adjacent = {
        "interest_income": _format_money(interest_income),
        "cash_charitable_contributions": _format_money(cash_charity),
        "federal_estimated_tax_payments_tracked": _format_money(estimated_payments),
    }

    return {
        "summary": {
            "opening_balance": _format_money(opening_balance),
            "checking_balance": _format_money(checking_balance),
            "bookkeeping_income_statement": {
                "revenue": _format_money(income_statement["revenue"]),
                "expenses": _format_money(income_statement["expenses"]),
                "net": _format_money(income_statement["net"]),
                "equivalent_to_schedule_c_style": income_statement["net"] == schedule_c_net,
            },
            "schedule_c_style": {
                "tax_treatment_authoritative": False,
                "gross_receipts": _format_money(gross_receipts),
                "cash_expenses_by_category": {
                    key: _format_money(value)
                    for key, value in grouped["schedule_c_style.cash_expenses"].items()
                },
                "cash_expenses_before_mileage": _format_money(cash_expenses),
                "net_before_mileage": _format_money(schedule_c_net),
            },
            "tax_adjacent": tax_adjacent,
        },
        "unmapped_tax_facts": [
            {
                "code": "BUSINESS_MILEAGE",
                "value": context.business_miles,
                "unit": "mile",
                "status": context.mileage_status,
                "deduction_usd": None,
            },
            {
                "code": "CHARITY_TREATMENT",
                "amount": tax_adjacent["cash_charitable_contributions"],
                "status": "summarized_no_deductibility_decision",
            },
            {
                "code": "ESTIMATED_PAYMENT_TREATMENT",
                "amount": tax_adjacent["federal_estimated_tax_payments_tracked"],
                "status": "summarized_no_tax_liability_or_refund",
            },
        ],
        "unsupported_capabilities": list(UNSUPPORTED_CAPABILITIES),
        "warnings": [dict(item) for item in BASE_WARNINGS],
    }


def _account_balances(normalized: dict[str, Any]) -> dict[str, Decimal]:
    accounts = normalized.get("accounts")
    if not isinstance(accounts, list):
        _schema_mismatch("normalized accounts must be a list")
    result: dict[str, Decimal] = {}
    for account in accounts:
        if not isinstance(account, dict):
            _schema_mismatch("normalized account must be an object")
        name = account.get("name")
        balance = account.get("ledger_balance")
        if not isinstance(name, str) or not isinstance(balance, str):
            _schema_mismatch("normalized account name and balance must be strings")
        result[name] = Decimal(balance)
    return result


def _category_magnitudes(
    normalized: dict[str, Any],
    category_map: CategoryMap,
    account_balances: dict[str, Decimal],
) -> dict[str, Decimal]:
    category_source_totals = {category: ZERO for category in category_map.categories}
    transactions = normalized.get("transactions")
    if not isinstance(transactions, list):
        _schema_mismatch("normalized transactions must be a list")

    for transaction in transactions:
        if not isinstance(transaction, dict):
            _schema_mismatch("normalized transaction must be an object")
        category = transaction.get("category")
        amount = transaction.get("source_amount")
        if not isinstance(category, str) or not isinstance(amount, str):
            _schema_mismatch("normalized transaction category and source amount must be strings")
        if category not in category_source_totals:
            _invariant_failed("normalized transaction category was not present in the category map")
        category_source_totals[category] += Decimal(amount)

    category_amounts: dict[str, Decimal] = {}
    for category, rule in category_map.categories.items():
        source_total = category_source_totals[category]
        if rule.expected_source_sign == "positive" and source_total < ZERO:
            _invariant_failed(f"positive category summarized to a negative source amount: {category}")
        if rule.expected_source_sign == "negative" and source_total > ZERO:
            _invariant_failed(f"negative category summarized to a positive source amount: {category}")

        source_magnitude = abs(source_total)
        account_balance = account_balances.get(category)
        if account_balance is None:
            if source_magnitude != ZERO:
                _invariant_failed(f"category account was missing from normalized balances: {category}")
        elif abs(account_balance) != source_magnitude:
            _invariant_failed(f"category balance did not match source summary magnitude: {category}")
        category_amounts[category] = source_magnitude
    return category_amounts


def _group_category_amounts(
    category_amounts: dict[str, Decimal],
    category_map: CategoryMap,
) -> dict[str, dict[str, Decimal]]:
    grouped = {
        "ledger.opening_balance": {},
        "schedule_c_style.gross_receipts": {},
        "schedule_c_style.cash_expenses": {},
        "tax_adjacent.interest_income": {},
        "tax_adjacent.cash_charitable_contributions": {},
        "tax_adjacent.federal_estimated_payments": {},
    }
    for category, rule in category_map.categories.items():
        bucket = grouped.get(rule.summary_bucket)
        if bucket is None:
            _invariant_failed(f"unsupported summary bucket in category map: {rule.summary_bucket}")
        amount = category_amounts[category]
        if amount != ZERO:
            bucket[rule.summary_key] = amount
    return grouped


def _decode_income_statement(raw: Any, category_map: CategoryMap) -> dict[str, Decimal]:
    if not isinstance(raw, dict):
        _schema_mismatch("hledger income-statement JSON must be an object")
    subreports = raw.get("cbrSubreports")
    if not isinstance(subreports, list):
        _schema_mismatch("hledger income-statement subreports must be a list")

    totals: dict[str, Decimal] = {}
    for item in subreports:
        if not isinstance(item, list) or len(item) != 3:
            _schema_mismatch("hledger income-statement subreport shape was unexpected")
        label, report, _is_revenue = item
        if label in {"Revenues", "Expenses"}:
            if label in totals:
                _invariant_failed(f"hledger income-statement duplicated {label}")
            totals[label] = _periodic_report_total(report, category_map)

    if set(totals) != {"Revenues", "Expenses"}:
        _invariant_failed("hledger income statement did not include both revenue and expense totals")
    net = _report_row_total(raw.get("cbrTotals"), category_map)
    if totals["Revenues"] - totals["Expenses"] != net:
        _invariant_failed("hledger income-statement total did not equal revenue minus expenses")
    return {
        "revenue": totals["Revenues"],
        "expenses": totals["Expenses"],
        "net": net,
    }


def _periodic_report_total(report: Any, category_map: CategoryMap) -> Decimal:
    if not isinstance(report, dict):
        _schema_mismatch("hledger periodic report must be an object")
    return _report_row_total(report.get("prTotals"), category_map)


def _report_row_total(row: Any, category_map: CategoryMap) -> Decimal:
    if not isinstance(row, dict):
        _schema_mismatch("hledger report total row must be an object")
    return _decode_amount_list(row.get("prrTotal"), category_map)


def _sum_values(values: dict[str, Decimal]) -> Decimal:
    return sum(values.values(), ZERO)


def _schema_mismatch(message: str) -> None:
    raise AdapterError("ENGINE_OUTPUT_SCHEMA_MISMATCH", message, exit_code=EXIT_HLEDGER_EXECUTION)


def _invariant_failed(message: str) -> None:
    raise AdapterError("ACCOUNTING_INVARIANT_FAILED", message, exit_code=EXIT_HLEDGER_EXECUTION)
