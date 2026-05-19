---
source_path: Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.xlsx
source_role: xlsx_testcase
canonical_status: schema_evidence
redaction_status: unredacted
---
# Workbook profile: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.xlsx

## Sheet: Trang tính1

- Row count: 9
- Column count: 49
- Headers: Test Case ID, Function, Group Tests, Scenario Outline, Test Case
Summary, Pre-conditions, Test Data, Test Steps, Expected
result, Environment, Priority, Regression, Automation, Manual Test Results
Round 1, Manual Test Results Round 2, Automation Test Results, Actual
result, BugID, Notes , Method & Header, Method &
Header, Happy Path (Method và Header hoàn toàn hợp lệ), Kiểm tra gọi API thành
công khi truyền đầy đủ Method POST và các Header bắt buộc hợp lệ, 1. Env:
SIT              2. DB: [PENDING_DOC]              3. URL:
http://sit-deposit.apps.uat2ttptnhs.ldapudtest.com/cctg-online-api              4. Endpoint:
/v1/customer/validate              5. Header: Content-Type=application/json,
authToken=valid_token, requestID=REQ001, X-App-Code=WEB, Accept-language=vi              6.
Pre-Data: Dữ liệu khách hàng tồn tại trong hệ thống, 1. File:
customer_validate.json              2. Body: {"requestCif": "6856078"}, 1. Thiết lập
URL: http://sit-deposit.apps.uat2ttptnhs.ldapudtest.com/cctg-online-api,
Endpoint: /v1/customer/validate.              2. Thiết lập Header:
Content-Type=application/json, authToken=valid_token, requestID=REQ001,
X-App-Code=WEB, Accept-language=vi.              3. Thiết lập dữ liệu Request Body từ file
customer_validate.json.              4. Gọi API customer_validate với Method POST (Giữ
nguyên data).              5. Kiểm tra giá trị trả về của các trường trong Response
Body:              - HTTP Status: 200              - Response Body:              - $.code = "0"              - $.message =
"SUCCESS"              - $.success = true, 5.              HTTP Status: 200              Response Body:              {              
"code": "0",               "message": "SUCCESS",               "errors": null,               "traceId":
"1735790943042-159b47e0-1aad-470b-b37f-945ec384c2a4",               "responseTime":
"2025-01-02T11:09:03.109+07:00",               "success":
true              }, SIT, High, Yes, Yes, , , , , ,  "TD_P1_002_TC_002", Method &
Header, Method & Header, Gọi API với sai HTTP Method (GET), Kiểm tra hệ thống
từ chối request khi sử dụng sai Method GET thay vì POST, 1. Env: SIT              2. DB:
[PENDING_DOC]              3. URL:
http://sit-deposit.apps.uat2ttptnhs.ldapudtest.com/cctg-online-api              4. Endpoint:
/v1/customer/validate              5. Header: Content-Type=application/json,
authToken=valid_token, 1. File: customer_validate.json              2. Body:
{"requestCif": "6856078"}, 1. Thiết lập URL:
http://sit-deposit.apps.uat2ttptnhs.ldapudtest.com/cctg-online-api, Endpoint:
/v1/customer/validate.              2. Thiết lập Header: Content-Type=application/json,
authToken=valid_token.              3. Thiết lập dữ liệu Request Body từ file
customer_validate.json.              4. Gọi API customer_validate với Method GET.              5. Kiểm
tra giá trị trả về:              - HTTP Status: 405 (Method Not Allowed) hoặc 404, 5.              HTTP
Status: 405              Response Body:              {               "timestamp":
"2025-01-02T11:09:03.109+07:00",               "status": 405,               "error": "Method Not
Allowed",               "path":
"/v1/customer/validate"              }, SIT, Medium, No, Yes
- Status values: [none detected]
- Formulas:
  - [none detected]

## Sheet: Trang tính2

- Row count: 24
- Column count: 67
- Headers: Test Case ID, Function, Group Tests, Scenario Outline, Test Case
Summary, Pre-conditions, Test Data, Test Steps, Expected
result, Environment, Priority, Regression, Automation, Manual Test Results
Round 1, Manual Test Results Round 2, Automation Test Results, Actual
result, BugID, Notes , , , , , , , , , , , , , , , , , ,  "TD_P1_002_TC_002", Method &
Header, Method & Header, Gọi API với sai HTTP Method (GET), Kiểm tra hệ thống
từ chối request khi sử dụng sai Method GET thay vì POST, 1. Env: SIT              2. DB:
[PENDING_DOC]              3. URL:
http://sit-deposit.apps.uat2ttptnhs.ldapudtest.com/cctg-online-api              4. Endpoint:
/v1/customer/validate              5. Header: Content-Type=application/json,
authToken=valid_token, 1. File: customer_validate.json              2. Body:
{"requestCif": "6856078"}, 1. Thiết lập URL:
http://sit-deposit.apps.uat2ttptnhs.ldapudtest.com/cctg-online-api, Endpoint:
/v1/customer/validate.              2. Thiết lập Header: Content-Type=application/json,
authToken=valid_token.              3. Thiết lập dữ liệu Request Body từ file
customer_validate.json.              4. Gọi API customer_validate với Method GET.              5. Kiểm
tra giá trị trả về:              - HTTP Status: 405 (Method Not Allowed) hoặc 404, 5.              HTTP
Status: 405              Response Body:              {               "timestamp":
"2025-01-02T11:09:03.109+07:00",               "status": 405,               "error": "Method Not
Allowed",               "path":
"/v1/customer/validate"              }, SIT, Medium, No, Yes
- Status values: [none detected]
- Formulas:
  - [none detected]

## Sheet: Trang tính3

- Row count: 1
- Column count: 19
- Headers: Test Case ID, Function, Group Tests, Scenario Outline, Test Case
Summary, Pre-conditions, Test Data, Test Steps, Expected
result, Environment, Priority, Regression, Automation, Manual Test Results
Round 1, Manual Test Results Round 2, Automation Test Results, Actual
result, BugID, Notes
- Status values: [none detected]
- Formulas:
  - [none detected]
