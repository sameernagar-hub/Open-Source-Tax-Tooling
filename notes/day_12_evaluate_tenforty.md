# Day 12 Evaluate Tool 4: tenforty

Planned phase date: 07-12-2026. Executed early on 07-09-2026 UTC / 07-08-2026 PDT at user request.

## Goal

Evaluate tenforty as the fourth Week 2 hands-on tool and the first direct tax-calculation library candidate, using the shared synthetic freelancer tax profile rather than transaction-level bookkeeping imports.

## What I Did

- Verified current tenforty package metadata from PyPI/GitHub and installed `tenforty==2025.10`.
- Attempted a native Windows venv install with Python `3.14.5`; installation failed while building the native extension and reported missing Microsoft C++ Build Tools.
- Started Docker Desktop and completed the evaluation in a disposable `python:3.12-slim` Linux container.
- Added `evidence/fixtures/tenforty_day12_evaluate.py` to map the canonical synthetic tax profile into tenforty function calls.
- Used `self_employment_income` for Schedule C net before mileage, `taxable_interest` for bank interest, and standard deduction for the baseline.
- Re-ran the calculation after applying the standard `TADD` software expense as a reduced Schedule C net-income value.
- Exported normalized JSON for the baseline, after-add case, itemized-charity probe, scenario grid, and failure tests.
- Created the completed fourth tool record at `tool_records/tool_4.md`.

## Evidence Captured

- `tool_records/tool_4.md`
- `notes/day_12_evaluate_tenforty.md`
- `evidence/commands/07-08-2026_tenforty_setup.txt`
- `evidence/commands/07-08-2026_tenforty_version.txt`
- `evidence/commands/07-08-2026_tenforty_workflow.txt`
- `evidence/commands/07-08-2026_tenforty_failure-tests.txt`
- `evidence/fixtures/tenforty_day12_evaluate.py`
- `evidence/fixtures/tenforty_day12_summary.json`
- `evidence/fixtures/tenforty_day12_scenario_grid.json`
- `evidence/fixtures/tenforty_day12_failure_results.json`

## Decisions Made

- Treat tenforty as the leading tax-calculation component candidate, not as a standalone bookkeeping or filing tool.
- Keep the baseline federal-only and standard-deduction-based because the synthetic charity amount is lower than the standard deduction and the profile intentionally leaves mileage unset.
- Model `TADD` by reducing Schedule C net income and re-running the calculation, because tenforty has no transaction store.
- Require a wrapper-side validation layer for negative income/domain assumptions and for recomputing suspicious output fields.
- Consider a two-stage prototype where hledger, Actual, or Firefly produces controlled tax summaries and tenforty performs the tax calculation.

## Problems / Open Questions

- Native Windows is a real portability blocker; upstream also documents Windows as unsupported.
- The README argument table omits the runtime `self_employment_income` argument found in the installed `2025.10` function signature.
- `federal_effective_tax_rate` looked wrong in the SE-tax-only baseline: tenforty reported `128678000000000.0`, while a wrapper recomputation from federal total tax over AGI gave about `15.0652%`.
- Federal estimated payments, refund/amount-due, mileage deduction, and full transaction details are not modeled by `evaluate_return`.
- Negative `self_employment_income` was accepted, so a production wrapper should enforce domain rules.

## Tomorrow's Starting Point

Execute Day 13 by either evaluating Filed Open Tax Engine as the fifth tax-specific CLI/JSON candidate or closing gaps across the four completed records before Day 14 prototype target selection.
