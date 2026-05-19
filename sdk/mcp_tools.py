from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TD_CASE_ID_RE = re.compile(r"\bTD_P[123]_\d{3}_TC_\d{3}\b")
TD_NODE_RE = re.compile(r"\bTD_P[123]_\d{3}\b")


def list_artifact_files(output_dir: str) -> list[str]:
    base = Path(output_dir)
    if not base.exists():
        return []
    return [str(path) for path in sorted(base.rglob("*")) if path.is_file()]


def validate_legacy_tsv(path: str) -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "validate_legacy_19col_tsv.py"), path]
    return _run(cmd)


def validate_testcase_tsv(path: str) -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "validate_output_contract.py"), "--testcase", path]
    return _run(cmd)


def validate_execution_tsv(path: str) -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "validate_output_contract.py"), "--execution", path]
    return _run(cmd)


def validate_paygates_dashboard(path: str) -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "validate_paygates_dashboard.py"), path]
    return _run(cmd)


def verify_runtime_prompt_manifest() -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "verify_runtime_prompt_manifest.py")]
    return _run(cmd)


def export_paygates_dashboard_tsv(testcase: str, output: str, execution: str = "", project: str = "", squad: str = "", sprint: str = "", epic: str = "", detail_link: str = "") -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "export_paygates_dashboard_tsv.py"), "--testcase", testcase, "--output", output]
    for flag, value in [("--execution", execution), ("--project", project), ("--squad", squad), ("--sprint", sprint), ("--epic", epic), ("--detail-link", detail_link)]:
        if value:
            cmd.extend([flag, value])
    return _run(cmd)


def export_paygates_dashboard_xlsx(input_tsv: str, output_xlsx: str) -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "export_paygates_dashboard_xlsx.py"), input_tsv, output_xlsx]
    return _run(cmd)


def export_legacy_19col_xlsx(input_path: str, output_xlsx: str) -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "export_legacy_19col_xlsx.py"), input_path, output_xlsx, "--formatted"]
    return _run(cmd)


def read_manual_execution_results(input_path: str, output_tsv: str, round: str = "1", test_execution_id: str = "", test_set_id: str = "", tester: str = "", build_version: str = "") -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "read_manual_execution_results.py"), "--input", input_path, "--output", output_tsv, "--round", round]
    for flag, value in [("--test-execution-id", test_execution_id), ("--test-set-id", test_set_id), ("--tester", tester), ("--build-version", build_version)]:
        if value:
            cmd.extend([flag, value])
    return _run(cmd)


def sync_paygates_dashboard_xlsx(dashboard_tsv: str, output_xlsx: str, source_workbook: str = "") -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "sync_paygates_dashboard_xlsx.py"), "--dashboard-tsv", dashboard_tsv, "--output", output_xlsx]
    if source_workbook:
        cmd.extend(["--source-workbook", source_workbook])
    return _run(cmd)


def verify_prompt_mirrors() -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "verify_prompt_mirrors.py")]
    return _run(cmd)


def check_api_td_case_ids(path: str) -> dict[str, object]:
    text = Path(path).read_text(encoding="utf-8-sig")
    legacy_ids = sorted(set(re.findall(r"\bTC-API-\d+\b", text)))
    td_case_ids = sorted(set(TD_CASE_ID_RE.findall(text)))
    return {
        "ok": not legacy_ids and bool(td_case_ids),
        "td_case_ids": td_case_ids,
        "legacy_ids": legacy_ids,
    }


def summarize_coverage_gaps(td_path: str, testcase_path: str) -> dict[str, object]:
    td_text = Path(td_path).read_text(encoding="utf-8-sig")
    testcase_text = Path(testcase_path).read_text(encoding="utf-8-sig")
    td_nodes = sorted(set(TD_NODE_RE.findall(td_text)))
    missing = [node for node in td_nodes if node not in testcase_text]
    return {
        "ok": not missing,
        "td_nodes": td_nodes,
        "missing_in_testcase": missing,
    }


def read_tsv_headers(path: str) -> list[str]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        return next(reader, [])


