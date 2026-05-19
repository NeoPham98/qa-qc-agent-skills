from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
        check=False,
    )


LEGACY_19_HEADER = [
    "Test Case ID",
    "Function",
    "Group Tests",
    "Scenario Outline",
    "Test Case Summary",
    "Pre-conditions",
    "Test Datas",
    "Test Steps",
    "Expected result",
    "Environment",
    "Priority",
    "Regression",
    "Automation",
    "Manual Test Results Round 1",
    "Manual Test Results Round 2",
    "Automation Test Results",
    "Actual result",
    "BugID",
    "Notes",
]


UAT_16_HEADER = [
    "Test Case ID",
    "Test Case Name",
    "Precondition",
    "Test Steps",
    "Test Data",
    "Expected Result",
    "Priority",
    "Test Type",
    "Module",
    "Requirement ID",
    "Execution Result",
    "Actual Result",
    "Bug ID",
    "Tester",
    "Execution Date",
    "Notes",
]


def write_quoted_tsv(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    lines = ["\t".join(f'"{cell}"' for cell in headers)]
    lines.extend("\t".join(f'"{cell}"' for cell in row) for row in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def legacy_row(tc_id: str, summary: str, data: str, steps: str, expected: str, group: str = "Granularity") -> list[str]:
    return [
        tc_id,
        "PAYGATES",
        group,
        summary,
        summary,
        "User and test data are available",
        data,
        steps,
        expected,
        "SIT",
        "High",
        "Yes",
        "No",
        "",
        "",
        "",
        "",
        "",
        "",
    ]


def coverage_row(category: str, tc_id: str | None = None, detail: str | None = None) -> list[str]:
    safe_category = category.lower().replace("_", " ")
    tc_id = tc_id or f"TD_P1_001_TC_{len(category):03d}"
    detail = detail or f"{safe_category} coverage check"
    return legacy_row(
        tc_id,
        f"Coverage: {category}; Primary Condition: {detail}; Source: tester-standard obligation",
        f"Coverage: {category}\nPrimary Condition: {detail}\nSource: [ASSUMPTION: tester-standard behavior]",
        f"1. Execute {detail}",
        f"Expected result for {detail}",
        group="Coverage Matrix",
    )


def uat_row(tc_id: str, name: str, data: str, expected: str) -> list[str]:
    return [
        tc_id,
        name,
        "Business request is available",
        "1. Login as business user\\n2. Open request\\n3. Execute business action",
        data,
        expected,
        "High",
        "UAT",
        "PAYGATES Approval",
        "REQ-PAY-001",
        "",
        "",
        "",
        "",
        "",
        "",
    ]


def test_validate_normalized_knowledge_flags_missing_metadata_and_secrets(tmp_path: Path) -> None:
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "bad.md").write_text("# Missing metadata\n\npassword=secret123\n", encoding="utf-8")

    result = run_script("validate_normalized_knowledge.py", "--input", str(knowledge))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("missing metadata front matter" in error for error in payload["errors"])


def test_validate_test_design_accepts_api_and_ui_contracts(tmp_path: Path) -> None:
    api = tmp_path / "API_TestDesign.md"
    api.write_text(
        "# POST /cards\n\n"
        "### TD_P1_001 - Header validation\n"
        "- METHOD_CHECK\n- CONTENT_TYPE_CHECK\n- MANDATORY_CHECK\n- TYPE_CHECK\n- LENGTH_CHECK\n- SCOPE_FIELDS\n- EG_CHECK\n"
        "- **Steps**: Verify POST /cards with valid header\n"
        "- **Expected**: HTTP Status: 200 and response code success\n"
        "- Source: RSD section 1\n\n"
        "### TD_P2_001 - Schema validation\n"
        "- **Steps**: Verify request body field type and required enum\n"
        "- **Expected**: HTTP Status: 400 when body field format is invalid\n"
        "- Source: API schema\n\n"
        "### TD_P3_001 - Business rule validation\n"
        "- **Steps**: Verify business rule when trạng thái is invalid\n"
        "- **Expected**: HTTP Status: 409 and lỗi code returned\n"
        "- Source: Business rule matrix\n",
        encoding="utf-8",
    )
    ui = tmp_path / "UI_TestDesign.md"
    ui.write_text(
        "### TD_001 - [ECP] - Invalid login\n"
        "- **Steps**: Enter invalid password\n"
        "- **Expected**: Error message appears\n"
        "- Source: RSD login flow\n",
        encoding="utf-8",
    )

    api_result = run_script("validate_test_design.py", str(api), "--type", "api")
    ui_result = run_script("validate_test_design.py", str(ui), "--type", "ui")

    assert api_result.returncode == 0, api_result.stdout + api_result.stderr
    assert ui_result.returncode == 0, ui_result.stdout + ui_result.stderr


def test_validate_testcase_contract_flags_alias_headers_and_db_checks(tmp_path: Path) -> None:
    path = tmp_path / "Legacy19TestCase.generated.tsv"
    path.write_text(
        '"Test Case ID"\t"Function"\t"Group Tests"\t"Scenario Outline"\t"Test Case / Summary"\t"Pre-conditions"\t"Test Data"\t"Test Steps"\t"Expected / result"\t"Environment"\t"Priority"\t"Regression"\t"Automation"\t"Manual Test Results / Round 1"\t"Manual Test Results Round 2"\t"Automation Test Results"\t"Actual result"\t"BugID"\t"Notes "\n'
        '"TD_P1_001_TC_001"\t"Cards"\t"Group A"\t"Negative invalid body"\t"Invalid request"\t"Setup"\t"{}"\t"Verify DB state after invalid body"\t"HTTP Status: 400"\t"SIT"\t"High"\t"Yes"\t"No"\t""\t""\t""\t""\t""\t"filled"\n',
        encoding="utf-8",
    )

    result = run_script("validate_testcase_contract.py", str(path), "--profile", "legacy_19_column_testcase")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("header does not match legacy 19-column contract" in error for error in payload["errors"])
    assert any("negative API case must not verify DB" in error for error in payload["errors"])
    assert any("Notes must be empty" in error for error in payload["errors"])


def test_validate_testcase_granularity_accepts_atomic_api_cases(tmp_path: Path) -> None:
    path = tmp_path / "api.tsv"
    write_quoted_tsv(
        path,
        LEGACY_19_HEADER,
        [
            legacy_row(
                "TD_P2_001_TC_001",
                "Primary Condition: requestCif missing",
                "Primary Condition: requestCif missing; requestCif=<omitted>; currency=VND",
                "POST /cards/list with requestCif omitted",
                "HTTP Status: 400; response errors.requestCif is returned",
            ),
            legacy_row(
                "TD_P2_001_TC_002",
                "Primary Condition: requestCif wrong type",
                "Primary Condition: requestCif wrong type; requestCif=12345; currency=VND",
                "POST /cards/list with requestCif as number",
                "HTTP Status: 400; response errors.requestCif type message is returned",
            ),
            legacy_row(
                "TD_P1_001_TC_001",
                "Primary Condition: Content-Type is text/plain",
                "Primary Condition: Content-Type is text/plain; header Content-Type=text/plain",
                "POST /cards/list with Content-Type text/plain",
                "HTTP Status: 415; response message states unsupported media type",
            ),
        ],
    )

    result = run_script("validate_testcase_granularity.py", str(path), "--profile", "api_legacy_19_column_testcase")

    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_testcase_granularity_rejects_bundled_api_case(tmp_path: Path) -> None:
    path = tmp_path / "api-bundled.tsv"
    write_quoted_tsv(
        path,
        LEGACY_19_HEADER,
        [
            legacy_row(
                "TD_P2_001_TC_001",
                "Primary Condition: requestCif missing and currency invalid and accountStatus inactive",
                "Primary Condition: requestCif missing and currency invalid and accountStatus inactive",
                "POST /cards/list with requestCif omitted, currency=XYZ, accountStatus=inactive",
                "HTTP Status: 400; response contains validation errors",
            )
        ],
    )

    result = run_script("validate_testcase_granularity.py", str(path), "--profile", "api_legacy_19_column_testcase")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("bundles multiple independent conditions" in error for error in payload["errors"])


def test_validate_testcase_granularity_accepts_atomic_ui_cases(tmp_path: Path) -> None:
    path = tmp_path / "ui.tsv"
    write_quoted_tsv(
        path,
        LEGACY_19_HEADER,
        [
            legacy_row(
                "TD_001_TC_001",
                "Primary Condition: password wrong",
                "Primary Condition: password wrong; username=maker01; password=wrongpass",
                "Open login screen and submit wrong password",
                "Login is rejected and password error message is shown",
                group="UI Login",
            ),
            legacy_row(
                "TD_002_TC_001",
                "Primary Condition: login button clicked with locked user",
                "Primary Condition: login button clicked with locked user; username=locked01",
                "Open login screen and click Login with locked user credentials",
                "Login is rejected and locked-user message is shown",
                group="UI Login",
            ),
        ],
    )

    result = run_script("validate_testcase_granularity.py", str(path), "--profile", "ui_legacy_19_column_testcase")

    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_testcase_granularity_rejects_bundled_ui_case(tmp_path: Path) -> None:
    path = tmp_path / "ui-bundled.tsv"
    write_quoted_tsv(
        path,
        LEGACY_19_HEADER,
        [
            legacy_row(
                "TD_001_TC_001",
                "Primary Condition: username empty and password empty and login button disabled",
                "Primary Condition: username empty and password empty and login button disabled",
                "Open login screen with username empty and password empty",
                "Login button is disabled and validation messages are shown",
                group="UI Login",
            )
        ],
    )

    result = run_script("validate_testcase_granularity.py", str(path), "--profile", "ui_legacy_19_column_testcase")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("bundles multiple independent conditions" in error for error in payload["errors"])


def test_validate_testcase_granularity_accepts_atomic_uat_case(tmp_path: Path) -> None:
    path = tmp_path / "uat.tsv"
    write_quoted_tsv(
        path,
        UAT_16_HEADER,
        [
            uat_row(
                "UAT_001",
                "Primary Condition: checker approves valid request",
                "Primary Condition: checker approves valid request; request status=Pending approval",
                "Request moves to approved state and audit trail is recorded",
            )
        ],
    )

    result = run_script("validate_testcase_granularity.py", str(path), "--profile", "uat_16_column_testcase")

    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_testcase_granularity_rejects_bundled_uat_case(tmp_path: Path) -> None:
    path = tmp_path / "uat-bundled.tsv"
    write_quoted_tsv(
        path,
        UAT_16_HEADER,
        [
            uat_row(
                "UAT_001",
                "Primary Condition: checker approve and reject and cancel request",
                "Primary Condition: checker approve and reject and cancel request",
                "Request reaches the selected final business state",
            )
        ],
    )

    result = run_script("validate_testcase_granularity.py", str(path), "--profile", "uat_16_column_testcase")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("bundles multiple independent conditions" in error for error in payload["errors"])


def test_validate_testcase_coverage_accepts_complete_api_profile(tmp_path: Path) -> None:
    path = tmp_path / "api-coverage.tsv"
    rows = [
        coverage_row("METHOD", "TD_P1_001_TC_001", "POST method succeeds"),
        coverage_row("CONTENT_TYPE", "TD_P1_002_TC_001", "Content-Type application/json succeeds"),
        coverage_row("AUTH", "TD_P1_003_TC_001", "missing authToken returns authentication error"),
        coverage_row("MANDATORY_HEADERS", "TD_P1_004_TC_001", "missing requestID returns header validation error"),
        coverage_row("LANGUAGE", "TD_P1_005_TC_001", "Accept-language en is accepted"),
        coverage_row("BODY_SCHEMA", "TD_P2_001_TC_001", "requestCif wrong type returns schema error"),
        coverage_row("BOUNDARY", "TD_P2_002_TC_001", "requestCif over max length returns validation error"),
        coverage_row("BUSINESS_ERROR", "TD_P3_001_TC_001", "documented business code 101 returns error"),
        coverage_row("RESPONSE_SCHEMA", "TD_P2_003_TC_001", "success response schema has code 0 and failure response schema has success=false"),
        coverage_row("ERROR_PRIORITY", "TD_P2_004_TC_001", "multiple validation errors return deterministic priority"),
    ]
    write_quoted_tsv(path, LEGACY_19_HEADER, rows)

    result = run_script("validate_testcase_coverage.py", str(path), "--profile", "api_legacy_19_column_testcase")

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] == "passed"
    assert payload["coverage"]["CONTENT_TYPE"] == 1


