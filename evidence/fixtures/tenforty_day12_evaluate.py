import argparse
import importlib.metadata
import inspect
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from tenforty import evaluate_return, evaluate_returns


DEFAULT_PROFILE = Path("evidence/fixtures/synthetic_freelancer_tax_profile.json")
OUT_DIR = Path("evidence/fixtures")


def round_money(value):
    return round(float(value), 2)


def load_profile(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def single_filing_status(value):
    mapping = {
        "single": "Single",
        "married_joint": "Married/Joint",
        "head_of_household": "Head_of_House",
        "married_separate": "Married/Sep",
        "widow": "Widow(er)",
    }
    return mapping.get(value, value)


def build_inputs(profile, schedule_c_net):
    return {
        "year": int(profile["tax_year"]),
        "state": None,
        "filing_status": single_filing_status(profile["filer"]["filing_status"]),
        "num_dependents": int(profile["filer"]["dependents"]),
        "standard_or_itemized": "Standard",
        "w2_income": round_money(profile["income"]["w2_wages"]),
        "taxable_interest": round_money(profile["income"]["interest_income"]),
        "self_employment_income": round_money(schedule_c_net),
    }


def evaluate_case(label, inputs):
    result = evaluate_return(**inputs).model_dump()
    agi = float(result["federal_adjusted_gross_income"])
    total_tax = float(result["federal_total_tax"])
    recomputed_effective_rate = None
    if agi:
        recomputed_effective_rate = round((total_tax / agi) * 100, 4)

    reported_effective_rate = result.get("federal_effective_tax_rate")
    reported_matches_recomputed = None
    if reported_effective_rate is not None and recomputed_effective_rate is not None:
        reported_matches_recomputed = abs(float(reported_effective_rate) - recomputed_effective_rate) < 0.1

    return {
        "label": label,
        "inputs": inputs,
        "outputs": result,
        "sanity_checks": {
            "recomputed_federal_effective_tax_rate_from_agi": recomputed_effective_rate,
            "reported_effective_rate_matches_recomputed": reported_matches_recomputed,
        },
    }


def compact_result(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "to_dicts"):
        return value.to_dicts()
    return str(value)


def run_failure_test(name, fn):
    try:
        result = fn()
        return {
            "name": name,
            "accepted": True,
            "result": compact_result(result),
        }
    except Exception as error:
        return {
            "name": name,
            "accepted": False,
            "errorType": type(error).__name__,
            "message": str(error),
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    args = parser.parse_args()

    profile = load_profile(args.profile)
    baseline_net = profile["expected_ledger_totals"]["schedule_c_net_before_mileage"]
    after_add_net = profile["standard_add_transaction_test"][
        "expected_schedule_c_net_before_mileage_after_add"
    ]

    baseline_inputs = build_inputs(profile, baseline_net)
    after_add_inputs = build_inputs(profile, after_add_net)
    itemized_probe_inputs = {
        **baseline_inputs,
        "standard_or_itemized": "Itemized",
        "itemized_deductions": round_money(
            profile["deductions_and_payments"]["cash_charitable_contributions"]
        ),
    }

    baseline = evaluate_case("baseline_standard_deduction", baseline_inputs)
    after_add = evaluate_case("after_tadd_standard_deduction", after_add_inputs)
    itemized_probe = evaluate_case("charity_itemized_probe", itemized_probe_inputs)

    grid = evaluate_returns(
        year=profile["tax_year"],
        filing_status=single_filing_status(profile["filer"]["filing_status"]),
        taxable_interest=round_money(profile["income"]["interest_income"]),
        self_employment_income=[baseline_net, after_add_net, 0, 15000],
    )

    failure_tests = [
        run_failure_test(
            "invalid_filing_status",
            lambda: evaluate_return(**{**baseline_inputs, "filing_status": "Singlee"}),
        ),
        run_failure_test(
            "unsupported_year",
            lambda: evaluate_return(**{**baseline_inputs, "year": 2026}),
        ),
        run_failure_test(
            "unsupported_state",
            lambda: evaluate_return(**{**baseline_inputs, "state": "CO"}),
        ),
        run_failure_test(
            "invalid_amount_type",
            lambda: evaluate_return(
                **{**baseline_inputs, "self_employment_income": "not-a-number"}
            ),
        ),
        run_failure_test(
            "negative_self_employment_income",
            lambda: evaluate_return(**{**baseline_inputs, "self_employment_income": -100.0}),
        ),
        run_failure_test(
            "missing_profile_file",
            lambda: load_profile(Path("evidence/fixtures/does_not_exist.csv")),
        ),
    ]

    tax_delta = round_money(
        after_add["outputs"]["federal_total_tax"] - baseline["outputs"]["federal_total_tax"]
    )

    summary = {
        "evaluatedAt": datetime.now(timezone.utc).isoformat(),
        "package": {
            "name": "tenforty",
            "version": importlib.metadata.version("tenforty"),
            "evaluate_return_signature": str(inspect.signature(evaluate_return)),
            "evaluate_returns_signature": str(inspect.signature(evaluate_returns)),
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "dataset": {
            "dataset_id": profile["dataset_id"],
            "tax_year": profile["tax_year"],
            "privacy": profile["privacy"],
            "input_profile": str(args.profile),
        },
        "mapping_assumptions": {
            "self_employment_income": (
                "Mapped from Schedule C net before mileage, not gross receipts. "
                "Cash expense categories are summarized before calling tenforty."
            ),
            "taxable_interest": "Mapped directly from the synthetic interest-income total.",
            "cash_charitable_contributions": (
                "Not applied to the baseline because the profile uses the standard deduction; "
                "evaluated separately as an itemized-deduction probe."
            ),
            "federal_estimated_tax_payments": (
                "Not modeled because tenforty returns tax liability and does not accept "
                "estimated-payment inputs in evaluate_return."
            ),
            "business_mileage": (
                "Not modeled because the synthetic profile intentionally leaves the mileage "
                "deduction unset."
            ),
            "state": "Federal-only profile, so state=None.",
        },
        "baseline": baseline,
        "afterAdd": after_add,
        "itemizedProbe": itemized_probe,
        "comparison": {
            "baseline_federal_total_tax": baseline["outputs"]["federal_total_tax"],
            "after_add_federal_total_tax": after_add["outputs"]["federal_total_tax"],
            "federal_total_tax_delta_after_tadd": tax_delta,
            "baseline_reported_effective_rate_warning": (
                baseline["sanity_checks"]["reported_effective_rate_matches_recomputed"] is False
            ),
        },
        "scenarioGrid": grid.to_dicts(),
        "failureTests": failure_tests,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = OUT_DIR / "tenforty_day12_summary.json"
    grid_path = OUT_DIR / "tenforty_day12_scenario_grid.json"
    failure_path = OUT_DIR / "tenforty_day12_failure_results.json"

    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    grid_path.write_text(json.dumps(summary["scenarioGrid"], indent=2) + "\n", encoding="utf-8")
    failure_path.write_text(json.dumps(failure_tests, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "packageVersion": summary["package"]["version"],
                "baselineFederalTotalTax": summary["comparison"]["baseline_federal_total_tax"],
                "afterAddFederalTotalTax": summary["comparison"]["after_add_federal_total_tax"],
                "federalTotalTaxDeltaAfterTadd": summary["comparison"][
                    "federal_total_tax_delta_after_tadd"
                ],
                "baselineEffectiveRateWarning": summary["comparison"][
                    "baseline_reported_effective_rate_warning"
                ],
                "failureTests": failure_tests,
                "summaryPath": str(summary_path),
                "gridPath": str(grid_path),
                "failurePath": str(failure_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
