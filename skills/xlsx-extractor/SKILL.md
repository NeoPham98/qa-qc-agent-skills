---
name: xlsx-extractor
description: Extracts BIDV workbook profiles for testcase contracts, Paygates tracker sheets, headers, aliases, statuses, formulas, and overflow columns.
role_affinity: [qa_lead, data_engineer]
domain: [bidv, xlsx, contracts]
lifecycle_stage: [bootstrap]
produces: [xlsx_profile, schema]
consumes: [xlsx_sources]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV XLSX Extractor

## Operating mode

Use this skill during BIDV knowledge/bootstrap analysis to derive workbook contracts from real BIDV samples without modifying the source workbooks.

## Required inputs

- BIDV source root containing `.xlsx` files.
- Output schema path, normally `knowledge/default/schemas/xlsx-profiles.yml`.

## Workflow

Run:

```bash
python scripts/extract_xlsx_profiles.py --source ../BIDV --output knowledge/default/schemas/xlsx-profiles.yml
```

The extractor records:

- Sheet names and row/column counts.
- Raw and normalized headers.
- Header aliases observed in testcase workbooks.
- Test Case ID trim/pattern findings.
- Status aliases from Paygates tracker samples.
- Formulas and known suspicious cross-sheet formula patterns.
- Overflow columns beyond the 19-column testcase contract.

## Guardrails

- Do not write back to BIDV source workbooks.
- Treat overflow columns as findings; do not silently trust them as contract changes.
- Report suspicious formulas first. Do not auto-fix tracker formulas without explicit approval.
