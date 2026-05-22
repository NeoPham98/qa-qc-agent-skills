# AI Tester Operating System

Package này triển khai **AI Tester Operating System**: một hệ agent skills làm việc như QC senior. Trục chính không phải raw input -> output artifact, mà là đọc nguồn, xây tri thức, hiểu tài liệu, cook knowledge, brainstorm/risk reasoning, planning, rồi mới sinh output QA/test.

Runtime chính là `workflow-packs/ai-tester/`. `workflow-packs/default/` được giữ làm output-generation subsystem để tái sử dụng prompt, contract, validator, exporter và golden examples hiện có.

## Operating mode chính

```text
Source/Input
-> Knowledge System
-> Input Understanding System
-> Knowledge Cooking System
-> Reasoning / Brainstorming System
-> Planning System
-> Cognition Gate
-> Output Generation System
-> Review / Approval System
-> Reflection / Memory System
```

Rule lõi:

```text
Không sinh TestPlan/TestDesign/TestCase/UAT/export trực tiếp từ raw input.
Output skills chỉ chạy sau khi cognition artifacts đạt cognition gate.
```

## AI Tester OS layers

| Layer | Nhiệm vụ | Component chính |
|---|---|---|
| Knowledge System | collect, classify, source quality, context package, memory | `knowledge-collector`, `source-quality-analyzer`, `context-builder`, `knowledge-retriever` |
| Input Understanding System | skim, break down, analyze API/UI/docs, detect gaps | `document-skimmer`, `document-breakdown`, `api-spec-analyzer`, `ui-flow-analyzer`, `ambiguity-conflict-detector` |
| Knowledge Cooking System | raw facts -> business/domain/coverage/risk model | `business-rule-extractor`, `domain-model-builder`, `coverage-model-builder`, `risk-model-builder` |
| Reasoning / Brainstorming System | risks, defect hypotheses, edge cases, coverage ideas | `risk-brainstormer`, `defect-hypothesis-generator`, `edge-case-brainstormer`, `coverage-idea-generator` |
| Planning System | strategy, coverage, test data, questions, artifact plan | `test-strategy-planner`, `coverage-planner`, `test-data-planner`, `question-planner` |
| Output Generation System | Test Plan, TD, TC, UAT, automation, execution, dashboard | existing output skills and `workflow-packs/default/` |
| Review / Approval System | output review, contract validation, supervisor approval | `output-reviewer`, `contract-validator`, `supervisor` |
| Reflection / Memory System | lessons, memory update, defect pattern update | `reflection-learner`, `feedback-to-knowledge-updater`, `defect-pattern-memory-updater` |

## Cognition gate

Before any final output generation, the AI Tester OS must provide:

- `SourceInventory.md`
- `DocumentMap.md`
- `FactInventory.md`
- `BusinessRuleModel.md` or blocker `OpenQuestions.md`
- `RiskModel.md`
- `CoveragePlan.md`
- `TesterStrategyPlan.md`
- `QuestionBacklog.md`

Missing facts must be visible as `OpenQuestions`, `QuestionBacklog`, or `[PENDING_DOC:<fact>]`. Hypotheses must not be treated as confirmed requirements.

## Universal file + prompt runner

Khi user chỉ “ném file + prompt”, dùng universal runner để tự phân loại source, suy luận intent, chọn route trong AI Tester OS và tạo artifact đúng gate:

```bash
python sdk/universal_delivery_runner.py \
  --workflow-pack ai-tester \
  --source ./input/api_spec.pdf \
  --prompt "Sinh test design, testcase 19 cột và test API theo AI Tester OS như QC senior" \
  --output-dir ./outputs/run-001 \
  --plan-only
```

`--workflow-pack ai-tester` là default. Chỉ dùng `--workflow-pack default` khi cần chạy legacy/output subsystem trực tiếp để tương thích.

## Output Generation Subsystem

