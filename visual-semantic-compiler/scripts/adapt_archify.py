#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
TYPE_MAP={'actor':'external','storage':'database','component':'backend','process':'backend','stage':'backend','data':'database','outcome':'backend','decision':'backend','state':'backend','concept':'backend','evidence':'external','claim':'external','other':'backend'}
ALLOWED={'frontend','backend','database','cloud','security','messagebus','external'}
def adapt(ir):
    if ir.get('representation',{}).get('type')!='architecture': raise ValueError('Archify adapter v1 supports architecture IR only')
    comps=[]
    for e in ir.get('entities',[]):
        t=TYPE_MAP.get(e.get('kind'))
        if t not in ALLOWED: raise ValueError(f"cannot map entity kind {e.get('kind')!r} to Archify architecture")
        comps.append({'id':e['id'],'type':t,'label':e['label']})
    conns=[]
    for r in ir.get('relationships',[]):
        x={'id':r['id'],'from':r['from'],'to':r['to'],'label':r.get('label') or r['semantic'],'route':'auto'}
        if r.get('kind') in {'return'}: x['variant']='dashed'
        conns.append(x)
    locale='en' if ir.get('intent',{}).get('language','').lower().startswith('en') else None
    meta={'title':ir['representation']['primary_question'],'quality_profile':'showcase','visual_preset':'editorial'}
    if locale:meta['locale']=locale
    return {'schema_version':1,'diagram_type':'architecture','meta':meta,'layout':{'mode':'grid','cols':max(1,min(6,len(comps)))},'components':comps,'connections':conns}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('ir');ap.add_argument('output');ap.add_argument('--json',action='store_true');a=ap.parse_args()
    try:
        raw=Path(a.ir).read_bytes();ir=json.loads(raw);candidate=adapt(ir);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);b=(json.dumps(candidate,ensure_ascii=False,indent=2)+'\n').encode();out.write_bytes(b)
        r={'schema_version':'visual-archify-adapter-receipt/v1','status':'success','adapter':'archify/architecture/v1','semantic_ir_sha256':hashlib.sha256(raw).hexdigest(),'candidate_sha256':hashlib.sha256(b).hexdigest(),'output':str(out)};print(json.dumps(r,ensure_ascii=False,indent=None if a.json else 2));return 0
    except Exception as ex:
        print(json.dumps({'schema_version':'visual-archify-adapter-receipt/v1','status':'error','error':str(ex)},ensure_ascii=False));return 1
if __name__=='__main__':sys.exit(main())
