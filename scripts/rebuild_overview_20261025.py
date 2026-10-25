from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

ROOT = Path(__file__).resolve().parents[1]
SRC = Path('/Users/mjm/Desktop/Survey Figures/02_main.pptx')
OUT = ROOT/'artifacts/overview_revision_20261025/pptx/Time-Series-Agents_Overview_Reorganized.pptx'
ASSET = ROOT/'artifacts/overview_revision_20261025/assets'
OUT.parent.mkdir(parents=True, exist_ok=True)

prs = Presentation(str(SRC))
slide = prs.slides[0]
# Remove a possible prior legend when rerunning this script.
for shape in list(slide.shapes):
    if getattr(shape, 'name', '').startswith('Overview icon key'):
        sp = shape._element
        sp.getparent().remove(sp)

# Top strip: five compact cards, well above the radial landscape.
card_w, card_h = 4.45, 0.72
left = (prs.slide_width/914400 - (5*card_w + 4*0.12))/2
left = max(0.8, left)
top = 0.20
labels = [
    ('LLM', 'Model side', 'llm.png', '2C6EAA'),
    ('General', 'Harness', 'general.png', '6E5A9E'),
    ('Time-Series', 'Harness', 'general_ts.png', 'B07A2A'),
    ('Task-Specific', 'Harness', 'task.png', '3A8B73'),
    ('Evaluation', 'Evidence', 'evaluation.png', '5D718A'),
]
card_nodes = []
for i,(line1,line2,img,color) in enumerate(labels):
    x = left + i*(card_w+0.12)
    # A quiet paper-like card; native PowerPoint shape.
    bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(top), Inches(card_w), Inches(card_h))
    bg.name = f'Overview icon key card {i+1} background'
    bg.fill.solid(); bg.fill.fore_color.rgb = RGBColor(248,250,252)
    bg.line.color.rgb = RGBColor(211,220,230); bg.line.width = Pt(0.65)
    # Narrow accent bar ties the key to the ring colors without a loud palette.
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(top), Inches(0.055), Inches(card_h))
    stripe.name = f'Overview icon key card {i+1} accent'
    stripe.fill.solid(); stripe.fill.fore_color.rgb = RGBColor.from_string(color)
    stripe.line.fill.background()
    # Old overview icon, retained as a transparent bitmap component.
    pic = slide.shapes.add_picture(str(ASSET/img), Inches(x+0.16), Inches(top+0.12), height=Inches(0.48))
    pic.name = f'Overview icon key card {i+1} icon'
    # Two-line label kept as editable text.
    tx = slide.shapes.add_textbox(Inches(x+0.83), Inches(top+0.08), Inches(card_w-0.95), Inches(card_h-0.12))
    tx.name = f'Overview icon key card {i+1} label'
    tf = tx.text_frame; tf.clear(); tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r=p.add_run(); r.text=line1; r.font.name='Comic Sans MS'; r.font.size=Pt(10.0); r.font.bold=True; r.font.color.rgb=RGBColor(39,53,72)
    r2=p.add_run(); r2.text='\n'+line2; r2.font.name='Comic Sans MS'; r2.font.size=Pt(8.8); r2.font.bold=False; r2.font.color.rgb=RGBColor(92,106,123)
    card_nodes.append((i+1, [bg._element, stripe._element, pic._element, tx._element]))

prs.save(str(OUT))

# XML grouping and removal of out-of-frame duplicates.
P_NS='http://schemas.openxmlformats.org/presentationml/2006/main'
A_NS='http://schemas.openxmlformats.org/drawingml/2006/main'
NSMAP={'p':P_NS,'a':A_NS}
qn=lambda ns,tag: f'{{{ns}}}{tag}'

def cNvPr(el):
    return el.xpath('./p:nvSpPr/p:cNvPr|./p:nvPicPr/p:cNvPr|./p:nvGrpSpPr/p:cNvPr', namespaces=NSMAP)[0]

def name(el):
    try:return cNvPr(el).get('name','')
    except:return ''

