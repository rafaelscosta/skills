#!/usr/bin/env python3
"""Validate the Senior Video Editor v0.1 skill slice with stdlib only."""

from __future__ import annotations

import hashlib
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
        for token in ("interview-to-story", "conflicting-brief", "coverage-gap", "blind-a-b-story", "hard-blind-story", "require_easy_case_non_regression: true", "require_discriminative_uplift_case: true", "prohibit_quality_average_from_masking_blocker: true"):
            if token not in text:
                out.append(Finding("error", "V105", str(evals), f"eval contract missing {token}"))
    evidence_specs = (
        (
            repo / "senior-video-editor/evals/v0.1/results/EV-SVE-002-blind-story-non-regression",
            repo / "senior-video-editor/evals/v0.1/fixtures/blind-a-b-story.md",
            repo / "senior-video-editor/evals/v0.1/oracles/blind-a-b-story.oracle.json",
            repo / "senior-video-editor/evals/v0.1/protocols/blind-a-b-story.md",
            "non_regression",
        ),
        (
            repo / "senior-video-editor/evals/v0.1/results/EV-SVE-003-hard-blind-story",
            repo / "senior-video-editor/evals/v0.1/fixtures/hard-blind-story.md",
            repo / "senior-video-editor/evals/v0.1/oracles/hard-blind-story.oracle.json",
            repo / "senior-video-editor/evals/v0.1/protocols/hard-blind-story.md",
            "majority_uplift",
        ),
    )
    for result_dir, fixture_path, oracle_path, protocol_path, policy in evidence_specs:
        manifest_path = result_dir / "manifest.json"
        if not manifest_path.is_file():
            out.append(Finding("error", "V106", str(manifest_path), "promotion evidence manifest missing"))
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            out.append(Finding("error", "V107", str(manifest_path), f"invalid promotion manifest: {exc}"))
            continue

        def digest(path: Path) -> str:
            return hashlib.sha256(path.read_bytes()).hexdigest()

        expected_hashes = manifest.get("evaluated_skill_sha256", {})
        for relative, expected in expected_hashes.items():
            target = repo / relative
            if not target.is_file():
                out.append(Finding("error", "V109", str(target), "evaluated skill file missing"))
                continue
            actual = digest(target)
            if actual != expected:
                out.append(Finding("error", "V110", str(target), f"skill drifted from evaluated artifact: {actual} != {expected}"))

        bound_files = (
            (fixture_path, "fixture_sha256", "V111"),
            (oracle_path, "oracle_sha256", "V112"),
            (protocol_path, "protocol_sha256", "V113"),
            (result_dir / "control.md", "control_sha256", "V114"),
            (result_dir / "treatment.md", "treatment_sha256", "V115"),
        )
        for path, field, code in bound_files:
            if not path.is_file():
                out.append(Finding("error", code, str(path), "bound evidence file missing"))
            elif digest(path) != manifest.get(field):
                out.append(Finding("error", code, str(path), f"evidence hash mismatch for {field}"))

        control_hash = manifest.get("control_sha256")
        treatment_hash = manifest.get("treatment_sha256")
        counts = {"treatment": 0, "control": 0, "tie": 0}
        treatment_block_failures = 0
        for index in (1, 2, 3):
            receipt_path = result_dir / f"judge-{index}.json"
            if not receipt_path.is_file():
                out.append(Finding("error", "V116", str(receipt_path), "judge receipt missing"))
                continue
            expected_receipt_hash = manifest.get("judge_receipt_sha256", {}).get(f"judge-{index}")
            if digest(receipt_path) != expected_receipt_hash:
                out.append(Finding("error", "V117", str(receipt_path), "judge receipt hash mismatch"))
                continue
            try:
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                out.append(Finding("error", "V118", str(receipt_path), f"invalid judge receipt: {exc}"))
                continue
            a_hash = receipt.get("candidate_a_sha256")
            b_hash = receipt.get("candidate_b_sha256")
            if {a_hash, b_hash} != {control_hash, treatment_hash}:
                out.append(Finding("error", "V119", str(receipt_path), "receipt candidates do not match sealed control/treatment hashes"))
                continue
            treatment_label = "A" if a_hash == treatment_hash else "B"
            control_label = "B" if treatment_label == "A" else "A"
            if receipt.get("blocking", {}).get(treatment_label, {}).get("status") != "PASS":
                treatment_block_failures += 1
            winner = receipt.get("overall_winner")
            if winner == "TIE":
                counts["tie"] += 1
            elif winner == treatment_label:
                counts["treatment"] += 1
            elif winner == control_label:
                counts["control"] += 1
            else:
                out.append(Finding("error", "V120", str(receipt_path), f"invalid overall_winner: {winner!r}"))

        manifest_wins = manifest.get("summary", {}).get("wins")
        if manifest_wins != counts:
            out.append(Finding("error", "V121", str(manifest_path), f"summary wins do not match receipts: {manifest_wins!r} != {counts!r}"))
        if treatment_block_failures:
            out.append(Finding("error", "V122", str(manifest_path), f"treatment has blocking failures in {treatment_block_failures} judge receipts"))
        if policy == "non_regression" and counts["treatment"] < counts["control"]:
            out.append(Finding("error", "V123", str(manifest_path), f"treatment regressed: {counts!r}"))
        if policy == "majority_uplift" and counts["treatment"] < 2:
            out.append(Finding("error", "V124", str(manifest_path), f"treatment lacks blind-judge majority uplift: {counts!r}"))
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
