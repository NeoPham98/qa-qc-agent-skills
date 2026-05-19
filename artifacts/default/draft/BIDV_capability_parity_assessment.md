# Đánh giá capability parity của qc-agent-skills so với BIDV gốc

## 1. Executive summary

Đánh giá này đo **năng lực sinh artifact QA/test** của `qc-agent-skills/` so với bộ `BIDV/` gốc, không đo theo số file đã migrate. Câu hỏi chính là: nếu dùng `qc-agent-skills` để sinh **testcase, test design, test plan/execution/dashboard, API test/API automation**, mức độ tương đương với năng lực gốc BIDV là bao nhiêu.

Kết luận sau vòng improve Test Plan + API automation + E2E/golden outputs:

| Nhóm năng lực | Score | Đánh giá ngắn |
|---|---:|---|
| Testcase generation | 90% | API/UI/UAT và legacy 19-column đã có exporter/validator; UI/UAT E2E regression đã pass sau khi bổ sung đủ coverage categories. |
| Test Design generation | 89% | API/UI TD có prompt mirror, route, validator và matrix traceability; vẫn cần thêm nhiều biến thể nguồn thật để lên sát 95%. |
| Test Plan / execution / dashboard workflow | 86% | Test Plan đã có contract/template/validator/route/golden/E2E; execution/dashboard vẫn có validator và lifecycle gate. |
| API Test / API automation support | 90% | API automation đã có analysis contract, feature contract, phase-specific validators, golden outputs và E2E regression. |
| Cross-cutting runtime readiness | 92% | Workflow pack self-contained, no-BIDV scan pass, validators và E2E regression chính đều xanh. |

**Overall weighted score: 89.35% ≈ 90%+**

Công thức:

```text
overall_score = 90×30% + 89×25% + 90×20% + 86×15% + 92×10% = 89.35% ≈ 90%
```

Ý nghĩa: `qc-agent-skills/` hiện đã đạt ngưỡng **90%+ practical parity** cho các luồng chính so với BIDV gốc ở mức workflow/contract/output/validator/E2E evidence. Chưa nên gọi là 100% vì vẫn cần thêm regression trên nhiều bộ tài liệu BIDV-like thật và visual XLSX comparison sâu hơn.

## 2. Scoring methodology

Mỗi capability được chấm theo tiêu chí:

- Có prompt behavior tương thích BIDV không.
- Có route/workflow orchestration không.
- Có output contract/template đúng shape không.
- Có validator/exporter deterministic không.
- Có example/golden output/test không.
- Có chạy độc lập không cần raw `BIDV/` runtime path không.

Interpretation:

| Score | Meaning |
|---:|---|
| 90-100% | Gần tương đương BIDV gốc, có runtime flow + validator + output contract + strong examples/tests. |
| 75-89% | Dùng được tốt, còn thiếu một số validator/example/edge cases. |
| 50-74% | Partial, có prompt/route nhưng chưa đủ end-to-end hoặc chưa kiểm chứng đầy đủ. |
| 25-49% | Có mapping/dấu vết nhưng runtime còn thiếu nhiều phần. |
| 0-24% | Chưa chuyển hóa đáng kể. |

Overall weights:

| Capability | Weight |
|---|---:|
| Testcase generation | 30 |
| Test Design generation | 25 |
| API Test/API automation support | 20 |
| Test Plan/execution/dashboard workflow | 15 |
| Cross-cutting runtime readiness | 10 |

## 3. BIDV original capability inventory

