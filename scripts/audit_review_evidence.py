"""Check review quotes against page-indexed primary-source text.

This is a transcription/locator check, not a semantic endorsement of a claim.
Only typography (Unicode, spacing, extraction hyphens) is normalized. Missing
quotes and wrong-page matches remain explicit failures for human adjudication.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def normalize(text):
    text = unicodedata.normalize('NFKC', text).replace('\u00ad', '')
    # PDF extraction can place a space or a newline after a hyphenated word.
    text = re.sub(r'(?<=\w)[-‐‑]\s+(?=\w)', '', text)
    text = text.translate(str.maketrans({'’': "'", '‘': "'", '“': '"', '”': '"', '–': '-', '—': '-'}))
    return re.sub(r'\s+', '', text)

def check_quote(evidence, cache):
    quote = normalize(evidence.get('quote', ''))
    if len(quote) < 15:
        return {'status': 'missing_or_short_quote'}
    pages = cache.get('pages', [])
    matches = [i+1 for i, page in enumerate(pages) if quote in normalize(page)]
    loc = evidence.get('locator', '')
    page_match = re.search(r'(?:PDF\s*)?p(?:age)?\.?\s*(\d+)', loc, re.I)
    declared = int(page_match.group(1)) if page_match else None
    if matches:
        return {'status': 'matched' if declared in matches else 'locator_mismatch',
                'declared_page': declared, 'matching_pages': matches}
    return {'status': 'quote_not_found', 'declared_page': declared}

def audit(paths):
    results = []
    for path in paths:
        records = json.loads(path.read_text())
        for r in records:
            extra = r.get('source_evidence', []) + r.get('scope_evidence', [])
            modules = r.get('modules', []) + ([{'id': r['citation_key']+':scope', 'evidence':extra}] if extra else [])
            for m in modules:
                for n, ev in enumerate(m.get('evidence', [])):
                    source = ev.get('source_path', '')
                    cache_path = ROOT / 'tmp/full_audit_sources' / (Path(source).stem + '.json')
                    if not cache_path.exists():
                        path_source = ROOT/source
                        if source and path_source.is_file():
                            result = {'status': 'matched_repository' if normalize(ev.get('quote','')) in normalize(path_source.read_text()) else 'quote_not_found'}
                        else:
                            result = {'status': 'non_pdf_source_requires_review'}
                    else:
                        result = check_quote(ev, json.loads(cache_path.read_text()))
                    results.append({'review_file': str(path.relative_to(ROOT)),
                                    'citation_key': r['citation_key'], 'module_id': m['id'],
                                    'evidence_index': n, **result})
    return results

if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('files', nargs='*');a=p.parse_args()
    paths = [Path(f).resolve() for f in a.files] if a.files else sorted((ROOT/'references/reviews/20261015_full_audit').glob('shard_*_review.json')) + [ROOT/'references/reviews/20261015_full_audit/initial_9_review.json']
    result = audit(paths)
    out = ROOT/'references/reviews/20261015_full_audit/evidence_check.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    from collections import Counter
    print(dict(Counter(x['status'] for x in result)))
