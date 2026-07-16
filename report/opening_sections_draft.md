# Opening Sections Draft

Day 23 artifact for Phase 23: Landscape and Method Draft.

Planned phase date: 07-23-2026. Executed early on 07-16-2026 at user request.

## Drafting Note

This is prose for the final report, not a new public-source refresh. It is written from repository evidence captured through 07-15-2026: the project README, execution plans, longlist, health snapshot, programmatic-surface survey, shortlist decision, evaluation checklist, tool records, comparison matrix, prototype decision, and prototype retrospective. Public release and project-health metadata should still be refreshed before final publication if the final report uses words like "current", "latest", or "active".

## 1. Introduction

Consumer tax work does not begin inside a tax form. It usually begins in bank exports, invoices, personal-budgeting categories, estimated payments, receipts, small-business expenses, and bookkeeping records that were created for day-to-day financial life rather than for annual filing. A human can often bridge those layers manually: read the bank record, decide whether an expense belongs on Schedule C, remember that estimated payments are not ordinary expenses, and transfer the result into tax software. For software, and especially for AI-assisted workflows, that bridge is a systems problem. The useful question is not only whether a project can calculate a tax number, but whether it exposes stable inputs, structured outputs, validation boundaries, clear failure modes, and enough semantic meaning to be connected safely to other tools.

This report studies that bridge in the open-source ecosystem. The guiding research question is: what does the open-source ecosystem for consumer tax bookkeeping and US tax-return preparation or submission-adjacent tooling look like, and how feasible is it to connect representative tools to other software through APIs, CLIs, file formats, schemas, libraries, or comparable programmatic surfaces?

The project is scoped around consumer and freelancer-oriented workflows, with a US tax focus where practical. That scope intentionally crosses categories. Some tools in the landscape are bookkeeping systems that know little about tax forms. Some are personal-finance applications with strong APIs but no native tax workflow. Some are tax calculation libraries or form engines that accept summarized facts but do not import raw transactions. Some official or government-adjacent projects are valuable reference architectures but are not usable third-party filing channels. The report treats those differences as the central finding rather than as noise.

The work was also deliberately constrained. All testing used generated synthetic data. No real taxpayer data, real bank data, personally identifiable information, secrets, production filing credentials, or live submission workflows belong in this repository. The prototype should be read as educational integration research, not tax advice and not production tax-preparation software. Its strongest claim is that a thin, explicit adapter can turn synthetic bookkeeping rows into validated tax-adjacent facts while preserving the boundary between bookkeeping summaries and tax filing.

The expected deliverables for the internship are a written research report, a small prototype integration, and a 20-30 minute presentation deck. By the time this draft was written, the project had already completed a five-tool hands-on evaluation and a frozen hledger-based prototype. The resulting thesis is narrower and more useful than "open-source tax software exists" or "AI can file taxes." The stronger thesis is that open-source bookkeeping tools and open-source tax tools expose useful programmatic surfaces, but they rarely cover the full chain from transactions to validated filing artifacts. The practical near-term integration win is a guarded bookkeeping fact layer that can feed downstream tax-aware tools later.

## 2. Method

The project used an evidence-first funnel. The first pass created a longlist of candidate tools and adjacent infrastructure, including plain-text accounting systems, desktop and self-hosted personal-finance applications, import/export utilities, tax calculation libraries, tax form engines, and official reference projects. The next pass normalized project health: license posture, visible release or activity signals, documentation quality, contributor/community signals, tax-year support for tax-specific projects, and data or automation substrate. A separate programmatic-surface survey then asked how each plausible tool could actually be driven from code.

Those early stages narrowed the landscape into a balanced shortlist for hands-on evaluation:

| Tool | Role in the shortlist | Why it mattered |
|---|---|---|
| hledger | Plain-text accounting and file/CLI/JSON workflow | Best low-friction candidate for turning synthetic transactions into structured reports. |
| Actual Budget | Local-first personal-finance app API/CLI | Strong official Node API and stable CLI, with a different integration model from plain-text accounting. |
| Firefly III | Self-hosted REST personal-finance system | Strongest REST JSON personal-finance comparator. |
| tenforty | Lightweight tax-calculation library | Clean Python calculation surface over OpenTaxSolver-style inputs. |
| Filed Open Tax Engine | Form-level federal tax CLI/JSON engine | Highest-upside tax-specific engine, with schemas, validation, line outputs, and MeF export evidence, but with maturity caveats. |

