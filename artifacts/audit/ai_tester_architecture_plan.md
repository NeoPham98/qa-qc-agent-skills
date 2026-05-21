# AI Tester Architecture Plan

## 1. Executive summary

Yêu cầu của sếp là chuyển repo `qa-qc-agent-skills/` từ mô hình thiên về:

```text
source / prompt -> route -> prompt/skill -> output -> validate/review
```

sang mô hình:

```text
AI tester cognition system
-> hiểu tri thức
-> đọc hiểu input
-> phân tích/cook knowledge
-> brainstorm/risk reasoning
-> lập kế hoạch test
-> sinh output
-> review/học lại
```

Hướng xử lý kiến trúc:

1. **Không bỏ kiến trúc hiện tại.** Phần hiện tại đang mạnh ở output generation, contract validation, review/approval gates.
2. **Không gọi trực tiếp output skills từ raw input.** Output skills hiện có phải nằm sau các cognition artifacts.
3. **Bổ sung AI Tester Cognition Layer phía trước output generation.** Layer này gồm knowledge setup, input understanding, knowledge cooking, reasoning/brainstorming, planning.
4. **Bổ sung Reflection/Learning Layer phía sau review.** Layer này cập nhật lessons, defect patterns và tester memory.
5. **Tạo workflow pack mới cho AI tester.** Không sửa trực tiếp `workflow-packs/default/` trong giai đoạn đầu; tạo `workflow-packs/ai-tester/` ở phase implementation sau.

---

## 2. Current vs target architecture

## 2.1 Current architecture

Kiến trúc hiện tại là hybrid prompt-compatible QA orchestration/artifact system:

```text
source / user prompt
-> intent classification / route planning
-> workflow route
-> prompt / skill execution
-> output artifact
-> deterministic validators
-> output review
-> supervisor approval
-> publish
```

Backbone hiện tại cần giữ:

- `agents/delivery-orchestrator/AGENT.md`
- `workflow-packs/default/workflow.yml`
- output skills hiện có:
  - `skills/test-plan-generate/SKILL.md`
  - `skills/api-td-generate/SKILL.md`
  - `skills/ui-td-generate/SKILL.md`
  - `skills/tc-generate-from-td/SKILL.md`
  - `skills/uat-tc-generate/SKILL.md`
  - dashboard/execution/automation skills
- review/validation layer:
  - `agents/output-reviewer/AGENT.md`
  - `agents/coverage-auditor/AGENT.md`
  - `agents/contract-validator/AGENT.md`
  - `agents/supervisor/AGENT.md`
  - `scripts/validate_*.py`

## 2.2 Target architecture

Kiến trúc mục tiêu là AI tester cognition-first:

```text
source / user prompt
-> collect/setup knowledge
-> skim/break/analyze input
-> cook business/risk/coverage knowledge
-> brainstorm/test strategy planning
-> generate output
-> review/learn/update memory
```

Output skills hiện tại vẫn dùng, nhưng chỉ được gọi sau khi đã có các artifact trung gian như:

- `DocumentMap`
- `SourceBreakdown`
- `FactInventory`
- `BusinessRuleModel`
- `RiskModel`
- `CoveragePlan`
- `TesterStrategyPlan`

---

## 3. Target capability layers

## 3.1 Tester Knowledge System

### Mục tiêu

Tạo hệ tri thức của tester trước khi đọc sâu hoặc sinh output.

### Skill/agent cần có

- `knowledge-collector`
- `source-quality-analyzer`
- `context-builder`
- `tester-memory-manager`

### Artifact trung gian

- `SourceInventory.md/json`
- `KnowledgeMap.md/json`
- `CanonicalContextPackage.md`
- `TesterMemory.md/json`
- `MissingInputList.md`

### Reuse từ repo hiện tại

- `sdk/source_manifest.py`
- `skills/doc-normalizer/SKILL.md`
- `skills/secret-redactor/SKILL.md`
- `agents/knowledge-retriever/AGENT.md`
- `workflow-packs/default/workflow.yml` routes `source_inventory`, `source_normalization`, `secret_redaction`, `knowledge_validation`

### Quan hệ với layer khác

Output của layer này là nguồn context an toàn cho Input Understanding System.

---

## 3.2 Input Understanding System

### Mục tiêu

AI tester phải đọc hiểu input cụ thể trước khi phân tích sâu hoặc sinh output.

### Skill/agent cần có

- `document-skimmer`
- `document-breakdown`
- `api-spec-analyzer`
- `ui-flow-analyzer`
- `ambiguity-conflict-detector`

