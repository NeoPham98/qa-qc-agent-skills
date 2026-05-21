# AI Tester Intermediate Artifacts

## 1. Purpose

This document defines the cognition artifacts that must exist before final QA outputs are generated. These artifacts make the AI tester workflow evidence-based: the system reads, understands, cooks knowledge, reasons, plans, generates output, then learns from review and execution.

## 2. Global artifact rules

Every cognition artifact must include:

- `Artifact ID`
- `Project`
- `Squad`
- `Epic`
- `Source Refs`
- `Created By`
- `Created At`
- `Confidence`
- `Open Questions`

Every source-backed claim must include one of:

- source manifest id
- normalized knowledge id
- current run file/page/sheet/section reference
- explicit `[PENDING_DOC:<fact>]` marker

Forbidden across all cognition artifacts:

- inventing missing business facts
- hiding ambiguity
- using raw secrets or unredacted runtime sources
- converting hypotheses into confirmed rules
- generating final testcase rows before planning artifacts exist

## 3. Knowledge artifacts

## 3.1 `SourceInventory.md/json`

### Purpose

List all sources and classify their role before understanding or generation.

### Required fields

| Field | Description |
|---|---|
| `Source ID` | Stable source identifier for the run. |
| `Source Kind` | API spec, UI spec, URD, RSD, PTTK, testcase, execution, dashboard, knowledge, prompt, other. |
| `Original Locator` | User-provided path/link/name. |
| `Runtime Locator` | Local/redacted/normalized runtime path when available. |
| `Canonical Status` | canonical, reference-only, legacy, unknown. |
| `Redaction Status` | redacted, unredacted, not-required, unknown. |
| `Candidate Roles` | Possible roles for routing. |
| `Detected Hints` | Headers, keywords, domain hints. |
| `Missing Metadata` | Required metadata not present. |

### Downstream consumers

- `KnowledgeMap`
- `CanonicalContextPackage`
- `DocumentMap`

## 3.2 `KnowledgeMap.md/json`

### Purpose

Map available knowledge by project, squad, epic, domain, module, feature, source type, and confidence.

### Required sections

- Project/domain map
- Module/feature map
- Available source coverage
- Missing knowledge areas
- Reusable memory references
- Source quality summary

### Downstream consumers

- `CanonicalContextPackage`
- `TesterMemory`
- `BusinessRuleModel`

## 3.3 `CanonicalContextPackage.md`

### Purpose

Provide the safe, minimal, traceable context package for cognition and output routes.

### Required sections

- Selected route or purpose
- Included source refs
- Excluded source refs and reason
- Redaction warnings
- Context facts
- Open questions
- Usage constraints

### Downstream consumers

- `DocumentMap`
- `FactInventory`
- output generation skills

## 3.4 `TesterMemory.md/json`

### Purpose

Store reusable tester knowledge by approved domain, module, rule, risk, defect pattern, and lesson.

### Required sections

- Domain memory
- Business rule memory
- Risk memory
- Defect pattern memory references
- Historical open questions
- Approved lessons
- Validity scope

### Downstream consumers

- `RiskModel`
- `DefectHypothesis`
- `TesterStrategyPlan`

## 3.5 `MissingInputList.md`

### Purpose

Track missing input before any artifact generation.

### Required fields

| Field | Description |
|---|---|
| `Missing Item` | Source, metadata, business rule, environment, data, role, or decision missing. |
| `Impact` | Which downstream artifact is affected. |
| `Severity` | blocker, major, minor. |
| `Owner` | BA, PO, Dev, QC, user, unknown. |
| `Question` | Clarification question to ask. |

## 4. Understanding artifacts

## 4.1 `DocumentMap.md`

### Purpose

Represent the structure of input documents after skimming.

### Required sections

- Source overview
- Section/table/API/screen index
- Important facts found
- Candidate business rules
- Candidate flows
- Candidate test-relevant areas
- Ambiguity/gap pointers

### Pass criteria

A reviewer can understand where important facts are located without rereading the full raw source.

## 4.2 `SourceBreakdown.md`

### Purpose

Break source content into testable units.

### Required fields

| Field | Description |
|---|---|
| `Unit ID` | Feature, flow, endpoint, field, rule, state, or integration unit. |
| `Unit Type` | api_operation, ui_flow, field, business_rule, state, permission, integration, data. |
| `Description` | Source-backed description. |
| `Source Ref` | Trace reference. |
| `Dependencies` | Related units. |
| `Testability` | testable, partially-testable, blocked. |
| `Notes` | Gaps or ambiguity. |

