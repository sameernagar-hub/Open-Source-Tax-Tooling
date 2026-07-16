# Tool Evaluations Draft

Day 24 artifact for Phase 24: Tool Evaluation Draft.

Planned phase date: 07-24-2026. Executed early on 07-16-2026 at user request.

## Drafting Note

This is draft prose for the final report's per-tool evaluation section. It is written from local evidence already captured in `tool_records/tool_1.md` through `tool_records/tool_5.md`, command transcripts under `evidence/commands/`, synthetic fixtures under `evidence/fixtures/`, and the synthesis in `research/comparison_matrix.md`. It does not refresh public release or project-health metadata.

## 4. Tool Evaluations

The hands-on phase evaluated five shortlisted tools: hledger, Actual Budget, Firefly III, tenforty, and Filed Open Tax Engine. They were not expected to solve the same problem. The first three are bookkeeping or personal-finance systems; the fourth is a tax calculation library; the fifth is a form-level federal tax engine. The common question was whether each tool could be driven safely and usefully from software using the shared synthetic freelancer facts.

Each subsection below uses the same pattern: identity and role, programmatic surface, workflow coverage, safety and failure behavior, project-health posture, and integration fit.

### 4.1 hledger

hledger is a mature plain-text accounting tool with a strong command-line workflow, CSV rules, JSON export, and an optional web/API surface. In this project it represented the file/CLI/JSON integration path: generate or validate local files, run deterministic read-only reports, and consume structured output without relying on a GUI. It is not a tax-preparation engine, but it is one of the clearest tools for turning tax-relevant bookkeeping facts into inspectable summaries.

The Day 9 evaluation drove hledger through its CLI using the canonical synthetic freelancer CSV and a local rules file. The workflow loaded 19 baseline synthetic transactions, produced balanced postings, exported `print -O json` output, and computed the expected baseline checking balance of `8964.77`. Adding the standard `TADD` software expense changed the checking balance to `8939.78`, matching the shared evaluation checklist. The income statement also produced the expected bookkeeping totals: revenue of `10327.75`, expenses of `1512.98`, and net of `8814.77`, while tax-specific facts such as estimated payments remained explicitly modeled outside hledger's tax logic because hledger has no native tax-return model.

The strongest programmatic surfaces were the CLI, CSV rules, local journal/file model, JSON report export, and documented hledger-web JSON API. The hands-on evaluation used only local files and CLI output, which kept setup friction low and made the workflow reproducible. The main implementation work for a wrapper is not calling hledger; it is normalizing hledger-shaped JSON into a smaller contract for downstream consumers and enforcing rules before hledger accepts overly broad accounting inputs.

Workflow coverage was strong for bookkeeping and reporting. hledger can represent accounts, categories, transactions, balances, income statements, and file-based imports. It can indirectly support Schedule C-style, Schedule A-style, and Schedule B-style summaries if the account tree is designed for those categories. It does not support Form 1040 preparation, tax liability calculation, refund calculation, PDF forms, MeF XML, or e-file submission. For the final report, that distinction is important: hledger is strong infrastructure, not tax software.

Failure behavior was mixed in the useful way that shaped the prototype. hledger rejected malformed dates, invalid amounts, and missing input files with clear errors. It also accepted unknown account names and duplicate transaction IDs under the tested defaults. Those behaviors are reasonable for an accounting tool, but risky for a tax-adjacent adapter. The Week 3 prototype therefore put stricter validation in front of hledger: controlled categories, duplicate ID detection, sign checks, tax-hint checks, synthetic-data acknowledgement, and scratch-only execution.

The project-health posture was strong in the captured evidence. The Day 5 snapshot described hledger as active and well documented, and the Day 9 record captured a local `1.52.1` Windows binary. The license is GPL-3.0-or-later, which is acceptable for local research but needs careful treatment if a wrapper redistributes hledger or embeds it in a larger product.

Integration fit: hledger was the best primary prototype target because it offered the lowest-risk path to a transparent bookkeeping fact layer. The recommended integration shape is a thin CLI adapter that validates CSV/category inputs, runs read-only hledger reports, parses JSON, and emits normalized tax-adjacent summaries with explicit unsupported capabilities.

Evidence: `tool_records/tool_1.md`, `evidence/commands/07-08-2026_hledger_workflow.txt`, `evidence/commands/07-08-2026_hledger_failure-tests.txt`, `evidence/fixtures/hledger_day9_baseline_print.json`, `evidence/fixtures/hledger_day9_baseline_checking_balance.json`, `research/comparison_matrix.md`, and `prototype/retrospective.md`.

### 4.2 Actual Budget

