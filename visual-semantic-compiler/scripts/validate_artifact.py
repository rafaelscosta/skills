#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

def validate_bytes(raw:bytes, expected_semantic_sha=None, expected_layout_sha=None):
    E=[];W=[]; text=raw.decode('utf-8','replace')
    def e(c,m):E.append({'code':c,'message':m})
    if '<svg' not in text or '</svg>' not in text:e('missing-inline-svg','artifact must contain inline SVG')
    if 'role="img"' not in text:e('svg-accessibility','inline SVG must expose role=img')
    if '<title id="diagram-title">' not in text:e('svg-title','inline SVG requires title')
    if '<desc id="diagram-desc">' not in text:e('svg-desc','inline SVG requires text-equivalent desc')
    m=re.search(r'<meta name="visual-semantic-ir-sha256" content="([0-9a-f]{64})">',text)
    if not m:e('semantic-digest','semantic digest meta tag missing')
    elif expected_semantic_sha and m.group(1)!=expected_semantic_sha:e('semantic-digest','artifact digest does not match frozen semantic IR')
    rm=re.search(r'<script type="application/json" id="visual-receipt">(.*?)</script>',text,re.S)
    embedded=None
    if not rm:e('embedded-receipt','embedded visual receipt missing')
    else:
        try: embedded=json.loads(rm.group(1))
        except Exception:e('embedded-receipt-json','embedded visual receipt must be valid JSON')
    if embedded is not None:
        if expected_semantic_sha and embedded.get('semantic_ir_sha256')!=expected_semantic_sha:e('embedded-semantic-digest','embedded receipt semantic digest mismatch')
        if expected_layout_sha and embedded.get('layout_sha256')!=expected_layout_sha:e('embedded-layout-digest','embedded receipt layout digest mismatch')
    if re.search(r'<(?:script|link)[^>]+(?:src|href)="https?://',text,re.I):e('external-runtime','canonical artifact must not require external script/style runtime')
    if '```mermaid' in text.lower():e('raw-mermaid','raw Mermaid source cannot be the delivered visual')
    return {'schema_version':'visual-artifact-receipt/v1','status':'invalid' if E else 'valid','artifact_sha256':hashlib.sha256(raw).hexdigest(),'artifact_bytes':len(raw),'checks':{'inline_svg':'failed' if any(x['code']=='missing-inline-svg' for x in E) else 'passed','accessibility':'failed' if any(x['code'] in {'svg-accessibility','svg-title','svg-desc'} for x in E) else 'passed','semantic_binding':'failed' if any(x['code'] in {'semantic-digest','embedded-semantic-digest','embedded-layout-digest','embedded-receipt-json'} for x in E) else 'passed','self_contained':'failed' if any(x['code']=='external-runtime' for x in E) else 'passed','source_hygiene':'failed' if any(x['code']=='raw-mermaid' for x in E) else 'passed'},'errors':E,'warnings':W,'perceptual_review':'pending'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('artifact');ap.add_argument('--semantic-sha256');ap.add_argument('--layout-sha256');ap.add_argument('--json',action='store_true');a=ap.parse_args()
    try:raw=Path(a.artifact).read_bytes()
    except Exception as ex:
        print(json.dumps({'schema_version':'visual-artifact-receipt/v1','status':'error','error':str(ex)}));return 2
    r=validate_bytes(raw,a.semantic_sha256,a.layout_sha256);print(json.dumps(r,ensure_ascii=False,indent=None if a.json else 2));return 0 if r['status']=='valid' else 1
if __name__=='__main__':sys.exit(main())
