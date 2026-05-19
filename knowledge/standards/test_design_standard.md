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

## Standard & Language Compliance
- **Default Language**: Vietnamese (`Tiếng Việt`) must be used for all test design nodes, steps, and expected results.
- **Control Parameters**: Every API Test Design document must contain the exact parameter list: `METHOD_CHECK`, `CONTENT_TYPE_CHECK`, `MANDATORY_CHECK`, `TYPE_CHECK`, `LENGTH_CHECK`, `SCOPE_FIELDS`, `EG_CHECK`.
- **Exact Section Headings**: API Test Design sections must use these exact headings:
  - `## Method & Header` (under which only `TD_P1_*` nodes reside)
  - `## Schema Validation` (under which only `TD_P2_*` nodes reside)
  - `## Value, Business Logic, Cross Logic` (under which only `TD_P3_*` nodes reside)
- **Preceding Endpoint Headings**: Every `TD_P*` node must be preceded by an HTTP method and endpoint heading (e.g. `### POST /v1/customer/validate`) within 3000 characters of text. Add these subheadings at the start of each section.
- **Forbidden Phrases**: Vague phrases such as `verify api works`, `validate invalid input`, `check response is correct`, `valid data`, `invalid data`, `data hợp lệ`, `data không hợp lệ`, `kiểm tra dữ liệu không hợp lệ`, `kiểm tra dữ liệu hợp lệ`, `như trên`, `tương tự` are strictly forbidden.
- **Specificity rules**:
  - `TD_P1` nodes must name the exact method/path/header/auth target under test.
  - `TD_P2` nodes must name the exact request/response field, schema rule, type, format, enum, null/empty, or boundary target.
  - `TD_P3` nodes must name the exact business rule, state transition, flow dependency, or error code/message.

