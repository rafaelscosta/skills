#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

SCHEMA_VERSION='visual-semantic-ir/v1'
ID_RE=re.compile(r'^[A-Za-z][A-Za-z0-9_-]*$')
REP_CLASSES={'narrative-visual','structural-diagram','mixed'}
NARRATIVE={'story-strip','before-after','storyboard','timeline'}
STRUCTURAL={'flow','state','architecture','sequence','dataflow','hierarchy','causal','structural-comparison','decision-tree','decision-table','concept-map','argument-map','swimlane','bpmn','sipoc','service-blueprint','c4','event-storming','statistical-chart','other'}
ENTITY_KINDS={'actor','component','state','decision','data','concept','stage','outcome','storage','process','evidence','claim','other'}
REL_KINDS={'flow','transition','call','return','data','dependency','containment','causation','comparison','handoff','reads','writes','supports','attacks','feedback','other'}
GROUP_KINDS={'boundary','lane','layer','comparison-side','phase','other'}
PROV={'explicit','inferred','general-knowledge','unknown'}
CONF={'high','medium','low','unknown'}
DIRECTIONS={'left-to-right','top-to-bottom','other'}
TOP={'schema_version','source_skill','intent','representation','entities','relationships','narrative_beats','groups','views','constraints','omissions','text_equivalent'}

def s(v): return isinstance(v,str) and bool(v.strip())
def err(E,c,p,m): E.append({'code':c,'path':p,'message':m})
def warn(W,c,p,m): W.append({'code':c,'path':p,'message':m})
def obj(v,p,E):
    if not isinstance(v,dict): err(E,'type',p,'must be an object'); return {}
    return v
def arr(v,p,E):
    if not isinstance(v,list): err(E,'type',p,'must be an array'); return []
    return v
def check_id(v,p,E):
    if not isinstance(v,str) or not ID_RE.match(v): err(E,'id',p,'invalid identifier'); return None
    return v

def provenance(v,p,E,W):
    if v is None: return
    x=obj(v,p,E)
    extra=set(x)-{'status','source_ref','locator','confidence','note'}
    if extra: err(E,'unknown-field',p,f'unknown fields: {sorted(extra)}')
    st=x.get('status')
    if st not in PROV: err(E,'provenance-status',p+'.status',f'must be one of {sorted(PROV)}')
    cf=x.get('confidence')
    if cf is not None and cf not in CONF: err(E,'provenance-confidence',p+'.confidence',f'must be one of {sorted(CONF)}')
    if st=='explicit' and not s(x.get('source_ref')): warn(W,'explicit-without-source',p,'explicit provenance should name source_ref when evidence exists')
    if st=='inferred' and cf is None: warn(W,'inference-confidence',p,'inferred provenance should record confidence')

def cycle(nodes,edges):
    g={n:[] for n in nodes}
    for a,b in edges:
        if a in g: g[a].append(b)
    visiting=set(); visited=set()
    def dfs(n):
        if n in visiting: return True
        if n in visited: return False
        visiting.add(n)
        for x in g.get(n,[]):
            if dfs(x): return True
        visiting.remove(n); visited.add(n); return False
    return any(dfs(n) for n in nodes if n not in visited)

