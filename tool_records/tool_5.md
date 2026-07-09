# Tool Record: Filed Open Tax Engine

## Status

| Field | Value |
|---|---|
| Tool slug | `filed-opentax` |
| Category | tax calculation / tax form generation / tax submission-adjacent infrastructure |
| Record status | complete draft |
| Last updated | 07-09-2026 UTC / 07-08-2026 PDT |
| Evaluator | Codex |
| Evaluation phase | Phase 13 |

## One-Sentence Summary

Filed Open Tax Engine is a current, agent-oriented US federal 1040 CLI with structured JSON form inputs, line-level outputs, validation, dependency graph inspection, and MeF XML export, making it the highest-upside form-level tax engine evaluated so far but also the newest and roughest candidate.

## Identity

| Field | Value | Evidence |
|---|---|---|
| Primary project URL | https://github.com/filedcom/opentax | [FILED-REPO] |
| Source repository | https://github.com/filedcom/opentax | [FILED-REPO] |
| Documentation | Repository README and public documentation site at https://opentax.filed.com/. | [FILED-README], [FILED-DOCS] |
| License | Dual-licensed under AGPL-3.0 and a Filed commercial license. | [FILED-REPO], [FILED-LICENSE] |
| Latest visible release | `v2.0.2`, published 2026-05-11; Windows x64 asset hash matched the release metadata. | [FILED-RELEASE], `evidence/commands/07-08-2026_filed-opentax_setup.txt` |
| Main implementation language | TypeScript/Deno, distributed as single native binaries for macOS, Linux, and Windows. | [FILED-README], `evidence/commands/07-08-2026_filed-opentax_version.txt` |
| Package/distribution channel | GitHub release binaries and installer script; Day 13 used the Windows x64 release binary without global installation. | [FILED-RELEASE], `evidence/commands/07-08-2026_filed-opentax_setup.txt` |
| Maintainer or organization | Filed / `filedcom`. | [FILED-REPO] |

## Research Fit

- Workflow category: Federal individual tax calculation and form-entry engine.
- Consumer/freelancer relevance: Strong for line-level 1040, Schedule C, Schedule SE, 1099-INT, estimated payments, and refund/amount-due style workflows.
- US tax relevance: Very strong within TY2025 federal 1040 scope.
- Non-US comparator value: Not applicable; US-focused.
- Why included: It directly tests the shortlist's high-upside CLI/JSON tax-engine candidate after hledger, Actual, Firefly III, and tenforty.
- Why this might be excluded later: It is new, AGPL/commercial-licensed, its validation/export path was noisy, and some schema/domain validation gaps need wrapper-side controls.

## Programmatic Surface

| Surface | Present? | Stability | Input shape | Output shape | Evidence |
|---|---:|---|---|---|---|
| CLI | yes | current but new | Commands such as `return create`, `form add`, `return get`, `return validate`, `return export`, `node inspect`, and `node graph` | JSON for most commands, text/JSON validation, MeF XML export | `evidence/commands/07-08-2026_filed-opentax_version.txt` |
| Library/API import | source-level only | not evaluated as public library | TypeScript/Deno internals | Engine/runtime objects | [FILED-REPO] |
| REST or HTTP API | no | N/A | N/A | N/A | Day 13 evaluation |
| Plugin or extension system | yes for agent/Claude skills, not a data plugin API | experimental | Agent skill instructions | Agent workflows | [FILED-README] |
| File format or schema | yes | strong but evolving | JSON form-entry payloads validated by Zod schemas | Local `.state/returns/<id>/return.json`; computed line JSON | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Database access | local file state | simple | CLI stores local return JSON under `./.state/returns` relative to the current working directory | Local JSON files | `evidence/fixtures/filed_opentax_day13_evaluate.mjs` |
| Export format | yes | tested with caveats | Return state | MeF XML with `--force`; PDF command present but not tested | `evidence/fixtures/filed_opentax_day13_baseline_mef.xml` |

Notes:

