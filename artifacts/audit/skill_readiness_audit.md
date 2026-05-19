# BIDV Skill Readiness Audit

Date: 2026-05-18
Scope: `BIDV/` vs `qc-agent-skills/`

## Executive summary

Overall readiness: **23 / 26 points = 88.5% covered**.

The agent skills package is broadly ready for BIDV-style QA/test artifact generation: it covers API TD, API testcase, UI TD, UI testcase, UAT testcase, legacy 19-column export, execution import, Paygates dashboard, coverage audit, output review, supervisor approval, and artifact lifecycle routing.

Main blockers are not missing core skills, but **wiring/naming consistency**:

1. Prompt mirror verification currently fails because manifest/registry paths point to `...` while the actual repo is `qc-agent-skills/...`.
2. Some source inventory entries mention historical sample files that are not present at the current `BIDV/` root.
3. API automation support is present, but should be validated against real `BIDV/api_automation/` framework expectations before claiming full execution readiness.
4. User wants neutral naming: many `qc-agent-skills/` paths include `bidv`; rename should be audited and applied carefully because references are widespread.

Cowork/subagent recommendation: **do not add a new cowork system yet**. The repo already has a strong closed-loop team model. Recommended action is to fix/standardize role wiring and path references first; add a new cowork role only if later audits prove a missing owner such as Excel similarity auditor or PDF extraction verifier.

## Source inventory summary from BIDV/

Observed inventory:

| Area | Count / examples | Role |
|---|---:|---|
| `BIDV/Prompt/API/` | API TD setup/context, method/header, schema, business logic, API TC from TD, Gen Script prompts | Source prompt engine for API test design, manual testcase, automation support |
| `BIDV/Prompt/UI/` and `BIDV/UI/` | `UI_Gen_TD.txt`, `UI_Gen_TC_From_TD.txt`, `UI_Gen_TC_For_UAT.txt` | Source prompt engine for UI TD, UI testcase, UAT testcase |
| `BIDV/template/` | 4 DOC templates | Reference format/source structure for PTTK/RSD-style docs |
| `BIDV/Faker_upd/` | 16 PDFs, 2 sample testcase XLSX | RSD/PTTK/URD/API source examples and expected testcase samples |
| `BIDV/api_automation/` | SDK modules and tests | Automation framework/context for generated API feature/script support |
| `BIDV/Tổng hợp Trạng Thái Test Case Paygates (1).xlsx` | root workbook | Historical Paygates dashboard/status baseline |

File totals from read-only inventory:

- `BIDV/`: 84 files, 22 directories.
- Main types: `.txt` 24, `.pdf` 16, `.py` 10, `.pyc` 10, `.xlsx` 4, `.doc/.docx` 6, `.jpg` 5, `.pptx` 1.

## Capability inventory summary from qc-agent-skills/

Observed inventory:

- `qc-agent-skills/README.md` defines one operating mode: BIDV Prompt-Compatible Orchestration Mode.
- `qc-agent-skills/data/source-inventory/` contains workflow map, prompt registry, prompt mirror manifest, source inventory, orchestration mode.
- `qc-agent-skills/data/output-contracts/` contains contracts for legacy 19-column testcase, UAT 16-column testcase, execution/status, Paygates dashboard, XRAY mapping, manual execution reader, Excel similarity, markdown normalization.
- `qc-agent-skills/prompts-verbatim/` contains runtime prompt mirrors.
- `qc-agent-skills/workflow-packs/default/` contains workflow routes, validators, contracts, prompts, examples, artifact policy, review gates.
- `qc-agent-skills/skills/` contains 20 BIDV-related skills.
- `qc-agent-skills/agents/` contains 15 BIDV-related agent roles.
- `qc-agent-skills/scripts/` contains exporters, validators, source manifest builder, normalizer, redactor, workflow runner, dashboard sync, and specificity/coverage checks.
- `qc-agent-skills/examples/` contains golden outputs, full xray chain, e2e API/UI/UAT examples, and SDK examples.
- `qc-agent-skills/artifacts/default/` contains draft/reviewed/approved/rejected/archive lifecycle artifacts.

