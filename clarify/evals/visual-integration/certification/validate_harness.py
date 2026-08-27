#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CONTROL_COMMIT = "a10b7e80f3dbe29422226aa31758f7c679e829af"
TREATMENT_COMMIT = "78cb5cde584ddc9b022b7b4de91930f1ac76a1b1"
EXPECTED_CASES = {"refund-operational-flow", "approval-loop", "source-bound-causal"}
REQUIRED = [
    "README.md",
    "STATUS.md",
    "VALIDATION.md",
    "inputs.yaml",
    "oracle.yaml",
    "baselines.yaml",
    "control-generator.md",
    "treatment-generator.md",
    "judge.md",
    "seal_pair.py",
    "score_ab.py",
    "promotion-policy.json",
    "run-metadata.template.json",
    "test_certification_harness.py",
]
FORBIDDEN_INPUT_TOKENS = [
    "critical_invariants",
    "judge_dimensions",
    "dimensions:",
    "automatic_failure",
    "promotion_rule",
    "claim_on_pass",
    "expected_",
    "source_file:",
]


def case_ids(text: str) -> set[str]:
    return set(re.findall(r"^\s*- id:\s*([A-Za-z0-9_-]+)\s*$", text, flags=re.MULTILINE))


def validate(root: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")

    inputs = (root / "inputs.yaml").read_text(encoding="utf-8") if (root / "inputs.yaml").is_file() else ""
    oracle = (root / "oracle.yaml").read_text(encoding="utf-8") if (root / "oracle.yaml").is_file() else ""
    baselines = (root / "baselines.yaml").read_text(encoding="utf-8") if (root / "baselines.yaml").is_file() else ""
    sealer = (root / "seal_pair.py").read_text(encoding="utf-8") if (root / "seal_pair.py").is_file() else ""
    scorer = (root / "score_ab.py").read_text(encoding="utf-8") if (root / "score_ab.py").is_file() else ""
    metadata_template = (root / "run-metadata.template.json").read_text(encoding="utf-8") if (root / "run-metadata.template.json").is_file() else ""

    leaked = [token for token in FORBIDDEN_INPUT_TOKENS if token.lower() in inputs.lower()]
    if leaked:
        errors.append(f"blind inputs contain judge-only or external-source tokens: {leaked}")
    if inputs.count("source_inline:") != 3:
        errors.append("blind inputs must be self-contained with source_inline for all three cases")

    input_cases = case_ids(inputs)
    oracle_cases = case_ids(oracle)
    if input_cases != EXPECTED_CASES:
        errors.append(f"inputs case set mismatch: {sorted(input_cases)}")
    if oracle_cases != EXPECTED_CASES:
        errors.append(f"oracle case set mismatch: {sorted(oracle_cases)}")

    commits = re.findall(r"repository_commit:\s*([0-9a-f]{40})", baselines)
    if commits != [CONTROL_COMMIT, TREATMENT_COMMIT]:
        errors.append(f"baselines must pin exact control/treatment commits in order: {CONTROL_COMMIT}, {TREATMENT_COMMIT}")
    if "integration: disabled" not in baselines:
        errors.append("control baseline must declare integration disabled")
    if "integration: enabled" not in baselines:
        errors.append("treatment baseline must declare integration enabled")

    for commit, label in [(CONTROL_COMMIT, "CONTROL_COMMIT"), (TREATMENT_COMMIT, "TREATMENT_COMMIT")]:
        if f'{label} = "{commit}"' not in sealer:
            errors.append(f"sealer {label} does not match frozen baseline")
    if "verify_hash_manifest(root)" not in sealer:
        errors.append("sealer must verify condition hash manifests")
    for field in ("model", "surface", "reasoning_effort", "tool_budget_profile"):
        if field not in sealer:
            errors.append(f"sealer must enforce matched field: {field}")

    for protocol in ["control-generator.md", "treatment-generator.md"]:
        text = (root / protocol).read_text(encoding="utf-8") if (root / protocol).is_file() else ""
        if "oracle.yaml" not in text or "Forbidden" not in text:
            errors.append(f"{protocol} must explicitly forbid oracle access")
        if "CONTEXT CONTAMINATED" not in text:
            errors.append(f"{protocol} must define contamination abort")
        if "hashes.sha256" not in text or "run-metadata.json" not in text:
            errors.append(f"{protocol} must require metadata and immutable hashes")

    judge = (root / "judge.md").read_text(encoding="utf-8") if (root / "judge.md").is_file() else ""
    if "condition-map.json" not in judge or "JUDGE UNBLINDED" not in judge:
        errors.append("judge protocol must forbid pre-score condition mapping")
    if "judge-preunblind.json" not in judge or "condition_mapping_seen" not in judge:
        errors.append("judge protocol must seal pre-unblind judgment")

    try:
        template = json.loads(metadata_template)
        required_meta = {
            "schema_version", "run_id", "condition", "repository_commit", "model", "surface",
            "reasoning_effort", "tool_budget_profile", "isolation", "case_count", "oracle_seen",
            "opposite_condition_seen", "prior_judgment_seen"
        }
        if not required_meta.issubset(template):
            errors.append(f"run metadata template missing fields: {sorted(required_meta - set(template))}")
    except Exception as exc:
        errors.append(f"invalid run-metadata.template.json: {exc}")

    try:
        policy = json.loads((root / "promotion-policy.json").read_text(encoding="utf-8"))
        if policy.get("treatment_case_wins_minimum") != 2:
            errors.append("promotion policy must require at least 2 treatment wins")
        if policy.get("critical_invariant_regressions_allowed") != 0:
            errors.append("promotion policy must allow zero critical invariant regressions")
        if policy.get("treatment_automatic_failures_allowed") != 0:
            errors.append("promotion policy must allow zero treatment automatic failures")
        if policy.get("fidelity_losses_allowed") != 0:
            errors.append("promotion policy must allow zero fidelity losses")
    except Exception as exc:
        errors.append(f"invalid promotion-policy.json: {exc}")

    for required_text in ("EXPECTED_CASES", "judgment manifest hash mismatch", "total must equal the sum of scores"):
        if required_text not in scorer:
            errors.append(f"post-unblind scorer missing structural guard: {required_text}")

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
