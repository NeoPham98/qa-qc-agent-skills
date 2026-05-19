from __future__ import annotations

from route_planner import RoutePlan


def infer_final_outputs(plan: RoutePlan) -> list[str]:
    outputs: list[str] = []
    for output in plan.final_outputs:
        if output not in outputs:
            outputs.append(output)
    return outputs


def user_facing_outputs(plan: RoutePlan) -> list[str]:
    return [output for output in infer_final_outputs(plan) if output not in {"OutputReview.md"}]
