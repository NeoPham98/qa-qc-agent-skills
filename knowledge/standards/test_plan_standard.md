# Test Plan Standard

## Purpose

This standard defines the minimum structure and workflow gate for Test Plan artifacts.

## Non-skip rule

A full workflow must produce a Test Plan before any Test Design or testcase generation.

Required order:

```text
Source Inventory -> Source Analysis -> Test Plan -> Test Design -> Matrix -> Test Case
```

## Minimum Test Plan contents

A valid Test Plan must contain:

1. Project / Squad / Epic / Module scope
2. Objective and business context
3. In-scope items
4. Out-of-scope items
5. Test levels and test types
6. Risks and assumptions
7. Environment and dependency needs
8. Entry criteria
9. Exit criteria
10. Test data needs
11. Deliverables
12. Roles / ownership
13. Traceable source references
14. Open questions and gaps

## Mandatory fields

| Field | Required | Notes |
|---|---:|---|
| Project | Yes | Project or program name. |
| Squad | Yes | Owning squad or workstream. |
| Epic / Module | Yes | Epic, module, or trunk scope. |
| Plan ID | Yes | Stable identifier such as `TP-001`. |
| Source Refs | Yes | Traceable references to inventory and analysis evidence. |
| Risks | Yes | Include delivery, business, and dependency risks when evidenced. |
| Entry Criteria | Yes | Conditions to start execution. |
| Exit Criteria | Yes | Conditions to complete the cycle. |
| Owner | Yes | Responsible team or role. |

## Quality rules

- Scope must be concrete and traceable to sources.
- Risks must reflect evidence, not generic filler.
- Out-of-scope must be explicit when partial coverage is intended.
- If business facts are incomplete, record open questions instead of inventing them.
- A Test Plan may summarize planned techniques, but it must not replace Test Design.
- **Language Standard**: For domestic projects (e.g., BIDV, Paygates), all generated artifacts (Test Plan, Test Design, Test Cases, and their Excel sheets) must be written in Vietnamese (Tiếng Việt) to align with source documents.

## Handoff rules

Test Plan handoff to Test Design must include:

- Project / Squad / Epic metadata,
- approved scope boundaries,
- source refs,
- risk areas,
- environment notes,
- open questions.

## Forbidden behavior

- Do not generate testcase rows directly from Test Plan.
- Do not skip source analysis.
- Do not treat a list of modules as a complete Test Plan.
- Do not hide unknowns that affect downstream design.
