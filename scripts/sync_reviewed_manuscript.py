"""Render the appendix profiles and the ledger snapshot of main.tex from adjudicated module records (schema 3.0).

In scope are records with inclusion == "reviewed_contribution"; profile rows of other records are dropped.
Task labels come from the controlled task axes and other labels, not from the source prose.

Usage:
  python3 scripts/sync_reviewed_manuscript.py                 # rewrite main.tex in place
  python3 scripts/sync_reviewed_manuscript.py --dry-run       # print a unified diff, write nothing
  python3 scripts/sync_reviewed_manuscript.py --tex copy.tex  # rewrite another file
"""
import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {"forecasting_prediction": "Forecasting and prediction",
            "data_augmentation_synthesis": "Data augmentation and synthesis",
            "anomaly_detection_diagnosis": "Anomaly detection and diagnosis",
            "decision_support": "Decision support"}
# second label of a forecasting work: rendered in place of the family name
FORECAST = {"value_forecasting": "Value forecasting", "event_forecasting": "Event forecasting"}
ROLES = [("feedback_driven_agent", "feedback-driven Agents"), ("fixed_workflow", "fixed workflows"),
         ("llm_side_technique", "LLM-side techniques"), ("resource", "resources")]
CRITERIA = [("process_validity", "process validity"), ("temporal_validity", "temporal validity"),
            ("task_performance", "task performance"), ("decision_utility", "decision utility")]
LAYER_NAMES = {"LLM": "LLM-side", "GH": "General Harness", "GTS": "General Time Series Harness",
               "TSK": "Task-Specific Harness"}
# Figure 3 is drawn by the V7 script; the legacy timeline writes the same coverage numbers.
COVERAGE = [ROOT / "artifacts/unified_v7_20261106/fig03/module_contribution_timeline_coverage.json",
            ROOT / "artifacts/module_contribution_timeline_coverage.json"]


def escape(v):
    # Manuscript wording keeps "time series" unhyphenated, also as a modifier.
    v = v.replace('time-series', 'time series').replace('Time-series', 'Time series')
    return v.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_').replace('–', '--').replace('—', '---')


def in_scope(r):
    return (r.get('inclusion') == 'reviewed_contribution'
            and r['module_level_contributions'].get('review_status') in ('paper_verified', 'repository_verified'))


def task_label(r):
    """Task families in canonical wording, then other task labels in lower case (e.g. time series classification)."""
    tasks = r['tasks']
    other = tasks.get('other_labels', [])
    fc = [FORECAST[o] for o in FORECAST if o in other]
    labels = []
    for a in tasks.get('axes', []):
        if a == 'forecasting_prediction' and fc: labels += fc
        elif a in FAMILIES: labels.append(FAMILIES[a])
    labels += [o.replace('_', ' ') for o in other if o not in FORECAST]
    return '; '.join(dict.fromkeys(labels))


def render_profiles(s, bykey):
    new = []
    for line in s.splitlines():
        if '& \\textbf{' not in line:
            new.append(line); continue
        match = re.search(r'\\citep\{([^}]+)\}', line)
        key = match.group(1) if match else ('moiraiagent2026' if '\\RepoMoirai' in line
                                            else 'zhang2025llm' if '\\RepoLLMTSFD' in line else None)
        if key not in bykey:
            new.append(line); continue
        r = bykey[key]
        mods = r['module_level_contributions'].get('modules')
        if mods is None:
            raise ValueError('Unreviewed profile ' + key)
        if not in_scope(r):
            continue                                   # background references get no profile
        first = line.split('& \\textbf{')[0]
        # Keep the printed Agent terminology marker aligned with the canonical record.
        first = first.replace(r'\selfclaim{}', '')
        if not r['claimed_as_agent'] and match:
            first = first.replace(match.group(0), match.group(0) + r'\selfclaim{}', 1)
        first = first.split(r'\newline')[0] + r'\newline ' + escape(task_label(r)) + ' '
        parts = []
        for layer in ['GH', 'GTS', 'TSK', 'LLM']:
            names = [escape(m['name']) for m in mods if m['layer'] == layer]
            if names:
                parts.append('\\textbf{' + layer + ':} ' + '; '.join(names) + '.')
        new.append(first + '& ' + r'\newline'.join(parts) + r'\\\midrule')
    return '\n'.join(new) + '\n'


