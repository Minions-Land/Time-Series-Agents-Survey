"""Figure 4 (fig:task-function-grid), V7 house style: from task requirements to Harness modules.

(a) Columns are the four output modes of the task grid (scripts/task_groups.py, Section 6), rows the four temporal
functions (Section 5). Each cell
names what that function supplies for that task (wording kept from the approved semantic revision, Figure04_Semantic).
Shaded regions with solid boundaries mark the forecast horizon, the diagnostic interval, the information beyond the
forecast origin t0 and the admissible action range, as the caption states.
(b) Assembling a demand-planning Agent cell by cell: general execution and shared temporal preparation serve any cell;
forecasting (regression after the current time) and the inventory decision (decision after the current time) are
task modules. Each step is tagged with its Harness layer and its cell.

usage: python3 build_fig04.py [out.pptx]
"""
import os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *   # noqa: F401,F403
from v7kit import _y, _calm

HERE = os.path.dirname(os.path.abspath(__file__))
H = 7.5

# ---- grid geometry (inches) ---------------------------------------------------------------------------------
GX0, GX1 = 0.40, 12.95          # grid extent inside zone (a)
RH_W = 2.55                     # row-header width
GAP = 0.07
CW = (GX1 - GX0 - RH_W - 4 * GAP) / 4
HDR_Y, HDR_H = 0.80, 0.90       # column-header row
ROW_Y, ROW_H = 1.78, 0.70


def col_x(j):
    return GX0 + RH_W + GAP + j * (CW + GAP)


def row_y(i):
    return ROW_Y + i * (ROW_H + GAP)


# Task groups (scripts/task_groups.py, ORDER) and their clay icons; header lines as displayed.
TASKS = [('timeseries', ['Regression']), ('anomaly', ['Classification']), ('synthesis', ['Generation']),
         ('decision', ['Decision', 'Making'])]
# Shared temporal functions (Section 5 headings), icons as on the General Time Series Harness plate of Figure 1.
FUNCS = [('calendar', ['Temporal Data', 'Management']), ('window', ['Temporal', 'Processing']),
         ('timeline', ['Temporal Context', 'and Memory']), ('cutoff', ['Temporal', 'Validation'])]
# Cell content: (glyph, label) per output mode. Regression: forecasting and imputation needs; Classification: labeled
# windows, candidate intervals, exemplars (FETA, MarsTSC) and evidence; Generation: synthesis and description
# (transforms and series views, references, fidelity and claim checks); Decision Making: state, actions, experience.
CELLS = [
    [('history', 'History'), ('streams', ['Labeled', 'Windows']), ('icon:data', 'Samples'), ('icon:inventory_stock', 'State')],
    [('horizon', 'Horizon'), ('interval', 'Intervals'), ('transforms', ['Transforms', 'and Views']), ('icon:policy', 'Actions')],
    [('events', 'Events'), ('icon:papers', 'Exemplars'), ('icon:reference_lookup', 'References'),
     ('icon:memory', 'Experience')],
    [('cutoff', 'Cutoff'), ('icon:evidence_check', 'Evidence'), ('fidelity', ['Fidelity', 'and Claims']), ('constraints', 'Constraints')],
]
TK, TS = HUE['tsk'], HUE['gts']


# ---- cell glyphs: (x, y, w, h) is the glyph box -------------------------------------------------------------
def spike_series(x, y, w, h, at=0.58, n=80):
    pts = []
    for k in range(n + 1):
        t = k / n
        v = 0.12 * math.sin(2 * math.pi * t * 6.3) + 0.06 * math.sin(2 * math.pi * t * 15.1 + 0.7)
        v += 0.95 * math.exp(-((t - at) / 0.05) ** 2)
        pts.append((x + w * t, y + h * 0.78 - h * 0.62 * v))
    return pts


def shaded(sh, x0, x1, y0, y1, key, fill=None, alpha=70):
    """Pale region with solid boundaries on both sides."""
    r = box(sh, x0, y0, x1 - x0, y1 - y0, fill=fill or HUE[key][2], shape=MSO_SHAPE.RECTANGLE)
    alpha_fill(r, alpha)
    for xx in (x0, x1):
        arrow(sh, xx, y0, xx, y1, color=HUE[key][0], lw=1.6, head=None)


def t0_pill(sh, x, y):
    p = box(sh, x - 0.29, y, 0.58, 0.22, fill=TS[0], radius=0.5)   # the current time (Now)
    runs(p, [('Now', 'FFFFFF', True, False)], 12)


