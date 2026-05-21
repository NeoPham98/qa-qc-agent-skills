# QA-QC Agent Skills Repository Report

## 1. Tổng quan nhanh

Repo `qa-qc-agent-skills/` là một package **Prompt-Compatible Orchestration Mode** cho QA/QC BIDV. Nó không hoạt động như một app web thông thường; thay vào đó nó dùng **orchestrator + workflow pack + skills + validators** để biến source tài liệu đầu vào thành các artifact QA/test có kiểm soát.

**Entrypoint chính**:
- `agents/delivery-orchestrator/AGENT.md`

**Runtime source of truth**:
- `workflow-packs/default/workflow.yml`
- `workflow-packs/default/`

**Luồng vận hành tổng thể**:

```text
User request / source docs
-> delivery orchestrator
-> route selection
-> prompt/skill execution
-> validator(s)
-> output review
-> supervisor approval
-> artifact publish
```

## 2. Danh sách hành động chính của hệ thống

Các “hành động” trong repo chủ yếu được định nghĩa trong `workflow-packs/default/workflow.yml` dưới dạng `routes` và `stages`.

### 2.1 Hành động nền tảng

| Hành động | Mục đích | Output chính |
|---|---|---|
| `source_inventory` | Lập inventory nguồn đầu vào | `source-manifest.yml` |
| `source_normalization` | Chuẩn hóa tài liệu nguồn sang dạng maintainable | `normalization-report.json` |
| `secret_redaction` | Redact secrets trước khi dùng runtime | `redaction-report.yml` |
| `knowledge_validation` | Kiểm tra knowledge runtime đã an toàn/chuẩn | `knowledge-validation-report.json` |

### 2.2 Hành động sinh tài liệu QA/Test

| Hành động | Mục đích | Output chính |
|---|---|---|
| `test_plan` | Sinh Test Plan | `TestPlan.md` |
| `api_operation_inventory` | Bóc tách inventory API/operation | `API_OperationInventory.md` |
| `api_td_setup_context` | Sinh phần context cho API Test Design | `API_TestDesign.md` |
| `api_td_method_header` | Sinh coverage method/header/auth | `API_TestDesign.md` |
| `api_td_schema_validation` | Sinh coverage schema/param/body | `API_TestDesign.md` |
| `api_td_business_logic` | Sinh coverage business/value/cross logic | `API_TestDesign.md` |
| `ui_td` | Sinh UI Test Design | `UI_TestDesign.md` |
| `test_generation_matrix` | Lập Coverage/Gap matrix | `CoverageMatrix.md`, `GapAnalysis.md` |
| `api_tc_from_td` | Sinh API testcase từ Test Design | `TestCaseSource.md`, `Legacy19TestCase.generated.*` |
| `ui_tc_from_td` | Sinh UI testcase từ Test Design | `TestCaseSource.md`, `Legacy19TestCase.generated.*` |
| `uat_tc` | Sinh UAT testcase | `UAT_TestCaseSource.md`, `UAT_TestCase.generated.tsv` |

### 2.3 Hành động export / automation / execution / dashboard

| Hành động | Mục đích | Output chính |
|---|---|---|
| `legacy_19col_export` | Export testcase sang BIDV legacy 19-column TSV/XLSX | `Legacy19TestCase.generated.tsv`, `Legacy19TestCase.generated.xlsx` |
| `uat_16col_export` | Export testcase UAT 16 cột | `UAT_TestCase.generated.tsv` |
| `api_testcase_analysis` | Phân tích testcase cho automation support | `API_TestCase_Analysis.md` |
| `api_method_header_feature` | Sinh Gherkin feature cho method/header | `api_method_header_validation.feature` |
| `api_schema_feature` | Sinh Gherkin feature cho validation/schema | `api_validation.feature` |
| `api_logic_business_feature` | Sinh Gherkin feature cho business logic | `api_logic_business.feature` |
| `manual_execution_reader` | Đọc kết quả execute manual từ workbook/TSV/CSV | `TestExecution.from-manual.tsv` |
| `paygates_dashboard` | Sinh dashboard Paygates | `PaygatesDashboard.generated.tsv`, `.xlsx` |
| `tracker_validation` | Validate tracker/dashboard | `TrackerValidation.json` |
| `coverage_audit` | Audit coverage và gap | `CoverageMatrix.md`, `GapAnalysis.md` |

### 2.4 Hành động gate / kiểm soát vòng đời

| Hành động | Mục đích | Output chính |
|---|---|---|
| `api_td_validation`, `ui_td_validation`, `api_tc_validation`, `uat_tc_validation` | Validate artifact theo contract | các file `.validation.json` hoặc TSV đã pass |
| `output_review` | Review output theo prompt fidelity, traceability, contract | `OutputReview.md` |
| `supervisor_approval` | Phê duyệt hoặc reject artifact | `SupervisorApproval.md` |
| `artifact_publish` | Publish artifact đã approved | `published-artifact-manifest.yml` |

---

## 3. Root level: từng folder/file và tác dụng

### 3.1 File gốc

| Path | Tác dụng |
|---|---|
| `README.md` | Tài liệu gốc giải thích operating mode duy nhất, entrypoint, output bắt buộc, standards, contracts, runner và scripts. Đây là file mô tả toàn repo quan trọng nhất. |
| `package.json` | Metadata npm tối thiểu của package; khai báo `cypress` là dev dependency. |
| `package-lock.json` | Lock dependency cho môi trường Node/Cypress. |
| `cypress.config.js` | Cấu hình Cypress; khởi tạo local mock HTTP server, đọc TSV đã generate và convert sang fixture JSON để chạy E2E demo. |
| `.gitignore` | Quy định file/folder không commit. |

### 3.2 Folder gốc

| Folder | Tác dụng |
|---|---|
| `.claude/` | Chứa template settings cho Claude Code hooks/permissions. |
| `.git/` | Metadata git repo, không phải runtime logic. |
| `agents/` | Định nghĩa các role agent điều phối/generate/review/validate/approve. |
| `artifacts/` | Chứa audit artifacts và draft runtime artifacts mẫu. |
| `cypress/` | Chứa test E2E Cypress và fixtures. |
| `data/` | Chứa output contracts và source inventory/routing reference. |
| `examples/` | Chứa ví dụ đầu ra chuẩn, chain end-to-end, SDK example. |
| `knowledge/` | Chứa standards và normalized knowledge/manifests. |
| `node_modules/` | Dependency cài đặt cục bộ, không phải logic nghiệp vụ. |
| `outputs/` | Chứa output của các run thực tế/mẫu. |
| `playbooks/` | Chứa recipe cho team orchestration. |
| `prompts-verbatim/` | Chứa bản mirror verbatim của runtime prompts BIDV. |
| `scripts/` | Chứa các script deterministic để export/validate/normalize/sync/publish. |
| `sdk/` | Chứa runner và core orchestration layer bằng Python. |
| `skills/` | Chứa các skill nghiệp vụ và prompt/template/reference con. |
| `tests/` | Chứa test cho contracts, validators, routes, E2E flow. |
| `workflow-packs/` | Chứa workflow pack runtime tự đủ. |

---

## 4. Folder `.claude/`

**Mục đích**: template cấu hình Claude Code cho permission và hook an toàn.

### File quan trọng
- `.claude/settings.example.json`: ví dụ cấu hình allow/deny tool và PostToolUse/Stop hooks; hiện hook gọi `python scripts/verify_prompt_mirrors.py` để đảm bảo prompt mirror đúng source.

**Hành động folder này hỗ trợ**:
- kiểm soát quyền chạy tool
- chặn lệnh destructive shell
- tự verify prompt mirror sau khi edit/write hoặc khi stop

---

## 5. Folder `agents/`

**Mục đích**: mô tả vai trò từng agent trong closed-loop delivery.

### 5.1 Agent lõi

| File | Vai trò / tác dụng |
|---|---|
| `agents/delivery-orchestrator/AGENT.md` | Agent trung tâm. Route request, enforce thứ tự gate, phân stage, chặn bypass validator/review/approval/publish. |
| `agents/knowledge-retriever/AGENT.md` | Lấy canonical redacted context cho route runtime, tránh lộ raw sensitive source. |
| `agents/api-test-design-agent/AGENT.md` | Sinh API Test Design theo pha P1/P2/P3 và bàn giao cho validator. |
| `agents/ui-test-design-agent/AGENT.md` | Sinh UI Test Design với canonical ID format. |
| `agents/testcase-generator/AGENT.md` | Sinh API/UI/UAT testcase đúng contract 19 cột hoặc 16 cột. |
| `agents/test-set-execution-manager/AGENT.md` | Build Test Set, import execution, status update và output execution artifacts. |
| `agents/output-reviewer/AGENT.md` | Review output về fidelity, traceability, lifecycle readiness. |
| `agents/contract-validator/AGENT.md` | Chạy deterministic validators cho Markdown/TSV/XLSX/profile/tracker/review lifecycle. |
| `agents/supervisor/AGENT.md` | Approve/reject artifact sau khi đã có validation + review evidence. |

