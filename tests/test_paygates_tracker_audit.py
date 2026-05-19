from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from test_xlsx_profiles import write_fixture_xlsx


DASHBOARD_HEADERS = [
    "Project / Product Scope",
    "Squad",
    "Sprint",
    "Epic / Function",
    "Requirement ID",
    "Test Condition ID",
    "Test Set ID",
    "Detail Artifact Link",
    "Passed",
    "Failed",
    "Untested",
    "Accepted",
    "N/A",
    "Total Test cases",
    "Current test status",
    "Test case generate type",
    "Automation test status",
    "Open Questions",
]


def run_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_dashboard_xlsx(path: Path, row: list[str]) -> None:
    write_fixture_xlsx(path, DASHBOARD_HEADERS, [row])


def workbook_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        return "\n".join(z.read(name).decode("utf-8", errors="replace") for name in z.namelist() if name.endswith(".xml"))


def test_paygates_tracker_audit_and_dashboard_sync() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        tracker = tmp_path / "Tổng hợp Trạng Thái Test Case Paygates (1).xlsx"
        write_fixture_xlsx(
            tracker,
            ["Feature", "Status", "Generate Type", "Automation Status", "Automation Type"],
            [["VA", "Read to UAT", "AI Gen", "In - Progress", "UI"]],
            'SUMIFS(Squad_VA!A:A,Squad_CnR!B:B,"Ready")',
        )

        tracker_result = run_script("validate_tracker.py", str(tracker))
        assert_true(tracker_result.returncode == 1, tracker_result.stdout + tracker_result.stderr)
        payload = json.loads(tracker_result.stdout)
        assert_true(any("Read to UAT" in error for error in payload["errors"]), str(payload))
        assert_true(any("AI Gen" in error for error in payload["errors"]), str(payload))
        assert_true(any("In - Progress" in error for error in payload["errors"]), str(payload))
        assert_true(any("UI" in error for error in payload["errors"]), str(payload))
        assert_true(any("Squad_VA" in error for error in payload["errors"]), str(payload))

        testcase = tmp_path / "Legacy19TestCase.generated.tsv"
        testcase.write_text(
            '"Test Case ID"\t"Function"\t"Group Tests"\t"Scenario Outline"\t"Test Case Summary"\t"Pre-conditions"\t"Test Datas"\t"Test Steps"\t"Expected result"\t"Environment"\t"Priority"\t"Regression"\t"Automation"\t"Manual Test Results Round 1"\t"Manual Test Results Round 2"\t"Automation Test Results"\t"Actual result"\t"BugID"\t"Notes"\n'
            '"TD_P1_001_TC_001"\t"Cards"\t"Group A"\t"Happy path"\t"Valid request"\t"Setup"\t"{}"\t"Verify API responds success"\t"Verify HTTP Status: 200"\t"SIT"\t"High"\t"Yes"\t"No"\t"PASS"\t""\t""\t""\t""\t""\n'
            '"TD_P2_001_TC_001"\t"Cards"\t"Group B"\t"Validation path"\t"Missing required field"\t"Setup"\t"{}"\t"Verify validation error"\t"Verify HTTP Status: 400"\t"SIT"\t"High"\t"Yes"\t"No"\t"FAIL"\t""\t""\t"Validation message shown"\t"BUG-001"\t""\n',
            encoding="utf-8",
        )

        execution = tmp_path / "TestExecution.from-manual.tsv"
        execution_result = run_script(
            "read_manual_execution_results.py",
            "--input",
            str(testcase),
            "--output",
            str(execution),
            "--test-execution-id",
            "EXEC-001",
            "--test-set-id",
            "SET-001",
            "--tester",
            "tester.bidv",
            "--build-version",
            "2026.05.16",
            "--environment",
            "SIT",
        )
        assert_true(execution_result.returncode == 0, execution_result.stdout + execution_result.stderr)

        dashboard_tsv = tmp_path / "PaygatesDashboard.generated.tsv"
        dashboard_result = run_script(
            "export_paygates_dashboard_tsv.py",
            "--testcase",
            str(testcase),
            "--execution",
            str(execution),
            "--project",
            "PAYGATES",
            "--squad",
            "Squad_Base",
            "--sprint",
            "Sprint 8",
            "--epic",
            "Cards",
            "--detail-link",
            "artifacts/default/reviewed/PAYGATES/Squad_Base/Cards",
            "--generate-type",
            "AI gen",
            "--automation-status",
            "Web UI",
            "--output",
            str(dashboard_tsv),
        )
        assert_true(dashboard_result.returncode == 0, dashboard_result.stdout + dashboard_result.stderr)

        dashboard_validate = run_script("validate_paygates_dashboard.py", str(dashboard_tsv))
        assert_true(dashboard_validate.returncode == 0, dashboard_validate.stdout + dashboard_validate.stderr)
        output_contract = run_script("validate_output_contract.py", "--dashboard", str(dashboard_tsv))
        assert_true(output_contract.returncode == 0, output_contract.stdout + output_contract.stderr)

        dashboard_xlsx = tmp_path / "PaygatesDashboard.generated.xlsx"
        export_xlsx = run_script("export_paygates_dashboard_xlsx.py", str(dashboard_tsv), str(dashboard_xlsx))
        assert_true(export_xlsx.returncode == 0, export_xlsx.stdout + export_xlsx.stderr)
        assert_true(dashboard_xlsx.exists(), "dashboard xlsx missing")

        text = dashboard_tsv.read_text(encoding="utf-8-sig")
        assert_true("AI gen" in text, text)
        assert_true("Web UI" in text, text)
        assert_true("Completed" not in text, text)
        assert_true("Failed" in text, text)
        xlsx_text = workbook_text(dashboard_xlsx)
        assert_true("AI gen" in xlsx_text, xlsx_text)
        assert_true("Web UI" in xlsx_text, xlsx_text)


if __name__ == "__main__":
    test_paygates_tracker_audit_and_dashboard_sync()
    print("test_paygates_tracker_audit: PASS")
