# Manual Execution Reader Contract

This contract defines deterministic import of manual execution results from legacy testcase workbooks or equivalent TSV/CSV tables.

## Supported source fields

| Source column | Purpose |
|---|---|
| Test Case ID | Required testcase identifier |
| Environment | Execution environment when present |
| Manual Test Results Round 1 | Manual round 1 status source |
| Manual Test Results Round 2 | Manual round 2 status source |
| Automation Test Results | Automation result status source |
| Actual result / Actual Result | Actual execution result detail |
| BugID | Defect identifier/link |
| Notes | Tester notes |
| Requirement ID | Optional traceability |
| Test Condition ID | Optional traceability |

## Output

The reader outputs a Test Execution TSV matching `test_status_excel_columns.md`.

## Status normalization

| Source value | Output Status |
|---|---|
| pass, passed, đạt | Pass |
| fail, failed, không đạt | Fail |
| empty, pending, not run, untested | Not Run |
| blocked | Blocked |
| retest | Retest |
| accepted | Accepted |
| unknown values | Not Run with an explicit open question in Notes |

## Fidelity rules

- Do not invent tester, build, test execution, test set, requirement, or test condition metadata.
- Missing metadata must be supplied by CLI or emitted as `[PENDING_DOC:<field>]`.
- Preserve Actual result, BugID, and Notes from the source table.
- The reader is contract/tool-driven and has `Source Prompt = N/A`, `Runtime Verbatim Prompt = N/A`.
