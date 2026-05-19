# BIDV Automation Test Agent Skills

Package này chỉ hỗ trợ **Prompt-Compatible Orchestration Mode**.

Agent skills không thay thế prompt/workflow hiện có của BIDV bằng native generation. Agent skills đóng vai trò điều phối: chọn đúng workflow pack/prompt đã đóng gói, gom đủ input mà prompt yêu cầu, generate theo đúng rule/prohibition của prompt, normalize output thành Markdown source-of-truth, export TSV/Excel-style đúng contract, rồi review trước handoff.

Runtime mặc định là self-contained workflow pack `workflow-packs/default/`; package không cần folder `BIDV/` tồn tại khi vận hành. Folder BIDV lịch sử chỉ là bootstrap/reference để tạo workflow pack.

## Operating mode duy nhất

```text
BIDV request
-> orchestrator intake
-> request classification
-> registry lookup
-> source/runtime verbatim prompt selection
-> prompt mirror verification
-> prompt-required input gathering
-> BIDV prompt-compatible generation
-> markdown normalization
-> TSV/Excel-style export
-> output review
-> handoff
```

Không có Native Agent Mode. Không generate freeform ngoài selected BIDV runtime verbatim prompt và source docs đã duyệt.

## Universal file + prompt runner

Khi user chỉ “ném file + prompt”, dùng universal runner để tự phân loại source, suy luận intent, chọn route trong workflow pack và tạo output QA/test cuối:

```bash
python sdk/universal_delivery_runner.py \
  --workflow-pack default \
  --source ./input/api_spec.pdf \
  --prompt "Sinh test design, testcase BIDV 19 cột và test API" \
  --output-dir ./outputs/run-001 \
  --plan-only
```

User-facing final outputs tùy route:

- `API_TestDesign.md` / `UI_TestDesign.md`
- `TestCaseSource.md`
- `Legacy19TestCase.generated.tsv` / `Legacy19TestCase.generated.xlsx`
- `UAT_TestCaseSource.md` / `UAT_TestCase.generated.tsv`
- API `.feature` files
- `TestExecution.from-manual.tsv`
- `PaygatesDashboard.generated.tsv` / `PaygatesDashboard.generated.xlsx`
- `CoverageMatrix.md` / `GapAnalysis.md`

For testcase-generation routes, `CoverageMatrix.md` is not optional: it is the dense senior-QC expansion layer used to split source rules by technique/value class/boundary/state/role before writing testcase rows. `GapAnalysis.md` records open questions, pruned combinations, and uncovered matrix rows.

Support artifacts như `source_manifest.json`, `route_plan.json`, `validation_report.json`, `OutputReview.md`, `handoff_summary.md` chỉ phục vụ trace/debug/validation.

## Entry point

Bắt đầu từ `agents/delivery-orchestrator/AGENT.md`.

Luồng end-to-end bất biến là:

```text
Project -> Squad -> Epic/Module -> Source Inventory -> Source Analysis -> Test Plan -> Test Design -> Test Generation Matrix / Coverage Matrix -> Test Case -> formatted Excel artifact -> Manual Execution -> Execution import / Status update -> Dashboard / Review -> Supervisor Approval -> Publish approved artifact
```

Mọi request Project/Squad/Epic/API/UI/UAT/Execution/Automation/Review phải đi qua orchestrator để:

1. xác định artifact cần sinh,
2. chọn prompt/workflow BIDV tương ứng,
3. xác nhận input bắt buộc,
4. điều phối skill chuyên trách,
5. kiểm output contract trước handoff.

## Source behavior

- Raw BIDV prompts trong `BIDV/Prompt/**` là source behavior reference.
- Runtime prompt mirrors trong `prompts-verbatim/**` phải khớp nguyên văn với source BIDV prompt và được verify bằng `scripts/verify_prompt_mirrors.py`.
- Files trong `skills/*/prompts/*.md` là non-runtime notes/wrappers nếu không được verify là content-equivalent với source prompt.
- BIDV specs/UI/test design/source docs là business source input.
- Output contracts trong `data/output-contracts/` quyết định export format.

## Readiness boundary

Agents are linked through orchestrator routing, the prompt registry, owning skills, runtime owning roles, prompt mirror verification, and output review/contract validation gates. A document-to-output run is BIDV-ready only after the selected runtime verbatim prompts are verified, generated artifacts record source/runtime prompt metadata, `OutputReview` passes, and required TSV/Excel-style validators pass.

## Output bắt buộc

- Markdown artifact để maintain, review và diff.
- Legacy BIDV 19-column TSV cho API/UI manual testcase khi cần output giống file BIDV hiện tại.
- UAT 16-column TSV khi workflow UAT yêu cầu.
- XRAY/TestLink-style TSV cho traceability, Test Set và Test Execution handoff khi cần.
- Review report trước handoff.

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

- One-mode definition: [orchestration_mode.md](data/source-inventory/orchestration_mode.md)
- BIDV workflow map: [workflow_map.md](data/source-inventory/workflow_map.md)
- Prompt fragment registry: [prompt_fragment_registry.md](data/source-inventory/prompt_fragment_registry.md)
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
