# Knowledge Artifacts Template

## SourceInventory

### Metadata

- Artifact ID: `<id>`
- Project: `<project>`
- Squad: `<squad>`
- Epic: `<epic>`
- Created By: `knowledge-collector`
- Created At: `<timestamp>`
- Confidence: `<high|medium|low>`

### Sources

| Source ID | Source Kind | Original Locator | Runtime Locator | Canonical Status | Redaction Status | Candidate Roles | Missing Metadata |
|---|---|---|---|---|---|---|---|
| `<source-id>` | `<kind>` | `<locator>` | `<runtime>` | `<canonical|reference-only|legacy|unknown>` | `<redacted|unredacted|not-required|unknown>` | `<roles>` | `<missing>` |

## KnowledgeMap

### Project/domain map

| Domain | Module/Feature | Available Source Refs | Coverage Status | Confidence | Notes |
|---|---|---|---|---|---|
| `<domain>` | `<module>` | `<refs>` | `<complete|partial|missing>` | `<confidence>` | `<notes>` |

### Missing knowledge areas

| Missing Area | Impact | Severity | Owner | Question |
|---|---|---|---|---|
| `<area>` | `<impact>` | `<blocker|major|minor>` | `<owner>` | `<question>` |

## CanonicalContextPackage

### Included source refs

| Source Ref | Reason Included | Usage Scope | Constraints |
|---|---|---|---|
| `<ref>` | `<reason>` | `<scope>` | `<constraints>` |

### Excluded source refs

| Source Ref | Reason Excluded | Follow-up |
|---|---|---|
| `<ref>` | `<reason>` | `<follow-up>` |

### Redaction warnings

| Source Ref | Warning | Required Action |
|---|---|---|
| `<ref>` | `<warning>` | `<action>` |

## MissingInputList

| Missing Item | Impact | Severity | Owner | Question | Proceed Rule |
|---|---|---|---|---|---|
| `<item>` | `<impact>` | `<blocker|major|minor>` | `<owner>` | `<question>` | `<stop|proceed-with-pending-marker|proceed>` |
