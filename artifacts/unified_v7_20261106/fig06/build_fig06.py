"""Figure 6 (fig:general-harness-functions): five functions of the General Harness, V7 house style.

Upper zone: one interaction episode around the LLM. Interface and Interaction (left), Planning and Orchestration
(top, one icon per second-level class), Tools and Execution (right), Memory and Context (bottom); each card's
subtitle lists its second-level classes. Amber arrows = the LLM acting; dashed blue = the Harness returning.
Lower zone: Optimization and Evolution turns recorded trajectories into tested updates, one asset per class
(Prompt Optimization, Experience Distillation, Tool and Skill Evolution, Harness Configuration Search), which feed
the next episode.
"""
import os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *
from PIL import ImageFont

H = 7.25
LD, LM, LL = HUE['llm']
GD, GM, GL = HUE['gh']
CX = W / 2
ROBOT = (CX, 2.14, 1.3)       # centre x, top y, size
EP = (0.2, 0.42, 12.93, 4.78)  # episode zone
EV = (0.2, 5.62, 12.93, 1.46)  # optimization zone


FONTS = {False: '/System/Library/Fonts/Supplemental/Comic Sans MS.ttf',
         True: '/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf'}
WARN = []


def T(sh, x, y, w, h, t, size=13, bold=True, color=INK, align='c', italic=False):
    """kit text box + a width check against the box (all boxes are non-wrapping)."""
    assert size >= 11.5, (t, size)
    for ln in (t if isinstance(t, list) else [t]):
        lw = ImageFont.truetype(FONTS[bold], int(size * 20)).getlength(ln) / (20 * 72)
        if lw > w - 0.04: WARN.append(f'overflow {ln!r} {lw:.2f} > {w:.2f}')
    return tx(sh, x, y, w, h, t, size=size, bold=bold, color=color, align=align, italic=italic)


def ico(name, fallback):
    return name if os.path.exists(os.path.join(ICON_DIR, name + '.png')) else fallback


def side_card(sh, x, y, w, h, icon, title, sub):
    sh = sh.add_group_shape().shapes
    card(sh, x, y, w, h, 'gh')
    ic(sh, icon, x + w / 2 - 0.52, y + 0.15, 1.04)
    T(sh, x, y + 1.27, w, 0.34, title, size=16, bold=True)
    T(sh, x, y + 1.66, w, 0.52, sub, size=12.5, color=GD, bold=True)


def episode(slide):
    zone(slide, *EP, 'Interaction Episode', 'gh')
    g = group(slide); sh = g.shapes
    rx, ry, rs = ROBOT
    # Planning and Orchestration (top): what it covers, from the caption
    pw, py, ph = 10.25, 0.78, 1.14
    px = CX - pw / 2
    root = sh; sh = root.add_group_shape().shapes
    card(sh, px, py, pw, ph, 'gh')
    ic(sh, 'planning', px + 0.14, py + 0.18, 0.78)
    T(sh, px + 1.0, py + ph / 2 - 0.18, 3.0, 0.36, 'Planning and Orchestration', size=16, bold=True, align='l')
    subs = [('schema', ['Decomposition', 'and Planning']), ('process', ['Execution', 'Control']),
            ('validate', ['Checkpoints and', 'Governance']), ('planner_team', ['Multi-Agent', 'Coordination'])]
    sx, iw = px + 4.15, 1.5
    arrow(sh, sx - 0.1, py + 0.14, sx - 0.1, py + ph - 0.14, color=GM, lw=1.0, head=None)
    for k, (nm, lab) in enumerate(subs):
        cx = sx + iw / 2 + k * iw
        ic(sh, nm, cx - 0.27, py + 0.07, 0.54)
        T(sh, cx - iw / 2, py + 0.6, iw, 0.48, lab, size=12.5, color=MUTE, bold=True)
    # side cards
    sh = root
    cw, ch, cy, cm = 3.7, 2.36, 2.2, 0.45
    side_card(sh, cm, cy, cw, ch, 'chat', 'Interface and Interaction',
              ['Reasoning Loop · Action Interface', 'Environment and Users'])
    side_card(sh, W - cm - cw, cy, cw, ch, 'tools', 'Tools and Execution',
              ['Function Calls · Code and Job Execution', 'Verification Tools'])
    # Memory and Context (bottom)
    mw, my, mh = 4.25, 4.1, 1.0
    mx = CX - mw / 2
    sh = root.add_group_shape().shapes
    card(sh, mx, my, mw, mh, 'gh')
    ic(sh, 'memory', mx + 0.16, my + 0.13, 0.74)
    T(sh, mx + 1.0, my + 0.06, mw - 1.06, 0.36, 'Memory and Context', size=16, bold=True, align='l')
    T(sh, mx + 1.0, my + 0.43, mw - 1.06, 0.5, ['Working Context · Episodic Records', 'Knowledge Retrieval · Shared State'],
      size=12.5, color=GD, bold=True, align='l')
    # LLM
    sh = root.add_group_shape().shapes
    halo(sh, rx, ry + 0.66, 1.9, 1.62)
    pedestal(sh, rx - 0.64, ry + rs - 0.2, 1.28, 0.32, 'llm')
    ic(sh, 'robot', rx - rs / 2, ry, rs)
    lab = box(sh, rx - 0.7, ry + rs + 0.17, 1.4, 0.32, fill=LD, radius=0.5); label_in(lab, 'LLM: Caller', size=14)
    # spokes: amber = LLM acts, dashed blue = Harness returns
    sh = root.add_group_shape().shapes
    my_ = ry + 0.62
    lx0, lx1 = cm + cw + 0.08, rx - 0.95
    arrow(sh, lx0, my_ - 0.2, lx1, my_ - 0.2, color=GD, lw=2.4, dash=MSO_LINE.DASH)
    arrow(sh, lx1, my_ + 0.2, lx0, my_ + 0.2, color=LD, lw=2.6)
    tx(sh, lx0, my_ - 0.56, lx1 - lx0, 0.3, 'Observe', size=14, bold=True, italic=True, color=GD)
    tx(sh, lx0, my_ + 0.27, lx1 - lx0, 0.3, 'Respond', size=14, bold=True, italic=True, color=LD)
    rx0, rx1 = rx + 0.95, W - cm - cw - 0.08
    arrow(sh, rx0, my_ - 0.2, rx1, my_ - 0.2, color=LD, lw=2.6)
    arrow(sh, rx1, my_ + 0.2, rx0, my_ + 0.2, color=GD, lw=2.4, dash=MSO_LINE.DASH)
    tx(sh, rx0, my_ - 0.56, rx1 - rx0, 0.3, 'Call', size=14, bold=True, italic=True, color=LD)
    tx(sh, rx0, my_ + 0.27, rx1 - rx0, 0.3, 'Return', size=14, bold=True, italic=True, color=GD)
    # planning (above) and memory (below)
    top, bot = py + ph + 0.06, my - 0.06
    curve(sh, [(rx - 0.5, ry + 0.1), (rx - 0.85, ry + 0.02), (rx - 1.2, top)], LD, lw=2.6)
    curve(sh, [(rx + 1.2, top), (rx + 0.85, ry + 0.02), (rx + 0.5, ry + 0.1)], GD, lw=2.4, dash=MSO_LINE.DASH)
    curve(sh, [(rx - 0.78, ry + 1.2), (rx - 1.0, ry + 1.45), (rx - 1.1, bot)], LD, lw=2.6)
    curve(sh, [(rx + 1.1, bot), (rx + 1.0, ry + 1.45), (rx + 0.78, ry + 1.2)], GD, lw=2.4, dash=MSO_LINE.DASH)
    return g


