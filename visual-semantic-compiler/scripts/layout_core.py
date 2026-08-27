#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, math
from collections import defaultdict, deque

LAYOUT_SCHEMA='visual-layout/v1'
SUPPORTED={'architecture','flow','state','sequence','dataflow','hierarchy','causal','structural-comparison','story-strip','before-after','timeline'}
NODE_W=176; NODE_H=68; GAP_X=220; GAP_Y=70; PAD=54; LABEL_H=24

def sha256_json(data):
    return hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def text_width(text, minimum=42, maximum=320):
    return max(minimum,min(maximum,14+len(str(text))*7))

def wrap_label(text,max_chars=24):
    words=str(text).split(); lines=[]; cur=''
    for word in words:
        candidate=word if not cur else cur+' '+word
        if cur and len(candidate)>max_chars:
            lines.append(cur); cur=word
        else:
            cur=candidate
    if cur: lines.append(cur)
    return lines or ['']

def center(n): return (n['x']+n['width']/2,n['y']+n['height']/2)

def _active_edges(ir): return [r for r in ir['relationships'] if r.get('kind') not in {'return','feedback'}]

def _levels(ir):
    ids=[e['id'] for e in ir['entities']]; indeg={i:0 for i in ids}; out=defaultdict(list)
    for r in _active_edges(ir):
        a,b=r['from'],r['to']
        if a in indeg and b in indeg: out[a].append(b); indeg[b]+=1
    q=deque([i for i in ids if indeg[i]==0]); level={i:0 for i in q}; seen=[]
    while q:
        a=q.popleft(); seen.append(a)
        for b in out[a]:
            level[b]=max(level.get(b,0),level[a]+1); indeg[b]-=1
            if indeg[b]==0:q.append(b)
    if len(seen)!=len(ids):
        for idx,i in enumerate(ids): level.setdefault(i,idx)
    return level

def _generic_nodes(ir):
    direction=ir['representation']['reading_direction']; ents=ir['entities']; levels=_levels(ir); buckets=defaultdict(list)
    for e in ents:buckets[levels[e['id']]].append(e)
    nodes=[]; max_slots=max((len(v) for v in buckets.values()),default=1)
    if direction=='top-to-bottom':
        for lev in sorted(buckets):
            items=buckets[lev]
            for j,e in enumerate(items):
                x=PAD+(j+(max_slots-len(items))/2)*(NODE_W+GAP_X); y=PAD+lev*(NODE_H+GAP_Y)
                nodes.append({'id':e['id'],'label':e['label'],'kind':e['kind'],'x':round(x,2),'y':y,'width':NODE_W,'height':NODE_H})
    else:
        for lev in sorted(buckets):
            items=buckets[lev]
            for j,e in enumerate(items):
                x=PAD+lev*(NODE_W+GAP_X); y=PAD+(j+(max_slots-len(items))/2)*(NODE_H+GAP_Y)
                nodes.append({'id':e['id'],'label':e['label'],'kind':e['kind'],'x':x,'y':round(y,2),'width':NODE_W,'height':NODE_H})
    return nodes

def _flow_levels(ir):
    ids=[e['id'] for e in ir['entities']]
    outgoing=defaultdict(list); indeg={i:0 for i in ids}
    for r in ir['relationships']:
        if r['from'] in indeg and r['to'] in indeg:
            outgoing[r['from']].append(r); indeg[r['to']]+=1
    roots=[i for i in ids if indeg[i]==0] or ids[:1]
    level={}; order=[]; back=set(); q=deque()
    for root in roots:
        if root not in level:
            level[root]=0; q.append(root); order.append(root)
    while q:
        a=q.popleft()
        for rel in outgoing.get(a,[]):
            b=rel['to']
            if b not in level:
                level[b]=level[a]+1; q.append(b); order.append(b)
            elif level[b] <= level[a]:
                back.add(rel['id'])
    for eid in ids:
        if eid not in level:
            level[eid]=max(level.values(),default=-1)+1; order.append(eid)
    return level,{eid:i for i,eid in enumerate(order)},back

def _flow_nodes(ir):
    direction=ir['representation']['reading_direction']; level,rank,back=_flow_levels(ir)
    byid={e['id']:e for e in ir['entities']}; buckets=defaultdict(list)
    for eid,lev in level.items(): buckets[lev].append(eid)
    for lev in buckets: buckets[lev].sort(key=lambda eid:rank[eid])
    max_slots=max((len(v) for v in buckets.values()),default=1)
    max_lines=max((len(wrap_label(e['label'])) for e in ir['entities']),default=1)
    flow_w=max(NODE_W,220); flow_h=NODE_H+max(0,max_lines-1)*22
    step_x=flow_w+GAP_X; step_y=flow_h+GAP_Y; nodes=[]
    if direction=='top-to-bottom':
        for lev in sorted(buckets):
            items=buckets[lev]
            for j,eid in enumerate(items):
                e=byid[eid]; x=PAD+(j+(max_slots-len(items))/2)*step_x; y=PAD+lev*step_y
                nodes.append({'id':eid,'label':e['label'],'kind':e['kind'],'x':round(x,2),'y':y,'width':flow_w,'height':flow_h})
    else:
        for lev in sorted(buckets):
            items=buckets[lev]
            for j,eid in enumerate(items):
                e=byid[eid]; x=PAD+lev*step_x; y=PAD+(j+(max_slots-len(items))/2)*step_y
                nodes.append({'id':eid,'label':e['label'],'kind':e['kind'],'x':x,'y':round(y,2),'width':flow_w,'height':flow_h})
    return nodes,back

