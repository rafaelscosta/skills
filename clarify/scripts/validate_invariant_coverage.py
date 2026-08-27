#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

SCHEMA='clarify-invariant-coverage/v1'
ALLOWED={'represented','text-only','omitted-with-reason','blocked'}

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def validate(coverage, ir=None, coverage_bytes=None, ir_bytes=None):
    errors=[]; warnings=[]
    def err(code,path,msg): errors.append({'code':code,'path':path,'message':msg})
    def warn(code,path,msg): warnings.append({'code':code,'path':path,'message':msg})

    if not isinstance(coverage,dict):
        return {'schema_version':'clarify-invariant-coverage-receipt/v1','status':'invalid','errors':[{'code':'shape','path':'$','message':'coverage must be object'}],'warnings':[]}
    if coverage.get('schema_version')!=SCHEMA: err('schema-version','$.schema_version',f'must equal {SCHEMA}')
    invs=coverage.get('invariants')
    entries=coverage.get('coverage')
    if not isinstance(invs,list) or not invs: err('invariants','$.invariants','must be a non-empty array'); invs=[]
    if not isinstance(entries,list): err('coverage','$.coverage','must be an array'); entries=[]

    inv_by={}
    for i,x in enumerate(invs):
        p=f'$.invariants[{i}]'
        if not isinstance(x,dict): err('invariant-shape',p,'must be object'); continue
        iid=x.get('id')
        if not isinstance(iid,str) or not iid.strip(): err('invariant-id',p+'.id','non-empty id required'); continue
        if iid in inv_by: err('duplicate-invariant',p+'.id',f'duplicate invariant {iid}')
        inv_by[iid]=x
        if not isinstance(x.get('statement'),str) or not x['statement'].strip(): err('invariant-statement',p+'.statement','non-empty statement required')
        if x.get('visual_relevant') not in {True,False}: err('visual-relevant',p+'.visual_relevant','must be boolean')

    seen={}
    ir_ids=set(); text_equiv=''
    if ir is not None:
        if not isinstance(ir,dict): err('ir-shape','ir','IR must be object')
        else:
            for coll in ('entities','relationships','narrative_beats'):
                for item in ir.get(coll,[]) if isinstance(ir.get(coll,[]),list) else []:
                    if isinstance(item,dict) and isinstance(item.get('id'),str): ir_ids.add(item['id'])
            text_equiv=str(ir.get('text_equivalent',''))

    for i,x in enumerate(entries):
        p=f'$.coverage[{i}]'
        if not isinstance(x,dict): err('coverage-entry-shape',p,'must be object'); continue
        iid=x.get('invariant_id')
        if iid not in inv_by: err('unknown-invariant',p+'.invariant_id',f'unknown invariant {iid!r}'); continue
        if iid in seen: err('duplicate-coverage',p+'.invariant_id',f'invariant {iid} covered more than once')
        seen[iid]=x
        status=x.get('status')
        if status not in ALLOWED: err('coverage-status',p+'.status',f'must be one of {sorted(ALLOWED)}'); continue
        refs=x.get('ir_refs',[])
        if refs is None: refs=[]
        if not isinstance(refs,list): err('ir-refs',p+'.ir_refs','must be array'); refs=[]
        reason=str(x.get('reason','')).strip()
        if status=='represented':
            if not refs: err('represented-without-ref',p+'.ir_refs','represented requires at least one IR ref')
            if ir is not None:
                for j,r in enumerate(refs):
                    if r not in ir_ids: err('missing-ir-ref',f'{p}.ir_refs[{j}]',f'IR id {r!r} not found')
        elif status=='text-only':
            if refs: err('text-only-with-ref',p+'.ir_refs','text-only must not claim IR refs')
            if not reason: err('text-only-reason',p+'.reason','text-only requires reason')
            if ir is not None and not text_equiv.strip(): err('text-equivalent-missing','ir.text_equivalent','text-only requires usable text equivalent')
        elif status=='omitted-with-reason':
            if refs: err('omitted-with-ref',p+'.ir_refs','omitted invariant must not claim IR refs')
            if not reason: err('omission-reason',p+'.reason','omitted-with-reason requires reason')
            if inv_by[iid].get('visual_relevant') is True:
                warn('visual-relevant-omitted',p,f'{iid} is visual-relevant but omitted with reason')
        elif status=='blocked':
            if refs: err('blocked-with-ref',p+'.ir_refs','blocked invariant must not claim IR refs')
            if not reason: err('blocked-reason',p+'.reason','blocked requires reason')

    for iid,x in inv_by.items():
        if x.get('visual_relevant') is True and iid not in seen:
            err('unaccounted-invariant','$.coverage',f'visual-relevant invariant {iid} is not accounted for')

    blocked=[iid for iid,x in seen.items() if x.get('status')=='blocked']
    if blocked: err('handoff-blocked','$.coverage',f'blocked invariants prevent trusted visual handoff: {blocked}')

    declared_ir=coverage.get('visual_ir_sha256')
    if declared_ir is not None:
        if ir_bytes is None: err('ir-binding-unverifiable','$.visual_ir_sha256','IR bytes required to verify declared digest')
        elif declared_ir != sha(ir_bytes): err('ir-binding','$.visual_ir_sha256','digest does not match IR bytes')

    receipt={
        'schema_version':'clarify-invariant-coverage-receipt/v1',
        'status':'invalid' if errors else 'valid',
        'coverage_sha256': sha(coverage_bytes if coverage_bytes is not None else json.dumps(coverage,sort_keys=True,separators=(',',':')).encode()),
        'visual_ir_sha256': sha(ir_bytes) if ir_bytes is not None else None,
        'metrics':{
            'invariants':len(inv_by),
            'visual_relevant':sum(1 for x in inv_by.values() if x.get('visual_relevant') is True),
            'represented':sum(1 for x in seen.values() if x.get('status')=='represented'),
            'text_only':sum(1 for x in seen.values() if x.get('status')=='text-only'),
            'omitted':sum(1 for x in seen.values() if x.get('status')=='omitted-with-reason'),
            'blocked':len(blocked),
        },
        'errors':errors,
        'warnings':warnings,
    }
    return receipt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('coverage')
    ap.add_argument('--ir')
    ap.add_argument('--json',action='store_true')
    a=ap.parse_args()
    try:
        cp=Path(a.coverage); cb=cp.read_bytes(); coverage=json.loads(cb)
        ir=ib=None
        if a.ir:
            ip=Path(a.ir); ib=ip.read_bytes(); ir=json.loads(ib)
        r=validate(coverage,ir,cb,ib)
    except Exception as ex:
        r={'schema_version':'clarify-invariant-coverage-receipt/v1','status':'error','errors':[{'code':'read-error','path':'$','message':str(ex)}],'warnings':[]}
        print(json.dumps(r,ensure_ascii=False) if a.json else json.dumps(r,ensure_ascii=False,indent=2)); return 2
    print(json.dumps(r,ensure_ascii=False) if a.json else json.dumps(r,ensure_ascii=False,indent=2))
    return 0 if r['status']=='valid' else 1

if __name__=='__main__': sys.exit(main())
