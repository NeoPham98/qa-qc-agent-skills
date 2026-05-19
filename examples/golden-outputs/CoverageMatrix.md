# Coverage Matrix Example

This example shows the expected density for testcase-generation routes. Real runs should expand source rules into concrete technique/value-class rows before testcase export.

| Matrix Row ID | Source Ref | Source Kind | Business Variant | Flow Or Screen | API Endpoint | Field Or Rule | Rule Type | Technique | Value Class | TD ID | Test Case ID | Coverage Status | Rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MTRX-API-001 | sample-api-spec#amount | runtime_input | Standard payment | API-only transfer | POST /payments | amount is required | required | ECP | valid_present | TD_P2_001 | TD_P2_001_TC_001 | covered | Happy path proves required amount accepted. |
| MTRX-API-002 | sample-api-spec#amount | runtime_input | Standard payment | API-only transfer | POST /payments | amount is required | required | ECP | missing | TD_P2_001 | TD_P2_001_TC_002 | covered | Mandatory negative case must verify exact error code/message. |
| MTRX-API-003 | sample-api-spec#amount | runtime_input | Standard payment | API-only transfer | POST /payments | amount min 10,000 | min | BVA | min-1 | TD_P2_002 | TD_P2_002_TC_001 | covered | Boundary below minimum should be rejected. |
| MTRX-API-004 | sample-api-spec#amount | runtime_input | Standard payment | API-only transfer | POST /payments | amount min 10,000 | min | BVA | min | TD_P2_002 | TD_P2_002_TC_002 | covered | Boundary at minimum should be accepted. |
| MTRX-API-005 | sample-api-spec#approval | runtime_input | Standard payment | Approval flow | POST /payments/{id}/approve | maker cannot approve own transaction | business | DT | maker_equals_checker | TD_P3_001 | TD_P3_001_TC_001 | covered | Decision-table row has distinct permission/business outcome. |
| MTRX-API-006 | sample-api-spec#status | runtime_input | Standard payment | Approval flow | POST /payments/{id}/approve | only Pending can be approved | state | ST | already_approved | TD_P3_002 | TD_P3_002_TC_001 | covered | Forbidden state transition should be rejected. |
| MTRX-API-007 | sample-api-spec#idempotency | runtime_input | Standard payment | API-only transfer | POST /payments | duplicate request id | business | EG | duplicate_request | TD_P3_003 | TD_P3_003_TC_001 | covered | Senior-QC error guessing for duplicate submission. |
| MTRX-API-008 | sample-api-spec#timeout | runtime_input | Standard payment | API-only transfer | POST /payments | upstream timeout behavior | error | EG | upstream_timeout | TD_P3_004 |  | open_question | Source does not define expected timeout status/message. |
