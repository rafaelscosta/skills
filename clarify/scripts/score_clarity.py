#!/usr/bin/env python3
"""Score Clarify rubric records while preserving the v1 scoring contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

BASE_DIMENSIONS = (
    "audience_fit",
    "main_message",
    "logical_order",
    "terminology",
    "sentence_clarity",
    "causal_completeness",
    "fidelity",
    "example_quality",
    "visual_fit",
    "actionability",
    "exceptions_recovery",
    "epistemic_clarity",
    "accessibility",
    "validation",
)

VISUAL_PROOF_DIMENSIONS = (
    "visual_invariant_coverage",
    "visual_delivery_proof",
)

ALL_DIMENSIONS = BASE_DIMENSIONS + VISUAL_PROOF_DIMENSIONS

# Preserve the original score_clarity.py behavior when callers provide only
# risk_level and the original fourteen dimensions.
LEGACY_CRITICAL_BY_RISK = {
    "low": ("fidelity", "main_message"),
    "medium": ("fidelity", "main_message", "logical_order"),
    "high": (
        "fidelity",
        "causal_completeness",
        "exceptions_recovery",
        "epistemic_clarity",
        "actionability",
        "validation",
    ),
    "critical": (
        "fidelity",
        "causal_completeness",
        "exceptions_recovery",
        "epistemic_clarity",
        "actionability",
        "validation",
        "accessibility",
    ),
}
LEGACY_THRESHOLDS = {"low": 20, "medium": 24, "high": 27, "critical": 27}

# Explicit rubric-v2 profiles mirror evals/rubric.yaml. Visual proof dimensions
# become score-bearing only for trusted_visual; they cannot inflate a prose-only
# or ordinary operational score.
PROFILES = {
    "low_risk_quick": {
        "dimensions": BASE_DIMENSIONS,
        "minimum_total": 20,
        "zero_forbidden": ("fidelity", "main_message"),
        "required_two": (),
    },
    "standard_reusable": {
        "dimensions": BASE_DIMENSIONS,
        "minimum_total": 24,
        "zero_forbidden": BASE_DIMENSIONS,
        "required_two": (),
    },
    "operational": {
        "dimensions": BASE_DIMENSIONS,
        "minimum_total": 25,
        "zero_forbidden": (),
        "required_two": ("fidelity", "actionability", "exceptions_recovery"),
    },
    "trusted_visual": {
        "dimensions": ALL_DIMENSIONS,
        "minimum_total": 30,
        "zero_forbidden": (),
        "required_two": (
            "fidelity",
            "visual_fit",
            "visual_invariant_coverage",
            "visual_delivery_proof",
            "accessibility",
            "epistemic_clarity",
        ),
    },
    "high_risk": {
        "dimensions": BASE_DIMENSIONS,
        "minimum_total": 27,
        "zero_forbidden": (),
        "required_two": (
            "fidelity",
            "causal_completeness",
            "exceptions_recovery",
            "epistemic_clarity",
            "actionability",
            "validation",
        ),
    },
}


def load_payload(path: str) -> dict:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_scores(scores: object, required_dimensions: tuple[str, ...]) -> dict[str, int]:
    if not isinstance(scores, dict):
        raise ValueError("Payload must contain an object named 'scores'.")

    missing = [name for name in required_dimensions if name not in scores]
    extra = [name for name in scores if name not in ALL_DIMENSIONS]
    if missing:
        raise ValueError(f"Missing dimensions: {missing}")
    if extra:
        raise ValueError(f"Unknown dimensions: {extra}")

    normalized: dict[str, int] = {}
    for name, value in scores.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0 or value > 2:
            raise ValueError(f"Score '{name}' must be an integer from 0 to 2.")
        normalized[name] = value
    return normalized


def evaluate_legacy(payload: dict) -> dict:
    risk = payload.get("risk_level", "medium")
    if risk not in LEGACY_THRESHOLDS:
        raise ValueError(f"Unsupported risk_level: {risk}")

    normalized = normalize_scores(payload.get("scores"), BASE_DIMENSIONS)
    # A legacy payload must remain the legacy surface. New visual-proof fields use
    # the explicit profile contract instead of silently changing old totals.
    unexpected_visual = [name for name in VISUAL_PROOF_DIMENSIONS if name in normalized]
    if unexpected_visual:
        raise ValueError(
            "Visual proof dimensions require an explicit profile, normally 'trusted_visual': "
            f"{unexpected_visual}"
        )

    scores = {name: normalized[name] for name in BASE_DIMENSIONS}
    total = sum(scores.values())
    critical = LEGACY_CRITICAL_BY_RISK[risk]
    failed_critical = [name for name in critical if scores[name] < 2]
    zero_dimensions = [name for name, value in scores.items() if value == 0]
    threshold = LEGACY_THRESHOLDS[risk]
    passed = total >= threshold and not failed_critical
    if risk in {"low", "medium"} and zero_dimensions:
        passed = False

    return {
        "scoring_contract": "clarify-rubric/v1-legacy",
        "risk_level": risk,
        "scores": scores,
        "total": total,
        "maximum": 28,
        "threshold": threshold,
        "critical_dimensions": list(critical),
        "failed_critical_dimensions": failed_critical,
        "zero_dimensions": zero_dimensions,
        "passed": passed,
    }


def evaluate_profile(payload: dict) -> dict:
    profile = payload.get("profile")
    if profile not in PROFILES:
        raise ValueError(f"Unsupported profile: {profile}")
    contract = PROFILES[profile]
    dimensions = contract["dimensions"]
    normalized = normalize_scores(payload.get("scores"), dimensions)

    # Extra known visual-proof dimensions are accepted only when they are part of
    # the selected profile. This prevents optional visual points from boosting a
    # non-visual threshold.
    non_scoring = [name for name in normalized if name not in dimensions]
    if non_scoring:
        raise ValueError(f"Dimensions not applicable to profile '{profile}': {non_scoring}")

    scores = {name: normalized[name] for name in dimensions}
    total = sum(scores.values())
    required_two = contract["required_two"]
    zero_forbidden = contract["zero_forbidden"]
    failed_required_two = [name for name in required_two if scores[name] < 2]
    failed_zero_forbidden = [name for name in zero_forbidden if scores[name] == 0]
    threshold = contract["minimum_total"]
    passed = total >= threshold and not failed_required_two and not failed_zero_forbidden

    return {
        "scoring_contract": "clarify-rubric/v2",
        "profile": profile,
        "scores": scores,
        "total": total,
        "maximum": len(dimensions) * 2,
        "threshold": threshold,
        "required_two": list(required_two),
        "failed_required_two": failed_required_two,
        "zero_forbidden": list(zero_forbidden),
        "failed_zero_forbidden": failed_zero_forbidden,
        "passed": passed,
    }


def evaluate(payload: dict) -> dict:
    if "profile" in payload:
        return evaluate_profile(payload)
    return evaluate_legacy(payload)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score a Clarify quality rubric JSON file.")
    parser.add_argument("path", nargs="?", default="-", help="JSON file or '-' for stdin.")
    args = parser.parse_args(argv)
    try:
        result = evaluate(load_payload(args.path))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
