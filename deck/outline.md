# Presentation Deck Outline

Day 28 planned date: 07-28-2026. Executed early on 07-20-2026 at user request.

## Draft Status

This is the slide-by-slide outline for a 20-30 minute mentor or portfolio presentation. It translates `report/full_report_draft.md` into a talk, keeps the prototype demo in the main story, and identifies the comparison visuals that matter most.

This presentation is educational research and prototype documentation. It is not tax advice, tax preparation, filing software, or a recommendation to use any tool with real taxpayer data.

## Talk Goal

By the end of the talk, the audience should understand:

- What open-source consumer tax and bookkeeping tooling exists.
- Which integration surfaces are realistic: CLI, API, REST, file format, schema, library, or report export.
- Why the evaluated tools do not form a complete open-source consumer filing stack.
- Why the project recommends a validated bookkeeping fact layer first.
- What the hledger prototype proves, and what it deliberately does not claim.

Core message:

> Open-source bookkeeping and tax tools expose useful programmatic surfaces, but the safest near-term integration is a guarded fact layer that turns synthetic bookkeeping records into validated, tax-adjacent summaries for later downstream tools.

## Suggested Timing

| Segment | Slides | Target time |
|---|---:|---:|
| Opening and scope | 1-4 | 4 min |
| Method and landscape | 5-7 | 5 min |
| Tool findings and comparison | 8-12 | 8 min |
| Prototype demo | 13-15 | 7 min |
| Recommendation and close | 16-18 | 5 min |
| Total | 18 | 29 min |

For a 20 minute version, combine slides 8 and 9, skip slide 11, and keep the demo to one live/replay pass plus one result slide.

## Story Arc

1. Start with the research question: can open-source tax-adjacent tools be driven safely from code?
2. Establish boundaries: synthetic data only, no filing claims, no real taxpayer automation.
3. Show the evidence funnel and the ecosystem map.
4. Compare the five hands-on tools by role, not by popularity.
5. State the core gap: bookkeeping tools have records; tax tools need summarized facts; filing-ready output is not solved here.
6. Demonstrate the prototype as the concrete bridge from synthetic transactions to validated facts.
7. End with the recommendation: hledger-backed fact layer first, then tax calculation or form-level experiments later.

## Slide Outline

### 1. Open-Source Tax Tooling: What Can Actually Be Integrated?

Time: 1 min

Purpose: Open with the project title and the practical integration question.

Key points:

- Internship project on open-source consumer tax tooling and programmatic surfaces.
- Focus is feasibility of integration, not building a tax product.
- Final deliverables: report, prototype, deck.

Visual:

- Clean title slide with a small pipeline motif: transactions -> summaries -> tax-aware tools.

Source:

- `README.md`
- `report/full_report_draft.md`

### 2. Research Question

Time: 1.5 min

Purpose: Make the study specific before introducing tools.

Key points:

- What tools exist around consumer and freelancer tax-adjacent workflows?
- Can they be connected through APIs, CLIs, file formats, schemas, libraries, or exports?
- Which integration path is useful without overclaiming filing readiness?

Visual:

- One large question with three small labels: ecosystem, integration surface, safe workflow.

Source:

- `README.md`
- `codex_execution_plan_ai_tax_tooling.md`

### 3. Scope and Safety Boundary

Time: 1.5 min

Purpose: Prevent the audience from hearing the project as tax-prep or e-file automation.

Key points:

- Synthetic freelancer data only.
- No real taxpayer data, bank data, PII, secrets, or live filing credentials.
- The prototype does not calculate tax liability, generate Form 1040, validate a return, produce PDFs, create reliable MeF artifacts, or file electronically.

Visual:

- Boundary diagram: "in scope" synthetic bookkeeping facts; "out of scope" filing, advice, real taxpayer data.

Source:

- `report/full_report_draft.md`
- `prototype/README.md`

### 4. Evaluation Method

Time: 2 min

Purpose: Show that conclusions came from evidence, not vibes.

Key points:

- Longlist -> health snapshot -> programmatic-surface survey -> shortlist -> hands-on evaluation -> failure testing -> comparison -> prototype decision.
- Every hands-on tool used the same synthetic scenario where possible.
- Scoring was directional; integration fit and safety mattered more than a single numeric winner.

Visual:

- Funnel or horizontal process strip with artifact names under each phase.

Source:

- `research/longlist.md`
- `research/project_health_snapshot.md`
- `research/programmatic_surface_survey.md`
- `research/shortlist.md`
- `research/evaluation_checklist.md`

### 5. Ecosystem Map

Time: 2 min

Purpose: Organize the open-source landscape by role.

Key points:

- Import/conversion tools move bank-style data into records.
- Bookkeeping and personal-finance tools model transactions and balances.
- Tax calculation libraries consume summarized facts.
- Form-level engines model return lines and filing-adjacent artifacts.
- Government/reference projects are useful context but not public third-party filing channels for this prototype.

Visual:

- Main visual: role map from import -> bookkeeping -> tax calculation -> forms/output -> filing-adjacent references.

Source:

- `report/full_report_draft.md`
- `research/programmatic_surface_survey.md`

### 6. Shortlist: Five Tools, Five Roles

Time: 2 min

Purpose: Explain why these tools were evaluated deeply.

Key points:

- hledger: plain-text file/CLI/JSON accounting.
- Actual Budget: local-first app/API and CLI.
- Firefly III: self-hosted REST JSON personal finance.
- tenforty: lightweight tax-liability calculation library.
- Filed Open Tax Engine: form-level federal tax engine.

Visual:

- Five-column role table with one "best role" label per tool.

Source:

- `research/shortlist.md`
- `tool_records/tool_1.md` through `tool_records/tool_5.md`

### 7. Shared Synthetic Freelancer Scenario

Time: 1.5 min

Purpose: Make the hands-on comparison concrete.

Key points:

- 2025 fictional freelancer with checking transactions, income, software/office expenses, interest income, charitable placeholders, estimated payments, and mileage metadata.
- Baseline checking balance: `8964.77`.
- Standard added transaction `TADD` changes checking balance to `8939.78`.

Visual:

- Compact transaction sample plus expected totals.

Source:

- `evidence/synthetic_dataset.md`
- `evidence/fixtures/synthetic_freelancer_transactions.csv`

### 8. Bookkeeping Tools: hledger, Actual Budget, Firefly III

Time: 3 min

Purpose: Compare the three transaction-modeling paths.

Key points:

- All three can support transaction-to-balance and transaction-to-summary workflows.
- hledger has the cleanest transparent file/CLI/JSON path.
- Actual Budget is the best local app/API backup.
- Firefly III is the strongest REST comparator but has heavier setup, auth, state, and AGPL hosting considerations.

Visual:

- Small comparison table: surface, setup weight, structured output, key caution.

Source:

- `tool_records/tool_1.md`
- `tool_records/tool_2.md`
- `tool_records/tool_3.md`
- `research/comparison_matrix.md`

### 9. Tax-Oriented Tools: tenforty and Filed Open Tax Engine

Time: 2.5 min

Purpose: Explain what tax-specific candidates add and why they are not complete answers.

Key points:

- tenforty calculates liability from summarized facts, but it does not import transactions or create filing artifacts.
- Filed Open Tax Engine reaches closest to form-level outputs, but maturity, validation/export noise, duplicate/date acceptance, and licensing need caution.
- Both are downstream candidates after bookkeeping facts are validated.

Visual:

- Two-card comparison: "calculation component" vs "form-level experiment".

Source:

- `tool_records/tool_4.md`
- `tool_records/tool_5.md`
- `report/full_report_draft.md`

### 10. Main Finding: Useful Pieces, No Complete Stack

Time: 2 min

Purpose: Land the central report conclusion.

Key points:

- Bookkeeping tools are good at records and summaries.
- Tax tools need already-summarized facts.
- Form-level engines are promising but not proof of validation-clean filing readiness.
- No evaluated project combines low-friction bookkeeping, complete US tax prep, validated filing artifacts, and production-ready third-party integration.

Visual:

- Capability gap ladder: transactions, balances, tax summaries, tax liability, form output, validation-clean filing, e-file submission.

Source:

- `report/full_report_draft.md`
- `research/comparison_matrix.md`

### 11. Comparison Visual: What Each Tool Is Best For

Time: 2 min

Purpose: Give the audience one scan-friendly comparison before the prototype.

Key points:

- hledger: transparent bookkeeping and reportable facts.
- Actual Budget: local app/API alternative.
- Firefly III: REST-first comparator.
- tenforty: downstream tax calculation.
- Filed Open Tax Engine: cautious form-level experimentation.

Visual:

- Main comparison matrix by use case and recommendation posture.

Source:

- `report/full_report_draft.md`
- `report/comparison_recommendation_draft.md`

### 12. Prototype Thesis

Time: 1.5 min

Purpose: Set up the demo with a clear claim.

Key points:

- The prototype is a synthetic-only hledger adapter.
- It proves a thin wrapper can validate controlled transactions, run read-only hledger reports, reconcile output, and emit normalized JSON.
- The prototype is a fact layer, not a filing bot.

Visual:

- One-sentence thesis plus architecture mini-flow.

Source:

- `prototype/design.md`
- `prototype/README.md`
- `report/prototype_writeup_draft.md`

### 13. Prototype Architecture

Time: 2 min

Purpose: Explain what the audience will see during the demo.

Key points:

- Inputs: synthetic CSV, synthetic context, category map.
- Wrapper preflight: dates, amounts, signs, IDs, accounts, categories, tax hints, synthetic acknowledgement.
- Execution: scratch CSV and read-only hledger reports.
- Output: reconciled JSON with balances, tax-adjacent summaries, warnings, limitations, and provenance.

Visual:

- Architecture flow: synthetic CSV + context -> validation -> hledger reports -> reconciliation -> normalized JSON -> execution lab.

