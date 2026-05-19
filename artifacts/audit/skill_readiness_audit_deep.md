# Deep audit readiness qc-agent-skills sau rename

## 1. Executive summary

Kết luận: `qc-agent-skills/` hiện đã bao phủ phần lớn chuỗi đầu ra BIDV chính, gồm API Test Design, API/UI testcase 19 cột, UI Test Design, UAT testcase 16 cột, Paygates dashboard/status, manual execution import, XRAY/TestLink-style traceability, review/supervisor/publish lifecycle và một phần API automation support.

Readiness tổng theo ma trận bắt buộc: **25 / 28 điểm = 89.3%**.

So với audit cũ 88.5%, readiness tăng nhẹ nhờ blocker prompt mirror đã được xử lý, prompt verifier pass, path rename sau `bidv` không làm gãy workflow pack, và các validator golden output chính pass. Tuy nhiên package vẫn chưa đạt 100% vì còn một số gap quan trọng: API automation mới ở mức prompt/support + scaffold, chưa chứng minh chạy end-to-end với framework thật; registry/workflow có điểm lệch traceability giữa prompt `*_BreakDown` và manifest mirror hiện tại; pytest suite chưa chạy được trong môi trường hiện tại vì thiếu `pytest`; một số output có contract/skill nhưng cần thêm kiểm chứng bằng workbook thực.

Không khuyến nghị thêm cowork/subagent mới ngay. Package đã có agent ownership đủ rõ; nên ưu tiên fix traceability prompt registry/manifest và bổ sung validation thực tế trước khi mở rộng cowork.

## 2. Scope và phương pháp

Audit này đọc sâu theo nhóm tài liệu đại diện, không chỉ đọc tên file:

- `BIDV/Prompt/API/` và `BIDV/Prompt/UI/`: đọc prompt gốc API TD, API testcase, UI TD, UI testcase, UAT testcase.
- `BIDV/Prompt/API/Gen Script/`: đọc prompt phân tích testcase và sinh feature automation.
- `BIDV/api_automation/`: đọc README, client, endpoint catalog, test catalog để đánh giá execution readiness.
- `BIDV/Faker_upd/`, `BIDV/template/`, workbook testcase XLSX, workbook Paygates: kiểm kê và inspect workbook bằng Python read-only.
- `qc-agent-skills/`: đọc README, workflow pack, validators, artifact/review gates, prompt registry/manifest, skills, agents, output contracts, examples, tests.
- Chạy validator read-only/deterministic trên golden outputs và workflow pack.

Không đổi folder nguồn `BIDV/`. Không sửa runtime package trong audit ngoài việc tạo báo cáo này.

## 3. Inventory chi tiết BIDV/

### 3.1 Prompt gốc