## 4.3 `FactInventory.md`

### Purpose

List confirmed facts before rules or plans are created.

### Required fields

| Field | Description |
|---|---|
| `Fact ID` | Stable fact id. |
| `Fact Type` | endpoint, method, header, request_field, response_field, ui_field, rule, state, permission, error, data. |
| `Fact` | Confirmed fact statement. |
| `Source Ref` | Source reference. |
| `Confidence` | high, medium, low. |
| `Impacted Artifact` | BusinessRuleModel, RiskModel, CoveragePlan, TestDesign, TestCase. |

## 4.4 `RuleInventory.md`

### Purpose

Capture raw candidate rules before they are cooked into a business model.

### Required fields

| Field | Description |
|---|---|
| `Raw Rule ID` | Candidate rule id. |
| `Raw Rule Text` | Rule as found in source. |
| `Source Ref` | Source reference. |
| `Parsed Condition` | Condition if available. |
| `Parsed Outcome` | Outcome if available. |
| `Gap` | Missing condition/outcome/exception/source. |

## 4.5 `OpenQuestions.md`

### Purpose

Make uncertainty visible instead of inventing facts.

### Required fields

| Field | Description |
|---|---|
| `Question ID` | Stable id. |
| `Question` | Clear question. |
| `Reason` | Missing, ambiguous, conflicting, untestable, stale. |
| `Source Ref` | Related source. |
| `Impacted Artifact` | Artifact blocked or degraded. |
| `Severity` | blocker, major, minor. |
| `Owner` | Expected answer owner. |

## 4.6 `GapAnalysis.md`

### Purpose

Record source gaps, contradictions, and untestable requirements.

### Required sections

- Missing facts
- Ambiguous statements
- Conflicting source statements
- Untestable requirements
- Impacted coverage
- Recommended next action

## 5. Cooking artifacts

## 5.1 `BusinessRuleModel.md/json`

### Purpose

Represent source-backed business rules in testable form.

### Required fields

| Field | Description |
|---|---|
| `Rule ID` | Stable business rule id. |
| `Condition` | Trigger or precondition. |
| `Action` | System/process action. |
| `Expected Outcome` | Expected result. |
| `Exception` | Exception path if any. |
| `Source Ref` | Trace reference. |
| `Confidence` | high, medium, low. |
| `Open Question Ref` | Link when incomplete. |

## 5.2 `DomainKnowledgeModel.md/json`

### Purpose

Represent domain entities, actors, states, transitions, and dependencies.

### Required sections

- Entities and fields
- Actors and permissions
- States and transitions
- External dependencies
- Data constraints
- Rule relationships

## 5.3 `CoverageModel.md/json`

### Purpose

Define coverage obligations before planning.

### Required fields

| Field | Description |
|---|---|
| `Coverage Item ID` | Stable coverage id. |
| `Coverage Type` | happy, negative, boundary, exception, error, permission, state, business, cross-logic, regression. |
| `Source Basis` | Rule/fact/risk/source ref. |
| `Required` | yes/no and reason. |
| `Priority` | high, medium, low. |
| `Notes` | Special test notes. |

## 5.4 `ReusableKnowledgeBase.md/json`

### Purpose

Store approved cooked knowledge for reuse.

### Required sections

- Reusable rules
- Reusable domain model parts
- Reusable risk patterns
- Reusable coverage obligations
- Validity scope
- Approval record

## 6. Reasoning artifacts

## 6.1 `RiskModel.md`

### Purpose

Represent test risks before test strategy and output generation.

### Required fields

| Field | Description |
|---|---|
| `Risk ID` | Stable id. |
| `Risk Category` | business, API, UI, data, security, permission, state, integration, regression, operational. |
| `Cause` | Why risk exists. |
| `Impact` | Impact if defect occurs. |
| `Evidence` | Source/rule/memory reference. |
| `Priority` | high, medium, low. |
| `Mitigation` | Planned test mitigation. |

## 6.2 `DefectHypothesis.md`

### Purpose

Describe likely defects to guide coverage.

### Required fields

| Field | Description |
|---|---|
| `Hypothesis ID` | Stable id. |
| `Hypothesis` | Possible defect statement. |
| `Why Plausible` | Rationale. |
| `Evidence` | Risk/rule/memory reference. |
| `Suggested Coverage` | Coverage idea or test data. |
| `Status` | hypothesis, validated, rejected. |

## 6.3 `EdgeCaseList.md`

### Purpose

List edge cases before they become test cases.

### Required fields