def evolution(slide):
    x0, y0, w0, h0 = EV
    zone(slide, *EV, 'Optimization and Evolution', 'gh')
    g = group(slide); sh = g.shapes
    by, bh = y0 + 0.37, 0.92
    cy = by + bh / 2
    # recorded trajectories
    paper(sh, 0.45, by, 2.05, bh, line=GM)
    ic(sh, ico('trajectory_path', 'process'), 0.53, cy - 0.33, 0.66)
    T(sh, 1.24, by, 1.24, bh, ['Recorded', 'Trajectories'], size=14, bold=True, align='l')
    # tested updates
    card(sh, 3.08, by, 1.7, bh, 'gh')
    ic(sh, 'validate', 3.17, cy - 0.33, 0.66)
    T(sh, 3.88, by, 0.86, bh, ['Tested', 'Updates'], size=14, bold=True, align='l')
    arrow(sh, 2.66, cy, 3.0, cy, color=GD, lw=2.6)
    arrow(sh, 4.86, cy, 5.2, cy, color=GD, lw=2.6)
    # reusable assets, one per second-level class
    ax0, ax1 = 5.28, 12.88
    card(sh, ax0, by, ax1 - ax0, bh, 'gh', fill=GL)
    items = [('request', ['Prompt', 'Optimization']), ('memory', ['Experience', 'Distillation']),
             ('tools', ['Tool and Skill', 'Evolution']), ('sliders', ['Harness', 'Configuration', 'Search'])]
    isz, lsz = 0.6, 13
    fnt = ImageFont.truetype(FONTS[True], int(lsz * 20))
    lws = [max(fnt.getlength(t) for t in lab) / (20 * 72) + 0.08 for _, lab in items]
    gap = (ax1 - ax0 - sum(isz + 0.06 + lw for lw in lws)) / (len(items) + 1)
    bx = ax0 + gap
    for (nm, lab), lw in zip(items, lws):
        ic(sh, nm, bx, cy - isz / 2, isz)
        T(sh, bx + isz + 0.06, by, lw, bh, lab, size=lsz, bold=True, color=GD, align='l')
        bx += isz + 0.06 + lw + gap
    return g


def across(slide):
    """Episode -> recorded trajectories; updated assets -> next episode."""
    g = group(slide); sh = g.shapes
    # the episode's trajectories are recorded; tested updates return to later episodes (zone to zone)
    arrow(sh, 2.17, 5.22, 2.17, 5.86, color=GD, lw=2.6, dash=MSO_LINE.DASH)
    tx(sh, 0.95, 5.3, 1.1, 0.3, 'Record', size=14, bold=True, italic=True, color=GD, align='r')
    arrow(sh, 10.14, 6.0, 10.14, 5.22, color=GD, lw=2.8)
    tx(sh, 10.28, 5.3, 1.1, 0.3, 'Update', size=14, bold=True, italic=True, color=GD, align='l')
    return g


def build(out):
    p, slide = new_slide(H)
    episode(slide)
    evolution(slide)
    across(slide)
    save(p, out)
    for w in WARN: print('WARN', w)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'Figure06_V7.pptx'))
