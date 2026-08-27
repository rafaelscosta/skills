#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, html, importlib.util, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
core=load('layout_core',ROOT/'scripts'/'layout_core.py'); lv=load('validate_layout',ROOT/'scripts'/'validate_layout.py'); av=load('validate_artifact',ROOT/'scripts'/'validate_artifact.py')
def shab(b):return hashlib.sha256(b).hexdigest()
def semantic_validate(path):
    proc=subprocess.run([sys.executable,str(ROOT/'scripts'/'validate_ir.py'),str(path),'--json'],capture_output=True,text=True)
    try:r=json.loads(proc.stdout)
    except Exception: raise RuntimeError(proc.stderr or proc.stdout or 'semantic validator returned invalid receipt')
    if proc.returncode!=0 or r.get('status')!='valid': raise RuntimeError('semantic validation failed: '+json.dumps(r.get('errors',[]),ensure_ascii=False))
    return r
def esc(s):return html.escape(str(s),quote=True)
def path_d(points):return ' '.join(('M' if i==0 else 'L')+f' {p[0]:.1f} {p[1]:.1f}' for i,p in enumerate(points))
def render_svg(ir,layout):
    w=layout['viewport']['width'];h=layout['viewport']['height']
    parts=[f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="diagram-title diagram-desc" xmlns="http://www.w3.org/2000/svg">',f'<title id="diagram-title">{esc(ir["representation"]["primary_question"])}</title>',f'<desc id="diagram-desc">{esc(ir["text_equivalent"])}</desc>','<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>']
    for l in layout.get('lifelines',[]):parts.append(f'<line class="lifeline" x1="{l["x"]}" y1="{l["y1"]}" x2="{l["x"]}" y2="{l["y2"]}"/>')
    for e in layout['edges']:
        parts.append(f'<path class="edge edge-{esc(e.get("kind","other"))}" d="{path_d(e["points"])}" marker-end="url(#arrow)"/>')
    for e in layout['edges']:
        lb=e.get('label_box')
        if lb: parts.append(f'<rect class="label-mask" x="{lb["x"]}" y="{lb["y"]}" width="{lb["width"]}" height="{lb["height"]}" rx="3"/><text class="edge-label" x="{lb["x"]+lb["width"]/2}" y="{lb["y"]+16}" text-anchor="middle">{esc(e.get("label",""))}</text>')
    for n in layout['nodes']:
        cls='beat' if n.get('kind')=='beat' else 'node'
        parts.append(f'<g class="{cls}" data-node-id="{esc(n["id"])}"><rect x="{n["x"]}" y="{n["y"]}" width="{n["width"]}" height="{n["height"]}" rx="5"/><text class="node-label" x="{n["x"]+n["width"]/2}" y="{n["y"]+n["height"]/2-2}" text-anchor="middle">{esc(n["label"])}</text>')
        if n.get('description'): parts.append(f'<text class="node-desc" x="{n["x"]+n["width"]/2}" y="{n["y"]+n["height"]/2+22}" text-anchor="middle">{esc(n["description"][:78])}</text>')
        parts.append('</g>')
    parts.append('</svg>');return ''.join(parts)
def html_doc(ir,layout,semantic_sha,layout_receipt):
    svg=render_svg(ir,layout); omissions=''.join(f'<li>{esc(x)}</li>' for x in ir.get('omissions',[])); embedded=json.dumps({'semantic_ir_sha256':semantic_sha,'layout_sha256':layout_receipt['layout_sha256'],'layout_checks':layout_receipt['checks']},ensure_ascii=False)
    return f'''<!doctype html><html lang="{esc(ir['intent']['language'])}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="visual-semantic-ir-sha256" content="{semantic_sha}"><title>{esc(ir['representation']['primary_question'])}</title><style>:root{{--bg:#F7F8FC;--panel:#fff;--ink:#111;--muted:#5F6272;--lav:#E7EAF6;--accent:#C42A1C}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Arial,Helvetica,sans-serif}}main{{max-width:1180px;margin:auto;padding:36px}}h1{{font-family:Georgia,serif;font-weight:400;font-size:34px;line-height:1.12;margin:0 0 12px}}.lede{{color:var(--muted);max-width:850px;line-height:1.55}}.panel{{margin-top:28px;background:var(--panel);border:1.5px solid var(--ink);padding:18px;overflow:auto}}svg{{display:block;width:100%;height:auto;min-width:640px;color:var(--ink)}}.node rect,.beat rect{{fill:var(--lav);stroke:var(--ink);stroke-width:1.5}}.beat rect{{fill:#fff}}.node-label{{font-family:Georgia,serif;font-size:15px}}.node-desc{{font-size:11px;fill:var(--muted)}}.edge,.lifeline{{fill:none;stroke:var(--ink);stroke-width:1.6}}.lifeline{{stroke-dasharray:5 5;opacity:.45}}.label-mask{{fill:#fff;stroke:none}}.edge-label{{font-size:11px;fill:var(--accent)}}.notes{{margin-top:22px;border-top:1px solid #c9cbd4;padding-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:24px}}h2{{font-family:Georgia,serif;font-weight:400}}li,p{{line-height:1.55}}@media(max-width:760px){{main{{padding:20px}}.notes{{grid-template-columns:1fr}}}}</style></head><body><main><h1>{esc(ir['representation']['primary_question'])}</h1><p class="lede">{esc(ir['text_equivalent'])}</p><section class="panel">{svg}</section><section class="notes"><div><h2>O que este visual mostra</h2><p>{esc(ir['text_equivalent'])}</p></div><div><h2>O que foi deixado de fora</h2><ul>{omissions or '<li>Nenhuma omissão material registrada.</li>'}</ul></div></section><script type="application/json" id="visual-receipt">{esc(embedded)}</script></main></body></html>'''
def deliver(ir_path,out_path,layout_path=None):
    sem=semantic_validate(ir_path); raw=ir_path.read_bytes(); ir=json.loads(raw); semantic_sha=sem.get('input_sha256') or shab(raw)
    layout=core.build_layout(ir,semantic_sha); lr=lv.validate(layout)
    if lr['status']!='valid': raise RuntimeError('layout validation failed: '+json.dumps(lr['errors'],ensure_ascii=False))
    html_bytes=html_doc(ir,layout,semantic_sha,lr).encode('utf-8'); ar=av.validate_bytes(html_bytes,semantic_sha)
    if ar['status']!='valid': raise RuntimeError('artifact validation failed: '+json.dumps(ar['errors'],ensure_ascii=False))
    out_path.parent.mkdir(parents=True,exist_ok=True)
    tmp=out_path.with_suffix(out_path.suffix+'.tmp'); tmp.write_bytes(html_bytes); os.replace(tmp,out_path)
    if layout_path: layout_path.write_text(json.dumps(layout,ensure_ascii=False,indent=2))
    return {'schema_version':'visual-render-receipt/v1','status':'success','representation_type':ir['representation']['type'],'semantic_ir_sha256':semantic_sha,'layout_sha256':lr['layout_sha256'],'artifact_sha256':shab(html_bytes),'artifact_bytes':len(html_bytes),'layout_validation':lr,'artifact_validation':ar,'output':str(out_path),'layout_output':str(layout_path) if layout_path else None,'perceptual_review':'pending'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('ir');ap.add_argument('output');ap.add_argument('--layout-output');ap.add_argument('--json',action='store_true');a=ap.parse_args()
    try:r=deliver(Path(a.ir),Path(a.output),Path(a.layout_output) if a.layout_output else None);print(json.dumps(r,ensure_ascii=False,indent=None if a.json else 2));return 0
    except Exception as ex:
        r={'schema_version':'visual-render-receipt/v1','status':'error','error':str(ex)};print(json.dumps(r,ensure_ascii=False));return 1
if __name__=='__main__':sys.exit(main())
