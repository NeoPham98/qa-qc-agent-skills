from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import hashlib
import json
from typing import Any


@dataclass
class GoogleSheetRef:
    spreadsheet_id: str
    url: str | None = None
    tab: str | None = None
    range: str | None = None
    exported_path: str | None = None


@dataclass
class SourceFingerprint:
    candidate_roles: list[str] = field(default_factory=list)
    detected_headers: list[str] = field(default_factory=list)
    detected_keywords: list[str] = field(default_factory=list)
    content_hints: list[str] = field(default_factory=list)


@dataclass
class SourceItem:
    id: str
    kind: str
    original_locator: str
    local_path: str | None = None
    google_sheet: GoogleSheetRef | None = None
    extension: str | None = None
    size_bytes: int | None = None
    sha256: str | None = None
    fingerprint: SourceFingerprint = field(default_factory=SourceFingerprint)


@dataclass
class UserContext:
    project: str | None = None
    squad: str | None = None
    sprint: str | None = None
    epic: str | None = None
    environment: str | None = None
    tester: str | None = None
    build_version: str | None = None


@dataclass
class SourceManifest:
    schema_version: str
    run_id: str
    user_prompt: str
    output_directory: str
    workflow_pack: str = "default"
    sources: list[SourceItem] = field(default_factory=list)
    user_context: UserContext = field(default_factory=UserContext)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_item_from_path(source_id: str, path: Path, root: Path | None = None) -> SourceItem:
    resolved = path.resolve()
    display = str(resolved if root is None else resolved.relative_to(root) if resolved.is_relative_to(root) else resolved)
    stat = resolved.stat()
    return SourceItem(
        id=source_id,
        kind="local_file",
        original_locator=str(path),
        local_path=display,
        extension=resolved.suffix.lower(),
        size_bytes=stat.st_size,
        sha256=file_sha256(resolved),
    )


def load_manifest(path: Path) -> SourceManifest:
    data = json.loads(path.read_text(encoding="utf-8"))
    sources = []
    for item in data.get("sources", []):
        gs = item.get("google_sheet")
        fp = item.get("fingerprint") or {}
        sources.append(SourceItem(
            id=item["id"],
            kind=item["kind"],
            original_locator=item["original_locator"],
            local_path=item.get("local_path"),
            google_sheet=GoogleSheetRef(**gs) if gs else None,
            extension=item.get("extension"),
            size_bytes=item.get("size_bytes"),
            sha256=item.get("sha256"),
            fingerprint=SourceFingerprint(**fp),
        ))
    ctx = UserContext(**(data.get("user_context") or {}))
    return SourceManifest(
        schema_version=data.get("schema_version", "1.0"),
        run_id=data["run_id"],
        user_prompt=data.get("user_prompt", ""),
        output_directory=data["output_directory"],
        workflow_pack=data.get("workflow_pack", "default"),
        sources=sources,
        user_context=ctx,
    )
