"""Refine the landscape fan chart (Figure 2) in the house palette while keeping its layout and content.

Input : artifacts/overview_revision_20261025/pptx/02_main_v2_source.pptx (the editable source, left untouched)
Output: Figure02_V7.pptx here; export.sh + crop() produce Figure02_V7.pdf / .png.
Changes: semantic sector tints (General Harness / General Time Series Harness / Task-Specific Harness), blue-violet
centre, hatch lines removed, softer spokes and ring outlines, canonical wording, clay icons, calmer tag text colours.
"""
import math, os, sys
from copy import deepcopy
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.enum.dml import MSO_LINE
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'kit'))
from v7kit import HUE, INK, ICON_DIR, rgb   # noqa: E402

SRC = os.path.join(HERE, '..', '..', 'overview_revision_20261025', 'pptx', '02_main_v2_source.pptx')
OUT = os.path.join(HERE, 'Figure02_V7.pptx')
CX, CY = 12.73, 10.53                                   # fan centre (group child coordinates, inches)
RINGS = [(2.07, 1.57), (4.25, 3.22), (7.58, 5.71), (12.23, 9.22)]   # (rx, ry): centre, inner, middle, outer
TINT = {   # (outer ring, middle ring, inner ring) per component
    'llm': ('FDF9F0', 'F9EFD9', 'F0DDB4'),
    'gh': ('F3F6FB', 'E6ECF6', 'CFDBEE'), 'gts': ('F1F8F7', 'E2F0EE', 'C9E3DF'), 'tsk': ('FCF5F1', 'F8E8E0', 'F0D2C4')}
YEAR, LINE_THIN, LINE_THICK, RING_LINE = '8E8573', 'B9BCDB', '7E82B8', 'C5C8E0'
E = 914400


def angle(x, y):
    return math.degrees(math.atan2((CY - y) / RINGS[3][1], (x - CX) / RINGS[3][0]))


def ends(sh):
    """Endpoints of a line shape, honouring flipH / flipV."""
    x0, y0, x1, y1 = sh.left / E, sh.top / E, (sh.left + sh.width) / E, (sh.top + sh.height) / E
    xf = sh._element.spPr.find(qn('a:xfrm'))
    if xf.get('flipH') == '1': x0, x1 = x1, x0
    if xf.get('flipV') == '1': y0, y1 = y1, y0
    return (x0, y0), (x1, y1)


def arc(rx, ry, a0, a1, n=90):
    return [(CX + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)), CY - ry * math.sin(math.radians(a0 + (a1 - a0) * k / n)))
            for k in range(n + 1)]


def sector(shapes, r_in, r_out, a0, a1, fill):
    pts = arc(*r_out, a0, a1) + (arc(*r_in, a1, a0) if r_in else [(CX, CY)])
    ff = shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    ff.add_line_segments([(Inches(x), Inches(y)) for x, y in pts[1:]], close=True)
    s = ff.convert_to_shape()
    s.fill.solid(); s.fill.fore_color.rgb = rgb(fill); s.line.fill.background()
    return s


def set_line(sh, color, width=None, dash=None):
    sh.line.color.rgb = rgb(color)
    if width: sh.line.width = Pt(width)


def set_lines(tb, lines, color, align=None, bold=None):
    """Replace a text box's lines, keeping the first run's font."""
    tf = tb.text_frame
    first = tf.paragraphs[0]
    rpr = deepcopy(first.runs[0]._r.find(qn('a:rPr'))) if first.runs else None
    ppr = first._p.find(qn('a:pPr'))
    txBody = tf._txBody
    for p in list(txBody.findall(qn('a:p'))): txBody.remove(p)
    for ln in lines:
        p = txBody.makeelement(qn('a:p'), {})
        if ppr is not None: p.append(deepcopy(ppr))
        r = p.makeelement(qn('a:r'), {})
        if rpr is not None: r.append(deepcopy(rpr))
        t = r.makeelement(qn('a:t'), {}); t.text = ln; r.append(t); p.append(r); txBody.append(p)
    for p in tf.paragraphs:
        if align is not None: p.alignment = align
        for r in p.runs:
            r.font.color.rgb = rgb(color)
            if bold is not None: r.font.bold = bold