### Artifact trung gian

- `DocumentMap.md`
- `SourceBreakdown.md`
- `FactInventory.md`
- `RuleInventory.md`
- `OpenQuestions.md`
- `GapAnalysis.md`

### Reuse từ repo hiện tại

- `agents/spec-ui-locator/AGENT.md`
- `agents/requirement-coverage-analyst/AGENT.md`
- `sdk/intent_classifier.py`
- `data/source-inventory/workflow_map.md`

### Quan hệ với layer khác

Layer này biến source/context thành facts, rules, open questions và gaps cho Knowledge Cooking System.

---

## 3.3 Knowledge Cooking System

### Mục tiêu

Biến tài liệu/facts thành knowledge tester có cấu trúc, tái sử dụng được.

### Skill/agent cần có

- `business-rule-extractor`
- `domain-model-builder`
- `coverage-model-builder`
- `risk-model-builder`

### Artifact trung gian

- `BusinessRuleModel.md/json`
- `DomainKnowledgeModel.md/json`
- `CoverageModel.md/json`
- `ReusableKnowledgeBase.md/json`

### Reuse từ repo hiện tại

- `knowledge/standards/*`
- `agents/requirement-coverage-analyst/AGENT.md`
- `agents/coverage-auditor/AGENT.md`
- `skills/coverage-audit/SKILL.md`
- `data/output-contracts/test_generation_matrix_contract.md`

### Quan hệ với layer khác

Layer này cung cấp business/risk/coverage knowledge cho Reasoning và Planning.

---

## 3.4 Reasoning / Brainstorming System

### Mục tiêu

AI tester phải suy nghĩ như tester senior: tìm rủi ro, defect hypothesis, edge cases, coverage ideas.

### Skill/agent cần có

- `risk-brainstormer`
- `defect-hypothesis-generator`
- `edge-case-brainstormer`
- `coverage-idea-generator`

### Artifact trung gian

- `RiskModel.md`
- `DefectHypothesis.md`
- `EdgeCaseList.md`
- `CoverageIdeaList.md`

### Reuse từ repo hiện tại

- `agents/delivery-orchestrator/AGENT.md` senior-QC rules
- `knowledge/standards/ai_assisted_testing_standard.md`
- `agents/output-reviewer/AGENT.md` senior-QC review rubric
- `agents/coverage-auditor/AGENT.md` coverage audit rules

### Quan hệ với layer khác

Layer này tạo risk/test ideas cho Planning System trước khi output generation.

---

## 3.5 Planning System

### Mục tiêu

AI tester phải lập kế hoạch test trước khi generate output.

### Skill/agent cần có

- `test-strategy-planner`
- `coverage-planner`
- `test-data-planner`
- `question-planner`

### Artifact trung gian

- `TesterStrategyPlan.md`
- `CoveragePlan.md`
- `TestDataPlan.md`
- `QuestionBacklog.md`
- `ArtifactPlan.md`

### Reuse từ repo hiện tại

- `sdk/route_planner.py`
- `workflow-packs/default/workflow.yml` route planning/output definitions
- `skills/test-plan-generate/SKILL.md`
- `knowledge/standards/test_plan_standard.md`

### Quan hệ với layer khác

Layer này quyết định artifact nào cần sinh, coverage nào bắt buộc, câu hỏi nào phải hỏi trước khi generate.

---

## 3.6 Output Generation System

### Mục tiêu

Sinh output cuối sau khi đã có tri thức, phân tích, reasoning và plan.

### Skill/agent hiện có cần giữ

- `test-plan-generate`
- `api-td-generate`
- `ui-td-generate`
- `tc-generate-from-td`
- `uat-tc-generate`
- `test-set-build`
- `test-execution-pack-generate`
- `paygates-dashboard-generate`
- `api-automation-support-generate`

### Artifact cuối

- `TestPlan.md`
- `API_TestDesign.md`
- `UI_TestDesign.md`
- `TestCaseSource.md`
- `CoverageMatrix.md`
- `GapAnalysis.md`
- `Legacy19TestCase.generated.tsv/xlsx`
- `UAT_TestCase.generated.tsv`
- `TestExecution.from-manual.tsv`
- `PaygatesDashboard.generated.tsv/xlsx`
- API `.feature` files

### Quan hệ với layer khác

Output skills phải consume upstream cognition artifacts:

- `BusinessRuleModel`
- `RiskModel`
- `CoveragePlan`
- `TesterStrategyPlan`
- `QuestionBacklog`

