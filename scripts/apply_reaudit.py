"""Apply the adjudicated 2026-11-06 Paper Card re-audit to the maintained ledger.

usage: python3 scripts/apply_reaudit.py [--impact] [--dry-run]

Reads references/reviews/20261106_terra_reaudit/out_final/<key>.json (one adjudicated record per work, rubric R0-R10)
and replaces, per work, the module list, claim summary and evidence, task coordinate, role of work, evaluation evidence,
review status and review_audit entry. Bibliographic fields, official resources and the boundary-review record are left
untouched. Packet line citations {"line", "quote"} become {"locator": "PDF p.X; source text L<n>", "quote"}: the packet
is pdftotext output of the PDF with page breaks turned into line breaks, so its lines are re-split by page; a quote is
assigned the page(s) of the lines it spans. Where no page is found the locator is "Source text L<n>".

--impact also fills task_impact_json from impact/<key>.json (rubric R11) where such a file exists; without it the column
keeps its current value. All records are validated before anything is written; the CSV, the function-view mapping and
the JSON ledger are replaced atomically. Re-running gives the same result.
"""
import argparse, csv, json, os, re, subprocess, sys, unicodedata
from collections import Counter
from pathlib import Path

import classification_manager as manager
import sync_function_view
from ledger_schema import SCHEMA, SCHEMA_VERSION, TASK_FAMILIES, canonical_tasks

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'references/reviews/20261106_terra_reaudit'
REL = FOLDER.relative_to(ROOT).as_posix()
MAPPING = FOLDER / 'module_function_mapping.json'
DATE = '2026-11-07'
CODERS = {'codex': 'Codex (gpt-6.1-sol)', 'haiku': 'Claude Haiku (fallback coder)'}
TASK_FIELDS = dict(zip(TASK_FAMILIES, manager.TASK_AXES))
MODULE_FIELDS = ('id', 'name', 'layer', 'dimensions', 'functions', 'view_status', 'llm_route', 'tasks', 'other_tasks',
                 'role', 'scope_reason', 'rubric_path', 'reuse_evidence', 'evidence', 'confidence')
sys.path.insert(0, str(FOLDER))
import check_outputs  # noqa: E402  (the re-audit's own validator and quote matcher)


def tokens_tagged(pairs):
    """[(tag, text)] -> [(token, tag)] with the same tokenization as check_outputs.tokens."""
    return [(t, tag) for tag, text in pairs for t in check_outputs.tokens(text)]


