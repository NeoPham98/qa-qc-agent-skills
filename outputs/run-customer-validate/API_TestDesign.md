# API Test Design / Điều kiện kiểm thử chi tiết

**Dự án**: CCTG Online  
**Epic**: Customer Validate  
**Tài liệu căn cứ**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf  

## Danh mục chỉ số bao phủ điều kiện (Control Parameters)

METHOD_CHECK, CONTENT_TYPE_CHECK, MANDATORY_CHECK, TYPE_CHECK, LENGTH_CHECK, SCOPE_FIELDS, EG_CHECK

---

## 1. Giao thức, Phương thức & Tiêu đề (Protocol, Method & Headers)

### POST /v1/customer/validate

### TD_P1_001 - [ST] - POST /v1/customer/validate với thông tin hợp lệ
- **Steps**: 
  1. Sử dụng phương thức `POST` gửi tới endpoint `/v1/customer/validate`.
  2. Đính kèm đầy đủ các header bắt buộc hợp lệ:
     - `authToken`: "ValidToken_QA_2026"
     - `requestID`: "REQ-20260520-001"
     - `X-App-Code`: "CCTG_ONLINE_PORTAL"
     - `Accept-language`: "vi"
     - `Content-Type`: "application/json"
  3. Gửi request body hợp lệ: `{ "requestCif": "685607800001" }` (Khách hàng thỏa mãn tất cả các điều kiện nghiệp vụ).
- **Expected**: 
  - HTTP Status: `200` OK.
  - Cấu trúc response body dạng JSON khớp đặc tả, có success = true, code = "0", message = "SUCCESS", errors = null, traceId dạng UUID, responseTime dạng ISO-8601.
- **Source**: Trang 1, 2 của tài liệu đặc tả.

### TD_P1_002 - [ECP] - Gọi API bằng các phương thức HTTP không được hỗ trợ (GET/PUT/DELETE/PATCH)
- **Steps**: 
  1. Sử dụng phương thức `GET` (hoặc `PUT`/`DELETE`/`PATCH`) gửi tới endpoint `/v1/customer/validate`.
  2. Đính kèm đầy đủ headers và body hợp lệ như TD_P1_001.
- **Expected**: 
  - HTTP Status: `405` Method Not Allowed (hoặc `400` Bad Request tùy cấu hình API Gateway).
  - Trả về mã lỗi mô tả phương thức không hợp lệ, success = false.
- **Source**: Giả định tiêu chuẩn an toàn API Gateway.

### TD_P1_003 - [ECP] - Header Content-Type không hợp lệ (không phải application/json)
- **Steps**: 
  1. Gửi request `POST /v1/customer/validate`.
  2. Thiết lập header `Content-Type`: "text/plain" hoặc "application/xml".
  3. Gửi request body hợp lệ dạng chuỗi thô hoặc XML.
- **Expected**: 
  - HTTP Status: `415` Unsupported Media Type hoặc `400` Bad Request.
  - Hệ thống báo lỗi kiểu dữ liệu không được hỗ trợ, success = false.
- **Source**: Giả định tiêu chuẩn an toàn API Gateway.

### TD_P1_004 - [ST] - Thiếu hoặc rỗng header authToken
- **Steps**: 
  1. Gửi request `POST /v1/customer/validate` nhưng loại bỏ header `authToken` (hoặc truyền giá trị rỗng `authToken` = "").
  2. Các tham số khác hợp lệ.
- **Expected**: 
  - HTTP Status: `401` Unauthorized (hoặc `400` Bad Request).
  - Response trả về success = false, thông tin chi tiết lỗi xác thực.
- **Source**: Trang 1 của đặc tả.

### TD_P1_005 - [ST] - Thiếu hoặc rỗng header requestID
- **Steps**: 
  1. Gửi request `POST /v1/customer/validate` nhưng loại bỏ header `requestID` (hoặc truyền giá trị rỗng `requestID` = "").
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response trả về success = false, mã lỗi và thông báo thiếu trường bắt buộc.
- **Source**: Trang 1 của đặc tả.