def get_xfrm(el):
    xs=el.xpath('.//a:xfrm',namespaces=NSMAP)
    return xs[0] if xs else None

def bbox(elements):
    vals=[]
    for e in elements:
        x=get_xfrm(e)
        if x is None: continue
        off=x.find('a:off',NSMAP); ext=x.find('a:ext',NSMAP)
        if off is None or ext is None: continue
        vals.append((int(off.get('x')),int(off.get('y')),int(ext.get('cx')),int(ext.get('cy'))))
    if not vals: return (0,0,0,0)
    x=min(v[0] for v in vals); y=min(v[1] for v in vals)
    x2=max(v[0]+v[2] for v in vals); y2=max(v[1]+v[3] for v in vals)
    return x,y,x2-x,y2-y

def make_group(id_, group_name, children):
    x,y,cx,cy=bbox(children)
    grp=etree.Element(qn(P_NS,'grpSp'), nsmap={'a':A_NS,'p':P_NS})
    nv=etree.SubElement(grp,qn(P_NS,'nvGrpSpPr'))
    etree.SubElement(nv,qn(P_NS,'cNvPr'),id=str(id_),name=group_name)
    etree.SubElement(nv,qn(P_NS,'cNvGrpSpPr'))
    etree.SubElement(nv,qn(P_NS,'nvPr'))
    gpr=etree.SubElement(grp,qn(P_NS,'grpSpPr'))
    xf=etree.SubElement(gpr,qn(A_NS,'xfrm'))
    etree.SubElement(xf,qn(A_NS,'off'),x=str(x),y=str(y))
    etree.SubElement(xf,qn(A_NS,'ext'),cx=str(cx),cy=str(cy))
    etree.SubElement(xf,qn(A_NS,'chOff'),x=str(x),y=str(y))
    etree.SubElement(xf,qn(A_NS,'chExt'),cx=str(cx),cy=str(cy))
    for c in children: grp.append(c)
    return grp

# Repack the slide XML while preserving every pre-existing object.
with ZipFile(OUT,'r') as zin:
    files={n:zin.read(n) for n in zin.namelist()}
slide_path='ppt/slides/slide1.xml'
root=etree.fromstring(files[slide_path])
spTree=root.find('.//p:spTree',NSMAP)
# Remove duplicated WorldReasoner groups outside the slide. Keep the in-frame one.
for ch in list(spTree):
    if name(ch).startswith('WorldReasoner') or 'WorldReasoner' in ' | '.join(ch.xpath('.//a:t/text()',namespaces=NSMAP)):
        xf=get_xfrm(ch); off=xf.find('a:off',NSMAP) if xf is not None else None
        if off is not None and int(off.get('y','0')) < 0:
            spTree.remove(ch)
# Find new card components by unique names and group them.
max_id=0
for el in root.xpath('.//p:cNvPr',namespaces=NSMAP):
    try:max_id=max(max_id,int(el.get('id','0')))
    except: pass
card_groups=[]
for idx in range(1,6):
    members=[]
    for ch in list(spTree):
        nm=name(ch)
        if nm.startswith(f'Overview icon key card {idx} '):
            members.append(ch)
    if len(members)!=4:
        raise RuntimeError(f'card {idx}: expected 4 components, found {len(members)}')
    # preserve original order in the group (background, accent, icon, label)
    first_index=min(list(spTree).index(m) for m in members)
    for m in members: spTree.remove(m)
    max_id+=1
    g=make_group(max_id,f'Overview icon key card {idx}',members)
    spTree.insert(first_index,g); card_groups.append(g)
# Outer legend group.
first_index=min(list(spTree).index(g) for g in card_groups)
for g in card_groups: spTree.remove(g)
max_id+=1
outer=make_group(max_id,'Overview icon key (five layer cues)',card_groups)
spTree.insert(first_index,outer)
files[slide_path]=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
# Write a new zip atomically via a temporary sibling.
tmp=OUT.with_suffix('.tmp.pptx')
with ZipFile(tmp,'w') as zout:
    for n,data in files.items(): zout.writestr(n,data)
tmp.replace(OUT)
print(OUT)
