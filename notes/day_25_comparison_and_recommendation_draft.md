# Day 25 - Comparison and Recommendation Draft

Planned date: 07-25-2026. Executed early on 07-16-2026 at user request.

## Goal

Turn the evaluated-tool findings into a clear comparison and recommendation, including the final comparison table, recommendations by use case, tools to avoid for automation, and the reason the prototype target was chosen.

## What I Did

- Added `report/comparison_recommendation_draft.md`.
- Built a compact final comparison table for hledger, Actual Budget, Firefly III, tenforty, and Filed Open Tax Engine.
- Drafted capability, safety, and licensing/deployment comparison prose.
- Separated recommendations by use case: transparent bookkeeping, local app/API integration, REST API integration, tax-liability scenarios, tax-form experimentation, and production filing/live automation.
- Explained why hledger was selected as the Week 3 prototype target and why Actual, Firefly III, tenforty, and Filed Open Tax Engine were not the first build target.
- Updated `README.md`, `report/README.md`, and `report/outline.md` so the new draft is easy to find.

## Evidence Captured

- `report/comparison_recommendation_draft.md`
- `report/outline.md`
- `report/README.md`
- `README.md`

## Verification

- This was a documentation-only phase.
- Ran `git diff --check` after editing to catch whitespace issues.
- Ran a non-ASCII scan over the new/updated Markdown files.

## Decisions Made

- State the recommendation as a layered architecture rather than a single universal winner.
- Recommend hledger as the prototype-backed transparent bookkeeping fact layer.
- Recommend Actual Budget as the local app/API alternative, Firefly III as the REST comparator, tenforty as a downstream calculation component, and Filed Open Tax Engine as cautious form-level experimentation.
- Avoid presenting any evaluated tool as a complete production filing stack.

## Problems / Open Questions

- Day 26 still needs the prototype section prose with architecture, setup, sample output, safety choices, and limitations.
- Final report publication still needs public metadata refresh if current/latest language remains.
- Final revision still needs table-density decisions and citation cleanup.

## Next Starting Point

Execute Day 26 by drafting the prototype report section from `prototype/design.md`, `prototype/README.md`, `prototype/run_day20_demo.py`, `prototype/retrospective.md`, and the execution lab artifacts.
