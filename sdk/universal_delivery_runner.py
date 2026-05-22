from __future__ import annotations

import argparse
import asyncio
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
from typing import AsyncIterator

from intent_classifier import classify_intent
from output_publishers.google_sheets_publisher import publish_to_google_sheet, write_local_handoff
from output_publishers.testrail_publisher import load_testrail_config_from_env, publish_testcases_from_import_csv
from route_planner import plan_route
from source_adapters.google_sheets import build_google_sheet_source
from source_adapters.local_files import expand_sources
from source_fingerprint import fingerprint_sources
from source_manifest import SourceManifest, UserContext
from validation_orchestrator import validate_planned_outputs
from workflow_pack_loader import load_workflow_pack

ROOT = Path(__file__).resolve().parents[1]

def build_system_prompt(workflow_pack: str) -> str:
    if workflow_pack == "ai-tester":
        return """
You are running the self-contained AI Tester Operating System router.
Use workflow-packs/ai-tester as the main workflow. Work like a senior QC: collect knowledge, understand input, cook facts into tester knowledge, reason about risks, plan coverage, pass the cognition gate, then generate QA/test outputs.
Do not generate TestPlan/TestDesign/TestCase/UAT/export directly from raw input. Output generation may reuse workflow-packs/default only as a downstream subsystem after cognition artifacts pass the gate.
Missing facts must be recorded in OpenQuestions, QuestionBacklog, or [PENDING_DOC:<fact>] markers. Do not treat hypotheses as confirmed requirements.
Never write to Google Sheets or external workbooks unless explicitly instructed and validated.
""".strip()
    return """
You are running the self-contained universal file+prompt router.
The original raw sample folder is not required at runtime. Use workflow-packs/default as the source of workflow behavior, prompts, contracts, output profiles, validators, and golden examples.
User-facing final outputs are QA/test artifacts: Test Design, Test Case, legacy 19-column TSV/XLSX, UAT testcase, API automation feature files, TestExecution TSV, Paygates dashboard, and Coverage/GAP reports.
Manifests, route plans, validation reports, OutputReview, and handoff summaries are support artifacts only. TD/TC routes should also maintain CoverageMatrix.md as support traceability unless coverage is the requested final output.
Do not invent missing business facts; record open questions.
Never write to Google Sheets or external workbooks unless explicitly instructed and validated.
""".strip()


def build_manifest(args: argparse.Namespace, output_dir: Path) -> SourceManifest:
    prompt = args.prompt or (Path(args.prompt_file).read_text(encoding="utf-8") if args.prompt_file else "")
    if not prompt:
        raise ValueError("Provide --prompt or --prompt-file")
    run_id = args.run_id or datetime.now().strftime("run-%Y%m%d-%H%M%S")
    sources = []
    if args.source:
        sources.extend(expand_sources([Path(p) for p in args.source], root=ROOT))
    if args.google_sheet:
        sources.append(build_google_sheet_source(f"source-{len(sources) + 1}", args.google_sheet, tab=args.sheet_tab, range_name=args.sheet_range))
    if not sources:
        raise ValueError("Provide at least one --source or --google-sheet")
    fingerprint_sources(sources, base_dir=ROOT)
    return SourceManifest(
        schema_version="1.0",
        run_id=run_id,
        user_prompt=prompt,
        output_directory=str(output_dir),
        workflow_pack=args.workflow_pack,
        sources=sources,
        user_context=UserContext(
            project=args.project,
            squad=args.squad,
            sprint=args.sprint,
            epic=args.epic,
            environment=args.environment,
            tester=args.tester,
            build_version=args.build_version,
        ),
    )


def write_plan_only_artifacts(output_dir: Path, manifest: SourceManifest, plan) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest.write(output_dir / "source_manifest.json")
    plan.write(output_dir / "route_plan.json")
    report = validate_planned_outputs(output_dir, plan)
    report.write(output_dir / "validation_report.json")
    write_local_handoff(output_dir, plan.final_outputs)


