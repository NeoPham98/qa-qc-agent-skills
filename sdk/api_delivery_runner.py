from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import AsyncIterator

from hooks import build_sdk_hooks


ROOT = Path(__file__).resolve().parents[1]


SYSTEM_PROMPT = """
You are running the delivery orchestrator for qc-agent-skills.
Use Prompt-Compatible Orchestration Mode only.
Select workflow steps from data/source-inventory/workflow_map.md and runtime verbatim prompts from data/source-inventory/prompt_fragment_registry.md.
Never use summarized skills/*/prompts/*.md notes as runtime prompts unless verified as content-equivalent to source prompts.
Preserve API phase routing: setup/context -> TD_P1 -> TD_P2 -> TD_P3 -> testcase from TD -> testcase analysis -> phase-specific automation support -> output review.
Do not invent missing business/API/schema/DB facts; record open questions instead.
Run deterministic validators before handoff when TSV artifacts are produced.
""".strip()


def verify_prompt_mirrors() -> None:
    cmd = [sys.executable, str(ROOT / "scripts" / "verify_runtime_prompt_manifest.py")]
    proc = subprocess.run(cmd, cwd=ROOT.parent, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"prompt mirror verification failed:\n{proc.stdout}{proc.stderr}")


def build_prompt(source: Path, output_dir: Path, scope: str, plan_only: bool) -> str:
    mode = "Plan the route only; do not edit files." if plan_only else "Execute the approved route and write artifacts under the output directory."
    return f"""
{mode}

Source input: {source}
Output directory: {output_dir}
Scope: {scope}

Required behavior:
1. Start from agents/delivery-orchestrator/AGENT.md.
2. Use the registry and workflow map before selecting any skill.
3. Keep Markdown as source-of-truth and TSV as derived output.
4. Record selected Source Prompt and Runtime Verbatim Prompt in generated Markdown artifacts.
5. Produce or require OutputReview before handoff.
""".strip()


def run_validator(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, cwd=ROOT.parent, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Post-run validation failed ({' '.join(cmd)}):\n{proc.stdout}{proc.stderr}")


def validate_markdown_prompt_metadata(output_dir: Path) -> None:
    markdown_files = [path for path in output_dir.rglob("*.md") if path.is_file()]
    missing: list[Path] = []
    for path in markdown_files:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        has_source = "source bidv prompt" in text or "source prompt" in text
        has_runtime = "runtime verbatim prompt" in text or "runtime prompt" in text
        if not (has_source and has_runtime):
            missing.append(path)
    if missing:
        rel = ", ".join(str(path.relative_to(output_dir)) for path in missing)
        raise RuntimeError(f"Markdown artifacts missing source/runtime prompt metadata: {rel}")


def validate_post_run(output_dir: Path) -> None:
    if not output_dir.exists():
        raise RuntimeError(f"Output directory was not created: {output_dir}")

    reviews = [path for path in output_dir.rglob("*.md") if "outputreview" in path.name.lower()]
    if not reviews:
        raise RuntimeError(f"Missing OutputReview Markdown artifact under: {output_dir}")

    validate_markdown_prompt_metadata(output_dir)

    legacy_candidates = [path for path in output_dir.rglob("*.tsv") if "legacy" in path.name.lower() or "19col" in path.name.lower()]
    for path in legacy_candidates:
        run_validator([sys.executable, str(ROOT / "scripts" / "validate_legacy_19col_tsv.py"), str(path)])

    testcase_candidates = [path for path in output_dir.rglob("*.tsv") if "testcase" in path.name.lower() and path not in legacy_candidates]
    execution_candidates = [path for path in output_dir.rglob("*.tsv") if "execution" in path.name.lower() or "status" in path.name.lower()]
    for testcase in testcase_candidates:
        run_validator([sys.executable, str(ROOT / "scripts" / "validate_output_contract.py"), "--testcase", str(testcase)])
    for execution in execution_candidates:
        run_validator([sys.executable, str(ROOT / "scripts" / "validate_output_contract.py"), "--execution", str(execution)])


def build_options(cwd: Path, max_turns: int, include_mcp: bool):
    try:
        from claude_agent_sdk import ClaudeAgentOptions
    except ImportError as exc:
        raise RuntimeError("Install claude-agent-sdk-python to use this runner") from exc

    mcp_servers = {}
    allowed_tools = ["Read", "Glob", "Grep", "Bash", "Write", "Edit"]
    if include_mcp:
        from mcp_tools import create_mcp_server

        mcp_servers["artifact_tools"] = create_mcp_server()
        allowed_tools.extend([
            "mcp__artifact_tools__list_artifact_files",
            "mcp__artifact_tools__validate_legacy_tsv",
            "mcp__artifact_tools__validate_testcase_tsv",
            "mcp__artifact_tools__verify_prompt_mirrors",
            "mcp__artifact_tools__verify_runtime_prompt_manifest",
            "mcp__artifact_tools__validate_paygates_dashboard",
            "mcp__artifact_tools__export_paygates_dashboard_tsv",
            "mcp__artifact_tools__export_paygates_dashboard_xlsx",
            "mcp__artifact_tools__export_legacy_19col_xlsx",
            "mcp__artifact_tools__read_manual_execution_results",
            "mcp__artifact_tools__sync_paygates_dashboard_xlsx",
            "mcp__artifact_tools__check_api_td_case_ids",
        ])

    return ClaudeAgentOptions(
        cwd=str(cwd),
        model="sonnet",
        fallback_model="haiku",
        max_turns=max_turns,
        permission_mode="dontAsk",
        allowed_tools=allowed_tools,
        disallowed_tools=["WebSearch"],
        mcp_servers=mcp_servers,
        hooks=build_sdk_hooks(),
    )


async def run_delivery(
    source: Path,
    output_dir: Path,
    scope: str,
    plan_only: bool,
    max_turns: int,
    include_mcp: bool,
    skip_post_run_validation: bool,
) -> AsyncIterator[str]:
    verify_prompt_mirrors()

    try:
        from claude_agent_sdk import ClaudeSDKClient
    except ImportError as exc:
        raise RuntimeError("Install claude-agent-sdk-python to use this runner") from exc

    options = build_options(ROOT.parent, max_turns=max_turns, include_mcp=include_mcp)
    prompt = build_prompt(source, output_dir, scope, plan_only)

    async with ClaudeSDKClient(options=options) as client:
        await client.query(f"{SYSTEM_PROMPT}\n\n{prompt}")
        async for message in client.receive_response():
            yield str(message)

    if not plan_only and not skip_post_run_validation:
        validate_post_run(output_dir)


async def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Run API delivery workflow through Claude Agent SDK")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--scope", default="full API delivery")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--max-turns", type=int, default=12)
    parser.add_argument("--include-mcp", action="store_true")
    parser.add_argument("--skip-post-run-validation", action="store_true")
    args = parser.parse_args()

    async for chunk in run_delivery(
        args.source,
        args.output_dir,
        args.scope,
        args.plan_only,
        args.max_turns,
        args.include_mcp,
        args.skip_post_run_validation,
    ):
        print(chunk)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
