from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from .errors import AdapterError
from .models import CategoryMap, CategoryRule, ContextSummary, InputFileSummary, LoadedTransactions, SourceTransaction


TRANSACTION_HEADER = [
    "transaction_id",
    "date",
    "payee",
    "description",
    "account",
    "category",
    "tax_hint",
    "amount_usd",
    "cleared",
    "memo",
]

TRANSACTION_ID_RE = re.compile(r"^[A-Z][A-Z0-9._-]{0,63}$")
DATE_RE = re.compile(r"^\d{2}-\d{2}-\d{4}$")
AMOUNT_RE = re.compile(r"^-?(0|[1-9][0-9]*)\.[0-9]{2}$")
EXPECTED_CATEGORY_KEYS = {
    "Equity:Opening Balances",
    "Income:Freelance:Design",
    "Income:Freelance:Consulting",
    "Income:Interest",
    "Expenses:Business:Software",
    "Expenses:Business:Office Equipment",
    "Expenses:Business:Office Supplies",
    "Expenses:Business:Travel",
    "Expenses:Business:Bank Fees",
    "Expenses:Business:Professional Education",
    "Expenses:Business:Coworking",
    "Expenses:Charity",
    "Liabilities:Federal Tax:Estimated Payments",
}
PRIVACY_LABEL = "synthetic-no-pii-no-real-account-data"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path, invalid_code: str = "CONTEXT_INVALID") -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AdapterError("INPUT_NOT_FOUND", f"Required file was not found: {path.name}") from exc
    except OSError as exc:
        raise AdapterError("INPUT_NOT_FOUND", f"Required file could not be opened: {path.name}") from exc

    def reject_constant(value: str) -> None:
        raise AdapterError(invalid_code, f"Unsupported JSON constant: {value}")

    try:
        return json.loads(text, parse_float=Decimal, parse_constant=reject_constant)
    except AdapterError:
        raise
    except json.JSONDecodeError as exc:
        raise AdapterError(
            invalid_code,
            f"Invalid JSON in {path.name}",
            detail={"line": exc.lineno, "column": exc.colno},
        ) from exc


def load_category_map(path: Path) -> CategoryMap:
    if not path.exists() or not path.is_file():
        raise AdapterError("CONFIG_INVALID", f"Category map is missing: {path.name}")
    raw = _load_json(path, invalid_code="CONFIG_INVALID")
    if not isinstance(raw, dict):
        raise AdapterError("CONFIG_INVALID", "Category map must be a JSON object")

    allowed_top_keys = {"schema_version", "dataset", "primary_account", "engine", "limits", "categories"}
    if set(raw) != allowed_top_keys:
        raise AdapterError("CONFIG_INVALID", "Category map has missing or unsupported top-level keys")
    if raw["schema_version"] != "1.0.0":
        raise AdapterError("CONFIG_INVALID", "Unsupported category-map schema version")

    dataset = raw["dataset"]
    engine = raw["engine"]
    limits = raw["limits"]
    categories_raw = raw["categories"]
    if not isinstance(dataset, dict) or not isinstance(engine, dict) or not isinstance(limits, dict):
        raise AdapterError("CONFIG_INVALID", "Category map sections must be JSON objects")
    if not isinstance(categories_raw, dict):
        raise AdapterError("CONFIG_INVALID", "Category map categories must be a JSON object")

    if set(categories_raw) != EXPECTED_CATEGORY_KEYS:
        raise AdapterError("CONFIG_INVALID", "Category map category keys differ from the version 1 table")
    if raw["primary_account"] != "Assets:Checking":
        raise AdapterError("CONFIG_INVALID", "Unsupported primary account")

    try:
        categories = {
            account: CategoryRule(
                account=account,
                summary_bucket=str(rule["summary_bucket"]),
                summary_key=str(rule["summary_key"]),
                expected_source_sign=str(rule["expected_source_sign"]),
                allowed_tax_hints=tuple(str(value) for value in rule["allowed_tax_hints"]),
            )
            for account, rule in categories_raw.items()
        }
    except (KeyError, TypeError) as exc:
        raise AdapterError("CONFIG_INVALID", "Category map category rule is incomplete") from exc

    for rule in categories.values():
        if rule.expected_source_sign not in {"positive", "negative"}:
            raise AdapterError("CONFIG_INVALID", "Category map contains an unsupported source-sign rule")
        if len(rule.allowed_tax_hints) != 1:
            raise AdapterError("CONFIG_INVALID", "Version 1 expects exactly one tax hint per category")

    try:
        return CategoryMap(
            schema_version=raw["schema_version"],
            dataset_id=str(dataset["id"]),
            tax_year=int(dataset["tax_year"]),
            currency=str(dataset["currency"]),
            synthetic_only=bool(dataset["synthetic_only"]),
            primary_account=str(raw["primary_account"]),
            tested_hledger_version=str(engine["tested_version"]),
            max_input_rows=int(limits["max_input_rows"]),
            max_input_bytes=int(limits["max_input_bytes"]),
            max_abs_amount_usd=Decimal(str(limits["max_abs_amount_usd"])),
            subprocess_timeout_seconds=int(limits["subprocess_timeout_seconds"]),
            max_subprocess_output_bytes=int(limits["max_subprocess_output_bytes"]),
            categories=categories,
            path=path,
            sha256=sha256_file(path),
        )
    except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
        raise AdapterError("CONFIG_INVALID", "Category map scalar fields are incomplete or invalid") from exc