---

## 3.7 Reflection / Learning System

### Mục tiêu

AI tester phải học từ validator failure, reviewer finding và execution result.

### Skill/agent cần có

- `reflection-learner`
- `feedback-to-knowledge-updater`
- `defect-pattern-memory-updater`
- mở rộng `tester-memory-manager`

### Artifact trung gian

- `ReviewFindings.md`
- `LessonsLearned.md`
- `DefectPatternMemory.md`
- `MemoryUpdate.md`

### Reuse từ repo hiện tại

- `agents/output-reviewer/AGENT.md`
- `agents/coverage-auditor/AGENT.md`
- `agents/supervisor/AGENT.md`
- `skills/supervisor-loop/SKILL.md`
- validator reports từ `scripts/validate_*.py`

### Quan hệ với layer khác

Layer này cập nhật Tester Knowledge System cho các run sau.

---

## 4. Proposed new skills/agents

## 4.1 Knowledge setup skills

| Skill/agent | Nhiệm vụ | Produces |
|---|---|---|
| `knowledge-collector` | Gom source, classify source, phát hiện thiếu source. | `SourceInventory`, `MissingInputList` |
| `source-quality-analyzer` | Đánh giá chất lượng source, conflict, stale docs, thiếu metadata. | `SourceQualityReport` |
| `context-builder` | Tạo context package an toàn cho route. | `CanonicalContextPackage` |
| `tester-memory-manager` | Lưu/retrieve/update memory theo project/domain/module. | `TesterMemory`, `MemoryUpdate` |

## 4.2 Input understanding skills

| Skill/agent | Nhiệm vụ | Produces |
|---|---|---|
| `document-skimmer` | Đọc lướt tài liệu, lập map section/table/API/UI/flow/rule. | `DocumentMap` |
| `document-breakdown` | Break tài liệu thành module/feature/flow/rule/field/state. | `SourceBreakdown` |
| `api-spec-analyzer` | Phân tích endpoint/header/request/response/error. | `ApiFactInventory` |
| `ui-flow-analyzer` | Phân tích screen/field/action/navigation/validation. | `UiFactInventory` |
| `ambiguity-conflict-detector` | Tìm ambiguity/conflict/gap/untestable requirement. | `OpenQuestions`, `GapAnalysis` |

## 4.3 Knowledge cooking skills

| Skill/agent | Nhiệm vụ | Produces |
|---|---|---|
| `business-rule-extractor` | Extract condition/action/outcome/exception/source. | `BusinessRuleModel` |
| `domain-model-builder` | Build entity/actor/state/flow model. | `DomainKnowledgeModel` |
| `coverage-model-builder` | Build coverage model từ rule/risk/source. | `CoverageModel` |
| `risk-model-builder` | Convert source/rules/history thành risk categories. | `RiskModel` |

## 4.4 Reasoning / brainstorming skills

| Skill/agent | Nhiệm vụ | Produces |
|---|---|---|
| `risk-brainstormer` | Brainstorm business/API/UI/data/state/permission risks. | `RiskModel` |
| `defect-hypothesis-generator` | Sinh giả thuyết lỗi cần kiểm. | `DefectHypothesis` |
| `edge-case-brainstormer` | Sinh edge cases/boundary/negative/state cases. | `EdgeCaseList` |
| `coverage-idea-generator` | Sinh coverage ideas theo risk/source/rule. | `CoverageIdeaList` |

## 4.5 Planning skills

| Skill/agent | Nhiệm vụ | Produces |
|---|---|---|
| `test-strategy-planner` | Lập strategy, scope, priority, risk, approach. | `TesterStrategyPlan` |
| `coverage-planner` | Lập coverage plan bắt buộc. | `CoveragePlan` |
| `test-data-planner` | Lập valid/invalid/boundary/role/state data plan. | `TestDataPlan` |
| `question-planner` | Gom câu hỏi cần hỏi BA/PO/user trước generation. | `QuestionBacklog` |

## 4.6 Reflection / learning skills

| Skill/agent | Nhiệm vụ | Produces |
|---|---|---|
| `reflection-learner` | Đọc validator/reviewer/execution feedback và rút lesson. | `LessonsLearned` |
| `feedback-to-knowledge-updater` | Cập nhật reusable knowledge từ feedback. | `MemoryUpdate` |
| `defect-pattern-memory-updater` | Lưu defect/review pattern để tái sử dụng. | `DefectPatternMemory` |

---

## 5. Intermediate artifact model

## 5.1 Knowledge artifacts

