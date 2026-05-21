# Understanding Artifacts Template

## DocumentMap

### Metadata

- Artifact ID: `<id>`
- Project: `<project>`
- Squad: `<squad>`
- Epic: `<epic>`
- Created By: `document-skimmer`
- Created At: `<timestamp>`
- Source Refs: `<refs>`
- Confidence: `<high|medium|low>`

### Document structure

| Source Ref | Section/Table/API/Screen | Location | Test Relevance | Notes |
|---|---|---|---|---|
| `<ref>` | `<item>` | `<location>` | `<high|medium|low>` | `<notes>` |

### Candidate test areas

| Area ID | Area | Type | Source Ref | Why Important |
|---|---|---|---|---|
| `<id>` | `<area>` | `<api|ui|business|data|state|permission>` | `<ref>` | `<reason>` |

## SourceBreakdown

| Unit ID | Unit Type | Description | Source Ref | Dependencies | Testability | Notes |
|---|---|---|---|---|---|---|
| `<id>` | `<type>` | `<description>` | `<ref>` | `<deps>` | `<testable|partially-testable|blocked>` | `<notes>` |

## FactInventory

| Fact ID | Fact Type | Fact | Source Ref | Confidence | Impacted Artifact |
|---|---|---|---|---|---|
| `<id>` | `<type>` | `<fact>` | `<ref>` | `<high|medium|low>` | `<artifact>` |

## RuleInventory

| Raw Rule ID | Raw Rule Text | Source Ref | Parsed Condition | Parsed Outcome | Gap |
|---|---|---|---|---|---|
| `<id>` | `<rule>` | `<ref>` | `<condition>` | `<outcome>` | `<gap>` |

## OpenQuestions

| Question ID | Question | Reason | Source Ref | Impacted Artifact | Severity | Owner |
|---|---|---|---|---|---|---|
| `<id>` | `<question>` | `<missing|ambiguous|conflicting|untestable|stale>` | `<ref>` | `<artifact>` | `<blocker|major|minor>` | `<owner>` |

## GapAnalysis

| Gap ID | Gap Type | Description | Source Ref | Impacted Coverage | Recommended Action |
|---|---|---|---|---|---|
| `<id>` | `<missing|ambiguous|conflicting|untestable>` | `<description>` | `<ref>` | `<coverage>` | `<action>` |
