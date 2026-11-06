"""V4 Sketch Notebook: sticky notes on plain paper, hand-drawn outlines, cycle around the agent."""
import math
from common import *
from pptx.enum.dml import MSO_LINE

ST, F = 'clay', 'Comic Sans MS'
H = 7.45   # slide height: notes area + time-series band
NOTE = dict(llm='FFE8A3', gh='CFE0FF', gts='C9F0E4', tsk='FFD3CC', ev='E3DCFF')


def _smooth(t):
    return 0.5 * math.sin(2 * math.pi * t * 5.2) + 0.2 * math.sin(2 * math.pi * t * 17.3 + 1.1) + 0.4 * t


def _y(t):
    """Deterministic seasonal series with a trend; t in [0, 1]."""
    noise = 0.16 * math.sin(97.1 * t + 0.3) + 0.11 * math.sin(211.7 * t + 2.0) + 0.07 * math.sin(353.9 * t)
    return 0.5 * math.sin(2 * math.pi * t * 5.2) + 0.2 * math.sin(2 * math.pi * t * 17.3 + 1.1) + 0.4 * t + noise


def poly(sh, pts, color, lw=1.6, dash=None, fill=None, alpha=None, closed=False):
    ff = sh.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    ff.add_line_segments([(Inches(x), Inches(y)) for x, y in pts[1:]], close=closed)
    s = ff.convert_to_shape()
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
        if alpha is not None:
            clr = s.fill._xPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
            etree.SubElement(clr, qn('a:alpha')).set('val', str(int(alpha * 1000)))
    else:
        s.fill.background()
    if color:
        s.line.color.rgb = rgb(color); s.line.width = Pt(lw)
        if dash: s.line.dash_style = dash
    else:
        s.line.fill.background()
    return s


def sparkline(sh, x, y, w, h, color):
    n = 120
    pts = [(x + w * k / n, y + h / 2 - h / 2.4 * _y(k / n)) for k in range(n + 1)]
    poly(sh, pts, color, lw=1.5)


def fanline(sh, x, y, w, h):
    """Noisy observed history, then a smooth dashed forecast with a widening band."""
    n, cut = 120, 78
    py = lambda v: y + h / 2 - h / 2.4 * v
    hist = [(x + w * k / n, py(_y(k / n))) for k in range(cut + 1)]
    trend = lambda k: 0.5 * math.sin(2 * math.pi * k / n * 5.2) + 0.4 * k / n
    d = _y(cut / n) - trend(cut)
    fut = [(x + w * k / n, py(trend(k) + d)) for k in range(cut, n + 1)]
    m = n - cut
    up = [(px, q - 0.02 - 0.12 * i / m) for i, (px, q) in enumerate(fut)]
    lo = [(px, q + 0.02 + 0.12 * i / m) for i, (px, q) in enumerate(fut)]
    poly(sh, up + lo[::-1], None, fill=C['tsk'], alpha=25, closed=True)
    poly(sh, hist, '333333', lw=1.4)
    poly(sh, fut, C['tsk'], lw=1.4, dash=MSO_LINE.DASH)


