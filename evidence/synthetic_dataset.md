# Synthetic Evaluation Dataset

Day 8 artifact for Phase 8: Evaluation Harness and Synthetic Data.

Planned phase date: 07-08-2026. Executed on 07-07-2026 at user request.

## Safety Statement

This dataset is fully synthetic. It does not contain real taxpayer data, real financial account data, personally identifiable information, secrets, real bank credentials, real employer data, or live filing credentials.

The scenario is designed for repeatable tool evaluation, not for tax advice. Tax hints are evaluation labels only and should not be treated as authoritative tax treatment.

## Dataset Identity

| Field | Value |
|---|---|
| Dataset ID | `synthetic-freelancer-2025-v1` |
| Scenario | Single US freelancer with simple consumer/tax-adjacent activity |
| Tax year | 2025 |
| Currency | USD |
| Accounting basis | Cash-basis style transaction fixture |
| Primary account | `Assets:Checking` |
| Fixture CSV | `evidence/fixtures/synthetic_freelancer_transactions.csv` |
| Fixture JSON | `evidence/fixtures/synthetic_freelancer_tax_profile.json` |

## Scenario

The synthetic filer is a single freelancer who receives several client payments, earns small bank interest, pays business expenses, makes cash charitable donations, and makes federal estimated tax payments. The dataset also includes a non-cash mileage log so tools can show whether they support mileage, notes, custom fields, tax-line mapping, or a separate calculation layer.

The same facts should be adapted to each shortlisted tool:

- Bookkeeping tools should load the CSV or equivalent journal entries, list accounts, compute balances, and generate income/expense reports.
- App/API-backed tools should create a test budget/book, import or add the transactions, query accounts, and export structured output where possible.
- Tax-oriented tools should use the summarized tax profile rather than pretending every bookkeeping transaction maps directly to a tax input.

## Accounts And Categories

| Name | Type | Intended use |
|---|---|---|
| `Assets:Checking` | Asset | Cash account for all baseline transactions. |
| `Equity:Opening Balances` | Equity | Synthetic starting balance. |
| `Income:Freelance:Design` | Income | Schedule C-style client income. |
| `Income:Freelance:Consulting` | Income | Schedule C-style client income. |
| `Income:Interest` | Income | Schedule B-style bank interest. |
| `Expenses:Business:Software` | Expense | Schedule C-style software/tooling expense. |
| `Expenses:Business:Office Equipment` | Expense | Schedule C-style office equipment expense. |
| `Expenses:Business:Office Supplies` | Expense | Schedule C-style office supplies expense. |
| `Expenses:Business:Travel` | Expense | Schedule C-style local travel expense. |
| `Expenses:Business:Bank Fees` | Expense | Schedule C-style bank fee expense. |
| `Expenses:Business:Professional Education` | Expense | Schedule C-style professional education placeholder. |
| `Expenses:Business:Coworking` | Expense | Schedule C-style workspace expense. |
| `Expenses:Charity` | Expense | Schedule A-style cash charitable contribution placeholder. |
| `Liabilities:Federal Tax:Estimated Payments` | Liability/payment bucket | Federal estimated tax payment tracking. |

## Baseline Transactions

Use these transactions as the canonical import set. Positive amounts are inflows to `Assets:Checking`; negative amounts are outflows from `Assets:Checking`.

| ID | Date | Payee | Category | Tax hint | Amount |
|---|---|---|---|---|---:|
| T000 | 01-01-2025 | Opening Balance | `Equity:Opening Balances` | None | 1200.00 |
| T001 | 01-15-2025 | Acme Design Co | `Income:Freelance:Design` | Schedule C gross receipts | 2500.00 |
| T002 | 01-31-2025 | CloudCode Tools | `Expenses:Business:Software` | Schedule C software | -59.00 |
| T003 | 02-03-2025 | DeskHub Supply | `Expenses:Business:Office Equipment` | Schedule C office equipment | -320.00 |
| T004 | 03-12-2025 | Northstar Analytics | `Income:Freelance:Consulting` | Schedule C gross receipts | 1800.00 |
| T005 | 03-16-2025 | Metro Transit | `Expenses:Business:Travel` | Schedule C local travel | -38.75 |
| T006 | 03-31-2025 | Sample Bank HYSA | `Income:Interest` | Schedule B interest | 42.18 |
| T007 | 04-05-2025 | City Library Foundation | `Expenses:Charity` | Schedule A cash charity | -120.00 |
| T008 | 05-08-2025 | OfficeMart | `Expenses:Business:Office Supplies` | Schedule C office supplies | -74.23 |
| T009 | 06-01-2025 | Sample Bank | `Expenses:Business:Bank Fees` | Schedule C bank fees | -12.00 |
| T010 | 06-15-2025 | Synthetic Federal Treasury | `Liabilities:Federal Tax:Estimated Payments` | Form 1040 estimated payments | -400.00 |
| T011 | 06-20-2025 | Acme Design Co | `Income:Freelance:Design` | Schedule C gross receipts | 3200.00 |
| T012 | 07-04-2025 | Open Source Finance Summit | `Expenses:Business:Professional Education` | Schedule C education placeholder | -249.00 |
| T013 | 08-15-2025 | CloudCode Tools | `Expenses:Business:Software` | Schedule C software | -180.00 |
| T014 | 09-03-2025 | DeskHub Coworking | `Expenses:Business:Coworking` | Schedule C workspace | -210.00 |
| T015 | 09-10-2025 | Neighborhood Food Fund | `Expenses:Charity` | Schedule A cash charity | -250.00 |
| T016 | 10-01-2025 | Sample Bank HYSA | `Income:Interest` | Schedule B interest | 35.57 |
| T017 | 11-05-2025 | Northstar Analytics | `Income:Freelance:Consulting` | Schedule C gross receipts | 2750.00 |
| T018 | 12-15-2025 | Synthetic Federal Treasury | `Liabilities:Federal Tax:Estimated Payments` | Form 1040 estimated payments | -650.00 |

