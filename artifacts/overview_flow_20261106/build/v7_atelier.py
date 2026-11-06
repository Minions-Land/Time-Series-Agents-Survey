"""V7 Atelier: an exploded isometric build of a Time Series Agent.

Left: scenario and data as stacked paper. Centre: General -> Time-Series -> Task-Specific harness plates with
the LLM on top, acting down and observing up through every layer. Right: an evaluation funnel that passes an
accepted output or sends the agent back to revise. Bottom: one time axis (history | t0 | forecast) under it all.
"""
import math
from common import *
from v4_sketch import poly, shadow, _y, _smooth, GLYPHS
from pptx.enum.dml import MSO_LINE

F = 'Comic Sans MS'
W, H = 13.333, 7.5
INK, MUTE = '1F2A44', '5E6472'
HUE = dict(  # (dark, mid, light) per component
    llm=('C9861A', 'F3C977', 'FDF2DC'), gh=('3B5BA5', '9FB3E1', 'E4EBF8'), gts=('23887C', '8ACDC4', 'DDF2EF'),
    tsk=('C9503F', 'EFA396', 'FCE6E1'), ev=('5B5F97', 'B3B6D6', 'ECEDF6'))
D = (0.6, -0.5)        # depth vector of the oblique projection
T = 0.34               # plate thickness
T0 = 9.925             # information cutoff on the shared time axis


def tx(sh, x, y, w, h, t, size=12, bold=False, color=INK, align='c', italic=False, anchor='m'):
    return text(sh, x, y, w, h, t, size=size, bold=bold, color=color, font=F, align=align, italic=italic, anchor=anchor, wrap=False)


def ic(sh, name, x, y, s):
    return icon(sh, 'clay', name, x, y, s)


def alpha_fill(shape, val):
    clr = shape.fill._xPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
    etree.SubElement(clr, qn('a:alpha')).set('val', str(int(val * 1000)))


def zone(slide, x, y, w, h, fill, line, title, tfill, bw):
    g = group(slide); sh = g.shapes
    box(sh, x, y, w, h, fill=fill, line=line, lw=1.0, radius=0.035, dash=MSO_LINE.DASH)
    b = box(sh, x + w / 2 - bw / 2, y - 0.22, bw, 0.44, fill=tfill, radius=0.5); shadow(b)
    label_in(b, title, size=16, font=F)
    return g


def paper(sh, x, y, w, h, line, n=3):
    """A stack of n sheets, offset up-right, with a drop shadow."""
    for k in range(n - 1, -1, -1):
        s = box(sh, x + 0.07 * k, y - 0.07 * k, w, h, fill='FFFFFF', line=line, lw=1.3 if k == 0 else 0.9,
                shape=MSO_SHAPE.RECTANGLE)
        sketchy(s)
        if k == n - 1: shadow(s)
    return s


def plate(slide, key, x, y, w, verb, name, glyphs):
    dk, md, lt = HUE[key]
    g = group(slide); sh = g.shapes
    dx, dy = D
    front = [(x, y), (x + w, y), (x + w, y + T), (x, y + T)]
    side = [(x + w, y), (x + w + dx, y + dy), (x + w + dx, y + dy + T), (x + w, y + T)]
    top = [(x, y), (x + w, y), (x + w + dx, y + dy), (x + dx, y + dy)]
    shadow(poly(sh, front, dk, lw=1.0, fill=dk, closed=True))
    poly(sh, side, dk, lw=1.0, fill=md, closed=True)
    poly(sh, top, dk, lw=1.3, fill=lt, closed=True)
    i = 0.07   # white bevel inset on the top face
    poly(sh, [(x + i * 2.2, y - i), (x + w - i * 0.6, y - i), (x + w + dx - i * 2.2, y + dy + i), (x + dx + i * 0.6, y + dy + i)],
         'FFFFFF', lw=1.2, closed=True)
    t = sh.add_textbox(Inches(x), Inches(y + 0.02), Inches(w), Inches(T - 0.04))
    tf = t.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    for s, b in ((verb + '   ', True), (name, False)):
        r = p.add_run(); r.text = s; f = r.font; f.size = Pt(14); f.bold = b; f.name = F; f.color.rgb = rgb('FFFFFF')
    if key == 'gts':   # a time ruler along the bottom of the time-series plate
        for k in range(int(w / 0.14) + 1):
            tl = 0.055 if k % 5 == 0 else 0.03
            arrow(sh, x + 0.07 + k * 0.14, y + T - tl, x + 0.07 + k * 0.14, y + T - 0.01, color='FFFFFF', lw=0.8, head=None)
    for k, (nm, cap) in enumerate(glyphs):
        cx = x + 0.45 * dx + w * [0.13, 0.33, 0.67, 0.87][k]
        base = y - 0.3
        ic(sh, nm, cx - 0.29, base - 0.6, 0.58)
        tx(sh, cx - 0.6, base - 0.01, 1.2, 0.22, cap, size=11.5, color=dk, bold=True)
    return g


