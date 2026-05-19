# Workflow Map

This map captures the workflow learned from the BIDV end-to-end sample folder. It is used by the orchestrator together with `prompt_fragment_registry.md`.

## root assets

| Root item | Workflow role |
|---|---|
| `BIDV/Prompt/` | Source prompt engine: API TD, API testcase, UI TD, UI testcase, UAT testcase, API automation support |
| `BIDV/UI/` | UI/design/source input for UI TD and UI testcase flows |
| `BIDV/template/` | Format/reference input for BIDV document/output style |
| `BIDV/NMS-Đặc tả API cho SDK-170326-075931.pdf` | API/spec input sample |
| `BIDV/VA_19.004 - Xem chi tiết yêu cầu Thêm mới KSV.xlsx` | Detailed testcase output baseline |
| `BIDV/Tổng hợp Trạng Thái Test Case Paygates (1).xlsx` | Dashboard/status output baseline |

## End-to-end workflow

```text
Business/API/UI source docs
+ project/squad/epic planning metadata
+ workflow-pack prompt mirrors and contracts
-> Test Plan
-> Operation Inventory / Rule Matrix Seeds
-> Test Design
+ workflow-pack testcase prompt mirrors and contracts
-> Testcase detail workbook/TSV
+ Coverage Matrix / GAP traceability
+ execution status
-> Test Execution/status data
+ squad/sprint/epic metadata
-> Paygates-style dashboard/status workbook
```

## Step map

| Step | When to use | Required input | Source prompt/workflow | Owning skill | Expected output | Similarity baseline |
|---|---|---|---|---|---|---|
| Test Plan | User requests a project/squad/epic test plan or a delivery route needs planning before TD/TC/execution | Project/Squad/Epic, source baseline, requirement baseline, environment, build/release | Internal test plan contract | `test-plan-generate` | `TestPlan.md` + review/approval | `test_plan_contract.md`; validated source baseline, deliverables, coverage strategy, and open questions |
| API spec extraction / operation inventory | User requests API TD/testcase from API spec or source docs | API PDF/source docs, optional normalized SDK enrichment references | Internal extraction contract before API TD prompts | `api-td-generate` / `delivery-orchestrator` | API Requirement Inventory / Operation Cards / Rule Matrix Seeds | Source fidelity and API specificity baseline |
| API TD setup/context | User requests API TD or API testcase and only API source/spec is available | Project/Squad/Epic, API spec, API scope | `BIDV/Prompt/API/API_TD_1_Setup_Context.txt` | `api-td-generate` | API TD context Markdown | API TD prompt output style |
| API TD method/header | API TD needs protocol/header/auth coverage | API context, endpoint, method, headers/auth | `BIDV/Prompt/API/API_TD_2_Method_Header.txt` | `api-td-generate` | `TD_P1_*` Method/Header conditions | API TD prompt output style |
| API TD schema validation | API TD needs request schema coverage | Request body/params/schema/constraints | `BIDV/Prompt/API/API_TD_3_Schema_Validation.txt` | `api-td-generate` | `TD_P2_*` Schema Validation conditions | API TD prompt output style |
| API TD value/business/cross logic | API TD needs business/data/rule coverage | Business rules, value ranges, state/cross-field dependencies | `BIDV/Prompt/API/API_TD_4_Value_Business_Cross_Logic.txt` | `api-td-generate` | `TD_P3_*` business/value/cross logic conditions | API TD prompt output style |
| API testcase from TD | User has API TD and wants manual testcase | API TD, API spec, endpoint/header/schema/error/DB data | `BIDV/Prompt/API/API_Gen_TC_From_TD_v2.txt` | `tc-generate-from-td` | Markdown testcase source + legacy 19-column TSV | `BIDV/VA_19.004 - Xem chi tiết yêu cầu Thêm mới KSV.xlsx` detail table shape |
| UI Test Design | User requests UI TD from UI/design/RSD/PTTK | UI docs, screen/field/button/message/business rules | `BIDV/Prompt/UI/UI_Gen_TD.txt` | `ui-td-generate` | UI TD Markdown/Markmap-style design | UI prompt output style |
| UI testcase from TD | User has UI TD and wants manual testcase | UI TD, UI docs, navigation, fields, messages, role/data | `BIDV/Prompt/UI/UI_Gen_TC_From_TD.txt` | `tc-generate-from-td` | Markdown testcase source + legacy 19-column TSV | `BIDV/VA_19.004 - Xem chi tiết yêu cầu Thêm mới KSV.xlsx` detail table shape |
| UAT testcase | User requests business-facing UAT cases | URD/business flow/actor/acceptance criteria | `BIDV/Prompt/UI/UI_Gen_TC_For_UAT.txt` | `uat-tc-generate` | Markdown UAT testcase source + UAT 16-column TSV | UAT prompt contract |
| API testcase analysis | User requests automation analysis from API testcase | API testcase source and automation scope | `BIDV/Prompt/API/Gen Script/API_TestCase_Analysis.txt` | `api-automation-support-generate` | Automation testcase analysis Markdown | API automation prompt output style |
| API automation script support | User requests feature/spec/script support | Testcase analysis, method/header/schema/business testcase subset, framework context | `BIDV/Prompt/API/Gen Script/API_Gen_Script_*.txt` | `api-automation-support-generate` | Automation support artifact | API automation prompt output style |
| Test execution/status | User has testcase and needs execution pack/status update | Testcase source, tester/build/environment/status | BIDV Excel execution workflow | `test-execution-pack-generate` | TestExecution Markdown + execution TSV | VA workbook summary/result columns |
| Manual execution reader/import | User has executed VA-style testcase workbook or legacy result table and needs normalized execution status | Executed legacy workbook/TSV/CSV, selected manual result round, execution metadata | Internal manual execution reader contract | `manual-execution-reader` | TestExecution TSV from manual result columns | `manual_execution_reader_contract.md`; `test_status_excel_columns.md` |
| Dashboard/status summary | User has testcase/execution/squad/sprint status, or needs a new Paygates-style dashboard without an external workbook | Testcase source, optional execution source, squad/sprint/epic/function metadata, testcase links | Internal Paygates dashboard contract | `paygates-dashboard-generate` | PaygatesDashboard Markdown + TSV + optional XLSX | `paygates_dashboard_contract.md`; historical `BIDV/Tổng hợp Trạng Thái Test Case Paygates (1).xlsx` only as optional parity reference |
| Legacy 19-column XLSX export | User has legacy testcase Markdown/TSV and needs a VA-style XLSX for manual execution | Legacy testcase Markdown or legacy 19-column TSV, output XLSX path | Internal legacy 19-column contract | `legacy-xlsx-exporter` | Legacy testcase XLSX | `legacy_19_column_testcase_contract.md`; `excel_output_similarity.md` |
| Paygates dashboard sync | User has validated Paygates dashboard TSV and needs XLSX workbook output or safe source workbook copy | Paygates dashboard TSV, explicit output XLSX path, optional source workbook | Internal Paygates dashboard contract | `paygates-dashboard-sync` | Paygates dashboard XLSX | `paygates_dashboard_contract.md` |

