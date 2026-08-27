#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path

STATUS_VALUE = {"failed": 0, "partial": 1, "passed": 2}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_for(mapping: dict, condition: str) -> str:
    for label, value in mapping.items():
        if value == condition:
            return label
    raise ValueError(f"condition {condition!r} missing from map")


def comparable_cost(blinded: Path, candidate: str):
    elapsed = []
    tools = []
    cases = blinded / f"candidate-{candidate}" / "cases"
    for case in sorted(p for p in cases.iterdir() if p.is_dir()):
        receipt = load_json(case / "receipt.json")
        e = receipt.get("elapsed_ms")
        t = receipt.get("tool_calls")
        if not isinstance(e, (int, float)) or not isinstance(t, (int, float)):
            return None
        elapsed.append(float(e))
        tools.append(float(t))
    if not elapsed:
        return None
    return {
        "median_elapsed_ms": statistics.median(elapsed),
        "median_tool_calls": statistics.median(tools),
    }


def evaluate(judgment: dict, condition_map: dict, policy: dict, blinded: Path) -> dict:
    errors = []
    mapping = condition_map.get("mapping") or {}
    if set(mapping) != {"A", "B"} or set(mapping.values()) != {"control", "treatment"}:
        errors.append("invalid condition map")
        return {"status": "invalid", "errors": errors}

    manifest = blinded / "manifest.json"
    manifest_sha = sha256(manifest)
    if condition_map.get("blinded_manifest_sha256") != manifest_sha:
        errors.append("condition map manifest hash mismatch")
    if judgment.get("blinded_manifest_sha256") != manifest_sha:
        errors.append("judgment manifest hash mismatch")
    if judgment.get("condition_mapping_seen") is not False:
        errors.append("judge must attest condition_mapping_seen=false")

    treatment = candidate_for(mapping, "treatment")
    control = candidate_for(mapping, "control")
    cases = judgment.get("cases") or []
    if len(cases) != 3 or len({c.get("case_id") for c in cases}) != 3:
        errors.append("judgment must contain exactly three unique cases")

    wins = losses = ties = 0
    critical_regressions = []
    automatic_failures = []
    fidelity_losses = []
    aggregate_treatment = 0
    aggregate_control = 0

    for case in cases:
        winner = case.get("winner")
        if winner == treatment:
            wins += 1
        elif winner == control:
            losses += 1
        elif winner == "tie":
            ties += 1
        else:
            errors.append(f"invalid winner for {case.get('case_id')}")

        t = case.get(treatment) or {}
        c = case.get(control) or {}
        aggregate_treatment += int(t.get("total", 0))
        aggregate_control += int(c.get("total", 0))

        ti = t.get("critical_invariants") or {}
        ci = c.get("critical_invariants") or {}
        for invariant in set(ti) | set(ci):
            tv = STATUS_VALUE.get(ti.get(invariant), -1)
            cv = STATUS_VALUE.get(ci.get(invariant), -1)
            if tv < cv:
                critical_regressions.append({
                    "case_id": case.get("case_id"),
                    "invariant": invariant,
                    "treatment": ti.get(invariant),
                    "control": ci.get(invariant),
                })

        for failure in t.get("automatic_failures") or []:
            automatic_failures.append({"case_id": case.get("case_id"), "failure": failure})

        ts = t.get("scores") or {}
        cs = c.get("scores") or {}
        if "fidelity" in ts and "fidelity" in cs and ts["fidelity"] < cs["fidelity"]:
            fidelity_losses.append({
                "case_id": case.get("case_id"),
                "treatment": ts["fidelity"],
                "control": cs["fidelity"],
            })

    reasons = []
    if wins < policy["treatment_case_wins_minimum"]:
        reasons.append("insufficient treatment case wins")
    if losses > policy["treatment_case_losses_maximum"]:
        reasons.append("too many treatment case losses")
    if len(critical_regressions) > policy["critical_invariant_regressions_allowed"]:
        reasons.append("critical invariant regression detected")
    if len(automatic_failures) > policy["treatment_automatic_failures_allowed"]:
        reasons.append("treatment automatic failure detected")
    if len(fidelity_losses) > policy["fidelity_losses_allowed"]:
        reasons.append("treatment fidelity loss detected")
    if policy.get("aggregate_score_must_not_regress") and aggregate_treatment < aggregate_control:
        reasons.append("treatment aggregate score regressed")

    cost = {"comparable": False}
    tcost = comparable_cost(blinded, treatment)
    ccost = comparable_cost(blinded, control)
    guard = policy.get("cost_guard") or {}
    if tcost and ccost:
        cost = {"comparable": True, "treatment": tcost, "control": ccost}
        elapsed_ratio = None if ccost["median_elapsed_ms"] == 0 else tcost["median_elapsed_ms"] / ccost["median_elapsed_ms"]
        tools_ratio = None if ccost["median_tool_calls"] == 0 else tcost["median_tool_calls"] / ccost["median_tool_calls"]
        cost["elapsed_ratio"] = elapsed_ratio
        cost["tool_calls_ratio"] = tools_ratio
        mult = float(guard.get("catastrophic_multiplier", 2.0))
        override_wins = int(guard.get("wins_required_to_override_catastrophic_cost", 3))
        catastrophic = (
            elapsed_ratio is not None and tools_ratio is not None
            and elapsed_ratio > mult and tools_ratio > mult
        )
        cost["catastrophic"] = catastrophic
        if guard.get("enabled_when_metrics_comparable") and catastrophic and wins < override_wins:
            reasons.append("catastrophic treatment execution-cost regression")

    passed = not errors and not reasons
    return {
        "schema_version": "clarify-visual-ab-promotion-receipt/v1",
        "status": "valid" if not errors else "invalid",
        "promotion_passed": passed,
        "treatment_candidate": treatment,
        "control_candidate": control,
        "case_results": {"wins": wins, "losses": losses, "ties": ties},
        "aggregate_scores": {"treatment": aggregate_treatment, "control": aggregate_control},
        "critical_invariant_regressions": critical_regressions,
        "treatment_automatic_failures": automatic_failures,
        "fidelity_losses": fidelity_losses,
        "cost": cost,
        "failure_reasons": reasons,
        "errors": errors,
        "claim": policy["claim_on_pass"] if passed else policy["claim_on_fail"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Unblind and score Clarify visual A/B judgment.")
    ap.add_argument("judgment")
    ap.add_argument("condition_map")
    ap.add_argument("blinded_dir")
    ap.add_argument("--policy", default=str(Path(__file__).with_name("promotion-policy.json")))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    judgment = load_json(Path(args.judgment))
    condition_map = load_json(Path(args.condition_map))
    policy = load_json(Path(args.policy))
    result = evaluate(judgment, condition_map, policy, Path(args.blinded_dir))
    print(json.dumps(result, ensure_ascii=False, indent=None if args.json else 2))
    if result["status"] != "valid":
        return 2
    return 0 if result["promotion_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
