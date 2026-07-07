# Research Log

This is the rolling daily research log. Add one entry at the end of each work session before moving to the next phase.

Use direct links to tool records, evidence files, source URLs, and commands whenever a note supports a later report claim.

## Entry Template

```md
## MM-DD-YYYY - Phase N: Title

### Goal

What today was supposed to accomplish.

### What I Did

- Concrete research, setup, or implementation steps completed.

### Evidence Captured

- Source links, command outputs, screenshots, metadata snapshots, or local files created.

### Decisions Made

- Choices that affect the shortlist, evaluation method, prototype direction, or report framing.

### Problems / Open Questions

- Gaps, confusing findings, tool failures, mentor questions, or follow-up searches.

### Tomorrow's Starting Point

- The first concrete action for the next phase.
```

## 07-02-2026 - Phase 2: Workspace and Evidence System

### Goal

Create the research workspace so future findings, command output, source links, and tool evaluations have consistent homes.

### What I Did

- Created the main workspace folders and trackable README files.
- Added evidence subfolders for commands, repository metadata, documentation notes, screenshots, and synthetic fixtures.
- Created `tool_records/template.md`.
- Created `notes/source_citation_conventions.md`.
- Wrote the Day 2 exit note at `notes/day_02_workspace_and_evidence.md`.

### Evidence Captured

- `tool_records/template.md`
- `notes/source_citation_conventions.md`
- `notes/day_02_workspace_and_evidence.md`
- `evidence/README.md`

### Decisions Made

- Use a dedicated citation convention with compact source IDs.
- Store local command and metadata evidence in purpose-specific evidence folders.
- Keep future tool evaluations in one template-driven file per tool.

### Problems / Open Questions

- None for this phase.

### Tomorrow's Starting Point

Create `research/longlist.md` for the starter candidate tools.

## 07-03-2026 - Maintenance: Changelog and Brief Alignment

### Goal

Create a persistent changelog and compare the repository plan against the attached internship brief.

### What I Did

- Extracted text from `C:\Users\nagar\Downloads\intern_project_description.pdf` with `pypdf`.
- Searched the execution plan, day-by-day plan, README, day notes, research log, and tool template for brief-specific requirements.
- Created `CHANGELOG.md` and backfilled Day 1 and Day 2 entries.
- Created `notes/internship_brief_alignment.md`.
- Updated the execution plan, day-by-day plan, README, and tool-record template with missing or implicit brief details.

### Evidence Captured

- `CHANGELOG.md`
- `notes/internship_brief_alignment.md`
- `codex_execution_plan_ai_tax_tooling.md`
- `day_by_day_ai_tax_tooling_phases.md`
- `tool_records/template.md`

### Decisions Made

- Keep the attached PDF out of the repository by default.
- Track third-party wrappers, exact tax-form coverage prompts, stated non-goals, annual tax-year support, and mentorship/logistics terms explicitly.
- Update `CHANGELOG.md` after every meaningful work session going forward.

### Problems / Open Questions

- `pdfinfo` was not installed, so PDF inspection used Python and `pypdf`.

### Tomorrow's Starting Point

Execute Phase 3 by creating `research/longlist.md` for the starter candidate tools.

## 07-04-2026 - Phase 3: Starter Tool Inventory

### Goal

Turn the starter candidate list into a structured longlist with first-pass metadata, docs links, release/status notes, licenses, categories, integration surfaces, and immediately visible wrappers or adjacent tools.

### What I Did

- Created `research/longlist.md` as the Day 3 exit artifact.
- Checked primary project, documentation, release, license, PyPI, and official government pages for the starter candidates.
- Captured first-pass entries for GnuCash, Beancount, Ledger CLI, hledger, Firefly III, OpenTaxSolver, IRS Direct File posture, OFX/QIF parser tooling, and CSV-to-ledger tooling.
- Added immediate adjacent prior art including piecash, beangulp, smart_importer, beancount-import, ledger-autosync, Firefly III Data Importer, and OpenFile.

### Evidence Captured

- `research/longlist.md`
- Source links and compact citation IDs inside `research/longlist.md`
- Primary source families checked: GitHub repositories/releases, PyPI package pages, official documentation sites, SourceForge project/download pages, and IRS Direct File pages.

### Decisions Made

- Treat IRS Direct File as reference architecture and schema/API prior art, not as an active filing candidate.
- Treat OFX/QIF and CSV-to-ledger tooling as adjacent import infrastructure rather than standalone tax or bookkeeping candidates.
- Keep both API-first and plain-text/CLI-first paths alive until the Day 7 shortlist decision.

### Problems / Open Questions

- OpenTaxSolver appears tax-form-relevant but may not expose a clean programmatic API.
- GnuCash Python bindings are optional/build-dependent and need local verification before being considered easy to automate.
- ledger-autosync has newer PyPI metadata than its GitHub latest-release page, so package/release metadata needs reconciliation during the health snapshot.
- OpenFile may deserve promotion to the longlist during Day 4 discovery because it is an active-looking fork of IRS Direct File, but accuracy and status caveats are prominent.

