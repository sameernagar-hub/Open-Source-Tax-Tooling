# Comparison and Recommendation Draft

Day 25 artifact for Phase 25: Comparison and Recommendation Draft.

Planned phase date: 07-25-2026. Executed early on 07-16-2026 at user request.

## Drafting Note

This is draft prose for the final report's comparison and recommendation sections. It is based on `research/comparison_matrix.md`, `research/prototype_target_decision.md`, the Day 23 opening draft, the Day 24 tool-evaluation draft, the five completed tool records, and the frozen prototype evidence. It does not refresh public project metadata.

## 5. Cross-Tool Comparison

The evaluated tools split into three roles that should not be collapsed into one ranking. hledger, Actual Budget, and Firefly III are bookkeeping or personal-finance integration surfaces. tenforty is a tax-liability calculation component. Filed Open Tax Engine is a form-level federal tax engine. The most important comparison finding is that the open-source ecosystem has strong pieces at each layer, but the safe connective tissue between layers still has to be built.

| Candidate | Best role | Primary surface tested | Strongest evidence | Main limitation | Recommendation posture |
|---|---|---|---|---|---|
| hledger | Transparent bookkeeping-to-summary adapter | CLI, CSV rules, JSON output | Loaded 19 synthetic transactions, produced JSON, matched checking balance `8964.77`, and became the Week 3 prototype base. | No native tax forms, tax calculation, payments/refund model, PDF, MeF, or e-file path. | Primary prototype target and recommended transparent bookkeeping layer. |
| Actual Budget | Local-first app/API backup | Official Node API and stable CLI | Created scratch budget, loaded synthetic transactions, matched baseline and after-`TADD` balances, exported normalized JSON. | No tax forms; direct-add path accepted unknown category IDs and duplicate imported IDs. | Best local app/API alternative, especially when MIT licensing matters. |
| Firefly III | REST-first personal-finance comparator | REST JSON API | Docker/API workflow posted transactions, returned expected balances, and exposed structured account/category/transaction data. | Docker/auth/database setup, AGPL obligations, unknown-category auto-create, no tax forms. | Best REST API comparator, but heavier than needed for first prototype. |
| tenforty | Tax-liability calculation component | Python library | Mapped summarized profile facts into `evaluate_return`, producing federal total tax `1286.78` baseline and `1283.25` after `TADD`. | No transaction import, balances, refunds/payments, complete forms, PDF, or e-file path; native Windows install failed. | Best downstream calculation component after a bookkeeping summary layer. |
| Filed Open Tax Engine | Form-level federal tax experimentation | CLI, JSON form entries, validation, MeF export | Produced TY2025 1040/Schedule C/SE-style outputs, total tax `1286.7809`, payments `1699.00`, and refund `412.2191`. | Young project, AGPL/commercial licensing, validation/export noise, duplicate input acceptance, malformed date acceptance. | Highest-upside form engine, but a cautious research recommendation. |

The comparison also shows why "API support" is not one thing. hledger is not a web API in the tested workflow, but it is highly automatable because local files and JSON reports are stable enough for a small wrapper. Actual Budget is API-backed but local-first, using an official Node package rather than REST. Firefly III is the cleanest HTTP API candidate. tenforty is a library API with no account or transaction model. Filed Open Tax Engine is a CLI and schema API around tax forms rather than financial transactions. A good integration plan has to choose the surface that matches the intended workflow.

### Capability Summary

| Capability | hledger | Actual Budget | Firefly III | tenforty | Filed Open Tax Engine |
|---|---|---|---|---|---|
| Transaction import or modeling | Strong | Strong | Strong | Unsupported | Unsupported; requires summarized form entries |
| Balance workflow | Strong | Strong | Strong | Unsupported | Unsupported |
| Structured output | JSON reports | API objects / CLI JSON | REST JSON | Python model / dataframe | CLI JSON / forced MeF XML |
| Tax-line mapping | Manual account/category mapping | Manual category/note mapping | Manual category/tag/note mapping | Aggregate tax inputs | Form-entry and line-level fields |
| Form 1040 support | Unsupported | Unsupported | Unsupported | Partial calculation outputs | Strongest tested form-level output |
| Schedule C support | Manual summaries | Manual summaries | Manual summaries | Net self-employment input | Gross receipts and expense lines tested |
| Payments/refund support | Manual tracking only | Manual tracking only | Manual tracking only | Unsupported | Tested estimated payments and refund output |
| PDF or MeF/e-file path | Unsupported | Unsupported | Unsupported | Unsupported | MeF export exists but was blocked without force |
| Best safety pattern | Validate before hledger CLI | Validate before direct API mutation | Validate before REST mutation | Validate domains and recompute sanity fields | Validate before form entry/export |
| Setup weight | Low | Low to moderate | Moderate to high | Moderate | Low to moderate |

