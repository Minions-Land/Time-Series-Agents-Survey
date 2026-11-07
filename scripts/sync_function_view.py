"""Attach the curated temporal-function reading view without changing module scope.

The reviewed CSV remains authoritative. The mapping is an explicitly reviewed
annotation keyed by module id, not keyword inference; coverage decisions include
non-applicability. Since the 2026-11-07 re-audit the mapping is generated from
the adjudicated records (scripts/apply_reaudit.py) and must agree with each
module's own `functions` and `view_status`.

usage: python3 scripts/sync_function_view.py [--mapping PATH]
"""
import argparse,csv,json
from ledger_schema import FUNCTIONS, LAYER_VIEW_STATUS, SCHEMA_VERSION
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAPPING=ROOT/'references/reviews/20261106_terra_reaudit/module_function_mapping.json'

def apply_view(rows, mapping):
    assignments=mapping['assignments']; seen=set()
    for row in rows:
        modules=json.loads(row.get('reviewed_modules_json') or '[]')
        for m in modules:
            mid=m['id'];seen.add(mid)
            if mid not in assignments:raise ValueError(f'Missing function decision: {mid}')
            a=assignments[mid]
            if set(a['functions'])-set(FUNCTIONS):raise ValueError(f'Unknown function: {mid}')
            if any(i<0 or i>=len(m['evidence']) for i in a['evidence_indices']):raise ValueError(f'Invalid evidence index: {mid}')
            if m['layer'] in {'GH','LLM'} and a['functions']:raise ValueError(f'Temporal functions inferred for {m["layer"]}: {mid}')
            if a['view_status'] not in LAYER_VIEW_STATUS[m['layer']]:raise ValueError(f'View status {a["view_status"]} not allowed for {m["layer"]}: {mid}')
            if m['layer']=='GTS' and not a['functions']:raise ValueError(f'GTS module without temporal function: {mid}')
            for field in ('functions','view_status'):
                if field in m and m[field]!=a[field]:raise ValueError(f'Function map disagrees with module {field}: {mid}')
            m['function_view']=a
        row['reviewed_modules_json']=json.dumps(modules,ensure_ascii=False)
        row['taxonomy_schema_version']=SCHEMA_VERSION
    if seen != assignments.keys():raise ValueError('Stale module IDs in function map')
    return rows

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--mapping',type=Path,default=MAPPING)
    a=ap.parse_args()
    p=ROOT/'paper_classification_ledger.csv'
    with p.open() as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
    rows=apply_view(rows,json.loads(a.mapping.read_text()))
    tmp=p.with_suffix('.csv.tmp')
    with tmp.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
    tmp.replace(p)
    print('Attached reviewed function view; original module IDs, roles, tasks and layers preserved.')