### 5.2 Agent hỗ trợ chuyên biệt

| File | Tác dụng |
|---|---|
| `agents/automation-support-agent/AGENT.md` | Chạy prompt API automation support trên reviewed testcase source. |
| `agents/coverage-auditor/AGENT.md` | Audit traceability và coverage giữa requirement, design, testcase, execution, automation. |
| `agents/contract-validator/AGENT.md` | Validator role chuyên trách. |
| `agents/format-normalizer/AGENT.md` | Chuẩn hóa output sang Markdown source-of-truth và export-ready structures. |
| `agents/qa-reviewer/AGENT.md` | Peer QA review trước gate output-reviewer chính thức. |
| `agents/requirement-coverage-analyst/AGENT.md` | Trích requirement và audit requirement-to-execution coverage. |
| `agents/spec-ui-locator/AGENT.md` | Tìm reference API/DB/UI field/button/screen/design cho generation agent. |

### 5.3 File phụ trong `agents/delivery-orchestrator/`

| File | Tác dụng |
|---|---|
| `skills_manifest.yml` | Liệt kê skill mà orchestrator dùng: test-plan, test-design, testcase, dashboard, export, validator, automation support... |
| `tools_manifest.yml` | Mô tả nhóm tool được phép dùng: read-only, write outputs, forbidden actions nếu chưa approval. |
| `playbooks/full_chain_handoff.md` | Hướng dẫn handoff full chain. |
| `playbooks/prompt_compatible_orchestration.md` | Playbook điều phối theo Prompt-Compatible Orchestration Mode. |
| `playbooks/prompt_migration.md` | Tài liệu chuyển đổi prompt/mirror. |
| `playbooks/universal_file_prompt_workflow.md` | Luồng universal runner khi user ném file + prompt. |
| `playbooks/xray_delivery.md` | Playbook cho XRAY-style delivery. |
| `prompts/output_contract_review.md` | Prompt/phụ trợ cho review contract output. |
| `prompts/task_package_intake.md` | Prompt/phụ trợ cho intake task package. |

---

## 6. Folder `skills/`

**Mục đích**: mô tả từng capability nghiệp vụ độc lập mà orchestrator gọi tới.

### 6.1 Skill generate/chuyển đổi chính

| Skill | File chính | Tác dụng |
|---|---|---|
| `api-td-generate` | `skills/api-td-generate/SKILL.md` | Sinh API Test Design qua các prompt fragment API TD. |
| `ui-td-generate` | `skills/ui-td-generate/SKILL.md` | Sinh UI Test Design từ prompt verbatim UI. |
| `tc-generate-from-td` | `skills/tc-generate-from-td/SKILL.md` | Sinh testcase API/UI từ Test Design. |
| `uat-tc-generate` | `skills/uat-tc-generate/SKILL.md` | Sinh UAT testcase theo contract 16 cột. |
| `test-plan-generate` | `skills/test-plan-generate/SKILL.md` | Sinh Test Plan như một orchestration step. |
| `test-set-build` | `skills/test-set-build/SKILL.md` | Build Test Set artifact từ testcase đã review. |
| `test-execution-pack-generate` | `skills/test-execution-pack-generate/SKILL.md` | Sinh execution pack từ testcase/test set đã review. |
| `paygates-dashboard-generate` | `skills/paygates-dashboard-generate/SKILL.md` | Sinh dashboard trạng thái dạng Paygates. |
| `paygates-dashboard-sync` | `skills/paygates-dashboard-sync/SKILL.md` | Sync/export dashboard TSV sang XLSX an toàn. |
| `legacy-xlsx-exporter` | `skills/legacy-xlsx-exporter/SKILL.md` | Export testcase 19 cột sang XLSX mà không cần workbook template ngoài. |
| `manual-execution-reader` | `skills/manual-execution-reader/SKILL.md` | Đọc kết quả manual execution và emit `TestExecution TSV`. |
| `api-automation-support-generate` | `skills/api-automation-support-generate/SKILL.md` | Sinh analysis và Gherkin feature cho API automation support. |

### 6.2 Skill kiểm soát chất lượng / tiện ích

| Skill | File chính | Tác dụng |
|---|---|---|
| `coverage-audit` | `skills/coverage-audit/SKILL.md` | Audit coverage và traceability. |
| `output-verify` | `skills/output-verify/SKILL.md` | Review output theo prompt fidelity, source fidelity, contract. |
| `testcase-validator` | `skills/testcase-validator/SKILL.md` | Chạy deterministic validator cho testcase contracts. |
| `tracker-validator` | `skills/tracker-validator/SKILL.md` | Audit Paygates tracker workbook/status/formula. |
| `doc-normalizer` | `skills/doc-normalizer/SKILL.md` | Chuẩn hóa nguồn BIDV bootstrap sang Markdown/TSV profile. |
| `secret-redactor` | `skills/secret-redactor/SKILL.md` | Redact credentials/token/cookie/internal endpoint. |
| `xlsx-extractor` | `skills/xlsx-extractor/SKILL.md` | Trích profile workbook, headers, alias, statuses, formulas. |
| `supervisor-loop` | `skills/supervisor-loop/SKILL.md` | Điều phối lifecycle reviewed/approved/rejected/archived. |
| `xray-test-workflow` | `skills/xray-test-workflow/SKILL.md` | Định nghĩa luật Prompt-Compatible Orchestration, traceability và handoff gates. |

### 6.3 Prompt/template/reference con trong skills

| Path | Tác dụng |
|---|---|
| `skills/api-td-generate/prompts/*.md` | Prompt fragment cho các bước API TD: setup context, method/header, schema validation, business logic. |
| `skills/tc-generate-from-td/prompts/*.md` | Prompt sinh testcase API/UI từ Test Design. |
| `skills/uat-tc-generate/prompts/ui_gen_tc_for_uat.md` | Prompt sinh UAT testcase. |
| `skills/ui-td-generate/prompts/ui_gen_td.md` | Prompt sinh UI Test Design. |
| `skills/api-automation-support-generate/prompts/*.md` | Prompt sinh API testcase analysis và các `.feature` support file. |
| `skills/paygates-dashboard-generate/templates/PaygatesDashboard.md` | Template dashboard Markdown. |
| `skills/xray-test-workflow/templates/*.md` | Template cho CoverageMatrix, OutputReview, RequirementInventory, TestCase, TestDesign, TestExecution, TestPlan, TestSet. |
| `skills/xray-test-workflow/reference/*.md` | Quy ước ID, source priority, mapping artifact XRAY. |

---

## 7. Folder `workflow-packs/default/`

**Mục đích**: runtime bundle tự đủ, là nguồn truth chính khi chạy thực tế.

### File điều khiển chính

| File | Tác dụng |
|---|---|
| `workflow.yml` | File quan trọng nhất của runtime pack: định nghĩa route, stage, final output, validator mapping, gate order. |
| `workflow.json` | Bản JSON tương ứng để runner/tooling dễ dùng. |
| `validators.yml` / `validators.json` | Map artifact -> script validator -> stage. |
| `artifact-policy.yml` | Chính sách publish artifact. |
| `review-gates.yml` | Gate yêu cầu `OutputReview` và `SupervisorApproval`. |
| `status-enums.yml` | Chuẩn hóa enum/status cho execution/dashboard flow. |
| `classifiers.yml` / `classifiers.json` | Luật classifier/route inference. |
| `output_profiles.yml` / `output_profiles.json` | Profile output cho runtime. |
| `excel-contract.yml` | Contract liên quan output Excel. |
| `canonical-sources.yml` | Danh sách nguồn chuẩn/canonical cho pack. |
| `README.md` | Giải thích workflow pack này là self-contained runtime pack. |

### Folder con

| Folder | Tác dụng |
|---|---|
| `contracts/` | Contract runtime đóng gói sẵn để validate output. |
| `prompts/API/`, `prompts/UI/` | Prompt verbatim dùng khi runtime generate API/UI TD/TC/UAT/automation support. |
| `examples/` | Golden example output để đối chiếu/parity. |

### Contracts trong workflow pack