def _ports(a,b,direction):
    ac=center(a); bc=center(b)
    if direction=='top-to-bottom': return (ac[0],a['y']+a['height']),(bc[0],b['y'])
    return (a['x']+a['width'],ac[1]),(b['x'],bc[1])

def _orthogonal(a,b,direction,kind):
    p1,p2=_ports(a,b,direction)
    if kind in {'return','feedback'}:
        if direction=='top-to-bottom':
            x=min(a['x'],b['x'])-42; return [list(p1),[x,p1[1]],[x,p2[1]],list(p2)]
        y=max(a['y']+a['height'],b['y']+b['height'])+54; return [list(p1),[p1[0],y],[p2[0],y],list(p2)]
    if direction=='top-to-bottom':
        m=(p1[1]+p2[1])/2; return [list(p1),[p1[0],m],[p2[0],m],list(p2)]
    m=(p1[0]+p2[0])/2; return [list(p1),[m,p1[1]],[m,p2[1]],list(p2)]

def _flow_edges(ir,nodes,back_ids):
    nmap={n['id']:n for n in nodes}; direction=ir['representation']['reading_direction']; edges=[]
    outer=max(n['x']+n['width'] for n in nodes)+78 if direction=='top-to-bottom' else max(n['y']+n['height'] for n in nodes)+78
    for r in ir['relationships']:
        a=nmap[r['from']]; b=nmap[r['to']]; label=r.get('label') or r['semantic']; lw=text_width(label)
        if r['id'] in back_ids:
            if direction=='top-to-bottom':
                p1=[a['x']+a['width'],a['y']+a['height']/2]; p2=[b['x']+b['width'],b['y']+b['height']/2]
                pts=[p1,[outer,p1[1]],[outer,p2[1]],p2]; mx=outer; my=(p1[1]+p2[1])/2
                lb={'x':mx-lw-8,'y':my-LABEL_H/2,'width':lw,'height':LABEL_H}
            else:
                p1=[a['x']+a['width']/2,a['y']+a['height']]; p2=[b['x']+b['width']/2,b['y']+b['height']]
                pts=[p1,[p1[0],outer],[p2[0],outer],p2]; mx=(p1[0]+p2[0])/2; my=outer
                lb={'x':mx-lw/2,'y':my-LABEL_H-8,'width':lw,'height':LABEL_H}
        else:
            pts=_orthogonal(a,b,direction,r['kind']); ac=center(a); bc=center(b)
            if direction=='top-to-bottom': mx=(ac[0]+bc[0])/2; my=(a['y']+a['height']+b['y'])/2
            else: mx=(a['x']+a['width']+b['x'])/2; my=(ac[1]+bc[1])/2
            lb={'x':mx-lw/2,'y':my-LABEL_H/2,'width':lw,'height':LABEL_H}
        edges.append({'id':r['id'],'from':r['from'],'to':r['to'],'kind':r['kind'],'semantic':r['semantic'],'points':pts,'label':label,'label_box':lb})
    return edges

def _comparison_nodes(ir):
    byid={e['id']:e for e in ir['entities']}; sides=[g for g in ir.get('groups',[]) if g.get('kind')=='comparison-side']; nodes=[]
    for c,g in enumerate(sides):
        for r,eid in enumerate(g['members']):
            e=byid[eid]; nodes.append({'id':eid,'label':e['label'],'kind':e['kind'],'x':PAD+c*(NODE_W+180),'y':PAD+54+r*(NODE_H+GAP_Y),'width':NODE_W,'height':NODE_H,'group_id':g['id']})
    placed={n['id'] for n in nodes}
    for e in ir['entities']:
        if e['id'] not in placed: nodes.append({'id':e['id'],'label':e['label'],'kind':e['kind'],'x':PAD,'y':PAD+54+len(nodes)*(NODE_H+GAP_Y),'width':NODE_W,'height':NODE_H})
    return nodes

