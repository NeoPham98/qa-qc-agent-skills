# Source Document Standard

## Purpose

This standard defines how source materials are identified, classified, traced, and prepared before any analysis, planning, design, or testcase generation.

## Non-skip rule

No downstream artifact may be created unless source materials were first inventoried, classified, and traced.

Required order:

```text
Project -> Squad -> Epic -> Source Inventory -> Source Classification -> Source Analysis -> downstream QA artifacts
```

## Supported source kinds

Accepted source kinds include:

- BRD
- URD
- RSD
- PTTK
- API detail/spec
- UI flow/wireframe/screen spec
- business rule table
- workbook/sheet
- prompt asset
- template
- golden example
- normalized knowledge
- execution workbook
- dashboard workbook

## Mandatory source fields

Each source entry must include at least:

| Field | Required | Notes |
|---|---:|---|
| Source ID | Yes | Stable identifier such as `SRC-API-001`. |
| Project | Yes | Project or program name. |
| Squad | Yes | Owning squad or workstream. |
| Epic / Module | Yes | Epic, module, or trunk. |
| Source Kind | Yes | One of the supported source kinds. |
| Title | Yes | Human-readable title. |
| Source Ref | Yes | Section/page/sheet/anchor used for traceability. |
| Classification | Yes | `authoritative`, `supporting`, `reference_only`, or `derived`. |
| Sensitivity | Yes | `public`, `internal`, `restricted`, or `secret`. |
| Runtime Eligibility | Yes | `allowed`, `redacted_only`, or `not_allowed`. |
| Owner | No | Document owner or accountable team. |
| Open Questions | No | Missing facts requiring clarification. |

## Classification rules

- `authoritative`: source of truth for business behavior, contract, or UI behavior.
- `supporting`: useful context but not final authority.
- `reference_only`: sample or historical material that must not override current evidence.
- `derived`: artifact produced from other sources and traceable back to them.

## Runtime usage rules

- Raw bootstrap folders are provenance only and must not become runtime dependencies.
- Sensitive raw materials must be redacted before runtime retrieval.
- Source refs must point to a stable source section, page, or sheet.
- If two sources conflict, record the conflict explicitly and mark open questions instead of choosing silently.

## Source analysis obligations

Before Test Plan or Test Design begins, source analysis must:

1. group evidence by Project, Squad, and Epic/Module,
2. split modules into business operations or UI/API surfaces,
3. identify business rules, validation rules, dependencies, and missing facts,
4. record `[PENDING_DOC:<fact>]` or open questions where evidence is missing.

## Forbidden behavior

- Do not skip source inventory.
- Do not infer missing business rules from naming conventions.
- Do not treat prompts as business truth unless they cite authoritative source evidence.
- Do not use raw sensitive assets directly at runtime.