Các file trong `workflow-packs/default/contracts/` là bản runtime của contract:
- `api_automation_analysis_contract.md`
- `api_automation_feature_contract.md`
- `excel_output_similarity.md`
- `legacy_19_column_testcase_contract.md`
- `manual_execution_reader_contract.md`
- `markdown_normalization_rules.md`
- `paygates_dashboard_contract.md`
- `test_generation_matrix_contract.md`
- `test_plan_contract.md`
- `test_status_excel_columns.md`
- `testcase_excel_columns.md`
- `uat_16_column_testcase_contract.md`
- `xray_field_mapping.md`

**Hành động folder này hỗ trợ**:
- chọn route theo intent/input
- map stage sang prompt/tool/validator
- định nghĩa output cuối và gate publish
- cung cấp prompt/contract/example phục vụ runtime

---

## 8. Folder `prompts-verbatim/`

**Mục đích**: mirror prompt BIDV gốc theo dạng verbatim để bảo toàn hành vi prompt.

### File chính

#### API
- `prompts-verbatim/API/API_TD_1_Setup_Context.txt`
- `prompts-verbatim/API/API_TD_2_Method_Header.txt`
- `prompts-verbatim/API/API_TD_2_Method_Header_BreakDown.txt`
- `prompts-verbatim/API/API_TD_3_Schema_Validation.txt`
- `prompts-verbatim/API/API_TD_3_Schema_Validation_BreakDown.txt`
- `prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic.txt`
- `prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.txt`
- `prompts-verbatim/API/API_Gen_TC_From_TD_v2.txt`

#### API Gen Script
- `prompts-verbatim/API/Gen Script/API_TestCase_Analysis.txt`
- `prompts-verbatim/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt`
- `prompts-verbatim/API/Gen Script/API_Gen_Script_Validation_Feature.txt`
- `prompts-verbatim/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt`

#### UI
- `prompts-verbatim/UI/UI_Gen_TD.txt`
- `prompts-verbatim/UI/UI_Gen_TC_From_TD.txt`
- `prompts-verbatim/UI/UI_Gen_TC_For_UAT.txt`

**Tác dụng**:
- giữ bản prompt runtime đúng source
- làm cơ sở cho `scripts/verify_prompt_mirrors.py`
- tránh native/freeform generation lệch hành vi gốc

---

## 9. Folder `data/`

### 9.1 `data/output-contracts/`

**Mục đích**: định nghĩa contract đầu ra để validator và report bám theo.

| File | Tác dụng |
|---|---|
| `legacy_19_column_testcase_contract.md` | Contract testcase legacy 19 cột. |
| `uat_16_column_testcase_contract.md` | Contract testcase UAT 16 cột. |
| `test_generation_matrix_contract.md` | Contract cho Coverage/Test Generation Matrix. |
| `markdown_normalization_rules.md` | Quy tắc normalize Markdown. |
| `excel_output_similarity.md` | Quy tắc similarity/parity với output Excel BIDV. |
| `testcase_excel_columns.md` | Mô tả cột testcase cho Excel/TestLink/XRAY-style. |
| `test_status_excel_columns.md` | Mô tả cột trạng thái execution. |
| `manual_execution_reader_contract.md` | Contract cho bước đọc manual execution. |
| `paygates_dashboard_contract.md` | Contract dashboard Paygates. |
| `xray_field_mapping.md` | Mapping trường XRAY/Jira. |
| `test_plan_contract.md` | Contract cho Test Plan. |
| `api_automation_analysis_contract.md` | Contract cho artifact phân tích testcase automation. |
| `api_automation_feature_contract.md` | Contract cho Gherkin feature automation. |

### 9.2 `data/source-inventory/`

**Mục đích**: tài liệu reference cho routing, source mapping, workflow map.

| File | Tác dụng |
|---|---|
| `orchestration_mode.md` | Mô tả operating mode duy nhất. |
| `workflow_map.md` | Bản đồ workflow từ source đến output. |
| `prompt_fragment_registry.md` | Registry các fragment prompt và công dụng. |
| `sources.md` | Danh sách nguồn/source references. |
| `prompt_mirror_manifest.json` | Manifest prompt mirror để verify. |

---

## 10. Folder `knowledge/`

### 10.1 `knowledge/standards/`

**Mục đích**: chuẩn nghiệp vụ QA/QC được package hóa.

| File | Tác dụng |
|---|---|
| `qc_delivery_standard.md` | Chuẩn vận hành QC delivery tổng quát. |
| `source_document_standard.md` | Chuẩn intake source document. |
| `test_plan_standard.md` | Chuẩn viết Test Plan. |
| `test_design_standard.md` | Chuẩn viết Test Design. |
| `testcase_standard.md` | Chuẩn viết testcase. |
| `test_generation_matrix_standard.md` | Chuẩn cho matrix/coverage. |
| `excel_output_standard.md` | Chuẩn output Excel. |
| `manual_execution_status_standard.md` | Chuẩn normalize status manual execution. |
| `ai_assisted_testing_standard.md` | Chuẩn AI-assisted testing. |
| `prompt_preservation_standard.md` | Chuẩn bảo toàn prompt. |
| `workflow_non_skip_gate_standard.md` | Chuẩn không được skip gate workflow. |

### 10.2 `knowledge/default/manifests/`

| File | Tác dụng |
|---|---|
| `canonical-sources.yml` | Danh sách nguồn canonical đã package hóa. |
| `normalization-report.json` | Báo cáo normalize knowledge. |
| `redaction-report.yml` | Báo cáo redact secret. |
| `source-manifest.yml` | Manifest nguồn của knowledge pack. |

### 10.3 `knowledge/default/normalized/`

**Mục đích**: kho normalized knowledge rất lớn dùng cho bootstrap/reference. Các file `.md` và `.tsv` trong cây con là dữ liệu nguồn đã chuẩn hóa, **không phải runtime source of truth trực tiếp** trừ khi đi qua pack/manifest/route phù hợp.

---

## 11. Folder `sdk/`

**Mục đích**: lớp runner/headless orchestration bằng Python.

| File | Tác dụng |
|---|---|
| `README.md` | Giải thích design, permission model, prompt mirror enforcement và flow dùng runner. |
| `universal_delivery_runner.py` | Runner phổ quát: build source manifest, classify intent, resolve route, tạo route/support artifacts. |
| `api_delivery_runner.py` | SDK runner cho full API delivery. |
| `paygates_dashboard_runner.py` | Runner deterministic cho dashboard/status. |
| `source_manifest.py` | Xây source manifest. |
| `source_fingerprint.py` | Fingerprint/nhận diện source. |
| `intent_classifier.py` | Phân loại intent từ input/prompt. |
| `workflow_pack_loader.py` | Load workflow pack. |
| `route_planner.py` | Lập route plan từ workflow pack. |
| `output_inference.py` | Suy luận output cần sinh. |
| `validation_orchestrator.py` | Điều phối validate nhiều bước. |
| `hooks.py` | Helper guardrail/hook policy. |
| `mcp_tools.py` | Deterministic helper tools cho inspection/export/import/sync. |

**Hành động folder này hỗ trợ**:
- chạy headless flow
- routing tự động từ file + prompt
- orchestration lặp lại được
- validator orchestration

---

## 12. Folder `scripts/`

**Mục đích**: các script deterministic để export/validate/normalize/bootstrap/sync/publish.

### 12.1 Nhóm export

| File | Tác dụng |
|---|---|
| `export_legacy_19col_tsv.py` | Export testcase Markdown sang TSV 19 cột. |
| `export_legacy_19col_xlsx.py` | Export testcase sang XLSX 19 cột có format. |
| `export_testcase_tsv.py` | Export testcase TSV compatible. |
| `export_execution_tsv.py` | Export execution TSV. |
| `export_paygates_dashboard_tsv.py` | Export dashboard Paygates sang TSV. |
| `export_paygates_dashboard_xlsx.py` | Export dashboard Paygates sang XLSX. |
| `export_test_design_xlsx.py` | Export Test Design sang XLSX. |
| `export_test_plan_xlsx.py` | Export Test Plan sang XLSX. |
| `export_testrail_cases_csv.py` | Export testcase sang CSV cho TestRail import. |

### 12.2 Nhóm validate

