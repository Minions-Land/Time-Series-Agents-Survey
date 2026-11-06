"""Figure 10 (fig:anomamind-workflow) in the V7 house style: AnomaMind's four-stage interval workflow.

Top row, one zone per stage (Acquire -> Construct -> Detect -> Refine). The harness stages use the Task-Specific
Harness hue (red); the trained detector uses the LLM-side hue (amber), following the manuscript's sentence
"The trained detector belongs to the LLM side; the surrounding evidence-acquisition and refinement procedure
supplies the anomaly-specific Harness."
  Acquire: coarse localization from visual anomaly patterns, knowledge memory K and numerical diagnostics N,
           giving candidate intervals.
  Construct: evidence state s_k = intervals (candidate boundaries), numerical evidence, context.
  Detect / Refine: the same schematic signal; the refined interval is narrower than the candidate region.
  Return path: Update Evidence (Refine -> Construct).
Lower band: detector training (SFT initialization -> RL) with the reward terms parse validity + interval
agreement - false-positive penalty.
"""
import math, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit')))
from v7kit import *

H = 7.4
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figure10_V7.pptx')
TK, LL, EV, BL, GT = HUE['tsk'], HUE['llm'], HUE['ev'], HUE['gh'], HUE['gts']
Z = dict(acq=(0.2, 3.05), con=(3.4, 3.0), det=(6.55, 3.2), ref=(9.9, 3.23))   # x, w
ZY, ZH = 0.42, 4.33
CAND, REFINED = (0.37, 0.71), (0.46, 0.63)


# ---- schematic signals ----------------------------------------------------------------------------------
def g(t, m, s):
    return math.exp(-0.5 * ((t - m) / s) ** 2)


def noise(t, seed=0.0):
    return (0.05 * math.sin(97 * t + seed) + 0.04 * math.sin(173 * t + 1 + 2 * seed) + 0.03 * math.sin(251 * t + 2 + seed)
            + 0.025 * math.sin(41 * t + 3 * seed))


def anomaly(t):           # one schematic signal used by both plots
    return 0.2 + noise(t) + 0.62 * g(t, 0.545, 0.028) + 0.28 * g(t, 0.505, 0.022) + 0.22 * g(t, 0.585, 0.02)


def sig(sh, x, y, w, h, f, color=INK, lw=1.6, n=160):
    pts = [(x + w * k / n, y + h - h * f(k / n)) for k in range(n + 1)]
    poly(sh, pts, color, lw=lw)


def math_runs(sh, x, y, w, h, parts, size, align='l'):
    """parts = [(text, colour, bold, italic, subscript)]"""
    tb = sh.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.02); tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
    for t, col, b, it, sub in parts:
        r = p.add_run(); r.text = t; f = r.font
        f.size = Pt(size); f.bold = b; f.italic = it; f.name = F; f.color.rgb = rgb(col)
        if sub: r.font._rPr.set('baseline', '-25000')
    return tb