| Prompt | Mục đích | Input/rule chính | Output kỳ vọng | Mirror runtime |
|---|---|---|---|---|
| `BIDV/Prompt/API/API_TD_1_Setup_Context.txt` | Thiết lập role và chiến lược API TD | Project/API scope, setup context; không sinh TD node ngay | Markmap API TD, 3 phase P1/P2/P3 | `prompts-verbatim/API/API_TD_1_Setup_Context.txt` |
| `BIDV/Prompt/API/API_TD_2_Method_Header.txt` | API TD Method/Header | Chỉ method, auth, content-type, custom headers; cấm body/business/DB | `TD_P1_*` | `prompts-verbatim/API/API_TD_2_Method_Header.txt` |
| `BIDV/Prompt/API/API_TD_3_Schema_Validation.txt` | API TD Schema Validation | Missing/empty/type/max/min nếu source có; cấm invent max length, cấm header/business | `TD_P2_*` | `prompts-verbatim/API/API_TD_3_Schema_Validation.txt` |
| `BIDV/Prompt/API/API_TD_4_Value_Business_Cross_Logic.txt` | API TD business/value/cross logic | BVA/ECP/EG/DT/ST; happy path verify DB; cấm retest schema/header | `TD_P3_*` | `prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic.txt` |
| `BIDV/Prompt/API/API_Gen_TC_From_TD_v2.txt` | API testcase từ TD | TD Markmap + API spec; không hallucinate; concrete data; happy path DB verify, negative no DB verify | TSV 19 cột | `prompts-verbatim/API/API_Gen_TC_From_TD_v2.txt` |
| `BIDV/Prompt/UI/UI_Gen_TD.txt` | UI Test Design | RSD/PTTK/UI docs; ECP/BVA/DT/ST/EG; ưu tiên vùng đỏ; cấm invent screen/field/message | UI TD Markmap | `prompts-verbatim/UI/UI_Gen_TD.txt` |
| `BIDV/Prompt/UI/UI_Gen_TC_From_TD.txt` | UI testcase từ TD | UI TD + UI source; quote all cells; UTF-8 BOM; one physical row/testcase | TSV 19 cột | `prompts-verbatim/UI/UI_Gen_TC_From_TD.txt` |
| `BIDV/Prompt/UI/UI_Gen_TC_For_UAT.txt` | UAT testcase | URD + RSD; business/user acceptance; cấm UI-only/technical validation khi URD không yêu cầu | TSV 16 cột prompt-style | `prompts-verbatim/UI/UI_Gen_TC_For_UAT.txt` |
| `BIDV/Prompt/API/Gen Script/API_TestCase_Analysis.txt` | Phân loại API testcase automation | TSV/XML testcase | Markdown table phân loại P1/P2/P3 | `prompts-verbatim/API/Gen Script/API_TestCase_Analysis.txt` |
| `BIDV/Prompt/API/Gen Script/API_Gen_Script_Validation_Feature.txt` | Sinh Gherkin schema validation | Chỉ TD_P2/schema; dùng example/properties | `.feature` support | `prompts-verbatim/API/Gen Script/API_Gen_Script_Validation_Feature.txt` |
| `BIDV/Prompt/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt` | Sinh Gherkin method/header | Chỉ TD_P1 | `.feature` support | `prompts-verbatim/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt` |
| `BIDV/Prompt/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt` | Sinh Gherkin logic/business | Chỉ TD_P3 | `.feature` support | `prompts-verbatim/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt` |

### 3.2 Source docs, templates, sample output

- `BIDV/Faker_upd/RSD/RSD_A`, `BIDV/Faker_upd/RSD/RSD_B`: RSD/URD/UI nghiệp vụ đại diện cho UI/UAT/API source.
- `BIDV/Faker_upd/PTTK/`: PTTK/API spec + sample testcase workbook.
- `BIDV/template/Template_PTTK_AI.doc`, `Template_PTTK_AI_ChiTiet_API.doc`, `Template_RSD_AI.doc`, `Template_RSD_ChiTiet_AI.doc`: template/reference input.
- Sample testcase workbook đã inspect:
  - `BIDV/Faker_upd/PTTK/1/NMS-[KH-660][CCTG Online] API check điều kiện KH-160526-040553-tcs.xlsx`
  - `BIDV/Faker_upd/PTTK/2/NMS-[KH-660][CCTG Online] API danh sách sản phẩm CCTG-160526-040713-tcs.xlsx`
  - Kết quả: workbook có cấu trúc legacy testcase 19 cột, nhiều sheet, testcase ID dạng `TD_P1_003_TC_003`, nhóm Method/Header, SIT, priority/regression/automation columns.
- Paygates dashboard workbook:
  - `BIDV/Tổng hợp Trạng Thái Test Case Paygates (1).xlsx`
  - Sheet chính: `Tổng hợp chung`, `Squad_Tester`, `Squad_Base`, `Tổng Hợp Test Case Theo Sprint`, `Tổng Hợp Test Case Automation T`, nhiều squad sheet, `Sprint 8`.
  - Có metrics Pass/Fail/Untested/Accepted/N/A/Total, generate type, automation status, links.

### 3.3 API automation framework

- `BIDV/api_automation/README.md`: NMS SDK scaffold, header builder, RequestID generator, response envelope assertions, endpoint catalog 15 APIs, schema validators, smoke skeleton.
- `BIDV/api_automation/nms_sdk/client.py`: `ApiConfig`, `ApiRequest`, `ApiClient.build_url()`, `ApiClient.build_request()`. Hiện chỉ build request, chưa tự gửi network call.
- `BIDV/api_automation/nms_sdk/endpoints.py`: `EndpointSpec`, 15 endpoint như `/accounts/list`, `/bidyield/list`, `/v1/buy/order`, `/trans/payment`, `/buy/check-customer`, `/v1/sell/order`, `/v1/contract/file`.
- `BIDV/api_automation/tests/test_endpoint_catalog.py`: test endpoint catalog/schema/smoke skeleton.

