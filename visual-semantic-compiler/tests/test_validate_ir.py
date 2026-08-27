import copy, importlib.util, json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validate_ir',ROOT/'scripts'/'validate_ir.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
BASE=json.loads((ROOT/'examples'/'concept-bridge-rag.json').read_text())

class ValidatorTests(unittest.TestCase):
    def test_valid_examples(self):
        for name in ['concept-bridge-rag.json','clarify-refund-flow.json']:
            data=json.loads((ROOT/'examples'/name).read_text())
            self.assertEqual(mod.validate(data)['status'],'valid')

    def test_missing_endpoint_fails(self):
        data=copy.deepcopy(BASE); data['relationships'][0]['to']='ghost'
        r=mod.validate(data)
        self.assertEqual(r['status'],'invalid')
        self.assertIn('missing-endpoint',{e['code'] for e in r['errors']})

    def test_sequence_requires_unique_order(self):
        data=copy.deepcopy(BASE); data['representation']['type']='sequence'
        for rel in data['relationships']: rel['order']=1
        r=mod.validate(data)
        self.assertIn('sequence-order',{e['code'] for e in r['errors']})

    def test_state_requires_state_entities_and_transitions(self):
        data=copy.deepcopy(BASE); data['representation']['type']='state'
        r=mod.validate(data)
        codes={e['code'] for e in r['errors']}
        self.assertIn('state-entity',codes); self.assertIn('state-transition',codes)

    def test_flow_branch_requires_labels(self):
        data=copy.deepcopy(BASE); data['representation']['type']='flow'
        data['relationships'].append({'id':'r6','from':'app','to':'store','kind':'flow','semantic':'alternate path'})
        r=mod.validate(data)
        self.assertIn('flow-branch-label',{e['code'] for e in r['errors']})

    def test_causal_rejects_dependency_edges(self):
        data=copy.deepcopy(BASE); data['representation']['type']='causal'
        r=mod.validate(data)
        self.assertIn('causal-kind',{e['code'] for e in r['errors']})

    def test_mixed_requires_distinct_narrative_and_structural_views(self):
        data=copy.deepcopy(BASE); data['representation']={'class':'mixed','type':'mixed','reading_direction':'top-to-bottom','primary_question':'Como funciona e quem se conecta?'}
        data['views']=[]
        r=mod.validate(data)
        self.assertIn('mixed-contract',{e['code'] for e in r['errors']})

if __name__=='__main__': unittest.main()