def validate(data):
    E=[]; W=[]
    checks={k:'pending' for k in ['schema_shape','unique_ids','relationship_integrity','representation_contract','type_contract','provenance_integrity','pedagogical_contract']}
    checks['layout_geometry']='deferred'
    root=obj(data,'$',E)
    if not root: return {'status':'invalid','schema_version':SCHEMA_VERSION,'checks':checks,'errors':E,'warnings':W}
    extra=set(root)-TOP
    if extra: err(E,'unknown-field','$',f'unknown top-level fields: {sorted(extra)}')
    if root.get('schema_version')!=SCHEMA_VERSION: err(E,'schema-version','$.schema_version',f'must equal {SCHEMA_VERSION}')
    if not s(root.get('source_skill')): err(E,'source-skill','$.source_skill','must be non-empty')

    intent=obj(root.get('intent'),'$.intent',E)
    extra=set(intent)-{'question','audience','depth','language','desired_outcome'}
    if extra: err(E,'unknown-field','$.intent',f'unknown fields: {sorted(extra)}')
    for f in ['question','audience','language']:
        if not s(intent.get(f)): err(E,'intent-field',f'$.intent.{f}','must be non-empty')

    rep=obj(root.get('representation'),'$.representation',E)
    extra=set(rep)-{'class','type','reading_direction','primary_question'}
    if extra: err(E,'unknown-field','$.representation',f'unknown fields: {sorted(extra)}')
    rc=rep.get('class'); rt=rep.get('type')
    if rc not in REP_CLASSES: err(E,'representation-class','$.representation.class',f'must be one of {sorted(REP_CLASSES)}')
    if rt not in NARRATIVE|STRUCTURAL|{'mixed'}: err(E,'representation-type','$.representation.type','unsupported representation type')
    if rep.get('reading_direction') not in DIRECTIONS: err(E,'reading-direction','$.representation.reading_direction',f'must be one of {sorted(DIRECTIONS)}')
    if not s(rep.get('primary_question')): err(E,'primary-question','$.representation.primary_question','must be non-empty')
    if rc=='narrative-visual' and rt not in NARRATIVE: err(E,'representation-fit','$.representation.type','narrative class requires narrative type')
    if rc=='structural-diagram' and rt not in STRUCTURAL: err(E,'representation-fit','$.representation.type','structural class requires structural type')
    if rc=='mixed' and rt!='mixed': err(E,'representation-fit','$.representation.type','mixed class requires type mixed')

    entities=arr(root.get('entities',[]),'$.entities',E); rels=arr(root.get('relationships',[]),'$.relationships',E)
    beats=arr(root.get('narrative_beats',[]),'$.narrative_beats',E); groups=arr(root.get('groups',[]),'$.groups',E); views=arr(root.get('views',[]),'$.views',E)
    omissions=arr(root.get('omissions',[]),'$.omissions',E)
    eids=set(); rids=set(); bids=set(); gids=set(); vids=set(); out={}; orders=[]

    for i,x0 in enumerate(entities):
        p=f'$.entities[{i}]'; x=obj(x0,p,E); extra=set(x)-{'id','label','kind','description','provenance'}
        if extra: err(E,'unknown-field',p,f'unknown fields: {sorted(extra)}')
        eid=check_id(x.get('id'),p+'.id',E)
        if eid:
            if eid in eids: err(E,'duplicate-id',p+'.id',f'duplicate {eid}')
            eids.add(eid)
        if not s(x.get('label')): err(E,'entity-label',p+'.label','must be a direct non-empty label')
        if x.get('kind') not in ENTITY_KINDS: err(E,'entity-kind',p+'.kind',f'must be one of {sorted(ENTITY_KINDS)}')
        provenance(x.get('provenance'),p+'.provenance',E,W)

    for i,x0 in enumerate(rels):
        p=f'$.relationships[{i}]'; x=obj(x0,p,E); extra=set(x)-{'id','from','to','kind','semantic','label','order','provenance'}
        if extra: err(E,'unknown-field',p,f'unknown fields: {sorted(extra)}')
        rid=check_id(x.get('id'),p+'.id',E)
        if rid:
            if rid in rids: err(E,'duplicate-id',p+'.id',f'duplicate {rid}')
            rids.add(rid)
        a=x.get('from'); b=x.get('to')
        if a not in eids: err(E,'missing-endpoint',p+'.from',f'unknown entity {a!r}')
        if b not in eids: err(E,'missing-endpoint',p+'.to',f'unknown entity {b!r}')
        if a in eids and b in eids: out.setdefault(a,[]).append(x)
        if x.get('kind') not in REL_KINDS: err(E,'relationship-kind',p+'.kind',f'must be one of {sorted(REL_KINDS)}')
        if not s(x.get('semantic')): err(E,'relationship-semantic',p+'.semantic','must name relationship meaning')
        if 'order' in x:
            if not isinstance(x['order'],int) or x['order']<=0: err(E,'relationship-order',p+'.order','must be positive integer')
            else: orders.append(x['order'])
        provenance(x.get('provenance'),p+'.provenance',E,W)

    for i,x0 in enumerate(beats):
        p=f'$.narrative_beats[{i}]'; x=obj(x0,p,E); extra=set(x)-{'id','title','action','actor','order','provenance'}
        if extra: err(E,'unknown-field',p,f'unknown fields: {sorted(extra)}')
        bid=check_id(x.get('id'),p+'.id',E)
        if bid:
            if bid in bids: err(E,'duplicate-id',p+'.id',f'duplicate {bid}')
            bids.add(bid)
        if not s(x.get('title')): err(E,'beat-title',p+'.title','must be non-empty')
        if not s(x.get('action')): err(E,'beat-action',p+'.action','must be non-empty')
        if not isinstance(x.get('order'),int) or x.get('order',0)<=0: err(E,'beat-order',p+'.order','must be positive integer')
        provenance(x.get('provenance'),p+'.provenance',E,W)

    for i,x0 in enumerate(groups):
        p=f'$.groups[{i}]'; x=obj(x0,p,E); extra=set(x)-{'id','label','kind','members'}
        if extra: err(E,'unknown-field',p,f'unknown fields: {sorted(extra)}')
        gid=check_id(x.get('id'),p+'.id',E)
        if gid:
            if gid in gids: err(E,'duplicate-id',p+'.id',f'duplicate {gid}')
            gids.add(gid)
        if not s(x.get('label')): err(E,'group-label',p+'.label','must be non-empty')
        if x.get('kind') not in GROUP_KINDS: err(E,'group-kind',p+'.kind',f'must be one of {sorted(GROUP_KINDS)}')
        for j,m in enumerate(arr(x.get('members'),p+'.members',E)):
            if m not in eids: err(E,'group-member',f'{p}.members[{j}]',f'unknown entity {m!r}')

    view_classes=set(); view_questions=set()
    for i,x0 in enumerate(views):
        p=f'$.views[{i}]'; x=obj(x0,p,E); extra=set(x)-{'id','class','type','question','reading_direction','entity_ids','relationship_ids','beat_ids'}
        if extra: err(E,'unknown-field',p,f'unknown fields: {sorted(extra)}')
        vid=check_id(x.get('id'),p+'.id',E)
        if vid:
            if vid in vids: err(E,'duplicate-id',p+'.id',f'duplicate {vid}')
            vids.add(vid)
        vc=x.get('class'); vt=x.get('type')
        if vc not in {'narrative-visual','structural-diagram'}: err(E,'view-class',p+'.class','must be narrative-visual or structural-diagram')
        else: view_classes.add(vc)
        if vc=='narrative-visual' and vt not in NARRATIVE: err(E,'view-type',p+'.type','invalid narrative type')
        if vc=='structural-diagram' and vt not in STRUCTURAL: err(E,'view-type',p+'.type','invalid structural type')
        q=x.get('question')
        if not s(q): err(E,'view-question',p+'.question','must be non-empty')
        else:
            qn=q.strip().lower()
            if qn in view_questions: err(E,'duplicate-view-question',p+'.question','views must answer distinct questions')
            view_questions.add(qn)
        if x.get('reading_direction') not in DIRECTIONS: err(E,'reading-direction',p+'.reading_direction','invalid direction')
        for f,known in [('entity_ids',eids),('relationship_ids',rids),('beat_ids',bids)]:
            for j,r in enumerate(arr(x.get(f,[]),p+'.'+f,E)):
                if r not in known: err(E,'view-reference',f'{p}.{f}[{j}]',f'unknown id {r!r}')

    c=obj(root.get('constraints',{}),'$.constraints',E); extra=set(c)-{'direct_labels','target_zero_crossings','max_primary_nodes','text_equivalent_required'}
    if extra: err(E,'unknown-field','$.constraints',f'unknown fields: {sorted(extra)}')
    for f in ['direct_labels','target_zero_crossings','text_equivalent_required']:
        if f in c and not isinstance(c[f],bool): err(E,'constraint-type','$.constraints.'+f,'must be boolean')
    if 'max_primary_nodes' in c:
        n=c['max_primary_nodes']
        if not isinstance(n,int) or n<=0: err(E,'constraint-type','$.constraints.max_primary_nodes','must be positive integer')
        elif len(entities)>n: warn(W,'node-budget','$.entities',f'{len(entities)} entities exceed max_primary_nodes={n}')
    for i,o in enumerate(omissions):
        if not s(o): err(E,'omission',f'$.omissions[{i}]','must be non-empty')
    if not s(root.get('text_equivalent')): err(E,'text-equivalent','$.text_equivalent','must provide usable text equivalent')

    if rc=='narrative-visual' and len(beats)<2: err(E,'narrative-contract','$.narrative_beats','requires at least two beats')
    if rc=='structural-diagram':
        if len(entities)<2: err(E,'structural-contract','$.entities','requires at least two entities')
        if len(rels)<1: err(E,'structural-contract','$.relationships','requires at least one relationship')
    if rc=='mixed':
        if len(views)<2: err(E,'mixed-contract','$.views','requires at least two views')
        if not {'narrative-visual','structural-diagram'}.issubset(view_classes): err(E,'mixed-contract','$.views','requires narrative and structural views')

    if rt=='flow':
        for src,rs in out.items():
            if len(rs)>1 and any(not s(r.get('label')) for r in rs): err(E,'flow-branch-label','$.relationships',f'branching from {src} requires labels')
    elif rt=='state':
        for i,x in enumerate(entities):
            if isinstance(x,dict) and x.get('kind')!='state': err(E,'state-entity',f'$.entities[{i}].kind','state diagram entities must be state')
        for i,x in enumerate(rels):
            if isinstance(x,dict) and x.get('kind')!='transition': err(E,'state-transition',f'$.relationships[{i}].kind','state relationships must be transition')
    elif rt=='sequence':
        if len(orders)!=len(rels) or len(set(orders))!=len(orders): err(E,'sequence-order','$.relationships','each sequence relationship needs a unique positive order')
    elif rt=='dataflow':
        for i,x in enumerate(rels):
            if isinstance(x,dict) and x.get('kind') not in {'data','reads','writes','flow'}: err(E,'dataflow-kind',f'$.relationships[{i}].kind','invalid dataflow relationship kind')
    elif rt=='hierarchy':
        hs=[]
        for i,x in enumerate(rels):
            if isinstance(x,dict):
                if x.get('kind') not in {'containment','dependency'}: err(E,'hierarchy-kind',f'$.relationships[{i}].kind','invalid hierarchy relationship kind')
                if x.get('from') in eids and x.get('to') in eids: hs.append((x['from'],x['to']))
        if cycle(eids,hs): err(E,'hierarchy-cycle','$.relationships','hierarchy cannot contain directed cycle')
    elif rt=='causal':
        for i,x in enumerate(rels):
            if isinstance(x,dict) and x.get('kind') not in {'causation','feedback'}: err(E,'causal-kind',f'$.relationships[{i}].kind','causal relationships must be causation or feedback')
    elif rt=='structural-comparison':
        if len([g for g in groups if isinstance(g,dict) and g.get('kind')=='comparison-side'])<2: err(E,'comparison-groups','$.groups','requires at least two comparison-side groups')

    shape_codes={'type','unknown-field','schema-version','source-skill','intent-field','representation-class','representation-type','reading-direction','entity-kind','relationship-kind','group-kind','constraint-type','omission'}
    checks['schema_shape']='fail' if any(x['code'] in shape_codes for x in E) else 'pass'
    checks['unique_ids']='fail' if any(x['code'] in {'id','duplicate-id'} for x in E) else 'pass'
    checks['relationship_integrity']='fail' if any(x['code'] in {'missing-endpoint','relationship-semantic','group-member','view-reference'} for x in E) else 'pass'
    checks['representation_contract']='fail' if any(x['code'] in {'representation-fit','narrative-contract','structural-contract','mixed-contract','view-class','view-type','view-question','duplicate-view-question'} for x in E) else 'pass'
    type_codes={'flow-branch-label','state-entity','state-transition','sequence-order','dataflow-kind','hierarchy-kind','hierarchy-cycle','causal-kind','comparison-groups'}
    checks['type_contract']='fail' if any(x['code'] in type_codes for x in E) else 'pass'
    checks['provenance_integrity']='fail' if any(x['code'].startswith('provenance-') for x in E) else 'pass'
    checks['pedagogical_contract']='fail' if any(x['code'] in {'primary-question','text-equivalent','entity-label','beat-title','beat-action'} for x in E) else 'pass'
    return {'status':'valid' if not E else 'invalid','schema_version':SCHEMA_VERSION,'checks':checks,'errors':E,'warnings':W}

