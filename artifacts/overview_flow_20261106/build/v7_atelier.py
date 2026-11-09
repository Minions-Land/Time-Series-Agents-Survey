"""V7 Atelier: an exploded isometric build of a Time Series Agent.

Left: scenario and data as stacked paper. Centre: General -> General Time Series -> Task-Specific Harness plates with
the LLM on top, acting down and observing up through every layer. Right: an evaluation funnel that passes an
accepted output (a forecast past the cutoff t0) or sends the agent back to revise.
"""
import math
from common import *
from v4_sketch import poly, shadow, _y, _smooth
from pptx.enum.dml import MSO_LINE

F = 'Comic Sans MS'
W, H = 13.333, 7.0
import sys as _sys
_sys.path.insert(0, os.path.join(ROOT, '..', 'unified_v7_20261106', 'kit'))
from v7kit import HUE, INK, MUTE, ZONE_FILL, PAPER_LINE   # one palette for every figure
D = (0.6, -0.5)        # depth vector of the oblique projection
T = 0.4                # plate thickness
CX = 6.72              # centre of the build zone
PLATES = dict(gh=(3.67, 6.2, 5.5), gts=(3.87, 4.75, 5.1), tsk=(4.07, 3.3, 4.7))   # front-left x, front y, width
VERBS = dict(gh=('REUSE', 'General Harness'), gts=('ADAPT', 'General Time Series Harness'),
             tsk=('REDESIGN', 'Task-Specific Harness'))
GLYPHS = dict(
    # captions follow the subsection headings of Sections 4-6
    gh=[('chat', 'Interaction'), ('memory', 'Memory'), ('tools', 'Tools'), ('planning', 'Planning'), ('runtime', 'Evolution')],
    gts=[('calendar', 'Data'), ('window', 'Processing'), ('timeline', 'Context'), ('cutoff', 'Validation')],
    # the four output modes of the task grid (Section 6, Table 7); 'Decision Making' breaks onto two lines
    tsk=[('timeseries', 'Regression'), ('anomaly', 'Classification'), ('synthesis', 'Generation'),
         ('decision', ['Decision', 'Making'])])
SPREAD = {4: [0.11, 0.33, 0.67, 0.89], 5: [0.1, 0.3, 0.5, 0.7, 0.9]}
SPREAD_TSK = [0.10, 0.335, 0.67, 0.885]      # four output modes; first lines share one row


def tx(sh, x, y, w, h, t, size=12, bold=False, color=INK, align='c', italic=False, anchor='m'):
    return text(sh, x, y, w, h, t, size=size, bold=bold, color=color, font=F, align=align, italic=italic, anchor=anchor, wrap=False)


def ic(sh, name, x, y, s):
    return icon(sh, 'clay', name, x, y, s)


def alpha_fill(shape, val):
    clr = shape.fill._xPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
    etree.SubElement(clr, qn('a:alpha')).set('val', str(int(val * 1000)))


def runs(shape, parts, size, align=PP_ALIGN.CENTER):
    """Fill a shape's text frame with styled runs: parts = [(text, colour, bold, subscript)]."""
    tf = shape.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = align
    for t, col, b, sub in parts:
        r = p.add_run(); r.text = t; f = r.font; f.size = Pt(size); f.bold = b; f.name = F; f.color.rgb = rgb(col)
        if sub: r.font._rPr.set('baseline', '-25000')
    return shape


def zone(slide, x, y, w, h, key, title, bw):
    g = group(slide); sh = g.shapes
    box(sh, x, y, w, h, fill=ZONE_FILL[key], radius=0.035)          # tint only, no frame
    b = box(sh, x + w / 2 - bw / 2, y - 0.25, bw, 0.5, fill=HUE[key][0], radius=0.5); shadow(b)
    label_in(b, title, size=19, font=F)
    return g


def paper(sh, x, y, w, h, line, n=3):
    """A stack of n sheets, offset up-right, with a drop shadow."""
    for k in range(n - 1, -1, -1):
        s = box(sh, x + 0.07 * k, y - 0.07 * k, w, h, fill='FFFFFF', line=PAPER_LINE, lw=1.0 if k == 0 else 0.75,
                shape=MSO_SHAPE.RECTANGLE)
        sketchy(s)
        if k == n - 1: shadow(s)
    return s


