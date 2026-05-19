# API TD Component 2 - Schema Validation

**Original source**: `BIDV/Prompt/API/API_TD_3_Schema_Validation.txt`

Runtime routes must use the workflow-pack prompt mirror and current source manifest, not the raw `BIDV/` path.

## Objective

Chỉ kiểm thử cấu trúc dữ liệu request body/params dựa trên PTTK.

Coverage:

- `[ST]` valid schema happy path.
- `[Missing]` required field missing key.
- `[Empty]` required field empty value.
- `[Type]` invalid data type.
- `[Max Length]` length N+1 khi PTTK có số cụ thể.
- Min length nếu PTTK có số cụ thể.

## Prohibitions

- Không test header/auth/token/content-type.
- Không tạo null case cho mandatory check; chỉ Missing và Empty.
- Không tự bịa max length/min length nếu tài liệu không ghi.
- Không test business value, negative amount, enum nghiệp vụ, cross logic.
- Không verify DB cho validation lỗi; chỉ happy path nếu phù hợp.

## Matrix traceability

For every generated TD node, maintain a corresponding generation matrix row using `test_generation_matrix_contract.md`:

- `source_ref` must reference a source manifest id, normalized knowledge id, workflow-pack contract id, prompt contract id, or current run source section/page/sheet.
- Do not reference a raw `BIDV/` folder path in TD output, matrix output, rationale, or support artifacts.
- Map schema rules to matrix rows with `Rule Type` values such as `required`, `type`, `length`, or `format` and `Technique` = `schema`.
- Preserve the prompt rule that mandatory checks create Missing and Empty cases only; do not add null mandatory matrix rows.
- Mark missing or ambiguous source facts as `open_question` instead of inferring them.

## Internal generation algorithm

1. Sinh `TD_P2_001` valid schema happy path.
2. Duyệt từng field trong request payload, bỏ qua header.
3. Với từng field, theo đúng thứ tự: Required Missing/Empty, Type, Max Length, Min Length.
4. Xong field hiện tại mới chuyển field tiếp theo.
5. Self-audit: không header, không null, không bịa length, không business rule.

## Output shape

```markdown
## Schema Validation
### TD_P2_001 - [ST] - Happy Path Full Flow (Valid Schema)
- **Steps**: Request body với đầy đủ thông tin hợp lệ.
- **Expected**: HTTP 200, Code 'SUCCESS'.
```