Actual Budget is a local-first personal-finance application with an official Node API and stable CLI. It represented the app/API-backed local workflow in the shortlist: more application-like than hledger, less server-heavy than Firefly III, and friendlier to integration than many traditional desktop finance tools. It is MIT-licensed and scriptable, but it is still a budgeting and personal-finance system rather than a tax-return product.

The Day 10 evaluation used npm packages `@actual-app/api` and `@actual-app/cli` in a scratch local environment. A helper script created a temporary Actual budget, created or reused category groups and categories, loaded the 19 baseline synthetic transactions, read account balances, added the `TADD` transaction, and exported normalized JSON summaries. The baseline checking balance was `8964.77`, and the after-`TADD` balance was `8939.78`. The wrapper summary also reproduced Schedule C-style totals from categories and notes, including after-`TADD` cash expenses of `1167.97` and net before mileage of `9082.03`.

The programmatic surface is one of Actual's strongest points. The official Node API can create and manipulate budgets, accounts, payees, categories, and transactions. The CLI is JSON-first and documented with table and CSV alternatives. Actual does not expose an official REST API, so it should be described as local-first/API-package driven rather than HTTP-service driven. Its data model is also app-owned, not plain text like hledger.

Workflow coverage was strong for personal finance. Actual handled accounts, transactions, categories, payees, balances, and exportable structured data. It could preserve tax hints in categories or notes and support wrapper-side summaries for Schedule C-style expenses, interest income, charitable contributions, and estimated payments. It did not calculate taxes, generate federal forms, model refunds, produce PDFs, or expose an e-file path. Tax-line mapping is manual and should live in a wrapper or controlled category design.

Safety behavior was good for scratch testing but uneven for direct mutation. The API supported a local temporary data directory, which made isolated evaluation straightforward. `importTransactions` offered reconciliation and dry-run-like behavior, and duplicate imported IDs were handled more cautiously there. Direct `addTransactions`, however, accepted a bogus category ID that later appeared as uncategorized, and it accepted a duplicate imported ID as a second transaction. Actual rejected malformed dates and invalid amounts, although the bad-date error was verbose.

The project-health and licensing posture were favorable in the captured evidence. The Day 5 snapshot and Day 10 record described a large active MIT project, current packages, useful docs, and a stable CLI. Compared with GPL/AGPL candidates, Actual is easier to imagine inside a wrapper or demo from a licensing point of view. The tradeoff is that its storage is application-owned and its tax relevance is indirect.

Integration fit: Actual Budget is the best backup prototype target when a local app/API workflow is preferred over hledger's plain-text CLI. A safe wrapper should create controlled accounts/categories, prefer import paths when deduplication matters, validate category IDs before direct adds, and export normalized JSON summaries rather than exposing raw app internals.

Evidence: `tool_records/tool_2.md`, `evidence/fixtures/actual_day10_summary.json`, `evidence/fixtures/actual_day10_transactions_after_add.json`, `evidence/fixtures/actual_day10_evaluate.mjs`, `evidence/commands/07-08-2026_actual_workflow.txt`, `evidence/commands/07-08-2026_actual_failure-tests.txt`, and `research/comparison_matrix.md`.

### 4.3 Firefly III

Firefly III is a mature self-hosted personal-finance manager with the strongest REST JSON surface among the evaluated bookkeeping tools. It represented the server/API integration style: a running web application, authentication, JSON request bodies, JSON responses, and API endpoints for accounts, categories, transactions, balances, and insights. It is a strong REST comparator, not a tax-preparation system.

The Day 11 evaluation used Docker containers for Firefly III and MariaDB, then generated a synthetic local user and API token for the evaluation. The workflow posted the synthetic freelancer data through REST endpoints. Because Firefly models account opening balances separately, the helper represented `T000` as an opening balance and posted the remaining 18 baseline rows as transaction API calls. The account API reported the expected checking balance of `8964.77`; after adding `TADD`, the balance changed to `8939.78`. Insight endpoints and wrapper aggregation produced the expected income and expense summaries.

Firefly's programmatic surface was the clearest HTTP API evaluated. It provided REST JSON endpoints, API documentation, structured error responses, account/category/transaction IDs, tags, notes, and external IDs. It also has adjacent ecosystem pieces such as Data Importer, rules, webhooks, and third-party apps. The cost of that surface is operational: Docker, database state, application keys, authentication, and token lifecycle all become part of the integration.

Workflow coverage was strong for personal-finance bookkeeping and reporting. Firefly can model accounts, counterpart accounts, categories, tags, transactions, balances, and category-level insights. Like hledger and Actual, it can preserve tax hints and support manual Schedule C-style summaries, but it has no native Form 1040 workflow, no tax calculation, no PDF tax forms, no MeF XML, and no e-file path. The Data Importer gives Firefly a realistic bank-import ecosystem, but the Day 11 evaluation focused on direct REST posting for repeatability.