def plate(slide, key):
    x, y, w = PLATES[key]
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
    verb, name = VERBS[key]
    runs(sh.add_textbox(Inches(x), Inches(y + 0.02), Inches(w), Inches(T - 0.06)),
         [(verb + '   ', 'FFFFFF', True, False), (name, 'FFFFFF', False, False)], 17)
    if key == 'gts':   # a time ruler along the bottom of the time-series plate
        for k in range(int(w / 0.14) + 1):
            tl = 0.06 if k % 5 == 0 else 0.032
            arrow(sh, x + 0.07 + k * 0.14, y + T - tl, x + 0.07 + k * 0.14, y + T - 0.01, color='FFFFFF', lw=0.8, head=None)
    for k, (nm, cap) in enumerate(GLYPHS[key]):
        cx = x + 0.45 * dx + w * (SPREAD_TSK if key == 'tsk' else SPREAD[len(GLYPHS[key])])[k]
        base = y - 0.32
        if key == 'tsk':   # slightly smaller icon so that two-line names fit on the top face
            ic(sh, nm, cx - 0.27, base - 0.7, 0.54)
            t = tx(sh, cx - 0.75, base - 0.15, 1.5, 0.34, cap, size=11.5, color=dk, bold=True, anchor='t')
            for para in t.text_frame.paragraphs: para.line_spacing = 0.8
            continue
        ic(sh, nm, cx - 0.33, base - 0.68, 0.66)
        tx(sh, cx - 0.7, base - 0.02, 1.4, 0.26, cap, size=13.5, color=dk, bold=True)
    return g


def pedestal(sh, x, y, w, h, key):
    dk, md, lt = HUE[key]
    e = box(sh, x, y, w, h, fill=lt, line=md, lw=1.4, shape=MSO_SHAPE.OVAL); shadow(e)
    box(sh, x + 0.08 * w, y + 0.12 * h, 0.84 * w, 0.62 * h, line='FFFFFF', lw=1.0, shape=MSO_SHAPE.OVAL)
    return e


def bezier(pts, n=40):
    (x0, y0), (cx, cy), (x1, y1) = pts
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1)
            for t in [k / n for k in range(n + 1)]]