def find_span(tagged, quote):
    """Tags of the first and last quote token, matched as in check_outputs.quote_ok; None if absent."""
    q = check_outputs.tokens(quote)
    if not q: return None
    win = [t for t, _ in tagged]
    joined, owner = '', []
    for i, t in enumerate(win):
        joined += t; owner += [i] * len(t)
    pos = joined.find(''.join(q))
    if pos >= 0:
        return tagged[owner[pos]][1], tagged[owner[pos + len(''.join(q)) - 1]][1]
    budget = max(3, len(q) // 10)
    for start in (i for i, t in enumerate(win) if t == q[0]):
        j, gaps, last = start + 1, [], start
        for t in q[1:]:
            g = 0
            while j < len(win) and win[j] != t and g <= 15:
                j += 1; g += 1
            if j >= len(win) or win[j] != t: break
            if g: gaps.append(g)
            last = j; j += 1
        else:
            if not gaps or (max(gaps) <= 15 and sum(gaps) - max(gaps) <= budget):
                return tagged[start][1], tagged[last][1]
    return None


class Source:
    """Packet lines of one work and, for a PDF source, the PDF page of every packet line."""

    def __init__(self, key):
        text = (FOLDER / 'packets' / f'{key}.txt').read_text()
        self.packet = f'{REL}/packets/{key}.txt'
        self.path = re.search(r'^SOURCE: (.*)$', text, re.M).group(1).strip()
        self.lines = check_outputs.packet_lines(key)
        self.page_of, self.pages, self.reproduced = {}, [], False
        pdf = ROOT / self.path
        if pdf.suffix.lower() != '.pdf' or not pdf.exists():
            return
        out = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(pdf), '-'], capture_output=True, text=True).stdout
        numbered = []  # (page, line text) in packet order: make_packets.py drops blank lines after replacing form feeds
        for page_no, page in enumerate(out.split('\f'), 1):
            lines = [ln for ln in (re.sub(r'\s+', ' ', x).strip() for x in page.splitlines()) if ln]
            self.pages.append(' '.join(lines))
            numbered += [(page_no, ln) for ln in lines]
        self.reproduced = [ln for _, ln in numbered] == [self.lines.get(i) for i in range(1, len(self.lines) + 1)]
        if self.reproduced:
            self.page_of = {i: page for i, (page, _) in enumerate(numbered, 1)}

    def pages_for(self, line, quote):
        """Sorted PDF pages holding the quote, or [] (then the caller falls back to the packet line)."""
        if self.reproduced:
            window = [(i, self.lines.get(i, '')) for i in range(line - 4, line + 9) if i in self.lines]
            span = find_span(tokens_tagged(window), quote)
            if span:
                return sorted({self.page_of[i] for i in range(span[0], span[1] + 1)}), 'pdf_page'
        for i in range(len(self.pages)):  # page text search when the packet cannot be re-split by page
            pair = [(i + 1, self.pages[i])] + ([(i + 2, self.pages[i + 1])] if i + 1 < len(self.pages) else [])
            span = find_span(tokens_tagged(pair), quote)
            if span:
                return sorted(set(range(span[0], span[1] + 1))), 'pdf_page_search'
        return [], 'packet_line'


def locate(ev, src, stats):
    """{'line', 'quote'} -> ledger evidence with a page locator (or a packet-line fallback)."""
    line, quote = ev['line'], ev['quote']
    pages, kind = src.pages_for(line, quote) if src.pages else ([], 'packet_line')
    stats[kind if pages else ('fallback_non_pdf' if not src.pages else 'fallback_not_found')] += 1
    if pages:
        where = f'PDF p.{pages[0]}' if len(pages) == 1 else f'PDF pp.{pages[0]}-{pages[-1]}'
        return {'locator_type': 'page_line', 'locator': f'{where}; source text L{line}', 'quote': quote,
                'source_path': src.path, 'packet_line': line}
    return {'locator_type': 'packet_line', 'locator': f'Source text L{line}', 'quote': quote,
            'source_path': src.packet, 'original_source': src.path, 'packet_line': line}


def locate_all(value, src, stats):
    """Convert every {'line', 'quote'} object inside a JSON value (used for task-impact records)."""
    if isinstance(value, dict):
        if isinstance(value.get('line'), int) and value.get('quote'):
            rest = {k: v for k, v in value.items() if k not in ('line', 'quote')}
            return {**locate(value, src, stats), **rest}
        return {k: locate_all(v, src, stats) for k, v in value.items()}
    if isinstance(value, list):
        return [locate_all(v, src, stats) for v in value]
    return value


def split_tasks(tasks, other):
    """Canonical families and other task values; a family recorded as an other task moves to the families."""
    values = canonical_tasks(list(tasks) + list(other))
    return [t for t in values if t in TASK_FAMILIES], [t for t in values if t not in TASK_FAMILIES]


def module_record(m, src, stats, notes):
    m = {k: m[k] for k in MODULE_FIELDS if k in m}
    tasks, other = split_tasks(m.get('tasks', []), m.get('other_tasks', []))
    if (tasks, other) != (m.get('tasks', []), m.get('other_tasks', [])):
        notes['module_task_normalized'].append(m['id'])
    m['tasks'], m['other_tasks'] = tasks, other
    m['evidence'] = [locate(e, src, stats) for e in m['evidence']]
    return m