def glyph(sh, kind, x, y, w, h):
    if kind.startswith('icon:'):
        s = 0.6
        ic(sh, kind[5:], x + (w - s) / 2, y + (h - s) / 2, s)
    elif kind == 'history':
        series(sh, x, y, w, h, INK, phase=0.05, lw=1.7)
    elif kind == 'streams':                       # several channels observed together
        for k, (col, ph) in enumerate([(INK, 0.0), (TS[0], 0.31), (HUE['gh'][0], 0.62)]):
            series(sh, x, y - 0.03 + k * h / 2.6, w, h / 2.4, col, phase=ph, amp=0.85, lw=1.4)
    elif kind == 'horizon':                       # forecast horizon after the history
        x0 = x + 0.6 * w
        shaded(sh, x0, x + w, y - 0.04, y + h + 0.04, 'tsk')
        series(sh, x, y, w, h, INK, phase=0.2, lw=1.6)
    elif kind == 'transforms':                    # a sample and its transformed view
        series(sh, x, y + 0.03, 0.36 * w, h - 0.06, INK, phase=0.1, lw=1.5, smooth=True, span=0.3)
        arrow(sh, x + 0.4 * w, y + h / 2, x + 0.6 * w, y + h / 2, color=TK[0], lw=1.8)
        series(sh, x + 0.64 * w, y + 0.03, 0.36 * w, h - 0.06, TK[0], phase=0.15, amp=1.35, lw=1.5, span=0.3)
    elif kind == 'interval':                      # diagnostic interval around an anomaly
        shaded(sh, x + 0.45 * w, x + 0.72 * w, y - 0.04, y + h + 0.04, 'tsk')
        poly(sh, spike_series(x, y, w, h), INK, lw=1.6)
    elif kind == 'events':                        # dated events placed on the series
        series(sh, x, y + 0.08, w, h - 0.08, INK, phase=0.4, lw=1.5)
        for fx in (0.3, 0.72):
            xx = x + fx * w
            arrow(sh, xx, y - 0.04, xx, y + h + 0.03, color=HUE['llm'][0], lw=1.3, dash=MSO_LINE.DASH, head=None)
            poly(sh, [(xx, y - 0.06), (xx + 0.14, y - 0.0), (xx, y + 0.06)], HUE['llm'][0], lw=1.0,
                 fill=HUE['llm'][1], closed=True)
    elif kind == 'cutoff':                        # information beyond the forecast origin t0
        y, h = y - 0.11, h - 0.06
        t0 = x + 0.58 * w
        box(sh, t0, y - 0.04, x + w - t0, h + 0.08, fill='DCE1EA', shape=MSO_SHAPE.RECTANGLE)
        pts = series_pts(x, y, w, h, phase=0.66)
        k0 = max(i for i, p in enumerate(pts) if p[0] <= t0)
        poly(sh, pts[:k0 + 1], INK, lw=1.6)
        poly(sh, pts[k0:], 'A3ABBA', lw=1.4, dash=MSO_LINE.ROUND_DOT)
        arrow(sh, t0, y - 0.07, t0, y + h + 0.05, color=TS[0], lw=1.8, head=None)
        t0_pill(sh, t0, y + h + 0.04)
    elif kind == 'fidelity':                      # generated sample against the observed one
        series(sh, x, y, w, h, INK, phase=0.12, lw=1.8, smooth=True, span=0.42)
        series(sh, x, y + 0.05, w, h, TK[0], phase=0.135, amp=0.85, lw=1.8, smooth=True,
               span=0.42).line.dash_style = MSO_LINE.DASH
    elif kind == 'constraints':                   # admissible action range
        cy = y + h / 2
        arrow(sh, x, cy, x + w, cy, color='A3ABBA', lw=1.2, head=None)
        shaded(sh, x + 0.2 * w, x + 0.8 * w, cy - 0.15, cy + 0.15, 'gts', alpha=85)
        d = box(sh, x + 0.48 * w - 0.065, cy - 0.065, 0.13, 0.13, fill=INK, shape=MSO_SHAPE.OVAL)


def series_pts(x, y, w, h, phase=0.0, amp=1.0, smooth=False, n=90, span=0.5):
    """The kit's deterministic series, returned as points; span < 1 shows a slice so a small glyph stays legible."""
    f = _calm if smooth else _y
    return [(x + w * k / n, y + h / 2 - h / 2.6 * amp * f((phase + span * k / n) % 1.0)) for k in range(n + 1)]


def series(sh, x, y, w, h, color=INK, phase=0.0, amp=1.0, lw=1.6, smooth=False, span=0.5):   # noqa: F811
    """kit series() on a slice, returning the shape so a dash can be applied."""
    return poly(sh, series_pts(x, y, w, h, phase, amp, smooth, span=span), color, lw=lw)