def time_band(slide):
    """History up to the information cutoff t0, then a forecast with widening uncertainty."""
    g = group(slide); sh = g.shapes
    x0, x1, t0, yc, amp = 0.55, 12.25, 9.35, 6.9, 0.2
    n = 220; kc = int(n * (t0 - x0) / (x1 - x0))
    xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    ys = [yc - amp * _y(k / n) for k in range(n + 1)]
    off = ys[kc] - (yc - amp * _smooth(kc / n))
    for k in range(kc + 1, n + 1):
        ys[k] = yc - amp * _smooth(k / n) + off
    ka = int(n * 0.3)                       # injected anomaly in the observed history
    ys[ka] -= 0.26
    box(sh, x0 - 0.1, 6.42, t0 - x0 + 0.1, 0.86, fill='EEF1F6', line=None, radius=0.15)
    text(sh, x0, 6.44, 3.2, 0.2, 'history: observed and available to the Agent', size=7.4, italic=True, color='555555', font=F, align='l')
    text(sh, t0 + 0.1, 6.44, 3.4, 0.2, 'future: forecast horizon, not yet observed', size=7.4, italic=True, color=C['tsk'], font=F, align='l')
    up = [(xs[k], ys[k] - 0.03 - 0.2 * (k - kc) / (n - kc)) for k in range(kc, n + 1)]
    lo = [(xs[k], ys[k] + 0.03 + 0.2 * (k - kc) / (n - kc)) for k in range(kc, n + 1)]
    poly(sh, up + lo[::-1], None, fill=C['tsk'], alpha=22, closed=True)
    poly(sh, list(zip(xs[:kc + 1], ys[:kc + 1])), '2B2B2B', lw=1.8)
    poly(sh, list(zip(xs[kc:], ys[kc:])), C['tsk'], lw=1.8, dash=MSO_LINE.DASH)
    cut = arrow(sh, t0, 6.4, t0, 7.3, color=C['gts'], lw=2, head=None, dash=MSO_LINE.DASH); sketchy(cut)
    tl = box(sh, t0 - 0.62, 7.12, 1.24, 0.24, fill=C['gts'], radius=0.5)
    label_in(tl, 't₀  information cutoff', size=7.2, font=F)
    an = box(sh, xs[ka] - 0.17, ys[ka] - 0.12, 0.34, 0.3, line=C['tsk'], lw=1.6, shape=MSO_SHAPE.OVAL); sketchy(an)
    text(sh, xs[ka] + 0.2, ys[ka] - 0.13, 0.9, 0.2, 'anomaly', size=7.2, bold=True, color=C['tsk'], font=F, align='l')
    icon(sh, ST, 'decision', 12.38, 6.72, 0.46)
    arrow(sh, x1 + 0.02, ys[-1], 12.4, 6.95, color=C['ev'], lw=1.4)
    text(sh, 12.05, 6.47, 1.1, 0.2, 'decision', size=7.2, bold=True, color=C['ev'], font=F, align='r')
    ax = arrow(sh, x0, 7.36, 12.95, 7.36, color='555555', lw=1.4); sketchy(ax)
    text(sh, 12.35, 7.16, 0.6, 0.2, 'time', size=7.4, italic=True, color='555555', font=F, align='r')
    lead = arrow(sh, 9.75, 5.72, t0 + 0.05, 6.4, color=C['gts'], lw=1.2, dash=MSO_LINE.ROUND_DOT)
    return g


def note(slide, st, x, y, w, h, rot):
    g = group(slide); sh = g.shapes
    n = box(sh, x, y, w, h, fill=NOTE[st['key']], line='3A3A3A', lw=1.5, shape=MSO_SHAPE.RECTANGLE)
    sketchy(n); n.rotation = rot
    tape = box(sh, x + w / 2 - 0.35, y - 0.1, 0.7, 0.2, fill='F2F2E6', line='BDBDB0', lw=0.5, shape=MSO_SHAPE.RECTANGLE)
    tape.rotation = rot - 3
    text(sh, x + 0.12, y + 0.08, w - 0.8, 0.3, st['name'], size=11 if len(st['name']) < 20 else 9.6, bold=True, color=C[st['key']], font=F, align='l')
    tag = box(sh, x + 0.12, y + 0.38, 0.85, 0.22, fill='FFFFFF', line=C[st['key']], lw=1.2, radius=0.5); sketchy(tag)
    label_in(tag, st['verb'], size=7.8, color=C[st['key']], font=F)
    icon(sh, ST, st['icon'], x + w - 0.74, y + 0.04, 0.68)
    text(sh, x + 0.12, y + 0.62, w - 0.85, 0.32, st['role'], size=7.8, italic=True, color='333333', font=F, align='l', anchor='t')
    text(sh, x + 0.12, y + 0.95, w - 0.2, h - 1.25, ['– ' + i for i in st['items']], size=7.3, color='222222', font=F, align='l', anchor='t')
    text(sh, x + 0.12, y + h - 0.3, w - 0.2, 0.24, '→ ' + st['claim'], size=7.6, bold=True, color=C[st['key']], font=F, align='l')
    return g


def hand_arrow(sh, x1, y1, x2, y2, color='333333', lw=2, label=None, lx=None, ly=None, curve=True, lwid=1.6):
    a = arrow(sh, x1, y1, x2, y2, color=color, lw=lw, curve=curve)
    if label:
        text(sh, lx, ly, lwid, 0.24, label, size=7.6, italic=True, color=color, font=F)
    return a


