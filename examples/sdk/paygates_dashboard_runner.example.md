# BIDV Paygates dashboard runner example

Generate a self-contained Paygates dashboard from internal testcase/execution artifacts:

```bash
python sdk/paygates_dashboard_runner.py \
  --testcase examples/full-xray-chain/TestCase.md \
  --execution examples/full-xray-chain/TestExecution.md \
  --output-dir examples/full-xray-chain \
  --project "BIDV Paygates" \
  --squad "Squad A" \
  --sprint "Sprint 1" \
  --epic "Paygates Regression" \
  --detail-link "examples/full-xray-chain/TestCase.md" \
  --include-xlsx
```

Outputs:

- `PaygatesDashboard.generated.tsv`
- `PaygatesDashboard.generated.xlsx`
