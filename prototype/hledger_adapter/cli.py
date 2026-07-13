from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .errors import AdapterError, EXIT_INTERNAL
from .hledger import probe_version, resolve_hledger_binary, run_engine_reports
from .normalize import normalize_transactions_and_accounts
from .summary import build_financial_summary
from .validation import load_category_map, load_context, load_transactions, sha256_file


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROTOTYPE_ROOT.parent
CONFIG_DIR = PROTOTYPE_ROOT / "config"
CATEGORY_MAP_PATH = CONFIG_DIR / "category_map.json"
RULES_PATH = CONFIG_DIR / "hledger.csv.rules"
DEFAULT_TRANSACTIONS = REPO_ROOT / "evidence" / "fixtures" / "synthetic_freelancer_transactions.csv"
DEFAULT_CONTEXT = REPO_ROOT / "evidence" / "fixtures" / "synthetic_freelancer_tax_profile.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m hledger_adapter",
        description="Synthetic-only hledger adapter prototype.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Load config and validate synthetic CSV/context inputs.")
    validate.add_argument("--transactions", action="append", required=True, help="Synthetic transaction CSV path. Repeatable.")
    validate.add_argument("--context", help="Optional synthetic context JSON path.")
    validate.add_argument("--confirm-synthetic", action="store_true", help="Acknowledge that custom inputs are synthetic only.")
    validate.set_defaults(handler=_handle_validate)

    smoke = subparsers.add_parser("smoke", help="Run the read-only hledger transaction/account reconciliation call.")
    smoke.add_argument("--transactions", action="append", help="Synthetic transaction CSV path. Repeatable.")
    smoke.add_argument("--context", help="Optional synthetic context JSON path.")
    smoke.add_argument("--hledger-bin", help="Path to a local hledger executable.")
    smoke.add_argument("--keep-scratch", action="store_true", help="Keep scratch files under prototype/.scratch/.")
    smoke.add_argument("--confirm-synthetic", action="store_true", help="Acknowledge that custom inputs are synthetic only.")
    smoke.set_defaults(handler=_handle_smoke)

    demo = subparsers.add_parser("demo", help="Run the canonical synthetic end-to-end summary.")
    demo.add_argument("--hledger-bin", help="Path to a local hledger executable.")
    demo.add_argument("--keep-scratch", action="store_true", help="Keep scratch files under prototype/.scratch/.")
    demo.set_defaults(handler=_handle_demo)

    summarize = subparsers.add_parser("summarize", help="Run the synthetic financial summary command.")
    summarize.add_argument("--transactions", action="append", required=True, help="Synthetic transaction CSV path. Repeatable.")
    summarize.add_argument("--context", help="Optional synthetic context JSON path.")
    summarize.add_argument("--hledger-bin", help="Path to a local hledger executable.")
    summarize.add_argument("--dry-run", action="store_true", help="Validate and emit the planned execution without running hledger.")
    summarize.add_argument("--keep-scratch", action="store_true", help="Keep scratch files under prototype/.scratch/.")
    summarize.add_argument("--confirm-synthetic", action="store_true", help="Acknowledge that custom inputs are synthetic only.")
    summarize.set_defaults(handler=_handle_summarize)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = args.handler(args)
    except AdapterError as exc:
        print(json.dumps(exc.to_payload(), indent=2, sort_keys=True), file=sys.stderr)
        return exc.exit_code
    except Exception as exc:
        payload = {
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc),
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True), file=sys.stderr)
        return EXIT_INTERNAL

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _handle_validate(args: argparse.Namespace) -> dict[str, Any]:
    _require_custom_ack(args.confirm_synthetic)
    return _load_and_describe(
        transaction_paths=[Path(value) for value in args.transactions],
        context_path=Path(args.context) if args.context else None,
        command="validate",
    )


def _handle_smoke(args: argparse.Namespace) -> dict[str, Any]:
    custom_inputs = bool(args.transactions or args.context)
    if custom_inputs:
        _require_custom_ack(args.confirm_synthetic)
    transaction_paths = [Path(value) for value in args.transactions] if args.transactions else [DEFAULT_TRANSACTIONS]
    context_path = Path(args.context) if args.context else DEFAULT_CONTEXT
    return _run_smoke(
        transaction_paths=transaction_paths,
        context_path=context_path,
        hledger_bin=args.hledger_bin,
        keep_scratch=args.keep_scratch,
        command="smoke",
        custom_inputs=custom_inputs,
    )


def _handle_demo(args: argparse.Namespace) -> dict[str, Any]:
    return _run_summary(
        transaction_paths=[DEFAULT_TRANSACTIONS],
        context_path=DEFAULT_CONTEXT,
        hledger_bin=args.hledger_bin,
        keep_scratch=args.keep_scratch,
        command="demo",
        custom_inputs=False,
    )


