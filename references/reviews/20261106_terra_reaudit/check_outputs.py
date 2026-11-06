"""Validate re-audit outputs and report how they differ from the current Paper Cards. Read-only on inputs.

usage: python3 check_outputs.py   -> check_report.md, changes.csv (one row per module decision)
Checks: closed vocabulary, required fields per layer, every quote verbatim in the packet (line-4 .. line+8, whitespace
normalised), and agreement between the blind pass and the final record.
"""
import csv, json, re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAYERS = {'LLM', 'GH', 'GTS', 'TSK'}
DIMS = {'Interface and Interaction', 'Memory and Context', 'Tools and Execution', 'Planning and Orchestration',
        'Optimization and Evolution'}
FUNCS = {'data_management', 'processing', 'context_memory', 'validation'}
VIEWS = {'mapped', 'task_procedure', 'general_runtime', 'model_side', 'resource_level'}
ROUTES = {'representation_alignment', 'instruction_reasoning', 'workflow_learning'}
TASKS = {'forecasting_prediction', 'data_augmentation_synthesis', 'anomaly_detection_diagnosis', 'decision_support'}
ROLES = {'method', 'model_training', 'training_data', 'infrastructure', 'evaluation'}
STATUS = {'paper_verified', 'repository_verified', 'out_of_scope', 'blocked'}
WORK_ROLES = {'llm_side_technique', 'fixed_workflow', 'feedback_driven_agent', 'resource', 'background'}
EVAL = ('process_validity', 'temporal_validity', 'task_performance', 'decision_utility')
norm = lambda s: re.sub(r'\s+', ' ', s or '').strip().lower()


def packet_lines(key):
    lines = {}
    for ln in (HERE / 'packets' / f'{key}.txt').read_text().splitlines():
        m = re.match(r'L(\d+): (.*)', ln)
        if m: lines[int(m.group(1))] = m.group(2)
    return lines


def quote_ok(lines, line, quote):
    if not isinstance(line, int) or not quote: return False
    window = norm(' '.join(lines.get(i, '') for i in range(line - 4, line + 9)))   # tolerate a cited line a few lines off
    q = norm(quote)
    return q in window or q.replace('- ', '') in window.replace('- ', '')


def check(rec, lines):
    errs = []
    if rec.get('status') not in STATUS: errs.append('status')
    if rec.get('role_of_work') not in WORK_ROLES: errs.append('role_of_work')
    for e in rec.get('claim_evidence') or []:
        if not quote_ok(lines, e.get('line'), e.get('quote')): errs.append('claim quote L%s' % e.get('line'))
    if rec.get('status') in ('paper_verified', 'repository_verified') and not rec.get('modules'): errs.append('no modules')
    for m in rec.get('modules') or []:
        mid = m.get('id', '?')
        L = m.get('layer')
        if L not in LAYERS: errs.append(f'{mid} layer'); continue
        if set(m.get('dimensions') or []) - DIMS: errs.append(f'{mid} dims {sorted(set(m["dimensions"]) - DIMS)}')
        if L != 'LLM' and not m.get('dimensions'): errs.append(f'{mid} no dimension')
        if L == 'LLM' and (m.get('dimensions') or not set(m.get('llm_route') or []) <= ROUTES or not m.get('llm_route')):
            errs.append(f'{mid} llm fields')
        if set(m.get('functions') or []) - FUNCS: errs.append(f'{mid} functions')
        if L == 'GTS' and not m.get('functions'): errs.append(f'{mid} GTS without function')
        if m.get('view_status') not in VIEWS: errs.append(f'{mid} view_status')
        if set(m.get('tasks') or []) - TASKS: errs.append(f'{mid} tasks')
        if L == 'TSK' and not (m.get('tasks') or m.get('other_tasks')): errs.append(f'{mid} TSK without task')
        if m.get('role') not in ROLES: errs.append(f'{mid} role')
        lvl = (m.get('reuse_evidence') or {}).get('level')
        if (L in ('GH', 'GTS')) != (lvl in ('demonstrated', 'inferred')): errs.append(f'{mid} reuse level')
        if not m.get('evidence'): errs.append(f'{mid} no evidence')
        for e in m.get('evidence') or []:
            if not quote_ok(lines, e.get('line'), e.get('quote')): errs.append(f'{mid} quote L{e.get("line")}')
    ev = rec.get('evaluation_evidence') or {}
    for k in EVAL:
        item = ev.get(k) or {}
        if item.get('present') and not quote_ok(lines, item.get('line'), item.get('quote')): errs.append(f'eval {k} quote')
    return errs


