# API Operation Inventory

## POST /v1/customer/validate

- **Method**: POST
- **Endpoint**: /v1/customer/validate
- **Source**: NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.pdf
- **Required headers**: authToken, requestID, X-App-Code, Accept-language
- **Required body fields**: requestCif
- **Response schema**: code, message, errors, traceId, responseTime, success
- **Business errors**: 
  - 101=quốc tịch không hợp lệ
  - 102=tuổi không hợp lệ
  - 103=loại khách hàng không hợp lệ
  - 104=tình trạng cư trú không hợp lệ
  - 109=Hiện tại đã hết giờ giao dịch. Quý khách vui lòng thực hiện từ {0} đến {1} hàng ngày.
