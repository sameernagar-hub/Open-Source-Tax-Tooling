# Day 14 Prototype Target Selection

Planned phase date: 07-14-2026. Executed early on 07-09-2026 UTC / 07-08-2026 PDT at user request.

## Goal

Build a comparison matrix from the five completed Week 2 tool records, score candidates for prototype value, feasibility, safety, and demo clarity, then choose the primary Week 3 prototype target and backup target.

## What I Did

- Reviewed the completed records for hledger, Actual Budget, Firefly III, tenforty, and Filed Open Tax Engine.
- Compared each candidate across setup friction, structured I/O, workflow coverage, tax coverage, failure behavior, safety, licensing, and demo clarity.
- Created `research/comparison_matrix.md` with the Day 14 matrix and selection scores.
- Created `research/prototype_target_decision.md` with the primary target, backup target, prototype thesis, guardrails, and Day 15 starting point.
- Chose hledger as the primary Week 3 prototype target and Actual Budget as the backup target.

## Evidence Captured

- `research/comparison_matrix.md`
- `research/prototype_target_decision.md`
- `tool_records/tool_1.md`
- `tool_records/tool_2.md`
- `tool_records/tool_3.md`
- `tool_records/tool_4.md`
- `tool_records/tool_5.md`

## Decisions Made

- Use hledger for the Week 3 prototype because it best balances full synthetic workflow coverage, local safety, setup feasibility, structured JSON output, and demo clarity.
- Frame the prototype as tax-adjacent bookkeeping infrastructure, not tax preparation, tax advice, or filing software.
- Use Actual Budget as the backup if the prototype needs an app/API surface instead of hledger's file/CLI/JSON surface.
- Keep tenforty as the most promising future tax-calculation component after a bookkeeping summary layer.
- Keep Filed Open Tax Engine as the highest-upside form-level research candidate, but not the first prototype target because of validation/export noise, maturity risk, and licensing concerns.
- Keep Firefly III as the best REST-first report comparator rather than the Week 3 prototype.

## Problems / Open Questions

- Day 15 should decide whether the hledger prototype uses a committed rules file, generates a rules file from mapping config, or supports both.
- The prototype needs a clear hledger binary discovery/install note without committing third-party binaries.
- GPL-3.0-or-later implications should be documented clearly before packaging or redistributing any wrapper.
- A later extension could call tenforty after hledger summary generation, but that is outside the first prototype scope unless the mentor explicitly requests direct tax calculation.

## Tomorrow's Starting Point

Execute Day 15 by creating `prototype/design.md`, narrowing the hledger adapter scope, defining input/output schemas, and updating the prototype README outline.