def _sequence_layout(ir):
    ents=ir['entities']; rels=sorted(ir['relationships'],key=lambda r:r.get('order',999999)); nodes=[]
    for i,e in enumerate(ents): nodes.append({'id':e['id'],'label':e['label'],'kind':e['kind'],'x':PAD+i*(NODE_W+72),'y':PAD,'width':NODE_W,'height':NODE_H})
    nmap={n['id']:n for n in nodes}; edges=[]; y0=PAD+NODE_H+62
    for i,r in enumerate(rels):
        a,b=nmap[r['from']],nmap[r['to']]; ax,_=center(a); bx,_=center(b); y=y0+i*56; label=r.get('label') or r['semantic']; lw=text_width(label)
        edges.append({'id':r['id'],'from':r['from'],'to':r['to'],'kind':r['kind'],'semantic':r['semantic'],'points':[[ax,y],[bx,y]],'label':label,'label_box':{'x':(ax+bx)/2-lw/2,'y':y-LABEL_H-4,'width':lw,'height':LABEL_H}})
    height=y0+max(1,len(rels))*56+PAD; width=PAD*2+max(1,len(ents))*NODE_W+max(0,len(ents)-1)*72
    lifelines=[{'entity_id':n['id'],'x':center(n)[0],'y1':n['y']+n['height'],'y2':height-PAD} for n in nodes]
    return nodes,edges,lifelines,width,height

def _story_layout(ir):
    beats=sorted(ir.get('narrative_beats',[]),key=lambda b:b['order']); nodes=[]
    for i,b in enumerate(beats): nodes.append({'id':b['id'],'label':b['title'],'kind':'beat','description':b['action'],'x':PAD,'y':PAD+i*(112+GAP_Y),'width':620,'height':112})
    width=PAD*2+620; height=PAD*2+max(1,len(nodes))*112+max(0,len(nodes)-1)*GAP_Y
    return nodes,[],[],width,height

def _edges(ir,nodes):
    nmap={n['id']:n for n in nodes}; direction=ir['representation']['reading_direction']; edges=[]; pairs={(x['from'],x['to']) for x in ir['relationships']}
    for r in ir['relationships']:
        a=nmap[r['from']]; b=nmap[r['to']]; route_kind=r['kind']
        if ir['representation']['type']=='state' and (r['to'],r['from']) in pairs and r['from']>r['to']: route_kind='return'
        pts=_orthogonal(a,b,direction,route_kind); label=r.get('label') or r['semantic']; lw=text_width(label); ac=center(a); bc=center(b)
        if route_kind in {'return','feedback'}:
            seg=max(zip(pts,pts[1:]),key=lambda ab:abs(ab[1][0]-ab[0][0])+abs(ab[1][1]-ab[0][1])); mx=(seg[0][0]+seg[1][0])/2; my=(seg[0][1]+seg[1][1])/2
        elif direction=='top-to-bottom': mx=(ac[0]+bc[0])/2; my=(a['y']+a['height']+b['y'])/2
        else: mx=(a['x']+a['width']+b['x'])/2; my=(ac[1]+bc[1])/2
        edges.append({'id':r['id'],'from':r['from'],'to':r['to'],'kind':r['kind'],'semantic':r['semantic'],'points':pts,'label':label,'label_box':{'x':mx-lw/2,'y':my-LABEL_H/2,'width':lw,'height':LABEL_H}})
    return edges

def build_layout(ir,semantic_sha256=None):
    typ=ir['representation']['type']
    if typ not in SUPPORTED: raise ValueError(f'unsupported canonical renderer type: {typ}')
    if typ=='sequence': nodes,edges,lifelines,width,height=_sequence_layout(ir)
    elif typ in {'story-strip','before-after','timeline'}: nodes,edges,lifelines,width,height=_story_layout(ir)
    elif typ=='flow':
        nodes,back_ids=_flow_nodes(ir); edges=_flow_edges(ir,nodes,back_ids); lifelines=[]
        maxx=max((n['x']+n['width'] for n in nodes),default=0); maxy=max((n['y']+n['height'] for n in nodes),default=0)
        for e in edges:
            for pt in e['points']: maxx=max(maxx,pt[0]); maxy=max(maxy,pt[1])
        width=max(720,math.ceil(maxx+PAD)); height=max(420,math.ceil(maxy+PAD))
    else:
        nodes=_comparison_nodes(ir) if typ=='structural-comparison' else _generic_nodes(ir); edges=_edges(ir,nodes); lifelines=[]
        maxx=max((n['x']+n['width'] for n in nodes),default=0); maxy=max((n['y']+n['height'] for n in nodes),default=0)
        for e in edges:
            for pt in e['points']: maxx=max(maxx,pt[0]); maxy=max(maxy,pt[1])
        width=max(720,math.ceil(maxx+PAD)); height=max(420,math.ceil(maxy+PAD))
    layout={'schema_version':LAYOUT_SCHEMA,'semantic_ir_sha256':semantic_sha256 or sha256_json(ir),'representation_type':typ,'reading_direction':ir['representation']['reading_direction'],'viewport':{'width':int(math.ceil(width)),'height':int(math.ceil(height)),'padding':PAD},'nodes':nodes,'edges':edges,'lifelines':lifelines,'constraints':{'target_zero_crossings':bool(ir.get('constraints',{}).get('target_zero_crossings',False))},'text_equivalent':ir['text_equivalent']}
    layout['layout_sha256']=sha256_json({k:v for k,v in layout.items() if k!='layout_sha256'})
    return layout