Safety and failure behavior were generally strong at the API-validation layer. Firefly returned HTTP 422 with field-level errors for malformed date and invalid amount inputs, and duplicate transaction hash rejection worked when `error_if_duplicate_hash` was configured. However, an unknown category name was accepted and auto-created, which is convenient for personal finance but risky for tax-controlled mappings. No transaction dry-run endpoint was found for the REST creation path, so wrapper-side validation remains necessary.

The captured project-health evidence was strong: large public project footprint, current Docker image and release evidence, mature docs, API docs, Data Importer, and an active ecosystem. The major nontechnical caveat is license posture. Firefly III is AGPL-3.0, so redistributed or hosted wrappers need careful review, especially if the integration becomes a network service.

Integration fit: Firefly III is the leading REST-first personal-finance comparator. It is the right choice if the project wants to demonstrate API automation against a self-hosted finance system. It is less attractive as the first small prototype because setup and licensing overhead are heavier than hledger, and tax semantics still live entirely in wrapper logic.

Evidence: `tool_records/tool_3.md`, `evidence/fixtures/firefly_day11_summary.json`, `evidence/fixtures/firefly_day11_transactions_after_add.json`, `evidence/fixtures/firefly_day11_failure_results.json`, `evidence/fixtures/firefly_day11_evaluate.mjs`, `evidence/commands/07-08-2026_firefly-iii_workflow.txt`, `evidence/commands/07-08-2026_firefly-iii_failure-tests.txt`, and `research/comparison_matrix.md`.

### 4.4 tenforty

tenforty is a lightweight Python library over Open Tax Solver logic. It was the strongest direct tax-calculation API candidate in the hands-on evaluation. Unlike hledger, Actual, and Firefly III, tenforty does not store transactions or maintain accounts. It accepts summarized tax facts and returns tax calculation outputs. That makes it valuable as a downstream component, but weak as a complete bookkeeping-to-filing workflow.

The Day 12 evaluation ran successfully in a Linux Docker container after native Windows installation failed during the package build. The helper mapped the synthetic freelancer tax profile into `evaluate_return` inputs, including filing status, taxable interest, and Schedule C-style net self-employment income. The baseline run produced federal AGI of `8541.38`, taxable income of `0.00`, self-employment tax of `1286.78`, and total federal tax of `1286.78`. The after-`TADD` run reduced self-employment income from `9107.02` to `9082.03` and total federal tax from `1286.78` to `1283.25`.

The programmatic surface is compact and wrapper-friendly: Python functions, typed or validated inputs, Pydantic-style model output for a single return, and Polars dataframe output for scenario sweeps. The Day 12 helper serialized those outputs to JSON. There is no native CLI, REST API, database, transaction import path, PDF generation, or MeF/e-file surface. The visible README also lagged the installed runtime signature for at least one important input: `self_employment_income` was present in the runtime and used in the evaluation, but not visible in the README argument table captured at the time.

Workflow coverage was strong for calculation and weak outside it. tenforty could calculate federal liability from summarized facts and support scenario analysis, but it could not list accounts, compute bank balances, import transactions, preserve source transaction IDs, calculate refunds from estimated payments, or produce complete tax forms. It supports aggregate-style inputs such as self-employment income and itemized deductions, not a full line-by-line Schedule C or Schedule A form workflow.

Safety behavior was good for a stateless calculation library, but wrappers still need sanity checks. Invalid types and unsupported filing statuses, years, or states returned clear validation or support errors. A negative self-employment income value was accepted and produced negative AGI, which may be legitimate in some tax contexts but should not pass accidentally from bookkeeping data. The evaluated output also contained a suspicious `federal_effective_tax_rate` value that did not match the wrapper's recomputation from AGI, so downstream integrations should recompute or sanity-check important derived fields.

Project health was promising but smaller than the major bookkeeping apps. The captured evidence showed a current tax-year package, MIT license, practical docs, and release activity, but a smaller public footprint. The underlying Open Tax Solver relationship also creates license questions for redistribution that are separate from tenforty's MIT package metadata.

Integration fit: tenforty is best treated as a second-stage calculation component. A strong architecture would feed it normalized summaries from hledger, Actual, or Firefly III, then return guarded liability estimates with explicit unmapped fields such as estimated payments, mileage, charity under the standard deduction, and unsupported form details. It should not be the standalone prototype if the goal is to demonstrate transaction ingestion and bookkeeping reconciliation.