def test_validate_testcase_coverage_rejects_api_missing_content_type(tmp_path: Path) -> None:
    path = tmp_path / "api-coverage-missing.tsv"
    rows = [
        coverage_row("METHOD", "TD_P1_001_TC_001", "POST method succeeds"),
        coverage_row("AUTH", "TD_P1_003_TC_001", "missing authToken returns authentication error"),
        coverage_row("MANDATORY_HEADERS", "TD_P1_004_TC_001", "missing requestID returns header validation error"),
        coverage_row("LANGUAGE", "TD_P1_005_TC_001", "Accept-language en is accepted"),
        coverage_row("BODY_SCHEMA", "TD_P2_001_TC_001", "requestCif wrong type returns schema error"),
        coverage_row("BOUNDARY", "TD_P2_002_TC_001", "requestCif over max length returns validation error"),
        coverage_row("BUSINESS_ERROR", "TD_P3_001_TC_001", "documented business code 101 returns error"),
        coverage_row("RESPONSE_SCHEMA", "TD_P2_003_TC_001", "success response schema has code 0 and failure response schema has success=false"),
        coverage_row("ERROR_PRIORITY", "TD_P2_004_TC_001", "multiple validation errors return deterministic priority"),
    ]
    write_quoted_tsv(path, LEGACY_19_HEADER, rows)

    result = run_script("validate_testcase_coverage.py", str(path), "--profile", "api_legacy_19_column_testcase")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert "missing required coverage category: CONTENT_TYPE" in payload["errors"]


