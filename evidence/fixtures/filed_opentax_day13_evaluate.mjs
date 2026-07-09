import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const repoRoot = process.cwd();
const evidenceDir = path.join(repoRoot, "evidence");
const fixturesDir = path.join(evidenceDir, "fixtures");
const commandsDir = path.join(evidenceDir, "commands");
mkdirSync(fixturesDir, { recursive: true });
mkdirSync(commandsDir, { recursive: true });

const localDate = "07-08-2026";
const slug = "filed-opentax";
const opentaxBin = process.env.OPENTAX_BIN || path.join(tmpdir(), "opentax-day13", "opentax.exe");
if (!existsSync(opentaxBin)) {
  throw new Error(`OpenTax binary not found at ${opentaxBin}. Set OPENTAX_BIN to override.`);
}

const runDir = path.join(tmpdir(), "opentax-day13", "eval-run");
rmSync(runDir, { recursive: true, force: true });
mkdirSync(runDir, { recursive: true });

function quoteArg(arg) {
  if (/^[A-Za-z0-9._:/\\=-]+$/.test(arg)) return arg;
  return JSON.stringify(arg);
}

function commandLabel(args) {
  return `opentax ${args.map(quoteArg).join(" ")}`;
}

function run(args, { allowFailure = false } = {}) {
  const result = spawnSync(opentaxBin, args, {
    cwd: runDir,
    encoding: "utf8",
    maxBuffer: 25 * 1024 * 1024,
  });
  const record = {
    command: commandLabel(args),
    exitCode: result.status ?? 0,
    stdout: result.stdout.trimEnd(),
    stderr: result.stderr.trimEnd(),
  };
  if (!allowFailure && record.exitCode !== 0) {
    throw new Error(`${record.command} failed with ${record.exitCode}\n${record.stderr || record.stdout}`);
  }
  return record;
}

function parseJson(record) {
  return JSON.parse(record.stdout);
}

function section(title, records) {
  const lines = [`# ${title}`, ""];
  for (const record of records) {
    lines.push(`$ ${record.command}`);
    lines.push(`exit=${record.exitCode}`);
    if (record.stdout) {
      lines.push("stdout:");
      lines.push(record.stdout);
    }
    if (record.stderr) {
      lines.push("stderr:");
      lines.push(record.stderr);
    }
    lines.push("");
  }
  return lines.join("\n");
}

function sha256(filePath) {
  return createHash("sha256").update(readFileSync(filePath)).digest("hex");
}

function payloadArg(payload) {
  return JSON.stringify(payload);
}

function baseGeneral() {
  return {
    filing_status: "single",
    taxpayer_first_name: "Sample",
    taxpayer_last_name: "Freelancer",
    taxpayer_dob: "1990-01-01",
    taxpayer_occupation: "Freelancer",
    digital_assets: false,
  };
}

function scheduleCPayload(extraSoftwareExpense = 0) {
  const partV = [
    { description: "Software", amount: 239 },
    { description: "Bank fees", amount: 12 },
    { description: "Professional education", amount: 249 },
  ];
  if (extraSoftwareExpense > 0) {
    partV.push({
      description: "Year-end software add-transaction test",
      amount: Number(extraSoftwareExpense.toFixed(2)),
    });
  }
  return {
    line_a_principal_business: "AI engineering consulting",
    line_b_business_code: "541511",
    line_c_business_name: "Sample Freelancer",
    line_f_accounting_method: "cash",
    line_g_material_participation: true,
    line_1_gross_receipts: 10250,
    line_18_office_expense: 320,
    line_20b_rent_other: 210,
    line_22_supplies: 74.23,
    line_24a_travel: 38.75,
    part_v_other_expenses: partV,
  };
}

function scheduleCExpenseTotal(payload) {
  const direct = [
    payload.line_18_office_expense,
    payload.line_20b_rent_other,
    payload.line_22_supplies,
    payload.line_24a_travel,
  ].reduce((sum, value) => sum + Number(value || 0), 0);
  const other = payload.part_v_other_expenses.reduce((sum, item) => sum + item.amount, 0);
  return Number((direct + other).toFixed(2));
}

function createReturn() {
  const createRecord = run(["return", "create", "--year", "2025"]);
  return { record: createRecord, returnId: parseJson(createRecord).returnId };
}

