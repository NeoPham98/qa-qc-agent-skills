# Cognition Artifact Contract

## Purpose

This contract defines the minimum requirements for AI tester cognition artifacts.

## Applies to

- `SourceInventory.md/json`
- `KnowledgeMap.md/json`
- `CanonicalContextPackage.md`
- `TesterMemory.md/json`
- `MissingInputList.md`
- `DocumentMap.md`
- `SourceBreakdown.md`
- `FactInventory.md`
- `RuleInventory.md`
- `OpenQuestions.md`
- `GapAnalysis.md`
- `BusinessRuleModel.md/json`
- `DomainKnowledgeModel.md/json`
- `CoverageModel.md/json`
- `RiskModel.md`
- `DefectHypothesis.md`
- `EdgeCaseList.md`
- `CoverageIdeaList.md`
- `TesterStrategyPlan.md`
- `CoveragePlan.md`
- `TestDataPlan.md`
- `QuestionBacklog.md`
- `ArtifactPlan.md`
- `ReviewFindings.md`
- `LessonsLearned.md`
- `DefectPatternMemory.md`
- `MemoryUpdate.md`

## Required metadata

Each artifact must include:

- `Artifact ID`
- `Project`
- `Squad`
- `Epic`
- `Source Refs`
- `Created By`
- `Created At`
- `Confidence`
- `Open Questions`

## Source trace rules

Every source-backed claim must include one of:

- source manifest id
- normalized knowledge id
- current run source section/page/sheet reference
- explicit `[PENDING_DOC:<fact>]` marker

## Forbidden behavior

- Do not invent missing facts.
- Do not hide blocker ambiguity.
- Do not expose raw secrets or unredacted runtime sources.
- Do not treat hypotheses as confirmed rules.
- Do not generate final testcase rows from cognition artifacts before planning is complete.

## Review requirements

A reviewer must be able to trace each business rule, risk, coverage item, and plan decision back to source evidence, approved memory, or an explicit pending marker.