File totals from read-only inventory:

- `qc-agent-skills/`: 1,252 files, 480 directories.
- Main types: `.md` 310, `.py` 68, `.tsv` 52, `.pyc` 54, `.xlsx` 17, `.yml` 18, `.json` 23, no-extension/git files 669.

## Coverage matrix

Scoring: 2 = Covered, 1 = Partial, 0 = Missing.

| Output / workflow | Score | Status | Evidence | Gap / note |
|---|---:|---|---|---|
| API TD - setup/context | 2 | Covered | `skills/api-td-generate/`, `workflow-packs/default/prompts/API/API_TD_1_Setup_Context.txt`, `validate_test_design.py` | Runtime mirror verification path currently points to old package name. |
| API TD - method/header | 2 | Covered | `_BreakDown` prompt in workflow pack, API TD skill, API TD validator | Registry uses old package path. |
| API TD - schema validation | 2 | Covered | `_BreakDown` prompt in workflow pack, API TD skill, specificity validator | Registry uses old package path. |
| API TD - business/cross logic | 2 | Covered | `_BreakDown` prompt in workflow pack, API TD skill, specificity validator | Registry uses old package path. |
| API testcase 19-column | 2 | Covered | `tc-generate-from-td`, legacy 19-col contract, TSV/XLSX exporters, validators, golden outputs | Good coverage. |
| UI Test Design | 2 | Covered | `ui-td-generate`, UI prompt mirror/workflow prompt, UI TD validator, golden output | Runtime mirror path reference still old in registry. |
| UI testcase from TD | 2 | Covered | `tc-generate-from-td`, UI prompt, legacy export, UI TC validation | Good coverage. |
| UAT testcase 16-column | 2 | Covered | `uat-tc-generate`, UAT 16-column contract, workflow route | Good coverage. |
| API automation feature/script support | 1 | Partial | `api-automation-support-generate`, Gen Script prompts, workflow routes to `.feature` outputs | Needs validation against real `BIDV/api_automation/` framework conventions and execution examples. |
| Paygates dashboard/status | 2 | Covered | Paygates dashboard contracts, TSV/XLSX exporters, validators, sync script, golden outputs | Strong coverage. |
| XRAY/TestSet/TestExecution | 2 | Covered | `xray-test-workflow`, TestSet/TestExecution templates, testcase/execution exporters and validators | Good coverage. |
| Source trace/coverage gap | 2 | Covered | `coverage-audit`, coverage auditor, CoverageMatrix example, workflow route | Good coverage; should run on real target artifacts for per-project gap ratio. |
| Output review/handoff | 2 | Covered | Output reviewer, contract validator, supervisor, review gates, artifact lifecycle workflow | Good coverage. |

Coverage ratio: `23 / (2 * 13) = 88.5%`.

## Secondary readiness ratios

| Dimension | Result | Notes |
|---|---:|---|
| Prompt coverage | 10/12 clearly mirrored in current manifest; workflow pack contains 12/12 runtime prompts including BreakDown variants | Verification fails due old package path, not necessarily missing files. |
| Output contract coverage | 9/9 major contracts present | Contracts exist for legacy testcase, UAT, execution, dashboard, XRAY, manual import, markdown normalization, Excel similarity. |
| Validator/exporter coverage | High | Workflow pack wires validators for TD, TC, execution, dashboard, tracker, artifact manifest. |
| Evidence/golden examples | High | Golden TSV/XLSX and e2e examples exist. API automation feature examples are less proven. |
| Governance/cowork coverage | High | Closed-loop lifecycle, reviewer, validator, coverage auditor, supervisor already exist. |

## Missing gaps

### P0 - Blocker

