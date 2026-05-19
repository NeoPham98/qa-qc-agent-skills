# API Test Design / Test Conditions

**Project**: PAYGATES  
**Epic**: CCTG  
**Source**: BIDV API sample evidence  

## Control parameter coverage

METHOD_CHECK, CONTENT_TYPE_CHECK, MANDATORY_CHECK, TYPE_CHECK, LENGTH_CHECK, SCOPE_FIELDS, EG_CHECK

## Coverage Obligations

- METHOD: Source-derived - `POST /accounts/list` and `POST /v1/buy/order` are documented; unsupported method is tester-standard gateway/API behavior.
- CONTENT_TYPE: Source-derived - request body is JSON and `Content-Type=application/json` is documented.
- AUTH: Source-derived - `AuthToken` header is documented.
- MANDATORY_HEADERS: Source-derived - `requestID`, `Accept-Language`, `X-App-Code`, and `Content-Type` are documented.
- LANGUAGE: Source-derived - `Accept-Language` header is documented.
- BODY_SCHEMA: Source-derived - required request fields are documented.
- BOUNDARY: Assumption-derived tester-standard - requestCif length/format boundary uses `<REQUEST_CIF_OVER_MAX_LENGTH>` because exact max is not in sample evidence.
- BUSINESS_ERROR: Source-derived - business errors `115=ACC_DETAIL_INVALID_CIF`, `117=IMPLICT_BALANCE` are documented.
- RESPONSE_SCHEMA: Source-derived - response envelope and account item fields are documented.
- ERROR_PRIORITY: Assumption-derived tester-standard - multiple validation errors verify deterministic priority without inventing error code.


### Operation Card - POST /accounts/list

- **Source reference**: API spec page 6
- **Method/Endpoint**: `POST /accounts/list`
- **Headers**: `AuthToken`, `requestID`, `Accept-Language`, `X-App-Code`, `Content-Type=application/json`
- **Required request fields**: `requestCif`
- **Response schema assertions**: `accountNumber`, `currentBalance`, `currency`, `minBal`, `acctBranchcode` are string-like fields in each account item

### Operation Card - POST /v1/buy/order

- **Source reference**: API spec page 9
- **Method/Endpoint**: `POST /v1/buy/order`
- **Required request fields**: `requestId`, `requestCif`, `orderAmount`, `expectedSalesDate`, `receivingAccount`
- **Known business errors**: `115=ACC_DETAIL_INVALID_CIF`, `117=IMPLICT_BALANCE`

## Method & Header

### TD_P1_001 - [ST] - POST /accounts/list với header bắt buộc hợp lệ
- **Steps**: Gửi `POST /accounts/list` với `AuthToken`, `requestID`, `Accept-Language`, `X-App-Code`, `Content-Type=application/json` và body có `requestCif` hợp lệ.
- **Expected**: HTTP Status `200`; response trả envelope có `code`, `message`, `success`, `data`; không phát sinh HTTP 500.
- **Source**: API spec page 6.

## Schema Validation

### TD_P2_001 - [ST] - POST /accounts/list thiếu field requestCif
- **Steps**: Gửi `POST /accounts/list` với body `{}` và header hợp lệ để kiểm tra missing required field `requestCif`.
- **Expected**: HTTP Status `400` hoặc validation status theo đặc tả; response có `success=false`, `code/message` mô tả thiếu `requestCif`.
- **Source**: API spec page 6 required field `requestCif`.

### TD_P2_002 - [ST] - POST /accounts/list kiểm tra response account item schema
- **Steps**: Gửi `POST /accounts/list` với `requestCif` hợp lệ và kiểm tra từng account item trong `data`.
- **Expected**: HTTP Status `200`; mỗi item có `accountNumber`, `currentBalance`, `currency`, `minBal`, `acctBranchcode` và các field này là string-like.
- **Source**: API response schema.

## Value, Business Logic, Cross Logic

### TD_P3_001 - [ST] - POST /v1/buy/order tài khoản nhận không thuộc CIF
- **Steps**: Gửi `POST /v1/buy/order` với `receivingAccount` không thuộc `requestCif` để kiểm tra business rule.
- **Expected**: HTTP Status theo đặc tả; response trả business error `115=ACC_DETAIL_INVALID_CIF`, `success=false`; không phát sinh HTTP 500.
- **Source**: API spec page 9 business error matrix.