The shortlist was not selected by score alone. It was balance-constrained: the evaluation needed to cover the most important integration styles, not merely pick five projects from the same category. Beancount, Ledger CLI, GnuCash, OpenTaxSolver, UsTaxes, PSL Tax-Calculator, PolicyEngine US, IRS Direct File, OpenFile, and several import-layer tools remained important landscape evidence or backups, but they did not all need full Week 2 execution.

### Evaluation Rubric

Each candidate was evaluated against the same broad dimensions:

| Dimension | Question asked | Evidence used |
|---|---|---|
| Identity and health | What is the project, how is it licensed, and does it show enough maintenance signal to matter? | Longlist, health snapshot, official docs, release pages, repository metadata. |
| Programmatic surface | Can software drive the tool through a CLI, library, REST API, file format, schema, database, plugin, or structured export? | Programmatic-surface survey, official docs, hands-on commands. |
| Setup and first useful operation | How much friction exists before a real operation works locally? | Setup transcripts, version checks, local scratch runs. |
| Common workflow coverage | Can the tool load data, add a standard synthetic transaction or equivalent, list accounts or fields, compute balances or tax outputs, run reports, and export results? | Shared evaluation checklist, tool records, fixtures. |
| Structured input/output | Does the tool return machine-readable data, or does a wrapper need to parse human-oriented output? | JSON, CSV, XML, Python objects, API responses, and command transcripts. |
| Tax workflow coverage | Does the tool support bookkeeping, tax-line mapping, Form 1040 concepts, schedules, payments/refunds, PDF output, MeF XML, or e-file-adjacent flows? | Tool records and tax workflow checklist. |
| Safety and failure behavior | How does the tool handle malformed dates, invalid amounts, unknown categories, missing files, duplicates, and validation boundaries? | Failure-test transcripts and wrapper behavior. |
| Integration fit | Is the tool a good candidate for a thin wrapper, an automation layer, an AI-agent-consumable workflow, or a future downstream component? | Comparison matrix and prototype target decision. |

Scores were used directionally. They helped compare candidates, but the report treats qualitative differences as equally important. For example, Firefly III has a stronger REST surface than hledger, but hledger had lower setup cost and a more transparent file workflow for the Week 3 prototype. Filed Open Tax Engine had stronger form-level upside than hledger, but its validation/export noise and young public footprint made it a riskier first prototype target.

### Shared Synthetic Dataset

The hands-on evaluations used the same fictional freelancer scenario. The baseline transaction fixture contained synthetic income, expenses, interest, charitable contributions, and estimated payments. The evaluation checklist defined expected comparable totals, including an ending checking balance of `8964.77`, freelance gross receipts of `10250.00`, interest income of `77.75`, Schedule C-style cash expenses before mileage of `1142.98`, Schedule C-style net before mileage of `9107.02`, cash charitable contributions of `370.00`, estimated federal tax payments of `1050.00`, and business miles preserved without assigning a deduction value. A standard added transaction, `TADD`, represented a software expense and changed the expected checking balance to `8939.78` and Schedule C-style cash expenses to `1167.97`.

That shared data made the evaluations comparable without forcing every tool into the same shape. Bookkeeping and personal-finance systems could import or model transaction rows and report balances. Tax calculation tools could receive summarized profile facts. Form engines could map the same facts into return entries. The method therefore measured both direct workflow support and the amount of wrapper logic required to reach an equivalent result.

### Failure Testing and Evidence Rules

Failure behavior was part of the evaluation rather than an afterthought. The shared failure checklist tested malformed dates, invalid amounts, unknown categories or accounts, missing files, and duplicate transaction IDs where applicable. The point was not to punish tools for being permissive in their native domain. Accounting systems often allow new accounts because that is useful in normal bookkeeping. The point was to identify where a tax-adjacent wrapper would need stricter validation before letting data enter a report or downstream calculation.

