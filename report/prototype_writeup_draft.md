# Prototype Writeup Draft

Day 26 artifact for Phase 26: Prototype Writeup.

Planned phase date: 07-26-2026. Executed early on 07-16-2026 at user request.

## Drafting Note

This is draft prose for the final report's prototype section. It is based on `prototype/design.md`, `prototype/README.md`, `prototype/run_day20_demo.py`, `run_day20_demo.py`, `prototype/retrospective.md`, the execution lab implementation, and a Day 26 local run of `python run_day20_demo.py --json`.

## 6. Prototype

The prototype is a synthetic-only hledger adapter. It is a small Python wrapper that drives a real open-source bookkeeping engine through local files, command-line calls, and JSON reports, then returns normalized bookkeeping and tax-adjacent facts for another program to consume. It does not prepare a tax return, calculate tax liability, decide deductibility, generate IRS forms, estimate a refund, or file anything.

The purpose of the prototype is to make the report's recommendation concrete. The earlier evaluations showed that hledger has useful raw integration surfaces but permissive accounting behavior around unknown accounts and duplicate IDs. The prototype shows how a wrapper can keep hledger's strengths while closing those gaps before any report command runs.

### Architecture

The adapter has six layers:

| Layer | Role |
|---|---|
| Synthetic fixtures | The canonical CSV transaction fixture and optional synthetic context file provide the only supported data. |
| Static configuration | `prototype/config/category_map.json` controls allowed accounts, categories, tax hints, signs, and summary buckets; `prototype/config/hledger.csv.rules` controls CSV conversion. |
| Python preflight | The wrapper validates schema, dates, decimal money, amount direction, duplicate IDs, source account, category, tax-hint pair, context identity, mileage fields, and synthetic-data acknowledgement. |
| Scratch execution | Validated CSV and rules are copied into a fresh temporary directory; hledger receives scratch copies rather than source paths. |
| Read-only hledger reports | The wrapper invokes `print -O json`, `balance --flat -O json`, and `incomestatement --depth 3 -O json` with `shell=False`, no host ledger file, color disabled, paging disabled, timeouts, and bounded output. |
| Normalized JSON | The wrapper reconciles hledger output against the validated input, removes host-specific fields, and emits versioned JSON with transactions, accounts, summaries, warnings, limitations, and provenance. |

In text form:

```text
synthetic CSV + synthetic context + category map
  -> wrapper preflight
  -> scratch CSV and static hledger rules
  -> read-only hledger reports
  -> JSON reconciliation
  -> normalized summary JSON
  -> execution lab live run or verified replay
```

The wrapper owns the safety policy. hledger remains the accounting engine, but it is not asked to decide which categories are allowed, whether transaction IDs are unique, whether a mileage deduction applies, or whether any tax treatment is valid.

### Demo Workflow

The main reviewer command is:

```text
python run_day20_demo.py --json
```

That root-level wrapper runs `prototype/run_day20_demo.py`, which executes two commands from `prototype/`:

| Command | Purpose |
|---|---|
| `python -m hledger_adapter demo` | Runs the canonical synthetic adapter demo against the committed transaction fixture and context. |
| `python tests/run_failure_matrix.py` | Runs the safety matrix for expected bad inputs and hledger discovery failures. |

The demo reports a lifecycle suitable for the execution lab: input validation, hledger discovery, version probe, scratch setup, transaction report, balance report, income statement, reconciliation, summary aggregation, failure matrix, and cleanup.

The Next.js execution lab under `prototype/execution_lab/` exposes the same workflow to reviewers. In local mode, its `/api/run` route runs `run_day20_demo.py --json` through Node's `spawn` with `shell: false` and optional hledger binary configuration. In Vercel or replay mode, it returns a verified replay message and uses committed command evidence rather than trying to run hledger in a deployed environment.

### Setup Summary

The Python adapter uses Python 3.11+ and only the standard library. hledger is a separate prerequisite and is not bundled, downloaded, installed, or redistributed by this repository.

The adapter resolves hledger in this order:

1. Explicit `--hledger-bin PATH`.
2. `HLEDGER_BIN`.
3. `hledger` or `hledger.exe` on `PATH`.
4. On Windows, the user-scoped Winget `simonmichael.hledger` package directory.

The Day 26 local verification found hledger through `PATH` and reported:

```text
hledger 1.52.1-g3834a163b-20260428, windows-x86_64
```

The execution lab is a separate Next.js app. For local review:

```text
cd prototype/execution_lab
npm install
npm run dev
```

The report should describe the execution lab as a reviewer surface, not as a production service. It shows the synthetic input rows, command interface, phase lifecycle, output totals, safety matrix, evidence links, artifacts, and architecture notes.

### Sample Output

On 07-16-2026, `python run_day20_demo.py --json` completed with overall status `passed`. The adapter demo passed, the failure matrix passed, and every lifecycle step reported `passed`.

Key summary values from the live run:

| Measure | Value |
|---|---:|
| Transactions | `19` |
| Postings | `38` |
| Accounts | `14` |
| Reconciliation status | `passed` |
| hledger version | `hledger 1.52.1-g3834a163b-20260428, windows-x86_64` |
| Ending checking balance | `8964.77` |
| Bookkeeping revenue | `10327.75` |
| Bookkeeping expenses | `1512.98` |
| Bookkeeping net | `8814.77` |
| Schedule C-style gross receipts | `10250.00` |
| Schedule C-style cash expenses before mileage | `1142.98` |
| Schedule C-style net before mileage | `9107.02` |
| Interest income | `77.75` |
| Cash charitable contributions | `370.00` |
| Federal estimated payments tracked | `1050.00` |
| Business miles preserved | `78.2` |
| Failure matrix | `15/15` passed |
| Scratch unchanged | `true` |

The adapter deliberately keeps hledger's bookkeeping income-statement net separate from the Schedule C-style net. The hledger income statement includes interest and charity, so its net is `8814.77`. The controlled Schedule C-style summary uses only mapped freelancer gross receipts and mapped business cash expenses, so its net before mileage is `9107.02`.

The normalized output also includes unsupported capabilities:

```text
tax_liability_calculation
deductibility_determination
form_1040_generation
schedule_generation
refund_calculation
return_validation
efile_submission
```

Those fields are not decorative. They are part of the prototype's argument: useful bookkeeping summaries are not the same as tax preparation.

### Safety Choices

The prototype's safety model is intentionally conservative:

| Safety choice | Why it matters |
|---|---|
| Synthetic-only inputs | The project does not handle real taxpayer data, real bank data, PII, credentials, or filing secrets. |
| Required acknowledgement for custom runs | The adapter forces the caller to acknowledge the synthetic-only boundary, while admitting that this is not a PII detector. |
| Static category map | Unknown categories, unknown accounts, mismatched tax hints, and wrong signs fail before hledger runs. |
| Duplicate ID detection | The wrapper closes a gap observed in raw hledger evaluation, where duplicate transaction IDs were accepted. |
| Scratch copies | hledger receives temporary copies and static rules, not original fixtures or user ledgers. |
| Read-only report commands | The adapter never invokes mutating hledger commands such as `add`, `import`, or `rewrite`. |
| Argument-array subprocesses | Commands use `shell=False`; payee and memo text remain data, not shell syntax. |
| Path and output redaction | Host-absolute paths and hledger source positions are removed from normalized JSON and bounded errors. |
| Exact decimal strings | Money values are represented as exact two-decimal strings, avoiding binary floating-point drift. |
| Failure matrix | Expected bad inputs produce stable structured errors before report execution when possible. |

The Day 26 verification preserved the Day 19 safety result: 15 out of 15 cases passed, including missing acknowledgement, malformed date, invalid amount, unknown category, unknown account, duplicate ID, missing file, tax-hint mismatch, wrong sign, context failures, dry-run option conflict, missing hledger, and unusable hledger.

### Limitations

The prototype is intentionally narrow:

- It supports one canonical 2025 USD synthetic freelancer fixture and controlled categories.
- It does not accept real taxpayer or financial data.
- It does not calculate tax liability, choose tax treatment, monetize mileage, decide deductibility, generate Form 1040 or schedules, calculate refunds, validate returns, produce PDFs, create MeF XML, or file electronically.
- It does not generalize to multiple currencies, arbitrary account maps, multi-year datasets, user ledgers, hledger-web, hosted services, credentials, or live financial accounts.
- It does not bundle hledger. Reviewers need a local hledger executable for live mode or can use the execution lab's verified replay path.
- It does not provide legal or license advice. The prototype source is MIT-licensed in this repository, while hledger is a separate GPL-3.0-or-later program.
- Optional Markdown output was deferred because the JSON contract, failure matrix, and execution lab carry the strongest evidence.

### What The Prototype Proves

The prototype proves that a thin wrapper can safely drive an open-source bookkeeping CLI and produce agent-consumable facts from controlled synthetic data. It also proves that the missing layer in the ecosystem is not merely "an API." The missing layer is stricter validation, normalized output, provenance, and honest boundaries around what the underlying tool does not do.

The strongest report wording is:

The hledger adapter demonstrates a conservative integration pattern for open-source tax-adjacent tooling: validate synthetic bookkeeping records, run read-only reports through a mature accounting engine, reconcile the output, and expose normalized facts that downstream tax calculation or form engines could consume later. It is useful precisely because it stops before claiming to be tax software.

## Evidence Used

- `prototype/design.md`
- `prototype/README.md`
- `prototype/run_day20_demo.py`
- `run_day20_demo.py`
- `prototype/retrospective.md`
- `prototype/execution_lab/`
- `prototype/tests/run_failure_matrix.py`
- `prototype/hledger_adapter/`
- `prototype/config/category_map.json`
- `prototype/config/hledger.csv.rules`
- `evidence/fixtures/synthetic_freelancer_transactions.csv`
- `evidence/fixtures/synthetic_freelancer_tax_profile.json`
- `evidence/commands/07-13-2026_hledger-adapter_day18_summary.txt`
- `evidence/commands/07-13-2026_hledger-adapter_day19_failures.txt`
