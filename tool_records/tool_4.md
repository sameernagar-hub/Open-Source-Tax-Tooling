# Tool Record: tenforty

## Status

| Field | Value |
|---|---|
| Tool slug | `tenforty` |
| Category | tax calculation / library / adjacent infrastructure |
| Record status | complete draft |
| Last updated | 07-09-2026 UTC / 07-08-2026 PDT |
| Evaluator | Codex |
| Evaluation phase | Phase 12 |

## One-Sentence Summary

tenforty is a lightweight Python library over Open Tax Solver that turns selected US federal and state tax inputs into structured tax-liability outputs, making it the strongest direct tax-calculation API candidate evaluated so far but not a bookkeeping, form-preparation, PDF, or e-file product.

## Identity

| Field | Value | Evidence |
|---|---|---|
| Primary project URL | https://github.com/mmacpherson/tenforty | [TENFORTY-REPO] |
| Source repository | https://github.com/mmacpherson/tenforty | [TENFORTY-REPO] |
| Documentation | README / PyPI project description; examples focus on `evaluate_return` and `evaluate_returns`. | [TENFORTY-README], [TENFORTY-PYPI] |
| License | MIT. | [TENFORTY-REPO], `evidence/commands/07-08-2026_tenforty_version.txt` |
| Latest visible release | `2025.10` installed from PyPI in the Linux container; GitHub releases page showed `v2025.10` as the newest visible release entry. | [TENFORTY-RELEASES], [TENFORTY-PYPI], `evidence/commands/07-08-2026_tenforty_version.txt` |
| Main implementation language | Python with Cython/OpenTaxSolver-backed native extension; repository also contains graph/backend implementation files. | [TENFORTY-REPO], `evidence/commands/07-08-2026_tenforty_setup.txt` |
| Package/distribution channel | PyPI package `tenforty`; no global install was performed. | [TENFORTY-PYPI], `evidence/commands/07-08-2026_tenforty_version.txt` |
| Maintainer or organization | Mike Macpherson / `mmacpherson`. | [TENFORTY-REPO], `evidence/commands/07-08-2026_tenforty_version.txt` |

## Research Fit

- Workflow category: Programmatic tax calculation library.
- Consumer/freelancer relevance: Good for estimating federal tax liability from summarized freelancer facts, especially self-employment income and interest income.
- US tax relevance: Stronger than the bookkeeping tools because it calculates federal tax and self-employment tax outputs.
- Non-US comparator value: Not applicable; US-focused.
- Why included: It adds the first direct tax-calculation API surface to the Week 2 comparison after three bookkeeping/personal-finance evaluations.
- Why this might be excluded later: It does not import transactions, produce complete filled tax forms, compute refunds from estimated payments, generate PDFs, or support e-file/submission.

## Programmatic Surface

| Surface | Present? | Stability | Input shape | Output shape | Evidence |
|---|---:|---|---|---|---|
| CLI | no | N/A | N/A | N/A | [TENFORTY-README] |
| Library/API import | yes | documented and tested | Python keyword arguments to `evaluate_return` and `evaluate_returns` | Pydantic-style model/dict for one return; Polars dataframe for scenario sweeps | [TENFORTY-README], `evidence/fixtures/tenforty_day12_evaluate.py` |
| REST or HTTP API | no | N/A | N/A | N/A | [TENFORTY-README] |
| Plugin or extension system | no public plugin system found | N/A | N/A | N/A | [TENFORTY-README] |
| File format or schema | partial | package-internal | Python arguments, package form JSON/model assets | Python model/dataframe output | `evidence/fixtures/tenforty_day12_summary.json` |
| Database access | no | N/A | N/A | N/A | Day 12 evaluation |
| Export format | yes through caller serialization | caller-controlled | Python model/dataframe | JSON if wrapper serializes `.model_dump()` or `.to_dicts()` | `evidence/fixtures/tenforty_day12_summary.json` |

Notes:

- Documented surfaces: `evaluate_return` for one case and `evaluate_returns` for list/grid scenario sweeps.
- Inferred surfaces: The package can be wrapped behind a small service or CLI, but that would be project code rather than a native tenforty interface.
- Missing or unclear surfaces: No official command-line interface, REST API, transaction import, refund/payment model, PDF generation, MeF/e-file, or full form object export.
- Documentation/runtime mismatch: The visible README argument table did not include `self_employment_income`, but the installed `2025.10` runtime signature did. Day 12 used `self_employment_income` because it is the best fit for the synthetic Schedule C net-income summary.

## Prior Art and Existing Integrations

- Third-party wrappers: A GPT-style interface is referenced in the README, but it was not evaluated.
- Package bindings: Native Python package; runtime uses Open Tax Solver logic under the hood.
- Plugins/extensions: None found.
- Example automation scripts: Day 12 added `evidence/fixtures/tenforty_day12_evaluate.py`.
- Related ecosystem tools: Open Tax Solver, the underlying tax-computation project; tenforty wraps it into Python. Open Tax Solver itself remains a mature text/PDF-oriented comparator.
- Evidence: [TENFORTY-README], [OTS-SF], `research/programmatic_surface_survey.md`.

## Setup and First Useful Operation

Environment:

- OS: Microsoft Windows 11 host; native Windows install attempted with Python `3.14.5`; successful evaluation ran in Docker `python:3.12-slim` on Linux/WSL2.
- Runtime/package manager: Python `3.12.13` inside container; pip; Docker `29.5.3`.
- Tool version: `tenforty 2025.10`.
- Install source: PyPI package installed in disposable Docker containers; native Windows venv attempt was isolated under `%TEMP%`.

Commands attempted:

```text
See:
- evidence/commands/07-08-2026_tenforty_setup.txt
- evidence/commands/07-08-2026_tenforty_version.txt
- evidence/commands/07-08-2026_tenforty_workflow.txt
- evidence/commands/07-08-2026_tenforty_failure-tests.txt
```

Results:

- Time to first useful operation: Moderate. Native Windows installation failed during wheel build; Docker startup and Linux package installation then produced a working run in one short session.
- First useful operation: `evaluate_return(year=2025, filing_status="Single", taxable_interest=77.75, self_employment_income=9107.02)`.
- First useful output: Federal total tax `1286.78`, all of it reported as self-employment tax, with federal AGI `8541.38`.
- Setup friction: Moderate. PyPI install works in Linux; native Windows is not supported upstream and the local build failed at the C++ build-tool/native-extension step.
- Evidence files: Listed above plus `evidence/fixtures/tenforty_day12_summary.json`, `evidence/fixtures/tenforty_day12_scenario_grid.json`, `evidence/fixtures/tenforty_day12_failure_results.json`, and `evidence/fixtures/tenforty_day12_evaluate.py`.

## Synthetic Workflow Results

For tenforty, the shared transaction CSV was intentionally summarized into tax-profile inputs instead of imported transaction-by-transaction.

| Operation | Result | Structured output? | Evidence |
|---|---|---:|---|
| Load data | Success at profile level. The helper read `synthetic_freelancer_tax_profile.json` and mapped 2025 single filing status, interest income, and Schedule C net before mileage into tenforty inputs. | yes | `evidence/fixtures/tenforty_day12_summary.json` |
| Add transaction | Partial/app-level adaptation. Applying `TADD` means re-running with Schedule C net changed from `9107.02` to `9082.03`; tenforty has no transaction store. | yes | `evidence/fixtures/tenforty_day12_summary.json` |
| List accounts | Not applicable. | N/A | Day 12 evaluation |
| Compute balance | Not applicable. | N/A | Day 12 evaluation |
| Run report | Success. Baseline federal total tax was `1286.78`; after `TADD`, federal total tax was `1283.25`, a delta of `-3.53`. | yes | `evidence/commands/07-08-2026_tenforty_workflow.txt` |
| Export result | Success through wrapper serialization of `.model_dump()` and Polars `.to_dicts()`. | yes | `evidence/fixtures/tenforty_day12_summary.json`, `evidence/fixtures/tenforty_day12_scenario_grid.json` |