Đánh giá: có scaffold automation và nguồn enrichment tốt, nhưng chưa chứng minh sinh `.feature` từ `qc-agent-skills` chạy thật với framework này.

## 4. Inventory capability qc-agent-skills/ sau rename

### 4.1 Runtime/routing/gates

- `qc-agent-skills/README.md`: xác nhận chỉ hỗ trợ BIDV Prompt-Compatible Orchestration Mode; final outputs gồm API/UI TD, testcase 19 cột, UAT 16 cột, `.feature`, execution TSV, Paygates dashboard, coverage/gap.
- `qc-agent-skills/workflow-packs/default/workflow.yml`: có route cho API TD/testcase, UI TD/testcase, UAT, API automation, manual execution, dashboard, coverage audit.
- `qc-agent-skills/workflow-packs/default/validators.yml`: map validators cho source manifest, normalized knowledge, redaction, API/UI TD, legacy 19-col, UAT 16-col, execution, dashboard, tracker, artifact manifest.
- `qc-agent-skills/workflow-packs/default/artifact-policy.yml`: lifecycle `draft -> reviewed -> approved`, artifact root `artifacts/default`.
- `qc-agent-skills/workflow-packs/default/review-gates.yml`: output reviewer không được là generator, supervisor approve only if validators/review/source trace/no secrets/manifest pass.

### 4.2 Prompt mirrors

- Manifest hiện tại: `qc-agent-skills/data/source-inventory/prompt_mirror_manifest.json`, 12 prompt entries.
- Scripts:
  - `qc-agent-skills/scripts/sync_prompts.py`
  - `qc-agent-skills/scripts/verify_prompt_mirrors.py`
- Verification pass: `BIDV prompt mirror verification passed (12 prompts)`.

Điểm cần chú ý: `prompt_fragment_registry.md` dòng API TD P1/P2/P3 đang trỏ tới source/runtime prompt `*_BreakDown.txt`, trong khi manifest hiện tại mirror 3 prompt gốc không hậu tố `_BreakDown`. `workflow-packs/default/prompts/API/*_BreakDown.txt` tồn tại, nhưng chưa thấy chúng nằm trong `prompts-verbatim/` và manifest verifier. Đây là gap traceability/registry consistency.

### 4.3 Skill/agent ownership

| Output/capability | Skill owner | Agent owner | Evidence |
|---|---|---|---|
| API TD | `skills/api-td-generate/SKILL.md` | `agents/api-test-design-agent/AGENT.md` | prompt mapping + API operation cards rule |
| API/UI testcase 19 cột | `skills/tc-generate-from-td/SKILL.md` | `agents/testcase-generator/AGENT.md` | TD-derived IDs + legacy export rule |
| UI TD | `skills/ui-td-generate/SKILL.md` | `agents/ui-test-design-agent/AGENT.md` | UI prompt mapping |
| UAT 16 cột | `skills/uat-tc-generate/SKILL.md` | UAT skill owner / orchestrator | UAT prompt mapping + 16-column export |
| API automation support | `skills/api-automation-support-generate/SKILL.md` | `agents/automation-support-agent/AGENT.md` | analysis -> phase-specific prompts |
| Manual execution import | `skills/manual-execution-reader/SKILL.md` | orchestrator/sdk runner | contract/tool-driven |
| Paygates dashboard | `skills/paygates-dashboard-generate/SKILL.md` | orchestrator/sdk runner | dashboard contract + exporter/validator |
| XRAY workflow | `skills/xray-test-workflow/SKILL.md` | `agents/delivery-orchestrator/AGENT.md` | separation + routing + gates |
| Coverage audit | `skills/coverage-audit/SKILL.md` | `agents/coverage-auditor/AGENT.md` | traceability/gap matrix |
| Output review | `skills/output-verify/SKILL.md` | `agents/output-reviewer/AGENT.md` | hard-fail rules |
| Contract validation | `skills/testcase-validator/SKILL.md` | `agents/contract-validator/AGENT.md` | deterministic validators |
| Supervisor approval | `skills/supervisor-loop/SKILL.md` | `agents/supervisor/AGENT.md` | final approval gate |

