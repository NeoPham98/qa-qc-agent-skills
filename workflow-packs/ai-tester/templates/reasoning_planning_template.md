# Reasoning and Planning Artifacts Template

## DefectHypothesis

| Hypothesis ID | Hypothesis | Why Plausible | Evidence | Suggested Coverage | Status |
|---|---|---|---|---|---|
| `<id>` | `<hypothesis>` | `<reason>` | `<risk/rule/memory>` | `<coverage>` | `<hypothesis|validated|rejected>` |

## EdgeCaseList

| Edge Case ID | Category | Description | Source/Risk Basis | Expected Behavior Known | Open Question Ref |
|---|---|---|---|---|---|
| `<id>` | `<boundary|negative|state|timing|permission|cross-rule|data|integration>` | `<description>` | `<basis>` | `<yes|no>` | `<question-ref>` |

## CoverageIdeaList

| Idea ID | Idea | Basis | Priority | Recommended Artifact |
|---|---|---|---|---|
| `<id>` | `<idea>` | `<rule/risk/hypothesis/edge>` | `<high|medium|low>` | `<artifact>` |

## TesterStrategyPlan

### Scope and assumptions

- Scope In: `<scope>`
- Scope Out: `<scope>`
- Assumptions: `<assumptions>`
- Blockers: `<blockers>`

### Strategy by risk

| Risk ID | Strategy | Test Level | Priority | Required Output |
|---|---|---|---|---|
| `<risk>` | `<strategy>` | `<api|ui|uat|regression|automation>` | `<priority>` | `<output>` |

### Output generation plan

| Order | Artifact | Upstream Required | Generator | Validators |
|---|---|---|---|---|
| `<n>` | `<artifact>` | `<upstream>` | `<skill/agent>` | `<validators>` |

## CoveragePlan

| Coverage Plan ID | Coverage Item Ref | Planned Artifact | Priority | Must Generate | Rationale |
|---|---|---|---|---|---|
| `<id>` | `<coverage-ref>` | `<artifact>` | `<priority>` | `<yes|no>` | `<rationale>` |

## TestDataPlan

| Data Class ID | Data Class | Validity | Boundary/Role/State | Source Basis | Notes |
|---|---|---|---|---|---|
| `<id>` | `<class>` | `<valid|invalid|boundary>` | `<constraint>` | `<source>` | `<notes>` |

## QuestionBacklog

| Question ID | Blocker | Impacted Output | Decision Needed | Proceed Rule | Owner |
|---|---|---|---|---|---|
| `<id>` | `<yes|no>` | `<output>` | `<decision>` | `<stop|proceed-with-pending-marker|proceed>` | `<owner>` |