def test_validate_testcase_coverage_rejects_api_missing_failure_response_schema(tmp_path: Path) -> None:
    path = tmp_path / "api-coverage-response-schema.tsv"
    rows = [
        coverage_row("METHOD", "TD_P1_001_TC_001", "POST method succeeds"),
        coverage_row("CONTENT_TYPE", "TD_P1_002_TC_001", "Content-Type application/json succeeds"),
        coverage_row("AUTH", "TD_P1_003_TC_001", "missing authToken returns authentication error"),
        coverage_row("MANDATORY_HEADERS", "TD_P1_004_TC_001", "missing requestID returns header validation error"),
        coverage_row("LANGUAGE", "TD_P1_005_TC_001", "Accept-language en is accepted"),
        coverage_row("BODY_SCHEMA", "TD_P2_001_TC_001", "requestCif wrong type returns schema error"),
        coverage_row("BOUNDARY", "TD_P2_002_TC_001", "requestCif over max length returns validation error"),
        coverage_row("BUSINESS_ERROR", "TD_P3_001_TC_001", "documented business code 101 returns error"),
        coverage_row("RESPONSE_SCHEMA", "TD_P2_003_TC_001", "success response schema has code 0 and traceId"),
        coverage_row("ERROR_PRIORITY", "TD_P2_004_TC_001", "multiple validation errors return deterministic priority"),
    ]
    write_quoted_tsv(path, LEGACY_19_HEADER, rows)

    result = run_script("validate_testcase_coverage.py", str(path), "--profile", "api_legacy_19_column_testcase")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert "missing required coverage detail: RESPONSE_SCHEMA failure schema" in payload["errors"]


