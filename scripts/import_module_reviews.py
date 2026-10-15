"""Apply adjudicated primary-source reviews to the maintained CSV.

Only records in review files are changed. Bibliographic titles/authors are
reported for separate verification, never silently replaced from a review.
"""
import csv
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT/'references/reviews/20261015_full_audit'
TASK_FIELDS = {'forecasting_prediction':'forecasting_reasoning',
               'data_augmentation_synthesis':'augmentation_synthesis',
               'anomaly_detection_diagnosis':'anomaly_detection_diagnosis',
               'decision_support':'decision_support'}

def apply_review(row, r):
    mods = r['modules']
    status = r['status']
    if status not in {'paper_verified', 'repository_verified', 'out_of_scope', 'blocked'}:
        raise ValueError(status)
    if status in {'out_of_scope', 'blocked'} and mods:
        raise ValueError('Unverified/out-of-scope modules: '+r['citation_key'])
    row['reviewed_modules_json'] = json.dumps(mods, ensure_ascii=False)
    row['taxonomy_review_status'] = status
    row['claim_review_status'] = status if status!='out_of_scope' else 'paper_verified'
    row['paper_claim_summary'] = r['claim_summary']
    row['claim_evidence_basis'] = 'primary_source_module_review_20261015'
    row['included_as'] = {'out_of_scope':'background_reference', 'blocked':'pending_evidence'}.get(status,'reviewed_contribution')
    row['review_audit_json'] = json.dumps({k:v for k,v in r.items() if k!='modules'}, ensure_ascii=False)
    evidence = [e for m in mods for e in m['evidence']] + r.get('source_evidence', []) + r.get('scope_evidence', [])
    row['source_evidence_json'] = json.dumps(evidence, ensure_ascii=False)
    for layer, field in [('LLM','llm_component_contribution'),('GH','general_harness_contribution'),('GTS','general_ts_harness_contribution'),('TSK','task_specific_harness_contribution')]:
        row[field] = '; '.join(m['name'] for m in mods if m['layer']==layer)
    row['llm_side_subdimensions'] = json.dumps([m['name'] for m in mods if m['layer']=='LLM'],ensure_ascii=False)
    layers = Counter(m['layer'] for m in mods)
    row['primary_locus'] = max(layers, key=lambda k:(layers[k],['GH','GTS','TSK','LLM'].index(k))) if layers else 'NONE'
    row['primary_contribution'] = r['claim_summary']
    tasks = set(r.get('task_memberships', []))
    other = set(r.get('other_tasks', []) + r.get('other_task_memberships', []))
    for m in mods:
        tasks.update(m.get('tasks', []));other.update(m.get('other_tasks', []))
    other.update(tasks-set(TASK_FIELDS));tasks.intersection_update(TASK_FIELDS)
    for task, legacy in TASK_FIELDS.items():
        row['task_axis_'+legacy] = 'Yes' if task in tasks else 'No'
    row['task_axis_other'] = '; '.join(sorted(other))
    row['task_axis_notes'] = 'Primary-source task contracts; labels beyond the four main families remain values of the same task coordinate.'
    row['harness_module_coding_basis'] = 'primary_source_module_review'
    row['harness_modules'] = '; '.join(sorted({d for m in mods if m['layer']!='LLM' for d in m.get('dimensions', [])}))
    row['classification_notes'] = ' '.join(r.get('corrections', []))
    # Remove old inferred projections; sync regenerates the reviewed ID views.
    for field in ['general_harness_dimensions','general_ts_harness_dimensions','task_specific_modules_json','module_level_contributions_json']:
        row[field] = ''
    row['general_ts_specificity_reason'] = json.dumps([m['scope_reason'] for m in mods if m['layer']=='GTS'],ensure_ascii=False)
    return row

if __name__ == '__main__':
    path=ROOT/'paper_classification_ledger.csv'
    with path.open() as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
    if 'review_audit_json' not in fields:fields.append('review_audit_json')
    reviews={}
    for p in sorted(FOLDER.glob('shard_*_review.json')):
        for r in json.loads(p.read_text()):
            if r['citation_key'] in reviews:raise ValueError('Duplicate review')
            reviews[r['citation_key']]=r
    for row in rows:
        if row['citation_key'] in reviews:apply_review(row,reviews[row['citation_key']])
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
    print('Applied',len(reviews),'reviews:',dict(Counter(r['status'] for r in reviews.values())))
