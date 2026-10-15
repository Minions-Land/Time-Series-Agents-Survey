"""Module identity must survive multiple dimensions and task memberships."""
import importlib.util
from pathlib import Path
import json
import unittest
p=Path(__file__).resolve().parents[1]/'classification_manager.py'
spec=importlib.util.spec_from_file_location('manager',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class IdentityTests(unittest.TestCase):
 def test_distinct_modules_in_one_dimension(self):
  gh=m.empty_dimensions();gts=m.empty_dimensions();gh['Tools and Execution']=['generic_executor','same'];gts['Tools and Execution']=['temporal_slice','same']
  tasks={'forecasting_prediction':{'dimensions':{'Tools and Execution':['forecast_selector','same']}}}
  a,b,c=m.exclusive_harness_layers(gh,gts,tasks)
  self.assertEqual(a['Tools and Execution'],['generic_executor']);self.assertEqual(b['Tools and Execution'],['temporal_slice'])
 def test_reviewed_record_preserves_shared_task_module(self):
  x={'id':'generator','layer':'TSK','dimensions':['Tools and Execution','Optimization and Evolution'],'tasks':['forecasting_prediction','data_augmentation_synthesis'],'scope_reason':'Forecast training data','evidence':[{'locator':'p4','quote':'source'}]}
  r=m.module_contribution_record({'reviewed_modules_json':json.dumps([x])})
  self.assertEqual(len(r['modules']),1);self.assertEqual(len(r['task_specific']),2)
 def test_duplicate_module_rejected(self):
  x={'id':'x','layer':'LLM','scope_reason':'training','evidence':[{'locator':'p1'}]}
  with self.assertRaises(ValueError):m.reviewed_module_record({'citation_key':'paper','reviewed_modules_json':json.dumps([x,x])})
 def test_other_task_is_same_coordinate(self):
  x={'id':'classifier','layer':'TSK','dimensions':['Tools and Execution'],'tasks':[], 'other_tasks':['classification'],'scope_reason':'Class output','evidence':[{'locator':'p4','quote':'source'}]}
  r=m.reviewed_module_record({'reviewed_modules_json':json.dumps([x])})
  self.assertEqual(list(r['task_specific']),['classification'])
  self.assertEqual(len(r['modules']),1)
 def test_exclusion_is_not_verified_module(self):
  r=m.reviewed_module_record({'reviewed_modules_json':'[]','taxonomy_review_status':'out_of_scope'})
  self.assertEqual(r['review_status'],'out_of_scope');self.assertEqual(r['modules'],[])
 def test_repository_is_not_paper_verification(self):
  x={'id':'repo','layer':'GH','dimensions':['Tools and Execution'],'scope_reason':'executor','evidence':[{'locator':'README','quote':'source'}]}
  r=m.reviewed_module_record({'reviewed_modules_json':json.dumps([x]),'taxonomy_review_status':'repository_verified'})
  self.assertEqual(r['review_status'],'repository_verified')
if __name__=='__main__':unittest.main()
