# Shortlist Decision

Day 7 artifact for Phase 7: Shortlist Decision.

Planned phase date: 07-07-2026. Executed on 07-07-2026.

## Purpose

Choose 3-5 tools for Week 2 hands-on evaluation based on the longlist, project-health snapshot, and programmatic-surface survey. The shortlist is balance-constrained: scores matter, but the final set must cover plain-text accounting, app/API-backed personal finance, and tax-oriented workflows.

Primary evidence base:

- `research/longlist.md`
- `research/project_health_snapshot.md`
- `research/programmatic_surface_survey.md`
- `research/exclusions.md`

## Decision Summary

Shortlist for Week 2:

1. hledger
2. Actual Budget
3. Firefly III
4. tenforty
5. Filed Open Tax Engine

This set gives the project one strong file/CLI/JSON accounting candidate, two contrasting personal-finance app candidates, and two tax-oriented candidates. It deliberately includes one mature REST app and one local-first app because the final recommendation needs to compare real integration styles, not only bookkeeping formats.

Primary backups:

- Beancount, if the plain-text slot should favor Python-native parsing and importer ecosystem depth over hledger's JSON/API output.
- OpenTaxSolver, if Filed Open Tax Engine proves too immature or if the mentor wants mature tax-form heritage over agent-oriented CLI/JSON design.
- UsTaxes, if the hands-on evaluation needs source-level consumer 1040 workflow coverage rather than a clean external API.
- GnuCash, if a mature desktop personal-finance comparator becomes important enough to absorb Windows setup and binding risk.

## Scoring Rubric

Scores are 1-5, where 5 is strongest. The total is a guide rather than an automatic ranking.

| Dimension | Meaning |
|---|---|
| Relevance | Fit with consumer/freelancer bookkeeping, tax prep, tax calculation, or tax-relevant reporting. |
| Integration surface | Quality of documented CLI, API, library, file format, schema, REST endpoint, or structured I/O. |
| Project health | Activity, release cadence, documentation, contributor/community signals, and evidence quality. |
| Tax workflow fit | Closeness to tax-line mapping, tax calculation, tax-form generation, filing-adjacent workflow, or useful tax reporting. |
| Demo potential | Likelihood of a clear Week 2 hands-on demo using synthetic data within reasonable setup time. |

## Score Matrix

| Candidate | Relevance | Integration surface | Project health | Tax workflow fit | Demo potential | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| tenforty | 5 | 5 | 3 | 5 | 5 | 23 | Shortlist |
| hledger | 4 | 5 | 5 | 3 | 5 | 22 | Shortlist |
| Filed Open Tax Engine | 5 | 5 | 2 | 5 | 5 | 22 | Shortlist with maturity caveat |
| Actual Budget | 4 | 5 | 5 | 2 | 5 | 21 | Shortlist |
| Firefly III | 4 | 5 | 5 | 2 | 4 | 20 | Shortlist |
| Beancount | 4 | 4 | 5 | 3 | 4 | 20 | Backup; strong but overlaps hledger |
| OpenTaxSolver | 5 | 2 | 4 | 5 | 3 | 19 | Backup; mature tax-form comparator |
| PSL Tax-Calculator | 2 | 5 | 5 | 3 | 4 | 19 | Comparator; policy model rather than consumer filing |
| UsTaxes | 5 | 2 | 3 | 5 | 3 | 18 | Backup; strong source-level 1040 app, weak external surface |
| GnuCash | 4 | 3 | 5 | 2 | 3 | 17 | Mature desktop comparator; setup risk |
| PolicyEngine US | 2 | 4 | 5 | 3 | 3 | 17 | Comparator; rules engine rather than filing tool |
| Ledger CLI | 3 | 3 | 4 | 2 | 3 | 15 | Baseline only; hledger is stronger for structured output |

## Shortlisted Tools

### hledger

hledger made the shortlist because it is the strongest all-around plain-text accounting integration candidate. The Day 6 survey found a stable CLI, explicit journal and CSV-rules workflows, structured JSON/CSV/SQL/HTML output, and hledger-web JSON API routes. It is tax-adjacent rather than tax-specific, but it is likely the safest first hands-on evaluation: synthetic transactions can be generated as CSV or journal entries, reports can be produced from the command line, and structured output can be consumed without scraping a GUI.

### Actual Budget

Actual Budget made the shortlist as the best local-first app/API-backed personal-finance candidate. Its official Node API and stable CLI give it a clearer automation story than most consumer finance apps, and the CLI's JSON/table/CSV output options make it practical for scripted evaluation. It is not a REST API, which is precisely why it is valuable next to Firefly III: the report can compare local library/CLI integration against server/API integration.

### Firefly III

Firefly III made the shortlist as the strongest REST-first personal-finance candidate. Its dedicated JSON API documentation, API-spec repository, data importer, and third-party ecosystem make it the cleanest representative of self-hosted finance software with HTTP integration. The main risk is setup weight: Docker/server configuration, authentication, database state, and AGPL licensing all need to be captured during hands-on evaluation.

### tenforty

