# Day 20 Project Lab UI Brief

This brief is the Day 20 UI target for the prototype phase. It turns the repository into a runnable, inspectable project application rather than a static dashboard.

## Purpose

Build a Vercel-ready web application that lets a reviewer see the internship work as an execution system:

- What the project is trying to prove.
- Why each artifact exists.
- How synthetic CSV rows move through validation, hledger execution, reconciliation, summary generation, and failure handling.
- What evidence supports each claim.
- How a future contributor can reproduce, extend, commit, and push changes safely.

The app should feel like a live engineering lab notebook with a working run surface, not a generic analytics dashboard.

## Experience Concept

Working name: `Tax Tooling Execution Lab`.

The first screen should be the actual prototype control room:

- A prominent `Run Synthetic Demo` action for local development.
- A `Replay Verified Run` action for Vercel/static environments.
- A live execution rail showing each step: input validation, hledger discovery, version probe, scratch-copy setup, `print`, `balance`, `incomestatement`, reconciliation, summary aggregation, failure matrix, and cleanup.
- Result panels for balances, Schedule C-style totals, tax-adjacent facts, warnings, and unsupported capabilities.
- Evidence drawers that show the exact note, command transcript, fixture, or tool record supporting the currently selected step.
- A contribution panel that shows the current Git workflow: create branch, run checks, commit, push, and open review.

## Manifest Contract

Day 20 should generate or load a JSON manifest from repository files. The manifest must not expose host-absolute paths or secrets.

Required manifest sections:

- `project`: research question, scope, synthetic-only boundary, current phase, next phase.
- `why`: short rationale entries for the selected tool, synthetic data, hledger adapter shape, safety matrix, and UI.
- `execution`: ordered workflow steps, commands, expected status, key output fields, and evidence links.
- `artifacts`: grouped repository files for changelog, notes, evidence, prototype, research, tool records, report, deck, and README files.
- `prototype`: commands, fixture names, known hledger boundary, summary totals, failure-matrix status.
- `evidence`: command transcripts, fixture hashes when available, and day notes.
- `contribution`: Git branch policy, checks to run, commit message style, push target, and review notes.

## Local Live Mode

When run locally, the UI should be able to trigger a real synthetic run:

```text
python -m hledger_adapter demo --hledger-bin <configured local hledger>
python tests/run_failure_matrix.py
```

The UI should stream or progressively reveal:

- Command being run, with local private paths redacted.
- Step status changes.
- Output excerpts from canonical JSON.
- Failure-matrix pass/fail counts.
- Scratch cleanup status.

The app must never accept real taxpayer data. Inputs are pinned to committed synthetic fixtures unless a future local-only advanced mode is explicitly added with the same synthetic acknowledgement policy as the CLI.

## Vercel Replay Mode

Vercel should not depend on a local hledger executable. The deployed experience should still show something running by replaying verified command evidence:

- Animate the same execution rail from recorded evidence.
- Use committed command transcripts and expected output summaries.
- Clearly label this as `verified replay` rather than a new backend execution.
- Keep the same result panels and evidence drawers as local live mode.

This gives a deployed reviewer a functioning walkthrough while preserving the licensing, binary, and local-environment boundary around hledger.

## Interface Requirements

- Responsive layout for mobile and desktop.
- Desktop: execution rail, result workspace, and evidence drawer visible together.
- Mobile: one primary action, step timeline, and swipe/tab access to results, evidence, and contribution.
- No generic filler sections, generic hero copy, or unrelated marketing language.
- No prompt-oriented copy. The interface should use engineering language tied to this project: synthetic fixture, adapter, hledger, reconciliation, evidence, failure matrix, artifact manifest, Git contribution.
- Use concise labels and real values from the project wherever possible.
- Do not expose host-absolute paths, temporary directories, secrets, or real-data instructions.

## Minimum Day 20 Acceptance Criteria

- The app opens locally and shows the project execution lab as the first screen.
- A project manifest is generated or checked in.
- The UI includes project `why` entries, artifact categories, execution steps, verification results, and contribution guidance.
- A local reviewer can either run or replay the synthetic demo from the UI.
- The failure matrix is visible as a first-class safety result, not buried in text.
- The UI makes clear that the prototype is bookkeeping-to-summary infrastructure, not tax preparation or tax advice.
- The app structure is ready for later Vercel deployment.