def _handle_summarize(args: argparse.Namespace) -> dict[str, Any]:
    _require_custom_ack(args.confirm_synthetic)
    if args.dry_run:
        if args.keep_scratch:
            raise AdapterError(
                "DRY_RUN_OPTION_CONFLICT",
                "Dry-run mode does not create scratch files, so --keep-scratch is not supported.",
            )
        return _run_summary_dry_run(args)
    return _run_summary(
        transaction_paths=[Path(value) for value in args.transactions],
        context_path=Path(args.context) if args.context else None,
        hledger_bin=args.hledger_bin,
        keep_scratch=args.keep_scratch,
        command="summarize",
        custom_inputs=True,
    )


def _run_summary_dry_run(args: argparse.Namespace) -> dict[str, Any]:
    category_map = load_category_map(CATEGORY_MAP_PATH)
    transaction_paths = [Path(value) for value in args.transactions]
    transactions = load_transactions(transaction_paths, category_map)
    context = load_context(Path(args.context) if args.context else None, category_map)
    binary = resolve_hledger_binary(args.hledger_bin)
    return {
        "schema_version": "1.0.0",
        "status": "ok",
        "command": "summarize",
        "mode": "dry_run",
        "adapter": _adapter_payload(),
        "dataset": _dataset_payload(category_map),
        "inputs": _input_payload(transactions),
        "context": _context_payload(context),
        "planned_operations": [
            "probe hledger --version",
            "copy validated inputs and static rules to scratch",
            "run hledger print -O json",
            "run hledger balance --flat -O json",
            "run hledger incomestatement --depth 3 -O json",
            "normalize transactions, accounts, balances, and summary buckets",
        ],
        "hledger": {
            "source": binary.source,
            "executable_name": binary.path.name,
            "version": None,
        },
        "config": _config_payload(category_map),
    }


def _run_summary(
    transaction_paths: list[Path],
    context_path: Path | None,
    hledger_bin: str | None,
    keep_scratch: bool,
    command: str,
    custom_inputs: bool,
) -> dict[str, Any]:
    category_map = load_category_map(CATEGORY_MAP_PATH)
    transactions = load_transactions(transaction_paths, category_map)
    context = load_context(context_path, category_map)
    binary = resolve_hledger_binary(hledger_bin)
    version = probe_version(binary, category_map)
    reports = run_engine_reports(
        binary=binary,
        transaction_paths=transaction_paths,
        rules_path=RULES_PATH,
        category_map=category_map,
        keep_scratch=keep_scratch,
        prototype_root=PROTOTYPE_ROOT,
    )
    normalized = normalize_transactions_and_accounts(reports, transactions, category_map)
    financial = build_financial_summary(normalized, reports, category_map, context)
    warnings = list(financial["warnings"])
    if not version.tested_version_match:
        warnings.append(
            {
                "code": "UNTESTED_HLEDGER_VERSION",
                "message": "hledger version differs from the tested 1.52.1 baseline.",
            }
        )
    if custom_inputs:
        warnings.append(
            {
                "code": "CUSTOM_SYNTHETIC_INPUTS_ACKNOWLEDGED",
                "message": "Caller acknowledged that supplied inputs are synthetic only.",
            }
        )
    return {
        "schema_version": "1.0.0",
        "status": "ok",
        "command": command,
        "mode": "executed",
        "adapter": _adapter_payload(),
        "dataset": _dataset_payload(category_map),
        "counts": normalized["counts"],
        "transactions": normalized["transactions"],
        "accounts": normalized["accounts"],
        "summary": financial["summary"],
        "unmapped_tax_facts": financial["unmapped_tax_facts"],
        "reconciliation": normalized["reconciliation"],
        "unsupported_capabilities": financial["unsupported_capabilities"],
        "inputs": _input_payload(transactions),
        "context": _context_payload(context),
        "hledger": {
            "source": binary.source,
            "executable_name": binary.path.name,
            "version": version.full_text,
            "parsed_version": version.parsed_version,
            "tested_version": category_map.tested_hledger_version,
            "tested_version_match": version.tested_version_match,
        },
        "config": _config_payload(category_map),
        "engine_reports": {
            "operations": list(reports.operations),
            "rules_sha256": reports.rules_sha256,
            "scratch": {
                "kept": reports.scratch_kept,
                "path": reports.scratch_path,
            },
        },
        "provenance": _provenance_payload(transactions, context, category_map, reports),
        "warnings": warnings,
        "limitations": [
            "Synthetic bookkeeping summary only; real taxpayer data is unsupported.",
            "Tax-adjacent labels are controlled mappings, not tax-treatment decisions.",
            "Mileage is preserved from context and no mileage deduction is calculated.",
        ],
    }