| File | Tác dụng |
|---|---|
| `validate_test_plan.py` | Validate Test Plan theo contract. |
| `validate_test_design.py` | Validate API/UI Test Design. |
| `validate_testcase_contract.py` | Validate testcase contract theo profile. |
| `validate_output_contract.py` | Validate output execution/testcase pack. |
| `validate_legacy_19col_tsv.py` | Validate TSV 19 cột. |
| `validate_test_generation_matrix.py` | Validate matrix/coverage. |
| `validate_paygates_dashboard.py` | Validate dashboard Paygates. |
| `validate_tracker.py` | Validate tracker/status workbook logic. |
| `validate_artifact_manifest.py` | Validate manifest publish artifact. |
| `validate_api_automation_analysis.py` | Validate analysis artifact cho automation support. |
| `validate_api_automation_feature.py` | Validate Gherkin feature output. |
| `validate_api_tc_coverage.py` | Validate coverage testcase API. |
| `validate_testcase_coverage.py` | Validate testcase coverage theo profile. |
| `validate_testcase_granularity.py` | Validate granularity của testcase. |
| `validate_api_td_specificity.py` | Validate độ đặc tả của API TD. |
| `validate_api_tc_specificity.py` | Validate độ đặc tả của API testcase. |
| `validate_mandatory_coverage_rules.py` | Validate rule coverage bắt buộc. |
| `validate_normalized_knowledge.py` | Validate normalized knowledge. |
| `validate_nms_sdk_coverage.py` | Validate coverage cho SDK/NMS enrichment. |
| `validate_no_bidv_runtime_refs.py` | Bảo đảm runtime không trỏ về raw BIDV refs. |
| `verify_prompt_mirrors.py` | Verify prompt mirrors khớp source. |
| `verify_runtime_prompt_manifest.py` | Verify runtime prompt manifest. |

### 12.3 Nhóm normalize / intake / migration / sync

| File | Tác dụng |
|---|---|
| `normalize_docs.py` | Chuẩn hóa docs. |
| `redact_secrets.py` | Redact secrets trong knowledge/output. |
| `build_source_manifest.py` | Build manifest nguồn. |
| `create_workflow_candidate.py` | Tạo candidate workflow từ source/context. |
| `extract_xlsx_profiles.py` | Trích profile từ workbook XLSX. |
| `read_manual_execution_results.py` | Đọc kết quả manual execution từ workbook. |
| `sync_paygates_dashboard_xlsx.py` | Sync dashboard TSV sang workbook XLSX. |
| `sync_prompts.py` | Đồng bộ prompts/mirror. |
| `apply_api_skill_updates.py` | Áp thay đổi cho nhóm skill API. |
| `run_closed_loop.py` | Chạy closed-loop delivery flow. |
| `publish_testrail_cases.py` | Publish cases sang TestRail. |

---

## 13. Folder `tests/`

**Mục đích**: test logic orchestration, validator, workflow pack, skill/agent contract và E2E chain.

| File | Tác dụng |
|---|---|
| `test_agent_contracts.py` | Kiểm tra agent nào cũng có Inputs/Outputs/Forbidden behavior; kiểm tra orchestrator và gate chính. |
| `test_validators.py` | Test validator layer. |
| `test_workflow_pack_closed_loop.py` | Test workflow pack closed-loop behavior. |
| `test_universal_router.py` | Test universal routing / route selection. |
| `test_source_manifest.py` | Test source manifest logic. |
| `test_doc_normalizer.py` | Test doc normalization. |
| `test_secret_redactor.py` | Test secret redaction. |
| `test_canonical_sources.py` | Test canonical source mapping. |
| `test_status_enums.py` | Test status enum normalization. |
| `test_xlsx_profiles.py` | Test trích profile XLSX. |
| `test_paygates_tracker_audit.py` | Test audit/tracker Paygates. |
| `test_supervisor_loop.py` | Test vòng đời supervisor loop. |
| `test_e2e_api_workflow.py` | Test E2E route API workflow. |
| `test_e2e_api_automation_workflow.py` | Test E2E API automation workflow. |
| `test_e2e_test_plan_workflow.py` | Test E2E Test Plan workflow. |
| `test_e2e_ui_uat_workflow.py` | Test E2E UI/UAT workflow. |

---

## 14. Folder `cypress/`

**Mục đích**: browser-based demo automation flow từ testcase TSV đã generate.

| File | Tác dụng |
|---|---|
| `cypress/e2e/customer_validate.cy.js` | Dùng fixture `testCases.json` để tạo các case API mock bằng `cy.intercept`, sau đó gọi local mock server và assert status/code/message theo testcase. |
| `cypress/fixtures/testCases.json` | Fixture được generate từ TSV qua `cypress.config.js`. |

**Quan hệ**:
- `cypress.config.js` đọc `outputs/run-customer-validate/Legacy19TestCase.generated.tsv`
- convert sang `cypress/fixtures/testCases.json`
- Cypress spec dùng fixture đó để chạy case demo

---

## 15. Folder `examples/`

**Mục đích**: ví dụ/golden outputs giúp so sánh output thật với baseline.

### Cấu trúc chính

| Folder | Tác dụng |
|---|---|
| `examples/e2e/` | Ví dụ output E2E theo từng route: `api-automation`, `api-cctg`, `test-plan`, `ui-uat`. |
| `examples/full-xray-chain/` | Chain mẫu đầy đủ từ RequirementInventory -> TestCase -> TestExecution -> Dashboard. |
| `examples/golden-outputs/` | Baseline output/golden files để parity và validation. |
| `examples/sdk/` | Ví dụ cách dùng SDK runner và dashboard sync. |

### File đại diện

- `examples/e2e/api-automation/API_TestCase_Analysis.md`: ví dụ analysis cho automation support
- `examples/e2e/api-automation/*.feature`: ví dụ Gherkin output
- `examples/full-xray-chain/CoverageMatrix.md`: ví dụ matrix traceability
- `examples/full-xray-chain/Legacy19TestCase.generated.xlsx`: ví dụ output XLSX
- `examples/golden-outputs/testcase-legacy-19col.tsv`: golden testcase TSV
- `examples/sdk/api_delivery_runner.example.md` và `paygates_dashboard_runner.example.md`: ví dụ CLI usage

---

## 16. Folder `artifacts/`

**Mục đích**: chứa artifact audit và draft artifacts của các run.

### Cấu trúc chính

| Path | Tác dụng |
|---|---|
| `artifacts/audit/skill_readiness_audit.md` | Audit readiness tổng quát. |
| `artifacts/audit/skill_readiness_audit_deep.md` | Audit readiness sâu hơn. |
| `artifacts/audit/repo_structure_report.md` | Report phân tích cấu trúc repo này. |
| `artifacts/default/draft/...` | Các artifact draft của route cụ thể, ví dụ source extract, route plan, API TD, matrix, testcase, review, approval, comparison data. |

**Ý nghĩa runtime**:
- `draft/` là nơi generator và intermediate artifact nằm trước khi publish
- orchestrator trong `AGENT.md` đã quy định chỉ publish-approved outputs mới được đi tiếp

---

## 17. Folder `outputs/`

**Mục đích**: kết quả của các run mẫu/thực tế theo run id riêng.

### Run folder đang thấy

| Folder | Tác dụng |
|---|---|
| `outputs/run-customer-testplan/` | Output route sinh Test Plan, gồm `route_plan.json`, `source_manifest.json`, `validation_report.json`, `OutputReview.md`, `SupervisorApproval.md`, `published-artifact-manifest.yml`, `TestPlan.md`, `TestPlan.generated.xlsx`. |
| `outputs/run-customer-validate/` | Output route sinh API TD + testcase + handoff summary + artifacts liên quan; còn được Cypress dùng làm input TSV. |
| `outputs/run-validate-customer/` | Output route khác ở mức route plan/validation summary. |

**Nhóm file thường gặp trong mỗi run**:
- `route_plan.json`: kế hoạch route đã chọn
- `source_manifest.json`: manifest nguồn
- `validation_report.json`: kết quả validator
- `OutputReview.md`: review gate
- `SupervisorApproval.md`: approval gate
- `published-artifact-manifest.yml`: publish result
- artifact chuyên biệt như `API_TestDesign.md`, `Legacy19TestCase.generated.tsv`, `handoff_summary.md`

---

## 18. Folder `playbooks/`

**Mục đích**: recipe cho team orchestration.

### File chính

| File | Tác dụng |
|---|---|
| `playbooks/agent-teams/api_delivery_team.md` | Công thức team đầy đủ cho API delivery. |
| `playbooks/agent-teams/output_review_team.md` | Công thức team review song song. |
| `playbooks/agent-teams/closed_loop_delivery_team.md` | Công thức team cho closed-loop delivery. |

---

## 19. Mối quan hệ giữa các folder

