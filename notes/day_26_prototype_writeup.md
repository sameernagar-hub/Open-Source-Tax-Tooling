# Day 26 - Prototype Writeup

Planned date: 07-26-2026. Executed early on 07-16-2026 at user request.

## Goal

Draft the prototype section of the report so a reader can understand the hledger adapter without reading every line of code.

## What I Did

- Added `report/prototype_writeup_draft.md`.
- Covered the adapter architecture, demo workflow, setup summary, sample output, safety choices, limitations, and what the prototype proves.
- Ran `python run_day20_demo.py --json` from the repository root and used the successful Day 26 live result in the sample-output section.
- Updated `README.md`, `report/README.md`, `report/outline.md`, and `prototype/README.md` so the new prototype writeup is easy to find.

## Evidence Captured

- `report/prototype_writeup_draft.md`
- `report/outline.md`
- `report/README.md`
- `prototype/README.md`
- `README.md`

## Verification

- `python run_day20_demo.py --json` passed locally.
- The demo reported 19 transactions, 38 postings, 14 accounts, checking balance `8964.77`, Schedule C-style net before mileage `9107.02`, hledger `1.52.1`, reconciliation `passed`, and 15/15 failure-matrix cases passed.
- Ran `git diff --check` after editing to catch whitespace issues.
- Ran a non-ASCII scan over the new/updated Markdown files.

## Decisions Made

- Treat the execution lab as a reviewer surface, not a production service.
- Keep JSON as the canonical output contract; optional Markdown remains deferred.
- Emphasize that the prototype proves validated bookkeeping-to-summary infrastructure, not tax preparation.

## Problems / Open Questions

- Day 27 still needs full report revision, citation cleanup, table-density decisions, and unsupported-claim checks.
- Final report publication still needs public metadata refresh if current/latest language remains.
- Final screenshots or rendered figures from the execution lab are still optional pending report design choices.

## Next Starting Point

Execute Day 27 by consolidating the report drafts, tightening prose, checking evidence links, removing unsupported claims, and deciding which tables belong in the main body versus appendices.
