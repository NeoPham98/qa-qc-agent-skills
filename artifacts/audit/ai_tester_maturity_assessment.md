# AI Tester Maturity Assessment

## 1. Executive conclusion

Kết luận chính:

1. Repo hiện tại **đã có nền tảng mạnh cho workflow QA artifact generation có kiểm soát**.
2. Repo hiện tại **chưa đạt đầy đủ mô hình AI tester giống con người** nếu định nghĩa “AI tester” là một hệ cognition có tự chủ thu thập tri thức, cooking tri thức, hiểu tài liệu đa bước, brainstorming/planning động, self-reflection và học qua vòng lặp.
3. Repo hiện tại đạt mức **hybrid prompt-compatible QA orchestration/artifact system**: có một số capability cognition được mô tả trong agent/standard, nhưng runtime vẫn chủ yếu là workflow/prompt/validator-driven.
4. Điểm mạnh hiện tại nằm ở **output generation, traceability, contract validation, review/approval gate**.
5. Điểm thiếu để đạt “AI tester như con người” nằm ở **living memory, cognitive skill taxonomy, skimming/breakdown skill độc lập, business/risk model persistent, brainstorming skill, dynamic tester planning loop, learning/reflection loop**.

## 2. Target model theo yêu cầu “AI tester như con người”

Target model được chia thành 6 capability groups:

| Group | Năng lực cần có |
|---|---|
| 1. Knowledge setup | Collecting data, source manifest, canonical source, redaction, context package, memory/context. |
| 2. Knowledge cooking | Normalize docs, extract requirement/rule/risk/coverage model, biến tài liệu thô thành tester knowledge. |
| 3. Input understanding | Skimming, breaking docs, locating API/UI/DB facts, ambiguity/gap/conflict detection. |
| 4. Tester reasoning / planning / brainstorming | Senior tester thinking, risk strategy, test strategy, dynamic planning, hypothesis/alternative exploration. |
| 5. Output generation | Test Plan, Test Design, Test Case, UAT, Matrix, Execution, Dashboard, Automation support. |
| 6. Feedback / reflection | Validators, output review, supervisor approval, retry/improve, robotic-output blockers, learning from feedback. |

Status dùng trong report:

- **Có**: repo có agent/skill/workflow/script rõ ràng, có inputs/outputs/gates hoặc implementation script.
- **Một phần**: repo có rule/standard/agent description hoặc một phần flow, nhưng thiếu runtime loop/implementation rõ ràng.
- **Không tìm thấy bằng chứng**: không có file hoặc rule cụ thể trong các phần đã đọc.

---

## 3. Capability matrix tổng hợp

| Capability group | Status | Evidence chính | Conclusion |
|---|---|---|---|
| Knowledge setup | Một phần | `doc-normalizer`, `knowledge-retriever`, `source_manifest.py`, workflow routes `source_inventory`, `source_normalization`, `secret_redaction`, `knowledge_validation` | Có pipeline setup knowledge, nhưng chưa thấy living tester memory/context manager. |
| Knowledge cooking | Một phần | `doc-normalizer`, `requirement-coverage-analyst`, `delivery-orchestrator`, `knowledge/standards/*` | Có normalize, requirement/coverage analysis và standards; chưa thấy persistent domain rule/risk model. |
| Input understanding | Một phần | `spec-ui-locator`, `requirement-coverage-analyst`, `knowledge-retriever`, `intent_classifier.py` | Có locate facts, source trace, open questions; chưa thấy skill riêng cho skimming/breakdown docs như cognitive capability độc lập. |
| Tester reasoning / planning / brainstorming | Một phần | `delivery-orchestrator` senior-QC rules, `ai_assisted_testing_standard.md`, `route_planner.py`, Test Plan route | Có planning/risk/decomposition rule; không tìm thấy brainstorming skill/stage và dynamic tester planning loop đầy đủ. |
| Output generation | Có | `workflow.yml` routes/stages cho Test Plan, API/UI TD, API/UI/UAT TC, automation, execution, dashboard, coverage audit | Đây là phần đầy đủ nhất của repo hiện tại. |
| Feedback / reflection | Một phần | `output-reviewer`, `coverage-auditor`, `contract-validator`, validators, supervisor gates, retry/improve rule | Có review/validator/retry gates; chưa thấy persistent learning/memory update từ feedback. |

---

## 4. Detailed assessment by capability

