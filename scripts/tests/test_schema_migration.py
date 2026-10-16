"""Regression checks for alias preservation and source-attributed resource export."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from migrate_ledger_schema import migrate
from ledger_schema import SCHEMA_VERSION
from check_ledger_consistency import check
import classification_manager as manager

class MigrationTests(unittest.TestCase):
 def test_idempotence_preserves_original_labels_and_evidence(self):
  module={'id':'paper:qa','tasks':[], 'other_tasks':['question_answering'], 'evidence':[{'quote':'Exact source text.'}]}
  rows=[{'task_axis_other':'question_answering; classification','reviewed_modules_json':json.dumps([module])}]
  migrated=migrate(copy.deepcopy(rows))
  self.assertEqual(migrated,migrate(copy.deepcopy(migrated)))
  self.assertEqual(migrated[0]['taxonomy_schema_version'],SCHEMA_VERSION)
  self.assertEqual(migrated[0]['task_axis_other'],'temporal_question_answering; time_series_classification')
  self.assertEqual(json.loads(migrated[0]['task_aliases_source_json'])['other'],rows[0]['task_axis_other'])
  self.assertEqual(json.loads(migrated[0]['reviewed_modules_json'])[0]['evidence'],module['evidence'])
 def test_resource_without_attribution_fails(self):
  rows=manager.read_csv(manager.LEDGER)[:1]
  records=json.loads(manager.JSON_LEDGER.read_text())[:1]
  resource={'kind':'repository','url':'https://github.com/example/example'}
  rows[0]['official_resources_json']=json.dumps([resource]);records[0]['official_resources']=[resource]
  self.assertTrue(any('missing resource attribution' in error for error in check(rows,records)))

if __name__=='__main__': unittest.main()
