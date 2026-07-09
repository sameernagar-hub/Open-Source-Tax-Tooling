# Synthetic Fixture Evidence

Store generated synthetic datasets, example inputs, and expected outputs here.

Never store real taxpayer data, real financial account data, personally identifiable information, secrets, or live filing credentials.

Current fixtures:

- `synthetic_freelancer_transactions.csv`: canonical Day 8 transaction fixture.
- `synthetic_freelancer_tax_profile.json`: canonical Day 8 tax-profile fixture.
- `hledger_synthetic_freelancer.rules`: hledger CSV conversion rules used for Day 9.
- `hledger_synthetic_freelancer_tadd.csv`: hledger add-transaction test fixture for `TADD`.
- `hledger_bad_date.csv`, `hledger_bad_amount.csv`, `hledger_unknown_account.csv`, `hledger_duplicate_t001.csv`: hledger Day 9 failure-test fixtures.
- `hledger_day9_baseline_print.json`, `hledger_day9_baseline_checking_balance.json`, `hledger_day9_with_tadd_print.json`: hledger Day 9 JSON export evidence.
- `actual_day10_evaluate.mjs`: Actual Budget Day 10 Node API evaluation helper.
- `actual_day10_summary.json`: Actual Budget Day 10 normalized workflow, totals, category, account, and failure-test evidence.
- `actual_day10_transactions_after_add.json`: Actual Budget Day 10 normalized transaction export after the standard `TADD` add-transaction test.
- `firefly_day11_evaluate.mjs`: Firefly III Day 11 REST API evaluation helper.
- `firefly_day11_summary.json`: Firefly III Day 11 normalized workflow, totals, insight, and mapping evidence.
- `firefly_day11_transactions_after_add.json`: Firefly III Day 11 normalized transaction export after the standard `TADD` add-transaction test.
- `firefly_day11_failure_results.json`: Firefly III Day 11 failure-test results.
- `tenforty_day12_evaluate.py`: tenforty Day 12 Python evaluation helper.
- `tenforty_day12_summary.json`: tenforty Day 12 normalized tax-calculation, mapping, sanity-check, and failure-test evidence.
- `tenforty_day12_scenario_grid.json`: tenforty Day 12 Polars scenario sweep exported as JSON.
- `tenforty_day12_failure_results.json`: tenforty Day 12 failure-test results.
- `filed_opentax_day13_evaluate.mjs`: Filed Open Tax Engine Day 13 CLI evaluation helper.
- `filed_opentax_day13_summary.json`: Filed Open Tax Engine Day 13 normalized workflow, tax-line, validation, export, mapping, and comparison evidence.
- `filed_opentax_day13_failure_results.json`: Filed Open Tax Engine Day 13 failure-test results.
- `filed_opentax_day13_baseline_mef.xml`: Forced MeF XML export from the Day 13 synthetic baseline return, retained as export evidence only.
