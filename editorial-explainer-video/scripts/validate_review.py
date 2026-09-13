#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path

WEIGHTS = {
    "plan": {
        "factual_epistemic_integrity":20, "explanatory_clarity":20, "narrative_coherence":20,
        "beat_closure":15, "visual_explanatory_value":15, "pacing_cognitive_load":10,
    },
    "owner_output": {
        "factual_epistemic_integrity":20, "explanatory_clarity":15, "narrative_coherence":10,
        "beat_closure":10, "visual_explanatory_value":20, "pacing_cognitive_load":10,
        "provenance_rights":5, "audiovisual_coherence":10,
    },
    "rough_cut": {
        "factual_epistemic_integrity":20, "explanatory_clarity":15, "narrative_coherence":15,
        "visual_explanatory_value":15, "audiovisual_coherence":10, "motion_editing_craft":10,
        "audio_quality":5, "pacing_cognitive_load":5, "provenance_rights":5,
    },
    "final": {
        "factual_epistemic_integrity":20, "explanatory_clarity":15, "narrative_coherence":15,
        "visual_explanatory_value":15, "audiovisual_coherence":10, "motion_editing_craft":10,
        "audio_quality":5, "pacing_cognitive_load":5, "provenance_rights":5,
    },
}
HARD_CODES = {
    "UNSUPPORTED_CRITICAL_CLAIM", "QUALIFIER_DROPPED", "CAUSALITY_OVERSTATED",
    "VISUAL_CONTRADICTS_CLAIM", "STALE_EVIDENCE_BINDING", "MISSING_REQUIRED_OWNER_OUTPUT",
    "UNREADABLE_LOAD_BEARING_VISUAL", "NARRATION_VISUAL_MISMATCH", "RIGHTS_OR_PROVENANCE_BLOCKER",
}

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def issue(code,path,message): return {"code":code,"path":path,"message":message}

def validate(review_path, plan_path, ledger_path, manifest_path):
    errors=[]; warnings=[]
    review=load(review_path); stage=review.get("artifact_stage")
    if review.get("schema") != "editorial-explainer-review/v1":
        errors.append(issue("review_schema_invalid","schema","expected editorial-explainer-review/v1"))
    if stage not in WEIGHTS:
        errors.append(issue("stage_invalid","artifact_stage",f"unsupported stage {stage}")); weights={}
    else: weights=WEIGHTS[stage]
    reviewer=review.get("reviewer") or {}
    if not reviewer.get("id") or reviewer.get("type") not in {"human","vision-model","language-model"}:
        errors.append(issue("reviewer_invalid","reviewer","reviewer id and supported type are required"))
    bindings=review.get("bindings") or {}
    expected={"plan_sha256":sha(plan_path),"evidence_ledger_sha256":sha(ledger_path),"capability_manifest_sha256":sha(manifest_path)}
    for k,v in expected.items():
        if bindings.get(k)!=v: errors.append(issue("review_binding_mismatch",f"bindings.{k}",f"expected {v}"))
    dims=review.get("dimensions") or {}
    score_pairs=[]
    for name,weight in weights.items():
        d=dims.get(name)
        if not isinstance(d,dict):
            errors.append(issue("dimension_missing",f"dimensions.{name}","required stage dimension missing")); continue
        status=d.get("status")
        if status!="SCORED":
            errors.append(issue("dimension_unscored",f"dimensions.{name}.status","required stage dimension must be SCORED")); continue
        score=d.get("score")
        if not isinstance(score,(int,float)) or not (0<=score<=5):
            errors.append(issue("dimension_score_invalid",f"dimensions.{name}.score","score must be 0..5")); continue
        if not str(d.get("rationale") or "").strip():
            errors.append(issue("dimension_rationale_missing",f"dimensions.{name}.rationale","scored dimension requires rationale"))
        if not (d.get("evidence_refs") or []):
            warnings.append(issue("dimension_evidence_ref_missing",f"dimensions.{name}.evidence_refs","scored dimension should name inspected evidence"))
        score_pairs.append((float(score),weight,name))
    for name,d in dims.items():
        if name in weights: continue
        if isinstance(d,dict) and d.get("status")=="SCORED":
            warnings.append(issue("extra_dimension_not_weighted",f"dimensions.{name}","dimension is recorded but not weighted at this stage"))
    hard=[]
    for i,h in enumerate(review.get("hard_fails") or []):
        code=h.get("code") if isinstance(h,dict) else None
        if code not in HARD_CODES:
            errors.append(issue("hard_fail_code_invalid",f"hard_fails[{i}].code",f"unsupported hard-fail code {code}"))
        else: hard.append(h)
        if isinstance(h,dict) and not str(h.get("evidence") or "").strip():
            errors.append(issue("hard_fail_evidence_missing",f"hard_fails[{i}].evidence","hard fail requires concrete evidence"))
    weighted=None
    if weights and len(score_pairs)==len(weights):
        weighted=round(sum((score/5.0)*weight for score,weight,_ in score_pairs),2)
    min_score=min([s for s,_,_ in score_pairs], default=None)
    expected_verdict="INSUFFICIENT_EVIDENCE"
    if weighted is not None:
        if hard or (min_score is not None and min_score<3) or weighted<70: expected_verdict="FAIL"
        elif weighted>=85 and min_score is not None and min_score>=3: expected_verdict="PASS"
        else: expected_verdict="REVISE"
    if review.get("verdict") != expected_verdict:
        errors.append(issue("verdict_mismatch","verdict",f"expected {expected_verdict} from rubric, got {review.get('verdict')}"))
    return {
        "schema":"editorial-explainer-review-validation/v1",
        "status":"PASSED" if not errors else "FAILED",
        "review_sha256":sha(review_path),
        "artifact_stage":stage,
        "weighted_score":weighted,
        "expected_verdict":expected_verdict,
        "hard_fail_count":len(hard),
        "errors":errors,"warnings":warnings,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('review'); ap.add_argument('plan'); ap.add_argument('ledger'); ap.add_argument('manifest'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    try:r=validate(a.review,a.plan,a.ledger,a.manifest)
    except Exception as e:r={"schema":"editorial-explainer-review-validation/v1","status":"FAILED","errors":[issue("validator_exception","$",str(e))],"warnings":[]}
    print(json.dumps(r,ensure_ascii=False,indent=2)); return 0 if r.get('status')=='PASSED' else 1
if __name__=='__main__': sys.exit(main())
