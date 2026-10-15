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
if __name__=='__main__':unittest.main()
