"""Figure 13 (fig:benchmark-qa), V7 house style: an evidence-conditioned answer in TS-Agent.

Left: the anomaly-location question and the native series (illustrative). Centre: the Reasoner chooses the next
analytical action, the Detect tool returns an observation, the Evidence Log records it. Right: the evidence gate
checks both required predicates before accepting the answer; missing evidence sends the Reasoner back.
Bottom: the records needed to trace the answer.
"""
import math, os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *
from pptx.enum.dml import MSO_LINE
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitcheck import width_in

H = 6.5
SAND = 'A49A86'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figure13_V7.pptx')


def spike_series(sh, x, y, w, h, n=160):
    """A calm oscillating series with one anomaly spike in the middle third."""
    pts = []
    for k in range(n + 1):
        t = k / n
        v = 0.12 * math.sin(2 * math.pi * 11 * t) + 0.05 * math.sin(2 * math.pi * 27 * t + 0.7)
        v += 1.0 * math.exp(-((t - 0.5) / 0.035) ** 2)
        pts.append((x + w * t, y + h * 0.78 - h * 0.72 * v))
    return poly(sh, pts, INK, lw=1.7)


def question_zone(slide):
    zone(slide, 0.2, 0.42, 3.95, 4.13, 'Question & Series', 'data')
    g = group(slide); sh = g.shapes
    x, w = 0.4, 3.4
    # the anomaly-location question
    paper(sh, x, 0.98, w, 1.3)
    ic(sh, 'request', x + 0.08, 1.01, 0.62)
    tx(sh, x + 0.78, 1.06, 2.2, 0.42, 'Question', size=17, bold=True, align='l')
    b = box(sh, x + 0.13, 1.66, w - 0.26, 0.54, fill='FFF6E3', line='D9C49A', lw=0.8, radius=0.3)
    label_in(b, ['“In which part does', 'the anomaly occur?”'], size=13, bold=False, color=INK, italic=True)
    # the native series (illustrative), split into head / middle / end
    paper(sh, x, 2.66, w, 1.72)
    tx(sh, x + 0.13, 2.7, 2.0, 0.4, 'Native Series', size=17, bold=True, align='l')
    pill(sh, x + w - 1.2, 2.77, 1.08, 0.28, 'Illustrative', key='data', size=12, light=True)
    px, pw, py, ph = x + 0.15, w - 0.3, 3.12, 0.72
    third = pw / 3
    band = box(sh, px + third, py - 0.04, third, ph + 0.08, fill=HUE['tsk'][1], shape=MSO_SHAPE.RECTANGLE)
    alpha_fill(band, 35)
    spike_series(sh, px, py, pw, ph)
    by = py + ph + 0.1
    for k, (lab, col, bd) in enumerate([('Head', MUTE, True), ('Middle', HUE['tsk'][0], True), ('End', MUTE, True)]):
        x0, x1 = px + k * third + 0.05, px + (k + 1) * third - 0.05
        c = HUE['tsk'][0] if k == 1 else '9A8F7A'
        poly(sh, [(x0, by - 0.06), (x0, by), (x1, by), (x1, by - 0.06)], c, lw=1.4)
        tx(sh, x0, by + 0.03, x1 - x0, 0.28, lab, size=13, bold=bd, color=col)
    return g


def analysis_zone(slide):
    zone(slide, 4.3, 0.42, 4.65, 4.13, 'Iterative Analysis', 'ink')
    g = group(slide); sh = g.shapes
    dk = HUE['llm'][0]
    cx = 5.25
    halo(sh, cx, 1.25, 1.5, 1.3)
    pedestal(sh, cx - 0.47, 1.67, 0.94, 0.28, 'llm')
    ic(sh, 'robot', cx - 0.6, 0.66, 1.2)
    st = box(sh, 6.0, 1.0, 1.32, 0.4, fill=dk, radius=0.5); label_in(st, 'Reasoner', size=16)
    # action down, observation down into the log
    arrow(sh, cx, 2.0, cx, 2.4, color=dk, lw=2.6)
    tx(sh, cx + 0.16, 2.04, 2.6, 0.32, 'Next Analytical Action', size=14, bold=True, italic=True, color=dk, align='l')
    tk, tl = HUE['gts'], HUE['gh']
    card(sh, 4.52, 2.43, 2.95, 0.8, 'gts')
    ic(sh, 'anomaly', 4.6, 2.49, 0.68)
    tx(sh, 5.36, 2.46, 2.0, 0.38, 'Detect', size=16, bold=True, color=tk[0], align='l')
    tx(sh, 5.36, 2.83, 2.1, 0.32, 'Presence & Interval', size=13, color=MUTE, align='l', bold=True)
    arrow(sh, cx, 3.25, cx, 3.68, color=INK, lw=2.0, dash=MSO_LINE.DASH)
    tx(sh, cx + 0.16, 3.28, 1.6, 0.3, 'Observation', size=14, bold=True, italic=True, color=INK, align='l')
    paper(sh, 4.52, 3.72, 2.85, 0.74, line=tl[1], n=2)
    ic(sh, 'evidence_log', 4.58, 3.76, 0.64)
    tx(sh, 5.3, 3.74, 2.0, 0.36, 'Evidence Log', size=16, bold=True, color=tl[0], align='l')
    tx(sh, 5.3, 4.08, 2.05, 0.32, 'Anomaly Found: Middle', size=13, color=INK, align='l')
    return g