- Documented surfaces: Single binary CLI, node/schema inspection, form-entry CRUD, return calculation, validation, dependency graph output, update command, and MeF/PDF export commands.
- Inferred surfaces: A wrapper can drive the CLI through an argument-array subprocess and parse JSON outputs; PowerShell inline JSON quoting was fragile, so Day 13 used Node `execFileSync`.
- Missing or unclear surfaces: No REST API, no bank/CSV transaction import, no native transaction ledger, no live e-file submission, and no documented stable library API for external consumers.

## Prior Art and Existing Integrations

- Third-party wrappers: None evaluated.
- Package bindings: No package-manager library binding evaluated; CLI binary is the intended integration surface.
- Plugins/extensions: Repository includes agent/Claude-oriented skills and workflow instructions.
- Example automation scripts: Day 13 added `evidence/fixtures/filed_opentax_day13_evaluate.mjs`.
- Related ecosystem tools: Contrasts with tenforty by exposing form-level schemas, estimated payments, refund output, validation, and MeF export instead of only aggregate liability calculation.
- Evidence: [FILED-README], `research/programmatic_surface_survey.md`, `evidence/fixtures/filed_opentax_day13_summary.json`.

## Setup and First Useful Operation

Environment:

- OS: Microsoft Windows 11 host.
- Runtime/package manager: No runtime required for the CLI binary; Node `v24.16.0` was used only for the Day 13 evaluation runner.
- Tool version: `opentax 2.0.2`.
- Install source: Official `opentax-windows-x64.exe` release asset downloaded to `%TEMP%\opentax-day13\opentax.exe`; SHA-256 matched the GitHub release metadata.

Commands attempted:

```text
See:
- evidence/commands/07-08-2026_filed-opentax_setup.txt
- evidence/commands/07-08-2026_filed-opentax_version.txt
- evidence/commands/07-08-2026_filed-opentax_workflow.txt
- evidence/commands/07-08-2026_filed-opentax_failure-tests.txt
```

Results:

- Time to first useful operation: Low. Downloading the 126 MB Windows binary and running `opentax version`/`node list` worked without a local build.
- First useful operation: Created a TY2025 return, added `general`, `f1099int`, `f1040es`, and `schedule_c` entries, then ran `return get`.
- First useful output: Baseline Form 1040 summary with total income `9184.77`, AGI `8541.3795`, total tax `1286.7809`, total payments `1699.00`, and refund `412.2191`.
- Setup friction: Low to moderate. The binary is easy to run, but CLI state is relative to the process working directory, and inline JSON arguments were unreliable through PowerShell native-command quoting.
- Evidence files: Listed above plus `evidence/fixtures/filed_opentax_day13_summary.json`, `evidence/fixtures/filed_opentax_day13_failure_results.json`, `evidence/fixtures/filed_opentax_day13_baseline_mef.xml`, and `evidence/fixtures/filed_opentax_day13_evaluate.mjs`.

## Synthetic Workflow Results

For Filed Open Tax Engine, the shared transaction CSV was summarized into form entries rather than imported row-by-row.

| Operation | Result | Structured output? | Evidence |
|---|---|---:|---|
| Load data | Success at tax-profile/form-entry level. The helper mapped filing status to `general`, bank interest to `f1099int`, estimated payments to `f1040es`, and freelancer income/expenses to `schedule_c`. | yes | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Add transaction | Partial/app-level adaptation. `TADD` was modeled as an extra Schedule C Part V software expense in a second return; OpenTax does not store bookkeeping transactions. | yes | `evidence/fixtures/filed_opentax_day13_summary.json` |
| List accounts | Not applicable. | N/A | Day 13 evaluation |
| Compute balance | Not applicable. | N/A | Day 13 evaluation |
| Run report | Success. `return get` produced summary fields, selected 1040 line values, forms computed, and warnings. | yes | `evidence/commands/07-08-2026_filed-opentax_workflow.txt` |
| Export result | Partial. JSON output worked well; MeF XML export without `--force` was blocked by reject-level rules; forced MeF XML exported with warnings. | yes | `evidence/fixtures/filed_opentax_day13_baseline_mef.xml` |

Key comparable totals:

