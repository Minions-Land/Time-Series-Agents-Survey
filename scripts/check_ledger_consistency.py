"""Read-only validation of the maintained CSV, published JSON and source-attributed resources."""
import json
from collections import Counter
from urllib.parse import urlsplit
import classification_manager as manager
from ledger_schema import (CONFIDENCE, EVALUATION_CRITERIA, FUNCTIONS, LAYER_VIEW_STATUS, LLM_ROUTES, MODULE_ROLES,
                           ROLES_OF_WORK, SCHEMA, SCHEMA_VERSION, canonical_task, dimension_errors)

RETAINED = {'paper_verified', 'repository_verified'}


def module_errors(module, row):
    """Vocabulary and per-layer field rules of the five-dimension schema (rubric R2-R9)."""
    mid, layer, errors = module['id'], module['layer'], []
    errors += [f'{mid}: {e}' for e in dimension_errors(module.get('dimensions', []))]
    if layer == 'LLM':
        if module.get('dimensions'): errors.append(f'{mid}: LLM-side module with mechanism dimensions')
        if not module.get('llm_route') or set(module['llm_route']) - set(LLM_ROUTES): errors.append(f'{mid}: invalid llm_route')
    else:
        if not module.get('dimensions'): errors.append(f'{mid}: Harness module without dimension')
        if module.get('llm_route'): errors.append(f'{mid}: llm_route on a Harness module')
    functions = module.get('functions', [])
    if set(functions) - set(FUNCTIONS): errors.append(f'{mid}: unknown temporal function')
    if layer in {'GH', 'LLM'} and functions: errors.append(f'{mid}: temporal function on {layer}')
    if layer == 'GTS' and not functions: errors.append(f'{mid}: GTS module without temporal function')
    if module.get('view_status') not in LAYER_VIEW_STATUS[layer]: errors.append(f'{mid}: view_status not allowed for {layer}')
    if module.get('role') not in MODULE_ROLES: errors.append(f'{mid}: unknown role')
    if module.get('confidence') not in CONFIDENCE: errors.append(f'{mid}: unknown confidence')
    if not module.get('rubric_path'): errors.append(f'{mid}: missing rubric_path')
    if layer == 'TSK' and not (module.get('tasks') or module.get('other_tasks')): errors.append(f'{mid}: TSK module without task')
    view = module.get('function_view', {})
    if view.get('functions') != functions or view.get('view_status') != module.get('view_status'):
        errors.append(f'{mid}: function view differs from module functions/view_status')
    if any(i < 0 or i >= len(module['evidence']) for i in view.get('evidence_indices', [])):
        errors.append(f'{mid}: invalid evidence index')
    for ev in module['evidence']:
        if not ev.get('locator') or not ev.get('quote'): errors.append(f'{mid}: evidence without locator or quote')
    reuse = module.get('reuse_evidence', {})
    expected = {'demonstrated', 'inferred'} if layer in {'GH', 'GTS'} else {'not_applicable'}
    if reuse.get('level') == 'demonstrated':
        # The level must rest on at least two recorded task values (module tasks, else work tasks).
        recorded = module.get('tasks', []) + module.get('other_tasks', [])
        if reuse.get('basis') == 'work' or not recorded:
            recorded = [n for n in manager.TASK_AXES if row.get(f'task_axis_{n}') == 'Yes'] + row['task_axis_other'].split(';')
        if len({canonical_task(t.strip()) for t in recorded + reuse.get('tasks', []) if t.strip()}) < 2:
            errors.append(f'{mid}: demonstrated reuse with fewer than two recorded tasks')
    if reuse.get('level') not in expected: errors.append(f'{mid}: invalid reuse evidence')
    return errors


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
        status=row.get('taxonomy_review_status')
        if status in RETAINED and not modules: errors.append(f'{key}: retained record without modules')
        if status not in RETAINED and modules: errors.append(f'{key}: excluded record with modules')
        if status=='out_of_scope' and row.get('included_as')!='background_reference':
            errors.append(f'{key}: out-of-scope record not marked background_reference')
        if row.get('role_of_work') not in ROLES_OF_WORK: errors.append(f'{key}: unknown role_of_work')
        if record.get('role_of_work')!=row.get('role_of_work'): errors.append(f'{key}: role_of_work projection differs')
        evaluation=json.loads(row.get('evaluation_evidence_json') or '{}')
        if set(evaluation)!=set(EVALUATION_CRITERIA): errors.append(f'{key}: evaluation evidence must list the four criteria')
        for name,item in evaluation.items():
            if item.get('present') is True and not (item.get('quote') and item.get('locator')):
                errors.append(f'{key}: {name} present without quote and locator')
            if item.get('present') is not True and (item.get('present') is not False or item.get('quote')):
                errors.append(f'{key}: {name} absent but carries evidence')
        if record.get('evaluation_evidence')!=evaluation: errors.append(f'{key}: evaluation evidence projection differs')
        for ev in json.loads(row.get('claim_evidence_json') or '[]'):
            if not ev.get('locator') or not ev.get('quote'): errors.append(f'{key}: claim evidence without locator or quote')
        impact=row.get('task_impact_json') or ''
        if impact and not isinstance(json.loads(impact),dict): errors.append(f'{key}: task_impact_json is not an object')
        for module in modules:
            ids.append(module['id'])
            errors += module_errors(module, row)
            for value in module.get('tasks',[])+module.get('other_tasks',[]):
                if canonical_task(value)!=value:errors.append(f'{module["id"]}: stale task alias {value}')
            if not set(module.get('tasks',[])+module.get('other_tasks',[]))<=set(record['tasks']['axes']+record['tasks']['other_labels']):
                errors.append(f'{module["id"]}: task absent from work memberships')
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