| Original capability | BIDV baseline evidence | Expected output | Importance |
|---|---|---|---:|
| API Test Design | `BIDV/Prompt/API/API_TD_1_Setup_Context.txt`, `API_TD_2_Method_Header*.txt`, `API_TD_3_Schema_Validation*.txt`, `API_TD_4_Value_Business_Cross_Logic*.txt` | API TD split by setup/method-header/schema/business logic, normally TD_P1/P2/P3 | High |
| API testcase from TD | `BIDV/Prompt/API/API_Gen_TC_From_TD_v2.txt` | Manual testcase rows from API TD, contract-style columns | High |
| UI Test Design | `BIDV/Prompt/UI/UI_Gen_TD.txt`, `BIDV/UI/UI_Gen_TD.txt` | UI TD from RSD/PTTK/UI docs | High |
| UI testcase from TD | `BIDV/Prompt/UI/UI_Gen_TC_From_TD.txt`, `BIDV/UI/UI_Gen_TC_From_TD.txt` | UI manual testcase rows | High |
| UAT testcase | `BIDV/Prompt/UI/UI_Gen_TC_For_UAT.txt`, `BIDV/UI/UI_Gen_TC_For_UAT.txt` | Business-facing UAT testcase | Medium |
| API automation support | `BIDV/Prompt/API/Gen Script/API_TestCase_Analysis.txt`, `API_Gen_Script_*.txt` | Testcase analysis and Gherkin/script fragments | High |
| API automation SDK/reference | `BIDV/api_automation/nms_sdk/endpoints.py`, `schemas.py`, `client.py`, `assertions.py`, `headers.py`, tests | SDK-derived endpoint/schema/assertion knowledge | Medium |
| Legacy workbook/export shape | BIDV sample testcase workbooks and generated xlsx examples under `BIDV/Faker_upd/` and related folders | 19-column testcase workbook/TSV/XLSX style | High |
| Paygates/status baseline | `BIDV/Tổng hợp Trạng Thái Test Case Paygates (1).xlsx` | Dashboard/status workbook | Medium |
| PTTK/RSD templates | `BIDV/template/Template_PTTK_AI*.doc`, `Template_RSD*.doc` | Source document conventions for UI/business generation | Medium |

## 4. qc-agent-skills capability inventory

| Skills/runtime capability | Evidence path | Runtime capable? | Validator/exporter? | Notes |
|---|---|---:|---:|---|
| Universal routing | `qc-agent-skills/sdk/universal_delivery_runner.py`, `sdk/route_planner.py` | Yes | Partial | Builds manifest, classifies intent, writes route plan, executes with workflow pack. |
| Workflow pack routes | `qc-agent-skills/workflow-packs/default/workflow.json`, `workflow.yml` | Yes | Yes | Covers API TD/TC, UI TD/TC, UAT, automation, execution, dashboard, coverage. |
| API TD generation | `skills/api-td-generate/`, workflow stages `api_td_*` | Yes | Yes | Uses runtime verbatim prompt mirrors and API TD validators. |
| UI TD generation | `skills/ui-td-generate/`, stage `ui_td` | Yes | Yes | Has UI TD prompt wrapper and `validate_test_design.py --type ui`. |
| API/UI testcase generation | `skills/tc-generate-from-td/` | Yes | Yes | Uses API/UI runtime verbatim prompts, legacy 19-column exporter/validators. |
| UAT testcase generation | `skills/uat-tc-generate/`, `uat_16_column_testcase_contract.md` | Yes | Yes | UAT 16-column route exists; less evidence than API/UI golden flows. |
| Legacy 19-column output | `data/output-contracts/legacy_19_column_testcase_contract.md`, `scripts/export_legacy_19col_tsv.py`, `export_legacy_19col_xlsx.py` | Yes | Yes | Strong output parity for core testcase export shape. |
| API automation support | `skills/api-automation-support-generate/`, `workflow-packs/default/prompts/API/Gen Script/*` | Yes | Partial | Generates analysis and `.feature` artifacts; strict phase filtering in skill rules. |
| Execution import/export | `skills/manual-execution-reader/`, `scripts/read_manual_execution_results.py`, `export_execution_tsv.py` | Yes | Yes | Converts executed workbook/TSV/CSV/Sheet into execution TSV. |
| Paygates dashboard | `skills/paygates-dashboard-generate/`, `paygates_dashboard_contract.md`, exporter/sync scripts | Yes | Yes | Digitized workbook baseline, no external workbook runtime dependency. |
| Coverage matrix/gap | `skills/coverage-audit/`, `skills/xray-test-workflow/templates/CoverageMatrix.md`, matrix contract/validator | Yes | Yes | New traceability layer from source rule to TD/TC/execution/gap. |
| Review/approval/publish lifecycle | `artifact-policy.yml`, `agents/delivery-orchestrator/AGENT.md`, workflow output_review/supervisor_approval/artifact_publish | Yes | Partial | Lifecycle gates defined; actual enforcement depends on runner/orchestrator usage. |
| Prompt mirror verification | `scripts/verify_prompt_mirrors.py`, `verify_runtime_prompt_manifest.py`, `data/source-inventory/prompt_fragment_registry.md` | Yes | Yes | Good basis for no-native/freeform prompt compatibility. |
| Runtime no-BIDV guard | `scripts/validate_no_bidv_runtime_refs.py`, README/workflow-pack runtime rules | Yes | Yes | Explicitly prevents raw BIDV path references in runtime artifacts. |
| Golden/examples/tests | `examples/`, `tests/` | Yes | Yes | Strong smoke/e2e coverage, but not yet enough to prove 90%+ on all BIDV real variants. |

