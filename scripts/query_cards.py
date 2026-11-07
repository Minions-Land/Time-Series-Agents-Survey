#!/usr/bin/env python3
"""Query the Paper Cards: an atomic lookup for people and coding agents. Read-only, standard library only.

Examples
  python3 scripts/query_cards.py --layer GTS --function context_memory          # shared temporal memory modules
  python3 scripts/query_cards.py --task anomaly_detection_diagnosis --layer TSK  # anomaly procedures
  python3 scripts/query_cards.py --text "information cutoff"                      # keyword over names, reasons, quotes
  python3 scripts/query_cards.py --work aion2026                                  # one full card
  python3 scripts/query_cards.py --role feedback_driven_agent --criterion temporal_validity --layer GTS
  python3 scripts/query_cards.py --stats                                          # counts by layer, function, task,
                                                                                  # role of work, evaluation criterion
Add --json for machine-readable output. Vocabulary: references/taxonomy_schema.json.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'paper_classification_ledger.json'


def modules(records):
    for r in records:
        mlc = r['module_level_contributions']
        if mlc.get('review_status') not in ('paper_verified', 'repository_verified'):
            continue
        for m in mlc.get('modules') or []:
            yield r, m


def functions(m):
    return m.get('functions') or (m.get('function_view') or {}).get('functions') or []


def retained(records):
    return [r for r in records if r['module_level_contributions'].get('review_status') in ('paper_verified', 'repository_verified')]


def criteria(r):
    return [k for k, v in (r.get('evaluation_evidence') or {}).items() if v.get('present')]


def matches(r, m, a):
    fv = functions(m)
    tasks = (m.get('tasks') or []) + (m.get('other_tasks') or [])
    if a.layer and m['layer'] != a.layer: return False
    if a.function and a.function not in fv: return False
    if a.task and a.task not in tasks: return False
    if a.dimension and not any(a.dimension.lower() in d.lower() for d in m.get('dimensions') or []): return False
    if a.reuse and (m.get('reuse_evidence') or {}).get('level') != a.reuse: return False
    if a.role and r.get('role_of_work') != a.role: return False
    if a.criterion and a.criterion not in criteria(r): return False
    if a.text:
        blob = ' '.join([r['citation']['title'], m['name'], m.get('scope_reason', '')] +
                        [e.get('quote', '') for e in m.get('evidence', [])]).lower()
        if a.text.lower() not in blob: return False
    return True


def row(r, m):
    ev = (m.get('evidence') or [{}])[0]
    return {'work': r['citation']['key'], 'title': r['citation']['title'], 'year': r['citation'].get('year'),
            'arxiv': r['citation'].get('arxiv_id'), 'module_id': m['id'], 'module': m['name'], 'layer': m['layer'],
            'dimensions': m.get('dimensions'), 'functions': functions(m), 'llm_route': m.get('llm_route'),
            'role_of_work': r.get('role_of_work'), 'confidence': m.get('confidence'),
            'tasks': (m.get('tasks') or []) + (m.get('other_tasks') or []),
            'reuse': (m.get('reuse_evidence') or {}).get('level'), 'scope_reason': m.get('scope_reason'),
            'evidence': {'locator': ev.get('locator'), 'quote': (ev.get('quote') or '')[:240]}}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--layer', choices=['LLM', 'GH', 'GTS', 'TSK'])
    p.add_argument('--function', choices=['data_management', 'processing', 'context_memory', 'validation'])
    p.add_argument('--task', help='e.g. forecasting_prediction, anomaly_detection_diagnosis, decision_support')
    p.add_argument('--dimension', help='substring of a mechanism dimension, e.g. "Memory"')
    p.add_argument('--reuse', choices=['demonstrated', 'inferred'])
    p.add_argument('--role', choices=['llm_side_technique', 'fixed_workflow', 'feedback_driven_agent', 'resource'],
                   help='role_of_work of the whole work')
    p.add_argument('--criterion', choices=['process_validity', 'temporal_validity', 'task_performance', 'decision_utility'],
                   help='work reports evidence for this evaluation criterion')
    p.add_argument('--text', help='case-insensitive keyword')
    p.add_argument('--work', help='citation key: print the whole card')
    p.add_argument('--stats', action='store_true')
    p.add_argument('--json', action='store_true')
    p.add_argument('--limit', type=int, default=50)
    a = p.parse_args()
    records = json.loads(LEDGER.read_text())
    if a.work:
        card = next((r for r in records if r['citation']['key'] == a.work), None)
        if not card: sys.exit(f'no work {a.work}')
        print(json.dumps(card, ensure_ascii=False, indent=1)); return
    if a.stats:
        ms, works = list(modules(records)), retained(records)
        out = {'records': len(records), 'works_in_scope': len(works),
               'excluded': Counter(r['module_level_contributions'].get('review_status') for r in records if r not in works),
               'modules': len(ms),
               'by_layer': Counter(m['layer'] for _, m in ms),
               'by_dimension': Counter(d for _, m in ms for d in m.get('dimensions') or []),
               'by_function': Counter(f for _, m in ms for f in functions(m)),
               'by_function_and_layer': Counter(f'{m["layer"]}:{f}' for _, m in ms for f in functions(m)),
               'by_llm_route': Counter(x for _, m in ms for x in m.get('llm_route') or []),
               'by_task': Counter(t for _, m in ms for t in m.get('tasks') or []),
               'by_task_and_layer': Counter(f'{t}:{m["layer"]}' for _, m in ms for t in m.get('tasks') or []),
               'by_other_task': Counter(t for _, m in ms for t in m.get('other_tasks') or []),
               'reuse_gh_gts': Counter(f'{m["layer"]}:{(m.get("reuse_evidence") or {}).get("level")}' for _, m in ms
                                       if m['layer'] in ('GH', 'GTS')),
               'works_by_role_of_work': Counter(r.get('role_of_work') for r in works),
               'works_by_task': Counter(t for r in works for t in r['tasks']['axes']),
               'works_by_evaluation_criterion': Counter(c for r in works for c in criteria(r))}
        out = {k: dict(sorted(v.items(), key=lambda x: (-x[1], x[0]))) if isinstance(v, Counter) else v for k, v in out.items()}
        print(json.dumps(out, indent=1)); return
    hits = [row(r, m) for r, m in modules(records) if matches(r, m, a)]
    if a.json:
        print(json.dumps(hits[:a.limit], ensure_ascii=False, indent=1))
    else:
        for h in hits[:a.limit]:
            print(f"[{h['layer']}] {h['module']}  ({h['work']}, {h['year']})  {h['evidence']['locator'] or ''}")
        print(f'{len(hits)} module(s){" (showing %d)" % a.limit if len(hits) > a.limit else ""}')


if __name__ == '__main__':
    main()
