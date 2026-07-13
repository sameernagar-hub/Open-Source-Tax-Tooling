# Day 17 Transaction and Account Reconciliation

Planned phase date: 07-17-2026. Executed early on 07-13-2026 PDT at user request.

## Goal

Implement account loading, transaction import/normalization, source validation before hledger, and structured transaction/account output.

## What I Did

- Extended validated transaction loading to retain structured source rows.
- Ran hledger `print -O json` and `balance --flat -O json` in the same scratch execution path.
- Added hledger amount decoding from `decimalMantissa` and `decimalPlaces`.
- Added normalized transaction output using validated CSV text fields and reconciled hledger postings.
- Added normalized account balance output using hledger's flat balance JSON.
- Added reconciliation checks for transaction IDs, dates, tags, two-posting shape, USD amounts, equal-and-opposite category postings, account sets, category balances, and checking balance.
- Updated `demo` and `smoke` to emit Day 17 transaction/account output.

## Evidence Captured

- `prototype/hledger_adapter/models.py`
- `prototype/hledger_adapter/validation.py`
- `prototype/hledger_adapter/hledger.py`
- `prototype/hledger_adapter/normalize.py`
- `prototype/hledger_adapter/cli.py`
- `evidence/commands/07-13-2026_hledger-adapter_day17_reconciliation.txt`

## Verification

- `python -m compileall hledger_adapter`
- `python -m hledger_adapter --help`
- `python -m hledger_adapter demo --hledger-bin <explicit hledger 1.52.1 path>`
- `python -m hledger_adapter smoke --transactions ../evidence/fixtures/synthetic_freelancer_transactions.csv --transactions ../evidence/fixtures/hledger_synthetic_freelancer_tadd.csv --context ../evidence/fixtures/synthetic_freelancer_tax_profile.json --hledger-bin <explicit hledger 1.52.1 path> --confirm-synthetic`
- `python -m hledger_adapter demo` without a binary to confirm `HLEDGER_NOT_FOUND` and exit 3.
- `python -m hledger_adapter validate --transactions ../evidence/fixtures/synthetic_freelancer_transactions.csv --transactions ../evidence/fixtures/hledger_duplicate_t001.csv --confirm-synthetic` to confirm `INPUT_ID_DUPLICATE` and exit 2.

Baseline result:

- Transactions: 19
- Postings: 38
- Accounts: 14
- Checking balance: `8964.77`
- Reconciliation: passed

Baseline plus `TADD` result:

- Transactions: 20
- Postings: 40
- Accounts: 14
- Checking balance: `8939.78`
- Software balance: `263.99`
- Reconciliation: passed

## Decisions Made

- Keep Day 17 output to transactions, accounts, counts, and reconciliation.
- Leave summary totals, income-statement cross-checks, and tax-adjacent aggregation for Day 18.
- Decode hledger's exact decimal representation and ignore `floatingPoint`.
- Use `balance --flat -O json` for account loading.
- Emit no raw source paths, hledger source positions, or raw report JSON in normal output.

## Problems / Open Questions

- hledger is still unavailable on `PATH` in this workspace.
- Failure fixture coverage is still manual and should become a Day 19 test matrix.
- The normalized summary schema is still intentionally incomplete.

## Tomorrow's Starting Point

Execute Day 18 by adding balance/report summary generation over reconciled postings, including the checking balance, income-statement cross-check, Schedule C-style buckets, and tax-adjacent facts.