## 4.1 Knowledge setup

### 4.1.1 Collecting data / source inventory

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Source inventory | Có | `workflow-packs/default/workflow.yml:21-40` định nghĩa route `source_inventory` với output `source-manifest.yml`. | Repo có route chính thức để build source inventory. |
| Source manifest data model | Có | `sdk/source_manifest.py:9-58` định nghĩa `GoogleSheetRef`, `SourceFingerprint`, `SourceItem`, `UserContext`, `SourceManifest`. | Repo có model để lưu source, fingerprint, context và output directory. |
| Source hashing / fingerprint support | Có | `sdk/source_manifest.py:68-88` có `file_sha256()` và `source_item_from_path()`. | Repo có cơ chế tracking file bằng hash và metadata cơ bản. |
| Multi-channel data collection | Một phần | `sdk/source_manifest.py:10-16` có `GoogleSheetRef`; `knowledge-retriever` nhận candidate source files tại `agents/knowledge-retriever/AGENT.md:20`. | Có biểu diễn Google Sheet/local file, nhưng chưa thấy collector agent/skill chuyên gom source đa kênh. |

### 4.1.2 Knowledge normalization / redaction / safe context

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Normalize raw docs | Có | `skills/doc-normalizer/SKILL.md:15-33` quy định normalize source manifest sang Markdown/TSV profile. | Repo có skill bootstrap knowledge normalization. |
| Metadata for normalized knowledge | Có | `skills/doc-normalizer/SKILL.md:35-43` yêu cầu metadata `source_path`, `source_role`, `canonical_status`, `redaction_status`. | Repo có rule metadata để trace nguồn normalized knowledge. |
| Prevent raw sensitive runtime use | Có | `skills/doc-normalizer/SKILL.md:44-48` cấm dùng normalized output trực tiếp trước redaction và cấm publish raw sensitive files. | Repo có guardrail rõ cho sensitive data. |
| Redacted canonical context retrieval | Có | `agents/knowledge-retriever/AGENT.md:30-38` prefer `knowledge/default/redacted/`, canonical sources, preserve path/role/status. | Repo có agent lấy context runtime an toàn từ knowledge đã redacted/canonical. |
| Missing input / open questions | Có | `agents/knowledge-retriever/AGENT.md:22-28` output có missing input list, Open Questions, redaction warning list. | Repo có cơ chế ghi nhận thiếu input thay vì tự bịa dữ liệu. |
| Living tester memory | Không tìm thấy bằng chứng | Các file đã đọc có manifest/context package, nhưng không có agent/skill tên memory manager hoặc cơ chế update memory qua nhiều run. | Repo chưa có bằng chứng về memory dài hạn kiểu tester tích lũy kinh nghiệm. |

### Kết luận Knowledge setup

**Status: Một phần.** Repo có pipeline setup knowledge tương đối rõ: inventory, source manifest, normalization, redaction, canonical/redacted retrieval. Repo chưa có bằng chứng về **living tester memory** hoặc **knowledge collector agent** tự chủ gom nguồn đa kênh như một tester con người.

---

## 4.2 Knowledge cooking

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Convert source into normalized artifacts | Có | `skills/doc-normalizer/SKILL.md:25-33` nêu workflow normalize `.txt/.md/.doc/.xlsx/.pptx/.pdf`. | Repo có cooking bước đầu: biến nguồn thô thành Markdown/TSV/profile. |
| Source analysis/decomposition in delivery flow | Có | `agents/delivery-orchestrator/AGENT.md:28-30` nêu flow có `source analysis/decomposition`. | Repo có rule orchestration cho phân tích và decomposition nguồn. |
| Requirement extraction | Có | `agents/requirement-coverage-analyst/AGENT.md:10-13` nêu extract requirements và audit requirement-to-design-to-testcase coverage. | Repo có agent role cho requirement extraction. |
| Coverage model / matrix | Có | `agents/requirement-coverage-analyst/AGENT.md:28-33` yêu cầu Requirement Inventory, Coverage Matrix, gap/open-question findings. | Repo có artifact hóa coverage knowledge. |
| Business rule / risk model persistent | Không tìm thấy bằng chứng | Có standards và coverage rules, nhưng không thấy file/agent/skill tạo persistent business rule graph, risk model, decision model dùng lại qua run. | Repo chưa có evidence về cooked knowledge model bền vững như tester cognition system. |
| Knowledge cooking lifecycle | Một phần | `workflow-packs/default/workflow.yml:41-103` có `source_normalization`, `secret_redaction`, `knowledge_validation`; chưa thấy route riêng cho business-rule/risk-model cooking. | Lifecycle knowledge hiện thiên về normalize/redact/validate hơn là tạo model nhận thức nghiệp vụ. |

