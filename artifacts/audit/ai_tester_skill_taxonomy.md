# AI Tester Skill Taxonomy

## 1. Purpose

This taxonomy converts the current QA artifact generator into an AI tester cognition system. The key rule is: output generation skills are not removed, but they must run after knowledge, understanding, cooking, reasoning, and planning artifacts exist.

## 2. Capability map

| Layer | Capability | Current status | Existing reuse | New skill/agent family |
|---|---|---|---|---|
| Tester Knowledge System | Collect, classify, normalize, redact, package, and retrieve knowledge. | Partial | `sdk/source_manifest.py`, `doc-normalizer`, `secret-redactor`, `knowledge-retriever` | knowledge setup |
| Input Understanding System | Skim, break down, analyze, and detect gaps in specific input. | Partial | `spec-ui-locator`, `requirement-coverage-analyst`, `intent_classifier.py` | document understanding |
| Knowledge Cooking System | Convert raw facts into structured business, domain, risk, and coverage models. | Partial | `requirement-coverage-analyst`, `coverage-auditor`, standards/contracts | knowledge cooking |
| Reasoning / Brainstorming System | Think like a senior tester: risks, defect hypotheses, edge cases, coverage ideas. | Missing as explicit layer | senior-QC rules in orchestrator/reviewer/auditor | reasoning and brainstorming |
| Planning System | Decide strategy, coverage, test data, question backlog, and output order. | Partial | `route_planner.py`, `test-plan-generate`, workflow routes | tester planning |
| Output Generation System | Generate Test Plan, Test Design, Test Case, execution, dashboard, automation support. | Strong | existing output skills and agents | existing output generation |
| Reflection / Learning System | Learn from validation, review, execution, and update memory. | Missing as explicit layer | output review, supervisor loop, validators | reflection and memory update |

## 3. Skill taxonomy

## 3.1 Knowledge setup skills

### `knowledge-collector`

- Goal: build a complete source inventory and identify missing source material.
- Inputs: user prompt, source paths, source manifest, canonical source registry.
- Outputs: `SourceInventory`, `MissingInputList`.
- Must not: infer business rules from filenames or folder names.

### `source-quality-analyzer`

- Goal: assess source freshness, completeness, conflicts, redaction state, and traceability readiness.
- Inputs: `SourceInventory`, source metadata, canonical source rules.
- Outputs: `SourceQualityReport`, quality warnings.
- Must not: silently approve incomplete or conflicting sources.

### `context-builder`

- Goal: package source context for downstream cognition and output routes.
- Inputs: `SourceInventory`, `KnowledgeMap`, redacted knowledge, selected route need.
- Outputs: `CanonicalContextPackage`.
- Must not: include unredacted secrets or unrelated source content.

### `tester-memory-manager`

- Goal: retrieve and update tester memory by project, domain, module, rule, risk, defect pattern, and lesson.
- Inputs: `KnowledgeMap`, `MemoryUpdate`, approved lessons.
- Outputs: `TesterMemory`, updated memory patch.
- Must not: treat unapproved reviewer findings as permanent memory.

## 3.2 Input understanding skills

### `document-skimmer`

- Goal: quickly map sections, tables, endpoints, screens, flows, rules, and unknowns.
- Inputs: `CanonicalContextPackage`, source files, source references.
- Outputs: `DocumentMap`.
- Must not: generate test cases.

### `document-breakdown`

- Goal: break documents into feature, flow, operation, rule, field, state, and dependency units.
- Inputs: `DocumentMap`, source references.
- Outputs: `SourceBreakdown`.
- Must not: merge unrelated rules for convenience.

### `api-spec-analyzer`

- Goal: extract endpoint, method, header, auth, request, response, validation, error envelope, and state facts.
- Inputs: API spec source, `SourceBreakdown`.
- Outputs: `FactInventory`, API-specific fact sections.
- Must not: invent status codes, error codes, or response messages.

### `ui-flow-analyzer`

- Goal: extract screen, field, button, navigation, validation, permission, state, and message facts.
- Inputs: UI/RSD/PTTK/URD sources, `SourceBreakdown`.
- Outputs: `FactInventory`, UI-specific fact sections.
- Must not: invent UI behavior not present in source.

### `ambiguity-conflict-detector`

- Goal: detect missing, ambiguous, conflicting, untestable, or stale requirements.
- Inputs: `FactInventory`, `RuleInventory`, source quality findings.
- Outputs: `OpenQuestions`, `GapAnalysis`.
- Must not: resolve ambiguity by guessing.

## 3.3 Knowledge cooking skills

### `business-rule-extractor`

- Goal: transform raw facts into condition/action/outcome/exception/source business rules.
- Inputs: `FactInventory`, `RuleInventory`, `OpenQuestions`.
- Outputs: `BusinessRuleModel`.
- Must not: include rules without source reference or explicit pending marker.

### `domain-model-builder`

- Goal: model domain entities, actors, states, transitions, dependencies, and constraints.
- Inputs: `FactInventory`, `BusinessRuleModel`.
- Outputs: `DomainKnowledgeModel`.
- Must not: mix domain facts from unrelated projects unless memory reuse is approved.

### `coverage-model-builder`

