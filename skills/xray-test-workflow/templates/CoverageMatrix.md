# Coverage Matrix / Test Generation Matrix

This matrix traces runtime source rules to Test Design nodes, testcase rows, execution, and gaps. Do not reference a raw `BIDV/` folder path here; use source manifest ids, normalized knowledge ids, workflow pack contract ids, or current run source sections/pages/sheets.

## Generation Matrix

| Matrix Row ID | Source Ref | Source Kind | Business Variant | Flow Or Screen | API Endpoint | Field Or Rule | Rule Type | Technique | Value Class | TD ID | Test Case ID | Coverage Status | Rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MTRX-API-001 | source-1#section-3.1 | runtime_input |  | API-only | POST /accounts/list | requestCif required | required | schema | missing | TD_P2_001 | TD_P2_001_TC_001 | covered | Required field missing coverage from runtime API spec. |

## Execution Trace

| Requirement ID | Test Condition ID | Test Case ID | Test Set ID | Test Execution ID | Execution Status | Defect Link | Gap |
|---|---|---|---|---|---|---|---|
| REQ-API-001 | TD_P2_001 | TD_P2_001_TC_001 | TS-SIT-001 | TE-SIT-B001-001 | Not Run |  |  |

## Gap Summary

| Gap ID | Severity | Matrix Row ID | Description | Fix Needed |
|---|---|---|---|---|
| GAP-001 | Low |  |  |  |
