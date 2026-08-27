#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

SCHEMA='visual-layout/v1'

def sha(b): return hashlib.sha256(b).hexdigest()
def canonical_layout_sha(layout):
    if not isinstance(layout,dict): return sha(b'')
    body={k:v for k,v in layout.items() if k!='layout_sha256'}
    return sha(json.dumps(body,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def error(E,c,s,m,e=None):
    x={'code':c,'subject':s,'message':m}
    if e is not None:x['evidence']=e
    E.append(x)
def warning(W,c,s,m,e=None):
    x={'code':c,'subject':s,'message':m}
    if e is not None:x['evidence']=e
    W.append(x)
def rect_overlap(a,b,gap=0):
    return not (a['x']+a['width']+gap<=b['x'] or b['x']+b['width']+gap<=a['x'] or a['y']+a['height']+gap<=b['y'] or b['y']+b['height']+gap<=a['y'])
def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def between(a,b,c): return min(a,b)-1e-9<=c<=max(a,b)+1e-9
def seg_intersect(a,b,c,d):
    o1,o2,o3,o4=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
    if (o1>0 and o2<0 or o1<0 and o2>0) and (o3>0 and o4<0 or o3<0 and o4>0): return True
    for o,p,q,r in [(o1,a,b,c),(o2,a,b,d),(o3,c,d,a),(o4,c,d,b)]:
        if abs(o)<1e-9 and between(p[0],q[0],r[0]) and between(p[1],q[1],r[1]): return True
    return False
def point_inside_rect(p,r,strict=True):
    if strict:return r['x']<p[0]<r['x']+r['width'] and r['y']<p[1]<r['y']+r['height']
    return r['x']<=p[0]<=r['x']+r['width'] and r['y']<=p[1]<=r['y']+r['height']
def segment_hits_rect(a,b,r):
    if point_inside_rect(a,r) or point_inside_rect(b,r): return True
    cs=[(r['x'],r['y']),(r['x']+r['width'],r['y']),(r['x']+r['width'],r['y']+r['height']),(r['x'],r['y']+r['height'])]
    return any(seg_intersect(a,b,cs[i],cs[(i+1)%4]) for i in range(4))
def explicit_outer_back_route(edge,nodes,direction):
    pts=edge.get('points',[])
    if len(pts)<4 or not nodes:return False
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    left=min(n['x'] for n in nodes); right=max(n['x']+n['width'] for n in nodes)
    top=min(n['y'] for n in nodes); bottom=max(n['y']+n['height'] for n in nodes)
    gutter=24
    if direction=='top-to-bottom': return max(xs)>=right+gutter or min(xs)<=left-gutter
    if direction=='left-to-right': return max(ys)>=bottom+gutter or min(ys)<=top-gutter
    return False

def validate(layout):
    E=[];W=[];checks={k:'pending' for k in ['shape','containment','node_separation','edge_node_clearance','edge_crossings','label_clearance','reading_direction','artifact_readiness']}
    if not isinstance(layout,dict): error(E,'shape','$','layout must be object'); return receipt(layout,E,W,checks)
    if layout.get('schema_version')!=SCHEMA:error(E,'schema-version','schema_version',f'must equal {SCHEMA}')
    declared=layout.get('layout_sha256'); actual=canonical_layout_sha(layout)
    if declared!=actual:error(E,'layout-digest','layout_sha256','declared layout digest does not match canonical layout bytes',{'declared':declared,'actual':actual})
    vp=layout.get('viewport',{}); nodes=layout.get('nodes',[]); edges=layout.get('edges',[])
    if not all(isinstance(vp.get(k),(int,float)) and vp[k]>0 for k in ['width','height']): error(E,'viewport','viewport','invalid width/height')
    ids=set()
    for n in nodes:
        if n.get('id') in ids:error(E,'duplicate-node',n.get('id'),'duplicate node id')
        ids.add(n.get('id'))
        for k in ['x','y','width','height']:
            if not isinstance(n.get(k),(int,float)):error(E,'node-geometry',n.get('id'),f'{k} must be numeric')
        if all(isinstance(n.get(k),(int,float)) for k in ['x','y','width','height']) and vp:
            if n['x']<0 or n['y']<0 or n['x']+n['width']>vp.get('width',0) or n['y']+n['height']>vp.get('height',0): error(E,'node-outside-viewport',n['id'],'node exceeds viewport')
    for i,a in enumerate(nodes):
        for b in nodes[i+1:]:
            if rect_overlap(a,b,12): error(E,'node-overlap',f"{a['id']}|{b['id']}",'nodes overlap or violate 12px clear gap')
    nmap={n['id']:n for n in nodes}
    segments=[]; label_boxes=[]
    for e in edges:
        if e.get('from') not in nmap or e.get('to') not in nmap:error(E,'edge-endpoint',e.get('id'),'edge endpoint missing')
        pts=e.get('points',[])
        if not isinstance(pts,list) or len(pts)<2:error(E,'edge-points',e.get('id'),'edge requires >=2 points');continue
        for a,b in zip(pts,pts[1:]):segments.append((e,a,b))
        lb=e.get('label_box')
        if lb:
            if lb['x']<0 or lb['y']<0 or lb['x']+lb['width']>vp.get('width',0) or lb['y']+lb['height']>vp.get('height',0): error(E,'label-outside-viewport',e['id'],'label exceeds viewport')
            label_boxes.append((e,lb))
        for n in nodes:
            if n['id'] in {e.get('from'),e.get('to')}:continue
            if any(segment_hits_rect(a,b,n) for a,b in zip(pts,pts[1:])): error(E,'edge-through-node',e['id'],f"edge crosses unrelated node {n['id']}")
    crossings=[]
    for i,(e1,a,b) in enumerate(segments):
        for e2,c,d in segments[i+1:]:
            if e1['id']==e2['id'] or {e1.get('from'),e1.get('to')} & {e2.get('from'),e2.get('to')}:continue
            if seg_intersect(a,b,c,d):crossings.append((e1['id'],e2['id']))
    if crossings:
        if layout.get('constraints',{}).get('target_zero_crossings'): error(E,'edge-crossing','edges',f'{len(crossings)} unrelated edge crossings',crossings[:8])
        else: warning(W,'edge-crossing','edges',f'{len(crossings)} unrelated edge crossings',crossings[:8])
    for i,(e,lb) in enumerate(label_boxes):
        for n in nodes:
            if rect_overlap(lb,n,4):error(E,'label-node-collision',e['id'],f"label overlaps node {n['id']}")
        for e2,lb2 in label_boxes[i+1:]:
            if rect_overlap(lb,lb2,4):error(E,'label-label-collision',f"{e['id']}|{e2['id']}",'relationship labels overlap')
    direction=layout.get('reading_direction'); typ=layout.get('representation_type')
    if typ not in {'state','sequence','structural-comparison'}:
        for e in edges:
            if e.get('kind') in {'return','feedback'}:continue
            a=nmap.get(e.get('from'));b=nmap.get(e.get('to'))
            if not a or not b:continue
            ac=(a['x']+a['width']/2,a['y']+a['height']/2);bc=(b['x']+b['width']/2,b['y']+b['height']/2)
            backward=(direction=='left-to-right' and bc[0]+4<ac[0]) or (direction=='top-to-bottom' and bc[1]+4<ac[1])
            if backward and not explicit_outer_back_route(e,nodes,direction):
                message='primary edge moves right-to-left' if direction=='left-to-right' else 'primary edge moves bottom-to-top'
                error(E,'reading-direction',e['id'],message)
    for k in checks:checks[k]='failed' if E else 'passed'
    return receipt(layout,E,W,checks)
def receipt(layout,E,W,checks):
    digest=canonical_layout_sha(layout)
    return {'schema_version':'visual-layout-receipt/v1','status':'invalid' if E else 'valid','layout_sha256':digest,'checks':checks,'errors':E,'warnings':W,'metrics':{'nodes':len(layout.get('nodes',[])) if isinstance(layout,dict) else 0,'edges':len(layout.get('edges',[])) if isinstance(layout,dict) else 0}}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('layout');ap.add_argument('--json',action='store_true');a=ap.parse_args()
    try:data=json.loads(Path(a.layout).read_text())
    except Exception as ex:
        r={'schema_version':'visual-layout-receipt/v1','status':'error','error':str(ex)};print(json.dumps(r) if a.json else str(ex));return 2
    r=validate(data); print(json.dumps(r,ensure_ascii=False,indent=None if a.json else 2));return 0 if r['status']=='valid' else 1
if __name__=='__main__':sys.exit(main())