Key comparable totals:

| Measure | Baseline | After `TADD` |
|---|---:|---:|
| Interest income input | `77.75` | `77.75` |
| Self-employment income input | `9107.02` | `9082.03` |
| Federal adjusted gross income | `8541.38` | `8518.16` |
| Federal taxable income | `0.00` | `0.00` |
| Federal income tax | `0.00` | `0.00` |
| Federal self-employment tax | `1286.78` | `1283.25` |
| Federal total tax | `1286.78` | `1283.25` |
| Wrapper recomputed federal effective rate from AGI | `15.0652%` | `15.0649%` |
| tenforty reported `federal_effective_tax_rate` | `128678000000000.0` | `128325000000000.0` |

Mapping assumptions:

- `self_employment_income` used Schedule C net before mileage, not gross receipts.
- Cash charitable contributions were not applied to the baseline because the profile uses the standard deduction; a separate itemized probe showed that forcing only `370.00` of itemized deductions increases tax.
- Federal estimated payments were not modeled because `evaluate_return` returns liability and does not accept payment/refund inputs.
- Business mileage was not modeled because the synthetic dataset intentionally leaves the mileage deduction unset.

## Workflow Coverage

| Capability | Coverage | Notes | Evidence |
|---|---|---|---|
| Bookkeeping | unsupported | No accounts, categories, ledgers, or transaction import. | [TENFORTY-README] |
| Reporting | strong for compact tax outputs | Returns AGI, taxable income, tax components, rates, and state fields. | `evidence/fixtures/tenforty_day12_summary.json` |
| Tax-line mapping | partial | Accepts selected high-level inputs, but not full form-line schemas. | [TENFORTY-README], `evidence/fixtures/tenforty_day12_summary.json` |
| Form 1040 | partial calculation | Outputs Form 1040-like AGI/tax fields, not filled forms. | [TENFORTY-README] |
| Schedule A | partial | `itemized_deductions` is aggregate, not line-level Schedule A detail. | `evidence/fixtures/tenforty_day12_summary.json` |
| Schedule B | partial | Interest/dividend inputs exist; no full Schedule B form output. | [TENFORTY-README] |
| Schedule C | partial | Runtime supports `self_employment_income`; Day 12 used net Schedule C-style income only. No gross/expense category input. | `evidence/fixtures/tenforty_day12_summary.json` |
| Schedule D | partial | Short-term and long-term capital gains inputs are documented, but not tested with the synthetic freelancer scenario. | [TENFORTY-README] |
| Schedule E | partial | Runtime signature includes `rental_income`, but Day 12 did not test it and no form output is exposed. | `evidence/fixtures/tenforty_day12_summary.json` |
| Common credits | partial/unclear | Dependents are accepted, but Day 12 did not validate child/dependent credit behavior. | `evidence/fixtures/tenforty_day12_summary.json` |
| Tax form generation | unsupported | No PDF or complete form generation exposed by tenforty. | [TENFORTY-README] |
| Tax-year support | strong within scope | Documented and validated years are 2018-2025. | [TENFORTY-README], `evidence/fixtures/tenforty_day12_failure_results.json` |
| E-file or submission path | unsupported | No MeF/e-file workflow. | [TENFORTY-README] |
| Import from banks/files | unsupported | Use another tool to summarize transactions first. | Day 12 evaluation |
| Export for other systems | strong if wrapped | Pydantic model and Polars dataframe serialize cleanly to JSON. | `evidence/fixtures/tenforty_day12_summary.json` |

Stated non-goals and exclusions:

- State returns: Supports selected states only; Day 12 tested federal-only. Unsupported Colorado produced `OTS does not support 2025/CO_Form104`.
- Foreign filers: Not evaluated.
- Business returns: Unsupported; only individual-return-style inputs were considered.
- Production filing: Unsupported.
- Other: Upstream states the package is informational/educational and does not provide tax advice.

## Safety and Failure Behavior

