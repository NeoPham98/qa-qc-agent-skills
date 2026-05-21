from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import base64
import csv
import json
import os
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass
class TestRailConfig:
    base_url: str
    username: str
    api_key: str
    project_id: str
    suite_id: str | None = None


class TestRailClient:
    def __init__(self, config: TestRailConfig) -> None:
        self.config = config
        self.base_url = config.base_url.rstrip("/")
        token = base64.b64encode(f"{config.username}:{config.api_key}".encode("utf-8")).decode("ascii")
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }

    def request(self, method: str, endpoint: str, payload: dict[str, Any] | None = None) -> Any:
        data = json.dumps(payload or {}).encode("utf-8") if payload is not None else None
        req = Request(f"{self.base_url}/index.php?/api/v2/{endpoint}", data=data, headers=self.headers, method=method)
        with urlopen(req) as response:
            body = response.read().decode("utf-8")
        return json.loads(body) if body else None

    def get_sections(self) -> list[dict[str, Any]]:
        params = {"project_id": self.config.project_id}
        if self.config.suite_id:
            params["suite_id"] = self.config.suite_id
        data = self.request("GET", f"get_sections/{self.config.project_id}&{urlencode(params)}")
        return data.get("sections", data) if isinstance(data, dict) else data

    def add_section(self, name: str) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": name}
        if self.config.suite_id:
            payload["suite_id"] = self.config.suite_id
        return self.request("POST", f"add_section/{self.config.project_id}", payload)

    def get_cases(self, section_id: int) -> list[dict[str, Any]]:
        params = {"section_id": section_id}
        if self.config.suite_id:
            params["suite_id"] = self.config.suite_id
        data = self.request("GET", f"get_cases/{self.config.project_id}&{urlencode(params)}")
        return data.get("cases", data) if isinstance(data, dict) else data

    def add_case(self, section_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", f"add_case/{section_id}", payload)

    def update_case(self, case_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", f"update_case/{case_id}", payload)


def load_testrail_config_from_env() -> TestRailConfig:
    base_url = os.environ.get("TESTRAIL_BASE_URL", "").strip()
    username = os.environ.get("TESTRAIL_USERNAME", "").strip()
    api_key = os.environ.get("TESTRAIL_API_KEY", "").strip()
    project_id = os.environ.get("TESTRAIL_PROJECT_ID", "").strip()
    suite_id = os.environ.get("TESTRAIL_SUITE_ID", "").strip() or None

    missing = [
        name
        for name, value in [
            ("TESTRAIL_BASE_URL", base_url),
            ("TESTRAIL_USERNAME", username),
            ("TESTRAIL_API_KEY", api_key),
            ("TESTRAIL_PROJECT_ID", project_id),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing TestRail env vars: {', '.join(missing)}")

    return TestRailConfig(
        base_url=base_url,
        username=username,
        api_key=api_key,
        project_id=project_id,
        suite_id=suite_id,
    )


def load_import_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise RuntimeError("TestRail import CSV has no header")
        rows = list(reader)
    if not rows:
        raise RuntimeError("TestRail import CSV contains no testcase rows")
    return rows


def find_or_create_section(client: TestRailClient, name: str, cache: dict[str, int]) -> int:
    normalized = name.strip() or "Generated"
    if normalized in cache:
        return cache[normalized]
    for section in client.get_sections():
        if section.get("name") == normalized:
            cache[normalized] = int(section["id"])
            return cache[normalized]
    created = client.add_section(normalized)
    cache[normalized] = int(created["id"])
    return cache[normalized]


def find_case_by_external_id(client: TestRailClient, section_id: int, external_id: str) -> dict[str, Any] | None:
    marker = f"[{external_id}]"
    for case in client.get_cases(section_id):
        title = str(case.get("title", ""))
        refs = str(case.get("refs", ""))
        if marker in title or external_id == refs or external_id in refs:
            return case
    return None


def case_payload(row: dict[str, str]) -> dict[str, Any]:
    external_id = row.get("External ID", "").strip()
    title = row.get("Title", "").strip() or external_id
    if external_id and not title.startswith(f"[{external_id}]"):
        title = f"[{external_id}] {title}"
    return {
        "title": title,
        "custom_preconds": row.get("Preconditions", ""),
        "custom_steps": row.get("Steps", ""),
        "custom_expected": row.get("Expected Result", ""),
        "refs": external_id,
    }


def publish_testcases_from_import_csv(
    csv_path: Path,
    *,
    config: TestRailConfig,
    approved: bool,
    mode: str = "api",
) -> list[dict[str, Any]]:
    if not approved:
        raise RuntimeError("TestRail write-back requires explicit approval via --write-back-testrail")

    rows = load_import_rows(csv_path)
    if mode != "api":
        return [{"mode": mode, "rows": len(rows), "csv": str(csv_path)}]

    client = TestRailClient(config)
    section_cache: dict[str, int] = {}
    results: list[dict[str, Any]] = []
    for row in rows:
        external_id = row.get("External ID", "").strip()
        if not external_id:
            raise RuntimeError("TestRail import row missing External ID")
        section_id = find_or_create_section(client, row.get("Section", "Generated"), section_cache)
        payload = case_payload(row)
        existing = find_case_by_external_id(client, section_id, external_id)
        if existing:
            updated = client.update_case(int(existing["id"]), payload)
            results.append({"action": "updated", "external_id": external_id, "case_id": updated.get("id", existing.get("id"))})
        else:
            created = client.add_case(section_id, payload)
            results.append({"action": "created", "external_id": external_id, "case_id": created.get("id")})
    return results
