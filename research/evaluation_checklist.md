# Evaluation Checklist

Day 8 artifact for Phase 8: Evaluation Harness and Synthetic Data.

Planned phase date: 07-08-2026. Executed on 07-07-2026 at user request.

## Purpose

Use this checklist during Week 2 hands-on evaluations so each shortlisted tool is tested against the same synthetic facts, core operations, safety checks, and evidence expectations.

Shortlisted tools from Day 7:

1. hledger
2. Actual Budget
3. Firefly III
4. tenforty
5. Filed Open Tax Engine

Shared dataset:

- Dataset brief: `evidence/synthetic_dataset.md`
- Transaction fixture: `evidence/fixtures/synthetic_freelancer_transactions.csv`
- Tax profile fixture: `evidence/fixtures/synthetic_freelancer_tax_profile.json`

## Evaluation Ground Rules

- Use synthetic data only.
- Use isolated local files, scratch directories, test databases, temporary containers, or local-only servers.
- Capture the tool version before exercising behavior.
- Prefer official docs, official packages, and documented APIs over inferred internals.
- Record every manual mapping from dataset fields to tool-specific fields.
- Preserve raw command output when it supports a setup, version, behavior, or failure claim.
- Treat setup friction as an evaluation finding, not as a reason to hide skipped work.

## Required Evidence Files

Use the tool slug in filenames.

| Evidence type | Suggested path |
|---|---|
| Setup transcript | `evidence/commands/MM-DD-YYYY_TOOL_setup.txt` |
| Version check | `evidence/commands/MM-DD-YYYY_TOOL_version.txt` |
| Common workflow transcript | `evidence/commands/MM-DD-YYYY_TOOL_workflow.txt` |
| Failure behavior transcript | `evidence/commands/MM-DD-YYYY_TOOL_failure-tests.txt` |
| Screenshots, if useful | `evidence/screenshots/MM-DD-YYYY_TOOL_DESCRIPTION.png` |
| Completed tool record | `tool_records/TOOL.md` |

## Setup Checklist

| Check | Result | Evidence |
|---|---|---|
| Confirm install path or run path. |  |  |
| Capture OS, shell, runtime, package manager, and install source. |  |  |
| Capture tool version or commit. |  |  |
| Identify license and any network/server implications. |  |  |
| Confirm whether the tool can run fully local for this evaluation. |  |  |
| Create or identify scratch workspace, test budget, test database, or temp files. |  |  |
| Confirm no real accounts, credentials, taxpayer data, or secrets are used. |  |  |

## Common Workflow Checklist

Every shortlisted tool should attempt the closest equivalent of these operations. Mark an operation as `not applicable` only when the tool's scope clearly does not support it.

| Operation | Minimum expected attempt | Success signal | Evidence |
|---|---|---|---|
| Load data | Import the baseline CSV, convert it to native entries, or enter the tax profile fixture. | Tool accepts or stores the baseline facts. |  |
| Add transaction | Add the standard `TADD` software transaction or equivalent. | Expected balance/net changes can be observed or computed. |  |
| List accounts/categories | List accounts, categories, nodes, forms, or fields relevant to the loaded data. | Output includes expected accounts/categories or equivalent tax fields. |  |
| Compute balance | Compute checking balance or equivalent financial state. | Baseline ending checking balance is `8964.77`, or after `TADD` is `8939.78`. |  |
| Run report | Produce income/expense, tax summary, calculation result, validation result, or form-state report. | Report can be compared with expected totals. |  |
| Export result | Export JSON, CSV, XML, PDF, text, database record, API response, or equivalent artifact. | Export path and output format are recorded. |  |

## Expected Totals For Comparison

| Measure | Baseline | After `TADD`, if applied |
|---|---:|---:|
| Ending checking balance | 8964.77 | 8939.78 |
| Freelance gross receipts | 10250.00 | 10250.00 |
| Interest income | 77.75 | 77.75 |
| Schedule C-style cash expenses before mileage | 1142.98 | 1167.97 |
| Schedule C-style net before mileage | 9107.02 | 9082.03 |
| Cash charitable contributions | 370.00 | 370.00 |
| Federal estimated tax payments | 1050.00 | 1050.00 |
| Business miles, no dollar value assigned | 78.2 | 78.2 |