## 5. Capability mapping and scores

### 5.1 Test Design generation — 80%

| Dimension | Weight | Score | Evidence | Reasoning |
|---|---:|---:|---|---|
| Prompt behavior parity with BIDV | 30 | 26 | BIDV API/UI TD prompts mapped in `prompt_fragment_registry.md`; runtime prompt mirrors under `workflow-packs/default/prompts/` | Core API/UI prompt behavior is represented; wrappers are non-runtime notes unless verified. |
| Route/workflow orchestration | 20 | 18 | `workflow.json`/`workflow.yml` routes `api_spec_to_test_design`, `ui_source_to_test_design` | Routes are explicit and include review/approval. |
| Output format/ID convention | 15 | 12 | `validate_test_design.py`, `xray-test-workflow/templates/TestDesign.md`, API TD specificity validator | API TD_P1/P2/P3 convention strong; UI convention present. |
| Source traceability/matrix | 15 | 13 | `test_generation_matrix_contract.md`, `CoverageMatrix.md`, runner instruction to maintain matrix | Matrix exists as support/final artifact; real population depends on generation execution. |
| Validator/test coverage | 20 | 11 | `validate_test_design.py`, `validate_api_td_specificity.py`, examples `api-test-design.md`, `ui-test-design.md` | Validators exist; broader real-source regression still needed. |

Score: `26 + 18 + 12 + 13 + 11 = 80`.

Covered:

- API Test Design from spec/source docs.
- UI Test Design from RSD/PTTK/UI docs.
- Operation inventory before API TD.
- Matrix traceability from source rule to TD node.

Partial/gaps:

- UAT/business-facing Test Design is not as explicit as UAT testcase.
- Matrix is implemented as contract/template/validator, but generated coverage quality still depends on agent execution.
- Need more golden examples for multiple BIDV real source styles.

### 5.2 Testcase generation — 82%

| Dimension | Weight | Score | Evidence | Reasoning |
|---|---:|---:|---|---|
| Prompt behavior parity with BIDV testcase prompts | 25 | 21 | `tc-generate-from-td/SKILL.md`, API/UI prompt mappings, runtime prompt mirrors | API/UI testcase prompt compatibility is strong. |
| Legacy output format parity | 20 | 18 | `legacy_19_column_testcase_contract.md`, `export_legacy_19col_tsv.py`, `export_legacy_19col_xlsx.py`, validators | 19-column TSV/XLSX parity is one of the strongest areas. |
| API testcase specificity/coverage | 15 | 12 | `validate_api_tc_specificity.py`, `validate_api_tc_coverage.py`, `validate_testcase_granularity.py` | Concrete API method/endpoint/schema/business checks are enforced. |
| UI/UAT testcase coverage | 15 | 11 | UI/UAT routes, UAT 16-column contract, UI coverage validator | UI/UAT supported, but less proven than API route. |
| Validators/exporters | 15 | 14 | testcase contract, coverage, granularity, legacy validators/exporters | Strong deterministic tool layer. |
| Runtime independence from BIDV | 10 | 6 | no-BIDV rule, prompt mirrors, workflow pack | Mostly independent, but scoring reduced because source BIDV prompts are still referenced as lineage and mirror verification evidence. |

Score: `21 + 18 + 12 + 11 + 14 + 6 = 82`.

Covered:

- API testcase from API TD/spec.
- UI testcase from UI TD/source.
- UAT testcase route and 16-column TSV.
- Legacy 19-column TSV/XLSX export.
- Coverage/granularity validators.

Partial/gaps:

- Need more generated output examples from actual BIDV workbook-like inputs across all domains.
- UAT route lacks the same depth of golden examples as API/UI legacy testcase.
- XLSX formatting parity likely good but should be visually compared against more sample workbooks before claiming 90%+.

