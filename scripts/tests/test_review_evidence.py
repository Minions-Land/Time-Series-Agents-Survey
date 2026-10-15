"""Evidence transcription checks reject paraphrases and misplaced locators."""
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('audit',Path(__file__).resolve().parents[1]/'audit_review_evidence.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
class EvidenceTests(unittest.TestCase):
 def test_typography_only_normalization(self):
  r=audit.check_quote({'quote':'The fine-grained model uses aligned observations.', 'locator':'PDF p.1; section 3'}, {'pages':['The ﬁne-grained model uses aligned\nobservations.']})
  self.assertEqual(r['status'],'matched')
 def test_wrong_page_is_not_approved(self):
  r=audit.check_quote({'quote':'The model uses aligned observations.', 'locator':'PDF p.1'}, {'pages':['Title','The model uses aligned observations.']})
  self.assertEqual(r['status'],'locator_mismatch');self.assertEqual(r['matching_pages'],[2])
 def test_paraphrase_is_not_a_quote(self):
  r=audit.check_quote({'quote':'The model guarantees temporal consistency.', 'locator':'PDF p.1'}, {'pages':['The model uses aligned observations.']})
  self.assertEqual(r['status'],'quote_not_found')
if __name__=='__main__':unittest.main()