function addForm(returnId, nodeType, payload) {
  return run(["form", "add", "--returnId", returnId, "--node_type", nodeType, payloadArg(payload)]);
}

function buildScenario(label, { extraSoftwareExpense = 0, scheduleA = null } = {}) {
  const records = [];
  const { record: createRecord, returnId } = createReturn();
  records.push(createRecord);
  const scheduleC = scheduleCPayload(extraSoftwareExpense);
  const additions = [
    addForm(returnId, "general", baseGeneral()),
    addForm(returnId, "f1099int", { payer_name: "Synthetic Bank", box1: 77.75 }),
    addForm(returnId, "f1040es", {
      payment_q1: 262.5,
      payment_q2: 262.5,
      payment_q3: 262.5,
      payment_q4: 262.5,
    }),
    addForm(returnId, "schedule_c", scheduleC),
  ];
  if (scheduleA) additions.push(addForm(returnId, "schedule_a", scheduleA));
  records.push(...additions);
  const listRecord = run(["form", "list", "--returnId", returnId]);
  const getRecord = run(["return", "get", "--returnId", returnId]);
  const validateRecord = run(["return", "validate", "--returnId", returnId, "--format", "json"], {
    allowFailure: true,
  });
  records.push(listRecord, getRecord, validateRecord);
  return {
    label,
    returnId,
    scheduleCExpenseTotal: scheduleCExpenseTotal(scheduleC),
    records,
    formList: parseJson(listRecord),
    returnGet: parseJson(getRecord),
    validation: validateRecord.exitCode === 0 ? parseJson(validateRecord) : {
      exitCode: validateRecord.exitCode,
      stdout: validateRecord.stdout,
      stderr: validateRecord.stderr,
    },
  };
}

function runFailureTests() {
  const tests = [];

  function capture(name, fn) {
    try {
      tests.push({ name, ...fn() });
    } catch (error) {
      tests.push({ name, accepted: false, unexpectedHarnessError: String(error?.message || error) });
    }
  }

  capture("invalid_filing_status_case", () => {
    const { returnId } = createReturn();
    const record = run([
      "form",
      "add",
      "--returnId",
      returnId,
      "--node_type",
      "general",
      payloadArg({ filing_status: "Single" }),
    ], { allowFailure: true });
    return { accepted: record.exitCode === 0, record };
  });

  capture("malformed_date_string", () => {
    const { returnId } = createReturn();
    const addRecord = addForm(returnId, "general", {
      filing_status: "single",
      taxpayer_dob: "13-40-2025",
    });
    const getRecord = run(["return", "get", "--returnId", returnId]);
    return { accepted: addRecord.exitCode === 0, record: addRecord, returnGet: parseJson(getRecord) };
  });

  capture("invalid_amount_type", () => {
    const { returnId } = createReturn();
    const payload = { ...scheduleCPayload(), line_1_gross_receipts: "not-a-number" };
    const record = run([
      "form",
      "add",
      "--returnId",
      returnId,
      "--node_type",
      "schedule_c",
      payloadArg(payload),
    ], { allowFailure: true });
    return { accepted: record.exitCode === 0, record };
  });

  capture("negative_gross_receipts", () => {
    const { returnId } = createReturn();
    const payload = { ...scheduleCPayload(), line_1_gross_receipts: -100 };
    const record = run([
      "form",
      "add",
      "--returnId",
      returnId,
      "--node_type",
      "schedule_c",
      payloadArg(payload),
    ], { allowFailure: true });
    return { accepted: record.exitCode === 0, record };
  });

  capture("unknown_node_type", () => {
    const { returnId } = createReturn();
    const record = run([
      "form",
      "add",
      "--returnId",
      returnId,
      "--node_type",
      "imaginary_node",
      payloadArg({ value: 1 }),
    ], { allowFailure: true });
    return { accepted: record.exitCode === 0, record };
  });

  capture("unsupported_year_get", () => {
    const createRecord = run(["return", "create", "--year", "2024"]);
    const returnId = parseJson(createRecord).returnId;
    const getRecord = run(["return", "get", "--returnId", returnId], { allowFailure: true });
    return {
      accepted: getRecord.exitCode === 0,
      createRecord,
      record: getRecord,
    };
  });

  capture("duplicate_interest_entry", () => {
    const { returnId } = createReturn();
    addForm(returnId, "general", baseGeneral());
    addForm(returnId, "f1099int", { payer_name: "Synthetic Bank", box1: 77.75 });
    const duplicateRecord = addForm(returnId, "f1099int", { payer_name: "Synthetic Bank", box1: 77.75 });
    const getRecord = run(["return", "get", "--returnId", returnId]);
    return {
      accepted: duplicateRecord.exitCode === 0,
      record: duplicateRecord,
      returnGet: parseJson(getRecord),
    };
  });

  capture("missing_return_id", () => {
    const record = run(["return", "get", "--returnId", "missing-return-id"], { allowFailure: true });
    return { accepted: record.exitCode === 0, record };
  });

  capture("invalid_json_argument", () => {
    const { returnId } = createReturn();
    const record = run([
      "form",
      "add",
      "--returnId",
      returnId,
      "--node_type",
      "general",
      "{not-json}",
    ], { allowFailure: true });
    return { accepted: record.exitCode === 0, record };
  });

  return tests;
}

