"""Attach the curated temporal-function reading view without changing module scope.

The reviewed CSV remains authoritative. The mapping is an explicitly reviewed
annotation, not keyword inference; coverage decisions include non-applicability.
"""
import csv,json
from ledger_schema import SCHEMA_VERSION
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAPPING=ROOT/'references/reviews/20261016_boundary_audit/module_function_mapping.json'

def apply_view(rows, mapping):
    assignments=mapping['assignments']; seen=set()
    for row in rows:
        modules=json.loads(row.get('reviewed_modules_json') or '[]')
        for m in modules:
            mid=m['id'];seen.add(mid)
            if mid not in assignments:raise ValueError(f'Missing function decision: {mid}')
            a=assignments[mid]
            if set(a['functions'])-mapping['functions'].keys():raise ValueError(f'Unknown function: {mid}')
            if any(i<0 or i>=len(m['evidence']) for i in a['evidence_indices']):raise ValueError(f'Invalid evidence index: {mid}')
            if m['layer'] in {'GH','LLM'} and a['functions']:raise ValueError(f'Temporal functions inferred for {m["layer"]}: {mid}')
            m['function_view']=a
        row['reviewed_modules_json']=json.dumps(modules,ensure_ascii=False)
        row['taxonomy_schema_version']=SCHEMA_VERSION
    if seen != assignments.keys():raise ValueError('Stale module IDs in function map')
    return rows

if __name__=='__main__':
    p=ROOT/'paper_classification_ledger.csv'
    with p.open() as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
    rows=apply_view(rows,json.loads(MAPPING.read_text()))
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
    print('Attached reviewed function view; original module IDs, roles, tasks and layers preserved.')
