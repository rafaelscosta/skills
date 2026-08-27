#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path

STATUS_VALUE = {"failed": 0, "partial": 1, "passed": 2}
EXPECTED_CASES = {"refund-operational-flow", "approval-loop", "source-bound-causal"}


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
        if not isinstance(e, (int, float)) or isinstance(e, bool):
            return None
        if not isinstance(t, (int, float)) or isinstance(t, bool):
            return None
        elapsed.append(float(e))
        tools.append(float(t))
    if not elapsed:
        return None
    return {
        "median_elapsed_ms": statistics.median(elapsed),
        "median_tool_calls": statistics.median(tools),
    }


def validate_candidate_result(case_id: str, label: str, result: dict, errors: list[str]) -> None:
    if not isinstance(result, dict):
        errors.append(f"{case_id} candidate {label} result must be an object")
        return
    invariants = result.get("critical_invariants")
    if not isinstance(invariants, dict) or not invariants:
        errors.append(f"{case_id} candidate {label} must score at least one critical invariant")
    else:
        for invariant, status in invariants.items():
            if not isinstance(invariant, str) or not invariant.strip() or status not in STATUS_VALUE:
                errors.append(f"{case_id} candidate {label} has invalid critical invariant status")
                break
    failures = result.get("automatic_failures")
    if not isinstance(failures, list) or any(not isinstance(x, str) for x in failures):
        errors.append(f"{case_id} candidate {label} automatic_failures must be a string array")
    scores = result.get("scores")
    if not isinstance(scores, dict) or not scores:
        errors.append(f"{case_id} candidate {label} scores must be a non-empty object")
        return
    for dimension, score in scores.items():
        if not isinstance(dimension, str) or not dimension.strip():
            errors.append(f"{case_id} candidate {label} has invalid score dimension")
            break
        if not isinstance(score, int) or isinstance(score, bool) or score < 0 or score > 2:
            errors.append(f"{case_id} candidate {label} score {dimension!r} must be integer 0..2")
            break
    total = result.get("total")
    expected_total = sum(scores.values()) if all(isinstance(v, int) and not isinstance(v, bool) for v in scores.values()) else None
    if not isinstance(total, int) or isinstance(total, bool) or expected_total is None or total != expected_total:
        errors.append(f"{case_id} candidate {label} total must equal the sum of scores")


def evaluate(judgment: dict, condition_map: dict, policy: dict, blinded: Path) -> dict:
    errors: list[str] = []
    mapping = condition_map.get("mapping") or {}
    if set(mapping) != {"A", "B"} or set(mapping.values()) != {"control", "treatment"}:
        errors.append("invalid condition map")
        return {"status": "invalid", "errors": errors}

    manifest_path = blinded / "manifest.json"
    if not manifest_path.is_file():
        return {"status": "invalid", "errors": ["blinded manifest missing"]}
    manifest_sha = sha256(manifest_path)
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:
        return {"status": "invalid", "errors": [f"invalid blinded manifest: {exc}"]}
    if manifest.get("schema_version") != "clarify-visual-ab-blinded/v1":
        errors.append("unexpected blinded manifest schema")
    candidates_manifest = manifest.get("candidates") or {}
    if set(candidates_manifest) != {"A", "B"}:
        errors.append("blinded manifest must contain candidates A and B")
    else:
        for label in ("A", "B"):
            case_set = set((candidates_manifest.get(label) or {}).get("cases") or {})
            if case_set != EXPECTED_CASES:
                errors.append(f"candidate {label} blinded case set mismatch")

    if condition_map.get("blinded_manifest_sha256") != manifest_sha:
        errors.append("condition map manifest hash mismatch")
    if judgment.get("schema_version") != "clarify-visual-ab-judgment/v1":
        errors.append("unexpected judgment schema")
    if judgment.get("blinded_manifest_sha256") != manifest_sha:
        errors.append("judgment manifest hash mismatch")
    if judgment.get("condition_mapping_seen") is not False:
        errors.append("judge must attest condition_mapping_seen=false")
    judge = judgment.get("judge")
    if not isinstance(judge, dict) or not str(judge.get("id", "")).strip() or judge.get("type") not in {"human", "model"}:
        errors.append("judgment requires identified human or model judge")

    treatment = candidate_for(mapping, "treatment")
    control = candidate_for(mapping, "control")
    cases = judgment.get("cases") or []
    judged_ids = {c.get("case_id") for c in cases if isinstance(c, dict)}
    if len(cases) != 3 or judged_ids != EXPECTED_CASES:
        errors.append("judgment must contain exactly the expected three cases")

    wins = losses = ties = 0
    critical_regressions = []
    automatic_failures = []
    fidelity_losses = []
    aggregate_treatment = 0
    aggregate_control = 0

    for case in cases:
        if not isinstance(case, dict):
            errors.append("each judgment case must be an object")
            continue
        case_id = case.get("case_id")
        winner = case.get("winner")
        if winner == treatment:
            wins += 1
        elif winner == control:
            losses += 1
        elif winner == "tie":
            ties += 1
        else:
            errors.append(f"invalid winner for {case_id}")

        for label in ("A", "B"):
            validate_candidate_result(str(case_id), label, case.get(label), errors)
        t = case.get(treatment) if isinstance(case.get(treatment), dict) else {}
        c = case.get(control) if isinstance(case.get(control), dict) else {}
        if isinstance(t.get("total"), int) and not isinstance(t.get("total"), bool):
            aggregate_treatment += t["total"]
        if isinstance(c.get("total"), int) and not isinstance(c.get("total"), bool):
            aggregate_control += c["total"]

        ti = t.get("critical_invariants") if isinstance(t.get("critical_invariants"), dict) else {}
        ci = c.get("critical_invariants") if isinstance(c.get("critical_invariants"), dict) else {}
        for invariant in set(ti) | set(ci):
            tv = STATUS_VALUE.get(ti.get(invariant), -1)
            cv = STATUS_VALUE.get(ci.get(invariant), -1)
            if tv < cv:
                critical_regressions.append({
                    "case_id": case_id,
                    "invariant": invariant,
                    "treatment": ti.get(invariant),
                    "control": ci.get(invariant),
                })

        for failure in t.get("automatic_failures") or []:
            automatic_failures.append({"case_id": case_id, "failure": failure})

        ts = t.get("scores") if isinstance(t.get("scores"), dict) else {}
        cs = c.get("scores") if isinstance(c.get("scores"), dict) else {}
        if "fidelity" in ts and "fidelity" in cs and ts["fidelity"] < cs["fidelity"]:
            fidelity_losses.append({
                "case_id": case_id,
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
    try:
        tcost = comparable_cost(blinded, treatment)
        ccost = comparable_cost(blinded, control)
    except Exception as exc:
        errors.append(f"cost receipt read failure: {exc}")
        tcost = ccost = None
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
