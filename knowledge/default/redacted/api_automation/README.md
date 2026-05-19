---
source_path: api_automation/README.md
source_role: automation_scaffold
canonical_status: reference
redaction_status: redacted
---
# NMS SDK API automation scaffold

Scaffold này được tạo từ đặc tả nguồn đã redacted.

## Phạm vi hiện có

- Common header builder: `AuthToken`, `requestID`, `Accept-Language`, `X-App-Code`, `Content-Type`
- RequestID UUID generator
- Common response envelope assertions
- Endpoint catalog cho 15 API trong PDF
- Schema validators mềm cho một số response quan trọng
- Smoke scenario skeleton cho các endpoint ít side effect
- API client foundation chỉ build request, chưa tự gửi network call

## Chạy test

Từ workspace root:

```bash
PYTHONPATH="E:[REDACTED_SECRET]" python -m unittest discover -s "E:[REDACTED_SECRET]"
```

## Bước tiếp theo

1. Bổ sung HTTP transport thực tế nếu đã có base URL/token test.
2. Thêm request payload factories theo dữ liệu SIT/UAT.
3. Mở rộng schema validators khi có response thật.
4. Tách pack smoke/regression/negative theo endpoint catalog.
