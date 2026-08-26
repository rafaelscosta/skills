#!/usr/bin/env python3
"""Deterministic structural validation for the youtube-fetcher skill bundle."""
from __future__ import annotations
import json
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "config.yaml",
    "agents/openai.yaml",
    "assets/icon.svg",
    "evals/trigger-cases.yaml",
    "evals/rubric.yaml",
    "requirements.txt",
    "LICENSE",
    "references/agent-recipes.md",
    "references/runtime-contract.md",
    "references/upstream.md",
    "references/metadata.schema.json",
    "references/chapters.schema.json",
    "references/chunks.schema.json",
    "references/manifest.schema.json",
    "references/receipt.schema.json",
    "scripts/fetch_transcript.py",
]

def main() -> int:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        raise SystemExit("Missing required files: " + ", ".join(missing))

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        raise SystemExit("SKILL.md must start with YAML frontmatter")
    frontmatter = skill.split("---", 2)[1]
    keys = [line.split(":", 1)[0] for line in frontmatter.splitlines() if line and not line[0].isspace()]
    if keys != ["name", "description"]:
        raise SystemExit(f"Unexpected SKILL.md frontmatter keys: {keys}")
    if "name: youtube-fetcher" not in frontmatter:
        raise SystemExit("SKILL.md name mismatch")

    metadata = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    for token in ("display_name: YouTube Fetcher", "$youtube-fetcher", "allow_implicit_invocation: true"):
        if token not in metadata:
            raise SystemExit(f"agents/openai.yaml missing: {token}")

    for path in sorted((ROOT / "references").glob("*.schema.json")):
        json.loads(path.read_text(encoding="utf-8"))

    py_compile.compile(str(ROOT / "scripts" / "fetch_transcript.py"), doraise=True)
    print("youtube-fetcher bundle: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
