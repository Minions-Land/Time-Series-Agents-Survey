"""Figure 8 (fig:task-specific-harness): the task grid, V7 house style.

Rows are the four output modes (regression, classification, generation, decision making); columns are the two sides
of the current time (observed record | after the current time), separated by a dashed Now divider. Each cell is a card
with a schematic output glyph, the cell name with its number of works, its second-level tasks, and how the output is
checked (Table tab:tsk-vocab). The two empty cells (projection, hindsight decision) are dashed cards marked as open
problems. Wording follows Table tab:tsk-vocab of main.tex; counts follow scripts/task_groups.py --grid.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit')))
from v7kit import *
from PIL import ImageFont

TK, TKm, TKl = HUE['tsk']
EV, EVm, EVl = HUE['ev']
GT = HUE['gts'][0]
SD, SDm, SDl = HUE['data']
FONTS = {False: '/System/Library/Fonts/Supplemental/Comic Sans MS.ttf',
         True: '/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf'}
WARN = []

H = 8.15
X0, HW = 0.2, 1.78            # row-header column
GAP = 0.34                    # gap between the two cell columns (holds the Now divider)
CW = (W - 0.2 - X0 - HW - 0.12 - GAP) / 2
CX = [X0 + HW + 0.12, X0 + HW + 0.12 + CW + GAP]
DIV = CX[0] + CW + GAP / 2
Y0, RH, RG = 0.98, 1.62, 0.14
RY = [Y0 + k * (RH + RG) for k in range(4)]
GW, GH = 1.55, 1.12           # glyph box


def width(t, size, bold):
    return ImageFont.truetype(FONTS[bold], int(size * 20)).getlength(t) / (20 * 72)


def T(sh, x, y, w, h, t, size=13, bold=True, color=INK, align='c', anchor='m', italic=False):
    assert size >= 11.5, (t, size)
    for ln in (t if isinstance(t, list) else [t]):
        if width(ln, size, bold) > w - 0.04: WARN.append(f'overflow {ln!r} {width(ln, size, bold):.2f} > {w:.2f}')
    return tx(sh, x, y, w, h, t, size=size, bold=bold, color=color, align=align, anchor=anchor, italic=italic)


def pline(sh, x, y, w, h, vals, color=INK, lw=1.6, dash=None):
    n = len(vals) - 1
    pts = [(x + w * k / n, y + h * (1 - v)) for k, v in enumerate(vals)]
    poly(sh, pts, color, lw=lw, dash=dash)
    return pts


def now_line(sh, x, y, h):
    arrow(sh, x, y, x, y + h, color=GT, lw=1.3, dash=MSO_LINE.DASH, head=None)


SER = [0.35, 0.55, 0.4, 0.7, 0.5, 0.62, 0.45, 0.8, 0.55, 0.72, 0.5, 0.66]


# --------------------------------------------------------------------------------------------- glyphs
def g_impute(sh, x, y):
    vals = SER
    n = len(vals) - 1
    pts = [(x + GW * k / n, y + GH * (1 - v)) for k, v in enumerate(vals)]
    poly(sh, pts[:5], INK, lw=1.6); poly(sh, pts[8:], INK, lw=1.6)
    poly(sh, pts[4:9], TK, lw=2.0, dash=MSO_LINE.DASH)
    b = box(sh, pts[4][0], y + 0.02, pts[8][0] - pts[4][0], GH - 0.04, fill=TK, radius=0.15); alpha_fill(b, 14)


def g_forecast(sh, x, y):
    mini_forecast(sh, x, y + 0.05, GW, GH - 0.3, cut=0.6)


def g_detect(sh, x, y):
    vals = [0.35, 0.5, 0.38, 0.52, 0.4, 0.95, 0.42, 0.5, 0.36, 0.48, 0.4, 0.5]
    pts = pline(sh, x, y + 0.1, GW, GH - 0.2, vals, INK, lw=1.6)
    b = box(sh, pts[4][0], y + 0.02, pts[6][0] - pts[4][0], GH - 0.06, fill=TK, line=TK, lw=1.0, radius=0.1,
            dash=MSO_LINE.DASH); alpha_fill(b, 20)
    for k, (lab, c) in enumerate((('A', TK), ('B', EV))):
        p = box(sh, x + 0.02 + 0.36 * k, y + GH - 0.3, 0.3, 0.26, fill=c, radius=0.5); label_in(p, lab, size=12)


def g_event(sh, x, y):
    pline(sh, x, y + 0.2, GW * 0.55, GH - 0.55, SER[:7], INK, lw=1.6)
    t0 = x + GW * 0.55
    now_line(sh, t0, y + 0.02, GH - 0.1)
    bx, bw, bh = t0 + 0.22, 0.34, GH - 0.3
    box(sh, bx, y + 0.12, bw, bh, fill='FFFFFF', line=EVm, lw=1.0, shape=MSO_SHAPE.RECTANGLE)
    box(sh, bx, y + 0.12 + bh * 0.3, bw, bh * 0.7, fill=TK, shape=MSO_SHAPE.RECTANGLE)
    T(sh, bx - 0.25, y + GH - 0.16, bw + 0.5, 0.22, '0.7', size=12, color=TK)


def g_describe(sh, x, y):
    s = paper(sh, x + 0.05, y + 0.12, GW - 0.2, GH - 0.18, n=2)
    pline(sh, x + 0.14, y + 0.18, GW - 0.38, 0.38, SER, INK, lw=1.4)
    for k in range(3):
        arrow(sh, x + 0.16, y + 0.68 + 0.13 * k, x + GW - 0.3 - 0.25 * (k == 2), y + 0.68 + 0.13 * k, color=TKm, lw=2.2, head=None)


def g_projection(sh, x, y):
    pline(sh, x, y + 0.25, GW * 0.45, GH - 0.6, SER[:6], INK, lw=1.6)
    t0 = x + GW * 0.45
    now_line(sh, t0, y + 0.02, GH - 0.1)
    yc = y + 0.25 + (GH - 0.6) * (1 - SER[5])
    for dy, lab in ((-0.32, 'If X'), (0.3, 'If Y')):
        curve(sh, [(t0, yc), (t0 + 0.35, yc + dy * 0.5), (x + GW - 0.05, yc + dy)], MUTE, lw=1.6, dash=MSO_LINE.DASH, head=False)
    T(sh, x + GW - 0.55, y - 0.02, 0.6, 0.22, 'If X', size=12, color=MUTE)
    T(sh, x + GW - 0.55, y + GH - 0.22, 0.6, 0.22, 'If Y', size=12, color=MUTE)


def g_hindsight(sh, x, y):
    vals = [0.4, 0.5, 0.45, 0.55, 0.5, 0.35, 0.25, 0.2, 0.15]
    pts = pline(sh, x, y + 0.18, GW * 0.82, GH - 0.42, vals, INK, lw=1.6)
    k0 = 4
    curve(sh, [pts[k0], (pts[6][0], pts[k0][1] - 0.2), (pts[-1][0], pts[k0][1] - 0.4)], MUTE, lw=1.6, dash=MSO_LINE.DASH, head=False)
    d = box(sh, pts[k0][0] - 0.08, pts[k0][1] - 0.08, 0.16, 0.16, fill=TK, shape=MSO_SHAPE.OVAL)
    now_line(sh, x + GW - 0.06, y + 0.02, GH - 0.1)
    T(sh, pts[k0][0] - 0.45, y + GH - 0.24, 0.9, 0.22, 'Earlier', size=12, color=TK)


def g_decide(sh, x, y):
    pline(sh, x, y + 0.25, GW * 0.42, GH - 0.6, SER[:6], INK, lw=1.6)
    t0 = x + GW * 0.42
    now_line(sh, t0, y + 0.02, GH - 0.1)
    yc = y + 0.25 + (GH - 0.6) * (1 - SER[5])
    for dy, lab in ((-0.3, 'A'), (0.3, 'B')):
        arrow(sh, t0 + 0.04, yc, t0 + 0.55, yc + dy, color=TK, lw=1.8)
        p = box(sh, t0 + 0.58, yc + dy - 0.14, 0.28, 0.28, fill='FFFFFF', line=TK, lw=1.3, shape=MSO_SHAPE.OVAL)
        label_in(p, lab, size=12, color=TK)


# ------------------------------------------------------------------------------------------------ cells
ROWS = [  # (mode, icon, [observed cell, future cell])
    ('Regression', 'timeseries', [
        (g_impute, 'Imputation and Estimation', 15, 'Imputation · Reconstruction · Estimation', 'Error Against Observed Values'),
        (g_forecast, 'Value Forecasting', 74, 'Point and Probabilistic Forecasts', 'Error · Proper Scoring Rules')]),
    ('Classification', 'anomaly', [
        (g_detect, 'Classification and Detection', 65, ['Classification · Anomaly Detection', 'Root Cause · Closed Questions'],
         'Accuracy · F1 · AUC'),
        (g_event, 'Event Forecasting', 14, 'Event Label · Event Probability', 'Accuracy · Brier Score')]),
    ('Generation', 'synthesis', [
        (g_describe, 'Description and Synthesis', 40, ['Open Questions · Explanation', 'Annotation · Synthesis'],
         'Quality · Fidelity · Use'),
        (g_projection, 'Projection', 0, 'Futures Under Assumed Conditions', 'No Realized Future to Score')]),
    ('Decision Making', 'decision', [
        (g_hindsight, 'Hindsight Decision', 0, 'Action That Should Have Been Taken', 'Replay · Counterfactual Estimate'),
        (g_decide, 'Decision', 46, 'Advisory Decision · Autonomous Control', 'Utility · Cost · Risk')]),
]


def cell(slide, x, y, spec):
    glyph, name, n, tasks, check = spec
    g = group(slide); sh = g.shapes
    empty = n == 0
    if empty:
        box(sh, x, y, CW, RH, fill=EVl, line=EVm, lw=1.4, radius=0.08, dash=MSO_LINE.DASH)
    else:
        card(sh, x, y, CW, RH, 'tsk')
    glyph(sh, x + 0.16, y + (RH - GH) / 2)
    tx0, tw = x + 0.16 + GW + 0.18, CW - GW - 0.42
    T(sh, tx0, y + 0.1, tw, 0.36, name if empty else f'{name} ({n})', size=15.5, color=EV if empty else TK, align='l')
    lines = tasks if isinstance(tasks, list) else [tasks]
    T(sh, tx0, y + 0.48, tw, 0.24 * len(lines) + 0.04, lines, size=12.5, bold=False, color=INK, align='l', anchor='t')
    cy = y + RH - 0.44
    b = box(sh, tx0, cy, tw, 0.32, fill=EVl if not empty else 'FFFFFF', line=EVm, lw=0.9, radius=0.5)
    T(sh, tx0 + 0.12, cy, tw - 0.2, 0.32, check, size=12.5, color=EV, align='l')
    if empty:
        p = box(sh, x + CW - 1.5, y + 0.12, 1.36, 0.3, fill=EV, radius=0.5); label_in(p, 'Open Problem', size=12.5)
    return g


def build(out):
    p, slide = new_slide(H)
    g = group(slide); sh = g.shapes
    # column banners
    for k, (t, key) in enumerate((('Observed Record', 'data'), ('After the Current Time', 'tsk'))):
        banner(sh, CX[k] + CW / 2, 0.22, 3.6, t, HUE[key][0], size=18, h=0.48)
    # Now divider
    arrow(sh, DIV, 0.82, DIV, RY[-1] + RH + 0.05, color=GT, lw=2.0, dash=MSO_LINE.DASH, head=None)
    pn = box(sh, DIV - 0.36, 0.3, 0.72, 0.32, fill=GT, radius=0.5); label_in(pn, 'Now', size=14)
    # row headers
    for (mode, icon, cells), y in zip(ROWS, RY):
        h = group(slide).shapes
        b = box(h, X0, y, HW, RH, fill=ZONE_FILL['tsk'], radius=0.08)
        ic(h, icon, X0 + (HW - 0.62) / 2, y + 0.2, 0.62)
        T(h, X0, y + 0.9, HW, 0.5, mode, size=15.5, color=TK)
        for k, spec in enumerate(cells):
            cell(slide, CX[k], y, spec)
    save(p, out)
    for w in WARN: print('WARN', w)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'Figure08_V7.pptx'))
