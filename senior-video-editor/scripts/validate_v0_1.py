#!/usr/bin/env python3
"""Validate the Senior Video Editor v0.1 skill slice with stdlib only."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SKILLS = (
    "video-edit-contract",
    "footage-intelligence",
    "story-edit",
    "senior-video-editor",
    "supervising-video-editor",
)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"`((?:references|scripts|evals)/[^`]+)`")


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def check_skill(repo: Path, skill: str) -> list[Finding]:
    root = repo / skill
    out: list[Finding] = []
    required = ("SKILL.md", "config.yaml", "agents/openai.yaml")
    for relative in required:
        if not (root / relative).is_file():
            out.append(Finding("error", "V001", str(root / relative), "required file missing"))
    if out:
        return out

    skill_path = root / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    try:
        fm = frontmatter(text)
    except ValueError as exc:
        out.append(Finding("error", "V002", str(skill_path), str(exc)))
        fm = {}

    if fm.get("name") != skill:
        out.append(Finding("error", "V003", str(skill_path), f"frontmatter name must be {skill!r}"))
    if fm.get("name") and not NAME_RE.fullmatch(fm["name"]):
        out.append(Finding("error", "V004", str(skill_path), "invalid skill name"))
    description = fm.get("description", "")
    if "Use when" not in description or "Do not use" not in description:
        out.append(Finding("error", "V005", str(skill_path), "description must contain positive and negative routing boundaries"))
    if len(text.splitlines()) > 500:
        out.append(Finding("error", "V006", str(skill_path), "SKILL.md exceeds 500-line v0.1 budget"))

    for match in REF_RE.finditer(text):
        target = root / match.group(1)
        if not target.exists():
            out.append(Finding("error", "V007", str(skill_path), f"missing referenced path: {match.group(1)}"))

    config = (root / "config.yaml").read_text(encoding="utf-8")
    if f"name: {skill}" not in config:
        out.append(Finding("error", "V008", str(root / "config.yaml"), "pack name does not match directory"))
    if 'version: "0.1.0"' not in config:
        out.append(Finding("error", "V009", str(root / "config.yaml"), "v0.1 slice must declare version 0.1.0"))

    metadata = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    for token in ("interface:", "display_name:", "short_description:", "default_prompt:", "policy:"):
        if token not in metadata:
            out.append(Finding("error", "V010", str(root / "agents/openai.yaml"), f"missing metadata token: {token}"))
    if f"${skill}" not in metadata:
        out.append(Finding("error", "V011", str(root / "agents/openai.yaml"), "default prompt must name explicit skill invocation"))

    for path in root.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            out.append(Finding("error", "V012", str(path), f"invalid JSON: {exc}"))

    return out


def cross_checks(repo: Path) -> list[Finding]:
    out: list[Finding] = []
    senior = (repo / "senior-video-editor/SKILL.md").read_text(encoding="utf-8")
    expected_route = (
        "$video-edit-contract",
        "$footage-intelligence",
        "$story-edit",
        "$supervising-video-editor",
    )
    for token in expected_route:
        if token not in senior:
            out.append(Finding("error", "V101", "senior-video-editor/SKILL.md", f"canonical route missing {token}"))

    supervisor = (repo / "supervising-video-editor/SKILL.md").read_text(encoding="utf-8")
    if "blocking gates" not in supervisor.lower():
        out.append(Finding("error", "V102", "supervising-video-editor/SKILL.md", "supervisor must define blocking gates"))
    if "do not rescue" not in supervisor.lower() and "do not repair" not in supervisor.lower():
        out.append(Finding("error", "V103", "supervising-video-editor/SKILL.md", "judge/generator separation is not explicit"))

    evals = repo / "senior-video-editor/evals/v0.1/cases.yaml"
    if not evals.is_file():
        out.append(Finding("error", "V104", str(evals), "eval suite missing"))
    else:
        text = evals.read_text(encoding="utf-8")
        for token in ("interview-to-story", "conflicting-brief", "coverage-gap", "blind-a-b-story", "prohibit_quality_average_from_masking_blocker: true"):
            if token not in text:
                out.append(Finding("error", "V105", str(evals), f"eval contract missing {token}"))
    return out


def main() -> int:
    script = Path(__file__).resolve()
    repo = script.parents[2]
    findings: list[Finding] = []
    for skill in SKILLS:
        findings.extend(check_skill(repo, skill))
    findings.extend(cross_checks(repo))
    errors = [item for item in findings if item.severity == "error"]
    print("SENIOR VIDEO EDITOR V0.1 VALIDATION")
    print(f"repo={repo}")
    print(f"skills={len(SKILLS)}")
    print(f"result={'PASS' if not errors else 'FAIL'}")
    print(f"errors={len(errors)}")
    for item in findings:
        print(f"[{item.severity.upper()}] {item.code} {item.path}: {item.message}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