- Goal: derive coverage obligations from rules, risks, source types, states, roles, boundaries, and errors.
- Inputs: `BusinessRuleModel`, `DomainKnowledgeModel`, mandatory coverage rules.
- Outputs: `CoverageModel`.
- Must not: skip negative, boundary, exception, permission, state, or cross-logic coverage when applicable.

### `risk-model-builder`

- Goal: convert source facts, rule complexity, gaps, and historical lessons into risk categories.
- Inputs: `BusinessRuleModel`, `DomainKnowledgeModel`, `TesterMemory`.
- Outputs: `RiskModel`.
- Must not: create risks unrelated to the source scope.

## 3.4 Reasoning / brainstorming skills

### `risk-brainstormer`

- Goal: expand risk thinking across business, API, UI, data, permission, state, integration, and regression dimensions.
- Inputs: `RiskModel`, `CoverageModel`, `TesterMemory`.
- Outputs: enriched `RiskModel`.
- Must not: replace source-backed facts with generic risk lists.

### `defect-hypothesis-generator`

- Goal: propose likely defect hypotheses that should influence coverage and test data.
- Inputs: `RiskModel`, `BusinessRuleModel`, `DefectPatternMemory`.
- Outputs: `DefectHypothesis`.
- Must not: mark hypotheses as confirmed requirements.

### `edge-case-brainstormer`

- Goal: identify edge, boundary, negative, state, timing, permission, and cross-rule cases.
- Inputs: `BusinessRuleModel`, `CoverageModel`, `RiskModel`.
- Outputs: `EdgeCaseList`.
- Must not: generate final testcase rows before planning.

### `coverage-idea-generator`

- Goal: convert reasoning outputs into candidate coverage ideas.
- Inputs: `RiskModel`, `DefectHypothesis`, `EdgeCaseList`.
- Outputs: `CoverageIdeaList`.
- Must not: duplicate ideas without traceable rationale.

## 3.5 Planning skills

### `test-strategy-planner`

- Goal: define scope, priority, test levels, approach, risks, and output route.
- Inputs: `CoverageIdeaList`, `RiskModel`, `BusinessRuleModel`, `OpenQuestions`.
- Outputs: `TesterStrategyPlan`.
- Must not: continue to output generation if blockers require clarification.

### `coverage-planner`

- Goal: define required coverage before Test Design/Test Case generation.
- Inputs: `CoverageModel`, `CoverageIdeaList`, `TesterStrategyPlan`.
- Outputs: `CoveragePlan`.
- Must not: reduce required coverage without explicit rationale.

### `test-data-planner`

- Goal: plan valid, invalid, boundary, role, state, integration, and regression data.
- Inputs: `BusinessRuleModel`, `CoveragePlan`, source constraints.
- Outputs: `TestDataPlan`.
- Must not: include production secrets or unsafe data.

### `question-planner`

- Goal: organize open questions by blocker/non-blocker, owner, impacted artifact, and decision needed.
- Inputs: `OpenQuestions`, `GapAnalysis`, `TesterStrategyPlan`.
- Outputs: `QuestionBacklog`.
- Must not: hide blocker questions to force output generation.

## 3.6 Output generation skills

These are existing skills and remain the final artifact generation layer:

- `test-plan-generate`
- `api-td-generate`
- `ui-td-generate`
- `tc-generate-from-td`
- `uat-tc-generate`
- `test-set-build`
- `test-execution-pack-generate`
- `paygates-dashboard-generate`
- `api-automation-support-generate`

New rule: these skills consume upstream cognition artifacts such as `BusinessRuleModel`, `RiskModel`, `CoveragePlan`, `TesterStrategyPlan`, and `QuestionBacklog`.

## 3.7 Reflection / learning skills

### `reflection-learner`

- Goal: summarize validator, reviewer, supervisor, and execution feedback into lessons.
- Inputs: validation reports, `OutputReview`, `SupervisorApproval`, execution results.
- Outputs: `LessonsLearned`.
- Must not: change approved artifacts directly.

### `feedback-to-knowledge-updater`

- Goal: transform approved lessons into reusable knowledge updates.
- Inputs: `LessonsLearned`, reviewer approval, memory policy.
- Outputs: `MemoryUpdate`.
- Must not: persist unapproved assumptions.

### `defect-pattern-memory-updater`

- Goal: store recurring defect, review, and execution failure patterns for future reasoning.
- Inputs: `LessonsLearned`, defect findings, execution failures.
- Outputs: `DefectPatternMemory`.
- Must not: store sensitive data or customer-specific secrets.

## 4. Handoff order

```text
knowledge setup
-> input understanding
-> knowledge cooking
-> reasoning / brainstorming
-> planning
-> output generation
-> validation / review / approval
-> reflection / learning
-> memory update
```

## 5. Acceptance criteria

- Every generated Test Plan/Test Design/Test Case route has upstream cognition artifacts.
- Missing or ambiguous source facts are visible in `OpenQuestions` or `QuestionBacklog`.
- Output skills are still reused and are not rewritten.
- Review findings can produce `LessonsLearned` and `MemoryUpdate`.
- Future routes can reuse `TesterMemory` and `DefectPatternMemory` without inventing source facts.