1. **Prompt mirror verification fails due old package path.**
   - Command run: `python qc-agent-skills/scripts/verify_prompt_mirrors.py`.
   - Failure: it looks for `prompts-verbatim/...` instead of actual `qc-agent-skills/prompts-verbatim/...`.
   - Affected files likely include:
     - `qc-agent-skills/data/source-inventory/prompt_mirror_manifest.json`
     - `qc-agent-skills/data/source-inventory/prompt_fragment_registry.md`
     - possibly `qc-agent-skills/scripts/verify_prompt_mirrors.py`

2. **Source inventory contains stale/historical root sample references.**
   - `workflow_map.md` references `BIDV/NMS-Đặc tả API cho SDK-170326-075931.pdf` and `BIDV/VA_19.004 - Xem chi tiết yêu cầu Thêm mới KSV.xlsx`, but current root listing did not show these exact files.
   - Current samples are under `BIDV/Faker_upd/**` and root Paygates workbook.

### P1 - Important

1. **API automation support needs real framework validation.**
   - The prompts and skills exist, but readiness should be checked against `BIDV/api_automation/nms_sdk/` and `BIDV/api_automation/tests/`.
   - Add or run tests proving generated `.feature` / script support maps to actual SDK conventions.

2. **Neutral naming request has broad blast radius.**
   - 641 paths in `qc-agent-skills/` contain `bidv`.
   - Renaming should be staged and reference-aware, not bulk rename.

3. **Prompt registry uses old package name.**
   - Many registry rows point to `...`.
   - This conflicts with the actual repo folder `qc-agent-skills/`.

### P2 - Nice-to-have

1. Remove committed/generated cache artifacts from future package hygiene if desired: `__pycache__`, `.DS_Store`, and `.git` object inventory noise.
2. Add benchmark/sample-comparison notes for Excel similarity beyond headers/contracts.
3. Add a concise architecture diagram in README after naming stabilizes.

## Cowork/subagent recommendation

Recommendation: **do not add a new cowork system now**.

The repo already has the correct cowork model:

| Role | Existing evidence | Recommendation |
|---|---|---|
| Lead/orchestrator | `agents/delivery-orchestrator/` | Keep; later rename neutrally if approved. |
| Knowledge retriever | `agents/knowledge-retriever/` | Keep. |
| Generator workers | API TD, UI TD, testcase, UAT, automation support skills/agents | Keep. |
| Contract validator | `agents/contract-validator/`, validators scripts | Keep. |
| Coverage auditor | `agents/coverage-auditor/`, `skills/coverage-audit/` | Keep. |
| Output reviewer | `agents/output-reviewer/`, review gates | Keep. |
| Supervisor | `agents/supervisor/`, supervisor loop skill | Keep. |

Recommended improvement: **Add missing role wiring**, not new cowork:

- Fix package path references in manifest/registry/scripts.
- Ensure every workflow route in `workflow-packs/default/workflow.yml` has matching skill/agent ownership and validator evidence.
- Only consider a new cowork role if future execution proves one of these gaps:
  - Excel similarity auditor.
  - PDF extraction verifier.
  - API automation script reviewer.

## Neutral naming audit: removing `bidv` from qc-agent-skills paths

User requested file/folder names inside `qc-agent-skills/` not contain `bidv`. This should be done after audit approval because references are widespread.

Initial path scan:

- Total paths containing `bidv`: **641**.
- High-impact areas:
  - `agents/*`
  - `skills/*`
  - `data/output-contracts/`
  - `data/source-inventory/*.md/json`
  - `workflow-packs/default/`
  - `knowledge/default/`
  - `artifacts/default/`
  - `examples/e2e/`
  - `examples/golden-outputs/*bidv*`
  - `scripts/*bidv*.py`
  - `tests/test_*.py`

### Recommended rename candidates