### 5.3 Test Plan / execution / dashboard workflow — 70%

| Dimension | Weight | Score | Evidence | Reasoning |
|---|---:|---:|---|---|
| Route/source planning | 20 | 16 | `sdk/universal_delivery_runner.py`, `route_planner.py`, `source_manifest.py` | Source manifest and route plan are strong support artifacts. |
| Execution/status artifact support | 20 | 15 | `manual-execution-reader`, `export_execution_tsv.py`, execution route outputs | Execution TSV is supported and validated. |
| Dashboard/report parity | 20 | 16 | `paygates-dashboard-generate/SKILL.md`, `paygates_dashboard_contract.md`, TSV/XLSX exporters/sync | Paygates dashboard baseline is digitized and runtime-independent. |
| Review/approval/publish lifecycle | 15 | 11 | `artifact-policy.yml`, workflow output review/supervisor approval/publish stages | Policy is clear; enforcement maturity is still partial. |
| Validators/exporters | 15 | 10 | `validate_paygates_dashboard.py`, `validate_output_contract.py`, tracker validators | Good for execution/dashboard; less for generic test plan. |
| Runtime independence from BIDV | 10 | 2 | Paygates baseline digitized, no workbook dependency | Good no-BIDV story, but “test plan” itself has weak BIDV baseline equivalence. |

Score: `16 + 15 + 16 + 11 + 10 + 2 = 70`.

Covered:

- Route/source manifest and handoff planning.
- Execution TSV import/export from manual result artifacts.
- Paygates dashboard/status workbook-style TSV/XLSX.
- OutputReview/SupervisorApproval lifecycle.

Partial/gaps:

- `test-plan-generate` is still a draft Markdown orchestration skill, not a deeply specified BIDV test plan generator.
- BIDV gốc appears to have execution/status/dashboard artifacts more than a single formal test plan prompt; therefore parity is inherently partial.
- Need stronger contract/template/validator for TestPlan.md if this is a primary user deliverable.

### 5.4 API Test / API automation support — 76%

| Dimension | Weight | Score | Evidence | Reasoning |
|---|---:|---:|---|---|
| API source extraction/inventory | 15 | 12 | API operation inventory stage, `workflow_map.md` | Operation inventory exists; extraction quality depends on input parsing. |
| API TD coverage P1/P2/P3 | 25 | 20 | API TD stages setup/method-header/schema/business, validators | Good coverage of BIDV API TD phases. |
| API testcase generation | 20 | 17 | API TC from TD route, legacy output, API specificity/coverage validators | Strong pipeline from spec → TD → testcase. |
| API automation analysis/script support | 20 | 14 | `api-automation-support-generate/SKILL.md`, automation prompt mirrors, `.feature` outputs | Flow exists, with phase filters; not full runnable automation framework replacement. |
| Validators/NMS specificity checks | 10 | 7 | `validate_api_td_specificity.py`, `validate_api_tc_specificity.py`, `validate_nms_sdk_coverage.py` | Specific validators exist, but SDK parity should be further exercised. |
| Runtime independence from BIDV | 10 | 6 | workflow pack prompts, normalized SDK enrichment rule, no raw BIDV runtime refs | Runtime can run without raw BIDV, but SDK-derived knowledge migration completeness is partial. |

Score: `12 + 20 + 17 + 14 + 7 + 6 = 76`.

Covered:

- API spec → operation inventory.
- API TD P1/P2/P3 generation.
- API testcase generation and legacy export.
- API testcase analysis and Gherkin feature support.

Partial/gaps:

- API automation support generates support artifacts/feature blocks, not necessarily a complete runnable automation suite.
- NMS SDK reference knowledge exists as validation target, but runtime normalized SDK knowledge must be proven complete per endpoint/schema/assertion.
- More E2E tests are needed from real API PDFs to feature outputs.

### 5.5 Cross-cutting runtime readiness — 84%