Evidence: `tool_records/tool_4.md`, `evidence/fixtures/tenforty_day12_summary.json`, `evidence/fixtures/tenforty_day12_scenario_grid.json`, `evidence/fixtures/tenforty_day12_failure_results.json`, `evidence/fixtures/tenforty_day12_evaluate.py`, `evidence/commands/07-08-2026_tenforty_workflow.txt`, `evidence/commands/07-08-2026_tenforty_failure-tests.txt`, and `research/comparison_matrix.md`.

### 4.5 Filed Open Tax Engine

Filed Open Tax Engine is a federal individual tax calculation and form-entry engine exposed through a single CLI. It was the highest-upside form-level candidate in the evaluation because it combined JSON form entries, node/schema inspection, validation, dependency graph output, computed line values, payments/refund outputs, and MeF XML export evidence. It was also the newest and roughest candidate, so the recommendation needs to remain cautious.

The Day 13 evaluation downloaded the Windows x64 release binary, verified the release hash, and drove the CLI from a Node helper using argument-array subprocess calls. That avoided fragile inline JSON quoting through PowerShell. The helper created a TY2025 return, added `general`, `f1099int`, `f1040es`, and `schedule_c` entries, and ran `return get`. The baseline output included total income of `9184.77`, AGI of `8541.3795`, total tax of `1286.7809`, total payments of `1699.00`, and refund of `412.2191`. After modeling `TADD` as an additional Schedule C software expense, total tax fell to `1283.2500` and refund increased to `415.7500`.

The programmatic surface was unusually aligned with agent/tooling integration. The CLI exposed return creation, form entry, schema/node inspection, validation, graph inspection, JSON output, and export commands. The wrapper could inspect expected inputs and parse computed line outputs without scraping a GUI. The local state model was simple enough for demos: return JSON lived under a local `.state/returns` directory relative to the working directory. There was no REST API, no native transaction ledger, no bank-file import, and no documented stable library API for external consumers.

Workflow coverage was the strongest of the evaluated tax-specific tools. Filed Open Tax Engine produced Form 1040-style outputs, Schedule C-style lines, Schedule SE-driven tax, estimated payments, an EITC value in the synthetic case, total payments, and refund output. It also accepted a forced Schedule A charity probe. MeF XML export existed, but the normal export path was blocked by reject-level validation rules; only forced export produced XML, and it emitted warnings. PDF export was visible as a command surface but not tested.

Safety and validation were the central caveat. The CLI had real validation commands and rejected invalid numeric types, negative gross receipts, unknown nodes, invalid JSON, and missing return IDs. But it accepted a malformed taxpayer date string because that field was schema-typed as a string. It accepted duplicate identical 1099-INT entries and double-counted interest. Creating a 2024 return succeeded, but computation later failed with `Unsupported form: f1040:2024`. The baseline validation summary reported many rejected and skipped rules, including warnings that appeared unrelated to the minimal synthetic return. A production-like wrapper would need supported-year checks, date validation, duplicate source-document detection, and a hard boundary between successful calculation and validation-clean export.

Project health was the weakest major score despite strong technical promise. The captured evidence described a current-looking but young project with a small public footprint, AGPL/commercial dual licensing, and narrow observed TY2025 catalog support. The docs and schema inspection are useful, but the validation/export behavior needs clearer explanation before relying on output for filing-adjacent workflows.

Integration fit: Filed Open Tax Engine is the high-upside form-level research candidate. It is the best evaluated tool for showing how structured form entries can produce line-level federal tax outputs. It was not selected as the primary Week 3 prototype target because maturity, validation noise, duplicate handling, date handling, and licensing risk would dominate a conservative demo. The right report framing is: promising form-engine candidate, not yet the safest base for a reliable first integration.

Evidence: `tool_records/tool_5.md`, `evidence/fixtures/filed_opentax_day13_summary.json`, `evidence/fixtures/filed_opentax_day13_failure_results.json`, `evidence/fixtures/filed_opentax_day13_baseline_mef.xml`, `evidence/fixtures/filed_opentax_day13_evaluate.mjs`, `evidence/commands/07-08-2026_filed-opentax_workflow.txt`, `evidence/commands/07-08-2026_filed-opentax_failure-tests.txt`, and `research/comparison_matrix.md`.

## Section Takeaway

The per-tool findings explain why the final recommendation cannot be a single blanket winner. hledger, Actual Budget, and Firefly III are strong bookkeeping or personal-finance integration surfaces, but they need wrapper-side tax mapping. tenforty can calculate liability from summarized facts, but it needs a bookkeeping layer before it. Filed Open Tax Engine reaches closest to form-level tax output, but it needs stronger validation, maturity, and licensing review before becoming the conservative prototype base.
