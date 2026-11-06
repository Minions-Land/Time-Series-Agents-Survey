#!/usr/bin/env python3
"""Rebuild references/pdf_manifest.csv, or fetch the reviewed PDFs it lists.

The original PDFs are not redistributed in this repository (their licences belong to the authors). The manifest
records each card's source URL and the SHA-256 of the copy that was reviewed, so a local copy can be fetched and
checked against the one the evidence quotes come from.

  python3 scripts/fetch_pdfs.py --manifest      # rebuild the manifest from the ledger and local PDFs
  python3 scripts/fetch_pdfs.py --fetch         # download missing arXiv PDFs into references/pdfs/ and verify hashes
"""
import argparse, csv, hashlib, json, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDFS = ROOT / 'references' / 'pdfs'
MANIFEST = ROOT / 'references' / 'pdf_manifest.csv'


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()


def build():
    rows = []
    for r in json.loads((ROOT / 'paper_classification_ledger.json').read_text()):
        c = r['citation']; k = c['key']; p = PDFS / f'{k}.pdf'
        url = f"https://arxiv.org/pdf/{c['arxiv_id']}" if c.get('arxiv_id') else (f"https://doi.org/{c['doi']}" if c.get('doi') else c.get('landing_url') or '')
        rows.append({'key': k, 'title': c['title'], 'arxiv_id': c.get('arxiv_id') or '', 'url': url,
                     'sha256': sha256(p) if p.exists() else '', 'bytes': p.stat().st_size if p.exists() else ''})
    with MANIFEST.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    print(f'{MANIFEST.relative_to(ROOT)}: {len(rows)} works, {sum(1 for r in rows if r["sha256"])} with a reviewed-copy hash')


def fetch():
    PDFS.mkdir(parents=True, exist_ok=True)
    for row in csv.DictReader(MANIFEST.open()):
        p = PDFS / f"{row['key']}.pdf"
        if p.exists() or not row['arxiv_id']: continue
        req = urllib.request.Request(row['url'], headers={'User-Agent': 'time-series-agents-survey/1.0'})
        try:
            p.write_bytes(urllib.request.urlopen(req, timeout=300).read())
        except Exception as e:
            print('failed', row['key'], e); continue
        ok = not row['sha256'] or sha256(p) == row['sha256']
        print(('ok' if ok else 'hash differs (another arXiv version?)'), row['key'])
        time.sleep(3)


if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('--manifest', action='store_true'); a.add_argument('--fetch', action='store_true')
    args = a.parse_args()
    if args.manifest or not args.fetch: build()
    if args.fetch: fetch()
