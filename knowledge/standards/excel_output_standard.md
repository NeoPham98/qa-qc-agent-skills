# Excel Output Standard

## Purpose

This standard defines how user-facing workbook outputs should be packaged after deterministic validation artifacts are prepared.

## Output rule

TSV or equivalent deterministic text artifact is the validation baseline. XLSX is the formatted handoff artifact for human users.

Required order:

```text
Validated source artifact -> deterministic TSV -> formatted XLSX
```

## Workbook expectations

Final Excel outputs should include, when applicable:

- correct sheet name and header row,
- preserved column order from the governing contract,
- autofilter,
- frozen header row,
- readable column widths,
- wrapped text for long steps and expected results,
- row counts consistent with the deterministic source artifact.

## Supported workbook families

- Test Plan workbook
- Test Design workbook
- Legacy 19-column testcase workbook
- UAT testcase workbook
- execution/status workbook
- dashboard workbook

## Quality rules

- XLSX must not silently diverge from validated TSV content.
- Human-facing formatting must not alter business meaning.
- Workbook formatting should support manual QC review and execution.
- Headers must remain exact when governed by an output contract.

## Forbidden behavior

- Do not use XLSX as the only source of truth for validation.
- Do not publish a workbook that has not passed its contract validator.
- Do not change column semantics to imitate a legacy sample if it breaks the current contract.
