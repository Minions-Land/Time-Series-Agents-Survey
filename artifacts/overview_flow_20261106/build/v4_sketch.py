"""V4 Sketch Notebook: sticky notes on plain paper, hand-drawn outlines, cycle around the agent."""
from common import *

ST, F = 'pixel', 'Comic Sans MS'
NOTE = dict(llm='FFE8A3', gh='CFE0FF', gts='C9F0E4', tsk='FFD3CC', ev='E3DCFF')


def note(slide, st, x, y, w, h, rot):
    g = group(slide); sh = g.shapes
    n = box(sh, x, y, w, h, fill=NOTE[st['key']], line='3A3A3A', lw=1.5, shape=MSO_SHAPE.RECTANGLE)
    sketchy(n); n.rotation = rot
    tape = box(sh, x + w / 2 - 0.35, y - 0.1, 0.7, 0.2, fill='F2F2E6', line='BDBDB0', lw=0.5, shape=MSO_SHAPE.RECTANGLE)
    tape.rotation = rot - 3
    text(sh, x + 0.12, y + 0.08, w - 0.8, 0.3, st['name'], size=11 if len(st['name']) < 20 else 9.6, bold=True, color=C[st['key']], font=F, align='l')
    tag = box(sh, x + 0.12, y + 0.38, 0.85, 0.22, fill='FFFFFF', line=C[st['key']], lw=1.2, radius=0.5); sketchy(tag)
    label_in(tag, st['verb'], size=7.8, color=C[st['key']], font=F)
    icon(sh, ST, st['icon'], x + w - 0.68, y + 0.06, 0.6)
    text(sh, x + 0.12, y + 0.62, w - 0.2, 0.32, st['role'], size=7.8, italic=True, color='333333', font=F, align='l', anchor='t')
    text(sh, x + 0.12, y + 0.95, w - 0.2, h - 1.25, ['– ' + i for i in st['items']], size=7.3, color='222222', font=F, align='l', anchor='t')
    text(sh, x + 0.12, y + h - 0.3, w - 0.2, 0.24, '→ ' + st['claim'], size=7.6, bold=True, color=C[st['key']], font=F, align='l')
    return g


def hand_arrow(sh, x1, y1, x2, y2, color='333333', lw=2, label=None, lx=None, ly=None, curve=True):
    a = arrow(sh, x1, y1, x2, y2, color=color, lw=lw, curve=curve)
    if label:
        text(sh, lx, ly, 1.6, 0.24, label, size=7.6, italic=True, color=color, font=F)
    return a


def build(out):
    p, slide = new_pres()
    box(slide.shapes, 0, 0, 13.333, 6.4, fill='FFFEF9', shape=MSO_SHAPE.RECTANGLE)
    tg = group(slide)
    text(tg.shapes, 1.2, 0.08, 11, 0.5, TITLE, size=21, bold=True, color='2B2B2B', font=F, align='l')
    ul = arrow(tg.shapes, 1.25, 0.58, 5.6, 0.58, color=C['llm'], lw=3, head=None); sketchy(ul)
    text(tg.shapes, 5.9, 0.2, 7.2, 0.3, MOTTO, size=9.5, bold=True, italic=True, color=C['gh'], font=F, align='r')
    w, h = 2.65, 1.95
    pos = dict(llm=(5.35, 0.85, -1.5), gh=(9.35, 1.25, 1.5), gts=(9.35, 3.75, -1), tsk=(5.35, 4.3, 1), ev=(1.4, 2.6, -1.5))
    for k, (x, y, r) in pos.items():
        note(slide, S[k], x, y, w, h, r)
    ag = group(slide); a = ag.shapes
    # cycle arrows
    hand_arrow(a, 8.05, 1.7, 9.3, 1.95, color=C['llm'], label=FLOW['act'], lx=7.9, ly=1.35)
    hand_arrow(a, 9.3, 2.55, 8.05, 2.5, color=C['gh'], label=FLOW['obs'], lx=7.75, ly=2.55)
    hand_arrow(a, 11.0, 3.25, 11.0, 3.72, color=C['gh'], label=FLOW['ops'], lx=11.1, ly=3.35)
    hand_arrow(a, 9.3, 4.9, 8.05, 5.2, color=C['gts'], label=FLOW['cap'], lx=7.7, ly=5.42)
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
    text(slide.shapes, 6.0, 6.08, 7.1, 0.26, 'Key claim: ' + KEY, size=8.4, bold=True, color='333333', font=F, align='r')
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