Không thấy self-approval: reviewer/supervisor tách khỏi generator, workflow gates bắt buộc review trước supervisor trước publish.

### 4.4 Contracts/exporters/validators/examples/tests

Contracts đọc/đối chiếu:

- `legacy_19_column_testcase_contract.md`: 19 cột, alias `Test Data/Test Datas`, API/UI ID policy.
- `uat_16_column_testcase_contract.md`: 16 cột UAT business-facing.
- `manual_execution_reader_contract.md`: normalize status từ workbook legacy sang TestExecution TSV.
- `paygates_dashboard_contract.md`: dashboard/status columns, count reconciliation.
- `excel_output_similarity.md`: similarity với VA-style testcase workbook và Paygates workbook.
- `xray_field_mapping.md`: Requirement/Test Plan/Test Design/Test Case/Test Set/Test Execution/Coverage mapping.
- `markdown_normalization_rules.md`, `testcase_excel_columns.md`, `test_status_excel_columns.md`: có mặt trong package.

Scripts hiện có gồm exporter/validator cho legacy TSV/XLSX, Paygates TSV/XLSX/sync, manual execution reader, output contract, API specificity, testcase granularity/coverage, workflow pack, prompt mirror, source manifest, closed loop.

Examples/tests hiện có:

- Golden outputs: API/UI TD, testcase compatible TSV, legacy 19-col TSV/XLSX, Paygates dashboard TSV/XLSX, TestExecution TSV.
- Full XRAY chain: RequirementInventory, TestSet, CoverageMatrix, TestCase, TestExecution, legacy/paygates generated outputs.
- E2E API/UI-UAT examples with OutputReview/SupervisorApproval.
- Tests include API e2e, UI/UAT e2e, workflow closed loop, validators, status enums, canonical sources, universal router, supervisor loop, xlsx profiles.

## 5. Coverage matrix

| Output / workflow | Source trong BIDV | Capability trong qc-agent-skills | Evidence | Score | Gap |
|---|---|---|---|---:|---|
| API TD - setup/context | `BIDV/Prompt/API/API_TD_1_Setup_Context.txt` | Mirror + `api-td-generate` + workflow route + API TD validator | `prompt_mirror_manifest.json`, `skills/api-td-generate/SKILL.md`, `workflow.yml`, validator pass | 2 | Không |
| API TD - method/header | `API_TD_2_Method_Header.txt` | Mirror + workflow stage + skill | `prompts-verbatim/API/API_TD_2_Method_Header.txt`, `workflow.yml` | 1 | Registry/workflow có `*_BreakDown` variant chưa nằm trong manifest mirror |
| API TD - schema validation | `API_TD_3_Schema_Validation.txt` | Mirror + workflow stage + specificity validator | `validate_api_td_specificity.py`, `workflow.yml` | 1 | Cùng gap `*_BreakDown` traceability |
| API TD - business/cross logic | `API_TD_4_Value_Business_Cross_Logic.txt` | Mirror + workflow stage + review rules | `api-td-generate`, `output-verify` | 1 | Cùng gap `*_BreakDown` traceability |
| API testcase 19-column | `API_Gen_TC_From_TD_v2.txt`, sample XLSX | TC skill + legacy 19-col contract/export/validate + golden example | `tc-generate-from-td`, `legacy_19_column_testcase_contract.md`, validator pass | 2 | Cần thêm sample comparison tự động với workbook thật |
| UI Test Design | `UI_Gen_TD.txt` | UI TD skill + validator + golden output | `ui-td-generate`, `validate_test_design.py --type ui`, `ui-test-design.md` | 2 | Không lớn |
| UI testcase from TD | `UI_Gen_TC_From_TD.txt` | TC skill + legacy export/validator | `tc-generate-from-td`, legacy contract | 2 | Cần thêm e2e validation bằng UI source thực |
| UAT testcase 16-column | `UI_Gen_TC_For_UAT.txt` | UAT skill + 16-col contract + route | `uat-tc-generate`, `uat_16_column_testcase_contract.md` | 2 | Prompt gốc header khác contract package; cần xác nhận deliberate mapping |
| API automation feature/script | `Prompt/API/Gen Script/*.txt`, `api_automation/` | Automation support skill/route/examples | `api-automation-support-generate`, `BIDV/api_automation` scaffold | 1 | Chưa chứng minh generated feature chạy với framework thật |
| Paygates dashboard/status | Root Paygates workbook | Dashboard contract/export/sync/validator | `paygates_dashboard_contract.md`, validator pass, golden TSV/XLSX | 2 | Cần comparison tự động với workbook thật để tăng confidence |
| Manual execution import | Legacy executed workbook/result columns | Reader + execution TSV contract + script | `manual-execution-reader`, `read_manual_execution_results.py`, output validator pass | 2 | Cần thêm fixture workbook thực có kết quả manual |
| XRAY/TestSet/TestExecution | Output contracts/examples | XRAY workflow + mapping + full-xray-chain examples | `xray-test-workflow`, `xray_field_mapping.md`, examples/full-xray-chain | 2 | Không ghi trực tiếp Xray/Jira nếu chưa có approval; đúng policy |
| Coverage/gap audit | RSD/PTTK/source docs | Coverage auditor + matrix outputs | `coverage-audit`, `coverage-auditor`, CoverageMatrix example | 2 | Cần chạy trên target source thực |
| Review/supervisor/publish lifecycle | All deliverables | Reviewer + validator + supervisor + artifact policy | `review-gates.yml`, `artifact-policy.yml`, tests workflow closed loop | 2 | Pytest chưa chạy do thiếu dependency môi trường |

