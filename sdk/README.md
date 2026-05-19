# Claude Agent SDK Runner

This folder contains repeatable/headless orchestration helpers for `qc-agent-skills` using `claude-agent-sdk-python` patterns.

## Design

- Skills and runtime verbatim prompts remain the source of prompt-compatible behavior.
- `delivery-orchestrator` remains the workflow entry point.
- SDK runners provide repeatable execution, permissions, hooks, and deterministic validation helpers.
- Agent Teams are runtime constructs; do not commit generated `.claude/teams` or task-list state.

## Permission model

`allowed_tools` only auto-approves tools; it is not a sandbox. Use `disallowed_tools`, conservative `permission_mode`, and hooks to block risky operations.

Recommended default for headless runs:

- allow read/search and explicit validation commands,
- disallow web search unless the task requires it,
- block destructive shell operations through hooks,
- require explicit approval for pushes, PRs, comments, Jira/Xray writes, or external state changes.

## Prompt mirror enforcement

Before development/source-fidelity handoff, run:

```bash
python scripts/verify_prompt_mirrors.py
```

Before packaged runtime handoff where the source prompt provenance folder is unavailable, run:

```bash
python scripts/verify_runtime_prompt_manifest.py
```

The SDK runner performs packaged runtime verification before starting delivery execution. If you enable project hooks, the same verification can be wired through `.claude/settings.json` based on the example file in `.claude/settings.example.json`.

## Files

- `universal_delivery_runner.py`: universal file+prompt router. It builds a source manifest, classifies intent, resolves a workflow-pack route, and targets final QA/test artifacts such as Test Design, TestCase, Excel, API feature files, execution TSV, dashboard, and coverage reports.
- `api_delivery_runner.py`: SDK workflow skeleton for full API delivery.
- `paygates_dashboard_runner.py`: deterministic Paygates dashboard/status generation from testcase and execution artifacts, with optional safe XLSX sync output.
- `source_manifest.py`, `source_fingerprint.py`, `intent_classifier.py`, `workflow_pack_loader.py`, `route_planner.py`, `output_inference.py`: universal routing core.
- `source_adapters/local_files.py`: local file/folder intake.
- `source_adapters/google_sheets.py`: Google Sheet source parsing/read bridge skeleton.
- `hooks.py`: reusable guardrail policy helpers.
- `mcp_tools.py`: deterministic validation/helper tools for artifact inspection, legacy XLSX export, manual execution import, and Paygates dashboard sync.
- `.claude/settings.example.json`: optional Claude Code project settings template for hooks and permissions.

## Universal file + prompt flow

For Antigravity/Claude-style usage where the user drops files and writes a prompt, use:

```bash
python sdk/universal_delivery_runner.py \
  --workflow-pack default \
  --source ./input/api_spec.pdf \
  --prompt "Sinh test design, testcase 19 cột và test API" \
  --output-dir ./outputs/run-001 \
  --plan-only
```

`--plan-only` creates route/support artifacts only. Execution mode delegates generation to Claude Agent SDK and should produce user-facing final outputs listed in `route_plan.json`.

Google Sheet intake is represented as a source role; read/write dependencies are optional and write-back is disabled by default.

## Typical flow

1. Prepare source docs, Google Sheet references, and output folder.
2. Run universal runner in plan/read-only mode for source fingerprinting and route confirmation.
3. Run generation route through prompt-compatible orchestrator/workflow pack.
4. Run deterministic validators.
5. Require `OutputReview` before handoff.

## Manual execution and dashboard sync helpers

The deterministic helper layer also supports the missing workbook bridge:

1. Export legacy testcase Markdown/TSV to formatted XLSX with `scripts/export_legacy_19col_xlsx.py --formatted`.
2. Import tester result columns from the returned workbook with `scripts/read_manual_execution_results.py`.
3. Generate Paygates dashboard TSV from testcase + execution TSV.
4. Safely write Paygates dashboard XLSX with `scripts/sync_paygates_dashboard_xlsx.py`, always using an explicit output path and never overwriting the source workbook.