def _run_smoke(
    transaction_paths: list[Path],
    context_path: Path,
    hledger_bin: str | None,
    keep_scratch: bool,
    command: str,
    custom_inputs: bool,
) -> dict[str, Any]:
    category_map = load_category_map(CATEGORY_MAP_PATH)
    transactions = load_transactions(transaction_paths, category_map)
    context = load_context(context_path, category_map)
    binary = resolve_hledger_binary(hledger_bin)
    version = probe_version(binary, category_map)
    reports = run_engine_reports(
        binary=binary,
        transaction_paths=transaction_paths,
        rules_path=RULES_PATH,
        category_map=category_map,
        keep_scratch=keep_scratch,
        prototype_root=PROTOTYPE_ROOT,
    )
    normalized = normalize_transactions_and_accounts(reports, transactions, category_map)
    warnings = []
    if not version.tested_version_match:
        warnings.append("UNTESTED_HLEDGER_VERSION")
    if custom_inputs:
        warnings.append("CUSTOM_SYNTHETIC_INPUTS_ACKNOWLEDGED")
    return {
        "status": "ok",
        "command": command,
        "mode": "executed",
        "adapter_version": __version__,
        "dataset": _dataset_payload(category_map),
        "counts": normalized["counts"],
        "transactions": normalized["transactions"],
        "accounts": normalized["accounts"],
        "reconciliation": normalized["reconciliation"],
        "inputs": _input_payload(transactions),
        "context": _context_payload(context),
        "hledger": {
            "source": binary.source,
            "executable_name": binary.path.name,
            "version": version.full_text,
            "parsed_version": version.parsed_version,
            "tested_version": category_map.tested_hledger_version,
            "tested_version_match": version.tested_version_match,
        },
        "config": _config_payload(category_map),
        "engine_reports": {
            "operations": list(reports.operations),
            "rules_sha256": reports.rules_sha256,
            "scratch": {
                "kept": reports.scratch_kept,
                "path": reports.scratch_path,
            },
        },
        "warnings": warnings,
        "limitations": [
            "Smoke output normalizes transactions and accounts only.",
            "Use summarize or demo for Day 18 tax-adjacent summary totals.",
        ],
    }


def _load_and_describe(transaction_paths: list[Path], context_path: Path | None, command: str) -> dict[str, Any]:
    category_map = load_category_map(CATEGORY_MAP_PATH)
    transactions = load_transactions(transaction_paths, category_map)
    context = load_context(context_path, category_map)
    return {
        "status": "ok",
        "command": command,
        "adapter_version": __version__,
        "dataset": _dataset_payload(category_map),
        "inputs": _input_payload(transactions),
        "context": _context_payload(context),
        "config": _config_payload(category_map),
    }


def _require_custom_ack(confirmed: bool) -> None:
    if not confirmed:
        raise AdapterError(
            "SYNTHETIC_CONFIRMATION_REQUIRED",
            "Custom runs require --confirm-synthetic because real taxpayer data is unsupported.",
        )


def _dataset_payload(category_map: Any) -> dict[str, Any]:
    return {
        "id": category_map.dataset_id,
        "tax_year": category_map.tax_year,
        "currency": category_map.currency,
        "synthetic_only": category_map.synthetic_only,
        "synthetic_data_acknowledged": True,
    }


def _adapter_payload() -> dict[str, str]:
    return {
        "name": "hledger_adapter",
        "version": __version__,
    }


def _input_payload(transactions: Any) -> list[dict[str, Any]]:
    return [
        {
            "name": item.name,
            "rows": item.rows,
            "bytes": item.bytes,
            "sha256": item.sha256,
        }
        for item in transactions.files
    ]


def _context_payload(context: Any) -> dict[str, Any]:
    return {
        "supplied": context.supplied,
        "name": context.name,
        "sha256": context.sha256,
        "mileage_status": context.mileage_status,
        "business_miles": context.business_miles,
    }


def _config_payload(category_map: Any) -> dict[str, Any]:
    return {
        "category_map_sha256": category_map.sha256,
        "rules_sha256": sha256_file(RULES_PATH),
        "category_count": len(category_map.categories),
    }


def _provenance_payload(transactions: Any, context: Any, category_map: Any, reports: Any) -> dict[str, Any]:
    context_payload = {
        "supplied": context.supplied,
        "name": context.name,
        "sha256": context.sha256,
    }
    return {
        "inputs": _input_payload(transactions),
        "context": context_payload,
        "mapping_sha256": category_map.sha256,
        "rules_sha256": reports.rules_sha256,
        "engine_operations": list(reports.operations),
    }
