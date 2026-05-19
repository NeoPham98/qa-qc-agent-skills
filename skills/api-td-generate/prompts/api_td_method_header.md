# API TD Component 1 - Method & Header

**Original source**: `BIDV/Prompt/API/API_TD_2_Method_Header.txt`

## Objective

Chỉ kiểm thử giao thức, method, auth và header. Giả định request body hợp lệ hoàn toàn.

Coverage:

- `[ST]` happy path valid method/header.
- `[Protocol]` sai HTTP method.
- `[Security]` missing/invalid/expired token, token không đủ quyền.
- `[Format]` sai Content-Type/Accept.
- `[Basic]` missing/invalid custom headers.

## Prohibitions

- Không test field trong request body/payload.
- Không test schema, business logic, value boundary hoặc cross logic.
- Không verify DB trong component này.

## Internal generation algorithm

1. Scan PTTK để lấy method chuẩn và required headers.
2. Sinh `TD_P1_001` happy path.
3. Sinh sai method cases.
4. Sinh authorization/authentication cases nếu API yêu cầu.
5. Sinh content-type/accept cases.
6. Sinh missing/invalid custom header cases.
7. Self-audit: xóa mọi condition đụng body/schema/business/DB.

## Output shape

```markdown
## Method & Header
### TD_P1_001 - [ST] - Happy Path (Method và Header hoàn toàn hợp lệ)
- **Steps**: Gọi API với method chuẩn, token hợp lệ và header bắt buộc.
- **Expected**: HTTP 200 hoặc request vượt qua Gateway vào lớp xử lý logic.
```