def test_validate_testcase_coverage_accepts_complete_ui_profile(tmp_path: Path) -> None:
    path = tmp_path / "ui-coverage.tsv"
    rows = [
        coverage_row("NAVIGATION", "TD_001_TC_001", "open target screen from menu"),
        coverage_row("FIELD_VALIDATION", "TD_002_TC_001", "invalid field value is rejected"),
        coverage_row("REQUIRED_FIELDS", "TD_003_TC_001", "mandatory field left blank is rejected"),
        coverage_row("FORMAT_VALIDATION", "TD_004_TC_001", "date field wrong format is rejected"),
        coverage_row("BOUNDARY", "TD_005_TC_001", "field over max length is rejected"),
        coverage_row("BUSINESS_RULE", "TD_006_TC_001", "business rule violation is rejected"),
        coverage_row("ROLE_PERMISSION", "TD_007_TC_001", "user without permission cannot submit"),
        coverage_row("STATE_TRANSITION", "TD_008_TC_001", "submit changes status to pending approval"),
        coverage_row("ERROR_MESSAGE", "TD_009_TC_001", "validation error message is displayed"),
        coverage_row("DATA_PERSISTENCE", "TD_010_TC_001", "saved data is displayed after reload"),
        coverage_row("CANCEL_BACK_REFRESH", "TD_011_TC_001", "back action preserves expected state"),
    ]
    write_quoted_tsv(path, LEGACY_19_HEADER, rows)

    result = run_script("validate_testcase_coverage.py", str(path), "--profile", "ui_legacy_19_column_testcase")

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["coverage"]["ROLE_PERMISSION"] == 1


