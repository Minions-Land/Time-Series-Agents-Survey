"""Five-dimension schema, re-audit import helpers and work-level evaluation evidence."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import apply_reaudit
import classification_manager as manager
from check_ledger_consistency import check, module_errors
from ledger_schema import DIMENSIONS, RETIRED_DIMENSIONS


def module(**kw):
    m = {'id': 'paper:m', 'name': 'm', 'layer': 'GH', 'dimensions': ['Tools and Execution'], 'functions': [],
         'view_status': 'general_runtime', 'llm_route': [], 'tasks': ['forecasting_prediction'], 'other_tasks': [],
         'role': 'method', 'scope_reason': 'r', 'rubric_path': ['R1:contributed'], 'confidence': 'high',
         'reuse_evidence': {'level': 'inferred', 'tasks': ['forecasting_prediction'], 'basis': 'module'},
         'evidence': [{'locator': 'PDF p.1; source text L3', 'quote': 'q'}]}
    m.update(kw)
    m['function_view'] = {'functions': m['functions'], 'view_status': m['view_status'], 'evidence_indices': [0]}
    return m


class SchemaTests(unittest.TestCase):
    def test_five_dimensions(self):
        self.assertEqual(len(DIMENSIONS), 5)
        self.assertTrue(set(RETIRED_DIMENSIONS).isdisjoint(DIMENSIONS))

    def test_retired_dimension_rejected(self):
        for label in RETIRED_DIMENSIONS:
            m = module(dimensions=[label])
            with self.assertRaisesRegex(ValueError, 'retired dimension'):
                manager.reviewed_module_record({'citation_key': 'paper', 'reviewed_modules_json': json.dumps([m])})
            self.assertTrue(any('retired dimension' in e for e in module_errors(m, {})))

    def test_layer_field_rules(self):
        self.assertEqual(module_errors(module(), {}), [])
        self.assertTrue(module_errors(module(layer='GTS', view_status='mapped'), {}))  # GTS needs a function
        self.assertTrue(module_errors(module(layer='LLM', view_status='model_side'), {}))  # LLM: no dimension, a route
        ok = module(layer='LLM', dimensions=[], llm_route=['instruction_reasoning'], view_status='model_side',
                    reuse_evidence={'level': 'not_applicable'})
        self.assertEqual(module_errors(ok, {}), [])


class ImportTests(unittest.TestCase):
    def test_span_tags_cover_wrapped_quote(self):
        tagged = apply_reaudit.tokens_tagged([(10, 'The agent re-'), (11, 'trieves aligned events'), (12, 'later.')])
        self.assertEqual(apply_reaudit.find_span(tagged, 'agent retrieves aligned events'), (10, 11))
        self.assertIsNone(apply_reaudit.find_span(tagged, 'agent invents events'))

    def test_family_in_other_tasks_moves(self):
        self.assertEqual(apply_reaudit.split_tasks([], ['decision_support', 'question_answering']),
                         (['decision_support'], ['temporal_question_answering']))

    def test_evaluation_present_needs_quote(self):
        rows = manager.read_csv(manager.LEDGER)[:1]
        records = json.loads(manager.JSON_LEDGER.read_text())[:1]
        self.assertEqual(check(rows, records), [])
        ev = json.loads(rows[0]['evaluation_evidence_json'])
        ev['decision_utility'] = {'present': True, 'locator': None, 'quote': None}
        rows[0]['evaluation_evidence_json'] = json.dumps(ev)
        records[0] = copy.deepcopy(records[0]); records[0]['evaluation_evidence'] = ev
        self.assertTrue(any('decision_utility present without quote' in e for e in check(rows, records)))


if __name__ == '__main__':
    unittest.main()