| Measure | Baseline | After `TADD` |
|---|---:|---:|
| Schedule C expense total mapped | `1142.98` | `1167.97` |
| 1040 line 9 total income | `9184.77` | `9159.78` |
| 1040 line 11 AGI | `8541.3795` | `8518.1550` |
| 1040 line 15 taxable income | `0.00` | `0.00` |
| 1040 line 24 total tax | `1286.7809` | `1283.2500` |
| Federal total tax delta after `TADD` | N/A | `-3.5310` |
| 1040 line 26 estimated tax | `1050.00` | `1050.00` |
| EITC computed by engine | `649.00` | `649.00` |
| 1040 line 33 total payments | `1699.00` | `1699.00` |
| 1040 line 35a refund | `412.2191` | `415.7500` |

Additional probes:

- Forced Schedule A charity probe recorded line 12e itemized deductions of `370.00`, but did not change tax because taxable income was already zero and the liability was self-employment tax.
- `return validate --format json` on the baseline reported `1917` total rules, `1278` passed, `44` rejected, `0` alerts, and `595` skipped.
- MeF export without `--force` was blocked by reject-level rules. MeF export with `--force` produced XML but emitted warnings, including a recurring `f2441` executor-node warning and many reject rules that looked unrelated to the minimal synthetic return.

Mapping assumptions:

- `filing_status=single` mapped to OpenTax `general.filing_status=single`.
- Interest income mapped to one `f1099int` entry with `box1=77.75`.
- Schedule C gross receipts mapped to `line_1_gross_receipts=10250`.
- Software, bank fees, and professional education were placed in Schedule C Part V other expenses; office equipment, coworking, supplies, and local travel were mapped to Schedule C expense lines.
- Estimated payments were split into four equal `f1040es` payments of `262.50`.
- Mileage was not modeled because the shared synthetic profile leaves mileage deduction unset.

## Workflow Coverage

| Capability | Coverage | Notes | Evidence |
|---|---|---|---|
| Bookkeeping | unsupported | No account ledger, transaction import, or bank balance workflow. | Day 13 evaluation |
| Reporting | strong | `return get` returns summary, forms, lines, and warnings. | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Tax-line mapping | strong within tested scope | Node schemas expose line-level payload fields for 1040 inputs and schedules. | `evidence/commands/07-08-2026_filed-opentax_version.txt` |
| Form 1040 | strong but needs validation review | Produced 1040 summary and line-level outputs; validation/export warnings need deeper explanation. | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Schedule A | partial tested | Accepted cash charitable contribution and computed line 12e itemized deductions in the forced probe. | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Schedule B | partial tested | `f1099int` flowed to interest lines and Schedule B appeared in computed forms. | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Schedule C | strong tested | Accepted gross receipts and line/Part V expenses; produced Schedule C income feeding AGI and SE tax. | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Schedule D | present but not tested | Node list includes Schedule D and capital-gain forms. | `evidence/commands/07-08-2026_filed-opentax_version.txt` |
| Schedule E | present but not tested | Node list includes Schedule E and K-1 nodes. | `evidence/commands/07-08-2026_filed-opentax_version.txt` |
| Common credits | partial tested | EITC was computed automatically for the low-income self-employed profile; child/dependent credits were not tested. | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Tax form generation | partial | MeF XML export produced output only with `--force`; PDF command exists but was not tested. | `evidence/fixtures/filed_opentax_day13_baseline_mef.xml` |
| Tax-year support | narrow/current | Catalog source exposes `f1040:2025`; creating a 2024 return succeeded, but `return get` failed with `Unsupported form: f1040:2024`. | `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| E-file or submission path | export-adjacent only | MeF XML export exists, but no live submission path was evaluated and validation rejects blocked normal export. | `evidence/commands/07-08-2026_filed-opentax_workflow.txt` |
| Import from banks/files | unsupported | Requires a wrapper to summarize transactions into form entries. | Day 13 evaluation |
| Export for other systems | strong JSON, partial MeF | CLI JSON is easy to consume; MeF XML needs validation cleanup before relying on it. | Day 13 evaluation |

Stated non-goals and exclusions:

- State returns: README says additional forms and state returns are coming; Day 13 evaluated federal TY2025 only.
- Foreign filers: Not evaluated.
- Business returns: Not evaluated; node list is centered on individual return support.
- Production filing: Not evaluated; README directs filing users to IRS.gov and the Day 13 synthetic return was not fileable.
- Other: AGPL/commercial licensing must be reviewed before redistribution or network-hosted wrappers.

## Safety and Failure Behavior

| Area | Finding | Evidence |
|---|---|---|
| Dry-run or validation mode | `return validate` exists and returns a rule summary; however, baseline validation was noisy and reported many reject rules for unrelated forms. | `evidence/fixtures/filed_opentax_day13_summary.json` |
| Scratch/test data support | Good if run from an isolated working directory, because state is local under `./.state/returns`. | `evidence/fixtures/filed_opentax_day13_evaluate.mjs` |
| Destructive operations | `form update` and `form delete` exist; Day 13 did not exercise destructive actions. | `evidence/commands/07-08-2026_filed-opentax_version.txt` |
| Bad date handling | A malformed `taxpayer_dob` string of `13-40-2025` was accepted because that field is schema-typed as string. | `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| Invalid amount handling | String `not-a-number` for Schedule C gross receipts was rejected. | `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| Negative amount handling | Negative Schedule C gross receipts were rejected by the `>=0` schema constraint. | `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| Unknown account/category handling | Not applicable for accounts/categories; unknown node type was rejected clearly. | `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| Duplicate input handling | Duplicate identical `f1099int` entries were accepted and double-counted interest. A wrapper needs duplicate detection where source document IDs exist. | `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| Missing file/return handling | Missing return ID failed clearly with a missing `return.json` path. | `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| Unsupported year handling | Creating a 2024 return was accepted, but computing it failed later with `Unsupported form: f1040:2024`. | `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| Error clarity | Good for schema errors, unknown nodes, invalid JSON, and missing returns; weak for broad validation/export rule noise. | `evidence/commands/07-08-2026_filed-opentax_failure-tests.txt` |