def function_assignment(m):
    r5 = [x for x in m.get('rubric_path', []) if x.startswith('R5')]
    return {'functions': m['functions'], 'view_status': m['view_status'],
            'rationale': f'Re-audit {DATE} (rubric R5): {m["view_status"]}' + (f'; {"; ".join(r5)}' if r5 else ''),
            'evidence_indices': list(range(len(m['evidence']))), 'reuse_proposals': []}


def apply_record(row, rec, selection, stats, notes):
    key = row['citation_key']
    src = Source(key)
    if src.pages and not src.reproduced: notes['pdf_not_resplit'].append(key)
    status = rec['status']
    modules = [module_record(m, src, stats, notes) for m in rec['modules']]
    if status in ('out_of_scope', 'blocked') and modules: raise ValueError(f'{key}: modules on an excluded record')
    tasks, other = split_tasks(rec['task_memberships'], rec['other_tasks'])
    m_tasks, m_other = split_tasks([t for m in modules for t in m['tasks']], [t for m in modules for t in m['other_tasks']])
    if set(m_tasks) - set(tasks) or set(m_other) - set(other): notes['work_task_added_from_module'].append(key)
    tasks = [t for t in TASK_FAMILIES if t in set(tasks) | set(m_tasks)]
    other = list(dict.fromkeys(other + m_other))
    claim_ev = [locate(e, src, stats) for e in rec['claim_evidence']]
    evaluation = {}
    for k in check_outputs.EVAL:
        item = rec['evaluation_evidence'].get(k) or {}
        evaluation[k] = ({'present': True, **locate(item, src, stats)} if item.get('present')
                         else {'present': False, 'locator': None, 'quote': None})
    previous = json.loads(row.get('review_audit_json') or '{}')
    history = previous.get('history', []) if previous.get('review') == 'terra_reaudit' else [previous] if previous else []
    adjudication = rec.get('adjudication')
    audit = {'review': 'terra_reaudit', 'date': DATE, 'record_file': f'{REL}/out_final/{key}.json',
             'rubric': f'{REL}/rubric_tree.yaml', 'packet': src.packet, 'source_path': src.path,
             'coder': CODERS[selection[key]], 'adjudicator': adjudication['reviewer'] if adjudication else None,
             'status': status, 'role_of_work': rec['role_of_work'], 'needs_human_review': rec['needs_human_review'],
             'notes': rec.get('notes', ''), 'reconciliation': rec.get('reconciliation', []),
             'adjudication': adjudication, 'history': history}

    row['reviewed_modules_json'] = json.dumps(modules, ensure_ascii=False)
    row['taxonomy_review_status'] = status
    row['claim_review_status'] = 'paper_verified' if status == 'out_of_scope' else status
    row['included_as'] = {'out_of_scope': 'background_reference', 'blocked': 'pending_evidence'}.get(status, 'reviewed_contribution')
    row['paper_claim_summary'] = row['primary_contribution'] = rec['claim_summary']
    row['claim_evidence_basis'] = f'terra_reaudit_{DATE.replace("-", "")}: ' + ' | '.join(e['locator'] for e in claim_ev)
    row['claim_evidence_json'] = json.dumps(claim_ev, ensure_ascii=False)
    row['source_evidence_json'] = json.dumps(claim_ev + [e for m in modules for e in m['evidence']], ensure_ascii=False)
    row['role_of_work'] = rec['role_of_work']
    row['evaluation_evidence_json'] = json.dumps(evaluation, ensure_ascii=False)
    row['review_audit_json'] = json.dumps(audit, ensure_ascii=False)
    row['classification_notes'] = (f'Re-audit {DATE}: ' + rec['notes']).strip() if rec.get('notes') else f'Re-audit {DATE}.'
    for task, legacy in TASK_FIELDS.items():
        row['task_axis_' + legacy] = 'Yes' if task in tasks else 'No'
    row['task_axis_other'] = '; '.join(other)
    row['task_axis_notes'] = f'Re-audit {DATE} task coordinate (rubric R7): work memberships plus every module task.'
    for layer, field in [('LLM', 'llm_component_contribution'), ('GH', 'general_harness_contribution'),
                         ('GTS', 'general_ts_harness_contribution'), ('TSK', 'task_specific_harness_contribution')]:
        row[field] = '; '.join(m['name'] for m in modules if m['layer'] == layer)
    row['llm_side_subdimensions'] = json.dumps(sorted({r for m in modules for r in m.get('llm_route', [])}))
    row['general_ts_specificity_reason'] = json.dumps([m['scope_reason'] for m in modules if m['layer'] == 'GTS'], ensure_ascii=False)
    row['harness_modules'] = '; '.join(sorted({d for m in modules if m['layer'] != 'LLM' for d in m['dimensions']}))
    row['harness_module_coding_basis'] = 'primary_source_module_review'
    layers = Counter(m['layer'] for m in modules)
    row['primary_locus'] = max(layers, key=lambda k: (layers[k], ['GH', 'GTS', 'TSK', 'LLM'].index(k))) if layers else 'NONE'
    for field in ('general_harness_dimensions', 'general_ts_harness_dimensions', 'task_specific_modules_json'):
        row[field] = ''
    row['taxonomy_schema_version'] = SCHEMA_VERSION
    return {m['id']: function_assignment(m) for m in modules}, src