### Kết luận Knowledge cooking

**Status: Một phần.** Repo có normalization, requirement/coverage analysis và standards. Repo chưa có bằng chứng về **business rule model**, **risk model**, **domain knowledge graph**, hoặc **persistent tester knowledge model** được cooking từ nguồn và tái sử dụng qua run.

---

## 4.3 Input understanding

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Locate API/DB/UI facts | Có | `agents/spec-ui-locator/AGENT.md:10-13` định nghĩa locate API, DB, UI field, button, screen, design references. | Repo có agent chuyên locate facts phục vụ generation. |
| API locator rows | Có | `agents/spec-ui-locator/AGENT.md:28-30` yêu cầu method, endpoint path, headers, request fields, response fields, status/error codes, source reference. | Repo có output contract cho API fact extraction. |
| DB/UI locator rows | Có | `agents/spec-ui-locator/AGENT.md:31-33` yêu cầu DB rows và UI locator rows. | Repo có output contract cho DB/UI fact extraction. |
| Separate fact vs assumption/open question | Có | `agents/spec-ui-locator/AGENT.md:39-43` yêu cầu separate confirmed facts from assumptions/open questions. | Repo có guardrail hiểu nguồn không bịa. |
| Requirement ambiguity/gap detection | Có | `agents/requirement-coverage-analyst/AGENT.md:31-33` yêu cầu gap/open-question findings cho uncovered, ambiguous, contradictory, untestable requirements. | Repo có capability phát hiện gap/ambiguity/contradiction ở mức agent role. |
| Skimming docs skill | Không tìm thấy bằng chứng | Không thấy agent/skill/stage tên `document-skimmer`, `skimming`, hoặc workflow riêng tạo document map từ skim. | Repo chưa có skill skimming độc lập. |
| Breaking docs into parts skill | Một phần | `agents/delivery-orchestrator/AGENT.md:54-55` yêu cầu decompose operation/UI flow/business rule/field/header/state/boundary; nhưng không thấy skill độc lập tên breakdown. | Có rule decomposition, chưa có cognitive skill/module riêng cho document breakdown. |
| Intent classification | Có | `sdk/intent_classifier.py:6-25` định nghĩa keyword map cho intents; `sdk/intent_classifier.py:39-50` classify intent và missing input cho dashboard metadata. | Repo có classifier rule-based cho intent. |
| Deep semantic input understanding | Một phần | Có locator/analyst/rules; classifier hiện dựa keyword/source roles tại `sdk/intent_classifier.py:39-84`. | Có input understanding theo workflow/role, chưa thấy implementation semantic analyzer sâu độc lập. |

### Kết luận Input understanding

**Status: Một phần.** Repo có fact locator, requirement coverage analyst, open question/gap handling và intent classifier. Repo chưa có bằng chứng về **document skimming skill**, **document breakdown skill** độc lập, hoặc **semantic understanding loop** tự chủ trước khi chọn output.

---

## 4.4 Tester reasoning / planning / brainstorming

### 4.4.1 Senior tester reasoning

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Senior-QC planning/coverage rule | Có | `agents/delivery-orchestrator/AGENT.md:50-61` enforce risk-based scope, decomposition, happy/exception/negative/boundary/error/business/cross coverage. | Repo có rule mô phỏng senior-QC thinking cho artifact routes. |
| Human-style quality standard | Có | `knowledge/standards/ai_assisted_testing_standard.md:29-39` yêu cầu read source, analyze deeply, split modules, design before cases, executable steps, measurable expected, visible gaps. | Repo có standard định nghĩa hành vi giống senior QC. |
| Coverage audit reasoning | Có | `agents/coverage-auditor/AGENT.md:42-48` yêu cầu split by field, value class, boundary, state, role, decision-table. | Repo có audit reasoning rule cụ thể. |
| Risk-based Test Plan review | Có | `agents/output-reviewer/AGENT.md:43` yêu cầu Test Plan senior-QC depth, risk-based coverage, defect patterns, data strategy. | Repo có review gate bắt lỗi Test Plan thiếu tư duy risk. |

