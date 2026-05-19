# BIDV API Delivery Runner Example

## Plan-only smoke

```bash
python sdk/api_delivery_runner.py \
  --source "Data/NMS-Đặc tả API cho SDK-170326-075931.pdf" \
  --output-dir "outputs/nms-sdk-api-qc" \
  --scope "full API TD, testcase, automation support, output review" \
  --plan-only \
  --max-turns 6
```

## Full run with deterministic MCP helpers

```bash
python sdk/api_delivery_runner.py \
  --source "Data/NMS-Đặc tả API cho SDK-170326-075931.pdf" \
  --output-dir "outputs/nms-sdk-api-qc-regenerated" \
  --scope "full API delivery with legacy TSV validation" \
  --include-mcp \
  --max-turns 16
```

## Expected safeguards

- The runner instructs Claude to use Prompt-Compatible Orchestration Mode only.
- Runtime team configs are not written into the repository.
- API spec-driven routes must produce or consume an API Requirement Inventory / Operation Cards artifact before TD generation.
- Generated TD/TC artifacts must include concrete method, endpoint, field/header/rule target, test data, expected HTTP status, and response/error assertions when source facts exist.
- Generated outputs must include OutputReview before handoff.
- Legacy TSV and testcase TSV should be validated with existing scripts or MCP helpers.
- API specificity validators should run in addition to legacy 19-column structural validation.
- API TD-derived testcase IDs must follow `TD_Px_NNN_TC_NNN`.
- Formatted XLSX exports should render escaped TSV newlines as real Excel line breaks.
