"""Build one packet (numbered source text) and one current-card file per ledger record.

usage: python3 make_packets.py            -> packets/<key>.txt, cards/<key>.json, keys_ready.txt, keys_missing.txt
Sources, in order: references/pdfs/<key>.pdf, references/source_snapshots/candidate_pdfs/<key>.pdf, then any existing
evidence source_path of the record (repository README or code for repository-verified resources).
"""
import json, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEDGER = ROOT / 'paper_classification_ledger.json'
CARD_FIELDS = ('id', 'name', 'layer', 'dimensions', 'tasks', 'other_tasks', 'role', 'scope_reason', 'reuse_evidence')


def source_for(rec):
    key = rec['citation']['key']
    for p in (ROOT / f'references/pdfs/{key}.pdf', ROOT / f'references/source_snapshots/candidate_pdfs/{key}.pdf'):
        if p.exists(): return p
    paths = {e.get('source_path') for m in rec['module_level_contributions'].get('modules') or [] for e in m.get('evidence', [])}
    for sp in sorted(p for p in paths if p):
        p = ROOT / sp
        if p.exists() and p.suffix.lower() != '.pdf': return p
    return None


def text_of(path):
    if path.suffix.lower() == '.pdf':
        out = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(path), '-'], capture_output=True, text=True).stdout
    else:
        out = path.read_text(errors='replace')
    lines = [re.sub(r'\s+', ' ', ln).strip() for ln in out.replace('\f', '\n').splitlines()]
    return [ln for ln in lines if ln]


def card_of(rec):
    mlc = rec['module_level_contributions']
    mods = []
    for m in mlc.get('modules') or []:
        d = {k: m.get(k) for k in CARD_FIELDS if k in m}
        fv = m.get('function_view') or {}
        d['functions'] = fv.get('functions', []); d['view_status'] = fv.get('view_status')
        d['evidence_locators'] = [e.get('locator') for e in m.get('evidence', [])][:3]
        mods.append(d)
    return {'citation_key': rec['citation']['key'], 'title': rec['citation'].get('title'),
            'review_status': mlc.get('review_status'), 'work_type': rec.get('work_type'),
            'claim': rec.get('claim'), 'tasks': rec.get('tasks'), 'modules': mods}


def main():
    recs = json.loads(LEDGER.read_text())
    for d in ('packets', 'cards', 'out', 'logs'): (HERE / d).mkdir(exist_ok=True)
    ready, missing = [], []
    for rec in recs:
        key = rec['citation']['key']
        (HERE / 'cards' / f'{key}.json').write_text(json.dumps(card_of(rec), ensure_ascii=False, indent=1))
        src = source_for(rec)
        if not src:
            missing.append(key); continue
        lines = text_of(src)
        head = [f'KEY: {key}', f'TITLE: {rec["citation"].get("title", "")}', f'SOURCE: {src.relative_to(ROOT)}', '']
        body = [f'L{i}: {ln}' for i, ln in enumerate(lines, 1)]
        (HERE / 'packets' / f'{key}.txt').write_text('\n'.join(head + body) + '\n')
        ready.append(key)
    (HERE / 'keys_ready.txt').write_text('\n'.join(ready) + '\n')
    (HERE / 'keys_missing.txt').write_text('\n'.join(missing) + '\n')
    print(f'packets {len(ready)}, missing source {len(missing)}')


if __name__ == '__main__':
    main()