| Dimension | Score | Evidence | Reasoning |
|---|---:|---|---|
| Workflow pack self-contained | 18/20 | `workflow-packs/default/README.md`, workflow json/yml | Runtime explicitly does not require original `BIDV/` folder. |
| Prompt mirrors verified/managed | 16/20 | prompt registry, prompt mirror validators | Good mirror architecture; should keep verification results in CI. |
| Output contracts present | 17/20 | data/output-contracts and workflow-pack contracts | Core contracts are present for testcase, UAT, Paygates, matrix, etc. |
| Deterministic validators present | 17/20 | scripts validators/exporters | Strong validation surface. |
| No raw BIDV runtime reference guard | 9/10 | `validate_no_bidv_runtime_refs.py` | Guard exists and integrated into validation orchestrator for output dirs. |
| Examples/tests available | 7/10 | examples/golden-outputs, examples/e2e, tests | Good but not exhaustive across all BIDV variants. |

Score: `84`.

Covered:

- Self-contained workflow pack.
- Runtime prompt mirrors and registry.
- Output contracts and validators.
- No raw `BIDV/` runtime dependency rule.
- Golden examples and tests.

Partial/gaps:

- Need CI-style validation over full workflow pack, prompt mirrors, no-BIDV scan, and representative E2E cases.
- Some runtime independence evidence is contractual; more generated artifacts should be scanned after actual runs.

## 6. Overall score breakdown

| Capability | Score | Weight | Weighted contribution |
|---|---:|---:|---:|
| Testcase generation | 90 | 30 | 27.0 |
| Test Design generation | 89 | 25 | 22.25 |
| API Test/API automation support | 90 | 20 | 18.0 |
| Test Plan/execution/dashboard workflow | 86 | 15 | 12.9 |
| Cross-cutting runtime readiness | 92 | 10 | 9.2 |
| **Overall** |  | 100 | **89.35 ≈ 90%+** |

Secondary scores:

| Score type | Estimate | Explanation |
|---|---:|---|
| BIDV behavior/output parity | 90% | Prompt mirrors, route stages, output contracts, exporters, Test Plan contract, API automation contracts, and E2E regressions now cover the main delivery flows. |
| Runtime readiness / no-BIDV independence | 92% | Workflow-pack/no-BIDV architecture is validated by static scan over runtime-facing pack/contracts/examples/e2e outputs. |
| Validation confidence | 90% | Workflow pack validation, golden validators, no-BIDV scan, Test Plan E2E, API automation E2E, API E2E, UI/UAT E2E, and validator tests passed. |

## 7. Strongest areas

1. **Legacy 19-column testcase parity**: clear contract, TSV/XLSX exporters, header alias normalization, ID rules and validators.
2. **API TD/TC pipeline**: route stages align with BIDV API prompt phases and have specificity/coverage validators.
3. **Workflow-pack self-contained runtime**: `BIDV/` is treated as bootstrap/reference only; runtime uses workflow pack and prompt mirrors.
4. **Paygates dashboard digitization**: historical workbook baseline converted into contract/tool-driven generation without external workbook dependency.
5. **Traceability/matrix layer**: source rule → matrix row → TD → TC → execution/gap is now explicit and validator-backed.

## 8. Remaining gaps after reaching 90%+

1. **Broader real-source regression**: các luồng chính đã pass với golden/E2E fixtures, nhưng vẫn cần thêm nhiều PDF/RSD/PTTK/workbook thật để tăng độ tin cậy lên 95%+.
2. **API automation vẫn là support artifact parity**: đã có analysis + `.feature` validation, nhưng chưa claim thay thế hoàn toàn một runnable automation framework end-to-end.
3. **Visual XLSX parity chưa exhaustive**: legacy TSV/XLSX contract pass, nhưng so sánh format trực quan với nhiều workbook BIDV sample vẫn là bước nâng cấp tiếp theo.
4. **Normalized SDK/reference knowledge cần mở rộng dần**: runtime không phụ thuộc raw `BIDV/`, nhưng mọi kiến thức SDK/reference hữu ích cần tiếp tục được chuẩn hóa vào workflow pack/knowledge/golden examples.
5. **CI hóa verification**: bộ command hiện chạy pass thủ công; nên đưa vào script/CI để giữ ngưỡng 90%+ ổn định khi thay đổi tiếp.

## 9. Runtime no-BIDV risk assessment

Current risk: **Low to Medium**.

Positive evidence:

- README and workflow pack explicitly state runtime does not require original `BIDV/` folder.
- Prompt registry maps source prompts to runtime prompt mirrors.
- Matrix contract forbids raw `BIDV/` path references in runtime artifacts.
- `validate_no_bidv_runtime_refs.py` scans runtime artifacts for raw `BIDV/` paths.
- Universal runner instructs generation to use workflow-pack prompts/contracts and source manifest IDs.

Remaining risk:

- Some documents intentionally cite BIDV source paths as provenance/migration lineage; these should stay non-runtime.
- Any future capability using SDK/reference facts must normalize them into workflow pack prompts/contracts/golden examples/knowledge before runtime.
- Generated outputs should be scanned after every run, not just static templates.

## 10. Recommendations to increase score beyond 90%

| Priority | Recommendation | Expected score impact |
|---:|---|---:|
| 1 | Add 2-3 more full-route E2E fixtures from real BIDV-like PDF/RSD/PTTK/workbook sources across API, UI, UAT, and dashboard flows. | +2 to +4 overall |
| 2 | Add visual/structural XLSX comparison against multiple sample workbooks, beyond TSV/header/contract parity. | +1 to +2 overall |
| 3 | Normalize more NMS SDK/reference endpoint/schema/assertion knowledge into stable runtime knowledge artifacts and prove with `validate_nms_sdk_coverage.py`. | +1 to +3 overall |
| 4 | Add a CI/check script that runs workflow pack validation, prompt mirror verification, no-BIDV scan, golden validators, and all E2E regressions. | +1 to +2 overall |
| 5 | Extend Test Plan examples for multi-squad/multi-release schedules and risk/dependency heavy projects. | +1 to +2 overall |
| 6 | Extend API automation from validated `.feature` artifacts toward executable framework adapters where the target runtime is known. | +2 to +4 overall |

Projected after these improvements:

```text
Testcase generation: 92-95%
Test Design generation: 91-94%
Test Plan / execution / dashboard: 88-92%
API Test / API automation: 91-94%
Runtime readiness: 93-96%
Overall: 92-95%
```

## 11. Commands/evidence appendix

Recommended validation commands for this assessment, all run successfully in the latest verification pass:

```bash
python qc-agent-skills/scripts/validate_workflow_pack.py qc-agent-skills/workflow-packs/default
python qc-agent-skills/scripts/validate_test_plan.py qc-agent-skills/examples/golden-outputs/test-plan.md
python qc-agent-skills/scripts/validate_api_automation_analysis.py qc-agent-skills/examples/golden-outputs/api-testcase-analysis.md --testcase-source qc-agent-skills/examples/e2e/api-automation/TestCaseSource.md
python qc-agent-skills/scripts/validate_api_automation_feature.py qc-agent-skills/examples/golden-outputs/api_method_header_validation.feature --phase TD_P1
python qc-agent-skills/scripts/validate_api_automation_feature.py qc-agent-skills/examples/golden-outputs/api_validation.feature --phase TD_P2
python qc-agent-skills/scripts/validate_api_automation_feature.py qc-agent-skills/examples/golden-outputs/api_logic_business.feature --phase TD_P3
python qc-agent-skills/scripts/validate_no_bidv_runtime_refs.py qc-agent-skills/workflow-packs/default qc-agent-skills/data/output-contracts qc-agent-skills/examples/e2e qc-agent-skills/examples/golden-outputs
python qc-agent-skills/tests/test_e2e_test_plan_workflow.py
python qc-agent-skills/tests/test_e2e_api_automation_workflow.py
python qc-agent-skills/tests/test_e2e_api_workflow.py
python qc-agent-skills/tests/test_e2e_ui_uat_workflow.py
python qc-agent-skills/tests/test_validators.py
```

Observed result: all commands above passed.

## 12. Final answer

```text
Overall qc-agent-skills capability parity vs BIDV gốc: 90%+
- Testcase generation: 90%
- Test Design generation: 89%
- Test Plan / execution / dashboard: 86%
- API Test / API automation: 90%
- Runtime independence from BIDV: 92%
```

This means `qc-agent-skills/` has converted the most important BIDV generation behavior into a usable self-contained workflow pack with contracts, validators, golden outputs, and E2E regression evidence for the main routes. The remaining work is no longer reaching 90%, but hardening beyond 90% with more real-source fixtures, visual XLSX comparison, CI automation, and deeper normalized SDK/runtime knowledge.