### 4.4.2 Planning

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Route planning | Có | `sdk/route_planner.py:44-74` map classification sang route stages, outputs, support outputs. | Repo có route planning deterministic. |
| Test Plan route | Có | `workflow-packs/default/workflow.yml:104-133` route `source_to_test_plan` generate Test Plan từ project/scope/source baseline. | Repo có output skill cho Test Plan. |
| Dynamic tester planning loop | Không tìm thấy bằng chứng | `route_planner.py` là rule mapping; không thấy agent/skill lập kế hoạch động dựa trên hypothesis, alternatives, trade-off, ask/refine loop. | Repo chưa có planner cognition loop đầy đủ như tester senior. |

### 4.4.3 Brainstorming

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Brainstorming skill/stage | Không tìm thấy bằng chứng | Không thấy route/stage/agent/skill tên brainstorming, risk-brainstormer, hypothesis generation, test charter brainstorming trong các file đã đọc. | Repo chưa có capability brainstorming độc lập. |
| Alternative exploration | Một phần | `sdk/intent_classifier.py:100-108` có `infer_alternatives()` cho một số route alternatives. | Có alternatives ở mức route fallback, không phải divergent testing idea brainstorming. |
| Risk hypothesis generation | Không tìm thấy bằng chứng | Có risk-based review rules, nhưng không thấy artifact/skill tạo danh sách risk hypotheses trước TD/TC. | Repo chưa có risk-brainstorming artifact rõ ràng. |

### Kết luận Tester reasoning / planning / brainstorming

**Status: Một phần.** Repo có nhiều senior-QC rules, planning rules và review rubric. Repo chưa có bằng chứng về **brainstorming skill**, **dynamic tester planning loop**, hoặc **risk hypothesis generation** độc lập trước output generation.

---

## 4.5 Output generation

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Test Plan generation | Có | `workflow-packs/default/workflow.yml:104-133` route `source_to_test_plan`, output `TestPlan.md`, `TestPlan.generated.xlsx`. | Repo có output route Test Plan đầy đủ. |
| API Test Design | Có | `workflow-packs/default/workflow.yml:134-164` route `api_spec_to_test_design`, stages API operation inventory + TD fragments + validation. | Repo có route API TD đầy đủ. |
| API Test Case | Có | `workflow-packs/default/workflow.yml:165-207` route `api_spec_to_testcase`, output `TestCaseSource.md`, `CoverageMatrix.md`, `GapAnalysis.md`, TSV/XLSX. | Repo có route API testcase đầy đủ. |
| UI Test Design | Có | `workflow-packs/default/workflow.yml:244-270` route `ui_source_to_test_design`. | Repo có route UI TD. |
| UI Test Case | Có | `workflow-packs/default/workflow.yml:271-311` route `ui_source_to_testcase`. | Repo có route UI testcase. |
| UAT Test Case | Có | `workflow-packs/default/workflow.yml:346-377` route `urd_to_uat_testcase`, output `UAT_TestCaseSource.md`, `UAT_TestCase.generated.tsv`. | Repo có route UAT testcase. |
| API automation support | Có | `workflow-packs/default/workflow.yml:378-457` routes `testcase_to_api_automation` và `api_spec_to_automation`. | Repo có route automation support/Gherkin feature. |
| Manual execution import | Có | `workflow-packs/default/workflow.yml:458-481` route `executed_workbook_to_execution`. | Repo có route execution import. |
| Paygates dashboard | Có | `workflow-packs/default/workflow.yml:482-538` routes dashboard từ executed workbook hoặc testcase. | Repo có dashboard/status output route. |
| Coverage audit output | Có | `workflow-packs/default/workflow.yml:539-569` route `coverage_audit`, output `CoverageMatrix.md`, `GapAnalysis.md`. | Repo có coverage audit output route. |
| Validators/exporters | Có | `workflow-packs/default/workflow.yml:796-824` map validators sang scripts; `workflow.yml:686-700` có export 19col/UAT. | Repo có deterministic validation/export layer. |

### Kết luận Output generation

**Status: Có.** Đây là capability hoàn chỉnh nhất. Repo có route, stage, prompt/tool, final output và validator cho hầu hết artifact QA/QC: Test Plan, Test Design, Test Case, Coverage Matrix, Execution, Dashboard, Automation support.