| Area | Finding | Evidence |
|---|---|---|
| Dry-run or validation mode | Function calls are pure calculation-style calls with no persistent state; no separate dry-run needed for tested workflow. | `evidence/fixtures/tenforty_day12_evaluate.py` |
| Scratch/test data support | Excellent in Linux containers because calls are local and stateless. | `evidence/commands/07-08-2026_tenforty_workflow.txt` |
| Destructive operations | None in the tested workflow. | Day 12 evaluation |
| Bad date handling | Not applicable; no date inputs in evaluated API. | Day 12 evaluation |
| Invalid amount handling | Rejected string `not-a-number` for `self_employment_income` with a Pydantic validation error. | `evidence/fixtures/tenforty_day12_failure_results.json` |
| Unknown account/category handling | Not applicable; no accounts/categories. | Day 12 evaluation |
| Missing file handling | The Day 12 wrapper reported missing profile file as `FileNotFoundError`; this is wrapper behavior, not tenforty core behavior. | `evidence/fixtures/tenforty_day12_failure_results.json` |
| Unsupported filing status/year/state | Invalid filing status and unsupported year returned clear validation errors; unsupported state returned a direct OTS support error. | `evidence/fixtures/tenforty_day12_failure_results.json` |
| Negative income handling | `self_employment_income=-100.0` was accepted and produced negative AGI. A production wrapper should guard against unintended negative inputs. | `evidence/fixtures/tenforty_day12_failure_results.json` |
| Error clarity | Strong for enum/type validation, moderate for unsupported state, and weak for domain validation around negative self-employment income. | `evidence/commands/07-08-2026_tenforty_failure-tests.txt` |
| Output sanity | `federal_effective_tax_rate` for the baseline did not match the documented meaning. Wrapper recomputation from AGI gave about `15.0652%`, while tenforty reported `128678000000000.0`. | `evidence/fixtures/tenforty_day12_summary.json` |

## Project Health

| Signal | Finding | Evidence |
|---|---|---|
| Recent commits | Prior Day 5 snapshot found active release activity; current GitHub page showed a small but live project footprint. | `research/project_health_snapshot.md`, [TENFORTY-REPO] |
| Release cadence | PyPI/package version `2025.10` installed successfully; GitHub releases page showed `v2025.10` and prior 2025 OTS upgrades. | [TENFORTY-RELEASES], `evidence/commands/07-08-2026_tenforty_version.txt` |
| Annual tax-year support pattern | Strong within 2018-2025; release/versioning tracks tax-year support and Open Tax Solver updates. | [TENFORTY-README], [TENFORTY-RELEASES] |
| Issue/PR activity | Not deeply evaluated on Day 12; project is smaller than hledger/Actual/Firefly. | `research/project_health_snapshot.md` |
| Contributor signals | Small public footprint but practical docs, releases, package metadata, and test/validation references. | [TENFORTY-README], [TENFORTY-PYPI] |
| Documentation quality | Good for basic use and limitations, but Day 12 found the installed runtime signature had an important argument missing from the visible README table. | [TENFORTY-README], `evidence/fixtures/tenforty_day12_summary.json` |
| Data format durability | Moderate. Inputs are stable-looking function arguments, but not a formal tax-form schema. | [TENFORTY-README] |
| License constraints | MIT is integration-friendly; underlying Open Tax Solver is GPLv2, so redistribution/combined-work implications need separate review. | [TENFORTY-REPO], [OTS-SF] |

## Integration Assessment

- Best integration shape: Python library adapter that accepts a normalized tax profile, validates domains, calls `evaluate_return` or `evaluate_returns`, recomputes/sanity-checks key rates, and serializes a normalized JSON result.
- Thin-wrapper feasibility: High in Linux/WSL/Docker; low for native Windows without build-tool and compatibility work.
- Structured I/O quality: Excellent for selected tax inputs and outputs; much better than text/PDF scraping.
- Agent-consumable workflow fit: Strong for tax-liability "what if" scenarios, scenario sweeps, and explaining sensitivity to income/deductions.
- Main blockers: No transaction import, no full form/PDF/e-file workflow, native Windows unsupported, aggregate rather than line-level inputs, missing estimated-payment/refund handling, and the suspicious effective-rate field.
- Best demo idea: Synthetic tax-profile calculator that consumes summaries from hledger/Actual/Firefly, calls tenforty for federal liability, and returns normalized JSON with guardrails and explicit unmapped fields.
- Prototype suitability: High as a tax-calculation component; lower as a standalone final prototype because it needs a bookkeeping/summarization layer before it.