The comparable workflow results reinforce the split. The bookkeeping tools all matched the baseline checking balance of `8964.77` and after-`TADD` checking balance of `8939.78`. tenforty and Filed Open Tax Engine did not model checking balances, but they both calculated a federal tax change from the same Schedule C-style `TADD` adjustment. tenforty produced total federal tax of `1286.78` baseline and `1283.25` after `TADD`. Filed Open Tax Engine produced closely aligned totals of `1286.7809` baseline and `1283.2500` after `TADD`, while also modeling payments and refund output.

### Safety Comparison

All five tools need wrapper-side guardrails for production-like automation. The details differ:

| Safety area | Main finding |
|---|---|
| Malformed fields | hledger, Actual, and Firefly rejected malformed dates in the tested transaction workflows; Filed accepted a malformed taxpayer date string because the field was schema-typed as a string; tenforty had no date field in the evaluated API. |
| Invalid amounts | All applicable tools rejected clearly invalid amount strings. |
| Unknown categories/accounts | hledger accepted implicit accounts, Actual direct-add accepted a bogus category as uncategorized, and Firefly auto-created an unknown category. Tax-controlled wrappers need allowlists. |
| Duplicate source records | hledger accepted duplicate IDs, Actual direct-add accepted duplicate imported IDs, Firefly rejected duplicate hashes when configured, and Filed accepted duplicate 1099-INT entries and double-counted interest. |
| Export/file readiness | Filed's normal MeF export was blocked by reject-level validation rules; forced XML export worked but emitted warnings. Successful calculation should not be equated with a filing-ready return. |
| Local isolation | hledger and tenforty were easiest to isolate; Actual used a local scratch data directory; Firefly used scratch containers; Filed used an isolated working directory and local `.state`. |

The safety finding is not that the tools are broken. It is that each tool is optimized for its own domain. Personal-finance systems often make it easy to create categories; accounting tools often allow new accounts; tax engines may validate schema types without knowing whether a source document is duplicated. A tax-adjacent integration layer must be stricter than the underlying tool.

### Licensing and Deployment

License posture affects integration design. Actual Budget and tenforty are the easiest evaluated tools to imagine in wrapper experiments because their visible licenses are MIT, though tenforty's Open Tax Solver relationship still deserves separate review. hledger's GPL-3.0-or-later license is compatible with local research but matters for redistribution or embedding. Firefly III's AGPL-3.0 license is especially relevant if a wrapper becomes a hosted network service. Filed Open Tax Engine's AGPL/commercial dual licensing makes it important to separate local research from distribution or hosted-product claims.

## 6. Recommendation

The recommended near-term integration is not a filing bot. It is a validated bookkeeping fact layer that can feed tax-aware tools later. The safest first build is a small wrapper around hledger that accepts synthetic transactions, rejects bad or unsupported inputs before execution, runs read-only hledger reports, and returns normalized JSON summaries with explicit limitations.

### Recommended Path

| Use case | Recommendation | Why |
|---|---|---|
| Transparent bookkeeping and reportable facts | Use hledger first. | It has the clearest file/CLI/JSON path, low setup friction, inspectable inputs, deterministic reports, and proven prototype evidence. |
| Local app/API integration | Use Actual Budget as the backup. | It has an official Node API, stable CLI, MIT license, scratch local budget support, and successful transaction-to-summary evidence. |
| REST API integration | Use Firefly III as the comparator. | It has the strongest REST JSON API and realistic self-hosted finance workflow, but setup/auth/licensing overhead makes it heavier than hledger for the first prototype. |
| Tax-liability scenarios | Pair a bookkeeping summary with tenforty later. | tenforty can calculate liability from summarized facts, but it needs a separate transaction and validation layer. |
| Tax-form experimentation | Explore Filed Open Tax Engine cautiously. | It exposes the richest form-level surface, but validation/export noise, maturity, and licensing require guardrails before relying on it. |
| Production filing or live taxpayer automation | Do not claim support from this project. | None of the evaluated paths proves validation-clean production filing, live e-file submission, tax advice, or safe real-data handling. |

