# API TD Component 3 - Value, Business Logic, Cross Logic & Database

**Original source**: `BIDV/Prompt/API/API_TD_4_Value_Business_Cross_Logic.txt`

Runtime routes must use the workflow-pack prompt mirror and current source manifest, not the raw `BIDV/` path.

## Objective

Kiểm thử business rules sau khi request đã pass Method/Header và Schema Validation.

Coverage:

- `[ST]` happy path với data/state hợp lệ.
- `[BVA]` boundary cho number/date/amount: min-1, max+1, các biên có ý nghĩa.
- `[ECP]` invalid business partitions: âm, enum sai, format nghiệp vụ sai, ID không tồn tại.
- `[EG]` đúng 2 case cho text tự do: SQL/XSS injection trước, emoji/unicode sau.
- `[DT]` decision table cho rule phụ thuộc nhiều trường.
- `[ST]` state transition/precondition: account locked, pending exists, invalid lifecycle state.

## Prohibitions

- Không test header/auth/content-type.
- Không test lại schema: missing, empty, type, max length.
- Không verify DB cho lỗi nghiệp vụ HTTP 400/403/404.
- Không đưa HTTP 500 thành expected condition; HTTP 500 là defect.
- Happy path write API phải verify DB nếu tài liệu có DB/table/status.

## Decision table rule

Nếu có >=3 trường phụ thuộc:

1. Liệt kê N trường và trạng thái V/I.
2. Tạo lý thuyết 2^N combinations.
3. Loại combination không có nghĩa nghiệp vụ hoặc trùng coverage.
4. Chỉ giữ combination thực tế có expected result khác nhau.

## Matrix traceability

For every generated TD node, maintain a corresponding generation matrix row using `test_generation_matrix_contract.md`:

- `source_ref` must reference a source manifest id, normalized knowledge id, workflow-pack contract id, prompt contract id, or current run source section/page/sheet.
- Do not reference a raw `BIDV/` folder path in TD output, matrix output, rationale, or support artifacts.
- Map business/value/state rules to matrix rows with `Rule Type` values such as `business`, `cross_field`, `state`, `error`, `enum`, `min`, `max`, or `format`.
- Use `Technique` values that match the TD intent: `ECP`, `BVA`, `DT`, `ST`, or `EG`.
- For decision tables, keep only meaningful combinations with distinct expected results and record pruned combinations in matrix `Rationale` when relevant.
- Preserve the prompt rule that free-text EG produces exactly two cases when applicable.
- Mark missing or ambiguous business facts as `open_question` instead of inferring them.

## Internal generation algorithm

1. Sinh `TD_P3_001` happy path, Expected mô tả DB changes nếu có.
2. Duyệt từng payload field để sinh BVA/ECP/EG theo rule.
3. Scan global logic/state để sinh ST/DT.
4. Self-audit: không schema/header, EG đúng 2 case, DT đã lọc combination dư thừa.

## Output shape

```markdown
## Value, Business Logic, Cross Logic
### TD_P3_001 - [ST] - Happy Path (Dữ liệu và Trạng thái hợp lệ)
- **Steps**: Request body hợp lệ và precondition đúng.
- **Expected**: HTTP 200, Code 'SUCCESS'; DB thay đổi theo tài liệu.
```