def main():
    rows, report, stats = [], [], Counter()
    layer_moves, dims_new, agree = Counter(), Counter(), Counter()
    finals = sorted(p for p in (HERE / 'out').glob('*.json') if not p.name.endswith('.blind.json'))
    for p in finals:
        key = p.stem
        try:
            rec = json.loads(p.read_text())
        except Exception as e:
            report.append(f'- `{key}`: invalid JSON ({e})'); stats['invalid'] += 1; continue
        lines = packet_lines(key)
        errs = check(rec, lines)
        stats['records'] += 1; stats['valid' if not errs else 'with_errors'] += 1
        if errs: report.append(f'- `{key}`: ' + '; '.join(errs[:8]) + (' ...' if len(errs) > 8 else ''))
        card = json.loads((HERE / 'cards' / f'{key}.json').read_text())
        old = {m['id']: m for m in card['modules']}
        new = {m['id']: m for m in rec.get('modules') or []}
        for d in rec.get('reconciliation') or []:
            o = old.get(d.get('existing_id'), {})
            n = [new[i] for i in d.get('new_ids') or [] if i in new]
            stats['decision_' + str(d.get('decision'))] += 1
            for m in n:
                if o and o.get('layer') != m.get('layer'): layer_moves[f"{o.get('layer')}->{m.get('layer')}"] += 1
            rows.append({'key': key, 'existing_id': d.get('existing_id'), 'decision': d.get('decision'),
                         'old_layer': o.get('layer', ''), 'new_layers': ' '.join(m['layer'] for m in n),
                         'old_dims': '; '.join(o.get('dimensions') or []),
                         'new_dims': ' | '.join('; '.join(m.get('dimensions') or []) for m in n),
                         'reason': d.get('reason', '')})
        for m in new.values():
            for x in m.get('dimensions') or []: dims_new[x] += 1
            stats['modules_' + m.get('layer', '?')] += 1
            if m['id'] not in old: stats['new_modules'] += 1
        if rec.get('needs_human_review'): stats['needs_human_review'] += 1
        for k in EVAL:
            if ((rec.get('evaluation_evidence') or {}).get(k) or {}).get('present'): stats['eval_' + k] += 1
        bp = HERE / 'out' / f'{key}.blind.json'
        if bp.exists():
            try:
                blind = {m.get('id'): m.get('layer') for m in json.loads(bp.read_text()).get('modules') or []}
                bl, fl = Counter(blind.values()), Counter(m.get('layer') for m in new.values())
                agree['same_layer_profile' if bl == fl else 'different_layer_profile'] += 1
            except Exception:
                agree['blind_unreadable'] += 1
    with (HERE / 'changes.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'existing_id', 'decision', 'old_layer', 'new_layers', 'old_dims', 'new_dims', 'reason'])
        w.writeheader(); w.writerows(rows)
    out = ['# Re-audit check report', '', f'Records: {stats["records"]} (valid {stats["valid"]}, with errors {stats["with_errors"]}, invalid JSON {stats["invalid"]}).',
           f'Module decisions: ' + ', '.join(f'{k[9:]} {v}' for k, v in sorted(stats.items()) if k.startswith('decision_')) + '.',
           f'Layer moves: {dict(layer_moves)}. New module ids: {stats["new_modules"]}.',
           'Final modules by layer: ' + ', '.join(f'{k[8:]} {v}' for k, v in sorted(stats.items()) if k.startswith('modules_')) + '.',
           f'Dimensions used: {dict(dims_new.most_common())}.',
           'Evaluation evidence present: ' + ', '.join(f'{k} {stats["eval_" + k]}' for k in EVAL) + '.',
           f'Needs human review: {stats["needs_human_review"]}. Blind vs final layer profile: {dict(agree)}.', '',
           '## Records with errors', ''] + (report or ['None.'])
    (HERE / 'check_report.md').write_text('\n'.join(out) + '\n')
    print('\n'.join(out[:9]))


if __name__ == '__main__':
    main()
