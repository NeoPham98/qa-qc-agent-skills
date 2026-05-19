# API Test Design / Test Conditions

**Project**: BIDV Sample  
**Epic**: NMS SDK API sample  
**Source**: `normalized-knowledge:nms-sdk-api-spec`  
**Enrichment**: `normalized-knowledge:nms-sdk-api-automation/endpoints`, `normalized-knowledge:nms-sdk-api-automation/schemas`

## API Requirement Inventory / Operation Cards

### Operation Card - POST /accounts/list

- **Source reference**: PDF page 6; `endpoints.py::accounts_list`; `schemas.py::account_list_schema`
- **Method/Endpoint**: `POST /accounts/list`
- **Headers**: `AuthToken`, `requestID`, `Accept-Language`, `X-App-Code`, `Content-Type=application/json`
- **Required request fields**: `requestCif`
- **Response schema assertions**: `accountNumber`, `currentBalance`, `currency`, `minBal`, `acctBranchcode` are string-like fields in each account item
- **Known business errors**: `402=TKTT_NOT_FOUND`
- **Open questions**: exact validation error code for missing `requestCif`

### Operation Card - POST /v1/buy/order

- **Source reference**: PDF page 9; `endpoints.py::buy_order`
- **Method/Endpoint**: `POST /v1/buy/order`
- **Headers**: `AuthToken`, `requestID`, `Accept-Language`, `X-App-Code`, `Content-Type=application/json`
- **Required request fields**: `requestId`, `requestCif`, `orderAmount`, `expectedSalesDate`, `receivingAccount`
- **Known business errors**: `115=ACC_DETAIL_INVALID_CIF`, `117=IMPLICT_BALANCE`, `118=ACCOUNT_TYPE_INVALID`, `119=ACCOUNT_IS_JION_ACC`, `120=TRANSACTION_BUY_FAIL`, `240=IN_COT_TIME`
- **Open questions**: exact min/max amount and date boundary values from final API owner

# POST /accounts/list - Danh sách tài khoản nhận gốc/lãi

## Method & Header

### TD_P1_001 - [ST] - POST /accounts/list với header bắt buộc hợp lệ
- **Steps**: Gửi `POST /accounts/list` với `AuthToken`, `requestID`, `Accept-Language`, `X-App-Code`, `Content-Type=application/json` và body có `requestCif` hợp lệ.
- **Expected**: HTTP Status `200`; response trả envelope có `code`, `message`, `success`, `data`; không phát sinh HTTP 500.
- **Source**: PDF page 6; `endpoints.py::accounts_list`.

## Schema Validation

### TD_P2_001 - [ST] - POST /accounts/list thiếu field requestCif
- **Steps**: Gửi `POST /accounts/list` với body `{}` và header hợp lệ để kiểm tra missing required field `requestCif`.
- **Expected**: HTTP Status `400` hoặc validation status theo đặc tả; response có `success=false`, `code/message` mô tả thiếu `requestCif`.
- **Source**: PDF page 6; `endpoints.py` required field `requestCif`.

### TD_P2_002 - [ST] - POST /accounts/list kiểm tra response account item schema
- **Steps**: Gửi `POST /accounts/list` với `requestCif` hợp lệ và kiểm tra từng account item trong `data`.
- **Expected**: HTTP Status `200`; mỗi item có `accountNumber`, `currentBalance`, `currency`, `minBal`, `acctBranchcode` và các field này là string-like.
- **Source**: `schemas.py::account_list_schema`.

## Value, Business Logic, Cross Logic

### TD_P3_001 - [ST] - POST /accounts/list không tìm thấy tài khoản TKTT
- **Steps**: Gửi `POST /accounts/list` với `requestCif` hợp lệ nhưng không có TKTT đủ điều kiện nhận gốc/lãi.
- **Expected**: HTTP Status theo đặc tả; response trả business error `402=TKTT_NOT_FOUND`, `success=false`, không phát sinh HTTP 500.
- **Source**: PDF page 6; `endpoints.py` business error `402=TKTT_NOT_FOUND`.

# POST /v1/buy/order - Lập lệnh mua CDFlex

## Method & Header

### TD_P1_002 - [ST] - POST /v1/buy/order thiếu AuthToken
- **Steps**: Gửi `POST /v1/buy/order` với body hợp lệ nhưng bỏ header `AuthToken`.
- **Expected**: HTTP Status `401` hoặc auth status theo đặc tả; response có `success=false`, `code/message` thể hiện lỗi xác thực; không verify DB.
- **Source**: PDF page 9; common header contract.

## Schema Validation

### TD_P2_003 - [ST] - POST /v1/buy/order thiếu orderAmount
- **Steps**: Gửi `POST /v1/buy/order` với body có `requestId`, `requestCif`, `expectedSalesDate`, `receivingAccount` nhưng bỏ `orderAmount`.
- **Expected**: HTTP Status `400` hoặc validation status theo đặc tả; response có `success=false`, `code/message` mô tả thiếu `orderAmount`.
- **Source**: PDF page 9; `endpoints.py::buy_order` required field `orderAmount`.

## Value, Business Logic, Cross Logic

### TD_P3_002 - [ST] - POST /v1/buy/order tài khoản nhận không thuộc CIF
- **Steps**: Gửi `POST /v1/buy/order` với `receivingAccount` không thuộc `requestCif`.
- **Expected**: HTTP Status theo đặc tả; response trả business error `115=ACC_DETAIL_INVALID_CIF`, `success=false`; không phát sinh HTTP 500.
- **Source**: PDF page 9; `endpoints.py` business error `115=ACC_DETAIL_INVALID_CIF`.

### TD_P3_003 - [ST] - POST /v1/buy/order số dư khả dụng không đủ
- **Steps**: Gửi `POST /v1/buy/order` với `orderAmount` lớn hơn số dư khả dụng của `receivingAccount`.
- **Expected**: HTTP Status theo đặc tả; response trả business error `117=IMPLICT_BALANCE`, `success=false`; không phát sinh HTTP 500.
- **Source**: PDF page 9; `endpoints.py` business error `117=IMPLICT_BALANCE`.