def _run(cmd: list[str]) -> dict[str, object]:
    proc = subprocess.run(cmd, cwd=ROOT.parent, text=True, capture_output=True, check=False)
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "command": cmd,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def create_mcp_server():
    """Create an in-process SDK MCP server when claude-agent-sdk is installed."""
    try:
        from claude_agent_sdk import tool, create_sdk_mcp_server
    except ImportError as exc:
        raise RuntimeError("claude-agent-sdk-python is required for MCP server creation") from exc

    @tool("list_artifact_files", "List generated artifact files under an output directory", {"output_dir": str})
    async def list_artifact_files_tool(args: dict[str, str]) -> list[str]:
        return list_artifact_files(args["output_dir"])

    @tool("validate_legacy_tsv", "Validate legacy 19-column TSV", {"path": str})
    async def validate_legacy_tsv_tool(args: dict[str, str]) -> dict[str, object]:
        return validate_legacy_tsv(args["path"])

    @tool("validate_testcase_tsv", "Validate testcase TSV contract", {"path": str})
    async def validate_testcase_tsv_tool(args: dict[str, str]) -> dict[str, object]:
        return validate_testcase_tsv(args["path"])

    @tool("verify_prompt_mirrors", "Verify runtime prompt mirrors match source prompts", {})
    async def verify_prompt_mirrors_tool(_: dict[str, str]) -> dict[str, object]:
        return verify_prompt_mirrors()

    @tool("verify_runtime_prompt_manifest", "Verify packaged runtime prompt hashes", {})
    async def verify_runtime_prompt_manifest_tool(_: dict[str, str]) -> dict[str, object]:
        return verify_runtime_prompt_manifest()

    @tool("validate_paygates_dashboard", "Validate Paygates dashboard TSV", {"path": str})
    async def validate_paygates_dashboard_tool(args: dict[str, str]) -> dict[str, object]:
        return validate_paygates_dashboard(args["path"])

    @tool("export_paygates_dashboard_tsv", "Export Paygates dashboard TSV", {"testcase": str, "output": str, "execution": str, "project": str, "squad": str, "sprint": str, "epic": str, "detail_link": str})
    async def export_paygates_dashboard_tsv_tool(args: dict[str, str]) -> dict[str, object]:
        return export_paygates_dashboard_tsv(args["testcase"], args["output"], args.get("execution", ""), args.get("project", ""), args.get("squad", ""), args.get("sprint", ""), args.get("epic", ""), args.get("detail_link", ""))

    @tool("export_paygates_dashboard_xlsx", "Export Paygates dashboard XLSX from TSV", {"input_tsv": str, "output_xlsx": str})
    async def export_paygates_dashboard_xlsx_tool(args: dict[str, str]) -> dict[str, object]:
        return export_paygates_dashboard_xlsx(args["input_tsv"], args["output_xlsx"])

    @tool("export_legacy_19col_xlsx", "Export formatted legacy 19-column XLSX from Markdown or TSV", {"input_path": str, "output_xlsx": str})
    async def export_legacy_19col_xlsx_tool(args: dict[str, str]) -> dict[str, object]:
        return export_legacy_19col_xlsx(args["input_path"], args["output_xlsx"])

    @tool("read_manual_execution_results", "Read manual execution results into TestExecution TSV", {"input_path": str, "output_tsv": str, "round": str, "test_execution_id": str, "test_set_id": str, "tester": str, "build_version": str})
    async def read_manual_execution_results_tool(args: dict[str, str]) -> dict[str, object]:
        return read_manual_execution_results(args["input_path"], args["output_tsv"], args.get("round", "1"), args.get("test_execution_id", ""), args.get("test_set_id", ""), args.get("tester", ""), args.get("build_version", ""))

    @tool("sync_paygates_dashboard_xlsx", "Safely sync/export Paygates dashboard XLSX from validated TSV", {"dashboard_tsv": str, "output_xlsx": str, "source_workbook": str})
    async def sync_paygates_dashboard_xlsx_tool(args: dict[str, str]) -> dict[str, object]:
        return sync_paygates_dashboard_xlsx(args["dashboard_tsv"], args["output_xlsx"], args.get("source_workbook", ""))

    @tool("check_api_td_case_ids", "Check API testcase IDs follow TD_Px_NNN_TC_NNN", {"path": str})
    async def check_api_td_case_ids_tool(args: dict[str, str]) -> dict[str, object]:
        return check_api_td_case_ids(args["path"])

    return create_sdk_mcp_server(
        name="artifact_tools",
        version="0.1.0",
        tools=[
            list_artifact_files_tool,
            validate_legacy_tsv_tool,
            validate_testcase_tsv_tool,
            verify_prompt_mirrors_tool,
            verify_runtime_prompt_manifest_tool,
            validate_paygates_dashboard_tool,
            export_paygates_dashboard_tsv_tool,
            export_paygates_dashboard_xlsx_tool,
            export_legacy_19col_xlsx_tool,
            read_manual_execution_results_tool,
            sync_paygates_dashboard_xlsx_tool,
            check_api_td_case_ids_tool,
        ],
    )