Tổng: **25 / 28 = 89.3%**.

## 6. Sub-ratios readiness

| Nhóm | Đánh giá | Tỉ lệ |
|---|---|---:|
| Prompt mirror coverage | 12/12 prompt manifest hiện tại pass, nhưng registry có 3 `*_BreakDown` chưa được mirror/verify trong manifest | 85% |
| Output contract coverage | Legacy 19-col, UAT 16-col, execution, Paygates, XRAY, markdown, similarity đều có contract | 95% |
| Validator/exporter coverage | Core validators/exporters tồn tại và golden commands pass | 90% |
| Golden example/test coverage | Golden outputs + e2e examples + tests có mặt; pytest thiếu dependency nên chưa chạy suite | 80% |
| Workflow route coverage | Routes chính có trong workflow pack; workflow pack validator pass | 95% |
| Agent/skill ownership coverage | Owner rõ cho generator, validator, reviewer, supervisor, coverage | 95% |
| API automation execution readiness | Prompt support + scaffold, nhưng chưa chạy feature thực với framework/network | 55% |
| Post-rename wiring health | Workflow validator pass, không còn path `*bidv*`, không còn reference path cũ | 95% |

## 7. Gap analysis

### P0 - Blocker

Không thấy P0 đang active sau rename đối với golden workflow chính:

- Prompt mirror verifier pass 12 prompts.
- Core output validators pass.
- Workflow pack validator pass.
- Scan không còn path/reference cũ: `automation-test-agent-skills`, `workflow-packs/bidv-default`, `data/bidv-output-contracts`, `knowledge/bidv`, `artifacts/bidv`.

P0 tiềm ẩn cần xử lý trước release nếu runtime thật chọn `*_BreakDown`:

- `prompt_fragment_registry.md` và `workflow.yml` có API TD `*_BreakDown` prompts; manifest hiện tại chỉ verify non-BreakDown prompt mirrors. Nếu runtime bắt buộc dùng BreakDown, cần đưa BreakDown vào `prompts-verbatim/` + manifest hoặc đổi registry/workflow về prompt đã mirror.

### P1 - Important

1. API automation support chưa chứng minh generated `.feature` chạy được với `BIDV/api_automation/`; framework hiện chỉ build request, chưa gửi network call.
2. UAT 16-column contract package khác header prompt gốc UAT đã đọc. Cần quyết định contract nào là canonical hoặc thêm alias/export mapping rõ.
3. Manual execution reader và Paygates dashboard đã có contract/validator nhưng cần fixture workbook thực có execution result để prove import/sync end-to-end.
4. Test suite không chạy trong môi trường hiện tại vì `pytest` chưa cài, nên chưa có bằng chứng full regression pass.
5. Coverage audit capability có skill/agent/example nhưng chưa chạy trên toàn bộ target source docs thật.