## Project Health

| Signal | Finding | Evidence |
|---|---|---|
| Recent commits | Prior Day 5 snapshot found the public repo new and narrow, with activity around the May 2026 release. | `research/project_health_snapshot.md`, [FILED-REPO] |
| Release cadence | Latest visible release was `v2.0.2`, published 2026-05-11. | [FILED-RELEASE] |
| Annual tax-year support pattern | Current public catalog exposes TY2025 Form 1040 support only. | [FILED-CATALOG], `evidence/fixtures/filed_opentax_day13_failure_results.json` |
| Issue/PR activity | Small public footprint in earlier snapshot; not mature like hledger, Actual, or Firefly. | `research/project_health_snapshot.md` |
| Contributor signals | Strong README/agent positioning and binary releases, but the project is young. | [FILED-README], [FILED-RELEASE] |
| Documentation quality | Good for CLI onboarding and examples; schema inspection is especially useful. Validation/export limitations need more user-facing explanation. | `evidence/commands/07-08-2026_filed-opentax_version.txt` |
| Data format durability | Promising because schemas are explicit, but still evolving. | [FILED-README], `evidence/commands/07-08-2026_filed-opentax_version.txt` |
| License constraints | AGPL-3.0 plus commercial license could constrain hosted wrappers and redistribution. | [FILED-LICENSE] |

## Integration Assessment

- Best integration shape: CLI adapter that runs the binary from an isolated working directory, writes form-entry JSON through argument-array subprocess calls, parses `return get` JSON, and blocks normal export unless validation is clean.
- Thin-wrapper feasibility: High for local demos; moderate for production because validation, duplicate detection, local state management, and license constraints need design.
- Structured I/O quality: Excellent for schemas and computed line JSON; stronger form-level surface than tenforty.
- Agent-consumable workflow fit: Very strong for node inspection, dependency graph inspection, form-entry editing, and explainable 1040 line outputs.
- Main blockers: New project, AGPL/commercial licensing, no transaction import, only TY2025 evaluated, duplicate inputs accepted, malformed date string accepted, and validation/export noise.
- Best demo idea: A controlled synthetic 1040 form-entry adapter that maps a normalized freelancer profile into OpenTax nodes, explains computed Form 1040/Schedule C/SE lines, and surfaces validation rejects separately from calculation results.
- Prototype suitability: High if the Week 3 prototype should demonstrate form-level tax-engine integration; lower than tenforty/hledger if the prototype goal is a conservative, low-risk recommendation.