const releaseMetadata = {
  source: "https://github.com/filedcom/opentax/releases/tag/v2.0.2",
  asset: "opentax-windows-x64.exe",
  expectedSha256: "14eba305f5429c1b40643f38044ccdf004e8dd93c51fcb5241f8aeefff931e65",
  actualSha256: sha256(opentaxBin),
  binaryPath: opentaxBin,
};

const helpRecord = run(["--help"]);
const versionRecord = run(["version"]);
const nodeListRecord = run(["node", "list"]);
const inspectGeneralRecord = run(["node", "inspect", "--node_type", "general", "--json"]);
const inspectScheduleCRecord = run(["node", "inspect", "--node_type", "schedule_c", "--json"]);
const inspectF1099IntRecord = run(["node", "inspect", "--node_type", "f1099int", "--json"]);
const inspectF1040EsRecord = run(["node", "inspect", "--node_type", "f1040es", "--json"]);
const graphRecord = run(["node", "graph", "--node_type", "schedule_c", "--depth", "2", "--json"]);

const baseline = buildScenario("baseline_standard_deduction", {});
const afterAdd = buildScenario("after_tadd_standard_deduction", { extraSoftwareExpense: 24.99 });
const itemizedProbe = buildScenario("charity_forced_itemized_probe", {
  scheduleA: {
    force_itemized: true,
    line_11_cash_contributions: 370,
  },
});

const exportNoForceRecord = run([
  "return",
  "export",
  "--returnId",
  baseline.returnId,
  "--type",
  "mef",
], { allowFailure: true });
const exportForceRecord = run([
  "return",
  "export",
  "--returnId",
  baseline.returnId,
  "--type",
  "mef",
  "--force",
], { allowFailure: true });

const mefPath = path.join(fixturesDir, "filed_opentax_day13_baseline_mef.xml");
if (exportForceRecord.exitCode === 0 && exportForceRecord.stdout) {
  writeFileSync(mefPath, exportForceRecord.stdout + "\n");
}

const failureTests = runFailureTests();