| Current path/name | Proposed neutral name | Reason | References to update | Risk |
|---|---|---|---|---|
| `agents/delivery-orchestrator/` | `agents/delivery-orchestrator/` | Agent role is generic within this package | README, manifests, workflow map, playbooks | High |
| `agents/api-test-design-agent/` | `agents/api-test-design-agent/` | Remove domain prefix from folder | Orchestrator refs, team playbooks | Medium |
| `agents/testcase-generator/` | `agents/testcase-generator/` | Neutral role name | Registry, playbooks | Medium |
| `agents/output-reviewer/` | `agents/output-reviewer/` | Neutral role name | Review team playbook | Medium |
| `agents/contract-validator/` | `agents/contract-validator/` | Neutral role name | Workflow/review docs | Medium |
| `agents/coverage-auditor/` | `agents/coverage-auditor/` | Neutral role name | Coverage route docs | Medium |
| `agents/supervisor/` | `agents/supervisor/` | Neutral role name | Closed-loop playbook | Medium |
| `skills/api-td-generate/` | `skills/api-td-generate/` | Neutral skill package | Registry, workflow map, README | High |
| `skills/tc-generate-from-td/` | `skills/tc-generate-from-td/` | Neutral skill package | Registry, README | High |
| `skills/ui-td-generate/` | `skills/ui-td-generate/` | Neutral skill package | Registry, README | High |
| `skills/uat-tc-generate/` | `skills/uat-tc-generate/` | Neutral skill package | Registry, README | High |
| `skills/api-automation-support-generate/` | `skills/api-automation-support-generate/` | Neutral skill package | Registry, workflow map | High |
| `skills/xray-test-workflow/` | `skills/xray-test-workflow/` | Neutral skill package | README, links, examples | Medium |
| `skills/paygates-dashboard-generate/` | `skills/paygates-dashboard-generate/` | Neutral skill package | README, workflow map | Medium |
| `data/output-contracts/` | `data/output-contracts/` | Contract folder is package-local | README, workflow pack sync, scripts | High |
| `data/source-inventory/*.md/json` | remove `` prefix | Neutral file names | README, scripts, workflow refs | High |
| `workflow-packs/default/` | `workflow-packs/default/` or `workflow-packs/qa-default/` | Remove domain from pack name | README, runners, tests, examples | High |
| `knowledge/default/` | `knowledge/default/` or `knowledge/project/` | Runtime knowledge folder | manifest paths, normalizer/redactor scripts | High |
| `artifacts/default/` | `artifacts/default/` or `artifacts/project/` | Lifecycle artifacts folder | workflow pack artifact dirs, runners | High |
| `scripts/*bidv*.py` | remove `` from script names | Neutral command names | tests, README, workflow validators | High |
| `tests/test_*.py` | remove `` from test names | Neutral tests | test discovery unaffected; imports may change | Medium |
| `examples/e2e/` | `examples/e2e/` | Neutral example path | README links | Medium |
| `examples/golden-outputs/*bidv*` | remove `bidv` from filenames | Neutral artifacts | README, validators/tests | Medium |

### Naming recommendation

Do not bulk rename all 641 paths at once. Use phases:

1. Phase A: Fix stale package path references from `qc-agent-skills` to `qc-agent-skills` or relative paths.
2. Phase B: Rename top-level neutral folders with highest value: `data/output-contracts`, `workflow-packs/default`, skill/agent folder prefixes.
3. Phase C: Rename scripts/tests/examples after imports and docs are updated.
4. Phase D: Rename runtime artifact/knowledge folders only after confirming existing artifact history can move safely.

Important: Keeping the word **BIDV inside document content** is still appropriate where it describes the business/domain contract. The user request is about file/folder names.

## Recommended next actions

1. Fix prompt mirror manifest/registry path references so `verify_prompt_mirrors.py` passes in the current repo.
2. Re-run core validators against golden outputs:
   - legacy 19-column testcase TSV
   - Paygates dashboard TSV
   - testcase/execution TSV
   - workflow pack validation
3. Run focused API automation readiness audit against `BIDV/api_automation/`.
4. Produce a separate rename implementation plan for neutral naming and apply it in controlled phases.
5. After path fixes and validator run, update readiness score; expected score should move from **88.5%** to **95%+** if prompt verification and automation evidence pass.
