# Manual Execution Status Standard

## Purpose

This standard defines the lifecycle and normalization rules for manual execution and status reporting.

## Workflow position

Manual execution is a downstream activity after testcase preparation. Dashboard and status summaries depend on execution evidence.

Required order:

```text
Validated testcase workbook -> manual execution -> execution import -> dashboard/status artifacts
```

## Core statuses

Normalized execution lifecycle should use supported statuses such as:

- Not Run
- In Progress
- Passed
- Failed
- Blocked
- Retest

## Required execution fields

Execution artifacts should preserve or map:

- Test Case ID,
- execution status,
- actual result,
- evidence or note,
- BugID when applicable,
- execution round when applicable.

## Quality rules

- Preserve testcase identity from the testcase artifact.
- Normalize status aliases before dashboard reporting.
- Unknown statuses must be flagged, not silently remapped.
- Execution data must not erase source testcase traceability.

## Governance rules

- Import and normalization are allowed.
- Writing back to source workbooks or external systems requires explicit user approval.
- Dashboard generation must reflect execution evidence, not inferred progress.

## Forbidden behavior

- Do not overwrite the original execution workbook without approval.
- Do not invent pass/fail results.
- Do not treat dashboard summaries as substitutes for execution evidence.
