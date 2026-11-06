"""V1 loop layout: the agent at the centre of a GH -> GTS -> TSK -> EVAL loop, claim cards on both sides.

style='pixel' gives the pixel-arcade look; style='notes' gives sticky notes on plain paper (V6).
"""
from common import *
from pptx.enum.dml import MSO_LINE

NOTE = dict(llm='FFE8A3', gh='CFE0FF', gts='C9F0E4', tsk='FFD3CC', ev='E3DCFF')
LOOK = {
    'pixel': dict(icons='pixel', robot='pixel', HF='Menlo', BF='Avenir Next', bg=C['cream'], ring='8A93B2'),
    'notes': dict(icons='clay', robot='clay', HF='Comic Sans MS', BF='Comic Sans MS', bg='FFFEF9', ring='9AA0B4'),
}
ROT = dict(llm=-1.2, gh=0.8, gts=-0.6, tsk=1.0, ev=-0.8, io=0.6)


def card(slide, L, style, st, x, y, w, h):
    g = group(slide); sh = g.shapes; k = st['key']
    if style == 'pixel':
        box(sh, x, y, w, h, fill=C['white'], line=C['navy'], lw=1.5, radius=0.06)
        hb = box(sh, x, y, w, 0.34, fill=C[k], line=C['navy'], lw=1.5, radius=0.18)
        label_in(hb, f"{st['verb']}  ·  {st['name'].upper()}", size=9, font=L['HF'], align='l')
        hb.text_frame.margin_left = Inches(0.55)
        icon(sh, L['icons'], st['icon'], x + 0.04, y - 0.1, 0.48)
        tx, head_c = x + 0.12, C['ink']
    else:
        n = box(sh, x, y, w, h, fill=NOTE[k], line='3A3A3A', lw=1.4, shape=MSO_SHAPE.RECTANGLE)
        sketchy(n); n.rotation = ROT[k]
        tape = box(sh, x + w / 2 - 0.35, y - 0.1, 0.7, 0.2, fill='F2F2E6', line='BDBDB0', lw=0.5, shape=MSO_SHAPE.RECTANGLE)
        tape.rotation = ROT[k] - 3
        text(sh, x + 0.12, y + 0.04, w - 0.75, 0.3, [st['verb'] + '  ·  ' + st['name']], size=10.5, bold=True, color=C[k], font=L['HF'], align='l')
        icon(sh, L['icons'], st['icon'], x + w - 0.6, y + 0.03, 0.52)
        tx = x + 0.12
    text(sh, tx, y + 0.38, w - 0.7, 0.2, st['role'], size=7.8, italic=True, color=C['mute'], font=L['BF'], align='l')
    text(sh, tx, y + 0.6, w - 0.24, 0.7, ['▪ ' + i for i in st['items']], size=7.6, color=C['ink'], font=L['BF'], align='l', anchor='t')
    strip = box(sh, x + 0.1, y + h - 0.38, w - 0.2, 0.3, fill=C[k] if style == 'pixel' else 'FFFFFF',
                line=None if style == 'pixel' else C[k], lw=1.2, radius=0.35)
    label_in(strip, '→ ' + st['claim'], size=7.6, color='FFFFFF' if style == 'pixel' else C[k], font=L['BF'])
    return g


def io_card(slide, L, style, x, y, w, h):
    g = group(slide); ks = g.shapes
    if style == 'pixel':
        box(ks, x, y, w, h, fill=C['white'], line=C['navy'], lw=1.5, radius=0.06)
    else:
        n = box(ks, x, y, w, h, fill='FFFFFF', line='3A3A3A', lw=1.4, shape=MSO_SHAPE.RECTANGLE); sketchy(n); n.rotation = ROT['io']
    icon(ks, L['icons'], INPUT['icon'], x + 0.12, y + 0.1, 0.5); icon(ks, L['icons'], OUTPUT['icon'], x + 0.12, y + 0.66, 0.5)
    text(ks, x + 0.72, y + 0.12, w - 0.8, 0.46, ['IN   ' + INPUT['name'], INPUT['sub']], size=8.2, font=L['HF'], align='l', color=C['ink'])
    text(ks, x + 0.72, y + 0.68, w - 0.8, 0.46, ['OUT  ' + OUTPUT['name'], OUTPUT['sub']], size=8.2, font=L['HF'], align='l', color=C['ink'])
    kb = box(ks, x + 0.1, y + h - 0.5, w - 0.2, 0.4, fill=C['navy'] if style == 'pixel' else 'FFF3C4',
             line=None if style == 'pixel' else '3A3A3A', lw=1, radius=0.25)
    label_in(kb, ['KEY CLAIM', KEY], size=7.4, color='FFFFFF' if style == 'pixel' else C['ink'], font=L['BF'])
    return g


def badge(sh, L, style, x, y, w, t, fill, size=8.5):
    b = box(sh, x - w / 2, y - 0.16, w, 0.32, fill=fill, line=C['navy'] if style == 'pixel' else '3A3A3A', lw=1.2, radius=0.3)
    if style == 'notes': sketchy(b)
    return label_in(b, t, size=size, font=L['HF'])