### TD_P1_006 - [ST] - Thiếu hoặc rỗng header X-App-Code
- **Steps**: 
  1. Gửi request `POST /v1/customer/validate` nhưng loại bỏ header `X-App-Code` (hoặc truyền giá trị rỗng `X-App-Code` = "").
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response trả về success = false, mã lỗi báo thiếu app code.
- **Source**: Trang 1 của đặc tả.

### TD_P1_007 - [ST] - Thiếu header Accept-language
- **Steps**: 
  1. Gửi request `POST /v1/customer/validate` nhưng loại bỏ header `Accept-language`.
- **Expected**: 
  - HTTP Status: `400` Bad Request (hoặc mặc định sử dụng "vi").
  - Response trả về success = false.
- **Source**: Trang 1 của đặc tả.

### TD_P1_008 - [ECP] - Header Accept-language là giá trị không được hỗ trợ (ví dụ: "fr")
- **Steps**: 
  1. Gửi request `POST /v1/customer/validate` với header `Accept-language`: "fr".
- **Expected**: 
  - HTTP Status: `400` Bad Request (hoặc tự động fallback về tiếng Anh/tiếng Việt).
  - Response trả về thông báo lỗi ngôn ngữ không hỗ trợ hoặc phản hồi lỗi bằng ngôn ngữ mặc định.
- **Source**: Trang 1 của đặc tả.

---

## 2. Ràng buộc cấu trúc Payload Request (Body Schema Validation)

### POST /v1/customer/validate

### TD_P2_001 - [ST] - Request body rỗng {} hoặc thiếu trường requestCif
- **Steps**: 
  1. Gửi request `POST /v1/customer/validate`.
  2. Gửi request body rỗng `{}` hoặc thiếu hoàn toàn key `requestCif`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response trả về success = false, thông báo lỗi trường `requestCif` là bắt buộc.
- **Source**: Trang 1 của đặc tả.

### TD_P2_002 - [ECP] - Trường requestCif truyền sai kiểu dữ liệu (Number/Boolean/Object/Array)
- **Steps**: 
  1. Gửi request body có `requestCif` là kiểu số: `{ "requestCif": 685607800001 }`.
  2. Gửi request body có `requestCif` là kiểu boolean: `{ "requestCif": true }`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response trả về success = false, thông báo lỗi sai định dạng dữ liệu (Invalid type).
- **Source**: Trang 1 của đặc tả.

### TD_P2_003 - [BVA] - Trường requestCif rỗng "" (độ dài 0)
- **Steps**: 
  1. Gửi request body: `{ "requestCif": "" }`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response trả về success = false, thông báo lỗi trường bắt buộc không được để trống.
- **Source**: Trang 1 của đặc tả.

### TD_P2_004 - [BVA] - Trường requestCif có độ dài nhỏ hơn 12 ký tự (Biên dưới - 11 ký tự)
- **Steps**: 
  1. Gửi request body với `requestCif` dài 11 ký tự: `{ "requestCif": "12345678901" }`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response trả về success = false, thông báo lỗi độ dài `requestCif` không hợp lệ (yêu cầu đúng 12 ký tự).
- **Source**: Trang 1 của đặc tả.

### TD_P2_005 - [BVA] - Trường requestCif có độ dài lớn hơn 12 ký tự (Biên trên - 13 ký tự)
- **Steps**: 
  1. Gửi request body với `requestCif` dài 13 ký tự: `{ "requestCif": "1234567890123" }`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response trả về success = false, thông báo lỗi độ dài `requestCif` không hợp lệ.
- **Source**: Trang 1 của đặc tả.

### TD_P2_006 - [ECP] - Trường requestCif chứa ký tự không hợp lệ (chữ cái, khoảng trắng hoặc ký tự đặc biệt)
- **Steps**: 
  1. Gửi request body chứa chữ cái: `{ "requestCif": "12345678901a" }`.
  2. Gửi request body chứa khoảng trắng: `{ "requestCif": "12345678901 " }`.
  3. Gửi request body chứa ký tự đặc biệt: `{ "requestCif": "12345678901#" }`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response trả về success = false, thông báo lỗi định dạng CIF không hợp lệ.