def snapshot(records, active, mods):
    status = Counter(r['module_level_contributions']['review_status'] for r in active)
    excluded = len(records) - len(active)
    layers = Counter(m['layer'] for m in mods)
    roles = Counter(r.get('role_of_work') for r in active)
    criteria = Counter(c for r in active for c, v in (r.get('evaluation_evidence') or {}).items() if v.get('present'))
    families = Counter(a for r in active for a in r['tasks'].get('axes', []))
    others = Counter(o for r in active for o in r['tasks'].get('other_labels', []) if o not in FORECAST)
    top_other = [o.replace('_', ' ') for o, _ in others.most_common(4)]
    listing = lambda items: ', '.join(items[:-1]) + ', and ' + items[-1]
    return (r'\textbf{Current ledger snapshot.} The database contains \textbf{' + str(len(records)) + r'} examined records: '
            + str(len(active)) + ' works in scope (' + str(status['paper_verified']) + ' paper-supported works and '
            + str(status['repository_verified']) + ' repository-supported resources) and ' + str(excluded)
            + ' background records excluded from contribution counts. By role, the works in scope comprise '
            + listing([f'{roles[k]} {name}' for k, name in ROLES]) + '. '
            + 'They contain ' + str(len(mods)) + ' source-located modules: '
            + listing([f'{layers[k]} {LAYER_NAMES[k]}' for k in ('LLM', 'GH', 'GTS', 'TSK')]) + ' modules. '
            + 'Task memberships comprise '
            + listing([f'{families[k]} {name[0].lower() + name[1:]}' for k, name in FAMILIES.items()])
            + ' works; the most frequent other task labels are ' + listing(top_other) + '. '
            + 'Their own experiments provide evidence for '
            + listing([f'{name} in {criteria[k]}' for k, name in CRITERIA]) + ' works. '
            + 'Each module has one layer and may have several mechanism, temporal function, and task labels.')


def check_coverage(active):
    expected = Counter()
    for path in COVERAGE:
        if not path.exists():
            continue
        coverage = json.loads(path.read_text())
        undated = set(coverage['undated_records'])
        expected = Counter(m['layer'] for r in active if r['citation']['key'] not in undated
                           for m in r['module_level_contributions']['modules'])
        if any(expected[layer] != coverage['plotted_modules'][label] for layer, label in LAYER_NAMES.items()):
            raise ValueError(f'Timeline is stale ({path.relative_to(ROOT)}); regenerate Figure 3 first')
        return coverage
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--tex', type=Path, default=ROOT / 'main.tex')
    parser.add_argument('--dry-run', action='store_true', help='print a unified diff instead of writing')
    args = parser.parse_args()

    records = json.loads((ROOT / 'paper_classification_ledger.json').read_text())
    bykey = {r['citation']['key']: r for r in records}
    active = [r for r in records if in_scope(r)]
    mods = [m for r in active for m in r['module_level_contributions']['modules']]

    original = args.tex.read_text()
    s = render_profiles(original, bykey)
    text = snapshot(records, active, mods)
    s = re.sub(r'\\textbf\{Current ledger snapshot\.\}[^\n]*', lambda _: text, s)
    s = re.sub(r'Profiles of the \d+ (?:reviewed|retained) works\.', f'Profiles of the {len(active)} retained works.', s)
    s = re.sub(r'It covers \d+ examined records, including \d+ retained works and resources with \d+ module entries\.',
               f'It covers {len(records)} examined records, including {len(active)} retained works and resources '
               f'with {len(mods)} module entries.', s)
    coverage = check_coverage(active)
    if coverage:
        n = coverage['dated_records']
        s = re.sub(r'Cumulative source-reviewed module annotations across \d+ dated records',
                   f'Cumulative source-reviewed module annotations across {n} dated records', s)
        s = re.sub(r'(Module contributions by layer over time, from )\d+( dated records)', rf'\g<1>{n}\g<2>', s)

    if args.dry_run:
        sys.stdout.writelines(difflib.unified_diff(original.splitlines(True), s.splitlines(True),
                                                   str(args.tex), str(args.tex) + ' (synced)', n=0))
    else:
        args.tex.write_text(s)
    print('Snapshot:', len(records), 'examined;', len(active), 'in scope;', len(mods), 'modules;',
          dict(Counter(m['layer'] for m in mods)), file=sys.stderr)


if __name__ == '__main__':
    main()
