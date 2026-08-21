#!/usr/bin/env python3
"""Score a Clarify rubric JSON record and enforce critical gates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

DIMENSIONS = (
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

CRITICAL_BY_RISK = {
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

THRESHOLDS = {"low": 20, "medium": 24, "high": 27, "critical": 27}


def load_payload(path: str) -> dict:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evaluate(payload: dict) -> dict:
    risk = payload.get("risk_level", "medium")
    if risk not in THRESHOLDS:
        raise ValueError(f"Unsupported risk_level: {risk}")
    scores = payload.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("Payload must contain an object named 'scores'.")

    missing = [name for name in DIMENSIONS if name not in scores]
    extra = [name for name in scores if name not in DIMENSIONS]
    if missing:
        raise ValueError(f"Missing dimensions: {missing}")
    if extra:
        raise ValueError(f"Unknown dimensions: {extra}")

    normalized: dict[str, int] = {}
    for name in DIMENSIONS:
        value = scores[name]
        if not isinstance(value, int) or value < 0 or value > 2:
            raise ValueError(f"Score '{name}' must be an integer from 0 to 2.")
        normalized[name] = value

    total = sum(normalized.values())
    critical = CRITICAL_BY_RISK[risk]
    failed_critical = [name for name in critical if normalized[name] < 2]
    zero_dimensions = [name for name, value in normalized.items() if value == 0]
    threshold = THRESHOLDS[risk]
    passed = total >= threshold and not failed_critical
    if risk in {"low", "medium"} and zero_dimensions:
        passed = False

    return {
        "risk_level": risk,
        "scores": normalized,
        "total": total,
        "maximum": 28,
        "threshold": threshold,
        "critical_dimensions": list(critical),
        "failed_critical_dimensions": failed_critical,
        "zero_dimensions": zero_dimensions,
        "passed": passed,
    }


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