```text
README.md
-> agents/delivery-orchestrator/
-> workflow-packs/default/
   -> prompts/
   -> contracts/
   -> validators
-> skills/
-> scripts/ + sdk/
-> tests/
-> artifacts/ + outputs/
```

### Diễn giải
- `agents/` định nghĩa **ai làm gì**
- `skills/` định nghĩa **khả năng nghiệp vụ nào có sẵn**
- `workflow-packs/default/` định nghĩa **khi nào dùng khả năng nào, qua stage nào, validator nào**
- `prompts-verbatim/` và `workflow-packs/default/prompts/` giữ **hành vi prompt runtime**
- `data/` và `knowledge/` giữ **contract + standard + source mapping**
- `scripts/` và `sdk/` cung cấp **deterministic tooling và runner**
- `tests/` kiểm tra repo vẫn giữ đúng contract/orchestration behavior
- `examples/`, `artifacts/`, `outputs/` cho thấy **output mẫu, output draft, output runtime**

---

## 20. Kết luận

Repo này được tổ chức như một **hệ điều phối tài liệu QA/QC nhiều tầng**, không phải chỉ là bộ prompt rời rạc. Trục chính của nó là:

1. **Orchestrator** quyết định route và gate.
2. **Workflow pack** quyết định stage, prompt, validator, output.
3. **Skills + agents** thực thi từng phần của flow.
4. **Scripts + SDK** làm lớp deterministic cho export/validate/run.
5. **Standards + contracts + prompt mirrors** bảo đảm output bám đúng chuẩn BIDV.
6. **Artifacts/outputs/examples/tests** là bằng chứng cho vòng đời tạo, kiểm tra và bàn giao artifact.

Nếu cần phân tích sâu hơn nữa, bước tiếp theo hợp lý là tạo thêm một **appendix chi tiết theo từng file trong từng folder** cho các nhóm `scripts/`, `sdk/`, `agents/`, `skills/`.
---

## 21. Appendix inventory đầy đủ theo file
Phần này liệt kê toàn bộ file hiện thấy, loại trừ `.git/` và `node_modules/`, để đáp ứng yêu cầu kiểm kê từng file. Các mô tả ngắn được chuẩn hóa theo path, tên file và nhóm chức năng.

- Tổng số file được kiểm kê: `562`
- Số lượng theo top-level folder/file:
  - `.claude`: 1 file
  - `.gitignore`: 1 file
  - `README.md`: 1 file
  - `agents`: 24 file
  - `artifacts`: 21 file
  - `cypress`: 2 file
  - `cypress.config.js`: 1 file
  - `data`: 25 file
  - `examples`: 55 file
  - `knowledge`: 179 file
  - `outputs`: 32 file
  - `package-lock.json`: 1 file
  - `package.json`: 1 file
  - `playbooks`: 3 file
  - `prompts-verbatim`: 15 file
  - `scripts`: 51 file
  - `sdk`: 32 file
  - `skills`: 45 file
  - `tests`: 16 file
  - `workflow-packs`: 56 file

### 21.x `.claude`

| File | Tác dụng ngắn |
|---|---|
| `.claude/settings.example.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |

### 21.x `.gitignore`

| File | Tác dụng ngắn |
|---|---|
| `.gitignore` | Quy tắc loại trừ file khỏi git. |

### 21.x `README.md`

| File | Tác dụng ngắn |
|---|---|
| `README.md` | Tài liệu hướng dẫn/tổng quan cho phạm vi chứa file. |

### 21.x `agents`

| File | Tác dụng ngắn |
|---|---|
| `agents/api-test-design-agent/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/automation-support-agent/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/contract-validator/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/coverage-auditor/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/delivery-orchestrator/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/delivery-orchestrator/playbooks/full_chain_handoff.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |
| `agents/delivery-orchestrator/playbooks/prompt_compatible_orchestration.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |
| `agents/delivery-orchestrator/playbooks/prompt_migration.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |
| `agents/delivery-orchestrator/playbooks/universal_file_prompt_workflow.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `agents/delivery-orchestrator/playbooks/xray_delivery.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |
| `agents/delivery-orchestrator/prompts/output_contract_review.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |
| `agents/delivery-orchestrator/prompts/task_package_intake.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |
| `agents/delivery-orchestrator/skills_manifest.yml` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `agents/delivery-orchestrator/tools_manifest.yml` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `agents/format-normalizer/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/knowledge-retriever/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/output-reviewer/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/qa-reviewer/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/requirement-coverage-analyst/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/spec-ui-locator/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/supervisor/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/test-set-execution-manager/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/testcase-generator/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |
| `agents/ui-test-design-agent/AGENT.md` | Định nghĩa role/goal/input/output/forbidden behavior của agent. |

### 21.x `artifacts`

| File | Tác dụng ngắn |
|---|---|
| `artifacts/audit/repo_structure_report.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/audit/skill_readiness_audit.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/audit/skill_readiness_audit_deep.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/BIDV_capability_parity_assessment.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/API_OperationInventory.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/API_TestDesign.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/compare_expected_generated.py` | Python module/helper trong SDK hoặc tooling. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/comparison_data.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/ComparisonReview.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/granularity_validation.log` | File hỗ trợ/runtime artifact trong repo. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/Legacy19TestCase.formatted.xlsx` | Workbook Excel output/golden/reference artifact. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/Legacy19TestCase.generated.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/Legacy19TestCase.generated.xlsx` | Workbook Excel output/golden/reference artifact. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/OutputReview.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/RoutePlan.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/source.pdf` | Source document/reference input dạng PDF. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/SourceExtract.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/SourceExtract.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/SupervisorApproval.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/TestCaseSource.md` | Markdown audit/draft artifact trong lifecycle. |
| `artifacts/default/draft/KH-660-CCTG-API-testcases/TestGenerationMatrix.md` | Markdown audit/draft artifact trong lifecycle. |

### 21.x `cypress`

| File | Tác dụng ngắn |
|---|---|
| `cypress/e2e/customer_validate.cy.js` | JavaScript config/spec cho Cypress hoặc tooling. |
| `cypress/fixtures/testCases.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |

### 21.x `cypress.config.js`

| File | Tác dụng ngắn |
|---|---|
| `cypress.config.js` | Cấu hình Cypress và fixture generation cho E2E demo. |

### 21.x `data`

| File | Tác dụng ngắn |
|---|---|
| `data/bidv/excel_profile_map.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `data/bidv/prompt_map.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `data/bidv/source_registry.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `data/output-contracts/api_automation_analysis_contract.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/api_automation_feature_contract.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/excel_output_similarity.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/legacy_19_column_testcase_contract.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/mandatory_test_coverage_rules.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `data/output-contracts/manual_execution_reader_contract.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/markdown_normalization_rules.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/paygates_dashboard_contract.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/test_generation_matrix_contract.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/test_plan_contract.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/test_status_excel_columns.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/testcase_excel_columns.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/uat_16_column_testcase_contract.md` | Contract hoặc source-inventory reference. |
| `data/output-contracts/xray_field_mapping.md` | Contract hoặc source-inventory reference. |
| `data/source-inventory/orchestration_mode.md` | Contract hoặc source-inventory reference. |
| `data/source-inventory/prompt_fragment_registry.md` | Contract hoặc source-inventory reference. |
| `data/source-inventory/prompt_mirror_manifest.json` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `data/source-inventory/sources.md` | Contract hoặc source-inventory reference. |
| `data/source-inventory/workflow_map.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `data/source-knowledge/excel_profile_map.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `data/source-knowledge/prompt_map.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `data/source-knowledge/source_registry.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |

### 21.x `examples`

| File | Tác dụng ngắn |
|---|---|
| `examples/e2e/api-automation/api_logic_business.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `examples/e2e/api-automation/api_method_header_validation.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `examples/e2e/api-automation/API_TestCase_Analysis.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/api-automation/api_validation.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `examples/e2e/api-automation/OutputReview.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/api-automation/SupervisorApproval.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/api-automation/TestCaseSource.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/api-cctg/API_OperationInventory.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/api-cctg/API_TestDesign.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/api-cctg/OutputReview.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/api-cctg/SupervisorApproval.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/api-cctg/TestCaseSource.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/README.md` | Tài liệu hướng dẫn/tổng quan cho phạm vi chứa file. |
| `examples/e2e/test-plan/OutputReview.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/test-plan/SupervisorApproval.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/test-plan/TestPlan.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/ui-uat/OutputReview.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/ui-uat/SupervisorApproval.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/ui-uat/UAT_TestCaseSource.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/ui-uat/UI_TestCaseSource.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/e2e/ui-uat/UI_TestDesign.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/full-xray-chain/CoverageMatrix.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/full-xray-chain/Legacy19TestCase.generated.xlsx` | Workbook Excel output/golden/reference artifact. |
| `examples/full-xray-chain/Legacy19TestCase.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/full-xray-chain/PaygatesDashboard.from-manual.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/full-xray-chain/PaygatesDashboard.generated.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/full-xray-chain/PaygatesDashboard.generated.xlsx` | Workbook Excel output/golden/reference artifact. |
| `examples/full-xray-chain/PaygatesDashboard.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/full-xray-chain/PaygatesDashboard.synced-from-source.xlsx` | Workbook Excel output/golden/reference artifact. |
| `examples/full-xray-chain/PaygatesDashboard.synced.xlsx` | Workbook Excel output/golden/reference artifact. |
| `examples/full-xray-chain/RequirementInventory.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/full-xray-chain/TestCase.generated.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/full-xray-chain/TestCase.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/full-xray-chain/TestExecution.from-manual.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/full-xray-chain/TestExecution.generated.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/full-xray-chain/TestExecution.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/full-xray-chain/TestSet.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/golden-outputs/api-test-design.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/golden-outputs/api-testcase-analysis.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/golden-outputs/api_logic_business.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `examples/golden-outputs/api_method_header_validation.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `examples/golden-outputs/api_validation.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `examples/golden-outputs/CoverageMatrix.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/golden-outputs/paygates-dashboard-compatible.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/golden-outputs/paygates-dashboard-compatible.xlsx` | Workbook Excel output/golden/reference artifact. |
| `examples/golden-outputs/test-execution-compatible.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/golden-outputs/test-plan.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/golden-outputs/testcase-compatible.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/golden-outputs/testcase-legacy-19col.formatted.xlsx` | Workbook Excel output/golden/reference artifact. |
| `examples/golden-outputs/testcase-legacy-19col.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `examples/golden-outputs/testcase-legacy-19col.xlsx` | Workbook Excel output/golden/reference artifact. |
| `examples/golden-outputs/ui-test-design.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/sdk/api_delivery_runner.example.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/sdk/paygates_dashboard_runner.example.md` | Markdown example/golden artifact cho route tương ứng. |
| `examples/sdk/paygates_dashboard_sync.example.md` | Markdown example/golden artifact cho route tương ứng. |