const baselineLines = baseline.returnGet.lines;
const afterAddLines = afterAdd.returnGet.lines;
const summary = {
  evaluatedAt: new Date().toISOString(),
  package: {
    name: "Filed Open Tax Engine",
    version: versionRecord.stdout.trim(),
    release: "v2.0.2",
    releasePublishedAt: "2026-05-11T14:52:21Z",
    registeredNodeCountFromCli: 186,
  },
  environment: {
    node: process.version,
    platform: process.platform,
    arch: process.arch,
    runDir,
  },
  releaseMetadata: {
    ...releaseMetadata,
    hashMatches: releaseMetadata.actualSha256 === releaseMetadata.expectedSha256,
  },
  dataset: {
    dataset_id: "synthetic-freelancer-2025-v1",
    tax_year: 2025,
    privacy: "synthetic-no-pii-no-real-account-data",
    input_profile: "evidence/fixtures/synthetic_freelancer_tax_profile.json",
  },
  mappingAssumptions: {
    filingStatus: "Mapped profile filing_status=single to OpenTax general.filing_status=single.",
    interest: "Mapped synthetic interest income to one f1099int entry with box1=77.75.",
    scheduleC: "Mapped gross receipts and categorized expenses to one schedule_c entry. Software, bank fees, and professional education were retained as Part V other expenses.",
    addTransaction: "Modeled TADD by adding a Part V Schedule C expense of 24.99 in a second return; OpenTax has form entries, not a bookkeeping transaction ledger.",
    estimatedPayments: "Mapped total federal estimated payments of 1050.00 into four equal f1040es quarterly payments.",
    charity: "Cash charitable contributions were tested separately with schedule_a.force_itemized=true because the baseline standard deduction is larger than the contribution amount.",
    mileage: "Business miles were not converted to a deduction because the shared profile leaves mileage_rate_usd and mileage_deduction_usd null.",
  },
  baseline: {
    label: baseline.label,
    returnId: baseline.returnId,
    scheduleCExpenseTotal: baseline.scheduleCExpenseTotal,
    summary: baseline.returnGet.summary,
    keyLines: {
      line2b_taxableInterest: baselineLines.line2b_taxable_interest,
      line8_additionalIncome: baselineLines.line8_additional_income,
      line10_adjustments: baselineLines.line10_adjustments,
      line11_agi: baselineLines.line11_agi,
      line12a_standardDeduction: baselineLines.line12a_standard_deduction,
      line15_taxableIncome: baselineLines.line15_taxable_income,
      line17_additionalTaxes: baselineLines.line17_additional_taxes,
      line24_totalTax: baselineLines.line24_total_tax,
      line26_estimatedTax: baselineLines.line26_estimated_tax,
      line27_eitc: baselineLines.line27_eitc,
      line33_totalPayments: baselineLines.line33_total_payments,
      line35a_refund: baselineLines.line35a_refund,
      line37_amountOwed: baselineLines.line37_amount_owed,
    },
    forms: baseline.returnGet.forms,
    warnings: baseline.returnGet.warnings,
    validation: baseline.validation,
  },
  afterAdd: {
    label: afterAdd.label,
    returnId: afterAdd.returnId,
    scheduleCExpenseTotal: afterAdd.scheduleCExpenseTotal,
    summary: afterAdd.returnGet.summary,
    keyLines: {
      line2b_taxableInterest: afterAddLines.line2b_taxable_interest,
      line8_additionalIncome: afterAddLines.line8_additional_income,
      line10_adjustments: afterAddLines.line10_adjustments,
      line11_agi: afterAddLines.line11_agi,
      line15_taxableIncome: afterAddLines.line15_taxable_income,
      line17_additionalTaxes: afterAddLines.line17_additional_taxes,
      line24_totalTax: afterAddLines.line24_total_tax,
      line26_estimatedTax: afterAddLines.line26_estimated_tax,
      line27_eitc: afterAddLines.line27_eitc,
      line33_totalPayments: afterAddLines.line33_total_payments,
      line35a_refund: afterAddLines.line35a_refund,
      line37_amountOwed: afterAddLines.line37_amount_owed,
    },
    forms: afterAdd.returnGet.forms,
    warnings: afterAdd.returnGet.warnings,
    validation: afterAdd.validation,
  },
  itemizedProbe: {
    label: itemizedProbe.label,
    returnId: itemizedProbe.returnId,
    summary: itemizedProbe.returnGet.summary,
    keyLines: {
      line11_agi: itemizedProbe.returnGet.lines.line11_agi,
      line12e_itemizedDeductions: itemizedProbe.returnGet.lines.line12e_itemized_deductions,
      line15_taxableIncome: itemizedProbe.returnGet.lines.line15_taxable_income,
      line16_incomeTax: itemizedProbe.returnGet.lines.line16_income_tax,
      line24_totalTax: itemizedProbe.returnGet.lines.line24_total_tax,
      line35a_refund: itemizedProbe.returnGet.lines.line35a_refund,
      line37_amountOwed: itemizedProbe.returnGet.lines.line37_amount_owed,
    },
    warnings: itemizedProbe.returnGet.warnings,
  },
  comparison: {
    baselineFederalTotalTax: baseline.returnGet.summary.line24_total_tax,
    afterAddFederalTotalTax: afterAdd.returnGet.summary.line24_total_tax,
    federalTotalTaxDeltaAfterTadd: Number((afterAdd.returnGet.summary.line24_total_tax - baseline.returnGet.summary.line24_total_tax).toFixed(6)),
    baselineRefund: baseline.returnGet.summary.line35a_refund ?? 0,
    afterAddRefund: afterAdd.returnGet.summary.line35a_refund ?? 0,
    refundDeltaAfterTadd: Number(((afterAdd.returnGet.summary.line35a_refund ?? 0) - (baseline.returnGet.summary.line35a_refund ?? 0)).toFixed(6)),
  },
  exportTests: {
    mefNoForce: {
      exitCode: exportNoForceRecord.exitCode,
      stdout: exportNoForceRecord.stdout,
      stderr: exportNoForceRecord.stderr,
    },
    mefForce: {
      exitCode: exportForceRecord.exitCode,
      stdoutBytes: Buffer.byteLength(exportForceRecord.stdout || "", "utf8"),
      stderr: exportForceRecord.stderr,
      evidenceFile: exportForceRecord.exitCode === 0 && exportForceRecord.stdout ? "evidence/fixtures/filed_opentax_day13_baseline_mef.xml" : null,
      preview: exportForceRecord.stdout.slice(0, 500),
    },
  },
  failureTests: failureTests.map((test) => {
    const slim = { ...test };
    if (slim.record?.stdout && slim.record.stdout.length > 4000) {
      slim.record = { ...slim.record, stdout: `${slim.record.stdout.slice(0, 4000)}\n...[truncated]` };
    }
    return slim;
  }),
};

