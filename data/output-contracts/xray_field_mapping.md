# XRAY Field Mapping

| Markdown Artifact | XRAY/Jira Concept | Key Fields |
|---|---|---|
| Requirement Inventory | Requirement / Story | Requirement ID, summary, source, priority, risk |
| Test Plan | Test Plan | Test Plan ID, scope, environment, entry/exit criteria |
| Test Design / Test Condition | Coverage design layer | Test Condition ID, Requirement ID, coverage intent |
| Test Case | Xray Test | Test Case ID, steps, expected result, preconditions |
| Test Set | Xray Test Set | Test Set ID, included Test Case IDs, purpose |
| Test Execution | Xray Test Execution | Execution ID, Test Set ID, status, evidence, defect link |
| Coverage Matrix | Traceability / Coverage Report | Requirement -> Condition -> Test -> Execution -> Defect |

Không ghi trực tiếp Jira/Xray nếu chưa có phê duyệt riêng.