### Tomorrow's Starting Point

Execute Day 4 discovery search: expand the longlist with credible additional tools and create `research/exclusions.md` for closed-source, abandoned, irrelevant, or non-consumer candidates.

## 07-05-2026 - Phase 4: Discovery Search

### Goal

Find credible open-source tools not listed in the original brief, expand the longlist, and document exclusions.

### What I Did

- Searched for open-source US tax calculators, 1040/form generators, tax-benefit rules engines, withholding estimators, personal-finance apps, plain-text-accounting interfaces, and import/export tooling.
- Checked primary sources including GitHub repositories, official docs, IRS repositories/pages, PyPI pages, SourceForge pages, and project websites.
- Expanded `research/longlist.md` with newly discovered candidates and prior-art tools.
- Created `research/exclusions.md` for tools excluded because of license, scope, health, maturity, narrowness, or lack of public inspectability.
- Wrote the Day 4 exit note at `notes/day_04_discovery_search.md`.

### Evidence Captured

- `research/longlist.md`
- `research/exclusions.md`
- `notes/day_04_discovery_search.md`
- Source links and citation IDs embedded in the longlist and exclusions file.

### Decisions Made

- Promote UsTaxes, HabuTax, Filed Open Tax Engine, Tax-Calculator, PolicyEngine US, IRS Tax Withholding Estimator, tenforty, and OpenFile as tax-specific or tax-model candidates.
- Promote Actual Budget, KMyMoney, HomeBank, Money Manager Ex, Fava, Paisa, and ofxstatement as personal-finance, UI, or import-layer comparators.
- Treat OpenFile as a cautionary Direct File fork, not as an active filing-channel candidate.
- Treat Tax-Calculator and PolicyEngine US as programmatic tax-model comparators rather than consumer filing tools.
- Exclude or defer Akaunting, ERPNext, Maybe Finance, OpenTaxForms, Python-Taxes, TaxStuff, Kresus, ezBookkeeping, Skrooge, NBER TAXSIM, IRS Free File Fillable Forms, and closed commercial tax products.

### Problems / Open Questions

- New tax-engine candidates need health and accuracy scrutiny before shortlisting.
- Exact license details for KMyMoney and OpenFile need verification.
- Desktop personal-finance tools may be file-format-only, making them weaker for API-style integration.

### Tomorrow's Starting Point

Execute Day 5 by creating `research/project_health_snapshot.md` and normalizing release dates, recent activity, licenses, contributor signals, documentation quality, annual tax-year support, and data-format evidence for plausible candidates.

## 07-05-2026 - Phase 5: Metadata and Health Snapshot

### Goal

Gather comparable project-health evidence before choosing the shortlist.

### What I Did

- Created `research/project_health_snapshot.md` as the Day 5 exit artifact.
- Checked GitHub, PyPI, SourceForge, IRS, and official project documentation sources for health, release, license, docs, tax-year, and data-format evidence.
- Split candidates into core shortlist-pressure targets and supporting/lower-priority comparators.
- Wrote the Day 5 exit note at `notes/day_05_metadata_health_snapshot.md`.

### Evidence Captured

- `research/project_health_snapshot.md`
- `notes/day_05_metadata_health_snapshot.md`
- Source links and compact citation IDs inside the snapshot.

### Decisions Made

- Prioritize hledger, Firefly III, Actual Budget, Beancount, GnuCash, OpenTaxSolver, UsTaxes, tenforty, Tax-Calculator, and PolicyEngine US for Day 6 surface review.
- Treat IRS Direct File, OpenFile, and IRS Tax Withholding Estimator as reference/cautionary entries.
- Treat import tools such as ofxtools, ofxstatement, beangulp, smart_importer, beancount-import, and ledger-autosync as supporting infrastructure.

### Problems / Open Questions

- Some projects publish outside GitHub, so GitHub release metadata alone is not reliable.
- GnuCash automation on Windows needs local verification.
- Filed Open Tax Engine is promising but too new to trust without hands-on validation.

### Tomorrow's Starting Point

Execute Day 6 by creating `research/programmatic_surface_survey.md` and comparing documented/inferred automation surfaces across the strongest candidates.

## 07-06-2026 - Phase 6: Programmatic Surface Survey

### Goal

Compare how each plausible candidate can be driven from code before installing anything.

### What I Did

- Created `research/programmatic_surface_survey.md` as the Day 6 exit artifact.
- Checked official documentation, API docs, repositories, source architecture notes, and existing Day 5 evidence for the strongest candidates.
- Classified surfaces by whether they are documented stable, documented but constrained, experimental/new, inferred, reference-only, or unclear.
- Compared structured input/output support across CLI, library, REST API, plugin, file-format, schema, database, and report-export surfaces.

