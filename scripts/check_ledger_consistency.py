"""Read-only validation of the maintained CSV, published JSON and source-attributed resources."""
import json
from collections import Counter
from urllib.parse import urlsplit
import classification_manager as manager
from ledger_schema import SCHEMA_VERSION, SCHEMA, canonical_task

def check(rows, records):
    errors=[]; bykey={r['citation']['key']:r for r in records}; ids=[]
    if len(bykey)!=len(records): errors.append('Duplicate JSON citation key')
    if {r['citation_key'] for r in rows}!=set(bykey): errors.append('CSV/JSON record keys differ')
    for row in rows:
        key=row['citation_key']; record=bykey[key]
        if row['taxonomy_schema_version']!=SCHEMA_VERSION or record['schema_version']!=SCHEMA_VERSION:
            errors.append(f'{key}: schema mismatch')
        modules=json.loads(row['reviewed_modules_json'])
        if modules!=record['module_level_contributions']['modules']: errors.append(f'{key}: module projection differs')
        try: manager.reviewed_module_record(row)
        except (ValueError,KeyError) as exc: errors.append(str(exc))
        for module in modules:
            ids.append(module['id'])
            for value in module.get('tasks',[])+module.get('other_tasks',[]):
                if canonical_task(value)!=value:errors.append(f'{module["id"]}: stale task alias {value}')
            view=module.get('function_view',{})
            expected_status={'LLM':'model_side','GH':'general_runtime'}.get(module['layer'])
            if expected_status and (view.get('view_status')!=expected_status or view.get('functions')):
                errors.append(f'{module["id"]}: layer and function applicability conflict')
            if module['layer'] in {'GTS','TSK'} and view.get('view_status') in {'model_side','general_runtime'}:
                errors.append(f'{module["id"]}: stale function applicability')
            if not set(module.get('tasks',[])+module.get('other_tasks',[]))<=set(record['tasks']['axes']+record['tasks']['other_labels']):
                errors.append(f'{module["id"]}: task absent from work memberships')
            if any(i<0 or i>=len(module['evidence']) for i in view.get('evidence_indices',[])):
                errors.append(f'{module["id"]}: invalid evidence index')
        for value in record['tasks']['axes']+record['tasks']['other_labels']:
            if canonical_task(value)!=value:errors.append(f'{key}: stale work task alias')
        resources=json.loads(row.get('official_resources_json') or '[]')
        if resources!=record['official_resources']:errors.append(f'{key}: resource projection differs')
        seen=set()
        for resource in resources:
            url=resource.get('url',''); provenance=resource.get('provenance',{})
            if resource.get('kind') not in SCHEMA['official_resources']['kinds']:errors.append(f'{key}: unknown resource kind')
            if resource.get('availability',{}).get('status') not in {'reachable','http_error','landing_shell_reachable','fetch_failed'}:errors.append(f'{key}: unknown availability status')
            if url in seen:errors.append(f'{key}: duplicate resource {url}')
            seen.add(url)
            if urlsplit(url).scheme not in ('http','https'): errors.append(f'{key}: invalid resource URL')
            if not provenance or not provenance.get('locator') or not provenance.get('source_path'):
                errors.append(f'{key}: missing resource attribution {url}')
        if record['claimed_as_agent']!=(row['claimed_as_agent']=='Yes'):errors.append(f'{key}: Agent flag differs')
    if len(ids)!=len(set(ids)):errors.append('Duplicate module IDs')
    return errors

if __name__=='__main__':
    rows=manager.read_csv(manager.LEDGER);records=json.loads(manager.JSON_LEDGER.read_text())
    errors=check(rows,records)
    print(json.dumps({'records':len(rows),'modules':sum(len(r['module_level_contributions']['modules']) for r in records),'layers':dict(Counter(m['layer'] for r in records for m in r['module_level_contributions']['modules'])),'errors':errors},indent=2))
    raise SystemExit(bool(errors))
