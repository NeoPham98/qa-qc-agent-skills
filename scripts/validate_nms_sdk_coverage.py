#!/usr/bin/env python3
"""Cross-check generated API testcases against NMS SDK endpoint metadata."""

from __future__ import annotations

import argparse
import ast
import csv
from pathlib import Path


def parse_endpoints(path: Path) -> dict[str, dict[str, object]]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    endpoints: dict[str, dict[str, object]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "ENDPOINTS" and isinstance(node.value, ast.List):
                    for item in node.value.elts:
                        if not isinstance(item, ast.Call):
                            continue
                        data: dict[str, object] = {"required_fields": [], "business_errors": {}}
                        if len(item.args) >= 2 and isinstance(item.args[1], ast.Constant):
                            data["path"] = item.args[1].value
                        for kw in item.keywords:
                            if kw.arg == "required_fields" and isinstance(kw.value, ast.List):
                                data["required_fields"] = [elt.value for elt in kw.value.elts if isinstance(elt, ast.Constant)]
                            elif kw.arg == "business_errors" and isinstance(kw.value, ast.Dict):
                                data["business_errors"] = {
                                    k.value: v.value
                                    for k, v in zip(kw.value.keys, kw.value.values)
                                    if isinstance(k, ast.Constant) and isinstance(v, ast.Constant)
                                }
                        path_value = data.get("path")
                        if isinstance(path_value, str):
                            endpoints[path_value] = data
    return endpoints


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated testcase coverage against NMS SDK endpoint metadata")
    parser.add_argument("--testcase", type=Path, required=True)
    parser.add_argument("--endpoints", type=Path, required=True)
    parser.add_argument("--schemas", type=Path)
    parser.add_argument("--include-endpoint", action="append", dest="included_endpoints", help="Endpoint path to validate; repeatable. Defaults to every SDK endpoint.")
    parser.add_argument("--require-complete-errors", action="store_true", help="Require every SDK business error to appear in testcase output. By default this is warning-only.")
    args = parser.parse_args()

    endpoints = parse_endpoints(args.endpoints)
    if args.included_endpoints:
        requested = {endpoint.replace("C:/Program Files/Git", "", 1) for endpoint in args.included_endpoints}
        requested = {endpoint[1:] if endpoint.startswith("//") else endpoint for endpoint in requested}
        endpoints = {path: spec for path, spec in endpoints.items() if path in requested}
    with args.testcase.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    errors: list[str] = []
    warnings: list[str] = []
    for path, spec in endpoints.items():
        matching = [row for row in rows if path in " ".join(row.values())]
        if not matching:
            errors.append(f"missing testcase coverage for endpoint {path}")
            continue
        endpoint_blob = "\n".join(" ".join(row.values()) for row in matching)
        for field in spec.get("required_fields", []):
            if field not in endpoint_blob:
                errors.append(f"{path}: required field not referenced: {field}")
        for code, name in dict(spec.get("business_errors", {})).items():
            if code not in endpoint_blob and name not in endpoint_blob:
                message = f"{path}: business error not referenced: {code}={name}"
                if args.require_complete_errors:
                    errors.append(message)
                else:
                    warnings.append(message)

    if warnings:
        print("NMS SDK coverage warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("NMS SDK coverage validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"NMS SDK coverage validation passed ({len(endpoints)} endpoints checked, {len(rows)} testcase rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