### Evidence Captured

- `research/programmatic_surface_survey.md`
- `notes/day_06_programmatic_surface_survey.md`
- Source links and compact citation IDs embedded in the survey.

### Decisions Made

- Prioritize hledger, Actual Budget, Firefly III, Beancount, tenforty, and Filed Open Tax Engine for the Day 7 shortlist discussion.
- Treat OpenTaxSolver and UsTaxes as important tax-form candidates with weaker external API surfaces.
- Treat GnuCash as a mature desktop comparator requiring local CLI/binding verification.
- Treat Tax-Calculator and PolicyEngine US as policy/rules comparators, not filing products.
- Keep IRS Direct File, OpenFile, and IRS Tax Withholding Estimator as reference-only architecture evidence.

### Problems / Open Questions

- The Day 7 shortlist needs to decide whether both Actual and Firefly are necessary.
- Filed Open Tax Engine needs hands-on accuracy and maturity checks before it can be recommended.
- Beancount v2/v3 tooling differences need verification.
- GnuCash remains promising but likely setup-heavy on Windows.

### Tomorrow's Starting Point

Execute Day 7 by creating `research/shortlist.md`, scoring candidates, and selecting 3-5 tools for Week 2 hands-on evaluation.

## 07-07-2026 - Phase 7: Shortlist Decision

### Goal

Choose 3-5 tools for deep Week 2 evaluation and document a defensible selection rationale.

### What I Did

- Created `research/shortlist.md` as the Day 7 exit artifact.
- Scored plausible candidates across relevance, integration surface, project health, tax workflow fit, and demo potential.
- Selected hledger, Actual Budget, Firefly III, tenforty, and Filed Open Tax Engine for Week 2 hands-on evaluation.
- Created `notes/day_07_shortlist_decision.md` as the Day 7 exit note.
- Identified backup candidates and replacement conditions for Beancount, OpenTaxSolver, UsTaxes, and GnuCash.

### Evidence Captured

- `research/shortlist.md`
- `notes/day_07_shortlist_decision.md`
- Prior evidence from `research/longlist.md`, `research/project_health_snapshot.md`, `research/programmatic_surface_survey.md`, and `research/exclusions.md`.

### Decisions Made

- Use hledger for the plain-text accounting slot.
- Use Actual Budget and Firefly III to compare local-first API/CLI integration against REST JSON integration.
- Use tenforty and Filed Open Tax Engine for tax-oriented coverage.
- Keep Beancount as the first plain-text backup and OpenTaxSolver as the first mature tax-form backup.

### Problems / Open Questions

- Filed Open Tax Engine needs skeptical hands-on maturity and accuracy checks.
- Firefly III setup cost may affect Week 2 timing.
- tenforty's OpenTaxSolver dependency path needs local verification.

### Tomorrow's Starting Point

Execute Day 8 by creating the synthetic dataset and evaluation checklist for the five shortlisted tools.

## 07-07-2026 - Phase 8: Evaluation Harness and Synthetic Data

### Goal

Prepare shared synthetic fixtures and a repeatable evaluation checklist for the Week 2 hands-on tool evaluations.

### What I Did

- Created `evidence/synthetic_dataset.md` as the Day 8 synthetic dataset artifact.
- Created `evidence/fixtures/synthetic_freelancer_transactions.csv` and `evidence/fixtures/synthetic_freelancer_tax_profile.json`.
- Created `research/evaluation_checklist.md` with setup, workflow, tax-coverage, failure-testing, evidence, and tool-record checklists.
- Created `notes/day_08_evaluation_harness_and_synthetic_data.md` as the Day 8 exit note.
- Defined expected totals for the baseline dataset and standard add-transaction test.

### Evidence Captured

- `evidence/synthetic_dataset.md`
- `evidence/fixtures/synthetic_freelancer_transactions.csv`
- `evidence/fixtures/synthetic_freelancer_tax_profile.json`
- `research/evaluation_checklist.md`
- `notes/day_08_evaluation_harness_and_synthetic_data.md`

### Decisions Made

- Use a 2025 single-freelancer scenario with Schedule C-style income and expenses, interest income, charitable contribution placeholders, estimated tax payments, and mileage metadata.
- Keep mileage separate from cash transactions and assign no deduction value.
- Use `TADD` as the standard add-transaction test outside the baseline CSV.
- Start Day 9 with hledger to validate the shared dataset through the fastest likely file/CLI path.

### Problems / Open Questions

- Tax hints remain evaluation labels, not authoritative tax treatment.
- Tax-oriented tools may need manual assumptions when mapping from the bookkeeping fixture to form-like inputs.
- App/API-backed tools may need account/category setup before import.

### Tomorrow's Starting Point

Execute Day 9 by evaluating hledger with the shared dataset and filling the first tool record.