def build(out):
    p, slide = new_pres(h=H)
    box(slide.shapes, 0, 0, 13.333, H, fill='FFFEF9', shape=MSO_SHAPE.RECTANGLE)
    tg = group(slide)
    text(tg.shapes, 1.2, 0.08, 11, 0.5, TITLE, size=21, bold=True, color='2B2B2B', font=F, align='l')
    ul = arrow(tg.shapes, 1.25, 0.58, 5.6, 0.58, color=C['llm'], lw=3, head=None); sketchy(ul)
    text(tg.shapes, 5.9, 0.12, 7.2, 0.3, MOTTO, size=9.5, bold=True, italic=True, color=C['gh'], font=F, align='r')
    text(tg.shapes, 5.9, 0.42, 7.2, 0.26, 'Key claim: ' + KEY, size=8.4, bold=True, color='333333', font=F, align='r')
    w, h = 2.65, 1.95
    pos = dict(llm=(5.35, 0.85, -1.5), gh=(9.35, 1.25, 1.5), gts=(9.35, 3.75, -1), tsk=(5.35, 4.3, 1), ev=(1.4, 2.6, -1.5))
    for k, (x, y, r) in pos.items():
        note(slide, S[k], x, y, w, h, r)
    ag = group(slide); a = ag.shapes
    # cycle arrows
    hand_arrow(a, 8.05, 1.7, 9.3, 1.95, color=C['llm'], label=FLOW['act'], lx=7.9, ly=1.35)
    hand_arrow(a, 9.3, 2.55, 8.05, 2.5, color=C['gh'], label=FLOW['obs'], lx=7.75, ly=2.55)
    hand_arrow(a, 11.0, 3.25, 11.0, 3.72, color=C['gh'], label=FLOW['ops'], lx=11.1, ly=3.35)
    hand_arrow(a, 9.3, 4.9, 8.05, 5.2, color=C['gts'], label=FLOW['cap'], lx=8.05, ly=5.5, lwid=1.25)
    hand_arrow(a, 5.3, 5.3, 4.1, 4.4, color=C['tsk'], label=FLOW['cand'], lx=3.25, ly=5.05)
    hand_arrow(a, 3.4, 2.55, 5.3, 1.5, color=C['ev'], lw=2.8, label=FLOW['fb'], lx=3.9, ly=2.5)
    for c in a:
        if c.__class__.__name__ == 'Connector':
            sketchy(c)
    # centre agent
    icon(slide.shapes, 'clay', 'robot', 5.95, 2.75, 1.45)
    bub = slide.shapes.add_shape(MSO_SHAPE.CLOUD_CALLOUT, Inches(7.3), Inches(2.85), Inches(1.75), Inches(0.85))
    bub.fill.solid(); bub.fill.fore_color.rgb = rgb('FFFFFF'); bub.line.color.rgb = rgb('333333'); bub.line.width = Pt(1.2)
    bub.adjustments[0], bub.adjustments[1] = -0.62, 0.35
    label_in(bub, 'reuse, adapt, rebuild, verify', size=8, color='333333', font=F, bold=False)
    # input / output index cards
    ig = group(slide); i = ig.shapes
    ic = box(i, 1.25, 0.85, 2.3, 1.2, fill='FFFFFF', line='333333', lw=1.2, shape=MSO_SHAPE.RECTANGLE); sketchy(ic); ic.rotation = 2
    icon(i, ST, INPUT['icon'], 1.35, 0.95, 0.6)
    text(i, 2.0, 0.92, 1.5, 0.5, INPUT['name'], size=9, bold=True, color='2B2B2B', font=F, align='l')
    text(i, 1.35, 1.6, 2.15, 0.35, INPUT['sub'], size=7.2, italic=True, color='555555', font=F, align='l')
    hand_arrow(i, 3.55, 1.25, 5.3, 1.25, color='333333', curve=False)
    oc = box(i, 1.25, 5.0, 2.3, 1.15, fill='FFFFFF', line='333333', lw=1.2, shape=MSO_SHAPE.RECTANGLE); sketchy(oc); oc.rotation = -2
    icon(i, ST, OUTPUT['icon'], 1.35, 5.1, 0.6)
    text(i, 2.0, 5.07, 1.5, 0.55, OUTPUT['name'], size=8.6, bold=True, color='2B2B2B', font=F, align='l')
    text(i, 1.35, 5.72, 2.15, 0.3, FLOW['stop'], size=7.2, italic=True, color='555555', font=F, align='l')
    oa = hand_arrow(i, 2.4, 4.6, 2.4, 4.98, color=C['ev'], curve=False); sketchy(oa)
    # reuse note
    sparkline(i, 2.05, 1.28, 1.35, 0.26, C['gh'])
    fanline(i, 2.05, 5.42, 1.35, 0.26)
    time_band(slide)
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