Source:

- `prototype/design.md`
- `prototype/hledger_adapter/`
- `prototype/execution_lab/`

### 14. Demo: Run or Replay the Synthetic Workflow

Time: 3 min

Purpose: Show the project functioning.

Demo path:

- Preferred local command: `python run_day20_demo.py --json`.
- UI path: open the execution lab and run the synthetic demo when hledger is configured.
- Fallback: use verified replay from committed command evidence if live hledger execution is unavailable.

What to narrate:

- Validation happens before hledger sees the data.
- The adapter uses scratch copies and read-only commands.
- The execution lab shows command-to-result progression and evidence traceability.

Visual:

- Live terminal or execution-lab screen, not both unless time allows.

Source:

- `run_day20_demo.py`
- `prototype/execution_lab/`
- `evidence/commands/07-13-2026_hledger-adapter_day18_summary.txt`
- `evidence/commands/07-13-2026_hledger-adapter_day19_failures.txt`

### 15. Demo Readout: Results and Safety

Time: 2 min

Purpose: Turn the demo output into evidence.

Key points:

- 19 transactions, 38 postings, 14 accounts.
- Ending checking balance: `8964.77`.
- Bookkeeping revenue: `10327.75`; expenses: `1512.98`; net: `8814.77`.
- Schedule C-style net before mileage: `9107.02`.
- Interest income: `77.75`; cash charitable contributions: `370.00`; estimated payments tracked: `1050.00`.
- Failure matrix: 15/15 passed.

Visual:

- Result tiles plus small safety matrix.

Source:

- `report/full_report_draft.md`
- `prototype/run_day20_demo.py`
- `prototype/tests/run_failure_matrix.py`

### 16. Recommendation

Time: 2.5 min

Purpose: State the decision in use-case terms.

Key points:

- Use hledger as the prototype-backed pattern for transparent bookkeeping and reportable facts.
- Use Actual Budget when local app/API workflow or MIT license posture matters more.
- Treat Firefly III as the REST API comparator.
- Pair hledger summaries with tenforty later for tax-liability scenarios.
- Explore Filed Open Tax Engine cautiously for form-level experiments.
- Do not claim production filing or live taxpayer automation.

Visual:

- Recommendation stack or decision table by use case.

Source:

- `report/full_report_draft.md`
- `research/prototype_target_decision.md`

### 17. Limitations and Future Work

Time: 2 min

Purpose: Keep the conclusion honest and turn gaps into next actions.

Key points:

- Synthetic data only and one controlled freelancer fixture.
- Point-in-time tool evaluations need a public metadata refresh before final publication.
- License analysis is directional, not legal advice.
- Next best work: pair hledger summaries with tenforty, revisit Filed validation/export behavior, add screenshots/figures, expand synthetic data, analyze GPL/AGPL deployment implications.

Visual:

- Two columns: "Known limits" and "Next work".

Source:

- `report/full_report_draft.md`
- `prototype/retrospective.md`

### 18. Closing: What the Project Proves

Time: 1 min

Purpose: End with the portfolio-ready takeaway.

Key points:

- The project maps a fragmented ecosystem into integration roles.
- It evaluates five representative tools with shared synthetic evidence.
- It builds a working adapter that produces validated bookkeeping facts.
- The safe path is not automatic filing; it is trustworthy structured facts that downstream tools can consume.

Visual:

- Final takeaway sentence plus the prototype command.

Source:

- `report/full_report_draft.md`
- `prototype/README.md`

## Demo Placement Decision

Place the prototype demo after the cross-tool comparison and before the final recommendation. That ordering lets the audience see the core evidence before hearing the final architecture recommendation. It also keeps the prototype from feeling like an appendix.

## Priority Visuals For Day 29

Build these visuals first:

- Ecosystem role map: import -> bookkeeping -> tax calculation -> form/output -> filing-adjacent references.
- Five-tool role matrix with best role and main caution.
- Capability gap ladder showing why there is no complete open-source filing stack in the evaluated set.
- Prototype architecture flow from synthetic CSV to normalized JSON and execution lab.
- Demo result/safety readout with core totals and 15/15 failure matrix.
- Recommendation table by use case.

Optional visuals:

- Screenshot of the execution lab home view.
- Screenshot of a selected lifecycle phase popup.
- Small command-output excerpt from `python run_day20_demo.py --json`.

## Day 29 Build Notes

- Build the actual deck from this outline, not directly from the report.
- Keep each slide to one main claim.
- Prefer tables, architecture diagrams, and execution-lab screenshots over text-heavy paragraphs.
- Put dense evidence paths in speaker notes or appendix slides.
- Keep prototype caveats visible on the scope, demo, and recommendation slides.
- Include the demo command and the verified replay fallback in speaker notes.

## Appendix Candidates

Use appendix slides only if the final deck needs backup detail:

- Full tool capability matrix.
- Synthetic dataset details.
- Failure matrix cases.
- Evidence index.
- Publication checklist and metadata-refresh caveat.

