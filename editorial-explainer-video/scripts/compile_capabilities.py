#!/usr/bin/env python3
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path

KNOWN_OWNERS = {
    "data-viz-selector", "visual-semantic-compiler", "media-use",
    "motion-graphics", "motion-studio", "general-video"
}
ROUTES = {
    "SCALE": ["data-viz-selector", "motion-graphics"],
    "COMPARISON": ["data-viz-selector", "motion-graphics"],
    "CAUSALITY": ["visual-semantic-compiler", "motion-graphics"],
    "MECHANISM": ["visual-semantic-compiler", "motion-graphics"],
    "RELATIONSHIP": ["visual-semantic-compiler", "motion-graphics"],
    "CHRONOLOGY": ["visual-semantic-compiler", "motion-graphics"],
    "EVIDENCE": ["media-use", "motion-graphics"],
    "ATMOSPHERE": ["media-use", "motion-graphics"],
    "LOCATION": ["motion-graphics"],
    "DEFINITION": ["motion-graphics"],
    "CONTRAST": ["motion-graphics"],
    "EMPHASIS": ["motion-graphics"],
    "TRANSITION": ["motion-graphics"],
}
STAGES = {
    "data-viz-selector": "visual_spec",
    "visual-semantic-compiler": "semantic_visual",
    "media-use": "media_resolution",
    "motion-graphics": "motion_unit",
    "motion-studio": "creative_direction",
    "general-video": "sequence_assembly",
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def slug(s):
    return "".join(c if c.isalnum() else "-" for c in str(s)).strip("-").upper()

def import_validator():
    here = Path(__file__).resolve().parent / "validate_plan.py"
    spec = importlib.util.spec_from_file_location("validate_plan", here)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def issue(code, path, message):
    return {"code": code, "path": path, "message": message}

def claim_snapshot(claim):
    keys = ["claim_id", "statement", "claim_type", "materiality", "epistemic_status",
            "editorial_use", "required_qualifiers", "source_bindings", "numeric_context", "causal_review"]
    return {k: claim[k] for k in keys if k in claim}

def vsc_type(fn):
    return {"CAUSALITY":"causal", "CHRONOLOGY":"timeline", "MECHANISM":"flow",
            "RELATIONSHIP":"architecture"}.get(fn, "flow")

def motion_hint(fn, intent):
    if fn in {"SCALE", "COMPARISON"}: return "chart-or-stat"
    if fn == "LOCATION": return "map"
    if fn == "EVIDENCE": return "news-or-source-card"
    if fn == "EMPHASIS": return "kinetic-type-or-stat"
    if fn == "TRANSITION": return "transition"
    return intent or "editorial-motion"

def payload_for(owner, beat, claim_ctx, upstream_packet_ids):
    fn = beat.get("explanation_function")
    base = {
        "question_pt_br": beat.get("question_pt_br"),
        "narration_pt_br": beat.get("narration_pt_br"),
        "viewer_state_before_pt_br": beat.get("viewer_state_before_pt_br"),
        "viewer_state_after_pt_br": beat.get("viewer_state_after_pt_br"),
        "closure_test_pt_br": beat.get("closure_test_pt_br"),
        "representation_intent": (beat.get("visual") or {}).get("representation_intent"),
        "claim_context": claim_ctx,
        "upstream_packet_ids": upstream_packet_ids,
    }
    if owner == "data-viz-selector":
        base.update({"analytical_task": fn.lower(), "audience_mode": "public-editorial",
                     "instruction": "Choose the truthful visual form from the analytical question; do not invent data."})
    elif owner == "visual-semantic-compiler":
        base.update({"representation_class": "narrative" if fn == "CHRONOLOGY" else "structural",
                     "representation_type": vsc_type(fn),
                     "desired_outcome_pt_br": beat.get("viewer_state_after_pt_br"),
                     "instruction": "Preserve evidence strength and provenance; do not strengthen causal topology."})
    elif owner == "media-use":
        base.update({"media_role": "evidence" if fn == "EVIDENCE" else "atmosphere",
                     "authentic_evidence_preferred": True,
                     "synthetic_substitution_default": "deny_for_evidence",
                     "instruction": "Resolve or prepare media without changing the factual claim carried by the beat."})
    elif owner == "motion-graphics":
        base.update({"category_hint": motion_hint(fn, (beat.get("visual") or {}).get("representation_intent")),
                     "target_duration_seconds": beat.get("target_duration_seconds"),
                     "instruction": "Animate the approved semantic/media result; motion must serve comprehension."})
    return base

def compile_packets(plan_path, ledger_path, out_dir):
    plan_path, ledger_path, out_dir = Path(plan_path), Path(ledger_path), Path(out_dir)
    receipt = import_validator().validate(plan_path, ledger_path)
    if receipt.get("status") != "PASSED":
        return None, [issue("plan_validation_failed", "$", "explainer plan must pass validate_plan.py before W4 compilation")]
    plan, ledger = load(plan_path), load(ledger_path)
    psha, lsha = sha(plan_path), sha(ledger_path)
    claims = {c.get("claim_id"): c for c in ledger.get("claims", []) if c.get("claim_id")}
    errors=[]
    for i, beat in enumerate(plan.get("beats") or []):
        fn=beat.get("explanation_function"); route=ROUTES.get(fn)
        pref=(beat.get("visual") or {}).get("preferred_owner")
        if not route:
            errors.append(issue("route_missing", f"beats[{i}].explanation_function", f"no canonical route for {fn}")); continue
        if pref and pref not in KNOWN_OWNERS:
            errors.append(issue("preferred_owner_unknown", f"beats[{i}].visual.preferred_owner", f"unknown owner {pref}"))
        elif pref and pref not in route:
            errors.append(issue("preferred_owner_incompatible", f"beats[{i}].visual.preferred_owner", f"{pref} is incompatible with {fn}; canonical chain is {route}"))
    if errors: return None, errors

    packets=[]; beat_routes=[]
    direction_id="PKT-PROJECT-DIRECTION"
    direction={
        "schema":"editorial-explainer-capability-packet/v1", "packet_id":direction_id,
        "owner":"motion-studio", "stage":"creative_direction", "scope":"project",
        "beat_id":None, "beat_order":None, "plan_sha256":psha, "evidence_ledger_sha256":lsha,
        "claim_refs": sorted({cid for b in plan.get("beats",[]) for cid in (b.get("claim_refs") or [])}),
        "qualifier_acknowledgements": {}, "depends_on":[],
        "payload":{"subject":plan.get("subject"), "language":plan.get("language"), "thesis":plan.get("thesis"),
                   "viewer_arc":[{"beat_id":b.get("beat_id"),"before_pt_br":b.get("viewer_state_before_pt_br"),"after_pt_br":b.get("viewer_state_after_pt_br")} for b in plan.get("beats",[])],
                   "instruction":"Define art direction, frame system, motion system, audio direction, and QA bar without altering claims or qualifiers."},
        "guardrails":["preserve_claim_refs","preserve_required_qualifiers","do_not_invent_facts","do_not_strengthen_causality","audience_text_pt_br"]
    }
    packets.append(direction)

    terminal_ids=[]
    for beat in sorted(plan.get("beats") or [], key=lambda b:b.get("order",0)):
        fn=beat.get("explanation_function"); chain=ROUTES[fn]
        claim_ctx=[claim_snapshot(claims[cid]) for cid in beat.get("claim_refs",[]) if cid in claims]
        ids=[]; previous=[]
        for idx, owner in enumerate(chain,1):
            pid=f"PKT-{slug(beat.get('beat_id'))}-{idx}-{slug(owner)}"
            deps=list(previous)
            if owner=="motion-graphics" and direction_id not in deps: deps.append(direction_id)
            packet={
                "schema":"editorial-explainer-capability-packet/v1", "packet_id":pid,
                "owner":owner, "stage":STAGES[owner], "scope":"beat",
                "beat_id":beat.get("beat_id"), "beat_order":beat.get("order"),
                "plan_sha256":psha, "evidence_ledger_sha256":lsha,
                "claim_refs":list(beat.get("claim_refs") or []),
                "qualifier_acknowledgements":beat.get("qualifier_acknowledgements") or {},
                "depends_on":deps,
                "payload":payload_for(owner, beat, claim_ctx, previous),
                "guardrails":["preserve_claim_refs","preserve_required_qualifiers","do_not_invent_facts","do_not_strengthen_causality","audience_text_pt_br","downstream_owner_controls_implementation"]
            }
            packets.append(packet); ids.append(pid); previous=[pid]
        terminal=ids[-1]; terminal_ids.append(terminal)
        beat_routes.append({"beat_id":beat.get("beat_id"),"packet_ids":ids,"terminal_packet_id":terminal})

    assembly_id="PKT-PROJECT-ASSEMBLY"
    assembly={
        "schema":"editorial-explainer-capability-packet/v1", "packet_id":assembly_id,
        "owner":"general-video", "stage":"sequence_assembly", "scope":"project",
        "beat_id":None, "beat_order":None, "plan_sha256":psha, "evidence_ledger_sha256":lsha,
        "claim_refs":direction["claim_refs"], "qualifier_acknowledgements":{},
        "depends_on":[direction_id]+terminal_ids,
        "payload":{"subject":plan.get("subject"), "language":"pt-BR", "thesis":plan.get("thesis"),
                   "ordered_beats":[{"beat_id":b.get("beat_id"),"order":b.get("order"),"narration_pt_br":b.get("narration_pt_br"),"target_duration_seconds":b.get("target_duration_seconds")} for b in sorted(plan.get("beats",[]), key=lambda x:x.get("order",0))],
                   "audio_requirements":{"narration_language":"pt-BR","voiceover":True,"captions":True},
                   "instruction":"Assemble the approved beat outputs into a narrated multi-scene composition; defer media/audio/render details to canonical owners and preserve all upstream gates."},
        "guardrails":["preserve_claim_refs","preserve_required_qualifiers","do_not_invent_facts","do_not_strengthen_causality","render_only_after_owner_approval_gate"]
    }
    packets.append(assembly)

    out_dir.mkdir(parents=True,exist_ok=True); packet_dir=out_dir/'packets'; packet_dir.mkdir(exist_ok=True)
    entries=[]
    for packet in packets:
        rel=f"packets/{packet['packet_id']}.json"; target=out_dir/rel
        target.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        entries.append({"packet_id":packet["packet_id"],"owner":packet["owner"],"stage":packet["stage"],"scope":packet["scope"],"path":rel,"depends_on":packet["depends_on"]})
    manifest={
        "schema":"editorial-explainer-capability-manifest/v1", "subject":plan.get("subject"), "language":"pt-BR",
        "plan_sha256":psha, "evidence_ledger_sha256":lsha,
        "project_direction_packet_id":direction_id, "sequence_assembly_packet_id":assembly_id,
        "packets":entries, "beat_routes":beat_routes,
        "execution_status":"READY_FOR_OWNER_AVAILABILITY_CHECK"
    }
    mp=out_dir/'capability-manifest.json'; mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return mp, []

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('plan'); ap.add_argument('ledger'); ap.add_argument('out_dir'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    try: mp, errors=compile_packets(a.plan,a.ledger,a.out_dir)
    except Exception as e: mp, errors=None,[issue("compiler_exception","$",str(e))]
    result={"schema":"editorial-explainer-capability-compile/v1","status":"PASSED" if not errors else "FAILED","manifest":str(mp) if mp else None,"errors":errors}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not errors else 1
if __name__=='__main__': sys.exit(main())
