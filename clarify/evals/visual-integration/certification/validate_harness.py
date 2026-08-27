#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED = [
    "inputs.yaml",
    "oracle.yaml",
    "baselines.yaml",
    "control-generator.md",
    "treatment-generator.md",
    "judge.md",
    "seal_pair.py",
    "score_ab.py",
    "promotion-policy.json",
    "STATUS.md",
]
FORBIDDEN_INPUT_TOKENS = [
    "critical_invariants",
    "judge_dimensions",
    "dimensions:",
    "automatic_failure",
    "promotion_rule",
    "claim_on_pass",
    "expected_",
]
EXPECTED_CASES = {"refund-operational-flow", "approval-loop", "source-bound-causal"}


def case_ids(text: str) -> set[str]:
    return set(re.findall(r"^\s*- id:\s*([A-Za-z0-9_-]+)\s*$", text, flags=re.MULTILINE))


def validate(root: Path) -> dict:
    errors = []
    warnings = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")

    inputs = (root / "inputs.yaml").read_text(encoding="utf-8") if (root / "inputs.yaml").is_file() else ""
    oracle = (root / "oracle.yaml").read_text(encoding="utf-8") if (root / "oracle.yaml").is_file() else ""
    baselines = (root / "baselines.yaml").read_text(encoding="utf-8") if (root / "baselines.yaml").is_file() else ""

    leaked = [token for token in FORBIDDEN_INPUT_TOKENS if token.lower() in inputs.lower()]
    if leaked:
        errors.append(f"blind inputs contain judge-only tokens: {leaked}")

    input_cases = case_ids(inputs)
    oracle_cases = case_ids(oracle)
    if input_cases != EXPECTED_CASES:
        errors.append(f"inputs case set mismatch: {sorted(input_cases)}")
    if oracle_cases != EXPECTED_CASES:
        errors.append(f"oracle case set mismatch: {sorted(oracle_cases)}")

    commits = re.findall(r"repository_commit:\s*([0-9a-f]{40})", baselines)
    if len(commits) != 2:
        errors.append("baselines must contain exactly two 40-char repository commits")
    elif commits[0] == commits[1]:
        errors.append("control and treatment commits must differ")

    if "integration: disabled" not in baselines:
        errors.append("control baseline must declare integration disabled")
    if "integration: enabled" not in baselines:
        errors.append("treatment baseline must declare integration enabled")

    for protocol in ["control-generator.md", "treatment-generator.md"]:
        text = (root / protocol).read_text(encoding="utf-8") if (root / protocol).is_file() else ""
        if "oracle.yaml" not in text or "Forbidden" not in text:
            errors.append(f"{protocol} must explicitly forbid oracle access")
        if "CONTEXT CONTAMINATED" not in text:
            errors.append(f"{protocol} must define contamination abort")

    judge = (root / "judge.md").read_text(encoding="utf-8") if (root / "judge.md").is_file() else ""
    if "condition-map.json" not in judge or "JUDGE UNBLINDED" not in judge:
        errors.append("judge protocol must forbid pre-score condition mapping")

    try:
        policy = json.loads((root / "promotion-policy.json").read_text(encoding="utf-8"))
        if policy.get("treatment_case_wins_minimum") != 2:
            errors.append("promotion policy must require at least 2 treatment wins")
        if policy.get("critical_invariant_regressions_allowed") != 0:
            errors.append("promotion policy must allow zero critical invariant regressions")
    except Exception as exc:
        errors.append(f"invalid promotion-policy.json: {exc}")

    return {
        "schema_version": "clarify-visual-ab-harness-validation/v1",
        "status": "passed" if not errors else "failed",
        "input_cases": sorted(input_cases),
        "oracle_cases": sorted(oracle_cases),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parent))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = validate(Path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=None if args.json else 2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