## Standard Add-Transaction Test

Use this row only for the "add transaction" operation. It is intentionally excluded from the baseline totals.

| ID | Date | Payee | Category | Tax hint | Amount |
|---|---|---|---|---|---:|
| TADD | 12-31-2025 | CloudCode Tools | `Expenses:Business:Software` | Schedule C software | -24.99 |

If a tool successfully applies this test transaction, expected ending checking balance decreases from `8964.77` to `8939.78`, Schedule C cash expenses increase from `1142.98` to `1167.97`, and Schedule C net before mileage decreases from `9107.02` to `9082.03`.

## Mileage Log

Mileage is intentionally separate from the cash transaction CSV. Do not calculate a deduction unless a tool explicitly supports a mileage rate or the evaluator chooses a documented rate for a later experiment.

| ID | Date | Purpose | Business miles | Tax hint |
|---|---|---|---:|---|
| M001 | 02-20-2025 | Client site visit | 18.4 | Schedule C mileage placeholder |
| M002 | 04-02-2025 | Coworking client meeting | 37.2 | Schedule C mileage placeholder |
| M003 | 09-18-2025 | Client materials pickup | 22.6 | Schedule C mileage placeholder |
| Total |  |  | 78.2 |  |

## Expected Baseline Totals

These totals are for sanity checks after import or manual entry.

| Measure | Expected value |
|---|---:|
| Opening checking balance | 1200.00 |
| Freelance gross receipts | 10250.00 |
| Interest income | 77.75 |
| Total non-opening inflows | 10327.75 |
| Schedule C-style cash expenses before mileage | 1142.98 |
| Schedule C-style net before mileage | 9107.02 |
| Cash charitable contributions | 370.00 |
| Federal estimated tax payments | 1050.00 |
| Baseline non-opening outflows | 2562.98 |
| Ending checking balance | 8964.77 |
| Business miles, no dollar value assigned | 78.2 |

## Tax Profile Summary

Use this summary for tax-oriented tools that prefer form-like inputs over transaction imports.

| Field | Value |
|---|---:|
| Filing status | Single |
| Dependents | 0 |
| W-2 wages | 0.00 |
| Schedule C gross receipts | 10250.00 |
| Schedule C cash expenses before mileage | 1142.98 |
| Schedule C net before mileage | 9107.02 |
| Interest income | 77.75 |
| Cash charitable contributions | 370.00 |
| Federal estimated tax payments | 1050.00 |
| Business miles | 78.2 |

## Tool Adaptation Notes

| Tool | Suggested dataset path |
|---|---|
| hledger | Convert CSV to journal entries with rules, or create a journal directly from the account/category map. Validate reports against expected totals. |
| Actual Budget | Create an isolated local test budget and import/add transactions through the CLI or Node API. Use categories as budget categories. |
| Firefly III | Create isolated asset, revenue, and expense accounts through the REST API, then post baseline transactions and export/query results. |
| tenforty | Use the tax profile summary rather than the transaction CSV. Record which fields map directly and which require assumptions. |
| Filed Open Tax Engine | Inspect node/schema requirements, then enter the tax profile summary through supported JSON/CLI commands. Record every assumption. |

## Failure-Test Inputs

Use these bad inputs consistently when testing validation and error clarity.

| Test | Bad input |
|---|---|
| Malformed date | `13-40-2025` |
| Invalid amount | `not-a-number` |
| Unknown account/category | `Expenses:Business:Imaginary Category` |
| Missing input file | `evidence/fixtures/does_not_exist.csv` |
| Duplicate transaction ID | Repeat `T001` during import if the tool has an ID field. |

## Source Index

- [SHORTLIST-DAY7] `research/shortlist.md`, used for the selected evaluation target list.
- [PLAN-DAY8] `day_by_day_ai_tax_tooling_phases.md`, used for Day 8 required contents and exit artifacts.