def rpath(sh, pts, color, lw=2.4, dash=None, r=0.16, head=True):
    """Polyline with rounded corners and an arrowhead at the end."""
    out = [pts[0]]
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        def towards(p, q, d):
            L = math.hypot(q[0] - p[0], q[1] - p[1]); k = min(d, L / 2) / L
            return (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
        out += bezier([towards(b, a, r), b, towards(b, c, r)], n=10)
    out.append(pts[-1])
    s = poly(sh, out, color, lw=lw, dash=dash)
    if head:
        e = etree.SubElement(s.line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle'); e.set('w', 'med'); e.set('len', 'med')
    return s


def stage_zone(slide, key, num, title, hue):
    x, w = Z[key]
    g_ = zone(slide, x, ZY, w, ZH, None, hue); sh = g_.shapes   # banner joins the zone's group
    dk, md, lt = HUE[hue]
    bw = 0.155 * (len(title) + 3) + 0.6
    b = box(sh, x + w / 2 - bw / 2, ZY - 0.25, bw, 0.5, fill=dk, radius=0.5); shadow(b)
    runs(b, [(num + '  ', md, True, False), (title, 'FFFFFF', True, False)], 19)
    return g_


def plot(sh, x, y, w, h, span, label, key):
    """Card with an L axis, the schematic signal and a shaded interval with dashed bounds."""
    dk = HUE[key][0]
    card(sh, x, y, w, h, key=key)
    px, py, pw, ph = x + 0.28, y + 0.42, w - 0.5, h - 1.0
    a, b = span
    sx0, sx1 = px + pw * a, px + pw * b
    r = box(sh, sx0, py - 0.04, sx1 - sx0, ph + 0.12, fill=TK[0], shape=MSO_SHAPE.RECTANGLE); alpha_fill(r, 16)
    for xx in (sx0, sx1):
        arrow(sh, xx, py - 0.04, xx, py + ph + 0.08, color=TK[0], lw=1.2, dash=MSO_LINE.DASH, head=None)
    sig(sh, px, py, pw, ph, anomaly, lw=1.6)
    arrow(sh, px - 0.08, py + ph + 0.08, px + pw + 0.12, py + ph + 0.08, color='8C93A3', lw=1.3)
    arrow(sh, px - 0.08, py + ph + 0.08, px - 0.08, py - 0.12, color='8C93A3', lw=1.3)
    tx(sh, px + pw - 0.7, py + ph + 0.12, 0.8, 0.26, 'Time', size=12.5, bold=True, color=MUTE, align='r')
    tx(sh, (sx0 + sx1) / 2 - 1.0, y + 0.06, 2.0, 0.3, label, size=13.5, bold=True, color=TK[0])


# ---- stage 1: acquire -----------------------------------------------------------------------------------
def acquire(slide):
    g_ = group(slide); sh = g_.shapes
    x, w = Z['acq']; cx = x + w / 2
    tx(sh, x + 0.1, 0.8, w - 0.2, 0.34, 'Coarse Localization', size=15, bold=True, color=TK[0])
    paper(sh, 0.42, 1.36, 2.5, 1.0, 'B9A98A')
    for k, (sp, ph) in enumerate([(0.3, 0.0), (0.66, 1.7), (0.45, 3.1)]):
        sx, sy, sw, shh = 0.55, 1.42 + k * 0.3, 2.24, 0.26
        r = box(sh, sx + sw * (sp - 0.07), sy - 0.01, sw * 0.14, shh + 0.02, fill=TK[0], shape=MSO_SHAPE.RECTANGLE)
        alpha_fill(r, 18)
        sig(sh, sx, sy, sw, shh, lambda t, sp=sp, ph=ph: 0.4 + 1.6 * noise(t, ph) + 0.5 * g(t, sp, 0.015), lw=1.3, n=110)
    tx(sh, x + 0.05, 2.44, w - 0.1, 0.28, 'Visual Anomaly Patterns', size=13, bold=True, color=MUTE)
    for c, nm, cap in [(1.0, 'memory', ['Knowledge', 'Memory K']), (2.45, 'tools', ['Numerical', 'Diagnostics N'])]:
        ic(sh, nm, c - 0.3, 2.84, 0.6)
        t = tx(sh, c - 0.75, 3.46, 1.5, 0.46, cap, size=13, bold=True, color=TK[0])
        r = t.text_frame.paragraphs[1].runs[0]; letter = r.text[-1]; r.text = r.text[:-1]
        r2 = t.text_frame.paragraphs[1].add_run(); r2.text = letter
        f = r2.font; f.size = Pt(13); f.bold = True; f.italic = True; f.name = F; f.color.rgb = rgb(TK[0])
    # candidate intervals on a time line
    ly = 4.12
    arrow(sh, 0.5, ly, 2.95, ly, color='8C93A3', lw=1.3)
    for a, b in [(0.28, 0.42), (0.6, 0.8)]:
        box(sh, 0.5 + 2.4 * a, ly - 0.07, 2.4 * (b - a), 0.14, fill=TK[0], radius=0.5)
    tx(sh, x + 0.05, 4.24, w - 0.1, 0.28, 'Candidate Intervals', size=13.5, bold=True, color=TK[0])
    return g_


# ---- stage 2: construct ---------------------------------------------------------------------------------
def construct(slide):
    g_ = group(slide); sh = g_.shapes
    x, w = Z['con']
    math_runs(sh, x + 0.1, 0.8, w - 0.2, 0.34, [('Evidence State ', TK[0], True, False, False), ('s', TK[0], True, True, False),
                                               ('k', TK[0], True, True, True)], 15, align='c')
    tx(sh, x + 0.1, 1.13, w - 0.2, 0.28, 'Accumulate Tool Results', size=13, bold=True, color=MUTE)
    cx0, cw = x + 0.14, w - 0.28
    for k, (nm, title, sub) in enumerate([('window', 'Intervals', 'Candidate Boundaries'),
                                          ('data', 'Numerical Evidence', 'Statistics · Changes'),
                                          ('memory', 'Context', 'Retrieved Knowledge')]):
        y = 1.55 + k * 0.86
        card(sh, cx0, y, cw, 0.76, key='tsk')
        ic(sh, nm, cx0 + 0.07, y + 0.12, 0.52)
        tx(sh, cx0 + 0.64, y + 0.07, cw - 0.68, 0.32, title, size=14, bold=True, align='l')
        tx(sh, cx0 + 0.64, y + 0.4, cw - 0.68, 0.28, sub, size=12.5, bold=True, color=MUTE, align='l')
    return g_


# ---- stage 3: detect ------------------------------------------------------------------------------------
def detect(slide):
    g_ = group(slide); sh = g_.shapes
    x, w = Z['det']
    pedestal(sh, x + 0.16, 1.3, 0.92, 0.24, 'llm')
    ic(sh, 'llm', x + 0.3, 0.78, 0.64)
    tx(sh, x + 1.18, 0.8, 1.95, 0.34, 'Learned Detector', size=15, bold=True, color=LL[0], align='l')
    pill(sh, x + 1.2, 1.18, 1.18, 0.3, 'LLM-Side', key='llm', size=12.5)
    plot(sh, x + 0.15, 1.72, w - 0.3, 2.12, CAND, 'Candidate Region', 'llm')
    tx(sh, x + 0.1, 3.95, w - 0.2, 0.3, 'Interval Decisions', size=13.5, bold=True, color=LL[0])
    return g_


# ---- stage 4: refine ------------------------------------------------------------------------------------
def refine(slide):
    g_ = group(slide); sh = g_.shapes
    x, w = Z['ref']
    ic(sh, 'anomaly', x + 0.2, 0.8, 0.62)
    tx(sh, x + 0.92, 0.8, 2.2, 0.62, ['Review Uncertain', 'Intervals'], size=15, bold=True, color=TK[0], align='l')
    plot(sh, x + 0.15, 1.72, w - 0.3, 2.12, REFINED, 'Refined Interval', 'tsk')
    tx(sh, x + 0.1, 3.95, w - 0.2, 0.3, 'Accept or Revise', size=13.5, bold=True, color=TK[0])
    return g_


def flows(slide):
    g_ = group(slide); sh = g_.shapes
    y = 2.83
    arrow(sh, 3.16, y, 3.53, y, color=TK[0], lw=2.6)
    arrow(sh, 6.3, y, 6.68, y, color=TK[0], lw=2.6)
    arrow(sh, 9.63, y, 10.03, y, color=LL[0], lw=2.6)
    # return path: refinement updates the evidence state
    yb = 5.0
    rpath(sh, [(12.55, 3.86), (12.55, yb), (4.9, yb), (4.9, 4.14)], TK[0], lw=2.4, dash=MSO_LINE.DASH, r=0.2)
    b = box(sh, 7.9, yb - 0.17, 2.1, 0.34, fill='FFFFFF', line=TK[1], lw=1.0, radius=0.5)
    label_in(b, 'Update Evidence', size=13.5, color=TK[0], italic=True)
    return g_


# ---- lower band: detector training ----------------------------------------------------------------------
def training(slide):
    g_ = group(slide); sh = g_.shapes
    cy = 6.5
    p1 = box(sh, 0.5, cy - 0.25, 2.0, 0.5, fill=LL[2], line=LL[1], lw=1.2, radius=0.5); shadow(p1)
    label_in(p1, 'SFT Initialization', size=14, color=LL[0])
    arrow(sh, 2.56, cy, 2.98, cy, color=LL[0], lw=2.6)
    p2 = box(sh, 3.02, cy - 0.25, 0.78, 0.5, fill=LL[0], radius=0.5); shadow(p2)
    label_in(p2, 'RL', size=15)
    arrow(sh, 4.42, cy, 3.86, cy, color=LL[0], lw=2.6)
    # reward card: parse validity + interval agreement - false-positive penalty
    rx, ry, rw, rh = 4.48, 5.98, 8.45, 1.06
    card(sh, rx, ry, rw, rh, key='llm')
    math_runs(sh, rx + 0.12, ry + 0.06, 1.3, rh - 0.12, [('Reward ', LL[0], True, False, False), ('r', LL[0], True, True, False),
                                                       ('k', LL[0], True, True, True)], 15)
    gy, ly = ry + 0.1, ry + 0.7
    c1, c2, c3 = 6.65, 9.05, 11.6
    ic(sh, 'validate', c1 - 0.27, gy, 0.54)
    tx(sh, c1 - 0.9, ly, 1.8, 0.3, 'Parse Validity', size=13.5, bold=True, color=LL[0])
    tx(sh, 7.62, ry + 0.22, 0.5, 0.42, '+', size=26, bold=True, color=INK)
    # interval agreement: labeled vs predicted interval, overlap shaded
    ax, aw = c2 - 0.75, 1.5
    ov = box(sh, ax + aw * 0.3, gy + 0.06, aw * 0.42, 0.44, fill=LL[1], shape=MSO_SHAPE.RECTANGLE); alpha_fill(ov, 55)
    for (a, b, yy, col) in [(0.08, 0.72, gy + 0.16, INK), (0.3, 0.95, gy + 0.4, LL[0])]:
        arrow(sh, ax + aw * a, yy, ax + aw * b, yy, color=col, lw=2.4, head='oval', tail='oval')
    tx(sh, c2 - 1.0, ly, 2.0, 0.3, 'Interval Agreement', size=13.5, bold=True, color=LL[0])
    tx(sh, 10.08, ry + 0.25, 0.5, 0.4, '−', size=22, bold=True, color=INK)
    # false-positive penalty: a spurious spike, circled
    fx, fw = c3 - 0.8, 1.6
    sig(sh, fx, gy + 0.04, fw, 0.46, lambda t: 0.3 + 1.2 * noise(t, 0.7) + 0.55 * g(t, 0.55, 0.018), lw=1.4, n=110)
    box(sh, fx + fw * 0.55 - 0.24, gy - 0.02, 0.48, 0.56, line=TK[0], lw=1.6, shape=MSO_SHAPE.OVAL, dash=MSO_LINE.DASH)
    tx(sh, c3 - 1.15, ly, 2.3, 0.3, 'False-Positive Penalty', size=13.5, bold=True, color=LL[0])
    return g_


def build(out=OUT):
    p, slide = new_slide(H)
    stage_zone(slide, 'acq', '1', 'Acquire', 'tsk')
    stage_zone(slide, 'con', '2', 'Construct', 'tsk')
    stage_zone(slide, 'det', '3', 'Detect', 'llm')
    stage_zone(slide, 'ref', '4', 'Refine', 'tsk')
    zone(slide, 0.2, 5.62, 12.93, 1.62, 'Detector Training', 'llm', bw=3.1)
    acquire(slide)
    construct(slide)
    detect(slide)
    refine(slide)
    training(slide)
    flows(slide)
    save(p, out)
    return out


if __name__ == '__main__':
    print(build(sys.argv[1] if len(sys.argv) > 1 else OUT))
