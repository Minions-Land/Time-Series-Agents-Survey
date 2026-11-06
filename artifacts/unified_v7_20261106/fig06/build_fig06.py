"""Figure 6 (fig:general-harness-functions): five functions of the General Harness, V7 house style.

Upper zone: one interaction episode around the LLM. Interface and Interaction (left), Planning and Orchestration
(top, with execution control, verification checkpoints and coordination between roles), Tools and Execution
(right), Memory and Context (bottom). Amber arrows = the LLM acting; dashed blue = the Harness returning.
Lower zone: Optimization and Evolution turns recorded trajectories into tested updates of prompts, memory and
tools, which feed the next episode.
"""
import os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *

H = 7.25
LD, LM, LL = HUE['llm']
GD, GM, GL = HUE['gh']
CX = W / 2
ROBOT = (CX, 2.14, 1.3)       # centre x, top y, size
EP = (0.2, 0.42, 12.93, 4.78)  # episode zone
EV = (0.2, 5.62, 12.93, 1.46)  # optimization zone


def ico(name, fallback):
    return name if os.path.exists(os.path.join(ICON_DIR, name + '.png')) else fallback


def side_card(sh, x, y, w, h, icon, title, sub):
    sh = sh.add_group_shape().shapes
    card(sh, x, y, w, h, 'gh')
    ic(sh, icon, x + w / 2 - 0.55, y + 0.2, 1.1)
    tx(sh, x, y + 1.42, w, 0.34, title, size=16, bold=True)
    tx(sh, x, y + 1.8, w, 0.3, sub, size=13.5, color=GD, bold=True)


def episode(slide):
    zone(slide, *EP, 'Interaction Episode', 'gh')
    g = group(slide); sh = g.shapes
    rx, ry, rs = ROBOT
    # Planning and Orchestration (top): what it covers, from the caption
    px, py, pw, ph = 2.42, 0.78, 8.49, 1.14
    root = sh; sh = root.add_group_shape().shapes
    card(sh, px, py, pw, ph, 'gh')
    ic(sh, 'planning', px + 0.14, py + 0.17, 0.78)
    tx(sh, px + 1.0, py + 0.17, 3.1, 0.36, 'Planning and Orchestration', size=16, bold=True, align='l')
    tx(sh, px + 1.0, py + 0.55, 3.1, 0.3, 'Dependencies and Handoffs', size=13.5, color=GD, bold=True, align='l')
    subs = [('process', ['Execution', 'Control']), ('validate', ['Verification', 'Checkpoints']),
            ('planner_team', ['Coordination', 'Between Roles'])]
    sx = px + 4.3
    arrow(sh, sx - 0.12, py + 0.14, sx - 0.12, py + ph - 0.14, color=GM, lw=1.0, head=None)
    for k, (nm, lab) in enumerate(subs):
        cx = sx + 0.68 + k * 1.38
        ic(sh, nm, cx - 0.27, py + 0.07, 0.54)
        tx(sh, cx - 0.68, py + 0.6, 1.36, 0.48, lab, size=12.5, color=MUTE, bold=True)
    # side cards
    sh = root
    cw, ch, cy = 3.25, 2.36, 2.2
    side_card(sh, 0.55, cy, cw, ch, 'chat', 'Interface and Interaction', 'Observations and Actions')
    side_card(sh, W - 0.55 - cw, cy, cw, ch, 'tools', 'Tools and Execution', 'Calls, Artifacts and Status')
    # Memory and Context (bottom)
    mx, my, mw, mh = 4.4, 4.18, 4.53, 0.9
    sh = root.add_group_shape().shapes
    card(sh, mx, my, mw, mh, 'gh')
    ic(sh, 'memory', mx + 0.16, my + 0.08, 0.74)
    tx(sh, mx + 1.0, my + 0.1, 3.4, 0.36, 'Memory and Context', size=16, bold=True, align='l')
    tx(sh, mx + 1.0, my + 0.47, 3.4, 0.3, 'Evidence and Working State', size=13.5, color=GD, bold=True, align='l')
    # LLM
    sh = root.add_group_shape().shapes
    halo(sh, rx, ry + 0.66, 1.9, 1.62)
    pedestal(sh, rx - 0.64, ry + rs - 0.2, 1.28, 0.32, 'llm')
    ic(sh, 'robot', rx - rs / 2, ry, rs)
    lab = box(sh, rx - 0.36, ry + rs + 0.17, 0.72, 0.32, fill=LD, radius=0.5); label_in(lab, 'LLM', size=14)
    # spokes: amber = LLM acts, dashed blue = Harness returns
    sh = root.add_group_shape().shapes
    my_ = ry + 0.62
    lx0, lx1 = 0.55 + cw + 0.08, rx - 0.95
    arrow(sh, lx0, my_ - 0.2, lx1, my_ - 0.2, color=GD, lw=2.4, dash=MSO_LINE.DASH)
    arrow(sh, lx1, my_ + 0.2, lx0, my_ + 0.2, color=LD, lw=2.6)
    tx(sh, lx0, my_ - 0.56, lx1 - lx0, 0.3, 'Observe', size=14, bold=True, italic=True, color=GD)
    tx(sh, lx0, my_ + 0.27, lx1 - lx0, 0.3, 'Respond', size=14, bold=True, italic=True, color=LD)
    rx0, rx1 = rx + 0.95, W - 0.55 - cw - 0.08
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
    cy = y0 + 0.82
    # recorded trajectories
    paper(sh, 0.72, y0 + 0.4, 2.85, 0.86, line=GM)
    ic(sh, ico('trajectory_path', 'process'), 0.82, y0 + 0.47, 0.72)
    tx(sh, 1.6, y0 + 0.47, 1.95, 0.72, ['Recorded', 'Trajectories'], size=14, bold=True, align='l')
    # tested updates
    card(sh, 4.3, y0 + 0.4, 2.45, 0.86, 'gh')
    ic(sh, 'validate', 4.41, y0 + 0.47, 0.72)
    tx(sh, 5.2, y0 + 0.47, 1.5, 0.72, ['Tested', 'Updates'], size=14, bold=True, align='l')
    arrow(sh, 3.68, cy, 4.2, cy, color=GD, lw=2.6)
    arrow(sh, 6.85, cy, 7.37, cy, color=GD, lw=2.6)
    # reusable assets
    card(sh, 7.47, y0 + 0.4, 5.34, 0.86, 'gh', fill=GL)
    for k, (nm, lab) in enumerate([('request', 'Prompts'), ('memory', 'Memory'), ('tools', 'Tools')]):
        bx = 7.62 + k * 1.74
        ic(sh, nm, bx, y0 + 0.5, 0.66)
        tx(sh, bx + 0.7, y0 + 0.5, 0.95, 0.66, lab, size=14, bold=True, color=GD, align='l')
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


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'Figure06_V7.pptx'))
