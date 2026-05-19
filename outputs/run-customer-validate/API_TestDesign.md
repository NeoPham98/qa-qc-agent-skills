# API Test Design / Test Conditions

**Project**: CCTG Online  
**Epic**: Customer Validate  
**Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf  

## Control parameter coverage

METHOD_CHECK, CONTENT_TYPE_CHECK, MANDATORY_CHECK, TYPE_CHECK, LENGTH_CHECK, SCOPE_FIELDS, EG_CHECK

## Coverage Obligations

- METHOD: Source-derived - `POST /v1/customer/validate` is documented. Other HTTP methods are rejected.
- CONTENT_TYPE: Source-derived - request/response body is JSON with `Content-Type=application/json`.
- AUTH: Source-derived - `authToken` header is required for authorization.
- MANDATORY_HEADERS: Source-derived - `requestID`, `X-App-Code`, `Accept-language` headers are required.
- LANGUAGE: Source-derived - `Accept-language` supports `vi` and `en`.
- BODY_SCHEMA: Source-derived - request body requires `requestCif` field.
- BOUNDARY: Source-derived - `requestCif` length must be exactly 12 characters.
- BUSINESS_ERROR: Source-derived - errors 101, 102, 103, 104, 109 are mapped.
- RESPONSE_SCHEMA: Source-derived - response envelope includes code, message, success, errors, traceId, responseTime.
- ERROR_PRIORITY: Source-derived - validations are prioritized.

### Operation Card - POST /v1/customer/validate

- **Source reference**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1
- **Method/Endpoint**: `POST /v1/customer/validate`
- **Headers**: `authToken`, `requestID`, `X-App-Code`, `Accept-language`
- **Required request fields**: `requestCif`
- **Response schema assertions**: `code`, `message`, `errors`, `traceId`, `responseTime`, `success`
- **Known business errors**: `101=quốc tịch không hợp lệ`, `102=tuổi không hợp lệ`, `103=loại khách hàng không hợp lệ`, `104=tình trạng cư trú không hợp lệ`, `109=Hiện tại đã hết giờ giao dịch`

## POST /v1/customer/validate - API check điều kiện KH

## Method & Header

### TD_P1_001 - [ST] - POST /v1/customer/validate với header bắt buộc hợp lệ và method POST
- **Steps**: Gửi request `POST /v1/customer/validate` với headers `authToken`, `requestID`, `X-App-Code`, `Accept-language=vi` và request body `{ "requestCif": "123456789012" }`.
- **Expected**: HTTP Status `200`; response body trả về `success=true`, `code="0"`, `message="SUCCESS"`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1, 2.

### TD_P1_002 - [ST] - GET /v1/customer/validate với method không được hỗ trợ
- **Steps**: Gửi request `GET /v1/customer/validate` thay vì POST, sử dụng headers `authToken`, `requestID`, `X-App-Code`, `Accept-language=vi` và body rỗng.
- **Expected**: HTTP Status `405` Method Not Allowed hoặc HTTP 400 Bad Request; response body trả về `success=false`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P1_003 - [ST] - POST /v1/customer/validate thiếu header authToken
- **Steps**: Gửi request `POST /v1/customer/validate` không kèm theo header `authToken`, các headers khác hợp lệ và body có `requestCif` gồm 12 chữ số.
- **Expected**: HTTP Status `401` Unauthorized hoặc HTTP 400 Bad Request; response body trả về `success=false`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P1_004 - [ST] - POST /v1/customer/validate thiếu header requestID
- **Steps**: Gửi request `POST /v1/customer/validate` không kèm theo header `requestID`, các headers khác hợp lệ và body có `requestCif` gồm 12 chữ số.
- **Expected**: HTTP Status `400` Bad Request; response body trả về `success=false`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P1_005 - [ST] - POST /v1/customer/validate thiếu header X-App-Code
- **Steps**: Gửi request `POST /v1/customer/validate` không kèm theo header `X-App-Code`, các headers khác hợp lệ và body có `requestCif` gồm 12 chữ số.
- **Expected**: HTTP Status `400` Bad Request; response body trả về `success=false`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P1_006 - [ST] - POST /v1/customer/validate với Accept-language là vi
- **Steps**: Gửi request `POST /v1/customer/validate` với header `Accept-language=vi`, các headers khác hợp lệ và body có `requestCif` gồm 12 chữ số.
- **Expected**: HTTP Status `200` OK; response body trả về `success=true`, `code="0"`, `message="SUCCESS"` hiển thị bằng tiếng Việt.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P1_007 - [ST] - POST /v1/customer/validate với Accept-language là en
- **Steps**: Gửi request `POST /v1/customer/validate` với header `Accept-language=en`, các headers khác hợp lệ và body có `requestCif` gồm 12 chữ số.
- **Expected**: HTTP Status `200` OK; response body trả về `success=true`, `code="0"`, `message="SUCCESS"` hiển thị bằng tiếng Anh.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

## Schema Validation