def load_transactions(paths: list[Path], category_map: CategoryMap) -> LoadedTransactions:
    if not paths:
        raise AdapterError("INPUT_NOT_FOUND", "At least one transaction CSV is required")

    seen_ids: set[str] = set()
    transaction_ids: list[str] = []
    records: list[SourceTransaction] = []
    summaries: list[InputFileSummary] = []
    total_rows = 0

    for path in paths:
        if not path.exists() or not path.is_file():
            raise AdapterError("INPUT_NOT_FOUND", f"Transaction file was not found: {path.name}")
        byte_count = path.stat().st_size
        if byte_count > category_map.max_input_bytes:
            raise AdapterError("INPUT_SCHEMA_INVALID", f"Transaction file is too large: {path.name}")

        try:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.reader(handle)
                try:
                    header = next(reader)
                except StopIteration as exc:
                    raise AdapterError("INPUT_SCHEMA_INVALID", f"Transaction file is empty: {path.name}") from exc
                if header != TRANSACTION_HEADER:
                    raise AdapterError("INPUT_SCHEMA_INVALID", f"Unexpected transaction header in {path.name}")

                file_rows = 0
                for row_number, row in enumerate(reader, start=2):
                    file_rows += 1
                    total_rows += 1
                    if total_rows > category_map.max_input_rows:
                        raise AdapterError("INPUT_SCHEMA_INVALID", "Too many transaction rows")
                    if len(row) != len(TRANSACTION_HEADER):
                        raise AdapterError(
                            "INPUT_SCHEMA_INVALID",
                            f"Wrong column count in {path.name}",
                            detail={"row": row_number},
                        )
                    record = dict(zip(TRANSACTION_HEADER, row, strict=True))
                    source_transaction = _validate_transaction_row(record, row_number, path.name, category_map)
                    transaction_id = source_transaction.transaction_id
                    if transaction_id in seen_ids:
                        raise AdapterError(
                            "INPUT_ID_DUPLICATE",
                            "Duplicate transaction ID",
                            detail={"transaction_id": transaction_id},
                        )
                    seen_ids.add(transaction_id)
                    transaction_ids.append(transaction_id)
                    records.append(source_transaction)
        except UnicodeDecodeError as exc:
            raise AdapterError("INPUT_SCHEMA_INVALID", f"Transaction file is not UTF-8: {path.name}") from exc
        except OSError as exc:
            raise AdapterError("INPUT_NOT_FOUND", f"Transaction file could not be opened: {path.name}") from exc

        summaries.append(
            InputFileSummary(
                name=path.name,
                sha256=sha256_file(path),
                bytes=byte_count,
                rows=file_rows,
            )
        )

    return LoadedTransactions(
        files=tuple(summaries),
        row_count=total_rows,
        transaction_ids=tuple(transaction_ids),
        records=tuple(records),
    )


