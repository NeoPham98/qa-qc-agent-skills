# Cooking Artifacts Template

## BusinessRuleModel

### Metadata

- Artifact ID: `<id>`
- Project: `<project>`
- Squad: `<squad>`
- Epic: `<epic>`
- Created By: `business-rule-extractor`
- Created At: `<timestamp>`
- Source Refs: `<refs>`
- Confidence: `<high|medium|low>`

### Rules

| Rule ID | Condition | Action | Expected Outcome | Exception | Source Ref | Confidence | Open Question Ref |
|---|---|---|---|---|---|---|---|
| `<id>` | `<condition>` | `<action>` | `<outcome>` | `<exception>` | `<ref>` | `<confidence>` | `<question-ref>` |

## DomainKnowledgeModel

### Entities

| Entity ID | Entity | Fields | Source Ref | Notes |
|---|---|---|---|---|
| `<id>` | `<entity>` | `<fields>` | `<ref>` | `<notes>` |

### Actors and permissions

| Actor ID | Actor | Permission/Role | Allowed Actions | Source Ref |
|---|---|---|---|---|
| `<id>` | `<actor>` | `<role>` | `<actions>` | `<ref>` |

### States and transitions

| State ID | From State | Event | To State | Rules | Source Ref |
|---|---|---|---|---|---|
| `<id>` | `<from>` | `<event>` | `<to>` | `<rules>` | `<ref>` |

## CoverageModel

| Coverage Item ID | Coverage Type | Source Basis | Required | Priority | Notes |
|---|---|---|---|---|---|
| `<id>` | `<happy|negative|boundary|exception|error|permission|state|business|cross-logic|regression>` | `<rule/fact/risk/ref>` | `<yes|no>` | `<high|medium|low>` | `<notes>` |

## RiskModel

| Risk ID | Risk Category | Cause | Impact | Evidence | Priority | Mitigation |
|---|---|---|---|---|---|---|
| `<id>` | `<category>` | `<cause>` | `<impact>` | `<evidence>` | `<high|medium|low>` | `<mitigation>` |
