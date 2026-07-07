# Programmatic Surface Survey

Day 6 artifact for Phase 6: Programmatic Surface Survey.

Planned phase date: 07-06-2026. Executed on 07-06-2026.

## Purpose

This survey compares how the strongest candidate tools can be driven from code before any Week 2 hands-on installation. It focuses on documented automation surfaces, machine-readable inputs and outputs, and the risk that a prototype would need to parse human-oriented UI or prose instead of using stable structures.

Surface confidence labels:

- Documented stable: official docs describe a public CLI, API, library, schema, file format, or data contract that looks intended for routine use.
- Documented but constrained: official docs describe the surface, but setup, version, language, platform, or workflow constraints are material.
- Experimental or new: the surface is intentionally new, young, or not yet broadly proven.
- Inferred: the surface exists in source files, data files, or architecture docs, but is not presented as a public integration API.
- Unclear: source evidence did not establish a practical automation surface.

## Executive Findings

- Best code-facing candidates overall: hledger, Actual Budget, Firefly III, Beancount, tenforty, and Filed Open Tax Engine.
- Best low-setup prototype paths: hledger via plain-text journals plus JSON/CSV reports, Beancount via text files plus Python loader/query tooling, and tenforty via a direct Python function interface.
- Best app/API paths: Firefly III for a true REST JSON API, and Actual Budget for an official Node API plus a JSON-first CLI. Actual's docs are explicit that it is not an HTTP/REST API surface.
- Best tax-form or tax-calculation paths: tenforty, Filed Open Tax Engine, OpenTaxSolver, and UsTaxes. They are not equivalent: tenforty is a Python wrapper/calculation bridge, Filed is a new CLI/JSON tax engine, OpenTaxSolver is a mature text/PDF tax-form tool, and UsTaxes is a client-side form-prep app with useful source schemas but no obvious external API.
- Weakest prototype fits despite landscape value: IRS Direct File, OpenFile, and IRS Tax Withholding Estimator. They are valuable public-code/reference architectures, but they are not active consumer integration targets for this project.
- Most important Day 7 tradeoff: choose whether the shortlist is centered on reusable integration mechanics (hledger, Actual, Firefly, Beancount) or tax-form specificity (tenforty, Filed, OpenTaxSolver, UsTaxes). A balanced shortlist should include both.

## Surface Matrix