def _validate_transaction_row(
    record: dict[str, str],
    row_number: int,
    file_name: str,
    category_map: CategoryMap,
) -> SourceTransaction:
    for field in ("transaction_id", "date", "account", "category", "tax_hint", "amount_usd", "cleared"):
        value = record[field]
        if value != value.strip():
            raise AdapterError("INPUT_SCHEMA_INVALID", f"Whitespace is not allowed around {field}", detail={"row": row_number})
    for field, limit in (("payee", 200), ("description", 500), ("memo", 500)):
        value = record[field]
        if any(char in value for char in ("\x00", "\r", "\n")):
            raise AdapterError("INPUT_SCHEMA_INVALID", f"Invalid control character in {field}", detail={"row": row_number})
        if field != "memo" and not value:
            raise AdapterError("INPUT_SCHEMA_INVALID", f"Required text field is empty: {field}", detail={"row": row_number})
        if len(value) > limit:
            raise AdapterError("INPUT_SCHEMA_INVALID", f"Text field is too long: {field}", detail={"row": row_number})

    transaction_id = record["transaction_id"]
    if not TRANSACTION_ID_RE.match(transaction_id):
        raise AdapterError("INPUT_SCHEMA_INVALID", "Invalid transaction ID", detail={"row": row_number})

    if not DATE_RE.match(record["date"]):
        raise AdapterError("INPUT_DATE_INVALID", "Invalid transaction date format", detail={"row": row_number})
    try:
        parsed_date = datetime.strptime(record["date"], "%m-%d-%Y")
    except ValueError as exc:
        raise AdapterError("INPUT_DATE_INVALID", "Invalid transaction calendar date", detail={"row": row_number}) from exc
    if parsed_date.year != category_map.tax_year:
        raise AdapterError("INPUT_DATE_INVALID", "Transaction date is outside the configured tax year", detail={"row": row_number})

    if record["account"] != category_map.primary_account:
        raise AdapterError("INPUT_ACCOUNT_UNKNOWN", "Unsupported source account", detail={"row": row_number, "file": file_name})

    category = record["category"]
    rule = category_map.categories.get(category)
    if rule is None:
        raise AdapterError("INPUT_CATEGORY_UNKNOWN", "Unsupported category", detail={"row": row_number, "file": file_name})
    if record["tax_hint"] not in rule.allowed_tax_hints:
        raise AdapterError("INPUT_TAX_HINT_MISMATCH", "Tax hint does not match category", detail={"row": row_number})

    if not AMOUNT_RE.match(record["amount_usd"]):
        raise AdapterError("INPUT_AMOUNT_INVALID", "Invalid amount format", detail={"row": row_number})
    try:
        amount = Decimal(record["amount_usd"])
    except InvalidOperation as exc:
        raise AdapterError("INPUT_AMOUNT_INVALID", "Invalid amount value", detail={"row": row_number}) from exc
    if amount == Decimal("0.00") or abs(amount) > category_map.max_abs_amount_usd:
        raise AdapterError("INPUT_AMOUNT_INVALID", "Amount is zero or outside supported bounds", detail={"row": row_number})
    if rule.expected_source_sign == "positive" and amount <= 0:
        raise AdapterError("INPUT_SIGN_INVALID", "Category expects a positive source amount", detail={"row": row_number})
    if rule.expected_source_sign == "negative" and amount >= 0:
        raise AdapterError("INPUT_SIGN_INVALID", "Category expects a negative source amount", detail={"row": row_number})

    if record["cleared"] != "true":
        raise AdapterError("INPUT_SCHEMA_INVALID", "Version 1 requires cleared=true", detail={"row": row_number})

    return SourceTransaction(
        transaction_id=transaction_id,
        date=parsed_date.strftime("%Y-%m-%d"),
        payee=record["payee"],
        description=record["description"],
        source_account=record["account"],
        category=category,
        tax_hint=record["tax_hint"],
        amount_usd=amount,
        cleared=True,
        memo=record["memo"],
    )


def load_context(path: Path | None, category_map: CategoryMap) -> ContextSummary:
    if path is None:
        return ContextSummary(
            supplied=False,
            name=None,
            sha256=None,
            mileage_status="not_provided",
            business_miles=None,
        )
    if not path.exists() or not path.is_file():
        raise AdapterError("INPUT_NOT_FOUND", f"Context file was not found: {path.name}")
    raw = _load_json(path)
    if not isinstance(raw, dict):
        raise AdapterError("CONTEXT_INVALID", "Context must be a JSON object")
    if raw.get("dataset_id") != category_map.dataset_id:
        raise AdapterError("CONTEXT_INVALID", "Context dataset_id does not match the category map")
    if raw.get("tax_year") != category_map.tax_year:
        raise AdapterError("CONTEXT_INVALID", "Context tax_year does not match the category map")
    if raw.get("privacy") != PRIVACY_LABEL:
        raise AdapterError("CONTEXT_INVALID", "Context privacy label is unsupported")
    if raw.get("currency") != category_map.currency:
        raise AdapterError("CONTEXT_INVALID", "Context currency is unsupported")

    expenses = raw.get("schedule_c_expenses")
    if not isinstance(expenses, dict):
        raise AdapterError("CONTEXT_INVALID", "Context schedule_c_expenses must be an object")
    if expenses.get("mileage_rate_usd") is not None or expenses.get("mileage_deduction_usd") is not None:
        raise AdapterError("CONTEXT_INVALID", "Mileage rate and deduction must remain null in version 1")

    miles = expenses.get("business_miles")
    if isinstance(miles, bool) or not isinstance(miles, (int, Decimal)):
        raise AdapterError("CONTEXT_INVALID", "Business miles must be a JSON number")
    miles_decimal = Decimal(miles)
    if not miles_decimal.is_finite() or miles_decimal < 0:
        raise AdapterError("CONTEXT_INVALID", "Business miles must be finite and nonnegative")

    return ContextSummary(
        supplied=True,
        name=path.name,
        sha256=sha256_file(path),
        mileage_status="preserved_not_calculated",
        business_miles=format(miles_decimal, "f"),
    )
