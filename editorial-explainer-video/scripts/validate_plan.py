#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path

USABLE = {"ALLOW", "ALLOW_WITH_QUALIFICATION"}
CAUSE_LEVELS = {"PLAUSIBLE_CAUSE", "SUPPORTED_CAUSE"}

def norm(s):
    return " ".join(str(s).lower().split())

def issue(code, path, message):
    return {"code": code, "path": path, "message": message}

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate(plan_path, ledger_path):
    errors, warnings = [], []
    raw_ledger = Path(ledger_path).read_bytes()
    digest = hashlib.sha256(raw_ledger).hexdigest()
    plan, ledger = load(plan_path), json.loads(raw_ledger.decode("utf-8"))
    if plan.get("schema") != "editorial-explainer-plan/v1":
        errors.append(issue("plan_schema_invalid", "schema", "expected editorial-explainer-plan/v1"))
    if ledger.get("schema") != "editorial-evidence-ledger/v1":
        errors.append(issue("ledger_schema_invalid", "ledger.schema", "expected editorial-evidence-ledger/v1"))
    if plan.get("evidence_ledger_sha256") != digest:
        errors.append(issue("evidence_hash_mismatch", "evidence_ledger_sha256", "plan is not bound to the supplied ledger bytes"))

    claims = {}
    for i, c in enumerate(ledger.get("claims", [])):
        cid = c.get("claim_id")
        if not cid:
            continue
        if cid in claims:
            errors.append(issue("duplicate_claim_id", f"ledger.claims[{i}].claim_id", f"duplicate {cid}"))
        claims[cid] = c

    thesis = plan.get("thesis") or {}
    must = thesis.get("must_prove_claim_refs") or []
    if not must:
        errors.append(issue("must_prove_missing", "thesis.must_prove_claim_refs", "thesis needs at least one load-bearing claim"))

    def check_ref(cid, path):
        c = claims.get(cid)
        if c is None:
            errors.append(issue("claim_ref_missing", path, f"claim {cid} is absent from ledger")); return None
        if c.get("editorial_use") not in USABLE:
            errors.append(issue("claim_ref_blocked", path, f"claim {cid} is not permitted for downstream use"))
        return c

    for i, cid in enumerate(must):
        check_ref(cid, f"thesis.must_prove_claim_refs[{i}]")

    level = thesis.get("mechanism_epistemic_level")
    must_claims = [claims.get(cid) for cid in must if claims.get(cid)]
    causal_claims = [c for c in must_claims if c.get("claim_type") == "CAUSAL"]
    if level in CAUSE_LEVELS and not causal_claims:
        errors.append(issue("causal_level_without_causal_claim", "thesis.mechanism_epistemic_level", "causal mechanism level requires a causal must-prove claim"))
    if level == "SUPPORTED_CAUSE" and any(c.get("epistemic_status") != "VERIFIED" for c in causal_claims):
        errors.append(issue("causal_overclaim", "thesis.mechanism_epistemic_level", "SUPPORTED_CAUSE requires every load-bearing causal claim to be VERIFIED"))

    def qualifiers_ok(obj, objpath, cid, c):
        required = c.get("required_qualifiers") or []
        if not required:
            return
        ack = (obj.get("qualifier_acknowledgements") or {}).get(cid, [])
        missing = [q for q in required if q not in ack]
        if missing:
            errors.append(issue("required_qualifier_missing", f"{objpath}.qualifier_acknowledgements.{cid}", f"missing required qualifier(s): {missing}"))

    script_claims, beat_claims = set(), set()
    seen_blocks, block_orders = set(), set()
    for i, b in enumerate(plan.get("script_blocks") or []):
        path = f"script_blocks[{i}]"
        bid, order = b.get("block_id"), b.get("order")
        if not bid or bid in seen_blocks:
            errors.append(issue("script_block_id_invalid", f"{path}.block_id", "script block ids must be non-empty and unique"))
        seen_blocks.add(bid)
        if not isinstance(order, int) or order < 1 or order in block_orders:
            errors.append(issue("script_order_invalid", f"{path}.order", "script orders must be unique positive integers"))
        block_orders.add(order)
        refs = b.get("claim_refs") or []
        if b.get("fact_bearing") and not refs:
            errors.append(issue("factual_script_without_claims", f"{path}.claim_refs", "fact-bearing script block requires claim refs"))
        for j, cid in enumerate(refs):
            c = check_ref(cid, f"{path}.claim_refs[{j}]")
            if c:
                script_claims.add(cid); qualifiers_ok(b, path, cid, c)

    seen_beats, beat_orders = set(), set()
    beats = plan.get("beats") or []
    for i, b in enumerate(beats):
        path = f"beats[{i}]"; bid, order = b.get("beat_id"), b.get("order")
        if not bid or bid in seen_beats:
            errors.append(issue("beat_id_invalid", f"{path}.beat_id", "beat ids must be non-empty and unique"))
        seen_beats.add(bid)
        if not isinstance(order, int) or order < 1 or order in beat_orders:
            errors.append(issue("beat_order_invalid", f"{path}.order", "beat orders must be unique positive integers"))
        beat_orders.add(order)
        refs = b.get("claim_refs") or []
        if b.get("fact_bearing") and not refs:
            errors.append(issue("factual_beat_without_claims", f"{path}.claim_refs", "fact-bearing beat requires claim refs"))
        for j, cid in enumerate(refs):
            c = check_ref(cid, f"{path}.claim_refs[{j}]")
            if c:
                beat_claims.add(cid); qualifiers_ok(b, path, cid, c)
        before, after = b.get("viewer_state_before_pt_br", ""), b.get("viewer_state_after_pt_br", "")
        if norm(before) and norm(before) == norm(after):
            errors.append(issue("viewer_state_no_progress", path, "viewer state must materially change across the beat"))
        if not b.get("closure_test_pt_br"):
            errors.append(issue("closure_test_missing", f"{path}.closure_test_pt_br", "beat requires a closure test"))

    if beats:
        orders = [b.get("order") for b in beats if isinstance(b.get("order"), int)]
        if orders != sorted(orders):
            warnings.append(issue("beat_list_not_sorted", "beats", "beat objects are not listed in ascending order"))

    for cid in must:
        if cid not in script_claims:
            errors.append(issue("must_prove_absent_from_script", "script_blocks", f"must-prove claim {cid} is absent from script"))
        if cid not in beat_claims:
            errors.append(issue("must_prove_absent_from_beats", "beats", f"must-prove claim {cid} is absent from beats"))

    receipt = {
        "schema":"editorial-explainer-validation/v1",
        "status":"PASSED" if not errors else "FAILED",
        "plan_sha256":hashlib.sha256(Path(plan_path).read_bytes()).hexdigest(),
        "evidence_ledger_sha256":digest,
        "counts":{"claims":len(claims),"script_blocks":len(plan.get("script_blocks") or []),"beats":len(beats)},
        "errors":errors,"warnings":warnings,
        "behavioral_editorial_review":"pending"
    }
    return receipt

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('plan'); ap.add_argument('ledger'); ap.add_argument('--json',action='store_true'); args=ap.parse_args()
    try: receipt=validate(args.plan,args.ledger)
    except Exception as e:
        receipt={"schema":"editorial-explainer-validation/v1","status":"FAILED","errors":[issue("validator_exception","$",str(e))],"warnings":[],"behavioral_editorial_review":"pending"}
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    return 0 if receipt.get('status')=='PASSED' else 1
if __name__=='__main__': sys.exit(main())