## Scores

| Criterion | Score | Rationale |
|---|---:|---|
| Relevance to research question | 5 | Direct tax calculation and Python API surface, unlike the first three bookkeeping candidates. |
| Programmatic surface quality | 5 | Simple Python functions, typed/validated inputs, model/dataframe outputs. |
| Setup feasibility | 3 | Linux container worked cleanly; native Windows install failed and upstream documents Windows as unsupported. |
| Structured input/output | 5 | Pydantic-style model and Polars dataframe are easy to serialize. |
| Workflow coverage | 3 | Strong calculation core but no transaction import, complete forms, payments/refund model, PDFs, or e-file. |
| Safety and failure clarity | 4 | Good validation for enums/types/years; wrapper needed for negative inputs and suspicious output-field sanity checks. |
| Project health | 4 | Current tax-year package and practical docs, but smaller footprint and narrower validation than mature bookkeeping projects. |
| Prototype/demo potential | 4 | Excellent tax-calculation component, especially paired with a bookkeeping adapter; less suitable as the only prototype surface. |

## Evidence Index

- [x] Official project page: [TENFORTY-REPO] https://github.com/mmacpherson/tenforty
- [x] Source repository: [TENFORTY-REPO] https://github.com/mmacpherson/tenforty
- [x] License: [TENFORTY-REPO] https://github.com/mmacpherson/tenforty, `evidence/commands/07-08-2026_tenforty_version.txt`
- [x] Release/version: [TENFORTY-PYPI] https://pypi.org/project/tenforty/, [TENFORTY-RELEASES] https://github.com/mmacpherson/tenforty/releases, `evidence/commands/07-08-2026_tenforty_version.txt`
- [x] Documentation: [TENFORTY-README] https://raw.githubusercontent.com/mmacpherson/tenforty/main/README.md
- [x] Command output: `evidence/commands/07-08-2026_tenforty_setup.txt`, `evidence/commands/07-08-2026_tenforty_version.txt`, `evidence/commands/07-08-2026_tenforty_workflow.txt`, `evidence/commands/07-08-2026_tenforty_failure-tests.txt`
- [x] Metadata snapshot: `research/project_health_snapshot.md`, `research/programmatic_surface_survey.md`
- [ ] Screenshots, if any: Not needed for Python-library-only Day 12 evaluation.

## Open Questions

- Is the `federal_effective_tax_rate` output issue limited to SE-tax-only, zero-taxable-income cases, or broader?
- Should the final prototype pair hledger or Actual with tenforty so bookkeeping summaries feed a real tax-calculation step?
- How should a wrapper expose unmapped facts such as estimated tax payments, charity under standard deduction, and mileage?
- Does the hidden/runtime `self_employment_income` argument need upstream documentation clarification before relying on it?
- What are the practical license implications of distributing tenforty together with its Open Tax Solver-derived native extension?

## Decision Notes

tenforty should remain the leading tax-calculation component candidate. It fills the largest gap left by hledger, Actual Budget, and Firefly III: those tools can organize tax-relevant transactions, while tenforty can calculate a federal liability from summarized tax facts. The best final architecture may be a two-stage adapter: bookkeeping tool for controlled category summaries, then tenforty for tax calculation with validation and output sanity checks.

[TENFORTY-REPO]: https://github.com/mmacpherson/tenforty
[TENFORTY-README]: https://raw.githubusercontent.com/mmacpherson/tenforty/main/README.md
[TENFORTY-PYPI]: https://pypi.org/project/tenforty/
[TENFORTY-RELEASES]: https://github.com/mmacpherson/tenforty/releases
[OTS-SF]: https://sourceforge.net/projects/opentaxsolver/