Claims in the final report are meant to trace back to local evidence files. Command output was saved under `evidence/commands/`, reusable fixtures under `evidence/fixtures/`, tool findings under `tool_records/`, and synthesis artifacts under `research/`. This matters because project websites, release pages, repository statistics, and API documentation can change quickly. The report should distinguish between durable findings from hands-on artifacts and point-in-time public metadata that may need refresh.

## 3. Landscape

The open-source tax-tooling landscape is best understood as a chain of roles rather than as one product category. A consumer tax workflow can begin with bank-file import, move through bookkeeping or budgeting, produce income and expense summaries, map those summaries to tax concepts, calculate liability, produce forms, validate filing artifacts, and possibly interact with submission systems. The evaluated ecosystem has strong pieces in several parts of that chain, but the pieces do not currently form one complete, low-friction open-source stack.

| Landscape layer | Representative projects from the research | Main integration pattern | Report interpretation |
|---|---|---|---|
| Import and conversion infrastructure | hledger CSV rules, ofxtools, ofxstatement, beangulp, smart_importer, beancount-import, ledger-autosync, Firefly III Data Importer | Convert bank exports or CSV/OFX/QIF-style data into bookkeeping records. | Essential substrate, but usually not a standalone tax product. |
| Plain-text accounting and CLI/file workflows | hledger, Beancount, Ledger CLI, Fava, Paisa | Versionable files, command-line reports, parser libraries, JSON/CSV exports, web views. | Strongest transparent bookkeeping layer; tax semantics require mapping. |
| Personal-finance applications | Actual Budget, Firefly III, GnuCash, KMyMoney, HomeBank, Money Manager Ex | Local app APIs, CLIs, REST APIs, desktop files, SQLite/XML stores, import/export flows. | Strong real-world finance systems; most are tax-adjacent rather than tax-preparation tools. |
| Tax calculation and policy models | tenforty, OpenTaxSolver, PSL Tax-Calculator, PolicyEngine US, IRS Tax Withholding Estimator | Python libraries, CLI calculators, policy variables, form-oriented text inputs, rules engines. | Useful for calculation or policy modeling, but generally not row-level bookkeeping systems. |
| Form-level tax engines and consumer return apps | Filed Open Tax Engine, UsTaxes, HabuTax, OpenTaxSolver, IRS Direct File/OpenFile as references | Form schemas, JSON or text inputs, PDF or MeF-adjacent output, app-internal state. | Closest to return preparation; integration maturity and supported-year scope vary heavily. |
| Filing and submission reference points | IRS Direct File posture, MeF XML concepts, Filed export evidence | Government or export-adjacent artifacts rather than general public filing APIs. | Important context, but not a green light for production third-party filing. |

Plain-text accounting tools are the cleanest bookkeeping substrate. hledger, Beancount, and Ledger CLI all make financial records inspectable and scriptable in ways that are friendly to adapters. hledger stood out in this project because it combined CSV rules, read-only CLI report execution, JSON output, and a documented hledger-web JSON API surface. Beancount remained a strong backup because of its Python ecosystem and explicit ledger language. Ledger CLI remained important as the historical baseline. The landscape lesson is that these tools are excellent at producing trustworthy accounting summaries, but they do not know which summaries are legally sufficient for a tax return. Any tax-aware use needs an explicit mapping layer and conservative validation.

Personal-finance applications offer a different kind of value. Actual Budget and Firefly III are both much closer to consumer finance workflows than raw ledger files, but they expose different integration models. Actual is local-first and scriptable through an official Node API and stable CLI. Firefly III is self-hosted and REST-first, with a JSON API and a visible third-party ecosystem. Mature desktop tools such as GnuCash, KMyMoney, HomeBank, and Money Manager Ex are relevant because many consumers already think in terms of GUI finance applications, but their automation paths are more likely to involve local files, optional bindings, import/export workflows, or database formats than a single clean API. Across this category, native tax support is thin; the tools can store and summarize facts, not decide tax treatment.