### TD_P2_001 - [ST] - POST /v1/customer/validate thiếu trường requestCif trong request body
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ, request body rỗng `{}` hoặc thiếu trường bắt buộc (mandatory required field) `requestCif`.
- **Expected**: HTTP Status `400` Bad Request; response body trả về `success=false` kèm chi tiết lỗi thiếu trường bắt buộc (required/mandatory parameter requestCif).
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P2_002 - [BVA] - POST /v1/customer/validate với trường requestCif có độ dài nhỏ hơn 12 ký tự
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ, request body chứa trường `requestCif` có độ dài 11 ký tự (length 11, ví dụ: "12345678901").
- **Expected**: HTTP Status `400` Bad Request; response body trả về `success=false` kèm chi tiết lỗi độ dài (invalid length/format validation for param requestCif).
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P2_003 - [BVA] - POST /v1/customer/validate với trường requestCif có độ dài lớn hơn 12 ký tự
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ, request body chứa trường `requestCif` có độ dài 13 ký tự (length 13, ví dụ: "1234567890123").
- **Expected**: HTTP Status `400` Bad Request; response body trả về `success=false` kèm chi tiết lỗi độ dài (invalid length/format validation for param requestCif).
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P2_004 - [Type] - POST /v1/customer/validate với trường requestCif không phải kiểu string
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ, request body chứa trường `requestCif` không đúng kiểu dữ liệu string (invalid type/schema, ví dụ: kiểu số `123456789012` không để trong dấu ngoặc kép).
- **Expected**: HTTP Status `400` Bad Request; response body trả về `success=false` mô tả lỗi kiểu dữ liệu hoặc cấu trúc request không hợp lệ.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1.

### TD_P2_005 - [ST] - POST /v1/customer/validate kiểm tra cấu trúc (schema) response thành công
- **Steps**: Gửi request `POST /v1/customer/validate` với body có `requestCif` hợp lệ dài 12 ký tự, kiểm tra cấu trúc (response body schema) trả về.
- **Expected**: HTTP Status `200` OK; response body trả về đầy đủ các trường: `code` (string), `message` (string), `errors` (null), `traceId` (string), `responseTime` (datetime), `success` (boolean=true).
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 1, 2.

### TD_P2_006 - [ST] - POST /v1/customer/validate kiểm tra cấu trúc (schema) response thất bại
- **Steps**: Gửi request `POST /v1/customer/validate` gây ra lỗi nghiệp vụ (ví dụ: `requestCif` không thỏa mãn điều kiện mua), kiểm tra cấu trúc (response body schema) trả về.
- **Expected**: HTTP Status `400` Bad Request; response body trả về đầy đủ các trường: `code` (string), `message` (string), `errors` (array of string hoặc null), `traceId` (string), `responseTime` (datetime), `success` (boolean=false).
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 2.

## Value, Business Logic, Cross Logic

### TD_P3_001 - [ST] - POST /v1/customer/validate lỗi 101 quốc tịch không hợp lệ
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ và request body chứa `requestCif` của khách hàng có quốc tịch không phải Việt Nam (hoặc quốc tịch không thuộc danh sách cho phép của nghiệp vụ CCTG).
- **Expected**: HTTP Status `400`; response body trả về trạng thái thất bại với `success=false`, `code="101"`, `message="quốc tịch không hợp lệ"`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 2 business rules.

### TD_P3_002 - [ST] - POST /v1/customer/validate lỗi 102 tuổi không hợp lệ
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ và request body chứa `requestCif` của khách hàng chưa đủ tuổi (ví dụ dưới 18 tuổi hoặc không thỏa mãn quy định tuổi mua CCTG).
- **Expected**: HTTP Status `400`; response body trả về trạng thái thất bại với `success=false`, `code="102"`, `message="tuổi không hợp lệ"`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 2 business rules.

### TD_P3_003 - [ST] - POST /v1/customer/validate lỗi 103 loại khách hàng không hợp lệ
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ và request body chứa `requestCif` của khách hàng có loại khách hàng (customer type) không được phép giao dịch CCTG Online (ví dụ: Khách hàng định chế tài chính, Tổ chức...).
- **Expected**: HTTP Status `400`; response body trả về trạng thái thất bại với `success=false`, `code="103"`, `message="loại khách hàng không hợp lệ"`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 2 business rules.

### TD_P3_004 - [ST] - POST /v1/customer/validate lỗi 104 tình trạng cư trú không hợp lệ
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ và request body chứa `requestCif` của khách hàng có tình trạng cư trú (residency status) không hợp lệ (ví dụ: Không cư trú).
- **Expected**: HTTP Status `400`; response body trả về trạng thái thất bại với `success=false`, `code="104"`, `message="tình trạng cư trú không hợp lệ"`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 3 business rules.

### TD_P3_005 - [ST] - POST /v1/customer/validate lỗi 109 giao dịch ngoài giờ COT (hệ thống đã hết giờ giao dịch)
- **Steps**: Gửi request `POST /v1/customer/validate` với headers hợp lệ và request body chứa `requestCif` hợp lệ tại thời điểm hệ thống nằm ngoài khung giờ giao dịch cho phép (giờ Cut-Off Time).
- **Expected**: HTTP Status `400`; response body trả về trạng thái thất bại với `success=false`, `code="109"`, `message="Hiện tại đã hết giờ giao dịch. Quý khách vui lòng thực hiện từ {0} đến {1} hàng ngày."`.
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf page 3 business rules.
