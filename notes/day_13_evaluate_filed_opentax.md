# Day 13 Evaluate Tool 5: Filed Open Tax Engine

Planned phase date: 07-13-2026. Executed early on 07-09-2026 UTC / 07-08-2026 PDT at user request.

## Goal

Evaluate Filed Open Tax Engine as the fifth Week 2 hands-on tool and the second tax-oriented candidate, focusing on its CLI/JSON form-entry workflow, TY2025 Form 1040 coverage, validation behavior, and suitability for a Week 3 prototype.

## What I Did

- Verified the official GitHub release metadata for `v2.0.2`, published 2026-05-11.
- Downloaded the official `opentax-windows-x64.exe` binary into `%TEMP%` and verified its SHA-256 hash against the release metadata.
- Ran `opentax version`, `--help`, `node list`, `node inspect`, and `node graph` evidence captures.
- Added `evidence/fixtures/filed_opentax_day13_evaluate.mjs` to drive the CLI with safe argument-array subprocess calls, avoiding PowerShell JSON quoting issues.
- Ran the synthetic freelancer baseline as `general`, `f1099int`, `f1040es`, and `schedule_c` form entries.
- Modeled `TADD` by adding a second return with an extra `24.99` Schedule C Part V software expense.
- Tested a forced Schedule A charity probe with `370.00` of cash contributions.
- Ran return validation, MeF export without force, and MeF export with force.
- Ran failure tests for invalid filing status, malformed date string, invalid amount type, negative gross receipts, unknown node type, unsupported tax year, duplicate interest entry, missing return ID, and invalid JSON.
- Created the completed fifth tool record at `tool_records/tool_5.md`.

## Evidence Captured

- `tool_records/tool_5.md`
- `notes/day_13_evaluate_filed_opentax.md`
- `evidence/commands/07-08-2026_filed-opentax_setup.txt`
- `evidence/commands/07-08-2026_filed-opentax_version.txt`
- `evidence/commands/07-08-2026_filed-opentax_workflow.txt`
- `evidence/commands/07-08-2026_filed-opentax_failure-tests.txt`
- `evidence/fixtures/filed_opentax_day13_evaluate.mjs`
- `evidence/fixtures/filed_opentax_day13_summary.json`
- `evidence/fixtures/filed_opentax_day13_failure_results.json`
- `evidence/fixtures/filed_opentax_day13_baseline_mef.xml`

## Key Results

- Baseline federal total tax was `1286.78094441`, matching the expected self-employment-tax-only shape from tenforty within rounding.
- After `TADD`, total tax fell to `1283.249969865`, a delta of about `-3.530975`.
- OpenTax modeled estimated tax payments and EITC, producing a baseline refund of `412.21905559` and an after-`TADD` refund of `415.750030135`.
- The forced Schedule A charity probe recorded `370.00` of itemized deductions but did not change the final tax because taxable income was already zero.
- Baseline validation reported `1917` rules total, `1278` passed, `44` rejected, `0` alerts, and `595` skipped.
- MeF export without `--force` was blocked by reject-level rules; forced MeF export produced XML with warnings.

## Decisions Made

- Treat Filed Open Tax Engine as the strongest form-level CLI/JSON tax-engine candidate, but not as a mature filing-ready system yet.
- Keep it in prototype consideration if Day 14 prioritizes schema inspection, Form 1040 line outputs, Schedule C/SE mapping, validation, and MeF export.
- Prefer tenforty if the prototype should minimize maturity risk and only needs compact tax-liability calculation.
- Require wrapper-side controls for supported years, date formats, duplicate source forms, shell-safe JSON invocation, local state isolation, and validation/export gating.
- Keep AGPL/commercial licensing visible before any hosted wrapper or binary redistribution decision.

## Problems / Open Questions

- The CLI stores returns under `./.state/returns` relative to the current working directory; wrappers need an explicit scratch directory.
- Inline JSON arguments were unreliable through PowerShell native command invocation; Node `execFileSync` argument arrays worked cleanly.
- Malformed date strings were accepted for `taxpayer_dob`.
- Duplicate identical `f1099int` entries were accepted and double-counted interest.
- Creating a 2024 return was accepted, but computing it failed later with `Unsupported form: f1040:2024`; earlier validation would be better.
- Baseline calculation emitted an `f2441` executor warning even though no child/dependent-care input was provided.
- Validation/export emitted many reject-level rules that looked unrelated to the minimal synthetic return, so fileability claims need deeper review.

## Tomorrow's Starting Point

Execute Day 14 by building the comparison matrix across hledger, Actual Budget, Firefly III, tenforty, and Filed Open Tax Engine, then choose the primary Week 3 prototype target and backup target.
