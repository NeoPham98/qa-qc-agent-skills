---
name: secret-redactor
description: Redacts credentials, tokens, cookies, and internal endpoints from normalized BIDV knowledge before runtime use.
role_affinity: [security_reviewer, knowledge_engineer]
domain: [bidv, security, redaction]
lifecycle_stage: [bootstrap]
produces: [redacted_knowledge, redaction_report]
consumes: [normalized_knowledge]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Secret Redactor

## Operating mode

Use this skill after `doc-normalizer` and before any runtime agent retrieves BIDV knowledge.

## Required inputs

- Normalized knowledge folder, normally `knowledge/default/normalized/`.
- Redacted output folder, normally `knowledge/default/redacted/`.
- Redaction report path, normally `knowledge/default/manifests/redaction-report.yml`.

## Workflow

Run:

```bash
python scripts/redact_secrets.py --input knowledge/default/normalized --output knowledge/default/redacted --report knowledge/default/manifests/redaction-report.yml
```

The redactor masks:

- Bearer tokens and long token-like values.
- Password, DB user, API key, TestLink key assignments.
- Cookies and Set-Cookie headers.
- Internal URLs, hostnames, JDBC URLs, and private IP addresses.

## Output requirements

- Preserve folder structure from normalized knowledge.
- Update Markdown metadata from `redaction_status: unredacted` to `redaction_status: redacted`.
- Generate a report with source path, redaction type, and count.

## Guardrails

- Runtime agents must prefer `knowledge/default/redacted/`.
- Never publish raw `Prompt/API/Gen Script/properties.txt` content.
- If a secret pattern remains after redaction, block runtime handoff and report the file path.