| Candidate | Primary code-facing surfaces | Surface confidence | Structured input | Structured output | Day 7 implication | Evidence |
|---|---|---|---|---|---|---|
| hledger | CLI, plain-text journal, CSV/SSV/TSV import rules, JSON/CSV/SQL/HTML report output, hledger-web JSON API | Documented stable | Journal files, CSV/SSV/TSV plus rules files, command arguments | JSON, CSV, SQL, HTML, text; web API JSON | Strongest file/CLI/API hybrid. Shortlist unless a pure REST app is prioritized over plain-text accounting. | [DOC-HLEDGER-CLI], [DOC-HLEDGER-WEB], [DOC-HLEDGER-CSV] |
| Actual Budget | Official Node package, stable CLI, ActualQL query CLI, local/sync budget files | Documented stable, but not REST | Node API calls, CLI JSON/file inputs, server config, local data directory | JSON default, table, CSV; Node objects | Very strong app-style candidate if Node is acceptable. Good contrast to Firefly because it is local-first and non-REST. | [DOC-ACTUAL-API], [DOC-ACTUAL-CLI] |
| Firefly III | REST JSON API, generated API spec/source, data importer with CLI/API import surfaces | Documented stable, setup-heavy | JSON API payloads, personal access/OAuth-style auth, CSV/CAMT import through importer | JSON API responses, import results | Strongest REST candidate; keep if the shortlist needs a self-hosted app with true HTTP API coverage. AGPL and Docker/setup cost matter. | [DOC-FIREFLY-API], [REPO-FIREFLY-API], [REPO-FIREFLY-IMPORTER] |
| Beancount | Plain-text Beancount language, Python API/reference, CLI checks/reports/query, plugins/importers | Documented stable, with v2/v3 tooling caveat | Beancount text files, Python data structures, importer output | Python objects, CSV/HTML/text/report tables, Beancount syntax | Strong transparent-data candidate. Verify current Beancount 3 command names and importer path during hands-on work. | [DOC-BEANCOUNT], [DOC-BEANCOUNT-LANG], [DOC-BEANCOUNT-TOOLS] |
| Ledger CLI | CLI reports, plain-text journal, CSV/XML/lisp-style outputs, Python/C++ extension docs | Documented stable for CLI/file; API docs are older/lower-priority | Ledger journal text, CSV conversion command | Text, CSV, XML, price DB, lisp/org-style outputs | Good baseline, but hledger likely wins for JSON/web API and Beancount wins for Python-native parsing. | [DOC-LEDGER], [DOC-LEDGER-CSV], [DOC-LEDGER-XML], [DOC-LEDGER-PY] |
| GnuCash | GUI app, `gnucash-cli` reports/quotes, optional Python bindings, XML/SQL storage, QIF/OFX/HBCI import | Documented but constrained | GnuCash book files, QIF/OFX/HBCI/CSV-style imports, optional Python scripts | HTML/report exports, book storage, quote output; not JSON-first | Keep as mature desktop comparator. Prototype only if local Windows CLI/bindings are smooth. | [DOC-GNUCASH-PY], [DOC-GNUCASH-IFACES], [DOC-GNUCASH-CLI] |
| OpenTaxSolver | Core command-line taxsolve programs, GUI wrapper, line-oriented text input files, PDF fill workflow | Documented stable but not API-oriented | Text files with tax line labels, form templates, Form 8949 CSV | Text `_out.txt` results, filled PDFs | Keep as legacy tax-form comparator. Weak for an API wrapper unless text input/output is enough. | [DOC-OTS], [DOC-OTS-INPUT], [DOC-OTS-HOWITWORKS] |
| UsTaxes | Client-side React/Tauri app, Redux/localStorage data model, TypeScript form logic, year-specific PDF schemas | Inferred/public source, no public external API | UI form state, TypeScript data model, schema folders for PDF contract tests | Generated PDFs; internal calculated form values | Strong consumer-return codebase, but poor external integration surface. Evaluate if tax-form coverage matters more than API cleanliness. | [REPO-USTAXES], [DOC-USTAXES-ARCH], [REPO-USTAXES-SCHEMAS] |
| tenforty | Python package over OpenTaxSolver, `evaluate_return` and `evaluate_returns`, validated inputs, dataframe-friendly batch evaluation | Documented stable-looking package API | Python keyword arguments with documented domains; list-valued sweep inputs | Pydantic model/dict for single return, Polars dataframe for sweeps | Strongest lightweight programmatic tax-calculation bridge. Not a filing/form-prep product, but very prototype-friendly. | [REPO-TENFORTY], [PYPI-TENFORTY] |
| Filed Open Tax Engine | Single-binary CLI, node/schema inspection, JSON form entry commands, validation, MeF XML/PDF export claims, MCP/agent workflow | Experimental or new | JSON form entries, inspected node schemas, CLI return store | JSON, MeF XML, filled PDFs, dependency graph JSON | Highest tax-specific demo upside, but maturity and accuracy need hands-on verification before recommendation. | [REPO-FILED-OPENTAX], [DOC-FILED-OPENTAX] |
| PSL Tax-Calculator | Python package, `tc` CLI, CSV filing-unit inputs, policy/reform inputs, variable documentation | Documented stable | CSV records with documented variable names and required fields; policy/reform files | CLI output files/tables, Python objects/dataframes | Excellent policy-model comparator; not a consumer return-prep or filing tool. Keep if the report needs a mature tax-model API example. | [DOC-TAXCALC-CLI], [DOC-TAXCALC-PY] |
| PolicyEngine US | Python rules engine package for US tax-benefit rules and microsimulation | Documented stable at project level, less consumer-filing oriented | Python package/rules inputs; household/microsimulation data | Python calculation results/model outputs | Keep as rules-as-code comparator, not a consumer filing prototype target. | [REPO-POLICYENGINE-US] |
| IRS Direct File | Public reference source, Fact Graph architecture, MeF/state-transfer concepts | Reference-only | Internal app/state data and public-code architecture | Form translations, MeF-oriented artifacts in upstream architecture | Do not shortlist as active integration target because the public service is unavailable/reference-only. | [GH-DIRECT-FILE], [IRS-DIRECT-FILE], [NOTE-DAY5] |
| OpenFile | Direct File fork/reference app | Reference/cautionary | Inherited Direct File-style app data | Inherited Direct File-style outputs | Use only as architecture/caution evidence unless mentor wants Direct File fork analysis. | [GH-OPENFILE], [DOC-OPENFILE], [NOTE-DAY5] |
| IRS Tax Withholding Estimator | Official public withholding-estimator codebase | Reference-only | Internal estimator inputs/code paths | W-4/W-4P-oriented estimator outputs | Useful official transparency example; out of scope for return-prep prototype. | [GH-IRS-TWE], [NOTE-DAY5] |

## Candidate Notes

