# Test Execution Status Column Contract

Các cột bắt buộc cho execution/status export:

| Column | Required | Purpose |
|---|---:|---|
| Test Execution ID | Yes | ID lần chạy |
| Test Set ID | Yes | Test set được chạy |
| Test Case ID | Yes | Testcase được execute |
| Environment | Yes | SIT/UAT/Regression env |
| Build / Version | Yes | Build/version chạy test |
| Tester | Yes | Nhân sự execute |
| Planned Run Date | No | Ngày dự kiến |
| Status | Yes | Not Run/Pass/Fail/Blocked/Retest |
| Actual Result | No | Kết quả thực tế |
| Evidence | No | Link/path evidence |
| Defect Link | No | Jira/defect link |
| Requirement ID | Yes | Trace requirement |
| Test Condition ID | Yes | Trace test condition |
| Notes | No | Ghi chú |
