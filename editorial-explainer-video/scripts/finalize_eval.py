#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def issue(code,path,message): return {"code":code,"path":path,"message":message}

def finalize(machine_path, review_path, review_validation_path):
    machine=load(machine_path); review=load(review_path); rv=load(review_validation_path)
    notes=[]; hard=[]
    if machine.get('schema')!='editorial-explainer-machine-eval/v1' or machine.get('status')!='PASSED':
        hard.append(issue('MACHINE_EVAL_FAILED','machine_eval','machine evaluation must pass'))
    if rv.get('schema')!='editorial-explainer-review-validation/v1' or rv.get('status')!='PASSED':
        hard.append(issue('REVIEW_VALIDATION_FAILED','review_validation','review validation must pass'))
    hard.extend(review.get('hard_fails') or [])
    status='FAIL' if hard else review.get('verdict','INSUFFICIENT_EVIDENCE')
    if status=='PASS' and review.get('artifact_stage')!='final':
        notes.append('PASS is stage-local; only artifact_stage=final may be used as final audiovisual certification.')
    return {
        'schema':'editorial-explainer-eval-summary/v1',
        'status':status,
        'machine_eval_sha256':sha(machine_path),
        'review_sha256':sha(review_path),
        'artifact_stage':review.get('artifact_stage'),
        'weighted_score':rv.get('weighted_score'),
        'hard_fails':hard,
        'notes':notes,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('machine'); ap.add_argument('review'); ap.add_argument('review_validation'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    try:r=finalize(a.machine,a.review,a.review_validation)
    except Exception as e:r={'schema':'editorial-explainer-eval-summary/v1','status':'FAIL','hard_fails':[issue('FINALIZER_EXCEPTION','$',str(e))],'notes':[]}
    print(json.dumps(r,ensure_ascii=False,indent=2)); return 0 if r.get('status') in {'PASS','REVISE'} else 1
if __name__=='__main__': sys.exit(main())