### hledger

hledger has the cleanest combination of plain-text durability and structured automation. The CLI reads journal files and delimited files, can be driven with explicit `-f` inputs, and offers strict/checking modes. The manual describes report output to HTML, CSV, JSON, and SQL, and hledger-web adds a JSON-over-HTTP surface. CSV/SSV/TSV imports are documented through rules files rather than ad hoc parsing. This makes hledger one of the safest Day 7 choices for a synthetic-data prototype: generate CSV or journal data, run reports, and consume JSON.

Status: shortlist-favorable.

### Actual Budget

Actual is not a REST API candidate, and that distinction matters. Its docs say the supported programmatic surface is the official `@actual-app/api` Node package, which works over a local copy of budget data and can connect to a server for sync. The CLI is unusually strong: config/env support, JSON as the default output format, CSV/table alternatives, transaction add/import commands, and ActualQL query support. This is a better code surface than most desktop personal-finance tools, while still representing a realistic local-first consumer budgeting app.

Status: shortlist-favorable, especially if Node is acceptable.

### Firefly III

Firefly III is the clearest REST-first personal-finance candidate. Search-accessible official docs describe a REST-based JSON API, and the API-docs repository stores endpoint source and generated specification files that can be downloaded into API tools. The Data Importer also supports automation-oriented import flows and file formats including CSV and CAMT. The cost is setup: this is a self-hosted web application with auth, database, Docker/server configuration, and AGPL implications.

Status: shortlist-favorable if REST API coverage is a priority.

### Beancount

Beancount remains a strong transparent-data candidate because the source of truth is a plain-text accounting language backed by Python parser/loader APIs, plugins, query tooling, and importer ecosystem. The docs also describe report generation via web/report/query tools and CSV/HTML-style outputs. One caveat: parts of the "running tools" documentation explicitly refer to v2 tools and note deprecation in v3, so hands-on evaluation should verify current Beancount 3 commands rather than assuming older tool names.

Status: shortlist-favorable, with tooling-version verification.

### Ledger CLI

Ledger is the canonical plain-text CLI accounting baseline. It never mutates the input journal during analysis, can emit CSV and XML, and documents Python/C++ extension surfaces. Its integration story is still more parse-and-wrap than hledger or Beancount: JSON is not the main path, and the practical prototype surface is likely journal generation plus CLI report consumption.

Status: keep as baseline or backup; hledger/Beancount are stronger primary candidates.

### GnuCash

GnuCash has a real automation story, but it is uneven. `gnucash-cli` supports report and quote-oriented automation, Python bindings exist, and GnuCash can store data in XML or SQL-backed books. The binding docs warn that Python support is optional and build/package dependent. The wiki also warns that direct SQL updates are effectively unsafe without the GnuCash API, and that much of the external-interface page is descriptive rather than authoritative. This makes GnuCash valuable as the mature desktop representative, but not the easiest prototype target on Windows.

Status: keep as desktop comparator; prototype only after local verification.

### OpenTaxSolver

OpenTaxSolver is closer to real US tax-form calculation than the bookkeeping tools, but it exposes a form-specific text workflow rather than a modern API. Inputs are line-oriented text files keyed to tax-form lines; the GUI runs the same core taxsolve programs; outputs are screen text, `_out.txt` files, and filled PDF forms. Form 8949 CSV support is useful but narrow. For integration, OTS is plausible if the prototype frames itself as a file adapter around templates and text outputs, not as a general API.

Status: keep as tax-form comparator; lower prototype priority.

### UsTaxes

UsTaxes is highly relevant to consumer 1040 workflows, but the code-facing surface is mostly internal. The README describes a client-side web/desktop app, localStorage persistence, and supported 2020-2025 federal inputs/forms. Architecture docs identify a Redux data model, TypeScript form logic, PDF export pipeline, and year-specific schema folders for PDF field contract tests. That is useful for research and potential source-level experimentation, but it is not a documented external CLI, library, or REST API.

Status: keep if consumer-return coverage matters; weaker for thin integration.

### tenforty

tenforty is the cleanest tax-calculation library surface found so far. It wraps OpenTaxSolver behind Python functions, documents valid input arguments, validates inputs, returns a Pydantic model for single returns, and returns Polars dataframes for multi-scenario sweeps. It is tax-calculation oriented rather than filing oriented, but the API is small, typed enough to wrap, and easy to demo with synthetic values.

Status: strong tax-calculation shortlist candidate.

### Filed Open Tax Engine

