from __future__ import annotations

from pathlib import Path

from source_adapters.google_sheets import write_tsv_to_new_sheet


def publish_to_google_sheet(spreadsheet_id: str, tab_prefix: str, outputs: list[Path], approved: bool = False) -> list[dict]:
    if not approved:
        raise RuntimeError("Google Sheet write-back requires explicit approval via --write-back-google-sheet.")
    results: list[dict] = []
    for path in outputs:
        if path.suffix.lower() != ".tsv":
            continue
        tab_name = safe_tab_name(f"{tab_prefix}_{path.stem}")
        results.append(write_tsv_to_new_sheet(spreadsheet_id, tab_name, path))
    return results


def safe_tab_name(value: str) -> str:
    cleaned = "".join(ch if ch not in "[]:*?/\\" else "_" for ch in value)
    return cleaned[:90] or "QC_Output"


def write_local_handoff(output_dir: Path, final_outputs: list[str]) -> Path:
    path = output_dir / "handoff_summary.md"
    lines = ["# Handoff Summary", "", "## User-facing final outputs", ""]
    lines.extend(f"- `{output}`" for output in final_outputs if output != "OutputReview.md")
    lines.extend(["", "## Support artifacts", "", "- `source_manifest.json`", "- `route_plan.json`", "- `validation_report.json`", "- `OutputReview.md`"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
