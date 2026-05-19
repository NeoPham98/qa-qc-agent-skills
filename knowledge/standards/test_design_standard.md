# Test Design Standard

## Purpose

This standard defines how Test Design artifacts are created from Test Plan and source evidence for API, UI, and UAT flows.

## Non-skip rule

Test Design may be created only after Source Inventory, Source Analysis, and Test Plan are available.

Required order:

```text
Source Inventory -> Source Analysis -> Test Plan -> Test Design
```

## Test Design obligations

Each Test Design node must represent a specific condition, rule, or behavior and remain traceable to source evidence.

Each node should identify, when applicable:

- module / epic / flow,
- business operation,
- API endpoint or UI screen/control,
- field or rule,
- precondition,
- test technique,
- expected behavior,
- source ref,
- open question or gap if evidence is incomplete.

## Required fields

| Field | Required | Notes |
|---|---:|---|
| TD ID | Yes | Stable identifier such as `TD-API-001`. |
| Project / Squad / Epic | Yes | Workflow anchor metadata. |
| Source Ref | Yes | Exact section/page/sheet/anchor reference. |
| Target | Yes | Endpoint, screen, control, state, field, or business rule. |
| Technique | Yes | `ECP`, `BVA`, `DT`, `ST`, `EG`, `schema`, `contract`, or equivalent supported technique. |
| Preconditions | No | Required setup when evidence supports it. |
| Expected Behavior | Yes | Concrete and testable. |
| Gap / Open Question | No | Required when behavior is not fully documented. |

## API-specific rules

API design should preserve staged analysis:

- method/header validation,
- schema validation,
- value/business/cross logic.

API Test Design must not collapse all checks into broad summary rows when field/rule expansion is possible.

## UI-specific rules

UI design must name the flow, screen, control, state, role, and validation/message evidence when available.

## Quality rules

- Happy path is required but never sufficient alone.
- Expand into concrete rules when field, state, role, or business evidence exists.
- Missing facts must become `open_question`, `gap`, or `[PENDING_DOC:<fact>]`.
- Test Design is the upstream source for matrix and testcase generation; it must be dense enough to support that handoff.

## Forbidden behavior

- Do not create testcase rows directly in Test Design.
- Do not invent controls, states, messages, or error codes.
- Do not skip source refs.
- Do not hand off to testcase generation without matrix preparation in applicable routes.
