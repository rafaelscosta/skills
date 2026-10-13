import importlib.util, json, shutil, sys, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('persuasion_validator',Path(__file__).with_name('validate_bundle.py'));mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
ROOT=Path(__file__).resolve().parents[1]
class Contracts(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'persuasion-architect';shutil.copytree(ROOT,self.root)
 def tearDown(self):self.tmp.cleanup()
 def test_commented_invariant_does_not_override_false(self):
  p=self.root/'config.yaml';p.write_text(p.read_text().replace('mechanism_contract_required_for_material_outcome_claims: true','mechanism_contract_required_for_material_outcome_claims: false # mechanism_contract_required_for_material_outcome_claims: true'));self.assertTrue(mod.validate(self.root))
 def test_yaml_scalar_rejected(self):
  (self.root/'config.yaml').write_text('scalar');self.assertTrue(mod.validate(self.root))
 def test_nested_qa_requirement_cannot_be_removed(self):
  p=self.root/'references/persuasion-architecture.schema.json';s=json.loads(p.read_text());s['properties']['qa']['required'].remove('scores');p.write_text(json.dumps(s));self.assertTrue(mod.validate(self.root))
 def test_unsafe_publication_rejected(self):
  p=self.root/'config.yaml';p.write_text(p.read_text().replace('publication_default: deny','publication_default: allow'));self.assertTrue(mod.validate(self.root))
 def test_duplicate_yaml_key_rejected(self):
  p=self.root/'config.yaml';p.write_text(p.read_text().replace('publication_default: deny','publication_default: allow\n  publication_default: deny'));self.assertTrue(mod.validate(self.root))
 def test_false_qa_floor_rejected(self):
  schema=json.loads((self.root/'references/persuasion-architecture.schema.json').read_text())
  def sample(node):
   if 'const' in node:return node['const']
   if 'enum' in node:return node['enum'][0]
   kind=node.get('type','string');kind=kind[0] if isinstance(kind,list) else kind
   if kind=='object':return {k:sample(node['properties'][k]) for k in node.get('required',[])}
   if kind=='array':return [sample(node['items']) for _ in range(node.get('minItems',0))]
   if kind in ['integer','number']:return node.get('minimum',0)
   if kind=='boolean':return False
   return ('P01' if node.get('pattern','').startswith('^P') else 'B01') if 'pattern' in node else 'Synthetic fixture'
  data=sample(schema);data['beliefs'][0]['belief_id']='B01';data['beliefs'][0]['dependencies']=[]
  self.assertEqual(mod.validate_architecture(self.root,data),[])
  data['qa']['critical_floor_passed']=True
  self.assertTrue(any(f.code=='P021' for f in mod.validate_architecture(self.root,data)))
 def test_valid_source(self):self.assertEqual(mod.validate(self.root),[])
if __name__=='__main__':unittest.main()