| Artifact | Purpose |
|---|---|
| `SourceInventory.md/json` | Danh sách source, source type, role, owner, confidence, missing info. |
| `KnowledgeMap.md/json` | Bản đồ tri thức theo project/squad/epic/module/domain. |
| `CanonicalContextPackage.md` | Context đã chọn, đã trace, an toàn cho route tiếp theo. |
| `TesterMemory.md/json` | Memory domain/rule/decision/open questions/lessons. |
| `MissingInputList.md` | Danh sách input còn thiếu. |

## 5.2 Understanding artifacts

| Artifact | Purpose |
|---|---|
| `DocumentMap.md` | Map section/table/API/UI/flow/rule trong tài liệu. |
| `SourceBreakdown.md` | Breakdown module/feature/flow/rule/field/state. |
| `FactInventory.md` | Fact đã xác nhận, có source reference. |
| `RuleInventory.md` | Rule thô trước khi cook thành business model. |
| `OpenQuestions.md` | Câu hỏi do thiếu/ambiguous/conflict source. |
| `GapAnalysis.md` | Gap/contradiction/untestable points. |

## 5.3 Cooking artifacts

| Artifact | Purpose |
|---|---|
| `BusinessRuleModel.md/json` | Rule có condition/action/outcome/exception/source. |
| `DomainKnowledgeModel.md/json` | Entity/actor/state/flow/domain model. |
| `CoverageModel.md/json` | Coverage model theo rule/risk/source. |
| `ReusableKnowledgeBase.md/json` | Knowledge đã cook, có thể reuse qua run. |

## 5.4 Reasoning artifacts

| Artifact | Purpose |
|---|---|
| `RiskModel.md` | Risk category, cause, impact, priority, source. |
| `DefectHypothesis.md` | Giả thuyết lỗi cần kiểm. |
| `EdgeCaseList.md` | Edge/boundary/negative/state/permission cases. |
| `CoverageIdeaList.md` | Ý tưởng coverage trước khi lập coverage plan. |

## 5.5 Planning artifacts

| Artifact | Purpose |
|---|---|
| `TesterStrategyPlan.md` | Strategy theo scope/risk/priority/approach. |
| `CoveragePlan.md` | Coverage bắt buộc trước output generation. |
| `TestDataPlan.md` | Valid/invalid/boundary/role/state data strategy. |
| `QuestionBacklog.md` | Câu hỏi cần hỏi trước hoặc trong generation. |
| `ArtifactPlan.md` | Artifact nào cần sinh và thứ tự sinh. |

## 5.6 Reflection artifacts

| Artifact | Purpose |
|---|---|
| `ReviewFindings.md` | Findings từ reviewer/validator/supervisor. |
| `LessonsLearned.md` | Bài học rút ra từ lỗi hoặc feedback. |
| `DefectPatternMemory.md` | Pattern lỗi/review/execution hay gặp. |
| `MemoryUpdate.md` | Patch cập nhật vào tester memory. |

---

## 6. Workflow pack strategy

## 6.1 Keep default workflow pack

Không sửa trực tiếp `workflow-packs/default/` ở giai đoạn đầu. Pack này tiếp tục là output-generation/runtime pack hiện tại.

## 6.2 Add AI tester workflow pack later

Ở giai đoạn implementation, tạo pack mới:

```text
workflow-packs/ai-tester/
```

Các file dự kiến:

```text
workflow-packs/ai-tester/workflow.yml
workflow-packs/ai-tester/validators.yml
workflow-packs/ai-tester/artifact-policy.yml
workflow-packs/ai-tester/review-gates.yml
workflow-packs/ai-tester/contracts/
workflow-packs/ai-tester/templates/
```

## 6.3 Cognition routes

Các route chính:

| Route | Purpose | Outputs |
|---|---|---|
| `source_to_knowledge` | Setup source/knowledge/context/memory. | `SourceInventory`, `KnowledgeMap`, `CanonicalContextPackage` |
| `source_to_understanding` | Skim/break/analyze input. | `DocumentMap`, `SourceBreakdown`, `FactInventory`, `OpenQuestions` |
| `understanding_to_cooked_knowledge` | Build business/domain/coverage models. | `BusinessRuleModel`, `DomainKnowledgeModel`, `CoverageModel` |
| `cooked_knowledge_to_strategy` | Brainstorm risks and plan strategy. | `RiskModel`, `DefectHypothesis`, `TesterStrategyPlan`, `CoveragePlan` |
| `strategy_to_outputs` | Call existing output generation skills. | `TestPlan`, `TestDesign`, `TestCase`, etc. |
| `review_to_memory_update` | Learn from review/execution. | `LessonsLearned`, `MemoryUpdate`, `DefectPatternMemory` |