### P2 - Nice-to-have

1. Thêm comparison report tự động giữa generated XLSX và workbook BIDV sample.
2. Bổ sung diagram flow tổng quan runtime mode sau rename.
3. Bổ sung benchmark Excel similarity/profile cho nhiều workbook hơn.
4. Dọn/hygiene generated artifacts theo lịch hoặc policy rõ hơn.

## 8. Post-rename wiring health

Kết quả kiểm tra sau rename tốt:

- `python qc-agent-skills/scripts/validate_workflow_pack.py qc-agent-skills/workflow-packs/default` → success.
- Scan stale references không thấy:
  - `automation-test-agent-skills`
  - `workflow-packs/bidv-default`
  - `data/bidv-output-contracts`
  - `knowledge/bidv`
  - `artifacts/bidv`
- `Glob **/*bidv*` trong `qc-agent-skills/` không còn match.
- Artifact lifecycle đã dùng `artifacts/default`.
- Workflow/tests đã dùng `workflow-packs/default`.

Rename không làm gãy agent skills ở mức route/validator/golden output hiện tại. Ảnh hưởng còn lại chủ yếu là prose/domain vẫn dùng chữ `BIDV` như domain/source behavior, điều này là đúng và nên giữ.

## 9. Cowork/subagent recommendation

Chưa nên thêm cowork/subagent mới như một capability riêng. Lý do:

- Package đã có role separation đầy đủ: orchestrator, generator, validator, output reviewer, supervisor, coverage auditor.
- Review gates đã cấm self-approval.
- Thêm cowork lúc này dễ tăng phức tạp mà chưa giải quyết gap chính.

Nên cải thiện playbook/team hiện có thay vì thêm role mới:

1. `api_delivery_team`: thêm bước kiểm BreakDown prompt manifest trước generation.
2. `output_review_team`: bắt buộc check prompt registry vs mirror manifest.
3. `automation-support-agent`: thêm checklist map generated feature với `BIDV/api_automation` conventions.

## 10. Recommended next actions

Ưu tiên theo thứ tự:

1. Fix traceability prompt registry/manifest cho API TD P1/P2/P3:
   - Hoặc mirror `*_BreakDown.txt` vào `prompts-verbatim/` và thêm vào `prompt_mirror_manifest.json`/`sync_prompts.py`.
   - Hoặc đổi registry/workflow về 3 prompt gốc đã mirror nếu BreakDown không phải runtime canonical.
2. Chuẩn hóa UAT 16-column mapping giữa prompt gốc và package contract; nếu chấp nhận khác biệt thì document alias/export mapping.
3. Cài hoặc vendor dependency test tối thiểu để chạy `python -m pytest qc-agent-skills/tests` trong CI/local.
4. Thêm fixture workbook thực cho manual execution reader và Paygates dashboard sync.
5. Tạo automation e2e spike: từ API testcase → analysis → `.feature` → map/validate với `BIDV/api_automation` scaffold.
6. Chạy coverage audit trên một bộ source thực trong `BIDV/Faker_upd/` để chứng minh gap matrix không chỉ là example.

## 11. Verification commands đã chạy

| Command | Result |
|---|---|
| `python qc-agent-skills/scripts/verify_prompt_mirrors.py` | PASS: `BIDV prompt mirror verification passed (12 prompts)` |
| `python qc-agent-skills/scripts/validate_legacy_19col_tsv.py qc-agent-skills/examples/golden-outputs/testcase-legacy-19col.tsv` | PASS |
| `python qc-agent-skills/scripts/validate_paygates_dashboard.py qc-agent-skills/examples/golden-outputs/paygates-dashboard-compatible.tsv` | PASS |
| `python qc-agent-skills/scripts/validate_output_contract.py --testcase qc-agent-skills/examples/golden-outputs/testcase-compatible.tsv --execution qc-agent-skills/examples/golden-outputs/test-execution-compatible.tsv` | PASS |
| `python qc-agent-skills/scripts/validate_workflow_pack.py qc-agent-skills/workflow-packs/default` | PASS |
| `python -m pytest qc-agent-skills/tests` | NOT RUN: environment missing `pytest` module |
| scan stale path references | PASS: no files found |
| `Glob qc-agent-skills/**/*bidv*` | PASS: no matches |