def test_validate_testcase_coverage_rejects_ui_missing_role_permission(tmp_path: Path) -> None:
    path = tmp_path / "ui-coverage-missing.tsv"
    rows = [
        coverage_row("NAVIGATION", "TD_001_TC_001", "open target screen from menu"),
        coverage_row("FIELD_VALIDATION", "TD_002_TC_001", "invalid field value is rejected"),
        coverage_row("REQUIRED_FIELDS", "TD_003_TC_001", "mandatory field left blank is rejected"),
        coverage_row("FORMAT_VALIDATION", "TD_004_TC_001", "date field wrong format is rejected"),
        coverage_row("BOUNDARY", "TD_005_TC_001", "field over max length is rejected"),
        coverage_row("BUSINESS_RULE", "TD_006_TC_001", "business rule violation is rejected"),
        coverage_row("STATE_TRANSITION", "TD_008_TC_001", "submit changes status to pending approval"),
        coverage_row("ERROR_MESSAGE", "TD_009_TC_001", "validation error message is displayed"),
        coverage_row("DATA_PERSISTENCE", "TD_010_TC_001", "saved data is displayed after reload"),
        coverage_row("CANCEL_BACK_REFRESH", "TD_011_TC_001", "back action preserves expected state"),
    ]
    write_quoted_tsv(path, LEGACY_19_HEADER, rows)

    result = run_script("validate_testcase_coverage.py", str(path), "--profile", "ui_legacy_19_column_testcase")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert "missing required coverage category: ROLE_PERMISSION" in payload["errors"]


