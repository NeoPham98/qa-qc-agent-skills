# Test Case Source Artifact

**Project**: BIDV Sample  
**Epic**: NMS SDK API sample  
**Export**: `../golden-outputs/testcase-legacy-19col.tsv`  
**Source**: `BIDV/NMS-Đặc tả API cho SDK-170326-075931.pdf` + SDK enrichment.

## POST /accounts/list

### TD_P1_001_TC_001
- **Derived from**: `TD_P1_001`
- **Scenario**: Header hợp lệ
- **Summary**: POST /accounts/list - kiểm tra header bắt buộc hợp lệ
- **Preconditions**: Env SIT; Endpoint /accounts/list; có AuthToken hợp lệ; source PDF page 6; SDK endpoints.py::accounts_list
- **Test Datas**: Headers: AuthToken, requestID, Accept-Language, X-App-Code, Content-Type; Body: `{ "requestCif": "123456789" }`
- **Test Steps**: Gửi POST /accounts/list với header/body hợp lệ và kiểm tra HTTP status/response envelope.
- **Expected Result**: HTTP Status 200; response có `code`, `message`, `success`, `data`; không phát sinh HTTP 500.

### TD_P2_001_TC_001
- **Derived from**: `TD_P2_001`
- **Scenario**: Thiếu required field `requestCif`
- **Summary**: POST /accounts/list - kiểm tra thiếu requestCif
- **Preconditions**: Env SIT; Endpoint /accounts/list; headers hợp lệ; source PDF page 6; SDK required field requestCif
- **Test Datas**: Body `{}`
- **Test Steps**: Gửi POST /accounts/list với body bỏ key `requestCif`.
- **Expected Result**: HTTP Status 400 hoặc validation status theo đặc tả; `success=false`; `code/message` mô tả thiếu `requestCif`.

### TD_P2_002_TC_001
- **Derived from**: `TD_P2_002`
- **Scenario**: Validate response account item schema
- **Summary**: POST /accounts/list - kiểm tra schema account item
- **Preconditions**: Env SIT; Endpoint /accounts/list; có CIF trả về danh sách tài khoản; `schemas.py::account_list_schema`
- **Test Datas**: Body `{ "requestCif": "123456789" }`
- **Test Steps**: Gửi POST /accounts/list và kiểm tra từng item trong `data`.
- **Expected Result**: HTTP Status 200; mỗi item có `accountNumber`, `currentBalance`, `currency`, `minBal`, `acctBranchcode` kiểu string.

## POST /v1/buy/order

### TD_P3_002_TC_001
- **Derived from**: `TD_P3_002`
- **Scenario**: Tài khoản nhận không thuộc CIF
- **Summary**: POST /v1/buy/order - kiểm tra business error ACC_DETAIL_INVALID_CIF
- **Preconditions**: Env SIT; Endpoint /v1/buy/order; headers hợp lệ; source PDF page 9; SDK business error `115=ACC_DETAIL_INVALID_CIF`
- **Test Datas**: Body `{ "requestId": "REQ-004", "requestCif": "123456789", "orderAmount": "1000000", "expectedSalesDate": "30/06/2026", "receivingAccount": "9999999999" }`
- **Test Steps**: Gửi POST /v1/buy/order với `receivingAccount` không thuộc `requestCif`.
- **Expected Result**: HTTP Status theo đặc tả; `success=false`; `code/message` tương ứng `115=ACC_DETAIL_INVALID_CIF`; không phát sinh HTTP 500.