---

## 4.6 Feedback / reflection

| Capability | Status | Evidence | Conclusion |
|---|---|---|---|
| Output review gate | Có | `workflow-packs/default/workflow.yml:777-782` stage `output_review`; `agents/output-reviewer/AGENT.md:24-29` output `OutputReview.md`, pass/fail/blocking issues. | Repo có review gate chính thức. |
| Supervisor approval gate | Có | `workflow-packs/default/workflow.yml:783-789` stage `supervisor_approval`; final outputs trong nhiều routes có `SupervisorApproval.md`. | Repo có approval gate chính thức. |
| Retry/improve rule | Có | `agents/delivery-orchestrator/AGENT.md:30` có `retry/improve`; `workflow.yml` routes có `max_retries: 2`. | Repo có loop retry ở mức workflow. |
| Robotic-output blocker | Có | `agents/output-reviewer/AGENT.md:49-50` xem robotic/generic/bundled/happy-case-only output là blocker. | Repo có review rule chống output máy móc. |
| Reviewer does not self-fix | Có | `agents/output-reviewer/AGENT.md:60-65` cấm silently fix, approve own output, ignore validator failures. | Repo tách vai trò generator/reviewer. |
| Persistent learning from feedback | Không tìm thấy bằng chứng | Không thấy memory update skill, learning loop, feedback-to-knowledge update route hoặc script lưu pattern lỗi để cải thiện lần sau. | Repo chưa có learning/reflection loop như AI tester tích lũy kinh nghiệm. |

### Kết luận Feedback / reflection

**Status: Một phần.** Repo có validator, review, approval, retry và blocker rules. Repo chưa có bằng chứng về **persistent self-learning**, **memory update**, hoặc **feedback-to-knowledge cooking** sau mỗi run.

---

## 5. Gap analysis

## 5.1 Missing or weak cognition skills

| Missing capability | Status hiện tại | Evidence gap | Tác động |
|---|---|---|---|
| `knowledge-collector` | Không tìm thấy bằng chứng | Có source manifest model nhưng không thấy agent/skill chuyên gom source đa kênh. | AI chưa giống tester tự đi gom tài liệu/context. |
| `tester-memory-manager` | Không tìm thấy bằng chứng | Không thấy route/agent/skill update/retrieve long-term tester memory qua run. | Không có năng lực tích lũy kinh nghiệm lâu dài. |
| `document-skimmer` | Không tìm thấy bằng chứng | Không thấy stage/skill skimming tạo document map. | Thiếu bước đọc lướt để hiểu cấu trúc tài liệu trước phân tích sâu. |
| `document-breakdown` | Một phần | Có decomposition rule trong orchestrator, nhưng không có skill/module độc lập. | Breakdown đang là rule trong flow, chưa là cognitive skill reusable. |
| `business-rule-extractor` | Một phần | Requirement analyst có extract requirements, nhưng chưa thấy business rule model persistent. | Chưa có rule inventory/model dùng lại qua output skills. |
| `risk-brainstormer` | Không tìm thấy bằng chứng | Có risk-based review rule, không thấy brainstorming/hypothesis stage. | Thiếu test idea/risk hypothesis generation như tester senior. |
| `test-strategy-planner` | Một phần | Có Test Plan generation và route planning, nhưng không có dynamic planning loop. | Planning hiện nghiêng về artifact generation và route mapping. |
| `learning/reflection loop` | Một phần | Có retry/review gates, không thấy feedback-to-memory update. | Hệ thống chưa học từ lỗi review/execution qua nhiều run. |

## 5.2 Existing strengths to preserve

| Strength | Evidence | Vì sao cần giữ |
|---|---|---|
| Prompt-compatible runtime discipline | `agents/delivery-orchestrator/AGENT.md:12-16` | Giữ hành vi tương thích prompt gốc, tránh freeform drift. |
| Contract/validator layer | `workflow-packs/default/workflow.yml:796-824` | Bảo đảm output có kiểm chứng deterministic. |
| Source fidelity / open questions | `agents/knowledge-retriever/AGENT.md:22-28`, `agents/spec-ui-locator/AGENT.md:39-43` | Giảm hallucination, giữ traceability. |
| Senior-QC review rubric | `agents/output-reviewer/AGENT.md:31-53` | Đẩy chất lượng output vượt format validation. |
| Output generation coverage | `workflow-packs/default/workflow.yml:104-569` | Đây là nền output layer đã tương đối đầy đủ. |