def build(out, style='pixel'):
    L = LOOK[style]; HF, BF = L['HF'], L['BF']
    p, slide = new_pres()
    box(slide.shapes, 0, 0, 13.333, 6.4, fill=L['bg'], shape=MSO_SHAPE.RECTANGLE)
    tg = group(slide)
    if style == 'pixel':
        t = box(tg.shapes, 4.4, 0.08, 4.53, 0.44, fill=C['navy'], radius=0.2)
        label_in(t, TITLE, size=13, font=HF)
        for dx in (4.1, 9.05):
            text(tg.shapes, dx, 0.1, 0.2, 0.4, '✦', size=14, color=C['llm'])
    else:
        text(tg.shapes, 3.6, 0.04, 6.13, 0.46, TITLE, size=19, bold=True, color='2B2B2B', font=HF)
        ul = arrow(tg.shapes, 4.3, 0.5, 9.0, 0.5, color=C['llm'], lw=3, head=None); sketchy(ul)
    text(tg.shapes, 3.9, 0.54, 5.53, 0.22, MOTTO, size=8.2, italic=True, bold=True, color=C['gh'], font=BF)
    lx, rx, cw, ch = 0.22, 9.5, 3.62, 1.72
    ys = [0.85, 2.67, 4.49]
    for key, y in zip(['llm', 'gh', 'gts'], ys):
        card(slide, L, style, S[key], lx, y, cw, ch)
    for key, y in zip(['tsk', 'ev'], ys):
        card(slide, L, style, S[key], rx, y, cw, ch)
    io_card(slide, L, style, rx, ys[2], cw, ch)
    # centre loop
    cx, cy, rxl, ryl = 6.665, 3.5, 2.05, 1.75
    lg = group(slide); ls = lg.shapes
    box(ls, cx - rxl, cy - ryl, 2 * rxl, 2 * ryl, line=L['ring'], lw=2, shape=MSO_SHAPE.OVAL, dash=MSO_LINE.DASH)
    box(ls, cx - 0.95, cy + 0.27, 1.9, 0.42, fill='D9D4C7' if style == 'pixel' else 'EDE7DA', line=None, shape=MSO_SHAPE.OVAL)
    icon(ls, L['robot'], 'robot', cx - 0.82, cy - 1.15, 1.64)
    badge(ls, L, style, cx, cy + 0.8, 1.6, 'LLM · ALIGN', fill=C['llm'], size=8)
    pos = dict(gh=(cx, cy - ryl), gts=(cx + rxl, cy), tsk=(cx, cy + ryl), ev=(cx - rxl, cy))
    order = ['gh', 'gts', 'tsk', 'ev']
    for a, b in zip(order, order[1:]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        arrow(ls, x1 + (0.62 if x2 > x1 else -0.62 if x2 < x1 else 0), y1 + (0.2 if y2 > y1 else -0.2),
              x2, y2 + (-0.2 if y2 > y1 else 0.2), color=C['navy'], lw=2)
    for k in order:
        x, y = pos[k]
        if k in ('gh', 'tsk'):
            icon(ls, L['icons'], S[k]['icon'], x - 1.3, y - 0.28, 0.55)
        else:
            icon(ls, L['icons'], S[k]['icon'], x - 0.28, y - 0.82, 0.55)
        badge(ls, L, style, x, y, 1.42, f"{S[k]['short']} · {S[k]['verb']}", fill=C[k])
    text(ls, cx + 1.05, cy - 1.35, 1.3, 0.3, FLOW['ops'], size=7, italic=True, color=C['mute'], font=BF)
    text(ls, cx + 1.05, cy + 1.05, 1.3, 0.3, FLOW['cap'], size=7, italic=True, color=C['mute'], font=BF)
    text(ls, cx - 2.35, cy + 1.05, 1.3, 0.3, FLOW['cand'], size=7, italic=True, color=C['mute'], font=BF)
    # LLM <-> GH, EVAL -> LLM
    arrow(ls, cx + 0.25, cy - 1.15, cx + 0.25, cy - ryl + 0.18, color=C['llm'], lw=2.2)
    text(ls, cx + 0.3, cy - 1.45, 0.8, 0.22, FLOW['act'], size=7, bold=True, color=C['llm'], font=HF, align='l')
    arrow(ls, cx - 0.25, cy - ryl + 0.18, cx - 0.25, cy - 1.15, color=C['gh'], lw=1.5, dash=MSO_LINE.DASH)
    text(ls, cx - 1.1, cy - 1.45, 0.8, 0.22, FLOW['obs'], size=7, bold=True, color=C['gh'], font=HF, align='r')
    arrow(ls, cx - rxl + 0.72, cy, cx - 0.8, cy - 0.15, color=C['ev'], lw=2.4)
    text(ls, cx - rxl + 0.62, cy - 0.42, 1.2, 0.22, FLOW['fb'], size=7, bold=True, color=C['ev'], font=HF, align='l')
    # input / output tokens
    ig = box(ls, 4.05, 0.85, 1.3, 0.3, fill=C['white'], line=C['navy'], lw=1.2, radius=0.3)
    label_in(ig, 'IN: data + task', size=7.5, color=C['navy'], font=HF)
    arrow(ls, 5.0, 1.15, cx - 0.55, cy - 1.05, color=C['navy'], lw=1.4)
    og = box(ls, 4.05, 5.8, 1.3, 0.3, fill=C['white'], line=C['navy'], lw=1.2, radius=0.3)
    label_in(og, 'OUT: accepted', size=7.5, color=C['navy'], font=HF)
    arrow(ls, cx - rxl, cy + 0.18, 4.7, 5.8, color=C['navy'], lw=1.4)
    text(ls, 4.0, 5.25, 1.2, 0.3, FLOW['stop'], size=7, italic=True, color=C['mute'], font=BF, align='l')
    ag = group(slide)
    arrow(ag.shapes, 7.5, 6.17, 9.3, 6.17, color=C['mute'], lw=1.2)
    text(ag.shapes, 6.3, 5.91, 3.0, 0.22, 'GH → GTS → TSK: ' + FLOW['axis'], size=7, italic=True, color=C['mute'], font=BF, align='r')
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1], *(sys.argv[2:3]))
