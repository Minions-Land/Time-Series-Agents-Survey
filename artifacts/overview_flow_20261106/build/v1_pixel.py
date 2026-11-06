"""V1 Pixel Arcade: AI4AI-style pixel robot loop with detail cards on both sides."""
from common import *
from pptx.enum.dml import MSO_LINE

ST = 'pixel'
HF = 'Menlo'          # retro monospace headings
BF = 'Avenir Next'


def card(slide, st, x, y, w, h):
    g = group(slide); sh = g.shapes
    box(sh, x, y, w, h, fill=C['white'], line=C['navy'], lw=1.5, radius=0.06)
    hb = box(sh, x, y, w, 0.34, fill=C[st['key']], line=C['navy'], lw=1.5, radius=0.18)
    label_in(hb, f"{st['sec']}  {st['name'].upper()}", size=9.5, font=HF, align='l')
    hb.text_frame.margin_left = Inches(0.5)
    icon(sh, ST, st['icon'], x + 0.04, y - 0.1, 0.48)
    text(sh, x + 0.12, y + 0.38, w - 0.24, 0.24, st['role'], size=8, italic=True, color=C['mute'], font=BF, align='l')
    text(sh, x + 0.12, y + 0.6, w - 0.24, h - 1.02, ['▪ ' + i for i in st['items']], size=7.6, color=C['ink'], font=BF, align='l', anchor='t')
    # logo chips, two per row
    cw = (w - 0.3) / 2
    for k, (name, lg) in enumerate(st['works'][:4]):
        cx = x + 0.12 + (k % 2) * (cw + 0.06); cy = y + h - 0.44 + (k // 2) * 0.2 - (0.2 if len(st['works']) > 2 else 0) + 0.2
        cy = y + h - 0.46 + (k // 2) * 0.21
        chip = box(sh, cx, cy, cw, 0.18, fill='F3F0E8', line='C9C2B2', lw=0.5, radius=0.5)
        if lg: logo(sh, lg, cx + 0.03, cy + 0.015, 0.15)
        text(sh, cx + 0.2, cy, cw - 0.22, 0.18, name, size=6.8, bold=True, color=C['ink'], font=BF, align='l')
    return g


def badge(sh, x, y, w, t, fill=C['navy'], size=9):
    b = box(sh, x - w / 2, y - 0.16, w, 0.32, fill=fill, line=C['navy'], lw=1.2, radius=0.12)
    return label_in(b, t, size=size, font=HF)


def build(out):
    p, slide = new_pres()
    box(slide.shapes, 0, 0, 13.333, 6.4, fill=C['cream'], shape=MSO_SHAPE.RECTANGLE)
    # title
    tg = group(slide)
    t = box(tg.shapes, 3.9, 0.12, 5.53, 0.46, fill=C['navy'], radius=0.2)
    label_in(t, TITLE, size=12.5, font=HF)
    for dx in (3.6, 9.55):
        text(tg.shapes, dx, 0.14, 0.2, 0.4, '✦', size=14, color=C['llm'])
    # side cards
    lx, rx, cw = 0.22, 9.5, 3.62
    card(slide, S['llm'], lx, 0.85, cw, 1.62)
    card(slide, S['gh'], lx, 2.62, cw, 1.78)
    card(slide, S['gts'], lx, 4.55, cw, 1.68)
    card(slide, S['tsk'], rx, 0.85, cw, 1.7)
    card(slide, S['ev'], rx, 2.7, cw, 1.7)
    # IO key card
    kg = group(slide); ks = kg.shapes
    box(ks, rx, 4.55, cw, 1.68, fill=C['white'], line=C['navy'], lw=1.5, radius=0.06)
    icon(ks, ST, INPUT['icon'], rx + 0.12, 4.66, 0.6); icon(ks, ST, OUTPUT['icon'], rx + 0.12, 5.42, 0.6)
    text(ks, rx + 0.8, 4.68, cw - 0.9, 0.56, ['IN  ' + INPUT['name'], INPUT['sub']], size=8.4, font=HF, align='l', color=C['ink'])
    text(ks, rx + 0.8, 5.44, cw - 0.9, 0.56, ['OUT ' + OUTPUT['name'], OUTPUT['sub']], size=8.4, font=HF, align='l', color=C['ink'])
    # center loop
    cx, cy, rxl, ryl = 6.665, 3.45, 2.05, 1.75
    lg = group(slide); ls = lg.shapes
    ring = box(ls, cx - rxl, cy - ryl, 2 * rxl, 2 * ryl, line='8A93B2', lw=2, shape=MSO_SHAPE.OVAL, dash=MSO_LINE.DASH)
    plat = box(ls, cx - 0.95, cy + 0.27, 1.9, 0.42, fill='D9D4C7', line='B9B2A2', lw=1, shape=MSO_SHAPE.OVAL)
    icon(ls, ST, 'robot', cx - 0.82, cy - 1.15, 1.64)
    badge(ls, cx, cy + 0.8, 1.6, 'LLM selects actions', fill=C['llm'], size=7.5)
    pos = dict(gh=(cx, cy - ryl), gts=(cx + rxl, cy), tsk=(cx, cy + ryl), ev=(cx - rxl, cy))
    order = ['gh', 'gts', 'tsk', 'ev']
    lab = dict(gh=FLOW['ops'], gts=FLOW['cap'], tsk=FLOW['cand'])
    for a, b in zip(order, order[1:]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        sx = 0.62 if x2 > x1 else -0.62 if x2 < x1 else 0
        arrow(ls, x1 + (0.55 if x2 > x1 else -0.55 if x2 < x1 else 0), y1 + (0.2 if y2 > y1 else -0.2),
              x2 + (0 if x2 != x1 else 0), y2 + (-0.2 if y2 > y1 else 0.2), color=C['navy'], lw=2)
    for k in order:
        x, y = pos[k]
        icon(ls, ST, S[k]['icon'], x - 1.22, y - 0.28, 0.55) if k in ('gh', 'tsk') else icon(ls, ST, S[k]['icon'], x - 0.28, y - 0.82, 0.55)
        badge(ls, x, y, 1.15, f"{S[k]['short']} {S[k]['sec']}", fill=C[k])
    # flow labels along chords
    text(ls, cx + 1.05, cy - 1.35, 1.3, 0.3, FLOW['ops'], size=7, italic=True, color=C['mute'], font=BF)
    text(ls, cx + 1.05, cy + 1.05, 1.3, 0.3, FLOW['cap'], size=7, italic=True, color=C['mute'], font=BF)
    text(ls, cx - 2.35, cy + 1.05, 1.3, 0.3, FLOW['cand'], size=7, italic=True, color=C['mute'], font=BF)
    # LLM <-> GH and EVAL -> LLM
    arrow(ls, cx + 0.25, cy - 1.15, cx + 0.25, cy - ryl + 0.18, color=C['llm'], lw=2.2)
    text(ls, cx + 0.3, cy - 1.45, 0.8, 0.22, FLOW['act'], size=7, bold=True, color=C['llm'], font=HF, align='l')
    arrow(ls, cx - 0.25, cy - ryl + 0.18, cx - 0.25, cy - 1.15, color=C['gh'], lw=1.5, dash=MSO_LINE.DASH)
    text(ls, cx - 1.1, cy - 1.45, 0.8, 0.22, FLOW['obs'], size=7, bold=True, color=C['gh'], font=HF, align='r')
    arrow(ls, cx - rxl + 0.58, cy, cx - 0.8, cy - 0.15, color=C['ev'], lw=2.4)
    text(ls, cx - rxl + 0.5, cy - 0.42, 1.2, 0.22, FLOW['fb'], size=7, bold=True, color=C['ev'], font=HF, align='l')
    # input / output tokens
    ig = box(ls, 4.05, 0.82, 1.3, 0.3, fill=C['white'], line=C['navy'], lw=1.2, radius=0.3)
    label_in(ig, 'IN: series + task', size=7.5, color=C['navy'], font=HF)
    arrow(ls, 5.0, 1.12, cx - 0.55, cy - 1.05, color=C['navy'], lw=1.4)
    og = box(ls, 4.05, 5.75, 1.3, 0.3, fill=C['white'], line=C['navy'], lw=1.2, radius=0.3)
    label_in(og, 'OUT: accepted', size=7.5, color=C['navy'], font=HF)
    arrow(ls, cx - rxl, cy + 0.18, 4.7, 5.75, color=C['navy'], lw=1.4)
    text(ls, 4.0, 5.2, 1.2, 0.3, FLOW['stop'], size=7, italic=True, color=C['mute'], font=BF, align='l')
    # reuse axis
    ag = group(slide)
    arrow(ag.shapes, 7.5, 6.12, 9.3, 6.12, color=C['mute'], lw=1.2)
    text(ag.shapes, 6.5, 5.86, 2.9, 0.22, 'GH → GTS → TSK: ' + FLOW['axis'], size=7, italic=True, color=C['mute'], font=BF, align='r')
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
