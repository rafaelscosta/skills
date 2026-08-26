#!/usr/bin/env python3
"""Validate the Concept Bridge v3.1 blind visual-certification firewall.

This validator is intentionally zero-dependency. It does not parse arbitrary YAML; it
checks the constrained certification fixtures for case identity, oracle separation,
and protocol presence before a behavioral run.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "evals" / "visual-certification"

INPUTS = CERT / "inputs.yaml"
RENDER_INPUTS = CERT / "render-inputs.yaml"
ORACLE = CERT / "oracle.yaml"
GENERATOR = CERT / "generator.md"
JUDGE = CERT / "judge.md"
RUNBOOK = CERT / "README.md"

CASE_RE = re.compile(r"^\s*- id:\s*([^\s#]+)\s*$", re.MULTILINE)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def case_ids(text: str, label: str) -> list[str]:
    ids = CASE_RE.findall(text)
    if not ids:
        fail(f"{label} contains no case ids")
    duplicates = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicates:
        fail(f"{label} contains duplicate case ids: {', '.join(duplicates)}")
    return ids


def assert_absent(text: str, tokens: list[str], label: str) -> None:
    lowered = text.lower()
    leaked = [token for token in tokens if token.lower() in lowered]
    if leaked:
        fail(f"{label} leaks judge-only tokens: {', '.join(leaked)}")


def main() -> int:
    inputs_text = read(INPUTS)
    render_text = read(RENDER_INPUTS)
    oracle_text = read(ORACLE)
    generator_text = read(GENERATOR)
    judge_text = read(JUDGE)
    runbook_text = read(RUNBOOK)

    blind_ids = case_ids(inputs_text, "inputs.yaml")
    render_ids = case_ids(render_text, "render-inputs.yaml")
    oracle_ids = case_ids(oracle_text, "oracle.yaml")

    assert_absent(
        inputs_text,
        ["expected_route:", "must:", "must_not:", "sealed_oracle", "minimum_total:"],
        "inputs.yaml",
    )
    assert_absent(
        render_text,
        ["expected_route:", "must:", "must_not:", "sealed_oracle", "minimum_total:"],
        "render-inputs.yaml",
    )

    if set(blind_ids) != set(oracle_ids):
        missing = sorted(set(blind_ids) - set(oracle_ids))
        extra = sorted(set(oracle_ids) - set(blind_ids))
        fail(
            "oracle/input case mismatch"
            + (f"; missing in oracle: {', '.join(missing)}" if missing else "")
            + (f"; extra in oracle: {', '.join(extra)}" if extra else "")
        )

    if len(blind_ids) != 15:
        fail(f"route suite must contain 15 cases, found {len(blind_ids)}")

    if len(render_ids) != 6:
        fail(f"render pilot must contain 6 cases, found {len(render_ids)}")

    unknown_render = sorted(set(render_ids) - set(blind_ids))
    if unknown_render:
        fail(f"render pilot contains unknown case ids: {', '.join(unknown_render)}")

    expected_route_count = oracle_text.count("expected_route:")
    if expected_route_count != len(oracle_ids):
        fail(
            f"oracle expected_route count mismatch: {expected_route_count} routes for "
            f"{len(oracle_ids)} cases"
        )

    for required_phrase in [
        "VISUAL CERT INVALID — CONTEXT CONTAMINATED",
        "oracle.yaml",
        "route-predictions.yaml",
        "render-receipts.yaml",
    ]:
        if required_phrase not in generator_text:
            fail(f"generator.md missing required firewall/output phrase: {required_phrase}")

    for required_phrase in [
        "15/15",
        "6/6",
        "INVALID — GENERATOR CONTAMINATED",
        "CONCEPT-BRIDGE v3.1 VISUAL BEHAVIOR: CERTIFIED",
    ]:
        if required_phrase not in judge_text:
            fail(f"judge.md missing required gate phrase: {required_phrase}")

    for required_phrase in [
        "CERTIFICATION HARNESS READY — BEHAVIORAL CERTIFICATION PENDING",
        "Generator",
        "Judge",
    ]:
        if required_phrase not in runbook_text:
            fail(f"README.md missing required status/protocol phrase: {required_phrase}")

    print("PASS: blind visual-certification firewall is structurally valid")
    print(f"  route cases: {len(blind_ids)}")
    print(f"  render pilot cases: {len(render_ids)}")
    print(f"  oracle cases: {len(oracle_ids)}")
    print("  blind inputs: no judge-only route/must/must_not fields detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
