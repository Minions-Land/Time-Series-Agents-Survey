"""Figure 14 (fig:benchmark-infrastructure), V7 house style: TimeClaw-Harness runtime and capability evolution.

Top: the generalist LLM selects an operation and its parameters, then uses the returned evidence. Middle: temporal
tools execute on the full-precision numerical workspace and return compact structured observations; episodic
memory retrieves a successful episode by signal and context keys. Bottom: experience-driven tool evolution turns
executed traces into candidate tools, tests them on held-out tasks and registers them in the runtime tool set.
"""
import os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *
from pptx.enum.dml import MSO_LINE

H = 7.5
SAND = 'A49A86'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figure14_V7.pptx')
MID_Y, MID_B = 2.85, 4.95       # middle row of zones (top, bottom)
EVO_Y, EVO_B = 5.75, 7.36        # evolution zone


def llm_zone(slide):
    zone(slide, 0.2, 0.42, 8.75, 1.68, 'Generalist LLM', 'llm')
    g = group(slide); sh = g.shapes
    dk, md, lt = HUE['llm']
    b = box(sh, 0.42, 0.98, 1.9, 0.66, fill='FFF6E3', line='D9C49A', lw=0.8, radius=0.3)
    label_in(b, ['Task + Context', '+ Observations'], size=13, bold=False, color=INK, italic=True)
    arrow(sh, 2.36, 1.31, 2.66, 1.31, color=SAND, lw=2.4)
    halo(sh, 3.2, 1.22, 1.3, 1.05)
    pedestal(sh, 2.8, 1.58, 0.8, 0.26, 'llm')
    ic(sh, 'llm', 2.72, 0.7, 0.96)
    arrow(sh, 3.72, 1.31, 4.06, 1.31, color=dk, lw=2.4)
    for x, w, lines in [(4.1, 2.3, ['Select Operation', '& Parameters']), (6.82, 1.96, ['Use the Returned', 'Evidence'])]:
        c = card(sh, x, 0.9, w, 0.82, 'llm')
        label_in(c, lines, size=15, color=dk)
    arrow(sh, 6.44, 1.31, 6.78, 1.31, color=dk, lw=2.4)
    return g


def workspace_zone(slide):
    zone(slide, 0.2, MID_Y, 4.25, MID_B - MID_Y, 'Numerical Workspace', 'data')
    g = group(slide); sh = g.shapes
    dk = HUE['data'][0]
    tx(sh, 0.4, 3.17, 3.85, 0.36, 'Full-Precision Series', size=15.5, bold=True, color=INK)
    x0, y0, cws, rh = 0.52, 3.6, [1.0, 1.35, 1.35], 0.3
    rows = [[[('Time', INK, True, False)], [('Channel 1', INK, True, False)], [('Channel 2', INK, True, False)]],
            [[('t', INK, False, False), ('1', INK, False, True)], [('x', INK, False, False), ('1,1', INK, False, True)],
             [('x', INK, False, False), ('1,2', INK, False, True)]],
            [[('t', INK, False, False), ('2', INK, False, True)], [('x', INK, False, False), ('2,1', INK, False, True)],
             [('x', INK, False, False), ('2,2', INK, False, True)]]]
    shadow(box(sh, x0, y0, sum(cws), rh * 3, fill='FFFFFF', line='B9A98A', lw=1.2, shape=MSO_SHAPE.RECTANGLE))
    for r, row in enumerate(rows):
        x = x0
        for c, parts in enumerate(row):
            cell = box(sh, x, y0 + r * rh, cws[c], rh, fill='EFE7D6' if r == 0 else 'FFFFFF', line='B9A98A', lw=0.9,
                       shape=MSO_SHAPE.RECTANGLE)
            runs(cell, parts, 13)
            x += cws[c]
    tx(sh, 0.3, 4.58, 4.05, 0.3, 'Windows & Metadata Remain Addressable', size=13, color=dk, bold=True)
    return g


def tools_zone(slide):
    zone(slide, 4.6, MID_Y, 4.35, MID_B - MID_Y, 'Temporal Tools', 'gts')
    g = group(slide); sh = g.shapes
    dk, md, lt = HUE['gts']
    tx(sh, 4.65, 3.17, 3.75, 0.32, 'Execute Directly on the Workspace', size=13.5, italic=True, bold=True, color=MUTE)
    for k, (nm, cap) in enumerate([('window', 'Slice'), ('transform', 'Transform'), ('anomaly', 'Analyze')]):
        cx = 5.43 + k * 1.13
        ic(sh, nm, cx - 0.31, 3.5, 0.62)
        tx(sh, cx - 0.6, 4.1, 1.2, 0.28, cap, size=14, bold=True, color=dk)
    pill(sh, 4.82, 4.47, 3.36, 0.34, 'Compact Structured Observations', key='gts', size=13, light=True)
    return g