Import and conversion tools are easy to underestimate. In practice, many integrations begin with CSV, OFX, QIF, or proprietary bank exports. Projects such as ofxtools, ofxstatement, beangulp, smart_importer, beancount-import, ledger-autosync, Firefly III Data Importer, and hledger CSV rules show that open-source finance workflows already have a lot of prior art around ingestion and categorization. For this project, they support the larger argument that the best near-term architecture starts before tax forms: normalize financial facts, preserve source identifiers, validate categories, and only then summarize for tax-aware tools.

Tax calculation libraries and policy models solve a different problem. tenforty was the strongest lightweight calculation component evaluated hands-on because it exposes a compact Python function surface and returns structured results. OpenTaxSolver has older, more mature tax-form heritage, but its practical integration story is text and PDF oriented rather than API oriented. PSL Tax-Calculator and PolicyEngine US are important examples of mature programmatic tax modeling, but they are not consumer return-preparation products in the same sense as a form engine or filing app. The landscape lesson is that tax calculation can be very programmatic without being a complete consumer filing workflow.

Form-level tax engines and consumer return apps sit closest to tax preparation. Filed Open Tax Engine was the highest-upside hands-on candidate because it exposed a CLI with JSON form entries, node/schema inspection, validation, line outputs, and forced MeF XML export evidence. It also carried the largest caution flags among evaluated tools: a small public footprint, dual AGPL/commercial licensing, validation/export noise, and input-validation gaps that would need wrapper controls. UsTaxes, HabuTax, OpenTaxSolver, IRS Direct File, and OpenFile matter in this same landscape because they show different approaches to form logic, PDF workflows, and official or forked reference architectures. The key distinction is that being closer to a return form does not automatically make a tool safer or easier to integrate.

Government and filing-adjacent projects require especially careful framing. IRS Direct File and OpenFile are useful architecture references, especially around fact graphs, form translation, and state or MeF-style concepts, but the evidence captured for this project treated Direct File as unavailable/reference-only rather than as an active third-party filing channel. Filed Open Tax Engine's MeF XML export evidence is meaningful, but export-adjacent output is not the same as live submission capability. The report should therefore avoid implying that any evaluated open-source path provides production e-file submission.

The shortlist was chosen to make those landscape roles concrete. hledger represented the file/CLI/JSON accounting path. Actual Budget represented a local app API/CLI path. Firefly III represented a REST-first self-hosted finance path. tenforty represented a tax-calculation library path. Filed Open Tax Engine represented a form-level tax-engine path. Together they showed the central pattern: open-source tools can expose excellent individual surfaces, but the safe integration layer is the missing connective tissue.

That pattern shaped the prototype recommendation. The project did not attempt to build a filing bot. It selected hledger for a conservative bookkeeping-to-summary adapter because hledger's raw strengths were practical and its weaknesses were manageable with wrapper validation. The adapter can reject unknown categories, duplicate IDs, bad signs, malformed dates, and unsupported tax hints before running read-only hledger reports. It can then return normalized JSON with balances, income and expense totals, Schedule C-style summaries, preserved noncomputed facts, warnings, and explicit unsupported capabilities. This is the landscape finding in working form: the most credible first step is not end-to-end tax filing, but a validated fact layer that keeps later tax calculation or form generation honest.

## Local Evidence Used

- `README.md`
- `codex_execution_plan_ai_tax_tooling.md`
- `day_by_day_ai_tax_tooling_phases.md`
- `research/longlist.md`
- `research/project_health_snapshot.md`
- `research/programmatic_surface_survey.md`
- `research/shortlist.md`
- `research/evaluation_checklist.md`
- `research/comparison_matrix.md`
- `research/prototype_target_decision.md`
- `tool_records/tool_1.md` through `tool_records/tool_5.md`
- `evidence/synthetic_dataset.md`
- `evidence/fixtures/`
- `evidence/commands/`
- `prototype/design.md`
- `prototype/README.md`
- `prototype/retrospective.md`