### 21.x `knowledge`

| File | Tác dụng ngắn |
|---|---|
| `knowledge/default/manifests/canonical-sources.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `knowledge/default/manifests/normalization-report.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `knowledge/default/manifests/redaction-report.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `knowledge/default/manifests/source-manifest.yml` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `knowledge/default/normalized/api_automation/nms_sdk/__init__.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/nms_sdk/assertions.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/nms_sdk/client.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/nms_sdk/endpoints.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/nms_sdk/headers.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/nms_sdk/schemas.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/nms_sdk/smoke.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/README.md` | Tài liệu hướng dẫn/tổng quan cho phạm vi chứa file. |
| `knowledge/default/normalized/api_automation/tests/test_client.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/tests/test_common_utilities.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/api_automation/tests/test_endpoint_catalog.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.Trang_t_nh1.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.Trang_t_nh2.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.Trang_t_nh3.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713-tcs.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713-tcs.Trang_t_nh1.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713-tcs.Trang_t_nh2.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/PTTK/DLHCM-[LH]_Squad 08_Rating_PTTK Chi tiết Sprint 5-160526-035458.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/PTTK/NMS-[KH-660][CCTG Online] API lấy thông tin người giới thiệu bằng mã cán bộ-160526-040727.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/PTTK/NMS-[KH-660][CCTG Online] API thông tin nhóm CCTG-160526-040705.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/CustomerIn-0.1 Đăng nhập SSO & Phân Quyền OneAccess-160526-035609.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_A/Làm rõ thông tin/NMS-KH truy vấn Chứng nhận quyền sở hữu CCTG (CNTG) của khoản CCTG đã mua trước đó-160526-040143.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_A/Làm rõ thông tin/NMS-Luồng KH rút trước hạn-160526-040235.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_A/Làm rõ thông tin/NMS-Luồng tất toán CCTG-160526-040404.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_A/Làm rõ thông tin/NMS-Đặc điểm CCTG và luồng mua CCTG-160526-040059.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_A/NMS-[KH-660][CCTG Online][URD]-160526-040025.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_B/PS0082025-BO_001.RSD_Quản lý Màn Hình Tham Số-160526-041133.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_B/Tài liệu reference trong RSD/PS0082025-MH1 Màn hình Quản lý tìm kiếm-160526-041158.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_B/Tài liệu reference trong RSD/PS0082025-MH2 Thêm mới Màn hình tham số-160526-041237.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_B/Tài liệu reference trong RSD/PS0082025-MH3 Chỉnh sửa Màn hình tham số.-160526-041254.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Faker_upd/RSD/RSD_B/Tài liệu reference trong RSD/PS0082025-MH4 Xem chi tiết Màn hình tham số.-160526-041329.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/[Old]_API_Gen_TC_From_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/[Old]_API_Gen_TD_v1.2.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/[Review_Prompt]Claude_Sonet_4.6.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/[Review_Prompt]Gemini_Pro_3_1.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/[Review_Prompt]Gemini_Pro_3_2.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/[Review_TD]Claude_Sonet_4.6.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/[Review_TD]Gemini_pro_3.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_Gen_TC_From_TD_v2.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_NewParameterGuideline.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_NewParameterGuideline.Sheet1.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Prompt/API/API_TD_1_Setup_Context.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_TD_2_Method_Header.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_TD_2_Method_Header_BreakDown.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_TD_3_Schema_Validation.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_TD_3_Schema_Validation_BreakDown.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_TD_4_Value_Business_Cross_Logic.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/Gen Script/API_Gen_Script_Logic_Business_Feature.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/Gen Script/API_Gen_Script_Validation_Feature.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/Gen Script/api_logic_business_example.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/Gen Script/api_method_header_validation_example.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/Gen Script/API_TestCase_Analysis.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/Gen Script/api_validation_example.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/API/Gen Script/properties.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/Side Workshop/Workshop Hướng dẫn sử dụng AI sinh test case.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/UI/UI_Gen_TC_For_UAT.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/UI/UI_Gen_TC_From_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Prompt/UI/UI_Gen_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/template/Template_PTTK_AI.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/template/Template_PTTK_AI_ChiTiet_API.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/template/Template_RSD_AI.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/template/Template_RSD_ChiTiet_AI.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).Sprint_8.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_Base.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_BO.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_CnR.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_DevPortal.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_Tester.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_VA.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).T_ng_h_p_chung.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).T_ng_H_p_Test_Case_Automation_T.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/Tổng hợp Trạng Thái Test Case Paygates (1).T_ng_H_p_Test_Case_Theo_Sprint.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/normalized/UI/UI_Gen_TC_For_UAT.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/UI/UI_Gen_TC_From_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/normalized/UI/UI_Gen_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/nms_sdk/__init__.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/nms_sdk/assertions.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/nms_sdk/client.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/nms_sdk/endpoints.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/nms_sdk/headers.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/nms_sdk/schemas.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/nms_sdk/smoke.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/README.md` | Tài liệu hướng dẫn/tổng quan cho phạm vi chứa file. |
| `knowledge/default/redacted/api_automation/tests/test_client.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/tests/test_common_utilities.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/api_automation/tests/test_endpoint_catalog.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.Trang_t_nh1.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.Trang_t_nh2.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.Trang_t_nh3.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713-tcs.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713-tcs.Trang_t_nh1.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713-tcs.Trang_t_nh2.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/PTTK/DLHCM-[LH]_Squad 08_Rating_PTTK Chi tiết Sprint 5-160526-035458.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/PTTK/NMS-[KH-660][CCTG Online] API lấy thông tin người giới thiệu bằng mã cán bộ-160526-040727.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/PTTK/NMS-[KH-660][CCTG Online] API thông tin nhóm CCTG-160526-040705.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/CustomerIn-0.1 Đăng nhập SSO & Phân Quyền OneAccess-160526-035609.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_A/Làm rõ thông tin/NMS-KH truy vấn Chứng nhận quyền sở hữu CCTG (CNTG) của khoản CCTG đã mua trước đó-160526-040143.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_A/Làm rõ thông tin/NMS-Luồng KH rút trước hạn-160526-040235.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_A/Làm rõ thông tin/NMS-Luồng tất toán CCTG-160526-040404.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_A/Làm rõ thông tin/NMS-Đặc điểm CCTG và luồng mua CCTG-160526-040059.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_A/NMS-[KH-660][CCTG Online][URD]-160526-040025.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_B/PS0082025-BO_001.RSD_Quản lý Màn Hình Tham Số-160526-041133.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_B/Tài liệu reference trong RSD/PS0082025-MH1 Màn hình Quản lý tìm kiếm-160526-041158.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_B/Tài liệu reference trong RSD/PS0082025-MH2 Thêm mới Màn hình tham số-160526-041237.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_B/Tài liệu reference trong RSD/PS0082025-MH3 Chỉnh sửa Màn hình tham số.-160526-041254.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Faker_upd/RSD/RSD_B/Tài liệu reference trong RSD/PS0082025-MH4 Xem chi tiết Màn hình tham số.-160526-041329.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/[Old]_API_Gen_TC_From_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/[Old]_API_Gen_TD_v1.2.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/[Review_Prompt]Claude_Sonet_4.6.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/[Review_Prompt]Gemini_Pro_3_1.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/[Review_Prompt]Gemini_Pro_3_2.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/[Review_TD]Claude_Sonet_4.6.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/[Review_TD]Gemini_pro_3.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_Gen_TC_From_TD_v2.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_NewParameterGuideline.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_NewParameterGuideline.Sheet1.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Prompt/API/API_TD_1_Setup_Context.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_TD_2_Method_Header.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_TD_2_Method_Header_BreakDown.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_TD_3_Schema_Validation.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_TD_3_Schema_Validation_BreakDown.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_TD_4_Value_Business_Cross_Logic.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/Gen Script/API_Gen_Script_Logic_Business_Feature.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/Gen Script/API_Gen_Script_Validation_Feature.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/Gen Script/api_logic_business_example.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/Gen Script/api_method_header_validation_example.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/Gen Script/API_TestCase_Analysis.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/Gen Script/api_validation_example.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/API/Gen Script/properties.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/Side Workshop/Workshop Hướng dẫn sử dụng AI sinh test case.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/UI/UI_Gen_TC_For_UAT.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/UI/UI_Gen_TC_From_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Prompt/UI/UI_Gen_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/template/Template_PTTK_AI.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/template/Template_PTTK_AI_ChiTiet_API.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/template/Template_RSD_AI.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/template/Template_RSD_ChiTiet_AI.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).Sprint_8.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_Base.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_BO.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_CnR.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_DevPortal.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_Tester.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).Squad_VA.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).T_ng_h_p_chung.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).T_ng_H_p_Test_Case_Automation_T.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/Tổng hợp Trạng Thái Test Case Paygates (1).T_ng_H_p_Test_Case_Theo_Sprint.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `knowledge/default/redacted/UI/UI_Gen_TC_For_UAT.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/UI/UI_Gen_TC_From_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/redacted/UI/UI_Gen_TD.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/default/schemas/status-enums.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `knowledge/default/schemas/xlsx-profiles.yml` | Cấu hình YAML cho source, workflow, registry hoặc policy. |
| `knowledge/standards/ai_assisted_testing_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/excel_output_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/manual_execution_status_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/prompt_preservation_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/qc_delivery_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/source_document_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/test_design_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/test_generation_matrix_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/test_plan_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/testcase_standard.md` | Knowledge/standard/source đã chuẩn hóa hoặc tài liệu chuẩn. |
| `knowledge/standards/workflow_non_skip_gate_standard.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |

### 21.x `outputs`

| File | Tác dụng ngắn |
|---|---|
| `outputs/run-customer-testplan/closed-loop-state.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-customer-testplan/no_secret_report.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-customer-testplan/OutputReview.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-testplan/published-artifact-manifest.yml` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `outputs/run-customer-testplan/route_plan.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-customer-testplan/source_manifest.json` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `outputs/run-customer-testplan/source_trace.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-testplan/SupervisorApproval.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-testplan/TestPlan.generated.xlsx` | Workbook Excel output/golden/reference artifact. |
| `outputs/run-customer-testplan/TestPlan.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-testplan/validation_report.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-customer-validate/API_OperationInventory.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-validate/API_TestDesign.generated.xlsx` | Workbook Excel output/golden/reference artifact. |
| `outputs/run-customer-validate/API_TestDesign.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-validate/closed-loop-state.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-customer-validate/handoff_summary.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-validate/Legacy19TestCase.generated.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `outputs/run-customer-validate/Legacy19TestCase.generated.xlsx` | Workbook Excel output/golden/reference artifact. |
| `outputs/run-customer-validate/no_secret_report.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-customer-validate/OutputReview.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-validate/published-artifact-manifest.yml` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `outputs/run-customer-validate/route_plan.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-customer-validate/source_manifest.json` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `outputs/run-customer-validate/source_trace.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-validate/SupervisorApproval.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-validate/TestCaseSource.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-customer-validate/TestRailImport.generated.csv` | File hỗ trợ/runtime artifact trong repo. |
| `outputs/run-customer-validate/validation_report.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-validate-customer/handoff_summary.md` | Markdown artifact sinh ra từ một run. |
| `outputs/run-validate-customer/route_plan.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |
| `outputs/run-validate-customer/source_manifest.json` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `outputs/run-validate-customer/validation_report.json` | Dữ liệu cấu hình, manifest, validation report hoặc fixture JSON. |

### 21.x `package-lock.json`

| File | Tác dụng ngắn |
|---|---|
| `package-lock.json` | Lock dependency Node/npm. |

### 21.x `package.json`

| File | Tác dụng ngắn |
|---|---|
| `package.json` | Metadata npm và dependency/script Node. |

### 21.x `playbooks`

| File | Tác dụng ngắn |
|---|---|
| `playbooks/agent-teams/api_delivery_team.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |
| `playbooks/agent-teams/closed_loop_delivery_team.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |
| `playbooks/agent-teams/output_review_team.md` | Tài liệu Markdown phục vụ vận hành hoặc tham chiếu. |

### 21.x `prompts-verbatim`

