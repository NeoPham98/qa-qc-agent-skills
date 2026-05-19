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
sys.path.insert(0, str(SDK))

from source_manifest import SourceFingerprint, SourceItem, SourceManifest


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "run_closed_loop.py"), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def write_manifest(path: Path, role: str = "api_spec") -> None:
    manifest = SourceManifest(
        schema_version="1.0",
        run_id="loop-test",
        user_prompt="Sinh testcase BIDV 19 cột",
        output_directory=str(path.parent / "out"),
        workflow_pack="default",
        sources=[
            SourceItem(
                id="source-1",
                kind="local_file",
                original_locator="input.md",
                local_path="input.md",
                extension=".md",
                fingerprint=SourceFingerprint(candidate_roles=[role]),
            )
        ],
    )
    manifest.write(path)


def write_success_outputs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "API_OperationInventory.md").write_text("# Inventory\n", encoding="utf-8")
    (output_dir / "API_TestDesign.md").write_text(
        "# API TD\n\n"
        "## POST /cards/check\n\n"
        "### TD_P1_001 - Header validation\n"
        "- METHOD_CHECK\n- CONTENT_TYPE_CHECK\n- MANDATORY_CHECK\n- TYPE_CHECK\n- LENGTH_CHECK\n- SCOPE_FIELDS\n- EG_CHECK\n"
        "- **Steps**: Send POST /cards/check with AuthToken, requestID, Accept-Language, Content-Type, and valid body.\n"
        "- **Expected**: HTTP Status: 200; response body contains code, message, success=true, and data.\n"
        "- Source: RSD section 1\n\n"
        "### TD_P2_001 - Schema validation\n"
        "- **Steps**: Send POST /cards/check with customerId as number instead of string.\n"
        "- **Expected**: HTTP Status: 400; response body contains code, message, and errors.customerId.\n"
        "- Source: API schema\n\n"
        "### TD_P3_001 - Business rule validation\n"
        "- **Steps**: Send POST /cards/check for customerState=CLOSED.\n"
        "- **Expected**: HTTP Status: 409; response body contains documented business error code and message.\n"
        "- Source: Business rule matrix\n",
        encoding="utf-8",
    )
    (output_dir / "TestCaseSource.md").write_text(
        "# TestCase Source\n\n"
        "## TD_P1_001_TC_001\n"
        "- Test Case ID: TD_P1_001_TC_001\n"
        "- Primary Condition: valid request success\n"
        "- Pre-conditions: SIT environment; POST /cards/check is available; AuthToken is valid.\n"
        "- Test Datas: Headers AuthToken=<token>, requestID=REQ-001, Accept-Language=vi, Content-Type=application/json; Body contains valid customerId.\n"
        "- Test Steps: Send POST /cards/check with the valid headers and body.\n"
        "- Expected result: HTTP Status: 200; response body contains code, message, success=true, and data.\n\n"
        "## TD_P2_001_TC_001\n"
        "- Test Case ID: TD_P2_001_TC_001\n"
        "- Primary Target: customerId request body field wrong type\n"
        "- Pre-conditions: SIT environment; POST /cards/check is available; AuthToken is valid.\n"
        "- Test Datas: Headers valid; Body customerId=12345 where schema expects string.\n"
        "- Test Steps: Send POST /cards/check with customerId as number.\n"
        "- Expected result: HTTP Status: 400; response body contains code, message, and errors.customerId.\n\n"
        "## TD_P3_001_TC_001\n"
        "- Test Case ID: TD_P3_001_TC_001\n"
        "- Atomic Target: documented business conflict for CLOSED customer state\n"
        "- Pre-conditions: SIT environment; POST /cards/check is available; customer state is CLOSED.\n"
        "- Test Datas: Headers valid; Body customerState=CLOSED.\n"
        "- Test Steps: Send POST /cards/check for a CLOSED customer.\n"
        "- Expected result: HTTP Status: 409; response body contains documented business error code and message.\n",
        encoding="utf-8",
    )
    (output_dir / "Legacy19TestCase.generated.tsv").write_text(
        '"Test Case ID"\t"Function"\t"Group Tests"\t"Scenario Outline"\t"Test Case Summary"\t"Pre-conditions"\t"Test Datas"\t"Test Steps"\t"Expected result"\t"Environment"\t"Priority"\t"Regression"\t"Automation"\t"Manual Test Results Round 1"\t"Manual Test Results Round 2"\t"Automation Test Results"\t"Actual result"\t"BugID"\t"Notes"\n'
        '"TD_P1_001_TC_001"\t"POST /cards/check"\t"Coverage: METHOD"\t"Happy path"\t"POST /cards/check - Primary Condition: valid request success"\t"Env SIT; Endpoint /cards/check"\t"Headers: AuthToken=<token>, requestID=REQ-001, Accept-Language=vi, Content-Type=application/json; Body: {valid body}"\t"Verify POST /cards/check returns success for valid request"\t"HTTP Status: 200; success response schema has code, message, traceId and data"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P1_002_TC_001"\t"POST /cards/check"\t"Coverage: CONTENT_TYPE"\t"Invalid content type"\t"POST /cards/check - Primary Condition: unsupported content type"\t"Env SIT; Endpoint /cards/check"\t"Headers: AuthToken=<token>, requestID=REQ-002, Accept-Language=vi, Content-Type=text/plain; Body: {valid body}"\t"Verify POST /cards/check rejects unsupported Content-Type header"\t"HTTP Status: 415; failure response has error code and message for content type"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P1_003_TC_001"\t"POST /cards/check"\t"Coverage: AUTH"\t"Auth token absent"\t"POST /cards/check - Primary Condition: auth token absent"\t"Env SIT; Endpoint /cards/check"\t"Headers: requestID=REQ-003, Accept-Language=vi, Content-Type=application/json; Body: {valid body}"\t"Verify POST /cards/check rejects request without AuthToken header"\t"HTTP Status: 401; failure response has error code and message for auth header"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P1_004_TC_001"\t"POST /cards/check"\t"Coverage: MANDATORY_HEADERS"\t"Request id absent"\t"POST /cards/check - Primary Condition: requestID header absent"\t"Env SIT; Endpoint /cards/check"\t"Headers: AuthToken=<token>, Accept-Language=vi, Content-Type=application/json; Body: {valid body}"\t"Verify POST /cards/check rejects request without requestID header"\t"HTTP Status: 400; failure response has error code and message for header"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P1_005_TC_001"\t"POST /cards/check"\t"Coverage: LANGUAGE"\t"Unsupported language"\t"POST /cards/check - Primary Condition: unsupported Accept-Language"\t"Env SIT; Endpoint /cards/check"\t"Headers: AuthToken=<token>, requestID=REQ-005, Accept-Language=zz, Content-Type=application/json; Body: {valid body}"\t"Verify POST /cards/check rejects unsupported language header"\t"HTTP Status: 400; failure response has error code and message for language"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P2_001_TC_001"\t"POST /cards/check"\t"Coverage: BODY_SCHEMA"\t"Invalid body type"\t"POST /cards/check - Primary Condition: request field wrong type"\t"Env SIT; Endpoint /cards/check"\t"Headers: valid; Body: {customerId: 12345}; expected string field"\t"Verify POST /cards/check rejects request body field wrong type"\t"HTTP Status: 400; success response schema and failure response body have code, message, errors and traceId"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P2_002_TC_001"\t"POST /cards/check"\t"Coverage: BOUNDARY"\t"Below min length"\t"POST /cards/check - Primary Condition: customerId below min length"\t"Env SIT; Endpoint /cards/check"\t"Headers: valid; Body: {customerId: A}; boundary min length - 1"\t"Verify POST /cards/check rejects customerId below min boundary"\t"HTTP Status: 400; failure response has validation code and message for boundary"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P2_003_TC_001"\t"POST /cards/check"\t"Coverage: RESPONSE_SCHEMA"\t"Failure envelope"\t"POST /cards/check - Primary Condition: failure response schema"\t"Env SIT; Endpoint /cards/check"\t"Headers: valid; Body: {malformed json}"\t"Verify POST /cards/check success response schema reference and failure response schema for malformed json"\t"HTTP Status: 400; failure response body has code, message, errors, traceId and responseTime"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P3_001_TC_001"\t"POST /cards/check"\t"Coverage: BUSINESS_ERROR"\t"Business conflict"\t"POST /cards/check - Primary Condition: documented business conflict"\t"Env SIT; Endpoint /cards/check"\t"Headers: valid; Body: {customerState: CLOSED}; business rule invalid state"\t"Verify POST /cards/check rejects customer with invalid state"\t"HTTP Status: 409; failure response has documented business error code and message"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n'
        '"TD_P3_002_TC_001"\t"POST /cards/check"\t"Coverage: ERROR_PRIORITY"\t"Multiple errors priority"\t"POST /cards/check - Primary Condition: auth error priority over body error"\t"Env SIT; Endpoint /cards/check"\t"Headers: no AuthToken; Body: {customerId: 12345}; multiple invalid inputs"\t"Verify POST /cards/check returns priority auth error before body validation"\t"HTTP Status: 401; failure response has priority error code and message"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t""\n',
        encoding="utf-8",
    )
    (output_dir / "Legacy19TestCase.generated.xlsx").write_text("placeholder xlsx", encoding="utf-8")
    (output_dir / "CoverageMatrix.md").write_text(
        '# Coverage Matrix\n\n'
        '| Matrix Row ID | Source Ref | Source Kind | Field Or Rule | Rule Type | Technique | Value Class | TD ID | Test Case ID | Coverage Status | Rationale |\n'
        '|---|---|---|---|---|---|---|---|---|---|---|\n'
        '| MTRX-001 | spec#method | api_spec | POST /cards/check method | method | ECP | valid | TD_P1_001 | TD_P1_001_TC_001 | covered | Valid method happy path. |\n'
        '| MTRX-002 | spec#header | api_spec | requestID header | required | ECP | missing | TD_P1_002 | TD_P1_002_TC_001 | covered | Missing required header negative case. |\n'
        '| MTRX-003 | spec#body | api_spec | customerId type | type | ECP | wrong_type | TD_P2_001 | TD_P2_001_TC_001 | covered | Wrong type schema validation. |\n'
        '| MTRX-004 | spec#boundary | api_spec | customerId min length | boundary | BVA | min-1 | TD_P2_002 | TD_P2_002_TC_001 | covered | Below boundary validation. |\n'
        '| MTRX-005 | spec#business | api_spec | customer state | business | DT | invalid_state | TD_P3_001 | TD_P3_001_TC_001 | covered | Documented business conflict. |\n',
        encoding="utf-8",
    )
    (output_dir / "OutputReview.md").write_text("# Output Review\n\n- Severity: minor\n- Summary: Reviewed and acceptable.\n", encoding="utf-8")
    (output_dir / "SupervisorApproval.md").write_text("# Supervisor Approval\n\n- Decision: approved\n- Reason: All gates passed.\n", encoding="utf-8")


