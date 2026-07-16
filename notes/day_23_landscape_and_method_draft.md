# Day 23 - Landscape and Method Draft

Planned date: 07-23-2026. Executed early on 07-16-2026 at user request.

## Goal

Draft the opening report sections so a reader understands the research question, motivation, evaluation method, open-source landscape, and shortlist rationale before the per-tool findings.

## What I Did

- Added `report/opening_sections_draft.md` with draft prose for the introduction, method, and landscape sections.
- Framed the report around the gap between bookkeeping facts, tax calculation, form output, and filing-adjacent workflows.
- Explained the evidence-first funnel: longlist, health snapshot, programmatic-surface survey, shortlist, shared synthetic workflow, failure tests, comparison, and prototype decision.
- Summarized the landscape by integration role rather than popularity: import infrastructure, plain-text accounting, personal-finance apps, tax calculation and policy models, form-level engines, and filing/submission reference points.
- Explained why the shortlist balanced hledger, Actual Budget, Firefly III, tenforty, and Filed Open Tax Engine.
- Updated `README.md`, `report/README.md`, and `report/outline.md` so the new draft is easy to find.

## Evidence Captured

- `report/opening_sections_draft.md`
- `report/outline.md`
- `report/README.md`
- `README.md`

## Verification

- This was a documentation-only phase.
- Ran `git diff --check` after editing to catch whitespace issues.
- The draft intentionally avoids claiming public release/project-health metadata was refreshed today.

## Decisions Made

- Keep the Day 23 prose as a separate draft file instead of replacing the Day 22 outline.
- Treat public release and project-health details as point-in-time evidence until a final publication refresh.
- Use the landscape section to support the prototype's conservative framing: a validated bookkeeping fact layer, not production tax preparation.

## Problems / Open Questions

- Final report publication still needs a last metadata refresh for public projects if the prose uses current/latest language.
- Table density is still undecided for the final report body versus appendix.
- Mentor or reviewer feedback may change the opening framing before final export.

## Next Starting Point

Execute Day 24 by drafting the per-tool evaluation sections from `tool_records/tool_1.md` through `tool_records/tool_5.md`.
