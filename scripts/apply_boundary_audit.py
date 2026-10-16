"""Apply independently adjudicated boundary reviews; preserve historical source records."""
import json
from collections import Counter
from pathlib import Path
import classification_manager as manager
from ledger_schema import SCHEMA_VERSION, canonical_tasks
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'references/reviews/20261016_boundary_audit'

def apply(rows, reviews, adjudications):
    bykey={r['citation_key']:r for r in reviews}
    for row in rows:
        key=row['citation_key'];review=bykey[key]
        modules=json.loads(row['reviewed_modules_json'])
        baseline_path=FOLDER/review['_file'].split('/')[-1].replace('shard_', 'assignment_')
        baseline=next(r for r in json.loads(baseline_path.read_text()) if r['citation']['key']==key)
        modules=baseline['module_level_contributions']['modules']
        decisions={m['id']:m for m in review['modules']}
        if set(decisions)!={m['id'] for m in modules}:
            raise ValueError(f'{key}: incomplete module review')
        final=[]
        for old in modules:
            decision=decisions[old['id']]
            judgment=adjudications.get(old['id'],{})
            if decision['decision']!='keep' and not judgment:
                raise ValueError(f'{old["id"]}: missing independent adjudication')
            action=judgment.get('action','keep')
            if action=='exclude':continue
            module=judgment.get('module') or (decision.get('proposed_module') if action=='change' else old)
            if module is None:raise ValueError(f'{old["id"]}: missing proposed module')
            if module['id']!=old['id']:raise ValueError('Module identity changed')
            for field in ('tasks','other_tasks'):
                if field in module:module[field]=canonical_tasks(module[field])
            final.append(module)
        row['reviewed_modules_json']=json.dumps(final,ensure_ascii=False)
        task_fields={'forecasting_prediction':'forecasting_reasoning','data_augmentation_synthesis':'augmentation_synthesis','anomaly_detection_diagnosis':'anomaly_detection_diagnosis','decision_support':'decision_support'}
        task_names={'forecasting_prediction':'Forecasting and prediction','data_augmentation_synthesis':'Data augmentation and synthesis','anomaly_detection_diagnosis':'Anomaly detection and diagnosis','decision_support':'Decision support'}
        for task in {t for m in final for t in m.get('tasks',[])}:
            if task in task_fields and row['task_axis_'+task_fields[task]]!='Yes':
                original=json.loads(row['task_aliases_source_json'])
                original.setdefault('source_label',row['task_family_original'])
                row['task_aliases_source_json']=json.dumps(original,ensure_ascii=False)
                row['task_axis_'+task_fields[task]]='Yes'
                row['task_family_original']+='; '+task_names[task]

        if modules and not final:
            row['taxonomy_review_status']='out_of_scope'
            row['included_as']='background_reference'
            note='Boundary review 2026-10-16: static grid violation remediation; retained as background rather than a temporal contribution.'
            if note not in row['classification_notes']:row['classification_notes']+=' '+note
        for layer,field in [('LLM','llm_component_contribution'),('GH','general_harness_contribution'),('GTS','general_ts_harness_contribution'),('TSK','task_specific_harness_contribution')]:
            row[field]='; '.join(m['name'] for m in final if m['layer']==layer)
        row['llm_side_subdimensions']=json.dumps([m['name'] for m in final if m['layer']=='LLM'],ensure_ascii=False)
        row['general_ts_specificity_reason']=json.dumps([m['scope_reason'] for m in final if m['layer']=='GTS'],ensure_ascii=False)
        row['harness_modules']='; '.join(sorted({d for m in final if m['layer']!='LLM' for d in m.get('dimensions',[])}))
        layers=Counter(m['layer'] for m in final)
        row['primary_locus']=max(layers,key=lambda k:(layers[k],['GH','GTS','TSK','LLM'].index(k))) if layers else 'NONE'
        for field in ['general_harness_dimensions','general_ts_harness_dimensions','task_specific_modules_json']:
            row[field]=''
        row['module_level_contributions_json']=json.dumps(manager.module_contribution_record(row),ensure_ascii=False)
        row['boundary_review_json']=json.dumps({'date':'2026-10-16','review_file':review['_file'],'reviewed_module_ids':list(decisions),'adjudication_file':'references/reviews/20261016_boundary_audit/adjudications.json','status':'reviewed'},ensure_ascii=False)
        resources=[]
        for entry in review.get('resource_links',[]):
            entry=json.loads(json.dumps(entry))
            kind=entry['kind'];entry['kind']={'code':'repository','evaluation':'benchmark'}.get(kind,kind)
            if entry['kind']!=kind:entry['source_kind']=kind
            availability=entry['availability']
            availability['checked_at']=availability.pop('checked_date',availability.get('checked_at','2026-10-16'))
            if 'resolved_url' in availability:availability['final_url']=availability.pop('resolved_url')
            if availability.get('http_status'):availability['http_status']=int(availability['http_status'])
            resources.append(entry)
        row['official_resources_json']=json.dumps(resources,ensure_ascii=False)
        row['resource_review_status']=review['resource_review_status']
        row['taxonomy_schema_version']=SCHEMA_VERSION
    return rows

if __name__=='__main__':
    reviews=[]
    for path in sorted(FOLDER.glob('shard_[123].json')):
        for record in json.loads(path.read_text()):
            record['_file']=str(path.relative_to(ROOT));reviews.append(record)
    if len({r['citation_key'] for r in reviews})!=len(reviews):raise ValueError('Duplicate records')
    rows=manager.read_csv(manager.LEDGER)
    if len(reviews)!=len(rows):raise ValueError('Incomplete corpus review')
    rows=apply(rows,reviews,json.loads((FOLDER/'adjudications.json').read_text()))
    manager.write_csv(rows);manager.generate_json(rows)
    print('Applied',len(rows),'reviewed records')