| Field | Description |
|---|---|
| `Edge Case ID` | Stable id. |
| `Category` | boundary, negative, state, timing, permission, cross-rule, data, integration. |
| `Description` | Edge condition. |
| `Source/Risk Basis` | Trace reference. |
| `Expected Behavior Known` | yes/no. |
| `Open Question Ref` | If unknown. |

## 6.4 `CoverageIdeaList.md`

### Purpose

Convert reasoning into coverage candidates for planning.

### Required fields

| Field | Description |
|---|---|
| `Idea ID` | Stable id. |
| `Idea` | Coverage idea. |
| `Basis` | Rule/risk/hypothesis/edge case. |
| `Priority` | high, medium, low. |
| `Recommended Artifact` | TestPlan, TestDesign, TestCase, Automation, Dashboard. |

## 7. Planning artifacts

## 7.1 `TesterStrategyPlan.md`

### Purpose

Define how the AI tester will test before generating outputs.

### Required sections

- Scope and assumptions
- Source baseline
- Strategy by risk
- Test levels and artifact sequence
- Blocker questions
- Coverage priorities
- Output generation plan
- Review expectations

## 7.2 `CoveragePlan.md`

### Purpose

Commit to required coverage before Test Design/Test Case generation.

### Required fields

| Field | Description |
|---|---|
| `Coverage Plan ID` | Stable id. |
| `Coverage Item Ref` | Link to `CoverageModel`. |
| `Planned Artifact` | TD, TC, UAT, automation, dashboard. |
| `Priority` | high, medium, low. |
| `Must Generate` | yes/no. |
| `Rationale` | Why included/excluded. |

## 7.3 `TestDataPlan.md`

### Purpose

Define data strategy before testcase generation.

### Required sections

- Valid data classes
- Invalid data classes
- Boundary values
- Role/permission data
- State transition data
- Integration data
- Data constraints and pending data

## 7.4 `QuestionBacklog.md`

### Purpose

Organize questions and decide whether generation can proceed.

### Required fields

| Field | Description |
|---|---|
| `Question ID` | Link to `OpenQuestions`. |
| `Blocker` | yes/no. |
| `Impacted Output` | TestPlan, TD, TC, automation, dashboard. |
| `Decision Needed` | What must be answered. |
| `Proceed Rule` | proceed, proceed-with-pending-marker, stop. |

## 7.5 `ArtifactPlan.md`

### Purpose

Define output artifacts and sequence.

### Required fields

| Field | Description |
|---|---|
| `Artifact` | Output artifact name. |
| `Upstream Required` | Required cognition artifacts. |
| `Generator` | Existing output skill/agent. |
| `Validators` | Required validators or review gates. |
| `Order` | Generation order. |

## 8. Reflection artifacts

## 8.1 `ReviewFindings.md`

### Purpose

Normalize validator, reviewer, and supervisor findings.

### Required fields

| Field | Description |
|---|---|
| `Finding ID` | Stable id. |
| `Source` | validator, output reviewer, supervisor, execution. |
| `Severity` | blocker, major, minor. |
| `Finding` | Clear issue. |
| `Impacted Artifact` | Artifact affected. |
| `Required Action` | Fix, ask, update memory, reject. |

## 8.2 `LessonsLearned.md`

### Purpose

Extract approved lessons from review/execution.

### Required sections

- What failed
- Why it failed
- What should change next run
- Applicable scope
- Approval status

## 8.3 `DefectPatternMemory.md`

### Purpose

Persist recurring defect and review patterns.

### Required fields

| Field | Description |
|---|---|
| `Pattern ID` | Stable id. |
| `Pattern` | Defect/review/execution pattern. |
| `Scope` | Domain/module/artifact applicability. |
| `Evidence` | Approved finding/lesson reference. |
| `Recommended Future Check` | How future runs should use it. |

## 8.4 `MemoryUpdate.md`

### Purpose

Represent an approved memory patch.

### Required fields

| Field | Description |
|---|---|
| `Update ID` | Stable id. |
| `Target Memory` | TesterMemory section to update. |
| `Change Type` | add, update, deprecate. |
| `Content` | Memory patch. |
| `Evidence` | Lesson/finding/source reference. |
| `Approval` | Required approval record. |

## 9. Minimum route gate

A cognition-first output route must satisfy this gate before calling final output skills:

```text
SourceInventory
+ DocumentMap
+ FactInventory
+ BusinessRuleModel or explicit OpenQuestions
+ RiskModel
+ CoveragePlan
+ TesterStrategyPlan
+ QuestionBacklog
```

If blocker questions exist, the route must stop or proceed only with explicit pending markers and reviewer-visible limitations.
