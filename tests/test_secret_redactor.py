from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from redact_secrets import contains_secret, redact_text, redact_tree


def test_redacts_tokens_credentials_and_internal_endpoints() -> None:
    text = "\n".join([
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456",
        "password=secret123",
        "DB_USER=app",
        "testlink_key=abcdef1234567890",
        "Cookie: JSESSIONID=abcdef1234567890; path=/",
        "url=http://10.10.20.30:8080/private",
        "host=192.168.1.10",
        "token=abcdefghijklmnopqrstuvwxyz1234567890ABCDEFG",
    ])

    redacted, findings = redact_text(text)

    assert "Bearer [REDACTED_SECRET]" in redacted
    assert "password=[REDACTED_CREDENTIAL]" in redacted
    assert "DB_USER=[REDACTED_CREDENTIAL]" in redacted
    assert "testlink_key=[REDACTED_SECRET]" in redacted
    assert "Cookie=[REDACTED_SECRET]" in redacted
    assert "[REDACTED_INTERNAL_ENDPOINT]" in redacted
    assert "secret123" not in redacted
    assert "10.10.20.30" not in redacted
    assert findings
    assert not contains_secret(redacted)


def test_redact_tree_preserves_structure_and_updates_metadata(tmp_path: Path) -> None:
    input_dir = tmp_path / "normalized"
    output_dir = tmp_path / "redacted"
    source = input_dir / "Prompt" / "API" / "Gen Script" / "properties.md"
    source.parent.mkdir(parents=True)
    source.write_text(
        "---\nsource_path: Prompt/API/Gen Script/properties.txt\nredaction_status: unredacted\n---\n\npassword=secret123\nhttp://172.16.1.2/app\n",
        encoding="utf-8",
    )

    report = redact_tree(input_dir, output_dir)
    redacted = (output_dir / "Prompt" / "API" / "Gen Script" / "properties.md").read_text(encoding="utf-8")

    assert report["total_files"] == 1
    assert report["total_redactions"] == 2
    assert "redaction_status: redacted" in redacted
    assert "secret123" not in redacted
    assert "172.16.1.2" not in redacted