### Why hledger Was Chosen for the Prototype

hledger was selected because it gave the best combination of evidence, feasibility, safety, and explanatory clarity. The prototype needed to show that a real open-source tool could be connected to a wrapper and driven repeatably from synthetic data. It also needed to avoid overstating tax capability. hledger fit that narrow target better than the other candidates.

The decisive points were:

| Criterion | hledger finding |
|---|---|
| Real programmatic surface | Documented CLI, CSV rules, JSON export, and optional hledger-web surface. |
| Feasibility | The Day 9 workflow already ran with local files, and the Week 3 adapter later proved the path with a one-command demo. |
| Transparency | Reviewers can inspect the CSV, rules file, command calls, hledger JSON, normalized JSON, and failure behavior. |
| Safety | The wrapper can run read-only reports against scratch data and reject unknown categories, duplicate IDs, bad signs, malformed dates, and unsupported tax hints before hledger runs. |
| Honest scope | hledger does not calculate taxes or file returns, which forces the prototype to describe itself as bookkeeping infrastructure rather than tax preparation. |

Actual Budget was the closest backup. It preserved the same transaction-to-summary shape and had an integration-friendly MIT license, but hledger's plain files and CLI reports were more transparent for a research prototype. Firefly III offered the best REST API, but Docker, authentication, database state, and AGPL concerns would have shifted too much of Week 3 toward server setup. tenforty and Filed Open Tax Engine were more tax-specific, but neither imported raw transactions; using either as the primary prototype would have skipped the bookkeeping integration problem that the project set out to study.

### Tools To Avoid For Automation

"Avoid" here means avoid as a primary automation target for this internship's conservative prototype, not avoid as projects.

| Automation target to avoid | Reason |
|---|---|
| GUI-only or scrape-oriented workflows | They are fragile, hard to validate, and weaker evidence than documented CLIs, APIs, libraries, schemas, or file formats. |
| Active filing claims from reference-only government code | IRS Direct File and OpenFile are valuable architecture references, but this project should not present them as active third-party filing channels. |
| Raw personal-finance category auto-creation for tax mapping | hledger, Actual, and Firefly all showed category/account/id behaviors that are too permissive without wrapper controls. |
| Forced tax-form export as proof of filing readiness | Filed Open Tax Engine's forced MeF XML export is useful evidence, but normal export was blocked and warnings remained. |
| Real taxpayer or live account automation | The repository is synthetic-data-only and does not evaluate production privacy, consent, credentials, filing authorization, or tax-advice obligations. |

### Final Recommendation Wording

The strongest recommendation is conservative:

Use hledger as the prototype-backed pattern for an open-source bookkeeping fact layer. Treat Actual Budget as the best local app/API alternative, Firefly III as the best REST API comparator, tenforty as the most promising downstream tax-liability component, and Filed Open Tax Engine as the highest-upside but highest-caution form-level candidate. Do not frame any evaluated tool as a complete open-source consumer filing stack.

This recommendation turns the evaluation into an architecture: first validate and summarize financial facts; then, if the use case requires it, pass those facts into a tax calculation or form-level component with additional validation. That layered approach is slower than claiming an end-to-end tax agent, but it is much closer to what the evidence supports.

## Evidence Used

- `research/comparison_matrix.md`
- `research/prototype_target_decision.md`
- `report/opening_sections_draft.md`
- `report/tool_evaluations_draft.md`
- `tool_records/tool_1.md` through `tool_records/tool_5.md`
- `prototype/design.md`
- `prototype/README.md`
- `prototype/retrospective.md`
- `evidence/commands/`
- `evidence/fixtures/`
