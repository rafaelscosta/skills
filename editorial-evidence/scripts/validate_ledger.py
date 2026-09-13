#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA = "editorial-evidence-ledger/v1"
CLAIM_TYPES = {"FACT","QUANTITATIVE","CAUSAL","CORRELATIONAL","ESTIMATE","QUOTE","INTERPRETATION","EXPERT_OPINION","UNCERTAIN"}
MATERIALITIES = {"HIGH","MEDIUM","LOW"}
STATUSES = {"VERIFIED","QUALIFIED","CONTESTED","UNSUPPORTED","STALE","RETRACTED"}
USES = {"ALLOW","ALLOW_WITH_QUALIFICATION","BLOCK"}
RELATIONS = {"SUPPORTS","REFUTES","CONTEXTUALIZES"}
AUTHORITIES = {"HIGH","MEDIUM","LOW","UNKNOWN"}
FRESHNESS = {"CURRENT","AGING","STALE","UNKNOWN"}


def issue(code, path, message):
    return {"code": code, "path": path, "message": message}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(data):
    errors, warnings = [], []
    if data.get("schema") != SCHEMA:
        errors.append(issue("ledger_schema", "schema", f"expected {SCHEMA}"))
    if not nonempty(data.get("subject")):
        errors.append(issue("subject_missing", "subject", "subject must be non-empty"))
    if data.get("mode") not in {"standard","heightened","adversarial"}:
        errors.append(issue("mode_invalid", "mode", "mode must be standard, heightened, or adversarial"))

    sources = data.get("sources")
    claims = data.get("claims")
    if not isinstance(sources, list):
        errors.append(issue("sources_type", "sources", "sources must be an array"))
        sources = []
    if not isinstance(claims, list):
        errors.append(issue("claims_type", "claims", "claims must be an array"))
        claims = []

    source_map = {}
    for i, src in enumerate(sources):
        p = f"sources[{i}]"
        if not isinstance(src, dict):
            errors.append(issue("source_type", p, "source must be an object"))
            continue
        sid = src.get("source_id")
        if not nonempty(sid):
            errors.append(issue("source_id_missing", f"{p}.source_id", "source_id required"))
            continue
        if sid in source_map:
            errors.append(issue("source_id_duplicate", f"{p}.source_id", f"duplicate source id {sid}"))
        source_map[sid] = src
        for key in ("title","locator"):
            if not nonempty(src.get(key)):
                errors.append(issue("source_field_missing", f"{p}.{key}", f"{key} required"))
        if src.get("authority") not in AUTHORITIES:
            errors.append(issue("source_authority_invalid", f"{p}.authority", "invalid authority"))
        if src.get("freshness") not in FRESHNESS:
            errors.append(issue("source_freshness_invalid", f"{p}.freshness", "invalid freshness"))

    seen_claims = set()
    for i, claim in enumerate(claims):
        p = f"claims[{i}]"
        if not isinstance(claim, dict):
            errors.append(issue("claim_type", p, "claim must be an object"))
            continue
        cid = claim.get("claim_id")
        if not nonempty(cid):
            errors.append(issue("claim_id_missing", f"{p}.claim_id", "claim_id required"))
            continue
        if cid in seen_claims:
            errors.append(issue("claim_id_duplicate", f"{p}.claim_id", f"duplicate claim id {cid}"))
        seen_claims.add(cid)

        if not nonempty(claim.get("statement")):
            errors.append(issue("claim_statement_missing", f"{p}.statement", "statement required"))
        ctype = claim.get("claim_type")
        materiality = claim.get("materiality")
        status = claim.get("epistemic_status")
        use = claim.get("editorial_use")
        if ctype not in CLAIM_TYPES:
            errors.append(issue("claim_type_invalid", f"{p}.claim_type", "invalid claim_type"))
        if materiality not in MATERIALITIES:
            errors.append(issue("materiality_invalid", f"{p}.materiality", "invalid materiality"))
        if status not in STATUSES:
            errors.append(issue("status_invalid", f"{p}.epistemic_status", "invalid epistemic_status"))
        if use not in USES:
            errors.append(issue("editorial_use_invalid", f"{p}.editorial_use", "invalid editorial_use"))

        qualifiers = claim.get("required_qualifiers")
        if not isinstance(qualifiers, list):
            errors.append(issue("qualifiers_type", f"{p}.required_qualifiers", "required_qualifiers must be an array"))
            qualifiers = []
        if status == "QUALIFIED" and not any(nonempty(q) for q in qualifiers):
            errors.append(issue("qualified_without_qualifier", f"{p}.required_qualifiers", "QUALIFIED claims need an explicit qualifier"))

        if status in {"UNSUPPORTED","STALE","RETRACTED"} and use != "BLOCK":
            errors.append(issue("blocked_status_allowed", f"{p}.editorial_use", f"{status} claims must be BLOCK"))
        if status == "CONTESTED" and use == "ALLOW":
            errors.append(issue("contested_unqualified", f"{p}.editorial_use", "CONTESTED claims cannot be ALLOW"))
        if status == "QUALIFIED" and use == "ALLOW":
            errors.append(issue("qualified_unqualified", f"{p}.editorial_use", "QUALIFIED claims cannot be ALLOW"))

        bindings = claim.get("source_bindings")
        if not isinstance(bindings, list):
            errors.append(issue("bindings_type", f"{p}.source_bindings", "source_bindings must be an array"))
            bindings = []
        support_bindings = []
        support_authorities = []
        support_freshness = []
        for j, binding in enumerate(bindings):
            bp = f"{p}.source_bindings[{j}]"
            if not isinstance(binding, dict):
                errors.append(issue("binding_type", bp, "binding must be an object"))
                continue
            sid = binding.get("source_id")
            if sid not in source_map:
                errors.append(issue("binding_missing_source", f"{bp}.source_id", f"unknown source {sid}"))
            relation = binding.get("relation")
            if relation not in RELATIONS:
                errors.append(issue("binding_relation_invalid", f"{bp}.relation", "invalid relation"))
            if relation == "SUPPORTS":
                support_bindings.append(binding)
                src = source_map.get(sid, {})
                support_authorities.append(src.get("authority"))
                support_freshness.append(src.get("freshness"))
            if materiality == "HIGH" and not nonempty(binding.get("locator")):
                errors.append(issue("high_materiality_locator_missing", f"{bp}.locator", "high-materiality bindings require precise locators"))

        if status == "VERIFIED" and materiality in {"HIGH","MEDIUM"} and not support_bindings:
            errors.append(issue("verified_without_support", f"{p}.source_bindings", "verified material claim needs supporting evidence"))
        if materiality == "HIGH" and support_bindings and not any(a in {"HIGH","MEDIUM"} for a in support_authorities):
            warnings.append(issue("weak_authority_high_materiality", p, "high-materiality claim has no HIGH/MEDIUM authority supporting source"))

        if claim.get("time_sensitive") is True and status in {"VERIFIED","QUALIFIED"}:
            if not nonempty(claim.get("freshness_checked_at")):
                errors.append(issue("freshness_check_missing", f"{p}.freshness_checked_at", "time-sensitive usable claims require freshness_checked_at"))
            if status == "VERIFIED" and support_freshness and all(f in {"STALE","UNKNOWN"} for f in support_freshness):
                errors.append(issue("verified_on_stale_sources", p, "verified time-sensitive claim cannot rely only on stale/unknown supporting sources"))

        if ctype == "QUANTITATIVE":
            numeric = claim.get("numeric_context")
            if not isinstance(numeric, (dict, str)) or (isinstance(numeric, str) and not numeric.strip()) or (isinstance(numeric, dict) and not numeric):
                target = errors if materiality == "HIGH" else warnings
                target.append(issue("numeric_context_missing", f"{p}.numeric_context", "quantitative claim needs metric/unit/period/comparison context"))

        if ctype == "QUOTE":
            quote = claim.get("quote")
            if not isinstance(quote, dict) or not nonempty(quote.get("original_text")) or not nonempty(quote.get("source_language")):
                errors.append(issue("quote_original_missing", f"{p}.quote", "quote requires original_text and source_language"))

        if ctype == "CAUSAL" and status == "VERIFIED":
            review = claim.get("causal_review")
            if not isinstance(review, dict) or not nonempty(review.get("basis")) or review.get("contradiction_search") is not True:
                errors.append(issue("causal_review_missing", f"{p}.causal_review", "verified causal claim requires basis and contradiction_search=true"))

    return errors, warnings, {"sources": len(sources), "claims": len(claims)}


def main():
    ap = argparse.ArgumentParser(description="Validate editorial-evidence-ledger/v1")
    ap.add_argument("ledger")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    path = Path(args.ledger)
    try:
        raw = path.read_bytes()
        data = json.loads(raw)
    except Exception as exc:
        receipt = {"schema":"editorial-evidence-validation/v1","status":"ERROR","error":str(exc)}
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 2
    errors, warnings, counts = validate(data)
    receipt = {
        "schema":"editorial-evidence-validation/v1",
        "status":"PASSED" if not errors else "FAILED",
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "counts": counts,
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    else:
        print(receipt["status"])
        for item in errors + warnings:
            print(f"{item['code']}: {item['path']}: {item['message']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