## 12. Appendix - representative files đã đọc

### BIDV

- `BIDV/Prompt/API/API_TD_1_Setup_Context.txt`
- `BIDV/Prompt/API/API_TD_2_Method_Header.txt`
- `BIDV/Prompt/API/API_TD_3_Schema_Validation.txt`
- `BIDV/Prompt/API/API_TD_4_Value_Business_Cross_Logic.txt`
- `BIDV/Prompt/API/API_Gen_TC_From_TD_v2.txt`
- `BIDV/Prompt/UI/UI_Gen_TD.txt`
- `BIDV/Prompt/UI/UI_Gen_TC_From_TD.txt`
- `BIDV/Prompt/UI/UI_Gen_TC_For_UAT.txt`
- `BIDV/Prompt/API/Gen Script/API_TestCase_Analysis.txt`
- `BIDV/Prompt/API/Gen Script/API_Gen_Script_Validation_Feature.txt`
- `BIDV/api_automation/README.md`
- `BIDV/api_automation/nms_sdk/client.py`
- `BIDV/api_automation/nms_sdk/endpoints.py`
- `BIDV/api_automation/tests/test_endpoint_catalog.py`
- `BIDV/Faker_upd/PTTK/1/...-tcs.xlsx` inspected read-only
- `BIDV/Faker_upd/PTTK/2/...-tcs.xlsx` inspected read-only
- `BIDV/Tổng hợp Trạng Thái Test Case Paygates (1).xlsx` inspected read-only
- `BIDV/template/*` inventory

### qc-agent-skills

- `qc-agent-skills/README.md`
- `qc-agent-skills/data/source-inventory/prompt_mirror_manifest.json`
- `qc-agent-skills/data/source-inventory/prompt_fragment_registry.md`
- `qc-agent-skills/data/source-inventory/workflow_map.md`
- `qc-agent-skills/scripts/sync_prompts.py`
- `qc-agent-skills/scripts/verify_prompt_mirrors.py`
- `qc-agent-skills/workflow-packs/default/workflow.yml`
- `qc-agent-skills/workflow-packs/default/validators.yml`
- `qc-agent-skills/workflow-packs/default/artifact-policy.yml`
- `qc-agent-skills/workflow-packs/default/review-gates.yml`
- `qc-agent-skills/skills/api-td-generate/SKILL.md`
- `qc-agent-skills/skills/tc-generate-from-td/SKILL.md`
- `qc-agent-skills/skills/ui-td-generate/SKILL.md`
- `qc-agent-skills/skills/uat-tc-generate/SKILL.md`
- `qc-agent-skills/skills/api-automation-support-generate/SKILL.md`
- `qc-agent-skills/skills/manual-execution-reader/SKILL.md`
- `qc-agent-skills/skills/paygates-dashboard-generate/SKILL.md`
- `qc-agent-skills/skills/xray-test-workflow/SKILL.md`
- `qc-agent-skills/skills/coverage-audit/SKILL.md`
- `qc-agent-skills/skills/output-verify/SKILL.md`
- `qc-agent-skills/skills/testcase-validator/SKILL.md`
- `qc-agent-skills/agents/delivery-orchestrator/AGENT.md`
- `qc-agent-skills/agents/coverage-auditor/AGENT.md`
- `qc-agent-skills/agents/contract-validator/AGENT.md`
- `qc-agent-skills/agents/output-reviewer/AGENT.md`
- `qc-agent-skills/agents/supervisor/AGENT.md`
- `qc-agent-skills/data/output-contracts/legacy_19_column_testcase_contract.md`
- `qc-agent-skills/data/output-contracts/uat_16_column_testcase_contract.md`
- `qc-agent-skills/data/output-contracts/manual_execution_reader_contract.md`
- `qc-agent-skills/data/output-contracts/paygates_dashboard_contract.md`
- `qc-agent-skills/data/output-contracts/excel_output_similarity.md`
- `qc-agent-skills/data/output-contracts/xray_field_mapping.md`
- `qc-agent-skills/tests/test_e2e_api_workflow.py`
- `qc-agent-skills/tests/test_workflow_pack_closed_loop.py`