def curve(sh, pts, color, lw=2.6, dash=None):
    """Quadratic Bezier through a control point, drawn as a freeform with an arrowhead."""
    s = poly(sh, bezier(pts), color, lw=lw, dash=dash)
    e = etree.SubElement(s.line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle'); e.set('w', 'med'); e.set('len', 'med')
    return s


def series(sh, x, y, w, h, color, phase=0.0, amp=1.0, lw=1.6):
    n = 90
    pts = [(x + w * k / n, y + h / 2 - h / 2.6 * amp * _y((k / n + phase) % 1.0)) for k in range(n + 1)]
    return poly(sh, pts, color, lw=lw)


def mini_forecast(sh, x, y, w, h, cut=0.62):
    """Observed history up to t0, then a dashed forecast inside a widening band."""
    n = 110; kc = int(n * cut); amp = h / 2.6
    xs = [x + w * k / n for k in range(n + 1)]
    ys = [y + h / 2 - amp * _y(k / n) for k in range(n + 1)]
    calm = lambda t: 0.5 * math.sin(2 * math.pi * t * 5.2) + 0.4 * t   # the forecast follows the seasonal trend
    off = ys[kc] - (y + h / 2 - amp * calm(kc / n))
    for k in range(kc + 1, n + 1):
        ys[k] = y + h / 2 - amp * calm(k / n) + off
    m = n - kc
    up = [(xs[k], ys[k] - 0.02 - 0.17 * (k - kc) / m) for k in range(kc, n + 1)]
    lo = [(xs[k], ys[k] + 0.02 + 0.17 * (k - kc) / m) for k in range(kc, n + 1)]
    poly(sh, up + lo[::-1], None, fill=HUE['tsk'][0], alpha=22, closed=True)
    poly(sh, list(zip(xs[:kc + 1], ys[:kc + 1])), INK, lw=1.5)
    poly(sh, list(zip(xs[kc:], ys[kc:])), HUE['tsk'][0], lw=1.8, dash=MSO_LINE.DASH)
    t0 = xs[kc]
    arrow(sh, t0, y - 0.06, t0, y + h + 0.02, color=HUE['gts'][0], lw=1.4, dash=MSO_LINE.DASH, head=None)
    pill = box(sh, t0 - 0.29, y + h + 0.02, 0.58, 0.24, fill=HUE['gts'][0], radius=0.5)
    runs(pill, [('Now', 'FFFFFF', True, False)], 12)   # the current time, as in every other figure


def inputs(slide):
    g = group(slide); sh = g.shapes
    x, w = 0.42, 2.5
    # task request
    paper(sh, x, 1.0, w, 1.5, 'B9A98A')
    ic(sh, 'request', x + 0.08, 1.03, 0.66)
    tx(sh, x + 0.8, 1.1, 1.6, 0.4, 'Task', size=17, bold=True, align='l')
    b = box(sh, x + 0.13, 1.8, w - 0.26, 0.6, fill=HUE['data'][2], radius=0.3)
    label_in(b, ['“Forecast next week,', 'flag risks, advise action”'], size=12.5, bold=False, color=INK, font=F)
    for p in b.text_frame.paragraphs: p.runs[0].font.italic = True
    # context
    paper(sh, x, 2.95, w, 1.35, 'B9A98A')
    tx(sh, x + 0.13, 3.0, 1.6, 0.4, 'Context', size=17, bold=True, align='l')
    for k, (nm, cap) in enumerate([('calendar', 'Events'), ('chat', 'Reports'), ('memory', 'History')]):
        cx = x + 0.45 + k * 0.8
        ic(sh, nm, cx - 0.28, 3.42, 0.56)
        tx(sh, cx - 0.45, 3.99, 0.9, 0.26, cap, size=13, color=MUTE, bold=True)
    # observed series
    paper(sh, x, 4.75, w, 1.75, 'B9A98A')
    tx(sh, x + 0.13, 4.8, 2.3, 0.4, 'Observed Series', size=17, bold=True, align='l')
    for k, (col, ph, a) in enumerate([(INK, 0.0, 1.0), (HUE['gts'][0], 0.23, 0.8), (HUE['gh'][0], 0.51, 0.7)]):
        series(sh, x + 0.15, 5.26 + k * 0.38, w - 0.3, 0.4, col, ph, a, lw=1.5)
    # bracket: data goes to the harness, the request goes to the LLM
    poly(sh, [(3.04, 2.95), (3.12, 2.95), (3.12, 6.5), (3.04, 6.5)], HUE['data'][1], lw=1.3)
    arrow(sh, 3.14, 4.72, 3.85, 4.98, color=HUE['data'][0], lw=2.4)
    arrow(sh, 2.99, 1.72, 3.42, 1.72, color=HUE['data'][0], lw=2.4)
    return g


def llm_block(slide):
    g = group(slide); sh = g.shapes
    dk, md, lt = HUE['llm']
    pedestal(sh, 3.42, 1.3, 2.3, 0.36, 'llm')
    st = box(sh, 3.48, 0.66, 1.62, 0.38, fill=dk, radius=0.5); label_in(st, 'LLM: Caller', size=16, font=F)
    for k, (nm, cap) in enumerate([('window', 'Read'), ('tools', 'Call'), ('reason', 'Interpret')]):   # Section 3: reads the state, calls functions, interprets results
        cx = 3.85 + k * 0.74
        ic(sh, nm, cx - 0.26, 1.03, 0.52)
        tx(sh, cx - 0.45, 1.64, 0.9, 0.26, cap, size=13, color=dk, bold=True)
    halo = box(sh, CX - 0.95, 0.62, 1.9, 1.75, fill=HUE['llm'][2], shape=MSO_SHAPE.OVAL); alpha_fill(halo, 90)
    pedestal(sh, CX - 0.6, 1.98, 1.2, 0.34, 'llm')
    ic(sh, 'robot', CX - 0.75, 0.7, 1.5)
    return g


def stack(slide):
    for k in ('gh', 'gts', 'tsk'):
        plate(slide, k)
    g = group(slide); sh = g.shapes
    # exploded-view drop lines from each plate's lower corners to the plate below
    for up, lo in (('gts', 'gh'), ('tsk', 'gts')):
        ux, uy, uw = PLATES[up]; ly = PLATES[lo][1]
        for px in (ux, ux + uw):
            arrow(sh, px, uy + T, px, ly - 0.12, color=HUE['ink'][1], lw=1.0, dash=MSO_LINE.ROUND_DOT, head=None)
    # action down / observation up through every layer
    gaps = [(2.36, 3.0), (3.3 + T + 0.03, 4.4)]   # the five-module base plate keeps its centre
    for y0, y1 in gaps:
        arrow(sh, CX - 0.13, y0, CX - 0.13, y1, color=HUE['llm'][0], lw=2.6)
        arrow(sh, CX + 0.13, y1, CX + 0.13, y0, color=INK, lw=2.0, dash=MSO_LINE.DASH)
    tx(sh, CX - 1.45, 2.03, 0.8, 0.28, 'Action', size=14, bold=True, color=HUE['llm'][0], align='r', italic=True)
    tx(sh, CX + 0.66, 2.03, 1.4, 0.28, 'Observation', size=14, bold=True, color=INK, align='l', italic=True)
    # specificity axis: the survey's general -> specific ordering
    ax = 10.0
    for (y0, y1), k in zip([(6.55, 5.4), (5.4, 4.3), (4.3, 3.3)], ('gh', 'gts', 'tsk')):
        arrow(sh, ax, y0, ax, y1, color=HUE[k][0], lw=3.4, head='triangle' if k == 'tsk' else None)
    lab = tx(sh, ax - 0.24 - 1.15, 4.75 - 0.14, 2.3, 0.28, 'General  →  Specific', size=13, italic=True, bold=True, color=MUTE)
    lab.rotation = -90
    return g


def funnel(slide):
    g = group(slide); sh = g.shapes
    dk, md, lt = HUE['ev']
    cx, y0, h, gap, top, bot = 11.71, 1.0, 0.58, 0.06, 2.72, 1.62
    rows = [('process', 'Process'), ('time_check', 'Temporal'), ('benchmark', 'Task'), ('utility', 'Decision')]
    second = ['Validity', 'Validity', 'Performance', 'Utility']   # evaluation criteria named in Sections 2 and 9
    fills = ['F3F4FA', 'E6E7F3', 'D8DAEC', 'CACDE5']   # light -> mid of the evaluation hue
    span = 4 * h + 3 * gap
    for k, (nm, lab) in enumerate(rows):
        ya, yb = y0 + k * (h + gap), y0 + k * (h + gap) + h
        wa, wb = top - (top - bot) * (ya - y0) / span, top - (top - bot) * (yb - y0) / span
        shadow(poly(sh, [(cx - wa / 2, ya), (cx + wa / 2, ya), (cx + wb / 2, yb), (cx - wb / 2, yb)], dk, lw=1.3, fill=fills[k], closed=True))
        ic(sh, nm, cx - wb / 2 + 0.08, ya + 0.05, 0.48)
        t = tx(sh, cx - wb / 2 + 0.58, ya + 0.02, wb - 0.6, h - 0.04, [lab, second[k]], size=12.5, bold=True, color=dk, align='l')
        t.text_frame.paragraphs[1].runs[0].font.bold = False
    arrow(sh, cx, y0 + span + 0.02, cx, 3.84, color=dk, lw=2.6)
    # accepted output: a forecast past the cutoff, plus what it serves
    paper(sh, 10.45, 3.98, 2.5, 2.57, '8E92BC')
    ic(sh, 'validate', 10.52, 4.03, 0.52)
    tx(sh, 11.06, 4.06, 1.9, 0.44, 'Final Output', size=16, bold=True, align='l')
    mini_forecast(sh, 10.65, 4.66, 2.1, 0.62)
    for k, (nm, cap) in enumerate([('forecast', 'Forecast'), ('anomaly', 'Diagnosis'), ('decision', 'Decision')]):
        x = 10.9 + k * 0.8
        ic(sh, nm, x - 0.26, 5.55, 0.52)
        tx(sh, x - 0.45, 6.09, 0.9, 0.26, cap, size=12.5, color=MUTE, bold=True)
    return g


def flows(slide):
    g = group(slide); sh = g.shapes
    ev, tk = HUE['ev'][0], HUE['tsk'][0]
    x, y, w = PLATES['tsk']
    cand = [(x + w + 0.3, y - 0.05), (9.75, 2.25), (10.6, 1.95)]
    curve(sh, cand, tk, lw=2.8)
    lab = tx(sh, 9.98 - 0.6, 2.68 - 0.15, 1.2, 0.3, 'Candidate', size=14, bold=True, italic=True, color=tk)
    lab.rotation = -38
    curve(sh, [(10.42, 1.15), (9.0, 0.32), (7.55, 1.12)], ev, lw=3.2)
    ic(sh, 'feedback', 8.3, 0.93, 0.46)
    tx(sh, 8.8, 0.98, 1.0, 0.34, 'Revise', size=15, bold=True, italic=True, color=ev, align='l')
    return g


def build(out):
    p, slide = new_pres(W, H)
    box(slide.shapes, 0, 0, W, H, fill='FFFFFF', shape=MSO_SHAPE.RECTANGLE)
    zone(slide, 0.2, 0.42, 2.95, 6.4, 'data', 'Scenario & Data', 2.6)
    zone(slide, 3.27, 0.42, 6.9, 6.4, 'ink', 'Build a Time Series Agent', 4.4)
    zone(slide, 10.29, 0.42, 2.84, 6.4, 'ev', 'Evaluation', 2.2)
    inputs(slide)
    stack(slide)
    llm_block(slide)
    funnel(slide)
    flows(slide)
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