- **Source**: Trang 1 của đặc tả.

---

## 3. Quy tắc Nghiệp vụ Khách hàng (Customer Business Logic Validation)

### POST /v1/customer/validate

### TD_P3_001 - [ECP] - Kiểm tra điều kiện quốc tịch của khách hàng (Lỗi 101)
- **Steps**: 
  1. Chuẩn bị thông tin khách hàng có quốc tịch nước ngoài (ví dụ: Hoa Kỳ - US).
  2. Gửi request `POST /v1/customer/validate` với `requestCif` đại diện cho khách hàng này.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "101", message = "quốc tịch không hợp lệ".
- **Source**: Trang 2 của đặc tả.

### TD_P3_002 - [BVA] - Khách hàng chưa đủ 18 tuổi (Biên tuổi vi phạm - 17 tuổi)
- **Steps**: 
  1. Chuẩn bị khách hàng có ngày sinh tính đến thời điểm giao dịch hiện tại là tròn 17 tuổi.
  2. Gửi request `POST /v1/customer/validate` với `requestCif` đại diện cho khách hàng này.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "102", message = "tuổi không hợp lệ".
- **Source**: Trang 2 của đặc tả.

### TD_P3_003 - [BVA] - Khách hàng vừa tròn 18 tuổi (Biên tuổi hợp lệ)
- **Steps**: 
  1. Chuẩn bị khách hàng có ngày sinh tính đến thời điểm hiện tại tròn đúng 18 tuổi.
  2. Gửi request `POST /v1/customer/validate` với `requestCif` đại diện cho khách hàng này.
- **Expected**: 
  - HTTP Status: `200` OK.
  - Response: success = true, code = "0", message = "SUCCESS".
- **Source**: Trang 2 của đặc tả.

### TD_P3_004 - [ECP] - Loại khách hàng không hợp lệ (Lỗi 103)
- **Steps**: 
  1. Chuẩn bị khách hàng là Tổ chức/Doanh nghiệp (không phải cá nhân hợp lệ).
  2. Gửi request `POST /v1/customer/validate` với `requestCif` đại diện cho khách hàng này.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "103", message = "loại khách hàng không hợp lệ".
- **Source**: Trang 2 của đặc tả.

### TD_P3_005 - [ECP] - Tình trạng cư trú không hợp lệ (Lỗi 104)
- **Steps**: 
  1. Chuẩn bị khách hàng có tình trạng cư trú là "Không cư trú" (Non-resident).
  2. Gửi request `POST /v1/customer/validate` với `requestCif` đại diện cho khách hàng này.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "104", message = "tình trạng cư trú không hợp lệ".
- **Source**: Trang 3 của đặc tả.

### TD_P3_006 - [ST] - Thực hiện giao dịch ngoài giờ giao dịch cho phép - Giờ COT (Lỗi 109)
- **Steps**: 
  1. Giả lập hệ thống đang nằm ngoài giờ giao dịch cho phép (ví dụ: 23:00 hoặc 05:00 sáng).
  2. Gửi request `POST /v1/customer/validate` với `requestCif` hợp lệ.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "109", message = "Hiện tại đã hết giờ giao dịch. Quý khách vui lòng thực hiện từ {0} đến {1} hàng ngày." (với `{0}` và `{1}` được thay thế bằng giờ mở/đóng cửa thực tế).
- **Source**: Trang 3 của đặc tả.

### POST /v1/customer/validate

### TD_P3_007 - [BVA] - Biên giao dịch giờ COT: Giao dịch ngay trước giờ mở cửa (Ví dụ: 07:59)
- **Steps**: 
  1. Giả lập giờ giao dịch của hệ thống lúc 07:59 (COT cho phép từ 08:00 đến 17:00).
  2. Gửi request `POST /v1/customer/validate`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "109", thông báo hết giờ giao dịch.
- **Source**: Trang 3 của đặc tả.

