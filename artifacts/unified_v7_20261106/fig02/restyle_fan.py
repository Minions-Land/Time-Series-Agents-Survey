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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'kit'))
from v7kit import HUE, INK, ICON_DIR, rgb   # noqa: E402

SRC = os.path.join(HERE, '..', '..', 'overview_revision_20261025', 'pptx', '02_main_v2_source.pptx')
OUT = os.path.join(HERE, 'Figure02_V7.pptx')
CX, CY = 12.73, 10.53                                   # fan centre (group child coordinates, inches)
RINGS = [(2.07, 1.57), (4.25, 3.22), (7.58, 5.71), (12.23, 9.22)]   # (rx, ry): centre, inner, middle, outer
TINT = {   # (outer ring, middle ring, inner ring) per component
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

    # sector boundaries come from the two thick spokes
    thick = [s for s in g.shapes if s.shape_type == 1 and s.line.fill.type == 1 and s.line.width and s.line.width.pt >= 1.9]
    bounds = sorted(max(angle(*p) for p in ends(s)) if False else angle(*max(ends(s), key=lambda q: math.hypot(q[0] - CX, q[1] - CY)))
                    for s in thick)
    a_tsk, a_gts = bounds[0], bounds[1]                       # e.g. ~61 deg and ~111 deg
    comps = [('tsk', 0, a_tsk), ('gts', a_tsk, a_gts), ('gh', a_gts, 180)]

    # 1) remove hatch lines, clear old ring fills, restyle outlines and spokes
    for s in list(g.shapes):
        if s.shape_type == 1 and s.line.fill.type == 1 and str(s.line.color.rgb) == 'DFDAEA':
            s._element.getparent().remove(s._element)
    for s in g.shapes:
        if s.shape_type == 5:
            if s.fill.type == 1: s.fill.background()
            if s.line.fill.type == 1:
                c = str(s.line.color.rgb)
                if c == '727783': set_line(s, 'FFFFFF', 2.5)           # centre outline on the blue-violet disc
                elif c == 'CDA16B': set_line(s, 'A9ACD3', 1.5)
                else: set_line(s, RING_LINE, 1.0)
        elif s.shape_type == 1 and s.line.fill.type == 1 and str(s.line.color.rgb) == '686B75':
            if s.line.width.pt >= 1.9: set_line(s, LINE_THICK, 2.25)
            else: set_line(s, LINE_THIN, 1.0)

    # 2) semantic sector tints and the blue-violet centre, at the bottom of the group
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

    # 3) wording and colours of the labels
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
    for s in list(g.shapes):
        if s.shape_type != 17: continue
        t = s.text_frame.text
        if t in wedge:
            lines, key = wedge[t]; set_lines(s, lines, HUE[key][0])
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

    # 4) tags: names in ink, years in a warm grey
    for s in walk(g.shapes):
        if s.shape_type == 17 and s.text_frame.text.strip() and s.shape_id not in by_id:
            col = YEAR if s.text_frame.text.strip().isdigit() else INK
            for p in s.text_frame.paragraphs:
                for r in p.runs: r.font.color.rgb = rgb(col)

    g._element.grpSpPr.remove(g._element.grpSpPr.find(qn('a:xfrm')))
    g._element.grpSpPr.insert(0, xfrm)

    # 5) clay icons for the 13 wedges (top-level pictures), ordered left to right around the fan
    names = ['chat', 'memory', 'tools', 'planning', 'runtime', 'calendar', 'window', 'timeline', 'cutoff',
             'forecast', 'synthesis', 'anomaly', 'decision']
    pics = [s for s in slide.shapes if s.shape_type == 13]
    v = lambda tag, att: int(xfrm.find(qn(tag)).get(att))
    kx, ky = v('a:ext', 'cx') / v('a:chExt', 'cx'), v('a:ext', 'cy') / v('a:chExt', 'cy')   # the group scales x and y differently
    cxs = v('a:off', 'x') + (CX * E - v('a:chOff', 'x')) * kx                 # fan centre in slide EMU
    cys = v('a:off', 'y') + (CY * E - v('a:chOff', 'y')) * ky
    pics.sort(key=lambda p: -math.atan2(cys - (p.top + p.height / 2), (p.left + p.width / 2) - cxs))
    for p, nm in zip(pics, names):
        c = (p.left + p.width / 2, p.top + p.height / 2); size = Inches(0.86)
        path = os.path.join(ICON_DIR + '_print', nm + '.png')
        slide.shapes.add_picture(path, int(c[0] - size / 2), int(c[1] - size / 2), size, size)
        p._element.getparent().remove(p._element)
    prs.save(OUT)
    print('saved', OUT, 'sectors at', round(a_tsk, 1), round(a_gts, 1))


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
