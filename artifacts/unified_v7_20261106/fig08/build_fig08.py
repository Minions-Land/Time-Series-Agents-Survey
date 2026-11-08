"""Figure 8 (fig:task-specific-harness), V7 house style.

Four task panels, one per task group (scripts/task_groups.py, in its order: Analysis of Observed Series, Forecasting,
Generation, Decision Making); the Analysis of Observed Series panel uses anomaly diagnosis with a localized interval. Each panel reads from the input series through the procedure to the resulting
artifact; dashed indigo paths are feedback that revises the procedure; the indigo strip at the bottom names the
evaluation target.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit')))
from v7kit import *
from PIL import ImageFont

H = 8.5
MATH = 'Times New Roman'
TK, TKm, TKl = HUE['tsk']
EV, EVm, EVl = HUE['ev']
SD, SDm, SDl = HUE['data']
PW, PH = 6.366, 3.72
PX = [0.2, 0.2 + PW + 0.2]
PY = [0.42, 0.42 + PH + 0.5]
FONTS = {False: '/System/Library/Fonts/Supplemental/Comic Sans MS.ttf',
         True: '/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf'}
WARN = []


def width(t, size, bold):
    return ImageFont.truetype(FONTS[bold], int(size * 20)).getlength(t) / (20 * 72)


def T(sh, x, y, w, h, t, size=13, bold=True, color=INK, align='c', anchor='m', italic=False):
    assert size >= 11.5, (t, size)
    for ln in (t if isinstance(t, list) else [t]):
        if width(ln, size, bold) > w - 0.04: WARN.append(f'overflow {ln!r} {width(ln, size, bold):.2f} > {w:.2f}')
    return tx(sh, x, y, w, h, t, size=size, bold=bold, color=color, align=align, anchor=anchor, italic=italic)


def dot(sh, cx, cy, r, fill, line=None):
    return box(sh, cx - r, cy - r, 2 * r, 2 * r, fill=fill, line=line, lw=1.0, shape=MSO_SHAPE.OVAL)


def pline(sh, x, y, w, h, vals, color=INK, lw=1.6, dash=None):
    n = len(vals) - 1
    pts = [(x + w * k / n, y + h * (1 - v)) for k, v in enumerate(vals)]
    poly(sh, pts, color, lw=lw, dash=dash)
    return pts


def head(shape):
    e = etree.SubElement(shape.line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle'); e.set('w', 'med'); e.set('len', 'med')
    return shape


def go(sh, pts, color=TK, lw=2.0, dash=None, tip=True):
    """Orthogonal (or any) polyline arrow through pts."""
    s = poly(sh, pts, color, lw=lw, dash=dash)
    return head(s) if tip else s


def fb(sh, pts):
    return go(sh, pts, color=EV, lw=2.2, dash=MSO_LINE.DASH)


def step(sh, x, y, w, label, icon=None, h=0.5, size=13, cy=None):
    """Procedure card: (x, y) top-left, or centred vertically on cy."""
    if cy is not None: y = cy - h / 2
    c = card(sh, x, y, w, h, key='tsk', lw=1.3, radius=0.22)
    if icon:
        ic(sh, icon, x + 0.06, y + (h - 0.42) / 2, 0.42)
        T(sh, x + 0.5, y, w - 0.54, h, label, size=size, align='c')
    else:
        T(sh, x, y, w, h, label, size=size)
    return c


def sheet(sh, x, y, w, h, vals, color=INK, n=2):
    """Input series on a small stack of paper."""
    paper(sh, x, y, w, h, line='B9A98A', n=n)
    pline(sh, x + 0.08, y + 0.1, w - 0.16, h - 0.2, vals, color, lw=1.6)


def caption(sh, cx, y, t, w=1.3, color=MUTE, size=13):
    return T(sh, cx - w / 2, y, w, 0.26, t, size=size, color=color)


def evaluation(sh, u, v, t):
    b = box(sh, u + 0.15, v + 3.2, PW - 0.3, 0.4, fill=EVl, line=EVm, lw=1.0, radius=0.5)
    p = box(sh, u + 0.2, v + 3.24, 1.2, 0.32, fill=EV, radius=0.5)
    label_in(p, 'Evaluation', size=13)
    T(sh, u + 1.45, v + 3.2, PW - 1.7, 0.4, t, size=13.5, color=EV, align='l')


def panel(slide, i, j, title, hero):
    u, v = PX[j], PY[i]
    zone(slide, u, v, PW, PH, title, 'tsk')
    g = group(slide); sh = g.shapes
    ic(sh, hero, u + 0.12, v - 0.33, 0.64)
    return g, sh, u, v


def fc_glyph(sh, x, y, w, h, cut=0.55):
    """History (ink) up to t0, then a dashed forecast inside a widening band; returns t0."""
    hist = [0.25, 0.5, 0.35, 0.58, 0.42, 0.66, 0.5, 0.62]
    fut = [0.62, 0.74, 0.6, 0.8, 0.66, 0.86]
    t0 = x + w * cut
    hp = [(x + (t0 - x) * k / (len(hist) - 1), y + h * (1 - v)) for k, v in enumerate(hist)]
    fp = [(t0 + (x + w - t0) * k / (len(fut) - 1), y + h * (1 - v)) for k, v in enumerate(fut)]
    m = len(fut) - 1
    up = [(px, py - 0.02 - 0.13 * k / m) for k, (px, py) in enumerate(fp)]
    lo = [(px, py + 0.02 + 0.13 * k / m) for k, (px, py) in enumerate(fp)]
    poly(sh, up + lo[::-1], None, fill=TK, alpha=22, closed=True)
    poly(sh, hp, INK, lw=1.6)
    poly(sh, fp, TK, lw=1.8, dash=MSO_LINE.DASH)
    arrow(sh, t0, y - 0.08, t0, y + h + 0.04, color=HUE['gts'][0], lw=1.3, dash=MSO_LINE.DASH, head=None)
    p = box(sh, t0 - 0.29, y + h + 0.04, 0.58, 0.25, fill=HUE['gts'][0], radius=0.5)   # forecast origin = current time (Now)
    tf = p.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    r = tf.paragraphs[0].add_run(); r.text = 'Now'; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r.font.size = Pt(12); r.font.bold = True; r.font.name = F; r.font.color.rgb = rgb('FFFFFF')
    return t0


SER = [0.35, 0.55, 0.4, 0.7, 0.5, 0.62, 0.45, 0.8, 0.55, 0.72, 0.5, 0.66]


# ------------------------------------------------------------------------------------------------ forecasting
def forecasting(slide):
    g, sh, u, v = panel(slide, 0, 1, 'Forecasting', 'forecast')
    ya, yb = v + 1.22, v + 2.6
    # history -> select models -> baseline -> revise (+context) -> revised forecast with its horizon
    sheet(sh, u + 0.18, ya - 0.3, 0.92, 0.6, SER)
    caption(sh, u + 0.64, ya + 0.33, 'History')
    arrow(sh, u + 1.2, ya, u + 1.4, ya, color=TK, lw=2.0)
    card(sh, u + 1.42, ya - 0.5, 1.34, 1.0, key='tsk', lw=1.3, radius=0.15)
    T(sh, u + 1.42, ya - 0.47, 1.34, 0.34, 'Select Models', size=13)
    for k in range(3):
        c = box(sh, u + 1.49 + k * 0.41, ya + 0.0, 0.38, 0.34, fill=TKl, line=TKm, lw=1.0, radius=0.3)
        runs(c, [('M', TK, True, False), (str(k + 1), TK, True, True)], 13)
    arrow(sh, u + 2.78, ya, u + 2.96, ya, color=TK, lw=2.0)
    pline(sh, u + 3.0, ya - 0.28, 0.62, 0.42, [0.2, 0.35, 0.3, 0.5, 0.45, 0.65, 0.6, 0.8], INK, lw=1.6)
    caption(sh, u + 3.31, ya + 0.33, 'Baseline')
    arrow(sh, u + 3.66, ya, u + 3.84, ya, color=TK, lw=2.0)
    step(sh, u + 3.86, 0, 0.84, 'Revise', cy=ya)
    p = box(sh, u + 3.78, v + 0.42, 1.0, 0.34, fill=SDl, line=SDm, lw=1.2, radius=0.5); shadow(p)
    label_in(p, 'Context', size=13, color=INK)
    arrow(sh, u + 4.28, v + 0.77, u + 4.28, ya - 0.26, color=SD, lw=2.0)
    arrow(sh, u + 4.72, ya, u + 4.9, ya, color=TK, lw=2.0)
    fx, fw = u + 4.95, 1.1
    t0 = fc_glyph(sh, fx, ya - 0.27, fw, 0.5, cut=0.46)
    caption(sh, fx + fw / 2 - 0.12, ya + 0.5, 'Revised', w=1.0)
    yh = ya - 0.42   # horizon bracket over the forecast part
    poly(sh, [(t0 + 0.02, yh + 0.06), (t0 + 0.02, yh), (fx + fw, yh), (fx + fw, yh + 0.06)], TK, lw=1.4)
    T(sh, (t0 + fx + fw) / 2 - 0.5, yh - 0.29, 1.0, 0.26, 'Horizon', size=12.5, color=TK)
    # event prediction
    arrow(sh, u + 0.64, ya + 0.6, u + 0.64, yb - 0.27, color=TK, lw=2.0)
    step(sh, u + 0.18, 0, 1.86, 'Predict Event', icon='timeline', cy=yb)
    arrow(sh, u + 2.06, yb, u + 2.26, yb, color=TK, lw=2.0)
    box(sh, u + 2.32, yb - 0.27, 0.24, 0.5, fill='FFFFFF', line=TKm, lw=1.0, shape=MSO_SHAPE.RECTANGLE)
    box(sh, u + 2.32, yb - 0.27 + 0.5 * 0.3, 0.24, 0.5 * 0.7, fill=TK, shape=MSO_SHAPE.RECTANGLE)
    arrow(sh, u + 2.26, yb + 0.23, u + 2.62, yb + 0.23, color=MUTE, lw=1.2, head=None)
    T(sh, u + 2.62, yb - 0.15, 1.05, 0.3, 'Probability', size=13, color=MUTE, align='l')
    # feedback: observed error -> refine prompt -> revise
    rx = u + 3.88
    step(sh, rx, 0, 1.9, 'Refine Prompt', icon='document', cy=yb)
    fb(sh, [(fx + fw + 0.08, ya), (fx + fw + 0.08, yb), (rx + 1.92, yb)])
    T(sh, u + 4.4, yb + 0.28, 1.7, 0.26, 'Observed Error', size=13, italic=True, color=EV, align='r')
    fb(sh, [(u + 4.28, yb - 0.27), (u + 4.28, ya + 0.27)])
    evaluation(sh, u, v, 'Forecast Error · Calibration')
    return g


# ------------------------------------------------------------------------------------------------ generation
def synthesis(slide):
    g, sh, u, v = panel(slide, 1, 0, 'Generation', 'synthesis')
    ys = [v + 0.98, v + 1.78, v + 2.58]
    sheet(sh, u + 0.18, ys[1] - 0.3, 0.86, 0.6, SER[::-1])
    caption(sh, u + 0.61, ys[1] + 0.33, 'Examples')
    bx = u + 1.24
    arrow(sh, u + 1.1, ys[1], bx, ys[1], color=TK, lw=2.0, head=None)
    poly(sh, [(bx, ys[0]), (bx, ys[2])], TK, lw=2.0)
    c1, c2 = u + 1.4, u + 3.02
    for y, a, b in ((ys[0], 'Set Conditions', 'Generator'), (ys[1], 'Configure', 'Transform'), (ys[2], 'Write Q&A', None)):
        arrow(sh, bx, y, c1 - 0.02, y, color=TK, lw=2.0)
        step(sh, c1, 0, 1.44, a, cy=y)
        arrow(sh, c1 + 1.46, y, c2 - 0.02, y, color=TK, lw=2.0)
        if b: step(sh, c2, 0, 1.08, b, cy=y)
    # generated samples, transformed views, Q/A pairs
    sx, sw, mx = u + 4.2, 0.42, u + 4.74
    for k, y in enumerate(ys[:2]):
        arrow(sh, c2 + 1.1, y, sx - 0.04, y, color=TK, lw=2.0, head=None)
        n = 3 - k
        for m in range(n):
            yy = y - 0.075 * (n - 1) + m * 0.15
            pts = [(sx + sw * q / 24, yy - 0.05 * math.sin(2 * math.pi * (q / 24 * 1.6 + 0.3 * m))) for q in range(25)]
            poly(sh, pts, [INK, TK, HUE['gts'][0]][m], lw=1.5)
        arrow(sh, sx + sw + 0.04, y, mx, y, color=TK, lw=2.0, head=None)
    for k, (q, yy) in enumerate((('Q', ys[2] - 0.15), ('A', ys[2] + 0.15))):
        c = box(sh, c2 + 0.08 * k, yy - 0.12, 0.98, 0.25, fill='FFFFFF', line=TKm, lw=1.0, radius=0.3); shadow(c)
        T(sh, c2 + 0.08 * k + 0.04, yy - 0.12, 0.3, 0.25, q, size=12.5, color=TK)
        arrow(sh, c2 + 0.08 * k + 0.34, yy, c2 + 0.08 * k + 0.86, yy, color=MUTE, lw=1.2, head=None)
    arrow(sh, c2 + 1.1, ys[2], mx, ys[2], color=TK, lw=2.0, head=None)
    poly(sh, [(mx, ys[0]), (mx, ys[2])], TK, lw=2.0)
    rx = u + 4.88
    arrow(sh, mx, ys[1], rx - 0.02, ys[1], color=TK, lw=2.0)
    step(sh, rx, 0, 1.34, 'Review', icon='evidence_check', cy=ys[1])
    arrow(sh, rx + 0.67, ys[1] + 0.27, rx + 0.67, ys[2] - 0.29, color=TK, lw=2.0)
    step(sh, rx, 0, 1.34, 'Learner', icon='learner', cy=ys[2])
    # refine loop back to the conditions
    yt = v + 0.46
    fb(sh, [(rx + 1.1, ys[1] - 0.27), (rx + 1.1, yt), (c1 + 0.72, yt), (c1 + 0.72, ys[0] - 0.27)])
    T(sh, rx + 0.2, yt + 0.04, 0.84, 0.28, 'Refine', size=13, italic=True, color=EV, align='r')
    evaluation(sh, u, v, 'Fidelity · Downstream Learning Utility')
    return g


# ------------------------------------------------------------------------------------------------ analysis of observed series
def anomaly(slide):
    g, sh, u, v = panel(slide, 0, 0, 'Analysis of Observed Series', 'anomaly')
    ya, yb = v + 1.6, v + 2.62
    spike = [0.35, 0.45, 0.3, 0.42, 0.36, 0.5, 0.95, 0.4, 0.38, 0.5, 0.33, 0.45]
    sheet(sh, u + 0.18, ya - 0.3, 0.9, 0.6, spike)
    caption(sh, u + 0.63, ya + 0.33, 'Series')
    # choose probes -> diagnostics / detector -> refine intervals -> intervals
    dx, dw = u + 1.42, 1.2
    step(sh, dx + 0.6 - 0.95, v + 0.44, 1.9, 'Choose Probes', icon='reference_lookup', h=0.48)
    arrow(sh, dx + 0.6, v + 0.93, dx + 0.6, ya - 0.52, color=TK, lw=2.0)
    fx = u + 1.26
    arrow(sh, u + 1.14, ya, fx, ya, color=TK, lw=2.0, head=None)
    poly(sh, [(fx, ya - 0.27), (fx, ya + 0.27)], TK, lw=2.0)
    for y, lab in ((ya - 0.27, 'Diagnostics'), (ya + 0.27, 'Detector')):
        arrow(sh, fx, y, dx - 0.02, y, color=TK, lw=2.0)
        step(sh, dx, 0, dw, lab, h=0.44, cy=y)
        arrow(sh, dx + dw + 0.02, y, dx + dw + 0.16, y, color=TK, lw=2.0, head=None)
    mx = dx + dw + 0.16
    poly(sh, [(mx, ya - 0.27), (mx, ya + 0.27)], TK, lw=2.0)
    rx = mx + 0.16
    arrow(sh, mx, ya, rx - 0.02, ya, color=TK, lw=2.0)
    step(sh, rx, 0, 1.62, 'Refine Intervals', cy=ya)
    arrow(sh, rx + 1.64, ya, rx + 1.82, ya, color=TK, lw=2.0)
    ix, iw = rx + 1.86, 1.0
    b = box(sh, ix + 0.42, ya - 0.34, 0.26, 0.62, fill=TK, line=TK, lw=1.0, dash=MSO_LINE.DASH, shape=MSO_SHAPE.RECTANGLE)
    alpha_fill(b, 18)
    pline(sh, ix, ya - 0.3, iw, 0.52, [0.3, 0.42, 0.28, 0.4, 0.35, 0.55, 0.95, 0.45, 0.3, 0.42, 0.32], INK, lw=1.6)
    caption(sh, ix + iw / 2, ya + 0.32, 'Intervals', w=1.0)
    # build detector from data / labels
    p = box(sh, u + 0.14, yb - 0.18, 1.42, 0.36, fill=SDl, line=SDm, lw=1.2, radius=0.5); shadow(p)
    T(sh, u + 0.14, yb - 0.18, 1.42, 0.36, 'Data / Labels', size=12.5, color=INK)
    bx = u + 1.72
    arrow(sh, u + 1.58, yb, bx - 0.02, yb, color=TK, lw=2.0)
    step(sh, bx, 0, 1.5, 'Build Detector', cy=yb)
    arrow(sh, dx + 0.6, yb - 0.27, dx + 0.6, ya + 0.5, color=TK, lw=2.0)
    # diagnose with logs -> candidate causes
    gx = u + 3.4
    ic(sh, 'logs', gx, yb - 0.3, 0.46)
    T(sh, gx - 0.17, yb + 0.15, 0.8, 0.26, 'Logs', size=12.5, color=MUTE)
    qx = u + 4.12
    arrow(sh, gx + 0.5, yb, qx - 0.02, yb, color=TK, lw=2.0)
    step(sh, qx, 0, 1.0, 'Diagnose', cy=yb)
    arrow(sh, ix + 0.3, ya + 0.6, ix + 0.3, yb - 0.27, color=TK, lw=2.0)
    arrow(sh, qx + 1.02, yb, qx + 1.14, yb, color=TK, lw=2.0)
    c = box(sh, qx + 1.16, yb - 0.36, 0.94, 0.72, fill='FFFFFF', line=TK, lw=1.3, dash=MSO_LINE.DASH, radius=0.12)
    T(sh, qx + 1.16, yb - 0.34, 0.94, 0.68, ['Cause A?', 'Cause B?'], size=12.5, bold=True, color=TK)
    evaluation(sh, u, v, 'Detection · Validation of Proposed Causes')
    return g


# ------------------------------------------------------------------------------------------------ decision making
def decision(slide):
    g, sh, u, v = panel(slide, 1, 1, 'Decision Making', 'decision')
    ya, yb, yr = v + 1.2, v + 2.34, v + 2.98
    sheet(sh, u + 0.26, ya - 0.3, 0.84, 0.6, SER)
    caption(sh, u + 0.68, ya + 0.33, 'State')
    ic(sh, 'memory', u + 0.43, yb - 0.32, 0.5)
    caption(sh, u + 0.68, yb + 0.17, 'Memory', w=1.0)
    rx = u + 1.34
    arrow(sh, u + 1.18, ya, rx - 0.02, ya, color=TK, lw=2.0)
    step(sh, rx, 0, 0.94, 'Retrieve', cy=ya)
    go(sh, [(u + 0.97, yb - 0.07), (rx + 0.47, yb - 0.07), (rx + 0.47, ya + 0.27)])
    px = rx + 1.1
    arrow(sh, rx + 0.96, ya, px - 0.02, ya, color=TK, lw=2.0)
    step(sh, px, 0, 1.5, 'Predict Futures', cy=ya)
    fx = px + 1.62
    arrow(sh, px + 1.54, ya, fx, ya, color=TK, lw=2.0, head=None)
    poly(sh, [(fx, ya - 0.45), (fx, ya + 0.45)], TK, lw=2.0)
    ax, aw = fx + 0.44, 0.5
    mx = ax + aw + 0.1
    for y, lab, vals, dash in ((ya - 0.45, 'A', [0.2, 0.35, 0.3, 0.55, 0.5, 0.8], None),
                               (ya + 0.45, 'B', [0.7, 0.6, 0.65, 0.4, 0.45, 0.2], MSO_LINE.DASH)):
        arrow(sh, fx, y, fx + 0.1, y, color=TK, lw=2.0, head=None)
        c = box(sh, fx + 0.1, y - 0.15, 0.3, 0.3, fill='FFFFFF', line=TK, lw=1.4, shape=MSO_SHAPE.OVAL)
        runs(c, [(lab, TK, True, False)], 12.5)
        pline(sh, ax, y - 0.16, aw, 0.32, vals, INK, lw=1.6, dash=dash)
        arrow(sh, ax + aw + 0.02, y, mx, y, color=TK, lw=2.0, head=None)
    poly(sh, [(mx, ya - 0.45), (mx, ya + 0.45)], TK, lw=2.0)
    sx = mx + 0.14
    arrow(sh, mx, ya, sx - 0.02, ya, color=TK, lw=2.0)
    step(sh, sx, 0, u + PW - 0.14 - sx, ['Select /', 'Check Risk'], h=0.74, size=12.5, cy=ya)
    # act in the environment, observe the outcome
    sim_w = 1.5
    smx = u + PW - 0.14 - sim_w
    acx = (sx + u + PW - 0.14) / 2
    arrow(sh, acx, ya + 0.38, acx, yb - 0.27, color=TK, lw=2.0)
    T(sh, acx - 0.82, (ya + 0.38 + yb - 0.27) / 2 - 0.14, 0.76, 0.28, 'Action', size=13, italic=True, color=TK, align='r')
    step(sh, smx, 0, sim_w, 'Simulator', icon='simulator', cy=yb)
    fb(sh, [(smx + sim_w / 2, yb + 0.27), (smx + sim_w / 2, yr), (u + 0.12, yr), (u + 0.12, ya), (u + 0.24, ya)])
    T(sh, u + 1.6, yr - 0.31, 2.2, 0.28, 'Observed Outcome', size=13, italic=True, color=EV)
    evaluation(sh, u, v, 'Action Utility · Risk · Latency')
    return g


def build(out):
    p, slide = new_slide(H)
    forecasting(slide); synthesis(slide); anomaly(slide); decision(slide)
    save(p, out)
    for w in WARN: print('WARN', w)


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figure08_V7.pptx'))
