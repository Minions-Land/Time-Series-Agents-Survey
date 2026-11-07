"""Validate task-impact records (rubric node R11) and summarize them. Read-only on inputs.

usage: python3 check_impact.py impact/<key>.json   -> print that record's errors (OK if none)
       python3 check_impact.py [impact_dir]          -> impact_report.md and impact.csv in that folder
"""
import csv, json, sys
from collections import Counter
from pathlib import Path

from check_outputs import packet_lines, quote_ok

HERE = Path(__file__).resolve().parent
FAMILIES = ('forecasting_prediction', 'data_augmentation_synthesis', 'anomaly_detection_diagnosis', 'decision_support')
PROBLEMS = {'information_availability', 'nonstationarity', 'data_quality', 'context_integration', 'decision_consequence',
            'verifiability', 'operational_deployment', 'other'}
GAINS = {'automation', 'metric_gain', 'practical_problem', 'measurement'}


def ev_ok(lines, ev):
    return isinstance(ev, dict) and quote_ok(lines, ev.get('line'), ev.get('quote'))


def check(rec, lines, module_ids):
    errs = []
    if rec.get('primary_gain') not in GAINS: errs.append('primary_gain')
    if rec.get('confidence') not in ('high', 'medium', 'low'): errs.append('confidence')
    tested_any = False
    for t in rec.get('tasks') or []:
        name = t.get('task', '?')
        if name not in FAMILIES and not str(name).startswith('other:'): errs.append(f'task {name}')
        for flag, key in (('automates', 'automation_evidence'), ('metric_gain', 'metric_evidence')):
            if not isinstance(t.get(flag), bool): errs.append(f'{name} {flag} not boolean')
            elif t[flag] and not ev_ok(lines, t.get(key)): errs.append(f'{name} {key} quote')
        for p in t.get('practical_problems') or []:
            if p.get('problem') not in PROBLEMS: errs.append(f'{name} problem {p.get("problem")}')
            if set(p.get('modules') or []) - module_ids: errs.append(f'{name} unknown module {sorted(set(p["modules"]) - module_ids)}')
            if not isinstance(p.get('tested'), bool): errs.append(f'{name} tested not boolean')
            if not ev_ok(lines, p.get('evidence')): errs.append(f'{name} {p.get("problem")} quote')
            tested_any = tested_any or p.get('tested') is True
    if not rec.get('tasks'): errs.append('no tasks')
    if rec.get('primary_gain') == 'practical_problem' and not tested_any: errs.append('practical_problem without a tested problem')
    return errs


def load(key):
    rec = json.loads((HERE / 'out_final' / f'{key}.json').read_text())
    return {m['id'] for m in rec.get('modules') or []}


def main(folder):
    rows, report, gains, cells = [], [], Counter(), Counter()
    recs = sorted(folder.glob('*.json'))
    for p in recs:
        rec = json.loads(p.read_text()); key = rec.get('citation_key') or p.stem
        errs = check(rec, packet_lines(key), load(key))
        if errs: report.append(f'- `{key}`: ' + '; '.join(errs[:8]))
        gains[rec.get('primary_gain')] += 1
        for t in rec.get('tasks') or []:
            probs = t.get('practical_problems') or []
            tested = sorted({x['problem'] for x in probs if x.get('tested')})
            claimed = sorted({x['problem'] for x in probs if not x.get('tested')})
            fam = t.get('task')
            cells[(fam, 'works')] += 1
            cells[(fam, 'automates')] += bool(t.get('automates'))
            cells[(fam, 'metric_gain')] += bool(t.get('metric_gain'))
            cells[(fam, 'tested_problem')] += bool(tested)
            cells[(fam, 'claimed_only')] += bool(claimed) and not tested
            for x in tested: cells[(fam, 'tested:' + x)] += 1
            for x in claimed: cells[(fam, 'claimed:' + x)] += 1
            rows.append({'key': key, 'task': fam, 'primary_gain': rec.get('primary_gain'), 'automates': t.get('automates'),
                         'metric_gain': t.get('metric_gain'), 'tested': ' '.join(tested), 'claimed_untested': ' '.join(claimed)})
    with (folder / 'impact.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    out = ['# Task-impact report', '', f'Records: {len(recs)}, with errors: {len(report)}. Primary gain: {dict(gains)}.', '',
           '| Task family | Works | Automates | Metric gain | Tested practical problem | Claimed, untested only |', '|---|---|---|---|---|---|']
    for fam in sorted({k[0] for k in cells}, key=str):
        out.append(f'| {fam} | ' + ' | '.join(str(cells[(fam, c)]) for c in ('works', 'automates', 'metric_gain', 'tested_problem', 'claimed_only')) + ' |')
    out += ['', 'Problems (tested / claimed only) by task family:', '']
    for fam in sorted({k[0] for k in cells}, key=str):
        probs = sorted({k[1].split(':', 1)[1] for k in cells if k[0] == fam and ':' in k[1]})
        out.append(f'- {fam}: ' + ', '.join(f'{x} {cells[(fam, "tested:" + x)]}/{cells[(fam, "claimed:" + x)]}' for x in probs))
    out += ['', '## Records with errors', ''] + (report or ['None.'])
    (folder / 'impact_report.md').write_text('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'impact'
    if arg.suffix == '.json':
        rec = json.loads(arg.read_text()); key = rec.get('citation_key') or arg.stem
        errs = check(rec, packet_lines(key), load(key))
        print('\n'.join(errs) if errs else 'OK'); sys.exit(1 if errs else 0)
    main(arg.resolve())