---

## 6. Final maturity verdict

| Dimension | Verdict |
|---|---|
| Repo có phải chỉ là input cụ thể → output cụ thể không? | Không hoàn toàn. Repo đã có orchestration, knowledge setup, standards, validators, review gates và traceability. |
| Repo đã là AI tester giống con người đầy đủ chưa? | Chưa. Repo thiếu living memory, cognitive skill taxonomy, skimming/breakdown skills độc lập, brainstorming, dynamic planning loop, persistent learning/reflection. |
| Repo hiện đúng nhất nên gọi là gì? | **Hybrid prompt-compatible QA orchestration/artifact system**. |
| Nền tảng nào đã đủ mạnh? | Output generation, contract validation, review/approval, traceability, senior-QC guardrails. |
| Nền tảng nào cần nâng cấp? | Tester cognition layer: collect → skim → break down → cook knowledge → brainstorm → plan → generate → reflect → update memory. |

---

## 7. Target architecture recommendation

Kiến trúc nâng cấp nên chuyển từ “route-to-output” sang “tester cognition first, output second”:

```text
Tester Knowledge Layer
  -> collect sources
  -> source registry
  -> canonical/redacted knowledge
  -> tester memory

Tester Understanding Layer
  -> skim documents
  -> segment/break down modules, APIs, UI flows, rules
  -> extract facts
  -> detect ambiguity/conflict/gap

Tester Reasoning Layer
  -> derive business rules
  -> brainstorm risks and defect hypotheses
  -> build coverage hypotheses
  -> define test strategy

Tester Planning Layer
  -> decide route
  -> ask missing questions
  -> define artifact plan
  -> define coverage model before generation

Tester Output Layer
  -> existing Test Plan / TD / TC / Matrix / Execution / Dashboard / Automation skills

Tester Reflection Layer
  -> validators
  -> output review
  -> supervisor approval
  -> execution feedback
  -> update knowledge/memory
```

---

## 8. Roadmap nâng cấp

### Phase 1: Cognitive skill taxonomy

Tạo registry phân loại skill theo:

- knowledge setup
- knowledge cooking
- input understanding
- reasoning
- planning
- output generation
- reflection

### Phase 2: Knowledge setup/cooking expansion

Thêm hoặc tách skill:

- `knowledge-collector`
- `tester-memory-manager`
- `business-rule-extractor`
- `risk-model-builder`
- `coverage-model-builder`

### Phase 3: Input understanding skills

Thêm skill:

- `document-skimmer`
- `document-breakdown`
- `api-spec-analyzer`
- `ui-flow-analyzer`
- `ambiguity-conflict-detector`

### Phase 4: Tester reasoning skills

Thêm skill:

- `risk-brainstormer`
- `defect-hypothesis-generator`
- `test-strategy-planner`
- `coverage-hypothesis-planner`

### Phase 5: Wire existing output skills behind cognition flow

Luồng mới:

```text
collect knowledge
-> skim/break/analyze
-> cook rule/risk/coverage model
-> brainstorm/planning
-> then generate Test Plan / TD / TC / Matrix / Execution / Dashboard
```

Không gọi trực tiếp output route khi chưa có cognition artifacts.

### Phase 6: Reflection and learning loop

Thêm:

- feedback-to-knowledge update
- recurring defect pattern memory
- rejected-output lesson log
- execution-result learning
- evaluator tests cho “tester-like behavior”

---

## 9. Implementation recommendation

Không nên bỏ kiến trúc hiện tại. Nên giữ `workflow-packs/default/`, agents output hiện có, validators và review gates. Việc cần làm là thêm một tầng cognition phía trước output generation:

```text
Current system:
source / prompt -> route -> generate artifact -> validate/review

Recommended system:
source / prompt
-> tester knowledge setup
-> tester input understanding
-> tester reasoning + planning
-> output generation
-> validate/review/reflect
-> update tester memory
```

Kết luận cuối cùng: repo hiện tại **đủ mạnh làm QA artifact orchestration engine**, nhưng **chưa đủ để gọi là một AI tester giống con người đầy đủ**. Để đạt yêu cầu của sếp, cần bổ sung các cognition skills và memory/reflection layer trước khi gọi các output-generation skills hiện có.