def pedestal(sh, x, y, w, h, key):
    dk, md, lt = HUE[key]
    e = box(sh, x, y, w, h, fill=lt, line=md, lw=1.4, shape=MSO_SHAPE.OVAL); shadow(e)
    box(sh, x + 0.08 * w, y + 0.12 * h, 0.84 * w, 0.62 * h, line='FFFFFF', lw=1.0, shape=MSO_SHAPE.OVAL)
    return e


def curve(sh, pts, color, lw=2.6, dash=None, head=True, n=40):
    """Quadratic Bezier through a control point, drawn as a freeform with an arrowhead."""
    (x0, y0), (cx, cy), (x1, y1) = pts
    seg = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1)
           for t in [k / n for k in range(n + 1)]]
    s = poly(sh, seg, color, lw=lw, dash=dash)
    if head:
        e = etree.SubElement(s.line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle'); e.set('w', 'med'); e.set('len', 'med')
    return s


def series(sh, x, y, w, h, color, phase=0.0, amp=1.0, lw=1.6):
    n = 90
    pts = [(x + w * k / n, y + h / 2 - h / 2.6 * amp * _y((k / n + phase) % 1.0)) for k in range(n + 1)]
    return poly(sh, pts, color, lw=lw)


def inputs(slide):
    g = group(slide); sh = g.shapes
    x, w = 0.5, 2.45
    # task request
    paper(sh, x, 0.95, w, 1.32, 'B9A98A')
    ic(sh, 'request', x + 0.08, 1.0, 0.62)
    tx(sh, x + 0.72, 1.06, 1.6, 0.3, 'task', size=14, bold=True, align='l')
    b = box(sh, x + 0.14, 1.66, w - 0.28, 0.5, fill='FFF6E3', line='D9C49A', lw=0.8, radius=0.3)
    label_in(b, '“forecast next week, flag risks, advise action”', size=10.5, bold=False, color=INK, font=F)
    b.text_frame.paragraphs[0].runs[0].font.italic = True
    # context
    paper(sh, x, 2.75, w, 1.12, 'B9A98A')
    tx(sh, x + 0.12, 2.81, 1.6, 0.3, 'context', size=14, bold=True, align='l')
    for k, (nm, cap) in enumerate([('calendar', 'events'), ('chat', 'reports'), ('memory', 'history')]):
        cx = x + 0.45 + k * 0.78
        ic(sh, nm, cx - 0.25, 3.11, 0.5)
        tx(sh, cx - 0.4, 3.6, 0.8, 0.22, cap, size=11, color=MUTE)
    # observed series
    paper(sh, x, 4.3, w, 1.62, 'B9A98A')
    tx(sh, x + 0.12, 4.36, 2.0, 0.3, 'observed series', size=14, bold=True, align='l')
    for k, (col, ph, a) in enumerate([(INK, 0.0, 1.0), (HUE['gts'][0], 0.23, 0.8), (HUE['gh'][0], 0.51, 0.7)]):
        series(sh, x + 0.15, 4.76 + k * 0.34, w - 0.3, 0.36, col, ph, a, lw=1.4)
    # bracket: data goes to the harness
    poly(sh, [(3.02, 2.8), (3.1, 2.8), (3.1, 5.9), (3.02, 5.9)], 'A49A86', lw=1.3)
    return g


def llm_block(slide):
    g = group(slide); sh = g.shapes
    dk, md, lt = HUE['llm']
    pedestal(sh, 3.55, 1.47, 2.15, 0.42, 'llm')
    st = box(sh, 3.62, 0.66, 0.92, 0.32, fill=dk, radius=0.5); label_in(st, 'ALIGN', size=12, font=F)
    tx(sh, 4.6, 0.62, 1.2, 0.4, 'LLM', size=18, bold=True, align='l')
    for k, (nm, cap) in enumerate([('encode', 'encode'), ('reason', 'reason'), ('policy', 'act')]):
        cx = 3.95 + k * 0.68
        ic(sh, nm, cx - 0.27, 1.08, 0.54)
        tx(sh, cx - 0.4, 1.9, 0.8, 0.22, cap, size=11.5, color=dk, bold=True)
    # the agent
    halo = box(sh, 5.6, 0.55, 1.9, 1.75, fill='FFF1CC', shape=MSO_SHAPE.OVAL); alpha_fill(halo, 55)
    pedestal(sh, 5.9, 2.0, 1.3, 0.34, 'llm')
    ic(sh, 'robot', 5.8, 0.66, 1.5)
    return g


def stack(slide):
    xs = dict(gh=(3.75, 5.95, 5.0), gts=(3.95, 4.65, 4.6), tsk=(4.15, 3.35, 4.2))
    verbs = dict(gh=('REUSE', 'General Harness'), gts=('ADAPT', 'General Time-Series Harness'),
                 tsk=('REBUILD', 'Task-Specific Harness'))
    for k in ('gh', 'gts', 'tsk'):
        x, y, w = xs[k]
        plate(slide, k, x, y, w, *verbs[k], GLYPHS[k])
    g = group(slide); sh = g.shapes
    # exploded-view drop lines from each plate's lower corners to the plate below
    for (ux, uy, uw), (lx, ly, lw_) in [(xs['gts'], xs['gh']), (xs['tsk'], xs['gts'])]:
        for px in (ux, ux + uw):
            arrow(sh, px, uy + T, px, ly - 0.12, color='8C93A3', lw=1.0, dash=MSO_LINE.ROUND_DOT, head=None)
    # action down / observation up through every layer
    cx = 6.55
    gaps = [(2.38, 2.98), (3.35 + T + 0.03, 4.3), (4.65 + T + 0.03, 5.6)]
    for y0, y1 in gaps:
        arrow(sh, cx - 0.12, y0, cx - 0.12, y1, color=HUE['llm'][0], lw=2.4)
        arrow(sh, cx + 0.12, y1, cx + 0.12, y0, color=INK, lw=1.8, dash=MSO_LINE.DASH)
    tx(sh, cx - 1.85, 2.12, 1.15, 0.24, 'action', size=12, bold=True, color=HUE['llm'][0], align='r', italic=True)
    tx(sh, cx + 0.7, 2.12, 1.3, 0.24, 'observation', size=12, bold=True, color=INK, align='l', italic=True)
    # specificity axis
    ax = 9.62
    for (y0, y1), k in zip([(6.25, 5.2), (5.2, 4.12), (4.12, 3.1)], ('gh', 'gts', 'tsk')):
        arrow(sh, ax, y0, ax, y1, color=HUE[k][0], lw=3.2, head='triangle' if k == 'tsk' else None)
    lab = tx(sh, ax - 0.22 - 1.1, 4.3 - 0.13, 2.2, 0.26, 'general  →  specific', size=11.5, italic=True, color=MUTE)
    lab.rotation = -90
    # data from the scenario into the harness
    arrow(sh, 3.12, 4.32, 3.9, 4.82, color='A49A86', lw=2.2)
    return g


def funnel(slide):
    g = group(slide); sh = g.shapes
    dk, md, lt = HUE['ev']
    cx, y0, h, gap, top, bot = 11.52, 0.98, 0.54, 0.07, 2.75, 1.45
    rows = [('process', 'valid run'), ('time_check', 'no look-ahead'), ('benchmark', 'accurate'), ('utility', 'useful')]
    fills = ['F1F1F8', 'E2E3F1', 'D2D4EA', 'C2C5E2']
    for k, (nm, lab) in enumerate(rows):
        ya, yb = y0 + k * (h + gap), y0 + k * (h + gap) + h
        wa = top - (top - bot) * (ya - y0) / (4 * h + 3 * gap)
        wb = top - (top - bot) * (yb - y0) / (4 * h + 3 * gap)
        s = poly(sh, [(cx - wa / 2, ya), (cx + wa / 2, ya), (cx + wb / 2, yb), (cx - wb / 2, yb)], dk, lw=1.3, fill=fills[k], closed=True)
        shadow(s)
        ic(sh, nm, cx - wb / 2 + 0.1, ya + 0.04, 0.46)
        tx(sh, cx - wb / 2 + 0.55, ya, wb - 0.6, h, lab, size=12.5, bold=True, color=dk, align='l')
    yend = y0 + 4 * h + 3 * gap
    arrow(sh, cx, yend + 0.02, cx, 3.6, color=dk, lw=2.4)
    # accepted output
    paper(sh, 10.3, 3.72, 2.45, 1.42, '8E92BC')
    ic(sh, 'validate', 10.38, 3.76, 0.52)
    tx(sh, 10.92, 3.8, 1.8, 0.36, 'accepted output', size=14, bold=True, align='l')
    for k, (nm, cap) in enumerate([('forecast', 'forecast'), ('anomaly', 'diagnosis'), ('decision', 'decision')]):
        x = 10.72 + k * 0.8
        ic(sh, nm, x - 0.25, 4.3, 0.5)
        tx(sh, x - 0.45, 4.8, 0.9, 0.22, cap, size=11, color=MUTE)
    arrow(sh, cx, 5.2, cx, 6.58, color=dk, lw=1.4, dash=MSO_LINE.ROUND_DOT)
    tx(sh, cx + 0.08, 5.72, 1.3, 0.24, 'act ahead', size=11.5, italic=True, color=MUTE, align='l')
    return g


def flows(slide):
    g = group(slide); sh = g.shapes
    ev = HUE['ev'][0]
    # task request -> LLM
    arrow(sh, 2.98, 1.62, 3.5, 1.66, color='A49A86', lw=2.2)
    # candidate output -> evaluation
    curve(sh, [(8.98, 3.0), (9.6, 2.0), (10.28, 1.9)], HUE['tsk'][0], lw=2.6)
    tx(sh, 8.05, 2.32, 1.2, 0.24, 'candidate', size=12, bold=True, italic=True, color=HUE['tsk'][0], align='r')
    # revise: evaluation -> agent
    curve(sh, [(10.2, 1.2), (8.8, 0.45), (7.3, 1.12)], ev, lw=3.0)
    ic(sh, 'feedback', 8.18, 0.98, 0.42)
    tx(sh, 8.62, 1.03, 0.9, 0.3, 'revise', size=13, bold=True, italic=True, color=ev, align='l')
    return g


def time_axis(slide):
    g = group(slide); sh = g.shapes
    x0, x1, yc, amp = 0.45, 12.4, 6.98, 0.21
    n = 260; kc = int(n * (T0 - x0) / (x1 - x0))
    xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    ys = [yc - amp * _y(k / n) for k in range(n + 1)]
    off = ys[kc] - (yc - amp * _smooth(kc / n))
    for k in range(kc + 1, n + 1):
        ys[k] = yc - amp * _smooth(k / n) + off
    ka = int(n * 0.31)
    ys[ka] -= 0.27
    hb = box(sh, x0 - 0.1, 6.56, T0 - x0 + 0.1, 0.72, fill='ECEEF2', radius=0.18); alpha_fill(hb, 75)
    fb = box(sh, T0, 6.56, 13.08 - T0, 0.72, fill=HUE['ev'][2], radius=0.18); alpha_fill(fb, 80)
    m = n - kc
    up = [(xs[k], ys[k] - 0.02 - 0.2 * (k - kc) / m) for k in range(kc, n + 1)]
    lo = [(xs[k], ys[k] + 0.02 + 0.2 * (k - kc) / m) for k in range(kc, n + 1)]
    poly(sh, up + lo[::-1], None, fill=HUE['tsk'][0], alpha=22, closed=True)
    poly(sh, list(zip(xs[:kc + 1], ys[:kc + 1])), INK, lw=1.6)
    poly(sh, list(zip(xs[kc:], ys[kc:])), HUE['tsk'][0], lw=1.8, dash=MSO_LINE.DASH)
    ax_ = xs[ka]
    o = box(sh, ax_ - 0.17, ys[ka] - 0.17, 0.34, 0.34, line=HUE['tsk'][0], lw=1.8, shape=MSO_SHAPE.OVAL); sketchy(o)
    ic(sh, 'anomaly', ax_ + 0.22, 6.6, 0.36)
    tx(sh, x0, 6.6, 1.4, 0.24, 'history', size=12, bold=True, color=MUTE, align='l')
    tx(sh, T0 + 0.12, 7.0, 1.4, 0.24, 'forecast', size=12, bold=True, color=HUE['tsk'][0], align='l')
    arrow(sh, T0, 6.5, T0, 7.22, color=HUE['gts'][0], lw=1.6, dash=MSO_LINE.DASH, head=None)
    pill = box(sh, T0 - 0.25, 7.2, 0.5, 0.27, fill=HUE['gts'][0], radius=0.5)
    tf = pill.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    for s, sub in (('t', False), ('0', True)):
        r = p.add_run(); r.text = s; f = r.font; f.size = Pt(12); f.bold = True; f.name = F; f.color.rgb = rgb('FFFFFF')
        if sub: r.font._rPr.set('baseline', '-25000')
    ic(sh, 'decision', 12.5, 6.68, 0.48)
    arrow(sh, 0.35, 7.34, 12.6, 7.34, color=INK, lw=1.4)
    tx(sh, 12.62, 7.22, 0.6, 0.24, 'time', size=11.5, italic=True, color=MUTE)
    return g


def build(out):
    p, slide = new_pres(W, H)
    box(slide.shapes, 0, 0, W, H, fill='FFFFFF', shape=MSO_SHAPE.RECTANGLE)
    zone(slide, 0.25, 0.3, 2.98, 6.12, 'FAF7F0', 'D8CDB5', 'Scenario & Data', '8A7A5C', 2.3)
    zone(slide, 3.38, 0.3, 6.5, 6.12, 'F5F7FB', 'C9D2E3', 'Build a Time Series Agent', INK, 3.9)
    zone(slide, 10.03, 0.3, 3.05, 6.12, 'F6F5FA', 'CFCFE3', 'Verify & Deliver', HUE['ev'][0], 2.4)
    inputs(slide)
    stack(slide)
    llm_block(slide)
    funnel(slide)
    flows(slide)
    time_axis(slide)
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
