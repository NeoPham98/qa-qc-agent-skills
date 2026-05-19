# API Test Case Source

| Test Case ID | Function | Group Tests | Scenario Outline | Test Case Summary | Pre-conditions | Test Datas | Test Steps | Expected result |
|---|---|---|---|---|---|---|---|---|
| TD_P1_001_TC_001 | Domestic Payment API | Method/Header | Validate POST with JSON content type | Verify POST method and JSON content type are accepted | SIT endpoint and customer CCTG0001 are available | `{"customerId":"CCTG0001","amount":100000,"beneficiaryAccount":"970400000001"}` | Send POST /payments/domestic with Content-Type application/json | HTTP 200 and resultCode 00 |
| TD_P2_001_TC_001 | Domestic Payment API | Schema/Validation | Missing amount field | Verify missing amount is rejected | SIT endpoint and customer CCTG0001 are available | `{"customerId":"CCTG0001","beneficiaryAccount":"970400000001"}` | Send POST /payments/domestic without amount | HTTP 400 and errorCode AMOUNT_REQUIRED |
| TD_P3_001_TC_001 | Domestic Payment API | Logic/Business | Insufficient balance | Verify insufficient balance is rejected | Customer CCTG0002 has availableBalance 50000 | `{"customerId":"CCTG0002","amount":100000,"beneficiaryAccount":"970400000001"}` | Send POST /payments/domestic with amount above available balance | HTTP 422 and errorCode INSUFFICIENT_BALANCE |
