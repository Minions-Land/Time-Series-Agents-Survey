"""Shared content and native-shape helpers for the overview-flow figure variants."""
import copy, os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(ROOT, 'logos')          # institution logos taken from the Figure 2 PPTX
ICONS = {'pixel': os.path.join(ROOT, 'icons', 'pixel'), 'clay': os.path.join(ROOT, 'icons', 'clay')}

# Palette follows Figure 1 of the manuscript.
C = dict(llm='F0A030', gh='3B5BA5', gts='2A9D8F', tsk='E05A47', ev='5B5F97',
         ink='1F2A44', mute='6B7280', cream='FBF3E4', white='FFFFFF', navy='16213E')

STAGES = [
    dict(key='llm', sec='§3', name='LLM Side', short='LLM',
         role='interprets temporal evidence and selects actions', icon='llm',
         items=['Representation alignment', 'Temporal instruction & reasoning', 'Workflow policy learning'],
         works=[('ChatTS', 'image17.png'), ('Time-LLM', None), ('TimeRLM', 'image19.png')]),
    dict(key='gh', sec='§4', name='General Harness', short='GH',
         role='executes actions, keeps state, coordinates roles', icon='runtime',
         items=['Interface & Interaction', 'Memory & Context', 'Tools & Execution', 'Planning & Orchestration', 'Optimization & Evolution'],
         works=[('TimeClaw-Harness', 'image10.png'), ('AION', 'image2.png'), ('TS-Agent', 'image1.png'), ('TradingAgents', 'image3.png')]),
    dict(key='gts', sec='§5', name='General Time Series Harness', short='GTS',
         role='supplies temporal data, tools and time constraints', icon='timeline',
         items=['Temporal Data Management', 'Temporal Processing', 'Temporal Context & Memory', 'Temporal Validation'],
         works=[('TimeSage-EV', 'image29.png'), ('OpenForecaster', 'image30.png'), ('TSQAgent', 'image13.png'), ('TS-Reasoner', 'image26.png')]),
    dict(key='tsk', sec='§6', name='Task-Specific Harness', short='TSK',
         role='organizes outputs around task objectives', icon='forecast',
         items=['Forecasting & Prediction', 'Data Augmentation & Synthesis', 'Anomaly Detection & Diagnosis', 'Decision Support'],
         works=[('FLAIRR-TS', 'image6.png'), ('MetaCaster', 'image5.png'), ('Argos', 'image12.png'), ('FinCon', 'image7.png')]),
    dict(key='ev', sec='§7', name='Validation & Evaluation', short='EVAL',
         role='checks process, temporal validity, task and decision utility', icon='validate',
         items=['Execution checks', 'Information-cutoff checks', 'Task metrics', 'Downstream utility'],
         works=[('TimeSeriesGym', 'image25.png'), ('Dr-CiK', 'image39.png'), ('TraceBench', 'image19.png'), ('TSFLab', None)]),
]
S = {s['key']: s for s in STAGES}
INPUT = dict(name='Time series & context', sub='observations · events · task request', icon='timeseries')
OUTPUT = dict(name='Forecast · diagnosis · decision', sub='accepted output', icon='decision')
FLOW = dict(act='action', obs='observation', ops='temporal operations', cap='shared temporal capabilities',
            cand='candidate output', fb='feedback: revise', stop='accept / terminate', axis='scope of reuse: general → specific')
TITLE = 'Time Series Agent: Components and Information Flow'


def rgb(h):
    return RGBColor.from_string(h)


def new_pres(w=13.333, h=6.4):
    p = Presentation()
    p.slide_width, p.slide_height = Inches(w), Inches(h)
    return p, p.slides.add_slide(p.slide_layouts[6])


def box(shapes, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=None, dash=None, shadow=False):
    s = shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = rgb(line); s.line.width = Pt(lw)
        if dash: s.line.dash_style = dash
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if not shadow:
        sp = s._element.spPr
        ef = etree.SubElement(sp, qn('a:effectLst'))
    s.text_frame.text = ''
    return s


def text(shapes, x, y, w, h, t, size=10, bold=False, color='1F2A44', font='Avenir Next', align='c', anchor='m', italic=False, wrap=True):
    tb = shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = Inches(0.02); tf.margin_top = tf.margin_bottom = Inches(0.0)
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        r = para.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = font; f.color.rgb = rgb(color)
    return tb


def label_in(shape, t, size=10, bold=True, color='FFFFFF', font='Avenir Next', align='c'):
    tf = shape.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04); tf.margin_top = tf.margin_bottom = Inches(0.01)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER}[align]
        r = para.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.name = font; f.color.rgb = rgb(color)
    return shape


def pic(shapes, path, x, y, w=None, h=None):
    kw = {}
    if w: kw['width'] = Inches(w)
    if h: kw['height'] = Inches(h)
    return shapes.add_picture(path, Inches(x), Inches(y), **kw)


def icon(shapes, style, name, x, y, size):
    path = os.path.join(ICONS[style], name + '.png')
    if not os.path.exists(path):
        return box(shapes, x, y, size, size, fill='DDDDDD', shape=MSO_SHAPE.OVAL)
    return pic(shapes, path, x, y, w=size, h=size)


def logo(shapes, fname, x, y, size):
    if not fname:
        return None
    stem = os.path.splitext(fname)[0]
    path = next(os.path.join(MEDIA, f) for f in os.listdir(MEDIA) if os.path.splitext(f)[0] == stem)
    return pic(shapes, path, x, y, w=size, h=size)


def arrow(shapes, x1, y1, x2, y2, color='1F2A44', lw=1.75, dash=None, head='triangle', tail=None, curve=False):
    kind = MSO_CONNECTOR.CURVE if curve else MSO_CONNECTOR.STRAIGHT
    c = shapes.add_connector(kind, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
    if dash: c.line.dash_style = dash
    ln = c.line._get_or_add_ln()
    if tail:
        e = etree.SubElement(ln, qn('a:headEnd')); e.set('type', tail); e.set('w', 'med'); e.set('len', 'med')
    if head:
        e = etree.SubElement(ln, qn('a:tailEnd')); e.set('type', head); e.set('w', 'med'); e.set('len', 'med')
    return c


SKETCH = ('<a:extLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:ext uri="{C807C97D-BFC1-408E-A445-0C87EB9F89A2}">'
          '<ask:lineSketchStyleProps xmlns:ask="http://schemas.microsoft.com/office/drawing/2018/sketchyshapes" sd="1219033472">'
          '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><ask:type><ask:lineSketchFreehand/></ask:type>'
          '</ask:lineSketchStyleProps></a:ext></a:extLst>')


def sketchy(shape):
    """Office 365 hand-drawn outline; renders natively in PowerPoint."""
    ln = shape._element.spPr.find(qn('a:ln'))
    if ln is None:
        return shape
    ln.append(etree.fromstring(SKETCH))
    return shape


def group(slide):
    return slide.shapes.add_group_shape()