def build_ai_tester_execution_requirements() -> str:
    return """
AI Tester OS requirements:
1. For end-to-end delivery, create cognition artifacts before final QA/test outputs: SourceInventory.md, DocumentMap.md, FactInventory.md, BusinessRuleModel.md or OpenQuestions.md, RiskModel.md, CoveragePlan.md, TesterStrategyPlan.md, and QuestionBacklog.md.
2. Each cognition artifact must include Artifact ID, Project, Squad, Epic, Source Refs, Created By, Created At, Confidence, and Open Questions.
3. Source-backed claims must include source manifest ids, normalized knowledge ids, source section/page/sheet refs, or [PENDING_DOC:<fact>] markers.
4. Missing facts must be visible in OpenQuestions.md, QuestionBacklog.md, or pending markers. Do not invent requirements.
5. Hypotheses belong in risk/defect reasoning only; do not treat them as confirmed business rules.
6. Run cognition gate validation before output stages. If the gate fails, write blocker rationale to OutputReview.md and SupervisorApproval.md instead of claiming approval.
7. Output stages may reuse workflow-packs/default prompts/contracts only after the cognition gate passes.
""".strip()


def build_output_generation_requirements() -> str:
    return """
Output generation requirements:
1. API_TestDesign.md must satisfy scripts/validate_test_design.py --type api and scripts/validate_api_td_specificity.py: include TD_P1, TD_P2, and TD_P3 nodes with headings like `### TD_P1_001 ...`; include control parameters METHOD_CHECK, CONTENT_TYPE_CHECK, MANDATORY_CHECK, TYPE_CHECK, LENGTH_CHECK, SCOPE_FIELDS, and EG_CHECK; include HTTP method plus endpoint heading such as `POST /path`; each TD node must include **Steps**, **Expected**, and Source/source reference text; TD_P2 nodes must name concrete field/schema/request/response/body/param targets; TD_P3 nodes must name concrete business/rule/error/code/state/flow targets.
2. Before writing Legacy19TestCase.generated.tsv, read workflow-packs/default/examples/testcase-legacy-19col.tsv and copy its 19-column header exactly, including quoted cells and tab separators. Every data row must have exactly the same 19 tab-separated columns and non-empty required cells.
3. Before writing CoverageMatrix.md, satisfy scripts/validate_test_generation_matrix.py: include a Markdown table with at least these columns: Matrix Row ID, Source Ref, Source Kind, Field Or Rule, Rule Type, Technique, Value Class, Coverage Status, Rationale, TD ID, Test Case ID. For every row whose Coverage Status is covered, populate a valid TD ID such as TD_P1_001/TD_P2_001/TD_P3_001 or a valid Test Case ID such as TD_P1_001_TC_001; use Coverage Status open_question for rows that cannot be traced to a TD/TC yet.
4. TestCaseSource.md must contain real testcase execution content, not metadata-only notes: include testcase IDs matching TD_P[123]_NNN_TC_NNN; include `Primary Condition:`, `Primary Target:`, or `Atomic Target:` markers naming exact field/header/param/path/body/business targets; include execution markers such as `Pre-conditions`, `Test Datas`, `Test Steps`, `Expected result`, or `Open Questions`; keep each testcase atomic.
5. Each row in Legacy19TestCase.generated.tsv must also satisfy scripts/validate_api_tc_specificity.py and scripts/validate_testcase_granularity.py: Test Case ID must match TD_P[123]_NNN_TC_NNN; Test Case Summary or Test Steps must include an HTTP method (GET/POST/PUT/PATCH/DELETE) and endpoint path; Expected result must include an HTTP status such as HTTP 200/HTTP 400 and a concrete response/error assertion mentioning code, message, success, data, errors, response, body, schema, field, lỗi, or mã lỗi; Test Case Summary or Test Datas or Expected result must contain `Primary Condition:`, `Primary Target:`, or `Atomic Target:` naming one exact field/header/param/path/body/business rule. Do not use generic phrases such as valid data, invalid data, correct response, appropriate error, như trên, tương tự, etc.
6. Legacy19TestCase.generated.tsv must include all API coverage categories required by scripts/validate_testcase_coverage.py for profile api_legacy_19_column_testcase. Across the generated rows, include explicit `Coverage: METHOD`, `Coverage: CONTENT_TYPE`, `Coverage: AUTH`, `Coverage: MANDATORY_HEADERS`, `Coverage: LANGUAGE`, `Coverage: BODY_SCHEMA`, `Coverage: BOUNDARY`, `Coverage: BUSINESS_ERROR`, `Coverage: RESPONSE_SCHEMA`, and `Coverage: ERROR_PRIORITY` markers in Notes or another testcase text column. Each marked row must still remain atomic with one Primary Condition.
""".strip()