Filed Open Tax Engine is purpose-built for code and agents: a single CLI, JSON-oriented form entries, node/schema inspection, return creation and validation, dependency-graph output, and claimed MeF XML/PDF export. The website also advertises an MCP/agent workflow. The risk is maturity: the public footprint is young, licensing is dual AGPL/commercial, and accuracy needs direct verification. It should not displace mature tools solely on promise, but it is a high-upside Week 2 evaluation candidate.

Status: shortlist only with explicit maturity caveat.

### PSL Tax-Calculator

Tax-Calculator is a mature programmatic tax model, not a consumer filing tool. Its CLI accepts CSV filing-unit records whose variable names match documented input variables; its Python interface is meant for model use. This is valuable for comparison because it shows what a well-developed tax computation API looks like, but it does not generate consumer 1040 workflows or filing artifacts in the way UsTaxes, OTS, or Filed aim to.

Status: keep as policy-model comparator, not prototype target unless scope shifts.

### PolicyEngine US

PolicyEngine US is another rules-as-code comparator. Its public description is a Python package containing a US tax-benefit rules engine and microsimulation data generation. It is useful for discussing maintainable policy logic, but it is not a consumer tax-return product. It should stay in the report as a contrast category unless the mentor wants policy modeling over filing/prep integration.

Status: keep as comparator, not prototype target.

## Supporting Import Infrastructure

The import-layer tools from Day 5 remain important because many practical integrations will start from bank exports rather than tax forms:

- ofxtools: Python OFX parser/client/generator; current enough to support a synthetic OFX ingestion experiment.
- ofxstatement: CLI and plugin system for converting bank statements to OFX; useful prior art for import plugins.
- beangulp, smart_importer, beancount-import: Beancount import and reconciliation substrate.
- ledger-autosync: prior art for OFX/bank-sync into Ledger journals.
- hledger CSV rules: the most direct import mechanism if the prototype is CSV-to-ledger-to-report.

These tools should support the shortlist rather than become standalone shortlist entries.

## Day 7 Shortlist Pressure

Recommended shortlist shape for Phase 7:

1. hledger - best all-around file/CLI/JSON accounting integration candidate.
2. Actual Budget - best local-first app API/CLI candidate.
3. Firefly III - best REST JSON personal-finance candidate.
4. tenforty - best lightweight tax-calculation library candidate.
5. One of Beancount, OpenTaxSolver, UsTaxes, or Filed Open Tax Engine depending on desired balance:
   - Choose Beancount for transparent accounting data and Python parsing.
   - Choose OpenTaxSolver for mature tax-form heritage.
   - Choose UsTaxes for consumer 1040 app coverage.
   - Choose Filed for agent-oriented CLI/JSON tax-engine upside, with maturity risk stated clearly.

If the shortlist must be capped at four, drop either Firefly III or Actual Budget based on whether the mentor prefers REST-first or local-first app integration.

## Open Questions For Day 7

- Does the shortlist need both Actual and Firefly, or is one app/API representative enough?
- Should Filed Open Tax Engine be included as a high-upside candidate despite being new?
- Is tenforty's tax-calculation scope enough for the tax-specific slot, or should the shortlist include a form/PDF-oriented tool too?
- Should GnuCash be evaluated hands-on as the mature desktop representative even if it is unlikely to become the prototype target?
- How much weight should AGPL obligations receive for a prototype wrapper that may expose network access?

## Source Index

