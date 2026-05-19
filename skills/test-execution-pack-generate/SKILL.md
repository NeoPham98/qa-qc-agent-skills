---
name: test-execution-pack-generate
description: Generates BIDV Test Execution artifacts from reviewed testcase/test set outputs.
role_affinity: [tester, qa_lead]
domain: [test_execution, bidv]
lifecycle_stage: [test_execution]
produces: [md, execution_tsv]
consumes: [testcase, test_set]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Test Execution Pack Generate

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. It prepares execution artifacts from reviewed prompt-compatible testcase/test set sources.

## Selection criteria

Use this skill when a Test Execution pack or execution TSV is requested.

## Required inputs

- Reviewed TestCase source.
- Test Set context if available.
- Environment, build/version, tester, planned run date when known.
- Expected execution contract.

## Workflow

1. Receive execution route from orchestrator.
2. Verify testcase/test set source and execution metadata.
3. Generate TestExecution Markdown.
4. Export execution TSV when required.
5. Send output to review.

## Outputs

- TestExecution Markdown.
- Test Execution TSV.

## Review gates

- Test Case/Test Execution separation preserved.
- Execution rows reference existing testcase IDs.
- Execution contract satisfied.
