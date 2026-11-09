"""Task groups: the task axis of the survey, grouped by what a task output refers to relative to the current time tau.

Leaves keep the standard task names (TimesNet/TSLib: forecasting, imputation, classification, anomaly detection;
Time-MQA: question answering). Groups:
  analysis     - Analysis of Observed Series: the output describes observations available at tau
  forecasting  - Forecasting: the output describes values or events after tau
  generation   - Generation: the output is a new series
  decision     - Decision Making: the output is an action

Forecasting modules carry a second label: value_forecasting (numerical values after tau) or event_forecasting
(a discrete outcome or event probability after tau); a module may carry both.

CELL places each label in the output-mode x time grid: mode in {regression, classification, generation, decision},
time in {before, after} the current time tau (decision is always after). `--grid` prints works per cell.

usage: python3 scripts/task_groups.py            -> summary (works and modules per group, reuse by group)
       python3 scripts/task_groups.py --json     -> the same as JSON
Import: from task_groups import GROUPS, LEAF, group_of, module_groups
"""
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / 'references/reviews/20261106_terra_reaudit/out_final'

GROUPS = {'analysis': 'Analysis of Observed Series', 'forecasting': 'Forecasting',
          'generation': 'Generation', 'decision': 'Decision Making'}
ORDER = ['analysis', 'forecasting', 'generation', 'decision']

# label -> (group, leaf)
LEAF = {
    'anomaly_detection_diagnosis': ('analysis', 'anomaly detection'),
    'change_point_detection': ('analysis', 'anomaly detection'),
    'time_series_event_detection': ('analysis', 'anomaly detection'),
    'time_series_classification': ('analysis', 'classification'),
    'imputation': ('analysis', 'imputation'),
    'reconstruction': ('analysis', 'imputation'),
    'temporal_question_answering': ('analysis', 'question answering'),
    'temporal_analysis': ('analysis', 'question answering'),
    'time_series_reporting': ('analysis', 'question answering'),
    'time_series_captioning': ('analysis', 'question answering'),
    'time_series_annotation': ('analysis', 'question answering'),
    'temporal_causal_analysis': ('analysis', 'question answering'),
    'etiological_reasoning': ('analysis', 'question answering'),
    'causal_discovery': ('analysis', 'question answering'),
    'traffic_simulation_analysis': ('analysis', 'question answering'),
    'data_quality': ('analysis', 'other'),
    'physiological_signal_estimation': ('analysis', 'other'),
    'time_series_segmentation': ('analysis', 'other'),
    'temporal_representation_learning': ('analysis', 'other'),
    'transfer_learning': ('analysis', 'other'),
    'forecasting_prediction': ('forecasting', 'forecasting'),
    'value_forecasting': ('forecasting', 'value forecasting'),
    'event_forecasting': ('forecasting', 'event forecasting'),
    'hydrologic_model_calibration': ('forecasting', 'forecasting'),
    'data_augmentation_synthesis': ('generation', 'generation'),
    'decision_support': ('decision', 'decision making'),
    'traffic_signal_control': ('decision', 'decision making'),
    'demand_optimization': ('decision', 'decision making'),
}


# label -> (output mode, time relative to tau); forecasting_prediction alone is resolved by its second label
CELL = {
    'imputation': ('regression', 'before'), 'reconstruction': ('regression', 'before'),
    'physiological_signal_estimation': ('regression', 'before'), 'hydrologic_model_calibration': ('regression', 'before'),
    'time_series_classification': ('classification', 'before'), 'anomaly_detection_diagnosis': ('classification', 'before'),
    'change_point_detection': ('classification', 'before'), 'time_series_event_detection': ('classification', 'before'),
    'data_quality': ('classification', 'before'), 'time_series_segmentation': ('classification', 'before'),
    'temporal_question_answering': ('generation', 'before'), 'temporal_analysis': ('generation', 'before'),
    'time_series_reporting': ('generation', 'before'), 'time_series_captioning': ('generation', 'before'),
    'time_series_annotation': ('generation', 'before'), 'temporal_causal_analysis': ('generation', 'before'),
    'etiological_reasoning': ('generation', 'before'), 'causal_discovery': ('generation', 'before'),
    'traffic_simulation_analysis': ('generation', 'before'), 'data_augmentation_synthesis': ('generation', 'before'),
    'value_forecasting': ('regression', 'after'), 'event_forecasting': ('classification', 'after'),
    'decision_support': ('decision', 'after'), 'traffic_signal_control': ('decision', 'after'),
    'demand_optimization': ('decision', 'after'),
}
MODES = ['regression', 'classification', 'generation', 'decision']


def group_of(label):
    return LEAF.get(label, (None, None))[0]


def labels(obj):
    return list(obj.get('tasks') or obj.get('task_memberships') or []) + list(obj.get('other_tasks') or [])


def module_groups(m):
    """Task groups a module is applied to in its source: its own task labels plus the tasks in its reuse evidence."""
    reuse = (m.get('reuse_evidence') or {}).get('tasks') or []
    return {g for g in map(group_of, labels(m) + list(reuse)) if g}


def records():
    for p in sorted(FINAL.glob('*.json')):
        r = json.loads(p.read_text())
        if r.get('status') != 'out_of_scope':
            yield r


def summary():
    works, leaves, mods, reuse, unmapped = Counter(), Counter(), Counter(), Counter(), Counter()
    n = 0
    for r in records():
        n += 1
        labs = set(labels(r))
        for m in r.get('modules') or []:
            labs |= set(labels(m))
            gs = module_groups(m)
            for g in gs: mods[(g, m.get('layer'))] += 1
            if m.get('layer') in ('GH', 'GTS'):
                reuse[(m['layer'], 'demonstrated' if len(gs) >= 2 else 'inferred')] += 1
        for g in {group_of(x) for x in labs} - {None}: works[g] += 1
        for lf in {LEAF[x][1] for x in labs if x in LEAF}: leaves[lf] += 1
        for x in labs:
            if x not in LEAF: unmapped[x] += 1
    return {'works': n, 'works_by_group': {GROUPS[g]: works[g] for g in ORDER}, 'works_by_leaf': dict(leaves.most_common()),
            'modules_by_group_layer': {f'{GROUPS[g]}:{l}': c for (g, l), c in sorted(mods.items())},
            'reuse_gh_gts': {f'{l}:{e}': c for (l, e), c in sorted(reuse.items())}, 'unmapped_labels': dict(unmapped)}


def grid():
    """Works per (mode, time) cell; method-only labels (representation, transfer learning) have no cell."""
    cells, none = Counter(), Counter()
    for r in records():
        labs = set(labels(r)) | {x for m in r.get('modules') or [] for x in labels(m)}
        for c in {CELL[x] for x in labs if x in CELL}: cells[c] += 1
        for x in labs - set(CELL) - {'forecasting_prediction'}: none[x] += 1
    return {'cells': {f'{m}:{t}': cells[(m, t)] for m in MODES for t in ('before', 'after')}, 'no_cell': dict(none)}


if __name__ == '__main__':
    if '--grid' in sys.argv:
        print(json.dumps(grid(), indent=1)); sys.exit()
    s = summary()
    print(json.dumps(s, indent=1, ensure_ascii=False))
