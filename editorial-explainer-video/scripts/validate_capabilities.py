#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path

ALLOWED_STAGE={
 "data-viz-selector":"visual_spec","visual-semantic-compiler":"semantic_visual",
 "media-use":"media_resolution","motion-graphics":"motion_unit",
 "motion-studio":"creative_direction","general-video":"sequence_assembly"
}

def issue(code,path,message): return {"code":code,"path":path,"message":message}
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def normobj(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def validate(manifest_path, plan_path, ledger_path):
    errors=[]; warnings=[]
    manifest_path, plan_path, ledger_path=Path(manifest_path),Path(plan_path),Path(ledger_path)
    manifest, plan, ledger=load(manifest_path),load(plan_path),load(ledger_path)
    psha,lsha=sha(plan_path),sha(ledger_path)
    if manifest.get("schema")!="editorial-explainer-capability-manifest/v1": errors.append(issue("manifest_schema_invalid","schema","expected editorial-explainer-capability-manifest/v1"))
    if manifest.get("plan_sha256")!=psha: errors.append(issue("plan_hash_mismatch","plan_sha256","manifest is not bound to exact plan bytes"))
    if manifest.get("evidence_ledger_sha256")!=lsha: errors.append(issue("ledger_hash_mismatch","evidence_ledger_sha256","manifest is not bound to exact ledger bytes"))
    base=manifest_path.parent.resolve(); packets={}; entries={}
    for i,e in enumerate(manifest.get("packets") or []):
        pid=e.get("packet_id"); rel=e.get("path")
        if not pid or pid in entries: errors.append(issue("packet_id_invalid",f"packets[{i}].packet_id","packet ids must be non-empty and unique")); continue
        entries[pid]=e
        try:
            pp=(base/rel).resolve()
            if base not in pp.parents: raise ValueError("packet path escapes manifest directory")
            pkt=load(pp); packets[pid]=pkt
        except Exception as ex: errors.append(issue("packet_read_failed",f"packets[{i}].path",str(ex)))
    for pid,pkt in packets.items():
        owner=pkt.get("owner"); stage=pkt.get("stage")
        if owner not in ALLOWED_STAGE: errors.append(issue("owner_unknown",f"packet:{pid}.owner",f"unknown owner {owner}"))
        elif ALLOWED_STAGE[owner]!=stage: errors.append(issue("owner_stage_mismatch",f"packet:{pid}.stage",f"{owner} requires {ALLOWED_STAGE[owner]}"))
        if pkt.get("plan_sha256")!=psha: errors.append(issue("packet_plan_hash_mismatch",f"packet:{pid}.plan_sha256","packet plan hash drift"))
        if pkt.get("evidence_ledger_sha256")!=lsha: errors.append(issue("packet_ledger_hash_mismatch",f"packet:{pid}.evidence_ledger_sha256","packet ledger hash drift"))
        for dep in pkt.get("depends_on") or []:
            if dep not in entries: errors.append(issue("packet_dependency_missing",f"packet:{pid}.depends_on",f"missing dependency {dep}"))
    # cycle detection
    graph={pid:list((packets.get(pid) or {}).get("depends_on") or []) for pid in entries}
    visiting=set(); done=set()
    def dfs(n):
        if n in visiting: return False
        if n in done: return True
        visiting.add(n)
        for d in graph.get(n,[]):
            if d in graph and not dfs(d): return False
        visiting.remove(n); done.add(n); return True
    for pid in graph:
        if not dfs(pid): errors.append(issue("dependency_cycle","packets",f"dependency cycle includes {pid}")); break
    beats={b.get("beat_id"):b for b in plan.get("beats") or [] if b.get("beat_id")}
    route_map={r.get("beat_id"):r for r in manifest.get("beat_routes") or [] if r.get("beat_id")}
    if set(route_map)!=set(beats): errors.append(issue("beat_route_coverage","beat_routes",f"expected beats {sorted(beats)} got {sorted(route_map)}"))
    for bid,beat in beats.items():
        route=route_map.get(bid) or {}; ids=route.get("packet_ids") or []
        if not ids: continue
        if route.get("terminal_packet_id")!=ids[-1]: errors.append(issue("terminal_packet_invalid",f"beat_routes.{bid}","terminal packet must be last in chain"))
        for pid in ids:
            pkt=packets.get(pid)
            if not pkt: continue
            if pkt.get("scope")!="beat" or pkt.get("beat_id")!=bid: errors.append(issue("packet_beat_binding_invalid",f"packet:{pid}",f"packet must be beat-scoped to {bid}"))
            if list(pkt.get("claim_refs") or [])!=list(beat.get("claim_refs") or []): errors.append(issue("packet_claim_drift",f"packet:{pid}.claim_refs","claim refs changed during handoff"))
            if normobj(pkt.get("qualifier_acknowledgements") or {})!=normobj(beat.get("qualifier_acknowledgements") or {}): errors.append(issue("packet_qualifier_drift",f"packet:{pid}.qualifier_acknowledgements","required qualifiers changed during handoff"))
            pay=pkt.get("payload") or {}
            for field in ["question_pt_br","narration_pt_br","viewer_state_before_pt_br","viewer_state_after_pt_br","closure_test_pt_br"]:
                if pay.get(field)!=beat.get(field): errors.append(issue("packet_semantic_drift",f"packet:{pid}.payload.{field}",f"{field} changed during handoff"))
    direction=manifest.get("project_direction_packet_id"); assembly=manifest.get("sequence_assembly_packet_id")
    if (packets.get(direction) or {}).get("owner")!="motion-studio": errors.append(issue("direction_owner_invalid","project_direction_packet_id","project direction must be owned by motion-studio"))
    ap=packets.get(assembly) or {}
    if ap.get("owner")!="general-video": errors.append(issue("assembly_owner_invalid","sequence_assembly_packet_id","sequence assembly must be owned by general-video"))
    required={direction}|{r.get("terminal_packet_id") for r in route_map.values() if r.get("terminal_packet_id")}
    missing=sorted(required-set(ap.get("depends_on") or []))
    if missing: errors.append(issue("assembly_dependency_incomplete",f"packet:{assembly}.depends_on",f"missing {missing}"))
    for pid,pkt in packets.items():
        if pkt.get("owner")=="motion-graphics" and direction not in (pkt.get("depends_on") or []):
            errors.append(issue("motion_without_direction",f"packet:{pid}.depends_on","motion packet must depend on motion-studio direction"))
    return {"schema":"editorial-explainer-capability-validation/v1","status":"PASSED" if not errors else "FAILED","manifest_sha256":sha(manifest_path),"plan_sha256":psha,"evidence_ledger_sha256":lsha,"counts":{"packets":len(packets),"beats":len(beats)},"errors":errors,"warnings":warnings,"owner_execution_review":"pending"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('manifest'); ap.add_argument('plan'); ap.add_argument('ledger'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    try:r=validate(a.manifest,a.plan,a.ledger)
    except Exception as e:r={"schema":"editorial-explainer-capability-validation/v1","status":"FAILED","errors":[issue("validator_exception","$",str(e))],"warnings":[],"owner_execution_review":"pending"}
    print(json.dumps(r,ensure_ascii=False,indent=2)); return 0 if r.get("status")=="PASSED" else 1
if __name__=='__main__': sys.exit(main())