def test_validate_tracker_reports_aliases_and_formula_warning(tmp_path: Path) -> None:
    sys.path.insert(0, str(SCRIPTS))
    sys.path.insert(0, str(SCRIPTS / "lib"))
    from test_xlsx_profiles import write_fixture_xlsx

    workbook = tmp_path / "Tổng hợp Trạng Thái Test Case Paygates (1).xlsx"
    write_fixture_xlsx(
        workbook,
        ["Feature", "Status", "Generate Type", "Automation Status", "Automation Type"],
        [["VA", "Read to UAT", "AI Gen", "In - Progress", "UI"]],
        "SUMIFS(Squad_VA!A:A,Squad_CnR!B:B,\"Ready\")",
    )

    result = run_script("validate_tracker.py", str(workbook))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("uses alias 'Read to UAT'" in error for error in payload["errors"])
    assert any("formula warning" in error for error in payload["errors"])


def test_validate_artifact_manifest_requires_approved_evidence(tmp_path: Path) -> None:
    manifest = tmp_path / "artifact-manifest.yml"
    manifest.write_text(
        "status: approved\n"
        "supervisor_decision: approved\n"
        "validation_report: reports/validation.json\n"
        "source_trace: reports/source-trace.md\n"
        "files:\n"
        "  OutputReview.md: reports/OutputReview.md\n"
        "  approved_artifact_path: artifacts/default/approved/PAYGATES/out.tsv\n"
        "  previous_approved_artifact_path: artifacts/default/approved/PAYGATES/out.tsv\n",
        encoding="utf-8",
    )

    result = run_script("validate_artifact_manifest.py", str(manifest))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("missing required approved artifact 'SupervisorApproval.md'" in error for error in payload["errors"])
    assert any("missing required evidence 'no_secret_report'" in error for error in payload["errors"])
    assert any("would overwrite existing approved artifact in place" in error for error in payload["errors"])


if __name__ == "__main__":
    import tempfile

    tests = [
        test_validate_normalized_knowledge_flags_missing_metadata_and_secrets,
        test_validate_test_design_accepts_api_and_ui_contracts,
        test_validate_testcase_contract_flags_alias_headers_and_db_checks,
        test_validate_testcase_granularity_accepts_atomic_api_cases,
        test_validate_testcase_granularity_rejects_bundled_api_case,
        test_validate_testcase_granularity_accepts_atomic_ui_cases,
        test_validate_testcase_granularity_rejects_bundled_ui_case,
        test_validate_testcase_granularity_accepts_atomic_uat_case,
        test_validate_testcase_granularity_rejects_bundled_uat_case,
        test_validate_testcase_coverage_accepts_complete_api_profile,
        test_validate_testcase_coverage_rejects_api_missing_content_type,
        test_validate_testcase_coverage_rejects_api_missing_failure_response_schema,
        test_validate_testcase_coverage_accepts_complete_ui_profile,
        test_validate_testcase_coverage_rejects_ui_missing_role_permission,
        test_validate_tracker_reports_aliases_and_formula_warning,
        test_validate_artifact_manifest_requires_approved_evidence,
    ]
    for test in tests:
        with tempfile.TemporaryDirectory() as directory:
            test(Path(directory))
    print("test_validators: PASS")

def test_no_bidv_runtime_refs_blocks_runtime_raw_path(tmp_path: Path) -> None:
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("validate_no_bidv_runtime_refs", ROOT / "scripts" / "validate_no_bidv_runtime_refs.py")
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    artifact = tmp_path / "RuntimeOutput.md"
    artifact.write_text("Use BIDV/Prompt/API/raw.txt during runtime\n", encoding="utf-8")

    errors = module.validate([artifact], {".md"})

    assert errors


def test_no_bidv_runtime_refs_skips_provenance_by_default(tmp_path: Path) -> None:
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("validate_no_bidv_runtime_refs", ROOT / "scripts" / "validate_no_bidv_runtime_refs.py")
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    provenance = tmp_path / "knowledge" / "default" / "manifests" / "normalization-report.json"
    provenance.parent.mkdir(parents=True)
    provenance.write_text('{"source": "BIDV/Prompt/API/raw.txt"}\n', encoding="utf-8")

    assert module.validate([tmp_path / "knowledge"], {".json"}) == []
    assert module.validate([tmp_path / "knowledge"], {".json"}, include_provenance=True)