writeFileSync(
  path.join(fixturesDir, "filed_opentax_day13_summary.json"),
  `${JSON.stringify(summary, null, 2)}\n`,
);

writeFileSync(
  path.join(fixturesDir, "filed_opentax_day13_failure_results.json"),
  `${JSON.stringify(summary.failureTests, null, 2)}\n`,
);

writeFileSync(
  path.join(commandsDir, `${localDate}_${slug}_setup.txt`),
  section("Filed OpenTax setup evidence", [
    {
      command: "download https://github.com/filedcom/opentax/releases/download/v2.0.2/opentax-windows-x64.exe",
      exitCode: releaseMetadata.actualSha256 === releaseMetadata.expectedSha256 ? 0 : 1,
      stdout: JSON.stringify(releaseMetadata, null, 2),
      stderr: "",
    },
  ]),
);

writeFileSync(
  path.join(commandsDir, `${localDate}_${slug}_version.txt`),
  section("Filed OpenTax version and schema evidence", [
    versionRecord,
    helpRecord,
    nodeListRecord,
    inspectGeneralRecord,
    inspectF1099IntRecord,
    inspectF1040EsRecord,
    inspectScheduleCRecord,
    graphRecord,
  ]),
);

writeFileSync(
  path.join(commandsDir, `${localDate}_${slug}_workflow.txt`),
  section("Filed OpenTax synthetic workflow evidence", [
    ...baseline.records,
    ...afterAdd.records,
    ...itemizedProbe.records,
    exportNoForceRecord,
    {
      ...exportForceRecord,
      stdout: exportForceRecord.stdout.length > 4000
        ? `${exportForceRecord.stdout.slice(0, 4000)}\n...[truncated; full XML in evidence/fixtures/filed_opentax_day13_baseline_mef.xml]`
        : exportForceRecord.stdout,
    },
  ]),
);

const failureRecords = [];
for (const test of failureTests) {
  if (test.createRecord) failureRecords.push(test.createRecord);
  if (test.record) failureRecords.push(test.record);
}
writeFileSync(
  path.join(commandsDir, `${localDate}_${slug}_failure-tests.txt`),
  section("Filed OpenTax failure-test evidence", failureRecords),
);

console.log(JSON.stringify({
  summaryFile: "evidence/fixtures/filed_opentax_day13_summary.json",
  failureFile: "evidence/fixtures/filed_opentax_day13_failure_results.json",
  setupEvidence: `evidence/commands/${localDate}_${slug}_setup.txt`,
  versionEvidence: `evidence/commands/${localDate}_${slug}_version.txt`,
  workflowEvidence: `evidence/commands/${localDate}_${slug}_workflow.txt`,
  failureEvidence: `evidence/commands/${localDate}_${slug}_failure-tests.txt`,
  baseline: summary.baseline.summary,
  afterAdd: summary.afterAdd.summary,
  comparison: summary.comparison,
}, null, 2));