def gate_zone(slide):
    zone(slide, 9.1, 0.42, 4.03, 4.13, 'Evidence Gate & Answer', 'ev')
    g = group(slide); sh = g.shapes
    ev, ts = HUE['ev'], HUE['gts']
    x, w = 9.32, 3.45
    paper(sh, x, 0.98, w, 1.42, line='8E92BC')
    ic(sh, 'planning', x + 0.08, 1.0, 0.56)
    tx(sh, x + 0.7, 1.04, 2.6, 0.42, 'Required Evidence', size=16, bold=True, color=ev[0], align='l')
    for k, pred in enumerate(['has_anomaly = true', 'anomaly_segment = middle']):
        y = 1.6 + k * 0.4
        c = box(sh, x + 0.2, y, 0.3, 0.3, fill=ts[0], shape=MSO_SHAPE.OVAL)
        label_in(c, '✓', size=12.5)
        tx(sh, x + 0.6, y - 0.03, 2.75, 0.36, pred, size=13.5, color=INK, align='l')
    cx = 11.05
    arrow(sh, cx, 2.43, cx, 2.72, color=ev[0], lw=2.6, head=None)
    ic(sh, 'evidence_gate', cx - 0.38, 2.55, 0.76)
    tx(sh, cx + 0.45, 2.75, 1.6, 0.36, 'Both Covered', size=14, bold=True, italic=True, color=ts[0], align='l')
    arrow(sh, cx, 3.3, cx, 3.58, color=ts[0], lw=2.6)
    card(sh, 9.5, 3.62, 3.15, 0.8, 'gts')
    ic(sh, 'validate', 9.6, 3.68, 0.68)
    textbox_runs(sh, 10.35, 3.7, 2.2, 0.62, [('Answer: ', INK, True, False), ('Middle', HUE['tsk'][0], True, False)], 18, align='l')
    return g


def flows(slide):
    g = group(slide); sh = g.shapes
    ev, tl = HUE['ev'][0], HUE['gh'][0]
    # question -> Reasoner, series -> Detect tool
    arrow(sh, 3.97, 1.62, 4.6, 1.45, color=SAND, lw=2.4)
    arrow(sh, 3.97, 3.3, 4.5, 2.92, color=SAND, lw=2.4)
    # observation recorded in the log fills the required evidence
    curve(sh, [(7.5, 4.0), (8.75, 3.95), (9.28, 2.25)], tl, lw=2.6)
    # an uncovered requirement sends the Reasoner to another analytical action
    curve(sh, [(9.28, 1.3), (8.45, 0.62), (7.42, 1.18)], ev, lw=3.0, dash=MSO_LINE.DASH)
    ic(sh, 'feedback', 7.48, 1.42, 0.46)
    tx(sh, 7.98, 1.38, 1.0, 0.56, ['Missing', 'Evidence'], size=14, bold=True, italic=True, color=ev, align='l')
    return g


def trace_zone(slide):
    zone(slide, 0.2, 5.0, 12.93, 1.3, 'Answer Trace', 'ink')
    g = group(slide); sh = g.shapes
    items = [('timeseries', 'Native Series', 'data'), ('tools', 'Tool + Arguments', 'gts'),
             ('data', 'Structured Observation', 'gh'), ('planning', 'Answer Evidence', 'ev')]
    cws = [0.74 + width_in(lab, 14.5, True) + 0.22 for _, lab, _ in items]
    gap = 0.62
    x = 0.2 + (12.93 - sum(cws) - 3 * gap) / 2
    for k, (nm, lab, key) in enumerate(items):
        cw = cws[k]
        card(sh, x, 5.38, cw, 0.72, key)
        ic(sh, nm, x + 0.08, 5.42, 0.64)
        tx(sh, x + 0.74, 5.42, cw - 0.8, 0.64, lab, size=14.5, bold=True, color=HUE[key][0], align='l')
        if k < 3:
            arrow(sh, x + cw + 0.1, 5.74, x + cw + gap - 0.1, 5.74, color=INK, lw=2.4)
        x += cw + gap
    return g


def build(out=OUT):
    p, slide = new_slide(H)
    question_zone(slide)
    analysis_zone(slide)
    gate_zone(slide)
    trace_zone(slide)
    flows(slide)
    save(p, out)
    return out


if __name__ == '__main__':
    print(build())
