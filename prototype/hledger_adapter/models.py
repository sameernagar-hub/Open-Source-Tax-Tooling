from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class CategoryRule:
    account: str
    summary_bucket: str
    summary_key: str
    expected_source_sign: str
    allowed_tax_hints: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CategoryMap:
    schema_version: str
    dataset_id: str
    tax_year: int
    currency: str
    synthetic_only: bool
    primary_account: str
    tested_hledger_version: str
    max_input_rows: int
    max_input_bytes: int
    max_abs_amount_usd: Decimal
    subprocess_timeout_seconds: int
    max_subprocess_output_bytes: int
    categories: dict[str, CategoryRule]
    path: Path
    sha256: str


@dataclass(frozen=True, slots=True)
class InputFileSummary:
    name: str
    sha256: str
    bytes: int
    rows: int


@dataclass(frozen=True, slots=True)
class SourceTransaction:
    transaction_id: str
    date: str
    payee: str
    description: str
    source_account: str
    category: str
    tax_hint: str
    amount_usd: Decimal
    cleared: bool
    memo: str


@dataclass(frozen=True, slots=True)
class LoadedTransactions:
    files: tuple[InputFileSummary, ...]
    row_count: int
    transaction_ids: tuple[str, ...]
    records: tuple[SourceTransaction, ...]


@dataclass(frozen=True, slots=True)
class ContextSummary:
    supplied: bool
    name: str | None
    sha256: str | None
    mileage_status: str
    business_miles: str | None


@dataclass(frozen=True, slots=True)
class HledgerBinary:
    path: Path
    source: str


@dataclass(frozen=True, slots=True)
class HledgerVersion:
    full_text: str
    parsed_version: str | None
    tested_version_match: bool


@dataclass(frozen=True, slots=True)
class EngineReports:
    print_json: Any
    balance_json: Any
    income_statement_json: Any
    rules_sha256: str
    scratch_kept: bool
    scratch_path: str | None
    operations: tuple[str, ...]