### TD_P3_008 - [BVA] - Biên giao dịch giờ COT: Giao dịch đúng giờ mở cửa (Ví dụ: 08:00)
- **Steps**: 
  1. Giả lập giờ giao dịch của hệ thống lúc đúng 08:00.
  2. Gửi request `POST /v1/customer/validate`.
- **Expected**: 
  - HTTP Status: `200` OK.
  - Response: success = true, code = "0".
- **Source**: Trang 3 của đặc tả.

### TD_P3_009 - [BVA] - Biên giao dịch giờ COT: Giao dịch đúng giờ đóng cửa (Ví dụ: 17:00)
- **Steps**: 
  1. Giả lập giờ giao dịch của hệ thống lúc đúng 17:00.
  2. Gửi request `POST /v1/customer/validate`.
- **Expected**: 
  - HTTP Status: `200` OK.
  - Response: success = true, code = "0".
- **Source**: Trang 3 của đặc tả.

### TD_P3_010 - [BVA] - Biên giao dịch giờ COT: Giao dịch ngay sau giờ đóng cửa (Ví dụ: 17:01)
- **Steps**: 
  1. Giả lập giờ giao dịch của hệ thống lúc 17:01.
  2. Gửi request `POST /v1/customer/validate`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "109", thông báo hết giờ giao dịch.
- **Source**: Trang 3 của đặc tả.

### TD_P3_011 - [DT] - Độ ưu tiên kiểm tra lỗi: Khách hàng vừa sai Quốc tịch (101) vừa chưa đủ tuổi (102)
- **Steps**: 
  1. Chuẩn bị khách hàng có quốc tịch nước ngoài (vi phạm 101) VÀ đồng thời chỉ mới 16 tuổi (vi phạm 102).
  2. Gửi request `POST /v1/customer/validate` với `requestCif` đại diện cho khách hàng này.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "101", message = "quốc tịch không hợp lệ" (Lỗi 101 được ưu tiên kiểm tra và trả về trước).
- **Source**: Trang 2 của đặc tả (Quy tắc độ ưu tiên kiểm tra lỗi).

### TD_P3_012 - [DT] - Độ ưu tiên kiểm tra lỗi: Khách hàng vừa chưa đủ tuổi (102) vừa sai loại khách hàng (103)
- **Steps**: 
  1. Chuẩn bị khách hàng chưa đủ 18 tuổi (vi phạm 102) VÀ đồng thời là loại khách hàng doanh nghiệp (vi phạm 103).
  2. Gửi request `POST /v1/customer/validate`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "102", message = "tuổi không hợp lệ" (Lỗi 102 được trả về trước lỗi 103).
- **Source**: Trang 2 của đặc tả.

### TD_P3_013 - [DT] - Độ ưu tiên kiểm tra lỗi: Khách hàng vừa sai loại khách hàng (103) vừa sai tình trạng cư trú (104)
- **Steps**: 
  1. Chuẩn bị khách hàng là doanh nghiệp (vi phạm 103) VÀ đồng thời ở trạng thái Không cư trú (vi phạm 104).
  2. Gửi request `POST /v1/customer/validate`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "103", message = "loại khách hàng không hợp lệ" (Lỗi 103 trả về trước lỗi 104).
- **Source**: Trang 2, 3 của đặc tả.

### TD_P3_014 - [DT] - Độ ưu tiên kiểm tra lỗi: Khách hàng vừa sai tình trạng cư trú (104) vừa ngoài giờ COT (109)
- **Steps**: 
  1. Giả lập hệ thống ngoài giờ COT (vi phạm 109) VÀ gửi request cho khách hàng có tình trạng Không cư trú (vi phạm 104).
  2. Gửi request `POST /v1/customer/validate`.
- **Expected**: 
  - HTTP Status: `400` Bad Request.
  - Response: success = false, code = "104", message = "tình trạng cư trú không hợp lệ" (Lỗi 104 được ưu tiên trả về trước lỗi 109).
- **Source**: Trang 3 của đặc tả.
