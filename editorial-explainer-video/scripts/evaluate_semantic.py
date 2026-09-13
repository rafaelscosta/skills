#!/usr/bin/env python3
import argparse, hashlib, json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate_plan import validate as validate_plan
from validate_capabilities import validate as validate_capabilities

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def ratio(num, den):
    return 1.0 if den == 0 else round(num / den, 6)

def issue(code, path, message):
    return {"code": code, "path": path, "message": message}

def evaluate(plan_path, ledger_path, manifest_path):
    hard_fails, warnings = [], []
    plan_receipt = validate_plan(plan_path, ledger_path)
    cap_receipt = validate_capabilities(manifest_path, plan_path, ledger_path)
    if plan_receipt.get("status") != "PASSED":
        hard_fails.append(issue("PLAN_VALIDATION_FAILED", "plan", "plan validator did not pass"))
    if cap_receipt.get("status") != "PASSED":
        hard_fails.append(issue("CAPABILITY_VALIDATION_FAILED", "capability_manifest", "capability validator did not pass"))

    plan, ledger, manifest = load(plan_path), load(ledger_path), load(manifest_path)
    claims = {c.get("claim_id"): c for c in ledger.get("claims", []) if c.get("claim_id")}
    must = list((plan.get("thesis") or {}).get("must_prove_claim_refs") or [])
    script = list(plan.get("script_blocks") or [])
    beats = list(plan.get("beats") or [])

    script_refs = [cid for b in script for cid in (b.get("claim_refs") or [])]
    beat_refs = [cid for b in beats for cid in (b.get("claim_refs") or [])]
    unique_used = set(script_refs) | set(beat_refs)
    traceable = sum(1 for cid in unique_used if cid in claims and claims[cid].get("editorial_use") in {"ALLOW", "ALLOW_WITH_QUALIFICATION"})

    required_qualifier_uses = 0
    survived_qualifier_uses = 0
    for obj in script + beats:
        for cid in obj.get("claim_refs") or []:
            c = claims.get(cid) or {}
            req = list(c.get("required_qualifiers") or [])
            if not req:
                continue
            required_qualifier_uses += 1
            ack = ((obj.get("qualifier_acknowledgements") or {}).get(cid) or [])
            if all(q in ack for q in req):
                survived_qualifier_uses += 1

    fact_beats = [b for b in beats if b.get("fact_bearing")]
    supported_fact_beats = [b for b in fact_beats if b.get("claim_refs")]
    evidence_required_beats = [b for b in beats if (b.get("visual") or {}).get("evidence_required")]
    evidence_bound_visual_beats = [b for b in evidence_required_beats if b.get("claim_refs")]
    progressed = [b for b in beats if " ".join(str(b.get("viewer_state_before_pt_br", "")).lower().split()) != " ".join(str(b.get("viewer_state_after_pt_br", "")).lower().split())]

    route_map = {r.get("beat_id"): r for r in manifest.get("beat_routes") or [] if r.get("beat_id")}
    route_covered = sum(1 for b in beats if b.get("beat_id") in route_map and (route_map[b.get("beat_id")].get("packet_ids") or []))

    # Handoff fidelity is exact only when the capability validator passed.
    handoff_fidelity = 1.0 if cap_receipt.get("status") == "PASSED" else 0.0
    must_script = sum(1 for cid in must if cid in set(script_refs))
    must_beats = sum(1 for cid in must if cid in set(beat_refs))

    total_words = 0
    total_duration = 0.0
    max_wps = 0.0
    max_claims = 0
    for b in beats:
        words = len(str(b.get("narration_pt_br", "")).split())
        duration = float(b.get("target_duration_seconds") or 0)
        total_words += words
        total_duration += duration
        if duration > 0:
            max_wps = max(max_wps, words / duration)
        max_claims = max(max_claims, len(b.get("claim_refs") or []))

    metrics = {
        "claim_traceability_ratio": ratio(traceable, len(unique_used)),
        "must_prove_script_coverage_ratio": ratio(must_script, len(must)),
        "must_prove_beat_coverage_ratio": ratio(must_beats, len(must)),
        "qualifier_survival_ratio": ratio(survived_qualifier_uses, required_qualifier_uses),
        "fact_bearing_beat_support_ratio": ratio(len(supported_fact_beats), len(fact_beats)),
        "visual_evidence_traceability_ratio": ratio(len(evidence_bound_visual_beats), len(evidence_required_beats)),
        "viewer_state_progress_ratio": ratio(len(progressed), len(beats)),
        "route_coverage_ratio": ratio(route_covered, len(beats)),
        "handoff_fidelity_ratio": handoff_fidelity,
    }
    diagnostics = {
        "total_beats": len(beats),
        "total_narration_words": total_words,
        "target_duration_seconds_total": round(total_duration, 3),
        "overall_narration_words_per_second": round((total_words / total_duration), 3) if total_duration > 0 else None,
        "max_beat_words_per_second": round(max_wps, 3),
        "max_claim_refs_per_beat": max_claims,
        "note": "Pacing/load values are diagnostics only and never create a quality verdict by themselves."
    }
    critical = [
        "claim_traceability_ratio", "must_prove_script_coverage_ratio", "must_prove_beat_coverage_ratio",
        "qualifier_survival_ratio", "fact_bearing_beat_support_ratio", "visual_evidence_traceability_ratio",
        "viewer_state_progress_ratio", "route_coverage_ratio", "handoff_fidelity_ratio"
    ]
    for key in critical:
        if metrics[key] < 1.0:
            hard_fails.append(issue("INTEGRATED_INVARIANT_FAILED", f"metrics.{key}", f"{key} must equal 1.0 for machine pass"))

    return {
        "schema": "editorial-explainer-machine-eval/v1",
        "status": "PASSED" if not hard_fails else "FAILED",
        "plan_sha256": sha(plan_path),
        "evidence_ledger_sha256": sha(ledger_path),
        "capability_manifest_sha256": sha(manifest_path),
        "metrics": metrics,
        "diagnostics": diagnostics,
        "hard_fails": hard_fails,
        "warnings": warnings,
        "reviewer_eval": "required_for_editorial_or_audiovisual_quality_claims"
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("ledger")
    ap.add_argument("manifest")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        out = evaluate(a.plan, a.ledger, a.manifest)
    except Exception as e:
        out = {"schema":"editorial-explainer-machine-eval/v1","status":"FAILED","hard_fails":[issue("EVAL_EXCEPTION","$",str(e))],"warnings":[]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("status") == "PASSED" else 1

if __name__ == "__main__":
    sys.exit(main())
