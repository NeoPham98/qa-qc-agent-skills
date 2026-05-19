# BIDV Paygates Dashboard Sync Runner Example

Generate a dashboard TSV, validate it, and write a safe synced XLSX output:

```bash
python sdk/paygates_dashboard_runner.py \
  --testcase examples/full-xray-chain/Legacy19TestCase.md \
  --execution examples/full-xray-chain/TestExecution.from-manual.tsv \
  --output-dir examples/full-xray-chain \
  --project "BIDV Paygates" \
  --squad "Squad A" \
  --sprint "Sprint 1" \
  --epic "Paygates Regression" \
  --detail-link "examples/full-xray-chain/Legacy19TestCase.generated.xlsx" \
  --include-xlsx \
  --sync-output examples/full-xray-chain/PaygatesDashboard.synced.xlsx
```

When a historical workbook is supplied for reference, preserve it and write to a different output path:

```bash
python sdk/paygates_dashboard_runner.py \
  --testcase examples/full-xray-chain/Legacy19TestCase.md \
  --execution examples/full-xray-chain/TestExecution.from-manual.tsv \
  --output-dir examples/full-xray-chain \
  --project "BIDV Paygates" \
  --squad "Squad A" \
  --sprint "Sprint 1" \
  --epic "Paygates Regression" \
  --sync-workbook "BIDV/Tổng hợp Trạng Thái Test Case Paygates (1).xlsx" \
  --sync-output examples/full-xray-chain/PaygatesDashboard.synced.xlsx
```
