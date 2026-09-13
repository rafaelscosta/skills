import copy, hashlib, importlib.util, json, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
sys.path.insert(0,str(SCRIPTS))
from compile_capabilities import compile_packets
from evaluate_semantic import evaluate
from validate_review import validate as validate_review
from finalize_eval import finalize

PLAN=ROOT/'tests/fixtures/valid-plan.json'
LEDGER=ROOT/'tests/fixtures/evidence-ledger.json'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')

def review_obj(manifest, verdict='PASS', hard_fails=None, scores=None):
    scores=scores or {
        'factual_epistemic_integrity':4.5,
        'explanatory_clarity':4.5,
        'narrative_coherence':4.5,
        'beat_closure':4.0,
        'visual_explanatory_value':4.0,
        'pacing_cognitive_load':4.0,
    }
    return {
        'schema':'editorial-explainer-review/v1',
        'artifact_stage':'plan',
        'reviewer':{'id':'fixture-reviewer','type':'language-model'},
        'bindings':{
            'plan_sha256':sha(PLAN),
            'evidence_ledger_sha256':sha(LEDGER),
            'capability_manifest_sha256':sha(manifest),
            'artifact_sha256':None,
        },
        'dimensions':{k:{'status':'SCORED','score':v,'rationale':f'Fixture rationale for {k}.','evidence_refs':['valid-plan.json']} for k,v in scores.items()},
        'hard_fails':hard_fails or [],
        'verdict':verdict,
    }

class EvalHarnessTests(unittest.TestCase):
    def build(self,tmp):
        manifest,errs=compile_packets(PLAN,LEDGER,Path(tmp)/'cap')
        self.assertFalse(errs)
        return manifest

    def test_machine_eval_passes_integrated_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            manifest=self.build(td)
            result=evaluate(PLAN,LEDGER,manifest)
            self.assertEqual(result['status'],'PASSED')
            self.assertTrue(all(v==1.0 for v in result['metrics'].values()))

    def test_machine_eval_fails_on_tampered_packet(self):
        with tempfile.TemporaryDirectory() as td:
            manifest=self.build(td)
            m=json.loads(Path(manifest).read_text())
            entry=next(e for e in m['packets'] if e['scope']=='beat')
            pp=Path(manifest).parent/entry['path']
            pkt=json.loads(pp.read_text())
            pkt['claim_refs']=[]
            write_json(pp,pkt)
            result=evaluate(PLAN,LEDGER,manifest)
            self.assertEqual(result['status'],'FAILED')
            self.assertTrue(any(h['code']=='CAPABILITY_VALIDATION_FAILED' for h in result['hard_fails']))

    def test_valid_plan_stage_review_and_summary_pass(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); manifest=self.build(td)
            rp=td/'review.json'; write_json(rp,review_obj(manifest))
            rv=validate_review(rp,PLAN,LEDGER,manifest)
            self.assertEqual(rv['status'],'PASSED')
            self.assertEqual(rv['expected_verdict'],'PASS')
            machine=evaluate(PLAN,LEDGER,manifest); mp=td/'machine.json'; write_json(mp,machine)
            rvp=td/'review-validation.json'; write_json(rvp,rv)
            summary=finalize(mp,rp,rvp)
            self.assertEqual(summary['status'],'PASS')
            self.assertTrue(any('stage-local' in n for n in summary['notes']))

    def test_high_score_hard_fail_forces_fail(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); manifest=self.build(td)
            hard=[{'code':'CAUSALITY_OVERSTATED','evidence':'Beat B002 visually implies exclusive causation.'}]
            review=review_obj(manifest,verdict='FAIL',hard_fails=hard,scores={
                'factual_epistemic_integrity':5.0,'explanatory_clarity':5.0,'narrative_coherence':5.0,
                'beat_closure':5.0,'visual_explanatory_value':5.0,'pacing_cognitive_load':5.0,
            })
            rp=td/'review.json'; write_json(rp,review)
            rv=validate_review(rp,PLAN,LEDGER,manifest)
            self.assertEqual(rv['status'],'PASSED')
            self.assertEqual(rv['expected_verdict'],'FAIL')
            mp=td/'machine.json'; write_json(mp,evaluate(PLAN,LEDGER,manifest))
            rvp=td/'rv.json'; write_json(rvp,rv)
            self.assertEqual(finalize(mp,rp,rvp)['status'],'FAIL')

    def test_stale_review_binding_fails(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); manifest=self.build(td)
            review=review_obj(manifest); review['bindings']['plan_sha256']='0'*64
            rp=td/'review.json'; write_json(rp,review)
            rv=validate_review(rp,PLAN,LEDGER,manifest)
            self.assertEqual(rv['status'],'FAILED')
            self.assertTrue(any(e['code']=='review_binding_mismatch' for e in rv['errors']))

if __name__=='__main__': unittest.main()
