# Prototype Target Decision

Day 14 artifact for Phase 14: Prototype Target Selection.

Planned phase date: 07-14-2026. Executed early on 07-09-2026 UTC / 07-08-2026 PDT at user request.

## Decision

Primary Week 3 prototype target: hledger.

Backup target: Actual Budget.

The Week 3 prototype should be a thin hledger CLI/JSON adapter that turns the synthetic freelancer transaction fixture into normalized, agent-consumable bookkeeping and tax-adjacent summaries. It should not claim to prepare, calculate, validate, or file a tax return.

## Prototype Thesis

A small wrapper around a real open-source bookkeeping engine can make tax-relevant financial facts safer and easier for other software to consume.

The prototype will prove that an integration layer can:

- Accept synthetic freelancer transactions.
- Validate source IDs, dates, amounts, and controlled account/category mappings before tool execution.
- Drive hledger through its documented file/CLI/JSON surface.
- Return normalized JSON for checking balance, income, expenses, and Schedule C-style summary fields.
- Preserve explicit unmapped facts such as mileage, estimated payments, charity, and unsupported tax-form calculations.
- Demonstrate honest boundaries between bookkeeping summaries and tax preparation.

## Why hledger

hledger is the best primary target because it has the strongest full-workflow fit under the project constraints:

| Criterion | Decision finding |
|---|---|
| Real programmatic surface | Documented CLI, CSV rules, JSON export, and optional hledger-web surface. |
| Week 3 feasibility | Official Windows binary worked without a global install; the Day 9 workflow already ran from local files. |
| Demo clarity | A reviewer can inspect the CSV, rules file, command calls, JSON output, and normalized wrapper result. |
| Safety | The tested workflow can stay read-only against isolated fixture files. Wrapper-side checks can close permissive account and duplicate-ID behavior. |
| Research value | It demonstrates the core connectivity problem: making open-source financial data and reports usable by another program without pretending to be tax software. |

The main tradeoff is that hledger is not a tax engine. That is acceptable for Week 3 if the prototype is framed as tax-adjacent bookkeeping infrastructure and the report separately explains where tenforty or Filed Open Tax Engine could sit downstream.

## Backup Target

Actual Budget is the backup because it preserves the primary demo shape while offering a different integration style:

- Official Node API and stable CLI.
- Local scratch budget support.
- Structured API objects that serialize cleanly to JSON.
- MIT license.
- Successful Day 10 transaction, balance, category, and summary workflow.

If hledger becomes unexpectedly blocked or if mentor feedback prefers an app/API integration over a file/CLI integration, the backup prototype should wrap Actual's Node API around the same synthetic transaction fixture and expose the same normalized output shape.

Backup guardrails:

- Prefer import/reconciliation paths when duplicate IDs matter.
- Validate category IDs and reconstructed category paths before mutation.
- Use an isolated local data directory.
- Normalize verbose API errors into concise wrapper errors.
- Keep sync/cloud behavior disabled or clearly out of scope.

## Non-Selected Candidates

Firefly III remains the best REST-first comparison point, but it is heavier than the prototype needs. Docker, auth, database state, AGPL obligations, missing transaction dry-run behavior, and unknown-category auto-creation would consume Week 3 time that is better spent on wrapper design and explanation.

tenforty remains the best tax-calculation component candidate. It is a strong future second stage after hledger summary generation, but as a standalone prototype it would skip the transaction-loading, account, balance, and bookkeeping workflow that the Week 2 harness was designed to test.

Filed Open Tax Engine remains the highest-upside form-level tax-engine candidate. It is not the primary target because the prototype would need to explain validation/export noise, malformed date acceptance, duplicate form handling, local state management, AGPL/commercial licensing, and current project maturity before the core integration story is even clear.

## Week 3 Scope

In scope for the hledger prototype:

- A small adapter under `prototype/`.
- A one-command demo against synthetic data.
- Validation for required columns, dates, numeric amounts, duplicate transaction IDs, known accounts/categories, and file paths.
- hledger subprocess execution through argument arrays, not shell string interpolation.
- JSON normalization for transactions and balances where hledger emits JSON.
- A generated Markdown or JSON summary with Schedule C-style gross receipts, cash expenses before mileage, net before mileage, checking balance, and unsupported/unmapped tax facts.
- Failure checks for malformed date, invalid amount, unknown category, missing file, and duplicate ID.
- README/design documentation that states the prototype is not tax advice or filing software.

Out of scope:

- Real taxpayer data or live financial accounts.
- Form 1040 generation, tax advice, refund calculation, or e-file submission.
- hledger-web server work.
- Direct use of tenforty or Filed Open Tax Engine in the first prototype.
- Hosted/network service deployment.
- Production license analysis beyond a clear GPL note.

## Guardrails

- Use synthetic data only.
- Keep all generated files in a scratch output directory under `prototype/` or a temporary path.
- Do not mutate user ledgers.
- Reject unknown categories and duplicate source IDs before calling hledger.
- Treat hledger output as accounting evidence, not authoritative tax treatment.
- Surface unmapped or unsupported tax facts explicitly rather than hiding them.
- Document GPL-3.0-or-later implications for redistribution or embedding.

## Day 15 Starting Point

Create `prototype/design.md` and update `prototype/README.md` with:

- Adapter shape: local CLI wrapper.
- Input schema: synthetic transaction CSV plus category/tax-hint mapping.
- Output schema: normalized JSON summary and optional Markdown report.
- Command plan: validate, run hledger, parse output, summarize, emit results.
- Failure-test plan: mirror the Day 8 shared failure checklist.
- Setup plan: detect hledger binary or document how to provide its path without committing binaries.