def walk(shapes):
    for s in shapes:
        yield s
        if s.shape_type == 6: yield from walk(s.shapes)


def main():
    prs = Presentation(SRC)
    slide = prs.slides[0]
    g = slide.shapes[0]
    xfrm = deepcopy(g._element.grpSpPr.find(qn('a:xfrm')))      # python-pptx would re-fit the group; restore later

    v = lambda tag, att: int(xfrm.find(qn(tag)).get(att))
    kx, ky = v('a:ext', 'cx') / v('a:chExt', 'cx'), v('a:ext', 'cy') / v('a:chExt', 'cy')   # the group scales x and y differently
    to_child = lambda X, Y: ((v('a:chOff', 'x') + (X - v('a:off', 'x')) / kx) / E, (v('a:chOff', 'y') + (Y - v('a:off', 'y')) / ky) / E)
    to_slide = lambda x, y: (v('a:off', 'x') + (x * E - v('a:chOff', 'x')) * kx, v('a:off', 'y') + (y * E - v('a:chOff', 'y')) * ky)

    # 1) remove hatch lines, clear old ring fills, restyle outlines and spokes
    for s in list(g.shapes):
        if s.shape_type == 1 and s.line.fill.type == 1 and str(s.line.color.rgb) == 'DFDAEA':
            s._element.getparent().remove(s._element)
    for s in g.shapes:
        if s.shape_type == 5:
            if s.fill.type == 1: s.fill.background()
            if s.line.fill.type == 1:
                c = str(s.line.color.rgb)
                # from the centre outwards the outlines get thinner, lighter and more sparsely dashed
                w_, col_, dash_ = {'727783': (2.5, 'FFFFFF', MSO_LINE.SQUARE_DOT), 'CDA16B': (2.0, '9396C6', MSO_LINE.SQUARE_DOT),
                                   '8AB2CC': (1.5, 'A9ACD3', MSO_LINE.DASH), 'B6A1C9': (1.0, 'C5C8E0', MSO_LINE.LONG_DASH)}[c]
                set_line(s, col_, w_); s.line.dash_style = dash_
        elif s.shape_type == 1 and s.line.fill.type == 1 and str(s.line.color.rgb) == '686B75':
            if s.line.width.pt >= 1.9: set_line(s, LINE_THICK, 2.25)
            else: set_line(s, LINE_THIN, 1.0)

    # 2) wording and colours of the labels
    wedge = {
        'Interface\n& Interaction': (['Interface', 'and Interaction'], 'gh'),
        'Memory\n& Context': (['Memory', 'and Context'], 'gh'),
        'Tools\n& Execution': (['Tools', 'and Execution'], 'gh'),
        'Planning\n& Orchestration': (['Planning', 'and Orchestration'], 'gh'),
        'Optimization\n& Evolution': (['Optimization', 'and Evolution'], 'gh'),
        'Temporal Data\nManagement': (['Temporal Data', 'Management'], 'gts'),
        'Temporal \nProcessing': (['Temporal', 'Processing'], 'gts'),
        'Temporal \nContext & Memory': (['Temporal', 'Context and Memory'], 'gts'),
        'Temporal\nValidation': (['Temporal', 'Validation'], 'gts'),
        'Forecasting \nPrediction': (['Forecasting', 'and Prediction'], 'tsk'),
        'Data Augmentation\n& Synthesis': (['Data Augmentation', 'and Synthesis'], 'tsk'),
        'Anomaly Detection \n& Diagnosis': (['Anomaly Detection', 'and Diagnosis'], 'tsk'),
        'Decision\nSupport': (['Decision', 'Support'], 'tsk'),
    }
    by_id = {s.shape_id: s for s in g.shapes}
    wedge_labels = []
    for s in list(g.shapes):
        if s.shape_type != 17: continue
        t = s.text_frame.text
        if t in wedge:
            lines, key = wedge[t]; set_lines(s, lines, HUE[key][0]); wedge_labels.append(s.shape_id)
            size = {'Temporal \nContext & Memory': 14.5, 'Interface\n& Interaction': 15}.get(t, 16)
            for p in s.text_frame.paragraphs:
                for r in p.runs: r.font.size = Pt(size)          # "and" makes the labels longer than the old "&"
            if t.startswith('Interface'): s.left += Inches(0.18)   # keep clear of the icon on its left
            if t.startswith('Temporal \nContext'): s.top += Inches(0.2)   # keep clear of the icon above it
    # layer names in the inner ring: General Harness | General Time Series Harness | Task-Specific Harness
    set_lines(by_id[47], ['General'], HUE['gh'][0]); set_lines(by_id[79], ['Harness'], HUE['gh'][0])
    for i in (289, 80):
        b = by_id[i]; b.left, b.width = Inches(CX - 2.1), Inches(4.2)
    set_lines(by_id[289], ['General Time Series'], HUE['gts'][0], align=PP_ALIGN.CENTER)
    set_lines(by_id[80], ['Harness'], HUE['gts'][0], align=PP_ALIGN.CENTER)
    by_id[80].top = by_id[289].top + Inches(0.5)
    set_lines(by_id[1090], ['Task-Specific'], HUE['tsk'][0]); set_lines(by_id[83], ['Harness'], HUE['tsk'][0])
    by_id[1090].top = Inches(8.88); by_id[83].left, by_id[83].top = Inches(14.36), Inches(9.42)
    for i in (81, 82, 84, 85):                                   # "Module", duplicate "Time Series" lines
        by_id[i]._element.getparent().remove(by_id[i]._element)
    set_lines(by_id[165], ['Time Series', 'Agents'], 'FFFFFF', align=PP_ALIGN.CENTER)

    # 3) LLM side: one new wedge at the far left. Its content takes the old Interface wedge's place; everything
    #    else turns clockwise so that 180 deg maps onto the old Interface boundary.
    thin = [s for s in g.shapes if s.shape_type == 1 and s.line.fill.type == 1 and s.line.width.pt < 1.9]
    outer = lambda s: max(ends(s), key=lambda q: math.hypot(q[0] - CX, q[1] - CY))
    a_b = max(angle(*outer(s)) for s in thin)                # old Interface | Memory boundary (~166 deg)
    # piecewise angle map: Task-Specific (sparse) is compressed, the other sectors only turn clockwise
    OLD, NEW = [0.0, 61.0, 111.3, 180.0], [0.0, 50.0, 99.5, 168.0]
    A_LLM = NEW[-1]                                          # new General Harness | LLM-side boundary
    def G(a):
        for (o0, o1), (n0, n1) in zip(zip(OLD, OLD[1:]), zip(NEW, NEW[1:])):
            if a <= o1 or o1 == OLD[-1]: return n0 + (a - o0) * (n1 - n0) / (o1 - o0)
    H = lambda a: A_LLM + (a - a_b) * (180 - A_LLM) / (180 - a_b)   # old Interface wedge -> new LLM wedge
    f = A_LLM / 180.0
    centre = lambda s: ((s.left + s.width / 2) / E, (s.top + s.height / 2) / E)
    ids = iter(range(5000, 9000))

    def clone(el):
        c = deepcopy(el)
        for nv in c.iter(qn('p:cNvPr')): nv.set('id', str(next(ids)))
        return c

    tags = [s for s in g.shapes if s.shape_type == 6 and angle(*centre(s)) > a_b]
    iface = next(s for s in g.shapes if s.shape_type == 17 and s.text_frame.text.startswith('Interface'))
    icons = [s for s in slide.shapes if s.shape_type == 13]
    icon_iface = max(icons, key=lambda p: angle(*to_child(p.left + p.width / 2, p.top + p.height / 2)))
    keep = set()                                             # new LLM-wedge shapes: not rotated
    for s in tags + [iface, icon_iface]:
        c = clone(s._element); s._element.addnext(c); keep.add(c.find('.//' + qn('p:cNvPr')).get('id'))

    def rot(x, y, m=None):
        X, Y = (x - CX) / RINGS[3][0], (CY - y) / RINGS[3][1]
        r, a = math.hypot(X, Y), math.degrees(math.atan2(Y, X))
        b = (m or G)(a)
        return CX + r * RINGS[3][0] * math.cos(math.radians(b)), CY - r * RINGS[3][1] * math.sin(math.radians(b)), a - b

    def set_geom(s, p0, p1):
        (x0, y0), (x1, y1) = p0, p1
        s.left, s.top = Inches(min(x0, x1)), Inches(min(y0, y1)); s.width, s.height = Inches(abs(x1 - x0)), Inches(abs(y1 - y0))
        xf = s._element.spPr.find(qn('a:xfrm'))
        for k, on in (('flipH', x1 < x0), ('flipV', y1 < y0)):
            if on: xf.set(k, '1')
            elif k in xf.attrib: del xf.attrib[k]

    sid = lambda s: s._element.find('.//' + qn('p:cNvPr')).get('id')
    for s in list(g.shapes):
        if sid(s) in keep or s.shape_type == 5 or s.shape_id == 165: continue
        if s.shape_type == 1 and s.line.fill.type == 1:
            p0, p1 = ends(s); set_geom(s, rot(*p0)[:2], rot(*p1)[:2])
        else:
            x, y = centre(s); nx, ny, da = rot(x, y)
            s.left, s.top = int(Inches(nx) - s.width / 2), int(Inches(ny) - s.height / 2)
            if s.shape_id in wedge_labels: s.rotation = (s.rotation + da) % 360
    for s in list(g.shapes):                                 # the LLM wedge's own shapes: into the 12 deg wedge
        if sid(s) in keep:
            x, y = centre(s); nx, ny, _ = rot(x, y, H)
            s.left, s.top = int(Inches(nx) - s.width / 2), int(Inches(ny) - s.height / 2)
    for p in icons:                                          # top-level wedge icons (slide coordinates)
        x, y = to_child(p.left + p.width / 2, p.top + p.height / 2); nx, ny, _ = rot(x, y, H if sid(p) in keep else None)
        X, Y = to_slide(nx, ny); p.left, p.top = int(X - p.width / 2), int(Y - p.height / 2)

    # the new sector boundary: a thick spoke at the old Interface | Memory angle
    thick = [s for s in g.shapes if s.shape_type == 1 and s.line.fill.type == 1 and s.line.width.pt >= 1.9]
    t0 = thick[0]; (p0, p1) = ends(t0)
    norm = lambda q: math.hypot((q[0] - CX) / RINGS[3][0], (CY - q[1]) / RINGS[3][1])
    r_in, r_out = sorted((norm(p0), norm(p1)))
    at = lambda r: (CX + r * RINGS[3][0] * math.cos(math.radians(A_LLM)), CY - r * RINGS[3][1] * math.sin(math.radians(A_LLM)))
    c = clone(t0._element); t0._element.addnext(c)
    new_spoke = next(s for s in g.shapes if s._element is c)
    inward = math.hypot(p0[0] - CX, p0[1] - CY) < math.hypot(p1[0] - CX, p1[1] - CY)
    set_geom(new_spoke, at(r_in) if inward else at(r_out), at(r_out) if inward else at(r_in))

    # LLM wedge content: label, inner-ring name, five representative LLM-side works (logos reused from the figure)
    llm_label = next(s for s in g.shapes if sid(s) in keep and s.shape_type == 17)
    set_lines(llm_label, ['Align, Reason', 'and Operate'], HUE['llm'][0])   # the three routes of Section 3
    inner = clone(by_id[47]._element); by_id[47]._element.addnext(inner)
    name = next(s for s in g.shapes if s._element is inner)
    set_lines(name, ['LLM Side'], HUE['llm'][0], align=PP_ALIGN.CENTER)
    for r_ in name.text_frame.paragraphs[0].runs: r_.font.size = Pt(19)
    rm = (RINGS[0][0] + RINGS[1][0]) / 2 / RINGS[3][0]; am = (A_LLM + 180) / 2
    cx_, cy_ = CX + rm * RINGS[3][0] * math.cos(math.radians(am)), CY - rm * RINGS[3][1] * math.sin(math.radians(am))
    name.width, name.height = Inches(2.0), Inches(0.45); name.left, name.top = Inches(cx_ - 1.0), Inches(cy_ - 0.24)

    logo_of = {}
    def scan(shs):
        for c_ in shs:
            if c_.shape_type != 6: continue
            fl = list(walk(c_.shapes)); pics = [k for k in fl if k.shape_type == 13]
            nm = [k.text_frame.text.strip() for k in fl if k.shape_type == 17 and k.text_frame.text.strip()
                  and not k.text_frame.text.strip().isdigit()]
            if len(pics) == 1 and nm: logo_of.setdefault(nm[0], pics[0])
            else: scan(c_.shapes)
    scan(g.shapes)
    works = [('ChatTS', '2025', 'HFMD'), ('Time-R1', '2025', 'MemCast'), ('ChatAD', '2026', 'ChatAD'),
             ('STRIDE', '2026', 'STRIDE'), ('CastFSR', '2026', 'MemCast')]   # (name, year, tag whose logo matches)
    new_tags = sorted((s for s in g.shapes if sid(s) in keep and s.shape_type == 6), key=lambda s: s.top)
    for t, (nm, yr, src) in zip(new_tags, works):
        fl = list(walk(t.shapes))
        for k in fl:
            if k.shape_type == 17 and k.text_frame.text.strip():
                is_year = k.text_frame.text.strip().isdigit()
                run0 = k.text_frame.paragraphs[0].runs[0]
                for p in k.text_frame.paragraphs:
                    for r_ in p.runs[1:] if p is k.text_frame.paragraphs[0] else p.runs: r_.text = ''
                run0.text = yr if is_year else nm
        old = next(k for k in fl if k.shape_type == 13)
        newpic = clone(logo_of[src]._element)
        nx_ = newpic.find(qn('p:spPr')).find(qn('a:xfrm')); ox_ = old._element.find(qn('p:spPr')).find(qn('a:xfrm'))
        nx_.getparent().replace(nx_, deepcopy(ox_))
        old._element.addnext(newpic); old._element.getparent().remove(old._element)

    # local nudges where the narrower wedges bring neighbouring tag columns together (child inches)
    spokes = sorted(angle(*outer(s)) for s in g.shapes if s.shape_type == 1 and s.line.fill.type == 1)
    order = ['tsk4', 'tsk3', 'tsk2', 'tsk1', 'gts4', 'gts3', 'gts2', 'gts1', 'optimization', 'planning', 'tools', 'memory',
             'interface', 'llm']
    # the Interface column now sits between TradingAgents and the LLM boundary: tighten its row spacing
    col = [t for t in g.shapes if t.shape_type == 6 and sid(t) not in keep
           and order[sum(1 for b_ in spokes if b_ < angle(*centre(t)))] == 'interface']
    mx = sum(centre(t)[0] for t in col) / len(col); my = sum(centre(t)[1] for t in col) / len(col)
    for t in col:
        x, y = centre(t)
        t.left = int(Inches(mx + 0.9 * (x - mx)) - t.width / 2); t.top = int(Inches(my + 0.9 * (y - my)) - t.height / 2)
    low = max(col, key=lambda t: centre(t)[1]); low.left += Inches(0.5)   # bottom tag: inward, clear of the LLM boundary
    tname = lambda t: next((k.text_frame.text.strip() for k in walk(t.shapes) if k.shape_type == 17
                            and k.text_frame.text.strip() and not k.text_frame.text.strip().isdigit()), '')
    for t in g.shapes:                                       # last Memory tag: a little inward, away from the Interface column
        if t.shape_type == 6 and tname(t) == 'TradingAgents': t.left += Inches(0.12)

    # 3b) Task-Specific Harness sector: the four task groups of scripts/task_groups.py, in its order from the General
    #     Time Series Harness boundary (50 deg) clockwise. The wedges are re-cut by the number of works they hold; the
    #     representative works are unchanged and move to the wedge of their group.
    retask_tsk(g, slide, sid, keep, wedge_labels, centre, to_child, to_slide, tname)

    # progressive spokes: each spoke is split at the ring edges; per band the width falls, the colour lightens and
    # the dash gets sparser (solid -> dense dash -> sparse dash), matching the fading fill
    EDGE = [r[0] / RINGS[3][0] for r in RINGS]               # normalised radii of the ring edges
    BAND = {True: [(2.75, '7E82B8', MSO_LINE.SOLID), (2.0, '9A9DCB', MSO_LINE.SQUARE_DOT), (1.25, 'B6B9DC', MSO_LINE.DASH)],
            False: [(1.5, '9A9DCB', MSO_LINE.SOLID), (1.25, 'A9ACD3', MSO_LINE.SQUARE_DOT), (0.85, 'C5C8E0', MSO_LINE.DASH)]}
    for sp_ in [x for x in g.shapes if x.shape_type == 1 and x.line.fill.type == 1]:
        p0, p1 = ends(sp_); pin, pout = sorted((p0, p1), key=norm)
        a_, rin, rout = angle(*pout), norm(pin), norm(pout)
        ln = sp_.line._get_or_add_ln()
        arrow_ = any(e.get('type', 'none') != 'none' for e in ln if e.tag in (qn('a:headEnd'), qn('a:tailEnd')))
        P = lambda r: (CX + r * RINGS[3][0] * math.cos(math.radians(a_)), CY - r * RINGS[3][1] * math.sin(math.radians(a_)))
        for b_ in range(3):
            lo, hi = max(rin, EDGE[b_]), min(rout, EDGE[b_ + 1])
            if hi - lo < 0.01: continue
            c_ = clone(sp_._element); sp_._element.addprevious(c_)
            seg = next(x for x in g.shapes if x._element is c_)
            for e in list(seg.line._get_or_add_ln()):
                if e.tag in (qn('a:headEnd'), qn('a:tailEnd')): seg.line._get_or_add_ln().remove(e)
            set_geom(seg, P(lo), P(hi))
            w_, col_, dash_ = BAND[sp_.line.width.pt >= 1.9][b_]
            set_line(seg, col_, w_); seg.line.dash_style = dash_
            if arrow_ and hi >= rout - 1e-6:
                e = etree.SubElement(seg.line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle'); e.set('w', 'sm'); e.set('len', 'sm')
        sp_._element.getparent().remove(sp_._element)

    # 4) sector tints (now four sectors) and the blue-violet centre, at the bottom of the group
    thick = [s for s in g.shapes if s.shape_type == 1 and s.line.fill.type == 1 and s.line.width.pt >= 1.9]
    bounds = sorted({round(angle(*outer(s)), 2) for s in thick})   # tsk | gts, gts | gh, gh | llm (spokes are split in bands)
    a_tsk, a_gts, a_gh = bounds[0], bounds[1], bounds[2]
    comps = [('tsk', 0, a_tsk), ('gts', a_tsk, a_gts), ('gh', a_gts, a_gh), ('llm', a_gh, 180)]
    new = []
    for key, a0, a1 in comps:
        new.append(sector(g.shapes, RINGS[2], RINGS[3], a0, a1, TINT[key][0]))
        new.append(sector(g.shapes, RINGS[1], RINGS[2], a0, a1, TINT[key][1]))
        new.append(sector(g.shapes, RINGS[0], RINGS[1], a0, a1, TINT[key][2]))
    new.append(sector(g.shapes, None, RINGS[0], 0, 180, HUE['ink'][0]))
    sp = g._element
    anchor = sp.find(qn('p:grpSpPr'))
    for s in reversed(new):
        sp.remove(s._element); anchor.addnext(s._element)

    # 5) tags: names in ink, years in a warm grey
    for s in walk(g.shapes):
        if s.shape_type == 17 and s.text_frame.text.strip() and s.shape_id not in by_id:
            col = YEAR if s.text_frame.text.strip().isdigit() else INK
            for p in s.text_frame.paragraphs:
                for r in p.runs: r.font.color.rgb = rgb(col)

    g._element.grpSpPr.remove(g._element.grpSpPr.find(qn('a:xfrm')))
    g._element.grpSpPr.insert(0, xfrm)

    # 6) clay icons for the 14 wedges (top-level pictures), ordered left to right around the fan
    names = ['llm', 'chat', 'memory', 'tools', 'planning', 'runtime', 'calendar', 'window', 'timeline', 'cutoff',
             'anomaly', 'forecast', 'synthesis', 'decision']   # task groups: analysis, forecasting, generation, decision
    pics = [s for s in slide.shapes if s.shape_type == 13]
    cxs, cys = to_slide(CX, CY)
    pics.sort(key=lambda p: -math.atan2(cys - (p.top + p.height / 2), (p.left + p.width / 2) - cxs))
    for p, nm in zip(pics, names):
        c = (p.left + p.width / 2, p.top + p.height / 2); size = Inches(0.86)
        path = os.path.join(ICON_DIR + '_print', nm + '.png')
        slide.shapes.add_picture(path, int(c[0] - size / 2), int(c[1] - size / 2), size, size)
        p._element.getparent().remove(p._element)
    prs.save(OUT)
    print('saved', OUT, 'sectors at', [round(b, 1) for b in bounds], 'rotation factor', round(f, 4), 'icons', len(pics))


# Task-Specific Harness wedges (scripts/task_groups.py, ORDER): new boundaries in degrees, from 50 (GTS | TSK) to 0.
TSK_GROUPS = [('Analysis of', 'Observed Series'), ('Forecasting',), ('Generation',), ('Decision', 'Making')]
TSK_BOUNDS = [50.0, 29.5, 18.5, 9.5, 0.0]
# Representative works per group. A work goes to the group of its Task-Specific Harness modules (ledger task labels
# mapped by task_groups.LEAF); a work whose modules span two groups stays in the group that matches its former family
# wedge (MarsTSC, AgentFM, AQuA, AgriWorld), else its first source task decides (GenAutoML, ChatAD). MOSAIC has no
# Task-Specific Harness module; its source tasks are forecasting and synthesis, and it fills the Generation wedge.
# Stacks: (centre x of the top tag, top y, x shift per row, names), child inches; rows 0.26 in apart (as before).
# The positions were searched so that every tag stays inside its wedge and the outer band (checked against the wedge spokes and the ring edges).
TSK_STACKS = [
    [(21.0, 4.30, -0.32, ['ARTIST', 'TS-Exam Agent', 'WeatherTGD', 'Time-RA', 'ChatAD', 'TraceBench']),
     (22.15, 5.46, -0.5, ['SAGE-AD', 'AnomaMind', 'Argos', 'AgentFM', 'SAGE-Sleep'])],
    [(23.1, 6.66, -0.5, ['MemCast', 'Dr-CiK', 'MarsTSC', 'MoiraiAgent', 'GenAutoML'])],
    [(23.9, 8.22, -0.8, ['MERIT', 'MOSAIC'])],
    [(23.9, 9.48, 0.0, ['AgriWorld', 'Fin-Analyst', 'LLMTraveler']), (21.6, 9.70, 0.0, ['AQuA', 'PandaAI'])],
]


def retask_tsk(g, slide, sid, keep, wedge_labels, centre, to_child, to_slide, tname):
    P = lambda r, a: (CX + r * RINGS[3][0] * math.cos(math.radians(a)), CY - r * RINGS[3][1] * math.sin(math.radians(a)))
    norm = lambda q: math.hypot((q[0] - CX) / RINGS[3][0], (CY - q[1]) / RINGS[3][1])
    radial = lambda a: math.degrees(math.atan2(RINGS[3][1] * math.sin(math.radians(a)), RINGS[3][0] * math.cos(math.radians(a))))
    lim = TSK_BOUNDS[0] - 1
    mids = [(a0 + a1) / 2 for a0, a1 in zip(TSK_BOUNDS, TSK_BOUNDS[1:])]
    label_at, icon_at = list(mids), list(mids)
    label_at[0], icon_at[0] = 35.5, 43.0          # the wide Analysis wedge: label and icon side by side, not overlapping
    # spokes: the three thin spokes inside the sector move to the new boundaries (same radii)
    outer = lambda s: max(ends(s), key=norm)
    thin = sorted((s for s in g.shapes if s.shape_type == 1 and s.line.fill.type == 1 and s.line.width.pt < 1.9
                   and angle(*outer(s)) < lim), key=lambda s: -angle(*outer(s)))
    assert len(thin) == 3, len(thin)
    for s, a in zip(thin, TSK_BOUNDS[1:4]):
        p0, p1 = ends(s); r0, r1 = norm(p0), norm(p1)
        (x0, y0), (x1, y1) = P(r0, a), P(r1, a)
        s.left, s.top = Inches(min(x0, x1)), Inches(min(y0, y1)); s.width, s.height = Inches(abs(x1 - x0)), Inches(abs(y1 - y0))
        xf = s._element.spPr.find(qn('a:xfrm'))
        for k, on in (('flipH', x1 < x0), ('flipV', y1 < y0)):
            if on: xf.set(k, '1')
            elif k in xf.attrib: del xf.attrib[k]
    # wedge labels: group names, centred in the new wedge at the old radius, reading along the radius
    labels = sorted((s for s in g.shapes if s.shape_id in wedge_labels and angle(*centre(s)) < lim), key=lambda s: -angle(*centre(s)))
    assert len(labels) == 4
    for s, lines, a in zip(labels, TSK_GROUPS, label_at):
        r = norm(centre(s)) - 0.01
        set_lines(s, list(lines), HUE['tsk'][0], align=PP_ALIGN.CENTER)
        for p in s.text_frame.paragraphs:
            for run in p.runs: run.font.size = Pt(16)
        s.text_frame.word_wrap = False
        s.width = Inches(2.4)
        x, y = P(r, a)
        s.left, s.top = int(Inches(x) - s.width / 2), int(Inches(y) - s.height / 2)
        s.rotation = (-(radial(a) + 4)) % 360
    # icons (top-level pictures, slide coordinates): to the middle of the new wedge, same radius
    pics = [p for p in slide.shapes if p.shape_type == 13]
    tsk_pics = sorted((p for p in pics if angle(*to_child(p.left + p.width / 2, p.top + p.height / 2)) < lim),
                      key=lambda p: -angle(*to_child(p.left + p.width / 2, p.top + p.height / 2)))
    assert len(tsk_pics) == 4
    for p, a in zip(tsk_pics, icon_at):
        r = norm(to_child(p.left + p.width / 2, p.top + p.height / 2))
        X, Y = to_slide(*P(r, a)); p.left, p.top = int(X - p.width / 2), int(Y - p.height / 2)
    # tags
    tags = {tname(t): t for t in g.shapes if t.shape_type == 6 and sid(t) not in keep and angle(*centre(t)) < lim}
    placed = set()
    for stacks in TSK_STACKS:
        for cx, top, dx, names in stacks:
            for k, nm in enumerate(names):
                t = tags[nm]; placed.add(nm)
                t.left, t.top = int(Inches(cx + dx * k) - t.width / 2), Inches(top + 0.26 * k)
    assert placed == set(tags), set(tags) ^ placed


def crop(pdf):
    """Crop the exported page to the fan (the slide has empty space on the right)."""
    from PyPDF2 import PdfReader, PdfWriter
    r = PdfReader(pdf); pg = r.pages[0]
    h = float(pg.mediabox.top)                                  # PDF origin is bottom-left
    pg.cropbox.lower_left = (0.10 * 72, 0.0); pg.cropbox.upper_right = (22.16 * 72, h - 0.16 * 72)
    pg.mediabox.lower_left = pg.cropbox.lower_left; pg.mediabox.upper_right = pg.cropbox.upper_right
    w = PdfWriter(); w.add_page(pg)
    tmp = pdf + '.tmp.pdf'
    with open(tmp, 'wb') as fh: w.write(fh)
    os.replace(tmp, pdf)


if __name__ == '__main__':
    if sys.argv[1:2] == ['--crop']: crop(sys.argv[2])
    else: main()