## Failure Behavior Checklist

Use the same failure tests where applicable.

| Failure test | Input | What to record |
|---|---|---|
| Malformed date | `13-40-2025` | Whether validation rejects it and whether the message identifies the field. |
| Invalid amount | `not-a-number` | Whether validation rejects it before state changes. |
| Unknown account/category | `Expenses:Business:Imaginary Category` | Whether the tool creates it implicitly, rejects it, or needs setup first. |
| Missing input file | `evidence/fixtures/does_not_exist.csv` | Whether error handling is clear and non-destructive. |
| Duplicate transaction ID | Repeat `T001` during import if IDs are supported. | Whether duplicates are rejected, merged, duplicated, or silently accepted. |

## Tax Workflow Checklist

For each tool, record what is explicit, inferred, or unsupported.

| Capability | Finding | Evidence |
|---|---|---|
| Form 1040 support |  |  |
| Schedule A support |  |  |
| Schedule B support |  |  |
| Schedule C support |  |  |
| Schedule D support |  |  |
| Schedule E support |  |  |
| Common credits |  |  |
| Tax-year support |  |  |
| Tax-line mapping |  |  |
| Tax form generation |  |  |
| PDF output |  |  |
| MeF XML or e-file path |  |  |
| Stated non-goals or disclaimers |  |  |

## Tool-Specific Starting Plans

### hledger

- Start with `evidence/fixtures/synthetic_freelancer_transactions.csv`.
- Create a minimal rules file or direct journal conversion in a scratch path.
- Run account listing, balance, income statement, and JSON/CSV export if available.
- Verify the ending checking balance and Schedule C-style income/expense totals.
- Test malformed CSV/date/amount and unknown account behavior.

### Actual Budget

- Create an isolated local test budget or data directory.
- Use the official CLI or Node API, depending on setup friction.
- Import or add baseline transactions and categories.
- Query accounts/categories and balances through JSON-oriented output where possible.
- Record whether Actual creates categories/accounts implicitly or requires setup.

### Firefly III

- Use an isolated local instance, container, or documented demo-safe setup.
- Create a personal access token or local auth only if required, and never commit secrets.
- Create asset, revenue, and expense accounts through the API or UI as needed.
- Post baseline transactions through the REST API and inspect JSON responses.
- Capture setup time, auth friction, and export/report options.

### tenforty

- Use `evidence/fixtures/synthetic_freelancer_tax_profile.json`.
- Map tax profile fields into documented function arguments.
- Record which fields are direct inputs, omitted, unsupported, or require assumptions.
- Capture structured return output for the baseline profile.
- Test invalid argument values and missing dependency behavior.

### Filed Open Tax Engine

- Use `evidence/fixtures/synthetic_freelancer_tax_profile.json`.
- Inspect available nodes, schemas, forms, validation, and example commands first.
- Map profile fields into JSON form entries only through documented CLI behavior.
- Capture validation output, dependency graph output, and any JSON/XML/PDF export.
- Treat accuracy and maturity as open questions until hands-on evidence is recorded.

## Tool Record Completion Checklist

For each evaluated tool, fill these sections in `tool_records/template.md` or a copied tool-specific record:

- Status
- One-Sentence Summary
- Identity
- Research Fit
- Programmatic Surface
- Setup and First Useful Operation
- Synthetic Workflow Results
- Workflow Coverage
- Safety and Failure Behavior
- Project Health
- Integration Assessment
- Scores
- Evidence Index
- Open Questions
- Decision Notes

## Minimum Day 9-13 Completion Definition

A tool evaluation is complete enough for comparison when it has:

- Version and setup evidence.
- At least one successful operation or a clearly documented blocker.
- A completed synthetic workflow table with success, failure, or not-applicable status.
- Failure behavior evidence for at least two bad inputs, unless setup failed before testing.
- A note on structured output quality.
- A note on tax workflow coverage or explicit non-fit.
- A provisional prototype suitability score.

## Day 9 Starting Point

Evaluate hledger first because it is the fastest likely path to a repeatable file/CLI workflow and will pressure-test the shared dataset before heavier app/API candidates.