Output subsystem giữ các năng lực hiện có:

- `API_TestDesign.md` / `UI_TestDesign.md`
- `TestCaseSource.md`
- `Legacy19TestCase.generated.tsv` / `Legacy19TestCase.generated.xlsx`
- `UAT_TestCaseSource.md` / `UAT_TestCase.generated.tsv`
- API `.feature` files
- `TestExecution.from-manual.tsv`
- `PaygatesDashboard.generated.tsv` / `PaygatesDashboard.generated.xlsx`
- `CoverageMatrix.md` / `GapAnalysis.md`

For testcase-generation routes, `CoverageMatrix.md` remains mandatory traceability: split source rules by technique/value class/boundary/state/role before writing testcase rows. `GapAnalysis.md` records open questions, pruned combinations, and uncovered matrix rows.

Support artifacts như `source_manifest.json`, `route_plan.json`, `validation_report.json`, `OutputReview.md`, `SupervisorApproval.md`, `handoff_summary.md` phục vụ trace/debug/validation.

## Entry point

Bắt đầu từ `agents/delivery-orchestrator/AGENT.md`, now acting as AI Tester Orchestrator.

Luồng end-to-end bất biến:

```text
Project -> Squad -> Epic/Module
-> Source Inventory
-> Document Map / Source Breakdown
-> Fact / Rule Inventory
-> Business / Domain / Coverage / Risk Model
-> Defect Hypothesis / Edge Case / Coverage Ideas
-> Tester Strategy / Coverage / Test Data / Question Plan
-> Cognition Gate
-> Test Plan / Test Design / Test Case / Export / Automation / Execution / Dashboard
-> Output Review
-> Supervisor Approval
-> Artifact Publish
-> Reflection / Memory Update
```

Mọi request Project/Squad/Epic/API/UI/UAT/Execution/Automation/Review phải đi qua AI Tester Orchestrator để:

1. xác định layer cần chạy,
2. chọn route trong `workflow-packs/ai-tester`,
3. xác nhận upstream cognition artifacts,
4. điều phối specialist/output subsystem,
5. kiểm cognition/output contracts trước handoff.

## Source behavior

- Raw BIDV prompts trong `BIDV/Prompt/**` là source behavior reference.
- Runtime prompt mirrors trong `prompts-verbatim/**` phải khớp nguyên văn với source BIDV prompt và được verify bằng `scripts/verify_prompt_mirrors.py` khi default/output subsystem cần dùng.
- Files trong `skills/*/prompts/*.md` là non-runtime notes/wrappers nếu không được verify là content-equivalent với source prompt.
- BIDV specs/UI/test design/source docs là business source input.
- Output contracts trong `data/output-contracts/` quyết định export format.

## Readiness boundary

A run is AI Tester OS-ready only after cognition artifacts satisfy `workflow-packs/ai-tester/contracts/cognition_artifact_contract.md`, cognition gate satisfies `workflow-packs/ai-tester/contracts/cognition_gate_contract.md`, selected output validators pass, `OutputReview.md` exists, and `SupervisorApproval.md` records approved/rejected status with blocker rationale.

## QA standards

- QC delivery: [qc_delivery_standard.md](knowledge/standards/qc_delivery_standard.md)
- Source document intake: [source_document_standard.md](knowledge/standards/source_document_standard.md)
- Test Plan: [test_plan_standard.md](knowledge/standards/test_plan_standard.md)
- Test Design: [test_design_standard.md](knowledge/standards/test_design_standard.md)
- Testcase: [testcase_standard.md](knowledge/standards/testcase_standard.md)
- Test Generation Matrix: [test_generation_matrix_standard.md](knowledge/standards/test_generation_matrix_standard.md)
- Excel output: [excel_output_standard.md](knowledge/standards/excel_output_standard.md)
- Manual execution status: [manual_execution_status_standard.md](knowledge/standards/manual_execution_status_standard.md)
- AI-assisted testing: [ai_assisted_testing_standard.md](knowledge/standards/ai_assisted_testing_standard.md)
- Prompt preservation: [prompt_preservation_standard.md](knowledge/standards/prompt_preservation_standard.md)
- Workflow non-skip gates: [workflow_non_skip_gate_standard.md](knowledge/standards/workflow_non_skip_gate_standard.md)