- [DOC-HLEDGER-CLI] hledger manual, https://hledger.org/1.52/hledger.html, accessed 07-06-2026.
- [DOC-HLEDGER-WEB] hledger-web manual, https://hledger.org/1.52/hledger-web.html, accessed 07-06-2026.
- [DOC-HLEDGER-CSV] hledger CSV import tutorial, https://hledger.org/import-csv.html, accessed 07-06-2026.
- [DOC-ACTUAL-API] Actual Budget API docs, https://actualbudget.org/docs/api/, accessed 07-06-2026.
- [DOC-ACTUAL-CLI] Actual Budget CLI docs, https://actualbudget.org/docs/api/cli/, accessed 07-06-2026.
- [DOC-FIREFLY-API] Firefly III API docs/search result, https://docs.firefly-iii.org/references/firefly-iii/api/ and https://api-docs.firefly-iii.org/, accessed 07-06-2026.
- [REPO-FIREFLY-API] Firefly III API docs repository, https://github.com/firefly-iii/api-docs, accessed 07-06-2026.
- [REPO-FIREFLY-IMPORTER] Firefly III Data Importer repository, https://github.com/firefly-iii/data-importer, accessed 07-06-2026.
- [DOC-BEANCOUNT] Beancount documentation index, https://beancount.github.io/docs/, accessed 07-06-2026.
- [DOC-BEANCOUNT-LANG] Beancount language syntax, https://beancount.github.io/docs/beancount_language_syntax.html, accessed 07-06-2026.
- [DOC-BEANCOUNT-TOOLS] Running Beancount and generating reports, https://beancount.github.io/docs/running_beancount_and_generating_reports.html, accessed 07-06-2026.
- [DOC-LEDGER] Ledger manual, https://ledger-cli.org/doc/ledger3.html, accessed 07-06-2026.
- [DOC-LEDGER-CSV] Ledger manual, CSV command and convert command sections, https://ledger-cli.org/doc/ledger3.html, accessed 07-06-2026.
- [DOC-LEDGER-XML] Ledger manual, XML command section, https://ledger-cli.org/doc/ledger3.html, accessed 07-06-2026.
- [DOC-LEDGER-PY] Ledger manual, Python extension section, https://ledger-cli.org/doc/ledger3.html, accessed 07-06-2026.
- [DOC-GNUCASH-PY] GnuCash Python bindings guide, https://www.gnucash.org/docs/v5/C/gnucash-guide/ch_python_bindings.html, accessed 07-06-2026.
- [DOC-GNUCASH-IFACES] GnuCash external interfaces wiki, https://wiki.gnucash.org/wiki/List_of_external_software_interfaces, accessed 07-06-2026.
- [DOC-GNUCASH-CLI] GnuCash command-line documentation/search result, https://www.gnucash.org/docs/v5/C/gnucash-manual/fq-command-line.html and https://wiki.gnucash.org/wiki/GnuCash_on_the_Command_Line, accessed 07-06-2026.
- [DOC-OTS] OpenTaxSolver home, https://opentaxsolver.sourceforge.net/, accessed 07-06-2026.
- [DOC-OTS-INPUT] OpenTaxSolver input format, https://opentaxsolver.sourceforge.net/input_format.html, accessed 07-06-2026.
- [DOC-OTS-HOWITWORKS] OpenTaxSolver how it works, https://opentaxsolver.sourceforge.net/howitworks.html, accessed 07-06-2026.
- [REPO-USTAXES] UsTaxes repository, https://github.com/ustaxes/UsTaxes, accessed 07-06-2026.
- [DOC-USTAXES-ARCH] UsTaxes architecture docs, https://github.com/ustaxes/UsTaxes/blob/master/docs/ARCHITECTURE.md, accessed 07-06-2026.
- [REPO-USTAXES-SCHEMAS] UsTaxes schema directory, https://github.com/ustaxes/UsTaxes/tree/master/schemas, accessed 07-06-2026.
- [REPO-TENFORTY] tenforty repository, https://github.com/mmacpherson/tenforty, accessed 07-06-2026.
- [PYPI-TENFORTY] tenforty PyPI, https://pypi.org/project/tenforty/, accessed 07-06-2026.
- [REPO-FILED-OPENTAX] Filed Open Tax Engine repository, https://github.com/filedcom/opentax, accessed 07-06-2026.
- [DOC-FILED-OPENTAX] Filed Open Tax Engine website, https://opentax.filed.com/, accessed 07-06-2026.
- [DOC-TAXCALC-CLI] Tax-Calculator CLI docs, https://taxcalc.pslmodels.org/guide/cli.html, accessed 07-06-2026.
- [DOC-TAXCALC-PY] Tax-Calculator Python interface docs, https://taxcalc.pslmodels.org/guide/python_interface.html, accessed 07-06-2026.
- [REPO-POLICYENGINE-US] PolicyEngine US repository, https://github.com/PolicyEngine/policyengine-us, accessed 07-06-2026.
- [GH-DIRECT-FILE] IRS Direct File repository, https://github.com/IRS-Public/direct-file, accessed 07-05-2026 in Day 5 snapshot.
- [IRS-DIRECT-FILE] IRS Direct File status page, https://www.irs.gov/filing/irs-direct-file-for-free, accessed 07-05-2026 in Day 5 snapshot.
- [GH-OPENFILE] OpenFile repository, https://github.com/openfiletax/openfile, accessed 07-05-2026 in Day 5 snapshot.
- [DOC-OPENFILE] OpenFile docs, https://docs.openfile.tax/en/latest/reference.html, accessed 07-05-2026 in Day 5 snapshot.
- [GH-IRS-TWE] IRS Tax Withholding Estimator repository, https://github.com/IRS-Public/tax-withholding-estimator, accessed 07-05-2026 in Day 5 snapshot.
- [NOTE-DAY5] Local Day 5 health snapshot, `research/project_health_snapshot.md`.