## Scores

| Criterion | Score | Rationale |
|---|---:|---|
| Relevance to research question | 5 | Directly targets open-source US federal tax calculation and form-level programmatic integration. |
| Programmatic surface quality | 5 | Single CLI, schema inspection, JSON form entries, computed line JSON, validation, graph output, and export commands. |
| Setup feasibility | 4 | Windows release binary worked and hash matched; binary is large and JSON quoting requires care in shells. |
| Structured input/output | 5 | Zod-backed schemas and JSON outputs are highly wrapper-friendly. |
| Workflow coverage | 4 | Strong 1040/Schedule C/SE coverage plus payments/refund; no bookkeeping import or live e-file, and export is currently noisy. |
| Safety and failure clarity | 3 | Good schema errors, but malformed dates and duplicate inputs need wrapper guards; validation/export produced broad reject noise. |
| Project health | 2 | Current-looking but young, small public footprint, and only TY2025 catalog support observed. |
| Prototype/demo potential | 4 | Excellent form-level demo upside, but maturity and licensing make it a cautious choice. |

## Evidence Index

- [x] Official project page: [FILED-REPO] https://github.com/filedcom/opentax
- [x] Source repository: [FILED-REPO] https://github.com/filedcom/opentax
- [x] License: [FILED-LICENSE] https://github.com/filedcom/opentax/blob/main/LICENSE
- [x] Release/version: [FILED-RELEASE] https://github.com/filedcom/opentax/releases/tag/v2.0.2, `evidence/commands/07-08-2026_filed-opentax_setup.txt`, `evidence/commands/07-08-2026_filed-opentax_version.txt`
- [x] Documentation: [FILED-README] https://raw.githubusercontent.com/filedcom/opentax/main/README.md, [FILED-DOCS] https://opentax.filed.com/
- [x] Command output: `evidence/commands/07-08-2026_filed-opentax_setup.txt`, `evidence/commands/07-08-2026_filed-opentax_version.txt`, `evidence/commands/07-08-2026_filed-opentax_workflow.txt`, `evidence/commands/07-08-2026_filed-opentax_failure-tests.txt`
- [x] Metadata snapshot: `research/project_health_snapshot.md`, `research/programmatic_surface_survey.md`
- [ ] Screenshots, if any: Not needed for CLI-only Day 13 evaluation.

## Open Questions

- Why does the baseline return trigger an `f2441` executor warning when no child/dependent-care input was provided?
- Why does MeF validation/export report reject rules for many forms that were not intentionally present in the synthetic return?
- Should the prototype rely on OpenTax's richer form-level surface despite its maturity risk, or use tenforty as a smaller tax-calculation component?
- Can a wrapper enforce date formats, duplicate source-document detection, and supported-year checks before calling the CLI?
- What are the practical AGPL/commercial-license implications for a demo wrapper, a hosted API, or redistribution with the binary?

## Decision Notes

Filed Open Tax Engine should remain in prototype consideration as the high-upside form-level CLI/JSON candidate. It is the only evaluated tool that combines Schedule C style inputs, 1040 line outputs, estimated payments, refund calculation, schema inspection, validation, graph output, and MeF XML export in one local CLI. The recommendation should stay cautious: for a robust Week 3 prototype, OpenTax needs wrapper-side guardrails and a clear explanation that successful calculation does not mean a validation-clean or file-ready return.

[FILED-REPO]: https://github.com/filedcom/opentax
[FILED-README]: https://raw.githubusercontent.com/filedcom/opentax/main/README.md
[FILED-DOCS]: https://opentax.filed.com/
[FILED-RELEASE]: https://github.com/filedcom/opentax/releases/tag/v2.0.2
[FILED-CATALOG]: https://raw.githubusercontent.com/filedcom/opentax/main/catalog.ts
[FILED-LICENSE]: https://github.com/filedcom/opentax/blob/main/LICENSE