def atomic_write(path, text):
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(text, encoding='utf-8'); os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--impact', action='store_true', help='also import impact/<key>.json into task_impact_json')
    ap.add_argument('--dry-run', action='store_true', help='validate and report without writing')
    a = ap.parse_args()
    rows = manager.read_csv(manager.LEDGER)
    records = {p.stem: json.loads(p.read_text()) for p in sorted((FOLDER / 'out_final').glob('*.json'))}
    with (FOLDER / 'selection.csv').open() as f:
        selection = {r['key']: r['source'] for r in csv.DictReader(f)}
    keys = {r['citation_key'] for r in rows}
    if keys != set(records): raise ValueError(f'Record/ledger keys differ: {sorted(keys ^ set(records))}')
    errors = {k: e for k, r in records.items() if (e := check_outputs.check(r, check_outputs.packet_lines(k)))}
    if errors: raise ValueError(f'Invalid re-audit records: {errors}')
    stats, notes, assignments, sources = Counter(), {k: [] for k in ('module_task_normalized', 'work_task_added_from_module', 'pdf_not_resplit')}, {}, {}
    for row in rows:
        mapping, sources[row['citation_key']] = apply_record(row, records[row['citation_key']], selection, stats, notes)
        assignments.update(mapping)
    impact_stats = Counter()
    if a.impact:
        for row in rows:
            p = FOLDER / 'impact' / f'{row["citation_key"]}.json'
            if p.exists():
                row['task_impact_json'] = json.dumps(locate_all(json.loads(p.read_text()), sources[row['citation_key']], impact_stats), ensure_ascii=False)
                impact_stats['records'] += 1
    mapping = {'version': '2.0', 'unit': 'module id of the 2026-11-07 re-audit',
               'functions': SCHEMA['temporal_function_view']['values'],
               'semantics': 'Non-exclusive reading view over the five mechanism dimensions, copied from each adjudicated module (rubric R5). Tags do not change scope or create contribution units.',
               'assignments': assignments, 'schema_version': SCHEMA_VERSION,
               'review_basis': f'{REL}/out_final (adjudicated re-audit records)'}
    rows = sync_function_view.apply_view(rows, mapping)
    for row in rows:
        row['module_level_contributions_json'] = json.dumps(manager.module_contribution_record(row), ensure_ascii=False)
    report = {'records': len(rows), 'status': dict(Counter(r['taxonomy_review_status'] for r in rows)),
              'modules': len(assignments), 'locators': dict(stats), 'notes': {k: v for k, v in notes.items() if v}}
    if a.impact: report['impact'] = dict(impact_stats)
    if not a.dry_run:
        atomic_write(MAPPING, json.dumps(mapping, indent=1, ensure_ascii=False) + '\n')
        manager.write_csv(rows)  # temporary file + rename
        manager.generate_json(rows)
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
