import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VALIDATOR=ROOT/'scripts'/'validate_plan.py'
LEDGER=ROOT/'tests'/'fixtures'/'evidence-ledger.json'
class ExplainerValidatorTests(unittest.TestCase):
    def run_case(self,name):
        p=subprocess.run([sys.executable,str(VALIDATOR),str(ROOT/'tests'/'fixtures'/name),str(LEDGER),'--json'],capture_output=True,text=True)
        return p, json.loads(p.stdout)
    def test_valid_plan_passes(self):
        p,r=self.run_case('valid-plan.json'); self.assertEqual(p.returncode,0); self.assertEqual(r['status'],'PASSED'); self.assertEqual(r['behavioral_editorial_review'],'pending')
    def test_invalid_plan_fails_closed(self):
        p,r=self.run_case('invalid-plan.json'); self.assertEqual(p.returncode,1); self.assertEqual(r['status'],'FAILED'); codes={e['code'] for e in r['errors']}; self.assertTrue({'evidence_hash_mismatch','required_qualifier_missing','viewer_state_no_progress','beat_order_invalid','causal_overclaim'} <= codes)
if __name__=='__main__': unittest.main()