def memory_zone(slide):
    zone(slide, 9.1, 0.42, 4.03, MID_B - 0.42, 'Episodic Memory', 'gh')
    g = group(slide); sh = g.shapes
    dk, md, lt = HUE['gh']
    for k, (nm, title, sub) in enumerate([('signal_key', 'Signal Key', 'Shape & Statistical Structure'),
                                          ('context_key', 'Context Key', 'Task & Textual Context')]):
        y = 0.88 + k * 0.92
        card(sh, 9.3, y, 3.63, 0.8, 'gh')
        ic(sh, nm, 9.37, y + 0.07, 0.66)
        tx(sh, 10.1, y + 0.05, 2.7, 0.36, title, size=15.5, bold=True, color=dk, align='l')
        tx(sh, 10.1, y + 0.41, 2.8, 0.3, sub, size=13, color=MUTE, align='l', bold=True)
    arrow(sh, 11.12, 2.62, 11.12, 2.86, color=dk, lw=2.4)
    ic(sh, 'memory', 9.42, 2.82, 0.58)
    tx(sh, 10.05, 2.88, 2.95, 0.44, 'Retrieve a Successful Episode', size=14, bold=True, color=dk, align='l')
    paper(sh, 9.32, 3.55, 3.45, 1.22, line=md, n=2)
    ic(sh, 'snowstorm', 9.42, 3.6, 0.6)
    tx(sh, 10.04, 3.71, 1.15, 0.36, 'Snowstorm', size=14, bold=True, color=INK, align='l')
    arrow(sh, 11.22, 3.89, 11.52, 3.89, color=INK, lw=2.0)
    tx(sh, 11.58, 3.71, 0.82, 0.36, 'Demand', size=14, bold=True, color=INK, align='l')
    arrow(sh, 12.5, 4.04, 12.5, 3.72, color=HUE['tsk'][0], lw=2.6)
    tx(sh, 9.4, 4.3, 3.3, 0.34, 'Rationale + Analytical Trace', size=13, color=MUTE, bold=True)
    return g


def evolution_zone(slide):
    g0 = zone(slide, 0.2, EVO_Y, 12.93, EVO_B - EVO_Y, None, 'ink')
    banner(g0.shapes, 3.6, EVO_Y - 0.25, 5.5, 'Experience-Driven Tool Evolution', INK, size=19)
    g = group(slide); sh = g.shapes
    steps = [('process', 'Executed Traces', ['Cluster Recurring', 'Procedures'], 'gh'),
             ('tools', 'Candidate Tool', ['Code + Invocation', 'Description'], 'gts'),
             ('benchmark', 'Held-Out Tasks', ['Meet the Success', 'Threshold'], 'ev'),
             ('toolbox', 'Registered Tool', ['Available to', 'Later Episodes'], 'gts')]
    cw, gap = 2.88, 0.42
    x = 0.2 + (12.93 - 4 * cw - 3 * gap) / 2
    for k, (nm, title, sub, key) in enumerate(steps):
        card(sh, x, 6.08, cw, 1.1, key)
        ic(sh, nm, x + 0.08, 6.2, 0.86)
        tx(sh, x + 0.98, 6.12, cw - 1.0, 0.38, title, size=15.5, bold=True, color=HUE[key][0], align='l')
        tx(sh, x + 0.98, 6.5, cw - 1.0, 0.6, sub, size=13, color=MUTE, align='l', bold=True)
        if k < 3:
            arrow(sh, x + cw + 0.07, 6.63, x + cw + gap - 0.07, 6.63, color=INK, lw=2.4)
        x += cw + gap
    return g


def flows(slide):
    g = group(slide); sh = g.shapes
    am, ts, bl = HUE['llm'][0], HUE['gts'][0], HUE['gh'][0]
    # operation + parameters down to the tools
    arrow(sh, 5.0, 1.74, 5.0, 2.97, color=am, lw=2.6)
    tx(sh, 2.5, 2.16, 2.35, 0.32, 'Operation + Parameters', size=14, bold=True, italic=True, color=am, align='r')
    # tools execute on the workspace
    arrow(sh, 5.08, 3.82, 4.32, 3.82, color=ts, lw=2.6)
    # compact observations back up to the LLM
    curve(sh, [(8.2, 4.64), (8.95, 3.4), (8.25, 1.76)], INK, lw=2.2, dash=MSO_LINE.DASH)
    # retrieved episode to the LLM
    curve(sh, [(9.38, 3.1), (8.9, 2.35), (8.77, 1.5)], bl, lw=2.6)
    # registered tools join the runtime tool set
    curve(sh, [(10.4, 6.06), (10.1, 5.15), (8.6, 4.9)], ts, lw=2.8)
    tx(sh, 10.42, 5.14, 2.7, 0.32, 'Add to the Runtime Tool Set', size=13.5, bold=True, italic=True, color=ts, align='l')
    return g


def build(out=OUT):
    p, slide = new_slide(H)
    llm_zone(slide)
    workspace_zone(slide)
    tools_zone(slide)
    memory_zone(slide)
    evolution_zone(slide)
    flows(slide)
    save(p, out)
    return out


if __name__ == '__main__':
    print(build())