def main(argv=None):
    ap=argparse.ArgumentParser(description='Validate Visual Semantic IR v1'); ap.add_argument('candidate'); ap.add_argument('--json',action='store_true'); a=ap.parse_args(argv)
    p=Path(a.candidate)
    try: raw=p.read_bytes()
    except OSError as ex: print(f'error: cannot read {p}: {ex}',file=sys.stderr); return 2
    try: data=json.loads(raw.decode('utf-8'))
    except Exception as ex:
        rec={'status':'invalid','schema_version':SCHEMA_VERSION,'candidate':str(p),'input_sha256':hashlib.sha256(raw).hexdigest(),'checks':{},'errors':[{'code':'json-parse','path':'$','message':str(ex)}],'warnings':[]}
        print(json.dumps(rec,ensure_ascii=False,separators=(',',':')) if a.json else json.dumps(rec,ensure_ascii=False,indent=2)); return 1
    rec=validate(data); rec['candidate']=str(p); rec['input_sha256']=hashlib.sha256(raw).hexdigest()
    print(json.dumps(rec,ensure_ascii=False,separators=(',',':')) if a.json else json.dumps(rec,ensure_ascii=False,indent=2)); return 0 if rec['status']=='valid' else 1
if __name__=='__main__': raise SystemExit(main())