| File | Tác dụng ngắn |
|---|---|
| `prompts-verbatim/API/API_Gen_TC_From_TD_v2.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/API_TD_1_Setup_Context.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/API_TD_2_Method_Header.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/API_TD_2_Method_Header_BreakDown.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/API_TD_3_Schema_Validation.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/API_TD_3_Schema_Validation_BreakDown.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/Gen Script/API_Gen_Script_Validation_Feature.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/API/Gen Script/API_TestCase_Analysis.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/UI/UI_Gen_TC_For_UAT.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/UI/UI_Gen_TC_From_TD.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `prompts-verbatim/UI/UI_Gen_TD.txt` | Prompt verbatim hoặc text extract/source intermediate. |

### 21.x `scripts`

| File | Tác dụng ngắn |
|---|---|
| `scripts/__pycache__/export_legacy_19col_tsv.cpython-314.pyc` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/__pycache__/export_testrail_cases_csv.cpython-314.pyc` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/__pycache__/publish_testrail_cases.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `scripts/apply_api_skill_updates.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/build_source_manifest.py` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `scripts/create_workflow_candidate.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/export_execution_tsv.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/export_legacy_19col_tsv.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/export_legacy_19col_xlsx.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/export_paygates_dashboard_tsv.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/export_paygates_dashboard_xlsx.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/export_test_design_xlsx.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/export_test_plan_xlsx.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/export_testcase_tsv.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/export_testrail_cases_csv.py` | Script export artifact sang TSV/XLSX/CSV hoặc format bàn giao. |
| `scripts/extract_xlsx_profiles.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/lib/__pycache__/minimal_xlsx.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `scripts/lib/markdown_tables.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/lib/minimal_xlsx.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/lib/paygates_dashboard.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/lib/xlsx_table.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/normalize_docs.py` | Script normalize tài liệu/source. |
| `scripts/publish_testrail_cases.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/read_manual_execution_results.py` | Script đọc/parse dữ liệu đầu vào hoặc execution result. |
| `scripts/redact_secrets.py` | Script redact secret/sensitive data. |
| `scripts/run_closed_loop.py` | Python module/helper trong SDK hoặc tooling. |
| `scripts/sync_paygates_dashboard_xlsx.py` | Script đồng bộ prompt/dashboard/workbook output. |
| `scripts/sync_prompts.py` | Script đồng bộ prompt/dashboard/workbook output. |
| `scripts/validate_api_automation_analysis.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_api_automation_feature.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_api_tc_coverage.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_api_tc_specificity.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_api_td_specificity.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_artifact_manifest.py` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `scripts/validate_legacy_19col_tsv.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_mandatory_coverage_rules.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_nms_sdk_coverage.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_no_bidv_runtime_refs.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_normalized_knowledge.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_output_contract.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_paygates_dashboard.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_test_design.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_test_generation_matrix.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_test_plan.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_testcase_contract.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_testcase_coverage.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_testcase_granularity.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_tracker.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/validate_workflow_pack.py` | Validator hoặc mapping kiểm tra contract/output. |
| `scripts/verify_prompt_mirrors.py` | Script verify tính nhất quán runtime/prompt manifest. |
| `scripts/verify_runtime_prompt_manifest.py` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |

### 21.x `sdk`

| File | Tác dụng ngắn |
|---|---|
| `sdk/__pycache__/intent_classifier.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/__pycache__/route_planner.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/__pycache__/source_fingerprint.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/__pycache__/source_manifest.cpython-314.pyc` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `sdk/__pycache__/universal_delivery_runner.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/__pycache__/validation_orchestrator.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/__pycache__/workflow_pack_loader.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/api_delivery_runner.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/hooks.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/intent_classifier.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/mcp_tools.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/output_inference.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/output_publishers/__init__.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/output_publishers/__pycache__/__init__.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/output_publishers/__pycache__/google_sheets_publisher.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/output_publishers/__pycache__/testrail_publisher.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/output_publishers/google_sheets_publisher.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/output_publishers/testrail_publisher.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/paygates_dashboard_runner.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/README.md` | Tài liệu hướng dẫn/tổng quan cho phạm vi chứa file. |
| `sdk/route_planner.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/source_adapters/__init__.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/source_adapters/__pycache__/__init__.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/source_adapters/__pycache__/google_sheets.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/source_adapters/__pycache__/local_files.cpython-314.pyc` | File hỗ trợ/runtime artifact trong repo. |
| `sdk/source_adapters/google_sheets.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/source_adapters/local_files.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/source_fingerprint.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/source_manifest.py` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `sdk/universal_delivery_runner.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/validation_orchestrator.py` | Python module/helper trong SDK hoặc tooling. |
| `sdk/workflow_pack_loader.py` | Python module/helper trong SDK hoặc tooling. |

### 21.x `skills`

| File | Tác dụng ngắn |
|---|---|
| `skills/api-automation-support-generate/prompts/api_gen_script_logic_business_feature.md` | Prompt/template/reference Markdown cho skill. |
| `skills/api-automation-support-generate/prompts/api_gen_script_method_header_validation_feature.md` | Prompt/template/reference Markdown cho skill. |
| `skills/api-automation-support-generate/prompts/api_gen_script_validation_feature.md` | Prompt/template/reference Markdown cho skill. |
| `skills/api-automation-support-generate/prompts/api_testcase_analysis.md` | Prompt/template/reference Markdown cho skill. |
| `skills/api-automation-support-generate/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/api-td-generate/prompts/api_td_method_header.md` | Prompt/template/reference Markdown cho skill. |
| `skills/api-td-generate/prompts/api_td_schema_validation.md` | Prompt/template/reference Markdown cho skill. |
| `skills/api-td-generate/prompts/api_td_setup_context.md` | Prompt/template/reference Markdown cho skill. |
| `skills/api-td-generate/prompts/api_td_value_business_cross_logic.md` | Prompt/template/reference Markdown cho skill. |
| `skills/api-td-generate/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/coverage-audit/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/doc-normalizer/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/legacy-xlsx-exporter/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/manual-execution-reader/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/output-verify/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/paygates-dashboard-generate/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/paygates-dashboard-generate/templates/PaygatesDashboard.md` | Prompt/template/reference Markdown cho skill. |
| `skills/paygates-dashboard-sync/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/secret-redactor/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/supervisor-loop/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/tc-generate-from-td/prompts/api_gen_tc_from_td.md` | Prompt/template/reference Markdown cho skill. |
| `skills/tc-generate-from-td/prompts/ui_gen_tc_from_td.md` | Prompt/template/reference Markdown cho skill. |
| `skills/tc-generate-from-td/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/test-execution-pack-generate/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/test-plan-generate/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/test-set-build/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/testcase-validator/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/tracker-validator/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/uat-tc-generate/prompts/ui_gen_tc_for_uat.md` | Prompt/template/reference Markdown cho skill. |
| `skills/uat-tc-generate/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/ui-td-generate/prompts/ui_gen_td.md` | Prompt/template/reference Markdown cho skill. |
| `skills/ui-td-generate/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/xlsx-extractor/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/xray-test-workflow/reference/id_conventions.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/reference/source_priority.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/reference/xray_artifact_mapping.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/SKILL.md` | Định nghĩa metadata, scope, input/output và luật vận hành của skill. |
| `skills/xray-test-workflow/templates/CoverageMatrix.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/templates/OutputReview.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/templates/RequirementInventory.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/templates/TestCase.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/templates/TestDesign.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/templates/TestExecution.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/templates/TestPlan.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `skills/xray-test-workflow/templates/TestSet.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |

### 21.x `tests`

| File | Tác dụng ngắn |
|---|---|
| `tests/test_agent_contracts.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_canonical_sources.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_doc_normalizer.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_e2e_api_automation_workflow.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_e2e_api_workflow.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_e2e_test_plan_workflow.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_e2e_ui_uat_workflow.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_paygates_tracker_audit.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_secret_redactor.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_source_manifest.py` | Manifest/registry mô tả nguồn, artifact hoặc prompt/runtime metadata. |
| `tests/test_status_enums.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_supervisor_loop.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_universal_router.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_validators.py` | Validator hoặc mapping kiểm tra contract/output. |
| `tests/test_workflow_pack_closed_loop.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |
| `tests/test_xlsx_profiles.py` | Pytest kiểm tra behavior/contract/validator/route tương ứng. |

### 21.x `workflow-packs`

| File | Tác dụng ngắn |
|---|---|
| `workflow-packs/default/artifact-policy.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/canonical-sources.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/classifiers.json` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/classifiers.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/api_automation_analysis_contract.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/api_automation_feature_contract.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/excel_output_similarity.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/legacy_19_column_testcase_contract.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/manual_execution_reader_contract.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/markdown_normalization_rules.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/paygates_dashboard_contract.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/test_generation_matrix_contract.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/test_plan_contract.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/test_status_excel_columns.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/testcase_excel_columns.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/uat_16_column_testcase_contract.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/contracts/xray_field_mapping.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/examples/api-test-design.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/examples/api-testcase-analysis.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/examples/api_logic_business.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `workflow-packs/default/examples/api_method_header_validation.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `workflow-packs/default/examples/api_validation.feature` | Gherkin feature output hoặc golden example cho API automation. |
| `workflow-packs/default/examples/paygates-dashboard-compatible.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `workflow-packs/default/examples/paygates-dashboard-compatible.xlsx` | Workbook Excel output/golden/reference artifact. |
| `workflow-packs/default/examples/test-execution-compatible.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `workflow-packs/default/examples/test-plan.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/examples/testcase-compatible.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `workflow-packs/default/examples/testcase-legacy-19col.formatted.xlsx` | Workbook Excel output/golden/reference artifact. |
| `workflow-packs/default/examples/testcase-legacy-19col.tsv` | Bảng TSV dữ liệu testcase/execution/dashboard/normalized source. |
| `workflow-packs/default/examples/testcase-legacy-19col.xlsx` | Workbook Excel output/golden/reference artifact. |
| `workflow-packs/default/examples/ui-test-design.md` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/excel-contract.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/output_profiles.json` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/output_profiles.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/prompts/API/API_Gen_TC_From_TD_v2.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/API_TD_1_Setup_Context.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/API_TD_2_Method_Header.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/API_TD_2_Method_Header_BreakDown.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/API_TD_3_Schema_Validation.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/API_TD_3_Schema_Validation_BreakDown.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/API_TD_4_Value_Business_Cross_Logic.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/Gen Script/API_Gen_Script_Validation_Feature.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/API/Gen Script/API_TestCase_Analysis.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/UI/UI_Gen_TC_For_UAT.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/UI/UI_Gen_TC_From_TD.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/prompts/UI/UI_Gen_TD.txt` | Prompt verbatim hoặc text extract/source intermediate. |
| `workflow-packs/default/README.md` | Tài liệu hướng dẫn/tổng quan cho phạm vi chứa file. |
| `workflow-packs/default/review-gates.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/status-enums.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/validators.json` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/validators.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/workflow.json` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |
| `workflow-packs/default/workflow.yml` | Định nghĩa hoặc tài liệu workflow/route/stage/gate. |

