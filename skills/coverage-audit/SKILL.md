---
name: coverage-audit
description: Audits coverage and traceability for BIDV prompt-compatible artifacts.
role_affinity: [qa_lead, tester]
domain: [coverage, traceability, bidv]
lifecycle_stage: [coverage_audit]
produces: [md, coverage_matrix]
consumes: [requirement_inventory, test_design, testcase, test_execution]
maturity: draft
tier: 2
languages: [vi, en]
---

# BIDV Coverage Audit

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. It audits reviewed prompt-compatible artifacts and does not generate native/freeform testcase content.

## Selection criteria

Use this skill when coverage, traceability, or gap audit is requested.

## Required inputs

- Requirement/Test Design/TestCase/TestExecution artifacts as applicable.
- Source docs and selected runtime prompt paths used upstream.
- Expected coverage output format.

## Workflow

1. Receive coverage route from orchestrator.
2. Verify available upstream artifacts.
3. Map requirements, TD IDs, TC IDs, execution IDs, and gaps.
4. Generate Coverage Matrix Markdown.
5. Send output to review.

## Outputs

- Coverage Matrix Markdown.
- Coverage gap summary.

## Review gates

- Traceability chain is explicit.
- Missing coverage is reported, not hidden.
- Source/prompt lineage is preserved.