---

## 7. Migration plan

## Phase 1: Architecture docs and taxonomy

### Deliverables

- `ai_tester_architecture_plan.md`
- `ai_tester_skill_taxonomy.md`
- `ai_tester_intermediate_artifacts.md`

### Goal

Chốt kiến trúc và language chung với sếp/team.

## Phase 2: Cognition contracts/templates

### Deliverables

Contracts/templates cho:

- `DocumentMap`
- `SourceBreakdown`
- `BusinessRuleModel`
- `RiskModel`
- `CoveragePlan`
- `TesterStrategyPlan`
- `TesterMemory`
- `LessonsLearned`

### Goal

Không để cognition skills thành prompt rời rạc; mọi artifact trung gian phải có contract.

## Phase 3: Cognition agents/skills skeleton

### Deliverables

Agent/skill definitions cho:

- `knowledge-collector`
- `document-skimmer`
- `document-breakdown`
- `business-rule-extractor`
- `risk-brainstormer`
- `test-strategy-planner`
- `tester-memory-manager`
- `reflection-learner`

### Goal

Tạo skeleton vai trò, inputs, outputs, forbidden behavior, handoff contracts.

## Phase 4: AI tester workflow pack

### Deliverables

- `workflow-packs/ai-tester/`
- cognition-first routes
- validators/review gates cho cognition artifacts

### Goal

Đưa AI tester cognition flow thành runtime workflow, không chỉ tài liệu.

## Phase 5: Wire output skills behind cognition artifacts

### Deliverables

Output skills consume upstream artifacts:

- `BusinessRuleModel`
- `RiskModel`
- `CoveragePlan`
- `TesterStrategyPlan`
- `QuestionBacklog`

### Goal

Chặn việc generate output trực tiếp từ raw input khi thiếu cognition artifacts.

## Phase 6: Evaluation and demo

### Deliverables

- evaluation scenarios
- golden examples
- tests chứng minh cognition-first behavior

### Goal

Chứng minh với sếp rằng AI đã làm việc giống tester: đọc hiểu, phân tích, brainstorm, plan, rồi mới sinh output.

---

## 8. Evaluation plan

| Scenario | Pass criteria |
|---|---|
| Raw API spec input | AI tạo `DocumentMap`, `BusinessRuleModel`, `RiskModel`, `CoveragePlan` trước `TestCaseSource`. |
| Missing requirement | AI tạo `OpenQuestions` hoặc `QuestionBacklog`, không invent rule. |
| Ambiguous UI flow | AI ghi ambiguity/conflict vào `GapAnalysis`. |
| Complex business rule | AI tạo `BusinessRuleModel` hoặc decision table trước TD/TC. |
| Risk-heavy feature | AI tạo `RiskModel` và `DefectHypothesis`. |
| Review rejects output | AI tạo `LessonsLearned` và `MemoryUpdate`. |
| Similar future feature | AI reuse `TesterMemory` hoặc `DefectPatternMemory`. |

---

## 9. Implementation boundaries

## 9.1 In scope for this architecture plan

- Define target architecture.
- Define capability layers.
- Define proposed skills/agents.
- Define intermediate artifacts.
- Define migration phases.
- Define evaluation criteria.

## 9.2 Out of scope for this architecture plan

- Implement new agents/skills.
- Modify existing workflow pack.
- Create `workflow-packs/ai-tester/`.
- Write validators/contracts.
- Refactor SDK runners.

Những phần out of scope sẽ được xử lý trong implementation plan sau.

---

## 10. Final recommendation

Hướng xử lý đúng yêu cầu sếp là:

```text
Giữ output engine hiện tại
+ thêm cognition layer phía trước
+ thêm reflection/memory layer phía sau
= AI tester architecture
```

Câu trả lời ngắn gọn cho sếp:

> Hệ hiện tại đã mạnh ở tầng sinh output và kiểm soát chất lượng. Để thành AI tester như con người, không gọi output skill trực tiếp từ raw input nữa. Cần thêm cognition flow trước output: knowledge setup, skimming/breakdown/analyzing docs, cooking business/risk/coverage knowledge, brainstorming, test strategy planning. Sau output cần reflection/memory update để AI học qua review/execution. Output skills hiện tại được giữ lại nhưng chuyển thành tầng cuối của AI tester system.
