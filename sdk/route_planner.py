from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any

from intent_classifier import IntentClassification


@dataclass
class RouteStage:
    id: str
    kind: str
    prompt: str | None = None
    outputs: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)


@dataclass
class RoutePlan:
    schema_version: str
    workflow_pack: str
    route_id: str
    confidence: float
    source_roles: list[str]
    prompt_intents: list[str]
    stages: list[RouteStage]
    final_outputs: list[str]
    support_outputs: list[str] = field(default_factory=lambda: ["source_manifest.json", "route_plan.json", "validation_report.json", "handoff_summary.md"])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def needs_generation_matrix(route_id: str, final_outputs: list[str]) -> bool:
    route_blob = " ".join([route_id, *final_outputs]).lower()
    return any(token in route_blob for token in ["test_design", "testcase", "coverage", "gap"])


def plan_route(workflow: dict[str, Any], classification: IntentClassification, pack_id: str = "default") -> RoutePlan:
    routes = workflow.get("routes", {})
    route = routes.get(classification.request_type)
    if route is None:
        available = ", ".join(sorted(routes)) or "<none>"
        raise ValueError(f"No route found for request type {classification.request_type!r} in workflow pack {pack_id!r}. Available routes: {available}")
    stage_defs = workflow.get("stages", {})
    stages: list[RouteStage] = []
    for stage_id in route.get("stages", []):
        definition = stage_defs.get(stage_id, {})
        stages.append(RouteStage(
            id=stage_id,
            kind=definition.get("kind", "agent"),
            prompt=definition.get("prompt"),
            outputs=definition.get("outputs", []),
            validators=definition.get("validators", []),
        ))
    final_outputs = route.get("final_outputs", [])
    support_outputs = ["source_manifest.json", "route_plan.json", "validation_report.json", "handoff_summary.md"]
    if needs_generation_matrix(classification.request_type, final_outputs) and "CoverageMatrix.md" not in final_outputs:
        support_outputs.append("CoverageMatrix.md")
    return RoutePlan(
        schema_version="1.0",
        workflow_pack=pack_id,
        route_id=classification.request_type,
        confidence=classification.confidence,
        source_roles=classification.source_roles,
        prompt_intents=classification.prompt_intents,
        stages=stages,
        final_outputs=final_outputs,
        support_outputs=support_outputs,
    )
