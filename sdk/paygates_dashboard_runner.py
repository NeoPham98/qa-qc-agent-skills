from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, cwd=ROOT.parent, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({' '.join(cmd)}):\n{proc.stdout}{proc.stderr}")
    if proc.stdout:
        print(proc.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Paygates dashboard artifacts")
    parser.add_argument("--testcase", required=True, type=Path)
    parser.add_argument("--execution", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--project", default="")
    parser.add_argument("--squad", default="")
    parser.add_argument("--sprint", default="")
    parser.add_argument("--epic", default="")
    parser.add_argument("--detail-link", default="")
    parser.add_argument("--include-xlsx", action="store_true")
    parser.add_argument("--sync-workbook", type=Path)
    parser.add_argument("--sync-output", type=Path)
    args = parser.parse_args()
    if args.sync_workbook and not args.sync_output:
        raise RuntimeError("--sync-output is required when --sync-workbook is provided")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    tsv = args.output_dir / "PaygatesDashboard.generated.tsv"
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "export_paygates_dashboard_tsv.py"),
        "--testcase",
        str(args.testcase),
        "--output",
        str(tsv),
    ]
    for flag, value in [("--execution", args.execution), ("--project", args.project), ("--squad", args.squad), ("--sprint", args.sprint), ("--epic", args.epic), ("--detail-link", args.detail_link)]:
        if value:
            cmd.extend([flag, str(value)])
    run(cmd)
    run([sys.executable, str(ROOT / "scripts" / "validate_paygates_dashboard.py"), str(tsv)])
    if args.include_xlsx:
        run([sys.executable, str(ROOT / "scripts" / "export_paygates_dashboard_xlsx.py"), str(tsv), str(args.output_dir / "PaygatesDashboard.generated.xlsx")])
    if args.sync_output:
        sync_cmd = [sys.executable, str(ROOT / "scripts" / "sync_paygates_dashboard_xlsx.py"), "--dashboard-tsv", str(tsv), "--output", str(args.sync_output)]
        if args.sync_workbook:
            sync_cmd.extend(["--source-workbook", str(args.sync_workbook)])
        run(sync_cmd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
