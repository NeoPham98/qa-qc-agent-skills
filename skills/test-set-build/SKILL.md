---
name: test-set-build
description: Builds BIDV Test Set artifacts as an orchestration step from reviewed testcase sources.
role_affinity: [qa_lead, tester]
domain: [test_set, testing, bidv]
lifecycle_stage: [test_execution]
produces: [md, test_set]
consumes: [testcase, source_docs]
maturity: draft
tier: 2
languages: [vi, en]
---

# BIDV Test Set Build

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. It groups reviewed prompt-compatible testcase artifacts; it does not create native/freeform testcase content.

## Selection criteria

Use this skill when testcase artifacts need to be grouped for execution or handoff.

## Required inputs

- Reviewed testcase source.
- Project/Squad/Epic/Test Set scope.
- Execution or release context.

## Workflow

1. Receive reviewed testcase source from orchestrator.
2. Group testcases by selected BIDV handoff criteria.
3. Preserve testcase IDs and traceability.
4. Normalize Test Set Markdown.
5. Send output to review.

## Outputs

- Test Set Markdown.

## Review gates

- All included testcase IDs exist.
- Grouping rationale is explicit.
- Traceability is preserved.
