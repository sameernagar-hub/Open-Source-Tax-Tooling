# Day 6 Programmatic Surface Survey

Planned phase date: 07-06-2026. Executed on 07-06-2026.

## Goal

Compare how each plausible candidate can be driven from code before installing anything.

## What I Did

- Created `research/programmatic_surface_survey.md` as the Phase 6 exit artifact.
- Reviewed official docs, repositories, API documentation, and source architecture notes for the strongest candidates carried forward from Day 5.
- Classified candidate surfaces as documented stable, documented but constrained, experimental/new, inferred, reference-only, or unclear.
- Compared CLI, library, REST API, plugin, file-format, schema, database, and structured-output surfaces.
- Separated primary shortlist pressure from supporting import infrastructure and reference-only official/public-code projects.

## Evidence Captured

- `research/programmatic_surface_survey.md`
- Source links and compact source IDs inside the survey.
- Key source families checked: hledger docs, Actual API/CLI docs, Firefly III API/docs repositories, Beancount docs, Ledger manual, GnuCash docs/wiki, OpenTaxSolver docs, UsTaxes README/architecture/schema folders, tenforty README/PyPI, Filed Open Tax Engine docs, Tax-Calculator docs, and PolicyEngine US repository.

## Decisions Made

- Treat hledger, Actual Budget, Firefly III, Beancount, tenforty, and Filed Open Tax Engine as the clearest code-facing candidates.
- Treat OpenTaxSolver and UsTaxes as important tax-form/consumer-return candidates with weaker external API surfaces.
- Treat GnuCash as a mature desktop comparator whose automation viability depends on local Windows CLI/binding verification.
- Keep Tax-Calculator and PolicyEngine US as mature policy/rules comparators rather than consumer filing candidates.
- Keep IRS Direct File, OpenFile, and IRS Tax Withholding Estimator as reference-only architecture evidence.
- Keep ofxtools, ofxstatement, beangulp, smart_importer, beancount-import, ledger-autosync, and hledger CSV rules as supporting import infrastructure.

## Problems / Open Questions

- Actual and Firefly both deserve shortlist consideration, but Day 7 may need to choose one if the shortlist is capped.
- Filed Open Tax Engine has the strongest agent-oriented CLI/JSON story but needs accuracy and maturity verification.
- Beancount documentation has v2/v3 tooling caveats that need hands-on verification before assuming exact command names.
- GnuCash Python bindings are optional and may be difficult on Windows.
- OpenTaxSolver is tax-form-relevant but text/PDF-oriented rather than API-oriented.

## Tomorrow's Starting Point

Execute Day 7 by creating `research/shortlist.md`, scoring the strongest candidates, and choosing 3-5 tools for Week 2 hands-on evaluation.
