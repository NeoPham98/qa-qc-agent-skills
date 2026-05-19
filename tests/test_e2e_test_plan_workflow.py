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
EXAMPLE = ROOT / "examples" / "e2e" / "test-plan"
sys.path.insert(0, str(SDK))

from source_manifest import SourceFingerprint, SourceItem, SourceManifest


FINAL_OUTPUTS = ["TestPlan.md", "TestPlan.generated.xlsx", "OutputReview.md", "SupervisorApproval.md"]


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
        run_id="test-plan-e2e-test",
        user_prompt="Sinh Test Plan cho scope PAYGATES CCTG",
        output_directory=str(output_dir),
        workflow_pack="default",
        sources=[
            SourceItem(
                id="test-plan-source",
                kind="local_file",
                original_locator="examples/e2e/test-plan/TestPlan.md",
                local_path="examples/e2e/test-plan/TestPlan.md",
                extension=".md",
                fingerprint=SourceFingerprint(candidate_roles=["business_requirement", "api_spec"]),
            )
        ],
    )
    manifest.write(path)


def copy_seed_outputs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in ["TestPlan.md", "OutputReview.md", "SupervisorApproval.md"]:
        shutil.copy2(EXAMPLE / name, output_dir / name)


def assert_no_raw_bidv(output_dir: Path) -> None:
    result = run_script("validate_no_bidv_runtime_refs.py", str(output_dir))
    assert_true(result.returncode == 0, result.stdout + result.stderr)


def test_test_plan_e2e_workflow_generates_valid_approved_artifacts() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        output_dir = tmp_path / "out"
        manifest = tmp_path / "source_manifest.json"
        copy_seed_outputs(output_dir)
        write_manifest(manifest, output_dir)

        plan_result = run_script("validate_test_plan.py", str(output_dir / "TestPlan.md"))
        assert_true(plan_result.returncode == 0, plan_result.stdout + plan_result.stderr)
        assert_no_raw_bidv(output_dir)

        export_tp_result = run_script(
            "export_test_plan_xlsx.py",
            str(output_dir / "TestPlan.md"),
            str(output_dir / "TestPlan.generated.xlsx"),
        )
        assert_true(export_tp_result.returncode == 0, export_tp_result.stdout + export_tp_result.stderr)

        approved_root = ROOT / "artifacts" / "default" / "approved" / "PAYGATES_E2E" / "Squad_Base" / "TEST_PLAN"
        reviewed_root = ROOT / "artifacts" / "default" / "reviewed" / "PAYGATES_E2E" / "Squad_Base" / "TEST_PLAN"
        archive_root = ROOT / "artifacts" / "default" / "archive" / "PAYGATES_E2E" / "Squad_Base" / "TEST_PLAN"
        rejected_root = ROOT / "artifacts" / "default" / "rejected" / "PAYGATES_E2E" / "Squad_Base" / "TEST_PLAN"
        for root in [approved_root, reviewed_root, archive_root, rejected_root]:
            shutil.rmtree(root, ignore_errors=True)

        try:
            loop_result = run_closed_loop(
                "--manifest",
                str(manifest),
                "--route-id",
                "source_to_test_plan",
                "--output-dir",
                str(output_dir),
                "--project",
                "PAYGATES_E2E",
                "--squad",
                "Squad_Base",
                "--epic",
                "TEST_PLAN",
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
    test_test_plan_e2e_workflow_generates_valid_approved_artifacts()
    print("test_e2e_test_plan_workflow: PASS")