## Output contracts

- Legacy 19-column testcase: [legacy_19_column_testcase_contract.md](data/output-contracts/legacy_19_column_testcase_contract.md)
- UAT 16-column testcase: [uat_16_column_testcase_contract.md](data/output-contracts/uat_16_column_testcase_contract.md)
- Test generation matrix / coverage matrix: [test_generation_matrix_contract.md](data/output-contracts/test_generation_matrix_contract.md)
- Markdown normalization: [markdown_normalization_rules.md](data/output-contracts/markdown_normalization_rules.md)
- BIDV Excel output similarity: [excel_output_similarity.md](data/output-contracts/excel_output_similarity.md)
- Extended testcase/TestLink-style contract: [testcase_excel_columns.md](data/output-contracts/testcase_excel_columns.md)
- Test execution/status contract: [test_status_excel_columns.md](data/output-contracts/test_status_excel_columns.md)
- Manual execution reader contract: [manual_execution_reader_contract.md](data/output-contracts/manual_execution_reader_contract.md)
- Paygates dashboard/status contract: [paygates_dashboard_contract.md](data/output-contracts/paygates_dashboard_contract.md)
- XRAY/Jira field mapping: [xray_field_mapping.md](data/output-contracts/xray_field_mapping.md)

## Routing references

- AI Tester workflow: [workflow.yml](workflow-packs/ai-tester/workflow.yml)
- Cognition artifact contract: [cognition_artifact_contract.md](workflow-packs/ai-tester/contracts/cognition_artifact_contract.md)
- Cognition gate contract: [cognition_gate_contract.md](workflow-packs/ai-tester/contracts/cognition_gate_contract.md)
- Output subsystem workflow: [workflow.yml](workflow-packs/default/workflow.yml)
- Prompt mirror manifest: [prompt_mirror_manifest.json](data/source-inventory/prompt_mirror_manifest.json)
- Orchestrator playbook: [prompt_compatible_orchestration.md](agents/delivery-orchestrator/playbooks/prompt_compatible_orchestration.md)

## Self-contained Paygates dashboard

`BIDV/Tổng hợp Trạng Thái Test Case Paygates (1).xlsx` is digitized as an internal contract, not required at runtime. Use the Paygates exporters to generate a maintainable dashboard from testcase/execution artifacts:

```bash
python scripts/export_paygates_dashboard_tsv.py --testcase examples/full-xray-chain/TestCase.md --execution examples/full-xray-chain/TestExecution.md --project "BIDV Paygates" --squad "Squad A" --sprint "Sprint 1" --epic "Paygates Regression" --detail-link "examples/full-xray-chain/TestCase.md" --output examples/full-xray-chain/PaygatesDashboard.generated.tsv
python scripts/validate_paygates_dashboard.py examples/full-xray-chain/PaygatesDashboard.generated.tsv
python scripts/export_paygates_dashboard_xlsx.py examples/full-xray-chain/PaygatesDashboard.generated.tsv examples/full-xray-chain/PaygatesDashboard.generated.xlsx
```

The generated dashboard follows [paygates_dashboard_contract.md](data/output-contracts/paygates_dashboard_contract.md) and does not depend on an external workbook template.

## Agent Teams và SDK runners

Agent Teams là runtime coordination construct; không commit `.claude/teams` hoặc task-list runtime state vào repo. Repo chỉ lưu reusable role definitions, playbooks, SDK runner, hooks/guardrails và validation helpers.

Reusable team recipes:

- Full API delivery team: [api_delivery_team.md](playbooks/agent-teams/api_delivery_team.md)
- Output review team: [output_review_team.md](playbooks/agent-teams/output_review_team.md)
- Closed-loop delivery team: [closed_loop_delivery_team.md](playbooks/agent-teams/closed_loop_delivery_team.md)

Reusable review/validation roles:

- Output reviewer: [AGENT.md](agents/output-reviewer/AGENT.md)
- Coverage auditor: [AGENT.md](agents/coverage-auditor/AGENT.md)
- Contract validator: [AGENT.md](agents/contract-validator/AGENT.md)

SDK runner layer:

- SDK guide: [README.md](sdk/README.md)
- Universal AI Tester OS runner: [universal_delivery_runner.py](sdk/universal_delivery_runner.py)
- BIDV API delivery runner: [api_delivery_runner.py](sdk/api_delivery_runner.py)
- BIDV Paygates dashboard runner: [paygates_dashboard_runner.py](sdk/paygates_dashboard_runner.py)
- Guardrail hooks: [hooks.py](sdk/hooks.py)
- Deterministic MCP/helper tools: [mcp_tools.py](sdk/mcp_tools.py)
- Claude Code settings example: [settings.example.json](.claude/settings.example.json)
- Runner example: [api_delivery_runner.example.md](examples/sdk/api_delivery_runner.example.md)

## Scripts

Generate and validate BIDV legacy 19-column testcase TSV/XLSX:

```bash
python scripts/export_legacy_19col_tsv.py examples/full-xray-chain/Legacy19TestCase.md examples/golden-outputs/testcase-legacy-19col.tsv
python scripts/validate_legacy_19col_tsv.py examples/golden-outputs/testcase-legacy-19col.tsv
python scripts/export_legacy_19col_xlsx.py examples/full-xray-chain/Legacy19TestCase.md examples/full-xray-chain/Legacy19TestCase.generated.xlsx
```

`export_legacy_19col_xlsx.py` creates formatted XLSX by default, with filters, wrapping, summary, and real Excel line breaks. Use `--formatted` only for explicitness; use `--basic` only when a minimal unstyled workbook is intentionally required.

Read manual execution result from a returned VA-style workbook and feed Paygates dashboard sync:

```bash
python scripts/read_manual_execution_results.py --input examples/full-xray-chain/Legacy19TestCase.generated.xlsx --output examples/full-xray-chain/TestExecution.from-manual.tsv --round 1 --test-execution-id TE-PAYGATES-001 --test-set-id TS-SIT-001 --tester tester01 --build-version SIT-001
python scripts/validate_output_contract.py --execution examples/full-xray-chain/TestExecution.from-manual.tsv
python scripts/export_paygates_dashboard_tsv.py --testcase examples/full-xray-chain/Legacy19TestCase.md --execution examples/full-xray-chain/TestExecution.from-manual.tsv --project "BIDV Paygates" --squad "Squad A" --sprint "Sprint 1" --epic "Paygates Regression" --detail-link "examples/full-xray-chain/Legacy19TestCase.generated.xlsx" --output examples/full-xray-chain/PaygatesDashboard.from-manual.tsv
python scripts/sync_paygates_dashboard_xlsx.py --dashboard-tsv examples/full-xray-chain/PaygatesDashboard.from-manual.tsv --output examples/full-xray-chain/PaygatesDashboard.synced.xlsx
```

Generate and validate XRAY-compatible testcase/execution TSV:

```bash
python scripts/export_testcase_tsv.py examples/full-xray-chain/TestCase.md examples/full-xray-chain/TestCase.generated.tsv
python scripts/export_execution_tsv.py examples/full-xray-chain/TestExecution.md examples/full-xray-chain/TestExecution.generated.tsv
python scripts/validate_output_contract.py --testcase examples/golden-outputs/testcase-compatible.tsv --execution examples/golden-outputs/test-execution-compatible.tsv
```