def build_execution_prompt(manifest_path: Path, route_plan_path: Path, workflow_pack: str) -> str:
    pack_requirements = build_ai_tester_execution_requirements() if workflow_pack == "ai-tester" else ""
    output_requirements = build_output_generation_requirements()
    return f"""
Execute the universal route using workflow pack `{workflow_pack}`.

Read:
- Source manifest: {manifest_path}
- Route plan: {route_plan_path}

Required behavior:
1. Use workflow pack prompts/contracts, not any external raw sample folder.
2. Generate the user-facing final outputs listed in route_plan.json.
3. Keep manifests/route/validation/report files as support artifacts only.
4. For prompt-backed stages, record workflow pack prompt path in generated Markdown.
5. Run deterministic validators where available.
6. Maintain CoverageMatrix.md when route_plan.json lists it as a final or support output. Use source manifest ids or workflow-pack/normalized ids for source_ref; never use raw sample paths.
7. Produce OutputReview.md and handoff_summary.md.
8. Do not create task-list items or plan-only placeholders. Write the required artifact files directly under the manifest output_directory before finishing.
9. If a required source fact is absent, write an explicit Open Question or [PENDING_DOC] marker instead of stopping generation.
10. Preserve the workflow route and prompt sequence exactly as defined by route_plan.json; these prompts are packaged end-user standard knowledge, not throwaway templates.
11. Do not claim review, supervisor approval, or publish readiness unless deterministic validators pass. If any validator fails or cannot be run, OutputReview.md and SupervisorApproval.md must state retry_required/rejected with the exact blocker.

{pack_requirements}

{output_requirements}
""".strip()


def build_options(cwd: Path, max_turns: int, include_mcp: bool):
    try:
        from claude_agent_sdk import ClaudeAgentOptions
    except ImportError as exc:
        raise RuntimeError("Install claude-agent-sdk to execute generation with this runner") from exc
    allowed_tools = ["Read", "Glob", "Grep", "Bash", "Write", "Edit"]
    return ClaudeAgentOptions(
        cwd=str(cwd),
        model="sonnet",
        fallback_model="haiku",
        max_turns=max_turns,
        permission_mode="dontAsk",
        tools=allowed_tools,
        allowed_tools=allowed_tools,
        disallowed_tools=["WebSearch", "Task", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet"],
    )


async def execute_with_claude(output_dir: Path, workflow_pack: str, max_turns: int, include_mcp: bool) -> AsyncIterator[str]:
    try:
        from claude_agent_sdk import ClaudeSDKClient
    except ImportError as exc:
        raise RuntimeError("Install claude-agent-sdk-python to execute generation with this runner") from exc
    options = build_options(ROOT, max_turns=max_turns, include_mcp=include_mcp)
    prompt = build_execution_prompt(output_dir / "source_manifest.json", output_dir / "route_plan.json", workflow_pack)
    async with ClaudeSDKClient(options=options) as client:
        await client.query(f"{build_system_prompt(workflow_pack)}\n\n{prompt}")
        async for message in client.receive_response():
            yield str(message)


def require_claude_agent_sdk() -> None:
    try:
        import claude_agent_sdk  # noqa: F401
    except ImportError as exc:
        raise RuntimeError("Install claude-agent-sdk to execute generation with this runner") from exc


def require_final_outputs(output_dir: Path, plan) -> None:
    missing = [output for output in plan.final_outputs if not (output_dir / output).exists()]
    if missing:
        raise RuntimeError(f"Generation completed without required final outputs: {missing}")


def maybe_export_testrail_csv(output_dir: Path, plan, enabled: bool) -> Path | None:
    if not enabled:
        return None
    legacy_tsv = next(
        (output_dir / output for output in plan.final_outputs if output == "Legacy19TestCase.generated.tsv" and (output_dir / output).exists()),
        None,
    )
    if legacy_tsv is None:
        return None
    csv_output = output_dir / "TestRailImport.generated.csv"
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "export_testrail_cases_csv.py"),
        "--input",
        str(legacy_tsv),
        "--output",
        str(csv_output),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"TestRail CSV export failed:\n{proc.stdout}{proc.stderr}")
    return csv_output


