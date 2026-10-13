import importlib.util,copy,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('handoff',Path(__file__).with_name('validate_handoff.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Handoff(unittest.TestCase):
 def setUp(self):
  self.contract={'objective':'Synthetic QA','audience':'QA','viewer_outcome':'Validate source contracts','format_profile':'test','must_preserve':[],'must_avoid':[],'acceptance_gates':['source truth'],'assumptions':[],'open_questions':[],'source_truth':['Synthetic fixture'],'target_duration_seconds':None}
  self.manifest={'assets':[{'id':'a','kind':'video','source_locator':'fixture://a','inspected':True}],'segments':[{'asset_id':'a','locator':'00:00','observations':['Synthetic observed frame']}],'risks':[],'missing_coverage':[]}
  self.qa={'verdict':'PASS','blocking_gates':[{'name':'truth','status':'PASS'}],'findings':[],'highest_value_defects':[],'confidence':1}
 def validate(self):return m.validate_handoff(self.contract,self.manifest,self.qa)
 def test_valid_nullable_duration(self):self.assertEqual(self.validate(),[])
 def test_source_truth_required(self):del self.contract['source_truth'];self.assertTrue(self.validate())
 def test_no_observation_of_uninspected_asset(self):self.manifest['assets'][0]['inspected']=False;self.assertTrue(self.validate())
 def test_unknown_asset_rejected(self):self.manifest['segments'][0]['asset_id']='missing';self.assertTrue(self.validate())
 def test_duplicate_asset_ids_rejected(self):self.manifest['assets']*=2;self.assertTrue(self.validate())
 def test_failed_or_uncertified_gate_cannot_pass(self):
  for status in ['FAIL','NOT_CERTIFIED']:
   self.qa['blocking_gates'][0]['status']=status;self.assertTrue(self.validate())
 def test_honest_blocked_gate_valid(self):self.qa['verdict']='BLOCK';self.qa['blocking_gates'][0]['status']='NOT_CERTIFIED';self.assertEqual(self.validate(),[])
if __name__=='__main__':unittest.main()