def write_retry_outputs(output_dir: Path) -> None:
    write_success_outputs(output_dir)
    (output_dir / "SupervisorApproval.md").write_text("# Supervisor Approval\n\n- Decision: retry_required\n- Reason: Needs revision.\n", encoding="utf-8")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_closed_loop_promotes_reviewed_and_approved_artifacts() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        manifest = tmp_path / "source_manifest.json"
        write_manifest(manifest)
        output_dir = tmp_path / "out"
        write_success_outputs(output_dir)

        result = run_script(
            "--manifest", str(manifest),
            "--route-id", "api_spec_to_testcase",
            "--output-dir", str(output_dir),
            "--project", "PAYGATES",
            "--squad", "Squad_Base",
            "--epic", "CCTG",
        )

        assert_true(result.returncode == 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        assert_true(payload["status"] == "passed", str(payload))
        assert_true(payload["lifecycle_state"] == "approved", str(payload))
        assert_true((output_dir / "published-artifact-manifest.yml").exists(), "manifest missing")
        assert_true((output_dir / "closed-loop-state.json").exists(), "state missing")
        assert_true(Path(payload["approved_artifact_path"]).exists(), "approved artifact missing")
        assert_true(Path(payload["reviewed_artifact_path"]).exists(), "reviewed artifact missing")


def test_closed_loop_rejects_after_retry_limit() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        manifest = tmp_path / "source_manifest.json"
        write_manifest(manifest)
        output_dir = tmp_path / "out"
        write_retry_outputs(output_dir)
        (output_dir / "Legacy19TestCase.generated.tsv").write_text(
            '"Test Case ID"\t"Function"\t"Group Tests"\t"Scenario Outline"\t"Test Case / Summary"\t"Pre-conditions"\t"Test Data"\t"Test Steps"\t"Expected / result"\t"Environment"\t"Priority"\t"Regression"\t"Automation"\t"Manual Test Results / Round 1"\t"Manual Test Results Round 2"\t"Automation Test Results"\t"Actual result"\t"BugID"\t"Notes "\n'
            '"TD_P1_001_TC_001"\t"Cards"\t"Group A"\t"Negative invalid body"\t"Invalid request"\t"Setup"\t"{}"\t"Verify DB state after invalid body"\t"HTTP Status: 400"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t"filled"\n',
            encoding="utf-8",
        )

        result = run_script(
            "--manifest", str(manifest),
            "--route-id", "api_spec_to_testcase",
            "--output-dir", str(output_dir),
            "--project", "PAYGATES",
            "--squad", "Squad_Base",
            "--epic", "CCTG",
            "--retry-count", "2",
        )

        assert_true(result.returncode == 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        assert_true(payload["lifecycle_state"] == "rejected", str(payload))
        assert_true(Path(payload["rejected_artifact_path"]).exists(), "rejected artifact missing")


def test_closed_loop_archives_previous_approved_artifact_before_replace() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        manifest = tmp_path / "source_manifest.json"
        write_manifest(manifest)
        output_dir = tmp_path / "out"
        write_success_outputs(output_dir)

        approved_root = ROOT / "artifacts" / "default" / "approved" / "PAYGATES" / "Squad_Base" / "CCTG"
        archive_root = ROOT / "artifacts" / "default" / "archive" / "PAYGATES" / "Squad_Base" / "CCTG"
        shutil.rmtree(approved_root, ignore_errors=True)
        shutil.rmtree(archive_root, ignore_errors=True)
        approved_dir = approved_root / "md"
        approved_dir.mkdir(parents=True, exist_ok=True)
        existing = approved_dir / "API_TestDesign.md"
        existing.write_text("old approved", encoding="utf-8")

        result = run_script(
            "--manifest", str(manifest),
            "--route-id", "api_spec_to_testcase",
            "--output-dir", str(output_dir),
            "--project", "PAYGATES",
            "--squad", "Squad_Base",
            "--epic", "CCTG",
        )

        assert_true(result.returncode == 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        assert_true(bool(payload["archived"]), str(payload))
        assert_true(archive_root.exists(), "archive root missing")
        assert_true(any(path.name.startswith("API_TestDesign.") for path in (archive_root / "md").iterdir()), "archived copy missing")

        shutil.rmtree(approved_root, ignore_errors=True)
        shutil.rmtree(archive_root, ignore_errors=True)


if __name__ == "__main__":
    test_closed_loop_promotes_reviewed_and_approved_artifacts()
    test_closed_loop_rejects_after_retry_limit()
    test_closed_loop_archives_previous_approved_artifact_before_replace()
    print("test_supervisor_loop: PASS")
