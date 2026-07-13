# Day 19 Safety and Failure Handling

Planned phase date: 07-19-2026. Executed early on 07-13-2026 PDT at user request.

## Goal

Make the prototype honest and safe by turning expected bad-input and hledger-discovery failures into a stable, repeatable matrix.

## What I Did

- Added `prototype/tests/run_failure_matrix.py`, a standard-library script that runs the CLI in subprocesses and verifies expected exit codes and structured error codes.
- Reused committed bad CSV fixtures for malformed date, invalid amount, unknown category, and duplicate transaction ID cases.
- Generated temporary synthetic fixtures for unknown source account, tax-hint mismatch, wrong amount sign, context dataset mismatch, and negative mileage.
- Added dry-run conflict, missing hledger, unusable hledger candidate, and missing synthetic acknowledgement cases.
- Confirmed preflight failures use `summarize --dry-run` where possible, so invalid inputs stop before backend report execution.
- Confirmed the matrix leaves scratch state unchanged.
- Updated the prototype README safety/failure sections and the project roadmap.
- Updated Phase 20 to include a Vercel-ready read-only project dashboard UI that can surface the changelog, notes, evidence, prototype status/output, research, tool records, report/deck state, and README files.

## Evidence Captured

- `prototype/tests/run_failure_matrix.py`
- `prototype/README.md`
- `prototype/design.md`
- `day_by_day_ai_tax_tooling_phases.md`
- `evidence/commands/07-13-2026_hledger-adapter_day19_failures.txt`

## Verification

- `python tests/run_failure_matrix.py`
- `python -m compileall hledger_adapter tests`

Matrix result:

- Cases: 15
- Passed: 15
- Failed: 0
- Scratch unchanged: true

Verified cases:

- Valid fixture validation succeeds.
- Missing synthetic acknowledgement: `SYNTHETIC_CONFIRMATION_REQUIRED`, exit 2.
- Malformed date: `INPUT_DATE_INVALID`, exit 2.
- Invalid amount: `INPUT_AMOUNT_INVALID`, exit 2.
- Unknown category: `INPUT_CATEGORY_UNKNOWN`, exit 2.
- Unknown source account: `INPUT_ACCOUNT_UNKNOWN`, exit 2.
- Duplicate transaction ID: `INPUT_ID_DUPLICATE`, exit 2.
- Missing transaction file: `INPUT_NOT_FOUND`, exit 2.
- Tax-hint mismatch: `INPUT_TAX_HINT_MISMATCH`, exit 2.
- Wrong amount sign: `INPUT_SIGN_INVALID`, exit 2.
- Context dataset mismatch: `CONTEXT_INVALID`, exit 2.
- Context negative mileage: `CONTEXT_INVALID`, exit 2.
- Dry-run plus kept scratch: `DRY_RUN_OPTION_CONFLICT`, exit 2.
- Missing hledger: `HLEDGER_NOT_FOUND`, exit 3.
- Unusable explicit hledger candidate: `HLEDGER_UNUSABLE`, exit 3.

## Decisions Made

- Keep the failure matrix dependency-free and runnable from `prototype/`.
- Generate edge-case fixtures at runtime so the evidence directory does not accumulate one-off bad files.
- Treat preflight validation, context validation, policy acknowledgement, dry-run option conflicts, and hledger discovery as Day 19 scope.
- Leave fake process-runner tests for hledger timeouts, malformed engine JSON, and reconciliation mutations to a later hardening pass if time allows.
- Add the dashboard UI to Day 20 rather than Day 19, because Day 19's exit criterion is safety/failure behavior.

## Problems / Open Questions

- The matrix does not simulate hledger timeout, nonzero process returns, malformed engine JSON, or corrupted engine schemas.
- The future dashboard should avoid directly exposing host-absolute paths or raw private machine context.
- Vercel deployment will need a static/project-manifest build step or a serverless read-only artifact index; the Day 20 plan now names that explicitly.

## Tomorrow's Starting Point

Execute Day 20 by adding demo packaging and a Vercel-ready project dashboard UI scaffold with a generated artifact manifest for changelog, notes, evidence, prototype, report, research, tool records, and deck/report state.