## Execution mode metadata

| Step | Recommended execution mode | Runtime owning role |
|---|---|---|
| Test Plan | single-agent or sdk-runner | test plan skill owner |
| API TD setup/context | single-agent or full-delivery-team | `api-test-design-agent` |
| API TD method/header | single-agent or full-delivery-team | `api-test-design-agent` |
| API TD schema validation | single-agent or full-delivery-team | `api-test-design-agent` |
| API TD value/business/cross logic | single-agent or full-delivery-team | `api-test-design-agent` |
| API testcase from TD | single-agent or full-delivery-team | `testcase-generator` |
| UI Test Design | single-agent | UI TD skill owner |
| UI testcase from TD | single-agent | `testcase-generator` |
| UAT testcase | single-agent | UAT testcase skill owner |
| API testcase analysis | single-agent or full-delivery-team | automation support skill owner |
| API automation script support | full-delivery-team when generated with TD/TC chain | automation support skill owner |
| Test execution/status | single-agent or sdk-runner | execution pack skill owner |
| Manual execution reader/import | single-agent or sdk-runner | `manual-execution-reader` |
| Dashboard/status summary | single-agent or sdk-runner | `paygates-dashboard-generate` |
| Legacy 19-column XLSX export | single-agent or sdk-runner | `legacy-xlsx-exporter` |
| Paygates dashboard sync | single-agent or sdk-runner | `paygates-dashboard-sync` |
| Output review | review-team | `output-reviewer` |

Use `playbooks/agent-teams/api_delivery_team.md` for full delivery and `playbooks/agent-teams/output_review_team.md` for parallel review. Use SDK runners when repeatable/headless execution and deterministic validators are required.

## API enrichment sources

For NMS API work, raw `BIDV/api_automation/...` files are bootstrap/migration references only and must not be read by runtime routes. Any SDK-derived endpoint, schema, required-field, business-error, or assertion knowledge needed at runtime must first be normalized into workflow-pack prompts, contracts, templates, golden examples, or approved knowledge artifacts with a stable source id. Normalized enrichment may fill known required fields, business errors, and schema assertions when traceable, but it must not silently override contradictory current-run source evidence.

## Matrix traceability flow

TD/TC routes should carry matrix traceability as a support artifact:

```text
Runtime source docs + normalized workflow knowledge
-> Operation Inventory
-> Rule Matrix Seeds
-> API/UI TD prompts
-> Testcase generation
-> Coverage Matrix / GAP report
```

Matrix rows must use source manifest ids, normalized knowledge ids, workflow-pack contract ids, prompt contract ids, or current run sections/pages/sheets as `source_ref`. Coverage audit routes should promote `CoverageMatrix.md` to a final output.

## Orchestrator rule

The orchestrator must select workflow step by considering both:

1. The output the user wants.
2. The upstream artifact/input currently available.

Examples:

- If user asks for testcase and only API spec exists, route first through API TD prompts, then API testcase prompt.
- If user asks for testcase and Test Design already exists, route directly to API/UI testcase prompt based on TD type.
- If user asks for dashboard/status, require testcase/execution metadata and use Paygates-style similarity checks.
- If mandatory input for the selected step is missing, ask or record open questions; do not replace it with native/freeform generation.
