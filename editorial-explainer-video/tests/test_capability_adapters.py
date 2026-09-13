import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
COMP=ROOT/'scripts'/'compile_capabilities.py'
VAL=ROOT/'scripts'/'validate_capabilities.py'
PLAN=ROOT/'tests'/'fixtures'/'valid-plan.json'
BAD=ROOT/'tests'/'fixtures'/'invalid-route-plan.json'
LEDGER=ROOT/'tests'/'fixtures'/'evidence-ledger.json'

class CapabilityAdapterTests(unittest.TestCase):
    def run_compile(self, plan, out):
        return subprocess.run([sys.executable,str(COMP),str(plan),str(LEDGER),str(out),'--json'],capture_output=True,text=True)

    def test_valid_compile_and_validation(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'handoff'; r=self.run_compile(PLAN,out)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            m=json.loads((out/'capability-manifest.json').read_text())
            routes={x['beat_id']:x for x in m['beat_routes']}
            b1=[json.loads((out/'packets'/f'{pid}.json').read_text()) for pid in routes['B001']['packet_ids']]
            b2=[json.loads((out/'packets'/f'{pid}.json').read_text()) for pid in routes['B002']['packet_ids']]
            self.assertEqual([x['owner'] for x in b1],['data-viz-selector','motion-graphics'])
            self.assertEqual([x['owner'] for x in b2],['visual-semantic-compiler','motion-graphics'])
            self.assertEqual(b2[0]['qualifier_acknowledgements']['C002'],['Tratar como uma explicação plausível, não como causa única.'])
            v=subprocess.run([sys.executable,str(VAL),str(out/'capability-manifest.json'),str(PLAN),str(LEDGER),'--json'],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stdout+v.stderr)
            self.assertEqual(json.loads(v.stdout)['status'],'PASSED')

    def test_tampered_qualifier_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'handoff'; self.assertEqual(self.run_compile(PLAN,out).returncode,0)
            m=json.loads((out/'capability-manifest.json').read_text()); route=next(x for x in m['beat_routes'] if x['beat_id']=='B002')
            p=out/'packets'/f"{route['packet_ids'][0]}.json"; pkt=json.loads(p.read_text()); pkt['qualifier_acknowledgements']={}; p.write_text(json.dumps(pkt,ensure_ascii=False,indent=2)+"\n")
            v=subprocess.run([sys.executable,str(VAL),str(out/'capability-manifest.json'),str(PLAN),str(LEDGER),'--json'],capture_output=True,text=True)
            self.assertNotEqual(v.returncode,0); codes={e['code'] for e in json.loads(v.stdout)['errors']}; self.assertIn('packet_qualifier_drift',codes)

    def test_incompatible_preferred_owner_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            r=self.run_compile(BAD,Path(td)/'handoff')
            self.assertNotEqual(r.returncode,0)
            codes={e['code'] for e in json.loads(r.stdout)['errors']}
            self.assertIn('preferred_owner_incompatible',codes)

if __name__=='__main__': unittest.main()
