# Day 15 Prototype Design

Planned phase date: 07-15-2026. Executed early on 07-11-2026 PDT at user request.

## Goal

Design the smallest useful Week 3 integration around the selected hledger target, define its exact input/output and safety contracts, and leave a narrow implementation slice for Day 16.

## What I Did

- Reviewed the Day 14 target decision, the completed hledger tool record, Day 9 command/JSON evidence, the shared synthetic dataset, and the Week 3 plan.
- Confirmed the integration shape as a local, read-only hledger CLI/JSON wrapper rather than reopening REST, library, or hledger-web options.
- Selected Python 3.11+ with standard-library-only implementation for robust CSV and exact-decimal handling without a server or third-party package.
- Defined versioned transaction CSV, category-map, optional mileage-context, normalized JSON, Markdown-view, error, and exit-code contracts.
- Chose one static adapter-owned hledger rules file plus a separate strict category map; no rules generator or arbitrary user rules in version 1.
- Defined binary discovery, process argument arrays, timeouts, scratch lifecycle, atomic output behavior, path redaction, and input/output reconciliation.
- Defined wrapper checks for duplicate IDs and unknown categories, which hledger accepted during Day 9.
- Separated controlled Schedule C-style aggregation from hledger's broader income-statement net.
- Defined baseline, `TADD`, shared failure, engine-failure, safety, and repeatability acceptance criteria.
- Replaced the prototype placeholder README with a design-stage draft that clearly labels all commands as planned, not implemented.

## Evidence Captured

- `prototype/design.md`
- `prototype/README.md`
- `research/prototype_target_decision.md`
- `tool_records/tool_1.md`
- `evidence/commands/07-08-2026_hledger_workflow.txt`
- `evidence/commands/07-08-2026_hledger_failure-tests.txt`
- `evidence/fixtures/hledger_day9_baseline_print.json`
- `evidence/fixtures/hledger_day9_baseline_checking_balance.json`
- `evidence/fixtures/synthetic_freelancer_transactions.csv`
- `evidence/fixtures/synthetic_freelancer_tax_profile.json`

## Decisions Made

- Use a local Python CLI over hledger's real executable, CSV rules, and JSON reports.
- Keep the adapter stateless and use only read-only `print`, `balance`, and `incomestatement` operations.
- Use one committed static rules file in the prototype and do not accept arbitrary rules.
- Use a versioned JSON category map as the sole summary-classification authority.
- Exact-validate tax hints but treat them as non-authoritative labels.
- Accept one or more CSV inputs so `TADD` can be demonstrated without mutating the baseline fixture.
- Require strict calendar dates, exact two-decimal USD amounts, expected signs, unique IDs, the configured source account, known categories, and matching tax hints before hledger runs.
- Require `cleared=true` in version 1 because the tested rules do not map clearing state into hledger.
- Parse hledger amounts from decimal mantissa and scale, never its binary floating-point convenience value.
- Reconcile every source transaction with exactly two equal-and-opposite USD postings.
- Emit money as fixed two-decimal JSON strings and preserve ledger versus summary sign conventions explicitly.
- Use the optional tax-profile context only for identity/privacy checks and mileage; never use its precomputed money totals as summary inputs.
- Report mileage as preserved but not calculated, or as not provided; never hardcode or monetize it.
- Never use hledger's overall income-statement net as the Schedule C-style result.
- Resolve hledger by explicit flag, then `HLEDGER_BIN`, then `PATH`; never auto-download or commit it.
- Treat hledger 1.52.1 as the tested baseline and warn on other versions unless output invariants fail.
- Keep JSON canonical and defer optional Markdown polish until the JSON contract is stable.
- Keep Actual Budget as a fallback only if the real hledger smoke path remains blocked after Day 16.

## Problems / Open Questions

- hledger is not currently available through `PATH` in this workspace, so Day 16 will need an explicit executable path, `HLEDGER_BIN`, or a documented local setup before the smoke call.
- Only hledger 1.52.1 has hands-on evidence; other versions remain unverified.
- The static Day 9 rules ignore the CSV `cleared` field, so version 1 constrains that field instead of claiming engine-confirmed clearing status.
- Synthetic-only use is a documented policy and explicit acknowledgement, not reliable PII detection.
- The project can document the separate MIT/GPL boundary, but it should not make a definitive legal conclusion about future combined packaging.
- Optional Markdown output remains deliberately deferred until the canonical JSON path works.

## Tomorrow's Starting Point

Execute Day 16 by scaffolding the Python adapter, adding the committed category map and static hledger rules, implementing configuration loading plus binary discovery/version capture, and proving a real read-only smoke call.
