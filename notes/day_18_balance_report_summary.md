# Day 18 Balance and Report Summary

Planned phase date: 07-18-2026. Executed early on 07-13-2026 PDT at user request.

## Goal

Implement balance calculation and tax-relevant report generation over reconciled hledger postings so the prototype can run an end-to-end synthetic summary workflow.

## What I Did

- Extended the hledger scratch runner to execute `incomestatement --depth 3 -O json` in addition to `print -O json` and `balance --flat -O json`.
- Added a Day 18 summary builder that derives mapped category magnitudes from normalized, reconciled transactions and account balances.
- Cross-checked mapped revenue and expense buckets against hledger's income-statement JSON.
- Implemented executed `summarize` output and upgraded `demo` to run the canonical fixed-fixture end-to-end summary.
- Added Schedule C-style gross receipts, cash-expense groupings, net before mileage, bookkeeping income-statement totals, interest income, cash charity, federal estimated-payment tracking, preserved mileage facts, warnings, limitations, and provenance.
- Kept `smoke` as the narrower transaction/account reconciliation command.

## Evidence Captured

- `prototype/hledger_adapter/models.py`
- `prototype/hledger_adapter/hledger.py`
- `prototype/hledger_adapter/summary.py`
- `prototype/hledger_adapter/cli.py`
- `prototype/README.md`
- `evidence/commands/07-13-2026_hledger-adapter_day18_summary.txt`

## Verification

- `python -m compileall hledger_adapter`
- `python -m hledger_adapter demo --hledger-bin <explicit hledger 1.52.1 path>`
- `python -m hledger_adapter summarize --transactions ../evidence/fixtures/synthetic_freelancer_transactions.csv --transactions ../evidence/fixtures/hledger_synthetic_freelancer_tadd.csv --context ../evidence/fixtures/synthetic_freelancer_tax_profile.json --hledger-bin <explicit hledger 1.52.1 path> --confirm-synthetic`
- `python -m hledger_adapter summarize --transactions ../evidence/fixtures/synthetic_freelancer_transactions.csv --context ../evidence/fixtures/synthetic_freelancer_tax_profile.json --hledger-bin <explicit hledger 1.52.1 path> --dry-run --confirm-synthetic`
- `python -m hledger_adapter smoke --hledger-bin <explicit hledger 1.52.1 path>`
- `python -m hledger_adapter summarize --transactions ../evidence/fixtures/synthetic_freelancer_transactions.csv --hledger-bin <explicit hledger 1.52.1 path> --confirm-synthetic`
- `python -m hledger_adapter --help`
- `Test-Path .scratch`

Baseline result:

- Transactions: 19
- Postings: 38
- Accounts: 14
- Opening checking balance: `1200.00`
- Ending checking balance: `8964.77`
- Bookkeeping income-statement revenue: `10327.75`
- Bookkeeping income-statement expenses: `1512.98`
- Bookkeeping income-statement net: `8814.77`
- Schedule C-style gross receipts: `10250.00`
- Schedule C-style cash expenses before mileage: `1142.98`
- Schedule C-style net before mileage: `9107.02`
- Interest income: `77.75`
- Cash charitable contributions: `370.00`
- Federal estimated payments tracked: `1050.00`
- Business miles preserved, not monetized: `78.2`

Baseline plus `TADD` result:

- Transactions: 20
- Postings: 40
- Accounts: 14
- Checking balance: `8939.78`
- Software cash expenses: `263.99`
- Schedule C-style cash expenses before mileage: `1167.97`
- Schedule C-style net before mileage: `9082.03`

Additional checks:

- Dry run emitted the planned operations and omitted `transactions` and `summary`.
- Smoke still emitted transaction/account reconciliation without a summary section.
- Missing context emitted mileage status `not_provided`, null mileage value, and null deduction.
- Default executed runs did not leave `prototype/.scratch/`.

## Decisions Made

- Treat hledger's income statement as a bookkeeping cross-check, not the source of Schedule C-style net.
- Derive Schedule C-style and tax-adjacent totals only from the controlled category map after transaction/account reconciliation passes.
- Preserve mileage quantity from context without selecting a rate or calculating a deduction.
- Keep warnings explicit that output is bookkeeping and non-authoritative tax-adjacent labeling.
- Leave file output and Markdown rendering for later phases after the JSON contract is stable.

## Problems / Open Questions

- hledger is still not installed on `PATH`; verification still uses the retained Day 9 executable path explicitly.
- Failure behavior is still mostly manual and should become a Day 19 matrix.
- The summary uses hledger JSON output only; no human-formatted report parsing was required.

## Tomorrow's Starting Point

Execute Day 19 by adding stable failure checks for malformed dates, invalid amounts, unknown categories/accounts, duplicate IDs, missing files, context failures, missing hledger, and dry-run option conflicts.