# ---- panel (a) ------------------------------------------------------------------------------------------------
def panel_a(slide):
    zone(slide, 0.2, 0.42, W - 0.4, 4.56, '(a)  Output Modes × Temporal Functions', key='ink', size=18, bw=6.4)
    # reading key in the empty corner
    g = group(slide); sh = g.shapes
    x, y = GX0 + 0.12, HDR_Y + 0.08
    arrow(sh, x + 0.16, y + 0.02, x + 0.16, y + 0.36, color=TK[0], lw=2.8)
    tx(sh, x + 0.42, y, 2.0, 0.38, 'Column: Assemble', size=14, bold=True, color=TK[0], align='l')
    arrow(sh, x, y + 0.6, x + 0.34, y + 0.6, color=TS[0], lw=2.8)
    tx(sh, x + 0.42, y + 0.41, 2.0, 0.38, 'Row: Compare', size=14, bold=True, color=TS[0], align='l')
    # task-group column headers: icon on the left, the group name (one or two lines) beside it
    g = group(slide); sh = g.shapes
    for j, (nm, lab) in enumerate(TASKS):
        x = col_x(j)
        b = box(sh, x, HDR_Y, CW, HDR_H, fill=TK[2], line=TK[1], lw=1.2, radius=0.12); shadow(b)
        ic(sh, nm, x + 0.08, HDR_Y + (HDR_H - 0.56) / 2, 0.56)
        tx(sh, x + 0.66, HDR_Y + 0.04, CW - 0.7, HDR_H - 0.08, lab, size=14, bold=True, color=TK[0])
    # rows: function header + four cells
    for i, (nm, lab) in enumerate(FUNCS):
        g = group(slide); sh = g.shapes
        y = row_y(i)
        b = box(sh, GX0, y, RH_W, ROW_H, fill=TS[2], line=TS[1], lw=1.2, radius=0.14); shadow(b)
        ic(sh, nm, GX0 + 0.08, y + (ROW_H - 0.56) / 2, 0.56)
        tx(sh, GX0 + 0.68, y + 0.03, RH_W - 0.72, ROW_H - 0.06, lab, size=14, bold=True, color=TS[0], align='l')
        for j, (kind, cap) in enumerate(CELLS[i]):
            x = col_x(j)
            card(sh, x, y, CW, ROW_H, key='ink', radius=0.12)
            glyph(sh, kind, x + 0.16, y + 0.17, 0.92, ROW_H - 0.36)
            tx(sh, x + 1.2, y, CW - 1.24, ROW_H, cap, size=14, bold=True, color=INK, align='l')


# ---- panel (b) ------------------------------------------------------------------------------------------------
BY, BH = 5.66, 1.55
STEPS = [  # (title, layer key, layer name, width, cell)
    ('Execute', 'gh', 'General Harness', 2.25, 'Any Cell'),
    ('Prepare', 'gts', 'General Time Series Harness', 3.2, 'Any Cell'),
    ('Forecast', 'tsk', 'Task-Specific Harness', 3.05, 'Regression · After'),
    ('Decide', 'tsk', 'Task-Specific Harness', 2.55, 'Decision · After'),
]


def pair(sh, names, cx, y, col, s=0.62, span=1.15):
    """Two icons centred on cx with a short arrow between them."""
    x0 = cx - span / 2 - s / 2
    ic(sh, names[0], x0, y, s)
    ic(sh, names[1], x0 + span, y, s)
    arrow(sh, x0 + s + 0.06, y + s / 2, x0 + span - 0.06, y + s / 2, color=col, lw=2.2)


def panel_b(slide):
    zone(slide, 0.2, BY - 0.3, W - 0.4, BH + 0.48, '(b)  Assembling a Demand-Planning Agent by Cell', key='data', size=18)
    gapw = (GX1 - GX0 - sum(s[3] for s in STEPS)) / 3
    x = GX0
    xs = []
    for k, (title, key, layer, w, cellname) in enumerate(STEPS):
        g = group(slide); sh = g.shapes
        dk, md, lt = HUE[key]
        card(sh, x, BY, w, BH, key=key, radius=0.1)
        tx(sh, x + 0.16, BY + 0.06, w - 0.3, 0.36, title, size=16.5, bold=True, color=dk, align='l')
        tx(sh, x + 0.16, BY + 0.08, w - 0.3, 0.34, cellname, size=12.5, bold=True, color=MUTE, align='r')
        pill(sh, x + 0.14, BY + BH - 0.42, w - 0.28, 0.32, layer, key=key, size=12.5, light=True)
        mid = BY + 0.43
        if title == 'Execute':
            pair(sh, ('tools', 'runtime'), x + w / 2, mid, dk)
        elif title == 'Prepare':
            pair(sh, ('window', 'timeline'), x + w / 2, mid, dk, span=1.25)
        elif title == 'Forecast':
            fx, fw = x + 0.25, w - 0.5
            t0 = mini_forecast(sh, fx, mid - 0.04, fw, 0.38, cut=0.55, t0_label=True)
            tx(sh, fx, mid + 0.36, t0 - fx - 0.24, 0.26, 'History', size=12.5, bold=True, color=MUTE)
            tx(sh, t0 + 0.24, mid + 0.36, fx + fw - t0 - 0.24, 0.26, 'Forecast', size=12.5, bold=True, color=dk)
        elif title == 'Decide':
            pair(sh, ('inventory_stock', 'decision'), x + w / 2, mid, dk)
        xs.append((x, w, dk))
        x += w + gapw
    g = group(slide); sh = g.shapes
    for (x0, w0, col), (x1, _, _) in zip(xs, xs[1:]):
        arrow(sh, x0 + w0 + 0.08, BY + BH / 2, x1 - 0.08, BY + BH / 2, color=col, lw=2.8)


def build(out):
    p, slide = new_slide(H)
    panel_a(slide)
    panel_b(slide)
    save(p, out)
    return out


if __name__ == '__main__':
    print(build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'Figure04_V7.pptx')))
