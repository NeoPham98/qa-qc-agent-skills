from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_status_enums(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def aliases(config: dict) -> dict[str, str]:
    merged: dict[str, str] = {}
    for domain in config["status_domains"].values():
        merged.update(domain.get("aliases", {}))
    return merged


def test_status_enum_aliases_normalize_known_values() -> None:
    config = load_status_enums(ROOT / "workflow-packs" / "default" / "status-enums.yml")
    known_aliases = aliases(config)

    assert known_aliases["Read to UAT"] == "Ready to UAT"
    assert known_aliases["AI Gen"] == "AI gen"
    assert known_aliases["In - Progress"] == "In-Progress"
    assert known_aliases["UI"] == "Web UI"


def test_status_enum_config_keeps_canonical_values() -> None:
    config = load_status_enums(ROOT / "workflow-packs" / "default" / "status-enums.yml")

    tracker_values = config["status_domains"]["tracker_status"]["canonical_values"]
    generate_type_values = config["status_domains"]["testcase_generate_type"]["canonical_values"]
    automation_status_values = config["status_domains"]["automation_status"]["canonical_values"]
    automation_type_values = config["status_domains"]["automation_type"]["canonical_values"]

    assert tracker_values == [
        "Ready to UAT",
        "Pending",
        "In-Test",
        "Update test cases",
        "Test case out of date",
        "Completed",
        "In-Progress",
    ]
    assert generate_type_values == ["AI gen", "Manual", "AI gen + Manual"]
    assert automation_status_values == ["Not Started", "In-Progress", "Completed", "N/A"]
    assert automation_type_values == ["API", "Web UI"]


def test_status_enum_validation_policy_warns_on_aliases_and_fails_unknowns() -> None:
    config = load_status_enums(ROOT / "workflow-packs" / "default" / "status-enums.yml")

    for domain in config["status_domains"].values():
        policy = domain["validation_policy"]
        assert policy["alias_usage"] == "warn"
        assert policy["unknown_value"] == "fail_final_artifact"


def test_knowledge_schema_matches_runtime_status_enums() -> None:
    runtime = load_status_enums(ROOT / "workflow-packs" / "default" / "status-enums.yml")
    knowledge = load_status_enums(ROOT / "knowledge" / "default" / "schemas" / "status-enums.yml")

    assert knowledge["status_domains"] == runtime["status_domains"]
    assert knowledge["source"] == "workflow-packs/default/status-enums.yml"
