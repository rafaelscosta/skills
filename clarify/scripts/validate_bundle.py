#!/usr/bin/env python3
"""Validate the structure and basic integrity of the clarify skill bundle."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"`((?:references|scripts|evals)/[^`]+)`")


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


def parse_frontmatter(text: str) -> tuple[dict[str, str], int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'.")
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not closed.") from exc

    values: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Unsupported frontmatter syntax at line {number}: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key or not value:
            raise ValueError(f"Empty frontmatter key/value at line {number}.")
        if key in values:
            raise ValueError(f"Duplicate frontmatter key: {key}")
        values[key] = value
    return values, end + 1


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    if not root.exists() or not root.is_dir():
        return [Finding("error", "B001", str(root), "Skill root does not exist or is not a directory.")]

    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        return [Finding("error", "B002", str(skill_path), "Required SKILL.md is missing.")]

    try:
        skill_text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [Finding("error", "B003", str(skill_path), f"Cannot read SKILL.md as UTF-8: {exc}")]

    try:
        frontmatter, _ = parse_frontmatter(skill_text)
    except ValueError as exc:
        findings.append(Finding("error", "B004", str(skill_path), str(exc)))
        frontmatter = {}

    allowed_keys = {"name", "description"}
    missing = allowed_keys - set(frontmatter)
    extras = set(frontmatter) - allowed_keys
    if missing:
        findings.append(Finding("error", "B005", str(skill_path), f"Missing frontmatter keys: {sorted(missing)}"))
    if extras:
        findings.append(Finding("error", "B006", str(skill_path), f"Unsupported frontmatter keys: {sorted(extras)}"))

    name = frontmatter.get("name", "")
    if name and not NAME_RE.fullmatch(name):
        findings.append(Finding("error", "B007", str(skill_path), f"Invalid skill name: {name}"))
    if name and root.name != name:
        findings.append(
            Finding("warning", "B008", str(root), f"Folder name '{root.name}' does not match skill name '{name}'.")
        )

    description = frontmatter.get("description", "")
    if description:
        if len(description) > 1024:
            findings.append(Finding("error", "B009", str(skill_path), "Description exceeds 1024 characters."))
        if "Use when" not in description:
            findings.append(Finding("warning", "B010", str(skill_path), "Description should state positive trigger conditions."))
        if "Do not use" not in description:
            findings.append(Finding("warning", "B011", str(skill_path), "Description should state a meaningful non-trigger boundary."))

    skill_lines = len(skill_text.splitlines())
    if skill_lines > 800:
        findings.append(Finding("error", "B012", str(skill_path), f"SKILL.md has {skill_lines} lines; move detail to references."))
    elif skill_lines > 500:
        findings.append(Finding("warning", "B013", str(skill_path), f"SKILL.md has {skill_lines} lines; prefer under 500."))

    for match in REFERENCE_RE.finditer(skill_text):
        relative = match.group(1)
        target = root / relative
        if not target.exists():
            findings.append(Finding("error", "B014", str(skill_path), f"Referenced path is missing: {relative}"))

    metadata_path = root / "agents" / "openai.yaml"
    if metadata_path.exists():
        try:
            metadata = metadata_path.read_text(encoding="utf-8")
            for required_text in ("interface:", "display_name:", "short_description:", "default_prompt:"):
                if required_text not in metadata:
                    findings.append(
                        Finding("error", "B015", str(metadata_path), f"Missing metadata field: {required_text}")
                    )
            if name and f"${name}" not in metadata:
                findings.append(
                    Finding("warning", "B016", str(metadata_path), f"Default prompt does not mention explicit invocation '${name}'.")
                )
            short_match = re.search(r"^\s*short_description:\s*[\"']?(.*?)[\"']?\s*$", metadata, re.MULTILINE)
            if short_match and len(short_match.group(1)) > 100:
                findings.append(Finding("warning", "B017", str(metadata_path), "short_description exceeds 100 characters."))
        except (OSError, UnicodeError) as exc:
            findings.append(Finding("error", "B018", str(metadata_path), f"Cannot read metadata: {exc}"))
    else:
        findings.append(Finding("warning", "B019", str(metadata_path), "Optional agents/openai.yaml metadata is missing."))

    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            findings.append(Finding("error", "B020", str(path), "Symlinks are not allowed in the portable bundle."))
            continue
        if not path.is_file():
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding("error", "B021", str(path), "File is not valid UTF-8 text."))
        except OSError as exc:
            findings.append(Finding("error", "B022", str(path), f"Cannot read file: {exc}"))

        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError, UnicodeError) as exc:
                findings.append(Finding("error", "B023", str(path), f"Invalid JSON: {exc}"))

        if path.suffix == ".py":
            try:
                source = path.read_text(encoding="utf-8")
                compile(source, str(path), "exec")
            except (SyntaxError, OSError, UnicodeError) as exc:
                findings.append(Finding("error", "B024", str(path), f"Python compile failure: {exc}"))

    for disallowed in ("README.md", "CHANGELOG.md", "INSTALL.md"):
        candidate = root / disallowed
        if candidate.exists():
            findings.append(
                Finding(
                    "warning",
                    "B025",
                    str(candidate),
                    "Keep operational guidance in SKILL.md or references to reduce bundle clutter.",
                )
            )

    return findings


def format_text(root: Path, findings: Sequence[Finding]) -> str:
    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    lines = [
        "CLARIFY BUNDLE VALIDATION",
        f"Root: {root}",
        f"Result: {'PASS' if errors == 0 else 'FAIL'}",
        f"Errors: {errors}",
        f"Warnings: {warnings}",
    ]
    for item in findings:
        lines.extend(
            [
                "",
                f"[{item.severity.upper()}] {item.code}",
                f"  Path: {item.path}",
                f"  {item.message}",
            ]
        )
    if not findings:
        lines.extend(["", "No structural findings."])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate an OpenAI-style skill bundle.")
    parser.add_argument("root", nargs="?", default=".", help="Skill directory.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--warnings-as-errors", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    findings = validate(root)
    if args.json:
        payload = {
            "root": str(root),
            "passed": not any(item.severity == "error" for item in findings),
            "findings": [asdict(item) for item in findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_text(root, findings))

    has_error = any(item.severity == "error" for item in findings)
    has_warning = any(item.severity == "warning" for item in findings)
    if has_error or (args.warnings_as_errors and has_warning):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
