from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SDK = ROOT / "sdk"
EXAMPLE = ROOT / "examples" / "e2e" / "api-automation"
sys.path.insert(0, str(SDK))

from source_manifest import SourceFingerprint, SourceItem, SourceManifest


FINAL_OUTPUTS = [
    "API_TestCase_Analysis.md",
    "api_method_header_validation.feature",
    "api_validation.feature",
    "api_logic_business.feature",
    "OutputReview.md",
    "SupervisorApproval.md",
]
FEATURE_PHASES = {
    "api_method_header_validation.feature": "TD_P1",
    "api_validation.feature": "TD_P2",
    "api_logic_business.feature": "TD_P3",
}
EXPECTED_IDS = {
    "TD_P1_001_TC_001": "api_method_header_validation.feature",
    "TD_P2_001_TC_001": "api_validation.feature",
    "TD_P3_001_TC_001": "api_logic_business.feature",
}


def run_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True, check=False)


def run_closed_loop(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPTS / "run_closed_loop.py"), *args], capture_output=True, text=True, check=False)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_manifest(path: Path, output_dir: Path) -> None:
    manifest = SourceManifest(
        schema_version="1.0",
        run_id="api-automation-e2e-test",
        user_prompt="Sinh API automation feature files từ testcase PAYGATES CCTG",
        output_directory=str(output_dir),
        workflow_pack="default",
        sources=[
            SourceItem(
                id="api-automation-testcase-source",
                kind="local_file",
                original_locator="examples/e2e/api-automation/TestCaseSource.md",
                local_path="examples/e2e/api-automation/TestCaseSource.md",
                extension=".md",
                fingerprint=SourceFingerprint(candidate_roles=["api_testcase", "testcase"]),
            )
        ],
    )
    manifest.write(path)


def copy_seed_outputs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in ["TestCaseSource.md", *FINAL_OUTPUTS]:
        shutil.copy2(EXAMPLE / name, output_dir / name)


def assert_no_raw_bidv(output_dir: Path) -> None:
    result = run_script("validate_no_bidv_runtime_refs.py", str(output_dir))
    assert_true(result.returncode == 0, result.stdout + result.stderr)


def assert_phase_traceability(output_dir: Path) -> None:
    analysis = (output_dir / "API_TestCase_Analysis.md").read_text(encoding="utf-8")
    for tc_id, feature_name in EXPECTED_IDS.items():
        assert_true(analysis.count(tc_id) == 1, f"{tc_id} should appear exactly once in analysis")
        for name in FEATURE_PHASES:
            feature = (output_dir / name).read_text(encoding="utf-8")
            expected_present = name == feature_name
            assert_true((tc_id in feature) is expected_present, f"{tc_id} phase placement mismatch in {name}")


def test_api_automation_e2e_workflow_generates_valid_approved_artifacts() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        output_dir = tmp_path / "out"
        manifest = tmp_path / "source_manifest.json"
        copy_seed_outputs(output_dir)
        write_manifest(manifest, output_dir)

        analysis_result = run_script(
            "validate_api_automation_analysis.py",
            str(output_dir / "API_TestCase_Analysis.md"),
            "--testcase-source",
            str(output_dir / "TestCaseSource.md"),
        )
        assert_true(analysis_result.returncode == 0, analysis_result.stdout + analysis_result.stderr)

        for name, phase in FEATURE_PHASES.items():
            feature_result = run_script("validate_api_automation_feature.py", str(output_dir / name), "--phase", phase)
            assert_true(feature_result.returncode == 0, feature_result.stdout + feature_result.stderr)

        for name in FINAL_OUTPUTS:
            assert_true((output_dir / name).exists(), f"missing final output {name}")
        assert_phase_traceability(output_dir)
        assert_no_raw_bidv(output_dir)

        approved_root = ROOT / "artifacts" / "default" / "approved" / "PAYGATES_E2E" / "Squad_Base" / "API_AUTOMATION"
        reviewed_root = ROOT / "artifacts" / "default" / "reviewed" / "PAYGATES_E2E" / "Squad_Base" / "API_AUTOMATION"
        archive_root = ROOT / "artifacts" / "default" / "archive" / "PAYGATES_E2E" / "Squad_Base" / "API_AUTOMATION"
        rejected_root = ROOT / "artifacts" / "default" / "rejected" / "PAYGATES_E2E" / "Squad_Base" / "API_AUTOMATION"
        for root in [approved_root, reviewed_root, archive_root, rejected_root]:
            shutil.rmtree(root, ignore_errors=True)

        try:
            loop_result = run_closed_loop(
                "--manifest",
                str(manifest),
                "--route-id",
                "testcase_to_api_automation",
                "--output-dir",
                str(output_dir),
                "--project",
                "PAYGATES_E2E",
                "--squad",
                "Squad_Base",
                "--epic",
                "API_AUTOMATION",
            )
            assert_true(loop_result.returncode == 0, loop_result.stdout + loop_result.stderr)
            payload = json.loads(loop_result.stdout)
            assert_true(payload["status"] == "passed", str(payload))
            assert_true(payload["lifecycle_state"] == "approved", str(payload))
            assert_true(Path(payload["approved_artifact_path"]).exists(), "approved artifact missing")
            assert_true((output_dir / "published-artifact-manifest.yml").exists(), "published manifest missing")
        finally:
            for root in [approved_root, reviewed_root, archive_root, rejected_root]:
                shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    test_api_automation_e2e_workflow_generates_valid_approved_artifacts()
    print("test_e2e_api_automation_workflow: PASS")
