import copy, importlib.util, json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validate_invariant_coverage',ROOT/'scripts'/'validate_invariant_coverage.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
IR=json.loads((ROOT/'evals'/'visual-integration'/'refund.ir.json').read_text())
BASE=json.loads((ROOT/'evals'/'visual-integration'/'refund.coverage.json').read_text())

class InvariantCoverageTests(unittest.TestCase):
    def test_valid_fixture(self):
        self.assertEqual(mod.validate(BASE,IR)['status'],'valid')

    def test_unaccounted_visual_invariant_fails(self):
        data=copy.deepcopy(BASE); data['coverage']=data['coverage'][1:]
        self.assertIn('unaccounted-invariant',{e['code'] for e in mod.validate(data,IR)['errors']})

    def test_missing_ir_ref_fails(self):
        data=copy.deepcopy(BASE); data['coverage'][0]['ir_refs']=['ghost']
        self.assertIn('missing-ir-ref',{e['code'] for e in mod.validate(data,IR)['errors']})

    def test_blocked_prevents_handoff(self):
        data=copy.deepcopy(BASE); data['coverage'][0]={'invariant_id':'INV-001','status':'blocked','ir_refs':[],'reason':'source conflict'}
        self.assertIn('handoff-blocked',{e['code'] for e in mod.validate(data,IR)['errors']})

    def test_omission_requires_reason(self):
        data=copy.deepcopy(BASE); data['coverage'][0]={'invariant_id':'INV-001','status':'omitted-with-reason','ir_refs':[]}
        self.assertIn('omission-reason',{e['code'] for e in mod.validate(data,IR)['errors']})

    def test_duplicate_coverage_fails(self):
        data=copy.deepcopy(BASE); data['coverage'].append(copy.deepcopy(data['coverage'][0]))
        self.assertIn('duplicate-coverage',{e['code'] for e in mod.validate(data,IR)['errors']})

    def test_ir_digest_binding(self):
        raw=json.dumps(IR,sort_keys=True,separators=(',',':')).encode()
        data=copy.deepcopy(BASE); data['visual_ir_sha256']=mod.sha(raw)
        self.assertEqual(mod.validate(data,IR,ir_bytes=raw)['status'],'valid')
        data['visual_ir_sha256']='0'*64
        self.assertIn('ir-binding',{e['code'] for e in mod.validate(data,IR,ir_bytes=raw)['errors']})

if __name__=='__main__': unittest.main()
