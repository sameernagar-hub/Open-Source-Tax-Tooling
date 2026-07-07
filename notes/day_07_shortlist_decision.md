# Day 7 Shortlist Decision

Planned phase date: 07-07-2026. Executed on 07-07-2026.

## Goal

Choose 3-5 tools for Week 2 hands-on evaluation and make the selection rationale defensible.

## What I Did

- Created `research/shortlist.md` as the Phase 7 exit artifact.
- Scored plausible candidates across relevance, integration surface, project health, tax workflow fit, and demo potential.
- Selected a balanced five-tool shortlist: hledger, Actual Budget, Firefly III, tenforty, and Filed Open Tax Engine.
- Identified primary backups and replacement conditions for Beancount, OpenTaxSolver, UsTaxes, and GnuCash.
- Wrote exclusion rationale for major non-shortlisted candidates and supporting import-layer tools.

## Evidence Captured

- `research/shortlist.md`
- Prior evidence from `research/longlist.md`, `research/project_health_snapshot.md`, `research/programmatic_surface_survey.md`, and `research/exclusions.md`.

## Decisions Made

- Use hledger as the main plain-text accounting evaluation target because it combines file/CLI workflows with structured JSON output and hledger-web API coverage.
- Use both Actual Budget and Firefly III because they represent different app integration styles: local-first Node API/CLI versus REST JSON self-hosted API.
- Use tenforty as the lightweight tax-calculation library candidate.
- Use Filed Open Tax Engine as a high-upside tax-specific CLI/JSON candidate, with explicit maturity and accuracy caveats.
- Keep Beancount as the first plain-text backup, OpenTaxSolver as the mature tax-form backup, and UsTaxes as the source-level consumer 1040 backup.

## Problems / Open Questions

- Filed Open Tax Engine may prove too immature for meaningful evaluation.
- Firefly III setup may be heavier than the other Week 2 tools.
- tenforty needs local verification of its OpenTaxSolver dependency path.
- The evaluation harness must keep the tax relevance of bookkeeping tools explicit through categories, account mappings, and reports.

## Tomorrow's Starting Point

Execute Day 8 by creating `evidence/synthetic_dataset.md` and `research/evaluation_checklist.md`, then define the common operations each shortlisted tool should attempt with synthetic data.