tenforty made the shortlist because it is the cleanest lightweight tax-calculation library surface found so far. It wraps OpenTaxSolver behind Python functions, documents accepted inputs, validates arguments, returns structured Python/Pydantic-style results for a single return, and supports dataframe-style scenario sweeps. It does not appear to be a full filing or form-preparation product, but it is highly suitable for a synthetic tax-calculation demo and helps keep the shortlist directly tax-relevant.

### Filed Open Tax Engine

Filed Open Tax Engine made the shortlist as the high-upside tax-specific CLI/JSON candidate. Its public positioning is unusually aligned with this project's question: single-binary CLI, JSON form entries, node/schema inspection, validation, dependency graph output, and claimed MeF XML/PDF export. The caveat is large and should stay visible: it is new, has a small public footprint, dual AGPL/commercial posture, and needs hands-on accuracy and maturity checks before any recommendation.

## Major Exclusions And Deferrals

Beancount is the hardest exclusion. It scored as strongly as Firefly III and has a healthy plain-text/Python ecosystem, but including both Beancount and hledger would over-weight plain-text accounting during a week that also needs app/API and tax-specific coverage. Beancount should be the first backup if hledger installation fails or if Python-native loader/query behavior becomes more valuable than hledger's JSON/web API surfaces.

Ledger CLI is kept as historical baseline rather than a Week 2 target. It remains important in the landscape, but hledger offers a more compelling structured-output and web/API story for this project's prototype direction.

GnuCash, KMyMoney, HomeBank, and Money Manager Ex remain landscape comparators. They are mature and relevant to personal finance, but their strongest integration paths appear to be desktop automation, files, optional bindings, local databases, or import/export workflows. GnuCash is the best of this group for future hands-on work, but it carries Windows CLI/binding uncertainty and weaker direct tax-workflow fit than the selected tools.

OpenTaxSolver and UsTaxes are important tax-form candidates but were not selected for the first shortlist. OpenTaxSolver has mature tax-form heritage and current tax-year support, but its external automation story is text/PDF-oriented rather than API-oriented. UsTaxes has direct consumer 1040 relevance and useful source schemas, but its public external integration surface is mostly inferred from internal app architecture. Either can replace Filed Open Tax Engine if the new engine proves too immature.

PSL Tax-Calculator and PolicyEngine US are strong programmatic tax-policy or rules-as-code comparators, not consumer return-preparation tools. They should remain in the report as examples of mature tax computation infrastructure, but they would shift Week 2 away from consumer bookkeeping and filing-adjacent workflows.

IRS Direct File, OpenFile, and the IRS Tax Withholding Estimator are reference-only for the current project. Direct File is no longer an active public filing path, OpenFile inherits Direct File complexity and accuracy/status caveats, and the Tax Withholding Estimator is a W-4/W-4P withholding tool rather than a return-prep target.

Import-layer tools such as ofxtools, ofxstatement, beangulp, smart_importer, beancount-import, ledger-autosync, and hledger CSV rules should support the selected evaluations instead of becoming standalone shortlist entries. They are most useful as evidence for how real-world bank data could enter the shortlisted systems.

## Week 2 Evaluation Order

Recommended order:

1. hledger - fastest likely path to a repeatable synthetic-data harness and structured report output.
2. Actual Budget - local-first app API/CLI contrast with hledger.
3. Firefly III - REST JSON API and self-hosted setup comparison.
4. tenforty - lightweight tax-calculation library and structured output.
5. Filed Open Tax Engine - tax-specific CLI/JSON engine, with OpenTaxSolver or UsTaxes as fallback if setup, maturity, or accuracy concerns block useful evaluation.

## Risks To Carry Forward

- hledger and Actual are bookkeeping/budgeting tools, so tax relevance must come from reporting, categorization, and mapping rather than built-in return preparation.
- Firefly III setup may consume more time than the plain-text or library candidates; capture setup cost as an evaluation finding, not just friction.
- tenforty depends on OpenTaxSolver behavior and needs Windows/local installation verification.
- Filed Open Tax Engine should be tested skeptically because its public footprint is small and its claims are high-value.
- AGPL obligations matter for Firefly III and Filed Open Tax Engine if any prototype exposes a network service or is redistributed.

## Done Criteria Check

- Scored plausible candidates across relevance, integration surface, project health, tax workflow fit, and demo potential.
- Chose a balanced five-tool shortlist with plain-text accounting, full personal-finance/API-backed apps, and tax-oriented tools.
- Wrote rationale for each shortlisted tool.
- Wrote exclusion and deferral rationale for major non-shortlisted tools.

## Source Index

- [LONG-DAY3-4] `research/longlist.md`, created during Days 3-4 and expanded during discovery.
- [HEALTH-DAY5] `research/project_health_snapshot.md`, accessed as the normalized health evidence for this decision.
- [SURFACE-DAY6] `research/programmatic_surface_survey.md`, accessed as the primary programmatic-surface evidence for this decision.
- [EXCL-DAY4] `research/exclusions.md`, accessed for prior exclusion and deferral rationale.

Detailed external source URLs and source IDs remain in those upstream artifacts to avoid duplicating the full evidence index here.
