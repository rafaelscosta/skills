#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def validate(evidence_path: Path, review_path: Path):
    errors=[]; warnings=[]
    try:
        evidence_raw=evidence_path.read_bytes(); evidence=json.loads(evidence_raw)
        review=json.loads(review_path.read_text())
    except Exception as ex:
        return {'schema_version':'visual-perceptual-gate-receipt/v1','status':'error','errors':[{'code':'read-error','message':str(ex)}]}
    def err(code,msg): errors.append({'code':code,'message':msg})
    if review.get('schema_version')!='visual-perceptual-review/v1': err('schema-version','review schema_version must be visual-perceptual-review/v1')
    if evidence.get('schema_version')!='visual-evidence-receipt/v1': err('evidence-schema','unexpected evidence receipt schema')
    artifact_sha=evidence.get('artifact_sha256')
    if review.get('artifact_sha256')!=artifact_sha: err('artifact-binding','review artifact_sha256 does not match evidence')
    evidence_sha=sha(evidence_raw)
    if review.get('evidence_sha256')!=evidence_sha: err('evidence-binding','review evidence_sha256 does not match evidence receipt bytes')
    reviewer=review.get('reviewer') or {}
    if not isinstance(reviewer,dict) or not str(reviewer.get('id','')).strip(): err('reviewer','reviewer.id is required')
    if reviewer.get('type') not in {'human','model'}: err('reviewer-type','reviewer.type must be human or model')
    status=review.get('status')
    if status not in {'passed','failed','skipped'}: err('review-status','status must be passed, failed, or skipped')
    defects=review.get('defects',[])
    if not isinstance(defects,list): err('defects','defects must be an array'); defects=[]
    if status=='passed':
        if evidence.get('status')!='passed': err('evidence-not-passed','perceptual pass requires automated evidence status passed')
        if defects: err('pass-with-defects','passed review cannot contain defects')
    elif status=='failed' and not defects: err('failure-without-defect','failed review must record at least one concrete defect')
    elif status=='skipped' and not str(review.get('reason','')).strip(): err('skip-without-reason','skipped review must record reason')
    for i,d in enumerate(defects):
        if not isinstance(d,dict): err('defect-shape',f'defects[{i}] must be object'); continue
        if not str(d.get('code','')).strip(): err('defect-code',f'defects[{i}].code required')
        if d.get('severity') not in {'critical','major','minor'}: err('defect-severity',f'defects[{i}].severity invalid')
        if not str(d.get('evidence','')).strip(): err('defect-evidence',f'defects[{i}].evidence required')
    combined='invalid'
    if not errors:
        combined={'passed':'perceptually-passed','failed':'perceptually-failed','skipped':'perceptual-review-skipped'}[status]
    return {'schema_version':'visual-perceptual-gate-receipt/v1','status':'invalid' if errors else 'valid','delivery_status':combined,'artifact_sha256':artifact_sha,'evidence_sha256':evidence_sha,'reviewer':reviewer,'review_status':status,'defects':defects,'errors':errors,'warnings':warnings}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('evidence'); ap.add_argument('review'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    r=validate(Path(a.evidence),Path(a.review)); print(json.dumps(r,ensure_ascii=False,indent=None if a.json else 2)); return 0 if r['status']=='valid' else 1
if __name__=='__main__': sys.exit(main())