def maybe_publish_testrail(csv_output: Path | None, enabled: bool, mode: str) -> None:
    if not enabled or csv_output is None:
        return
    if mode == "csv-only":
        return
    config = load_testrail_config_from_env()
    publish_testcases_from_import_csv(csv_output, config=config, approved=True, mode=mode)


async def async_main(args: argparse.Namespace) -> int:
    if not (args.plan_only or args.dry_run):
        require_claude_agent_sdk()
    output_dir = Path(args.output_dir).resolve()
    workflow = load_workflow_pack(ROOT, args.workflow_pack)
    manifest = build_manifest(args, output_dir)
    classification = classify_intent(manifest)
    plan = plan_route(workflow, classification, pack_id=args.workflow_pack)
    write_plan_only_artifacts(output_dir, manifest, plan)
    print(json.dumps({
        "request_type": classification.request_type,
        "confidence": classification.confidence,
        "source_roles": classification.source_roles,
        "prompt_intents": classification.prompt_intents,
        "final_outputs": plan.final_outputs,
        "output_dir": str(output_dir),
    }, ensure_ascii=False, indent=2))
    if args.plan_only or args.dry_run:
        return 0
    async for chunk in execute_with_claude(output_dir, args.workflow_pack, args.max_turns, args.include_mcp):
        print(chunk)
    require_final_outputs(output_dir, plan)
    report = validate_planned_outputs(output_dir, plan)
    report.write(output_dir / "validation_report.json")
    if args.write_back_google_sheet:
        if not args.target_sheet_id:
            raise RuntimeError("--target-sheet-id is required with --write-back-google-sheet")
        tsv_outputs = [output_dir / output for output in plan.final_outputs if output.endswith(".tsv") and (output_dir / output).exists()]
        publish_to_google_sheet(args.target_sheet_id, args.write_back_tab_prefix, tsv_outputs, approved=True)
    testrail_csv = maybe_export_testrail_csv(output_dir, plan, args.write_back_testrail or args.write_back_testrail_mode == "csv-only")
    maybe_publish_testrail(testrail_csv, args.write_back_testrail, args.write_back_testrail_mode)
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Universal file+prompt router")
    parser.add_argument("--source", action="append")
    parser.add_argument("--google-sheet")
    parser.add_argument("--sheet-tab")
    parser.add_argument("--sheet-range")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--workflow-pack", default="ai-tester")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--project")
    parser.add_argument("--squad")
    parser.add_argument("--sprint")
    parser.add_argument("--epic")
    parser.add_argument("--environment")
    parser.add_argument("--tester")
    parser.add_argument("--build-version")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--include-mcp", action="store_true")
    parser.add_argument("--max-turns", type=int, default=12)
    parser.add_argument("--write-back-google-sheet", action="store_true", help="Write TSV outputs to new tabs after successful generation and validation")
    parser.add_argument("--target-sheet-id", help="Target spreadsheet ID for explicit Google Sheet write-back")
    parser.add_argument("--write-back-tab-prefix", default="QC_Output", help="Prefix for new output tabs")
    parser.add_argument("--write-back-testrail", action="store_true", help="Publish generated testcase definitions to TestRail after validation")
    parser.add_argument("--write-back-testrail-mode", choices=["csv-only", "api"], default="csv-only", help="TestRail write-back mode; csv-only creates TestRailImport.generated.csv without calling TestRail")
    args = parser.parse_args()
    return asyncio.run(async_main(args))


if __name__ == "__main__":
    raise SystemExit(main())
