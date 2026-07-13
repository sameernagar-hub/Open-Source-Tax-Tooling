# Day 16 Adapter Skeleton

Planned phase date: 07-16-2026. Executed early on 07-13-2026 PDT at user request.

## Goal

Create the first working adapter layer around hledger: scaffold the Python package, commit configuration/rules, load synthetic fixtures, discover and version-probe hledger, expose CLI help, and prove a real read-only smoke call.

## What I Did

- Created the standard-library Python package under `prototype/hledger_adapter/`.
- Added module entry points so the adapter runs with `python -m hledger_adapter` from `prototype/`.
- Added `prototype/pyproject.toml`.
- Added `prototype/config/category_map.json` with the version 1 account, bucket, sign, and tax-hint table.
- Added `prototype/config/hledger.csv.rules` based on the tested Day 9 rules.
- Added `prototype/.gitignore` for kept scratch and Python bytecode.
- Implemented structured JSON errors and exit-code categories.
- Implemented `validate`, `smoke`, `demo`, and `summarize --dry-run`.
- Implemented category-map loading, strict synthetic transaction CSV validation, optional context validation, and provenance hashes.
- Implemented hledger discovery through `--hledger-bin`, `HLEDGER_BIN`, then `PATH`.
- Implemented hledger `--version` capture and a read-only `print -O json` smoke call through scratch copies.

## Evidence Captured

- `prototype/hledger_adapter/`
- `prototype/config/category_map.json`
- `prototype/config/hledger.csv.rules`
- `prototype/pyproject.toml`
- `prototype/.gitignore`
- `evidence/commands/07-13-2026_hledger-adapter_day16_smoke.txt`

## Verification

- `python -m hledger_adapter --help`
- `python -m compileall hledger_adapter`
- `python -m hledger_adapter validate --transactions ../evidence/fixtures/synthetic_freelancer_transactions.csv --context ../evidence/fixtures/synthetic_freelancer_tax_profile.json --confirm-synthetic`
- `python -m hledger_adapter summarize --transactions ../evidence/fixtures/synthetic_freelancer_transactions.csv --context ../evidence/fixtures/synthetic_freelancer_tax_profile.json --hledger-bin <explicit hledger 1.52.1 path> --dry-run --confirm-synthetic`
- `python -m hledger_adapter demo --hledger-bin <explicit hledger 1.52.1 path>`

The smoke run detected `hledger 1.52.1-g3834a163b-20260428, windows-x86_64`, matched the tested baseline, and saw 19 transactions with 38 postings.

## Decisions Made

- Keep `smoke` as the Day 16 proof command and reserve full `summarize` for normalized Day 18+ output.
- Keep `demo` pinned to the canonical synthetic fixture and context.
- Keep custom inputs gated by `--confirm-synthetic`.
- Use the retained Day 9 hledger executable only as an explicit verification input, not as a discovery fallback.
- Keep scratch files ephemeral by default; explicit kept scratch is confined to `prototype/.scratch/`.

## Problems / Open Questions

- hledger is still not on `PATH` in this workspace.
- Day 16 smoke verifies invocation and JSON shape, but not full reconciliation or summary totals.
- hledger versions other than 1.52.1 remain untested.

## Tomorrow's Starting Point

Execute Day 17 by normalizing hledger transaction/account JSON, reconciling source rows to balanced USD postings, and proving the first account/checking-balance invariants.

