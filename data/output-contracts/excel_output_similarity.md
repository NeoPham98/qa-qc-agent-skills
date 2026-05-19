# Excel Output Similarity Contract

This contract defines how generated outputs should be compared with baseline Excel outputs.

## Baseline files

| Baseline | Role |
|---|---|
| Legacy detailed testcase workbook | Detailed testcase workbook baseline |
| Paygates status workbook | Project/squad/sprint dashboard and status workbook baseline |

## Detailed testcase workbook similarity

Generated API/UI testcase outputs should match the `VA_19.004` workbook at the contract level.

### Required sheet-level behavior for Excel-style output

- Has testcase summary section when producing workbook-style output.
- Has detailed testcase table with legacy 19-column shape.
- Supports manual execution result fields for Round 1 and Round 2.
- Supports automation result, actual result, BugID and Notes.
- Legacy `.xlsx` exports may be generated from the validated Markdown/TSV contract without depending on the external VA workbook template.

### Required 19-column detail shape

| # | Column |
|---:|---|
| 1 | Test Case ID |
| 2 | Function |
| 3 | Group Tests |
| 4 | Scenario Outline |
| 5 | Test Case Summary |
| 6 | Pre-conditions |
| 7 | Test Data / Test Datas |
| 8 | Test Steps |
| 9 | Expected result |
| 10 | Environment |
| 11 | Priority |
| 12 | Regression |
| 13 | Automation |
| 14 | Manual Test Results Round 1 |
| 15 | Manual Test Results Round 2 |
| 16 | Automation Test Results |
| 17 | Actual result |
| 18 | BugID |
| 19 | Notes |

### Content similarity expectations

When source docs provide the details, testcase rows should include:

- business-readable function name,
- concrete role/persona,
- concrete preconditions,
- concrete test data,
- screen/navigation or API call evidence,
- expected response/status/message/field behavior,
- UI expected behavior when UI flow is involved,
- DB setup/verification when source docs provide DB details,
- execution result columns preserved for tester update,
- defect link/notes columns preserved,
- manual execution reader output preserves manual status, actual result, BugID and notes when importing from VA-style workbooks.

If source docs do not provide a detail, the output must show open questions or `[PENDING_DOC]`; it must not invent data just to look like the baseline.

## Paygates dashboard workbook similarity

Generated dashboard/status outputs should match the digitized Paygates contract in `paygates_dashboard_contract.md`. The historical Paygates workbook is an optional parity reference only; runtime generation must not depend on the external workbook existing.

### Required dashboard dimensions

- Project or product scope.
- Squad.
- Sprint.
- Epic/function.
- Testcase status counts.
- Automation status/estimate where source provides it.
- Link/path to testcase detail artifact.

### Required status metrics

- Passed.
- Failed.
- Untested.
- Accepted.
- N/A.
- Total Test cases.
- Current test status.
- Test case generate type when known.
- Automation test status when known.

### Similarity rules

- The generated dashboard does not need to reproduce Excel styling exactly.
- Markdown/TSV dashboard is acceptable as a normalized export layer.
- Totals must reconcile with testcase/execution artifacts when those artifacts are available.
- Missing squad/sprint/epic metadata must be explicit open questions.

## Review gate

Before handoff, the reviewer should answer:

| Check | Expected result |
|---|---|
| Testcase detail shape | Matches legacy 19-column contract |
| Testcase content depth | Uses concrete source data where available |
| Execution fields | Round/result/actual/BugID/notes fields preserved |
| Dashboard dimensions | Squad/sprint/epic/function/status dimensions represented when requested |
| Dashboard totals | Totals reconcile with testcase/execution source when available |
| Source fidelity | Missing values are open questions, not invented facts |
