# Day 8 Evaluation Harness and Synthetic Data

Planned phase date: 07-08-2026. Executed on 07-07-2026 at user request.

## Goal

Prepare shared synthetic fixtures and a repeatable evaluation checklist for the Week 2 hands-on tool evaluations.

## What I Did

- Created `evidence/synthetic_dataset.md` as the Phase 8 synthetic dataset artifact.
- Created `evidence/fixtures/synthetic_freelancer_transactions.csv` as the canonical transaction fixture.
- Created `evidence/fixtures/synthetic_freelancer_tax_profile.json` as the canonical tax-profile fixture for tax-oriented tools.
- Created `research/evaluation_checklist.md` with setup, workflow, tax-coverage, failure-testing, evidence, and tool-record checklists.
- Defined the common operations for shortlisted tools: load data, add transaction, list accounts/categories, compute balance, run report, and export result.
- Added expected totals for baseline and add-transaction test states.

## Evidence Captured

- `evidence/synthetic_dataset.md`
- `evidence/fixtures/synthetic_freelancer_transactions.csv`
- `evidence/fixtures/synthetic_freelancer_tax_profile.json`
- `research/evaluation_checklist.md`

## Decisions Made

- Use a 2025 single-freelancer scenario with Schedule C-style income and expenses, interest income, charitable contribution placeholders, estimated tax payments, and a separate mileage log.
- Keep mileage as non-cash metadata with no deduction value assigned.
- Keep `TADD` out of baseline totals so it can test add-transaction behavior consistently.
- Evaluate hledger first on Day 9 because it should be the fastest way to validate the shared file/CLI workflow.

## Problems / Open Questions

- The synthetic tax hints are not authoritative tax treatment and must stay framed as evaluation labels.
- Tax-oriented tools may require assumptions that do not map cleanly from bookkeeping categories.
- Firefly III and Actual Budget may require different setup flows for categories/accounts before importing transactions.

## Tomorrow's Starting Point

Execute Day 9 by evaluating hledger against the shared dataset, capturing setup/version evidence, running the common workflow, testing failure behavior, and filling the first tool record.
