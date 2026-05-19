#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

SECRET_PATTERNS = [
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}", re.IGNORECASE), "Bearer [REDACTED_SECRET]"),
    ("password", re.compile(r"(?i)\b(password|passwd|pwd)\s*[:=]\s*[^\s;,&\]\)]+"), lambda m: f"{m.group(1)}=[REDACTED_CREDENTIAL]"),
    ("db_username", re.compile(r"(?i)\b(user(name)?|db_user)\s*[:=]\s*[^\s;,&\]\)]+"), lambda m: f"{m.group(1)}=[REDACTED_CREDENTIAL]"),
    ("testlink_key", re.compile(r"(?i)\b(testlink[_-]?(key|api[_-]?key|token))\s*[:=]\s*[^\s;,&\]\)]+"), lambda m: f"{m.group(1)}=[REDACTED_SECRET]"),
    ("cookie", re.compile(r"(?i)\b(cookie|set-cookie)\s*[:=]\s*[^\n]+"), lambda m: f"{m.group(1)}=[REDACTED_SECRET]"),
    ("internal_url", re.compile(r"\bhttps?://(?:localhost|127\.0\.0\.1|10(?:\.\d{1,3}){3}|172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2}|192\.168(?:\.\d{1,3}){2}|[A-Za-z0-9.-]*\.(?:local|internal|intranet|corp|bidv))(?::\d+)?(?:/[^\s\]\)>'\"]*)?", re.IGNORECASE), "[REDACTED_INTERNAL_ENDPOINT]"),
    ("internal_ip", re.compile(r"\b(?:10(?:\.\d{1,3}){3}|172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2}|192\.168(?:\.\d{1,3}){2})\b"), "[REDACTED_INTERNAL_ENDPOINT]"),
    ("jdbc_url", re.compile(r"(?i)\bjdbc:[^\s\]\)>'\"]+"), "[REDACTED_INTERNAL_ENDPOINT]"),
    ("token_assignment", re.compile(r"(?i)\b(token|access_token|refresh_token|api_key|apikey|secret)\s*[:=]\s*[A-Za-z0-9._~+/=-]{12,}"), lambda m: f"{m.group(1)}=[REDACTED_SECRET]"),
    ("long_token", re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9._~+/=-]{40,}(?![A-Za-z0-9])"), "[REDACTED_SECRET]"),
]

METADATA_REDACTION_LINE = re.compile(r"^redaction_status:\s*unredacted\s*$", re.MULTILINE)


@dataclass
class RedactionFinding:
    redaction_type: str
    count: int


def redact_text(text: str) -> tuple[str, list[RedactionFinding]]:
    findings: list[RedactionFinding] = []
    redacted = text
    for name, pattern, replacement in SECRET_PATTERNS:
        redacted, count = pattern.subn(replacement, redacted)
        if count:
            findings.append(RedactionFinding(name, count))
    if METADATA_REDACTION_LINE.search(redacted):
        redacted = METADATA_REDACTION_LINE.sub("redaction_status: redacted", redacted)
    return redacted, findings


def contains_secret(text: str) -> bool:
    for _, pattern, _ in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            if "[REDACTED_" not in match.group(0):
                return True
    return False


def redact_tree(input_dir: Path, output_dir: Path) -> dict:
    results = []
    total_findings = 0
    for source in sorted(path for path in input_dir.rglob("*") if path.is_file()):
        relative = source.relative_to(input_dir)
        target = output_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() not in {".md", ".txt", ".tsv", ".json", ".yml", ".yaml", ".csv"}:
            target.write_bytes(source.read_bytes())
            results.append({"source_path": relative.as_posix(), "status": "copied_binary", "redactions": []})
            continue
        text = source.read_text(encoding="utf-8", errors="replace")
        redacted, findings = redact_text(text)
        target.write_text(redacted, encoding="utf-8")
        redaction_records = [{"type": finding.redaction_type, "count": finding.count} for finding in findings]
        total_findings += sum(finding.count for finding in findings)
        results.append({"source_path": relative.as_posix(), "status": "redacted" if findings else "copied", "redactions": redaction_records})
    return {"status": "success", "input": str(input_dir), "output": str(output_dir), "total_files": len(results), "total_redactions": total_findings, "files": results}


def write_report(report: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore
        output.write_text(yaml.safe_dump(report, allow_unicode=True, sort_keys=False), encoding="utf-8")
    except ImportError:
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Redact secrets from normalized knowledge")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    if not args.input.exists() or not args.input.is_dir():
        raise SystemExit(f"input directory not found: {args.input}")
    report = redact_tree(args.input, args.output)
    write_report(report, args.report)
    print(json.dumps({"status": report["status"], "total_files": report["total_files"], "total_redactions": report["total_redactions"], "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
