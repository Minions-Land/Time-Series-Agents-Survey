from pathlib import Path
from lxml import etree as E
import zipfile,json,copy,re
R=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def el(tag,**kw):return E.Element('{'+NS[tag.split(':')[0]]+'}'+tag.split(':')[1],**{k:str(v) for k,v in kw.items()})
def add(parent,tag,**kw):e=el(tag,**kw);parent.append(e);return e
sources={'4':'compact_revision_20261022/pptx/Figure04_Compact_grouped.pptx'}
ids={4:{*range(12,19),29,31,32,34,35,37,48,55,73,74,75,92,93,94,99,101,102,103}}
axes={4:{67}}
dash={4:{35,74}}
report={}
def effect(sp):
 for c in sp.findall('a:effectLst',NS):sp.remove(c)
 eff=add(sp,'a:effectLst');sh=add(eff,'a:outerShdw',blurRad=12700,dist=9000,dir=2700000,algn='ctr',rotWithShape=0);c=add(sh,'a:srgbClr',val='000000');add(c,'a:alpha',val=22000)
def solid(parent,color):
 for c in list(parent):
  if E.QName(c).localname in ['solidFill','gradFill','noFill','pattFill']:parent.remove(c)
 f=el('a:solidFill');add(f,'a:srgbClr',val=color);parent.insert(0,f)
def gradient(parent,colors):
 for c in list(parent):
  if E.QName(c).localname in ['solidFill','gradFill','noFill']:parent.remove(c)
 g=el('a:gradFill',rotWithShape='1');ls=add(g,'a:gsLst')
 for pos,col in colors:gs=add(ls,'a:gs',pos=pos);add(gs,'a:srgbClr',val=col)
 add(g,'a:lin',ang=0,scaled=1);parent.insert(0,g)
for istr,src in sources.items():
 i=int(istr);z=zipfile.ZipFile(R/'artifacts'/src);data={n:z.read(n) for n in z.namelist()};t=E.fromstring(data['ppt/slides/slide1.xml']);changed=[];fonts=[]
 for s in t.xpath('//p:sp|//p:cxnSp|//p:pic',namespaces=NS):
  n=s.find('.//p:cNvPr',NS);sid=int(n.get('id'));sp=s.find('p:spPr',NS);txt=' '.join(s.xpath('.//a:t/text()',namespaces=NS))
  if sid in ids[i]:
   ln=sp.find('a:ln',NS)
   if ln is not None:
    solid(ln,'000000');ln.set('cap','rnd')
    if sid in dash.get(i,set()):
     for c in ln.findall('a:prstDash',NS):ln.remove(c)
     add(ln,'a:prstDash',val='dash')
    effect(sp);changed.append(sid)
   if i==11 and 9<=sid<=17:solid(sp,'000000')
   if s.find('p:spPr/a:prstGeom',NS) is not None and s.find('p:spPr/a:prstGeom',NS).get('prst')=='ellipse':
    gradient(sp,[(0,'B0B0B0'),(35000,'333333'),(100000,'000000')])
  if sid in axes[i]:
   ln=sp.find('a:ln',NS)
   if ln is not None:
    ln.set('w',str(max(int(ln.get('w','12000'))*2,22000)));gradient(ln,[(0,'B4BAC0'),(45000,'747C83'),(100000,'343B41')]);effect(sp)
    if i==4:
     end=ln.find('a:tailEnd',NS)
     if end is None:end=add(ln,'a:tailEnd',type='triangle')
     end.set('w','med');end.set('len','med')
  # Short descriptive sentences remain in the source font; headings and labels change.
  name=n.get('name','').lower()
  explanatory=(len(txt.split())>5 or any(k in name for k in ['purpose','desc','learning signal','footer']) or (i==6 and sid in {10115,10120,10124,10130,10156}) or (i==12 and sid in {19,24,26,28,47,61,62,63,73,74}) or (i==14 and sid in {55,57,63,64,67}) or (i==15 and sid in {10512,10537,10548,10559,10583,10596}) or (i==8 and 'Evaluation' in txt))
  if txt and not explanatory:
   for pr in s.xpath('.//a:rPr|.//a:defRPr|.//a:endParaRPr',namespaces=NS):
    lat=pr.find('a:latin',NS)
    if lat is None:lat=add(pr,'a:latin',typeface='Comic Sans MS')
    lat.set('typeface','Comic Sans MS')
    if pr.get('sz'):pr.set('sz',str(round(int(pr.get('sz'))*(.78 if i==11 and sid in {65,66} else .88))))
   fonts.append(txt)
  # Original raster analytical glyphs: retain source pixels and apply grayscale in PPT.
  if (i==10 and n.get('name') in ['pattern0','pattern1','pattern2','false-alert']) or (i==12 and n.get('name')=='artifact'):
   blip=s.find('.//a:blip',NS);add(blip,'a:grayscl');effect(sp)
 
 for prop in t.xpath('//p:spPr',namespaces=NS):
  order={'xfrm':0,'prstGeom':1,'custGeom':1,'noFill':2,'solidFill':2,'gradFill':2,'blipFill':2,'pattFill':2,'ln':3,'effectLst':4,'scene3d':5,'sp3d':6,'extLst':7}
  prop[:]=sorted(prop,key=lambda c:order.get(E.QName(c).localname,8))
 # Every matrix cell is a short label; keep the native table editable.
 for pr in t.xpath('//a:tbl//a:rPr|//a:tbl//a:defRPr|//a:tbl//a:endParaRPr',namespaces=NS):
  lat=pr.find('a:latin',NS)
  if lat is None:lat=add(pr,'a:latin',typeface='Comic Sans MS')
  lat.set('typeface','Comic Sans MS')
  if pr.get('sz'):pr.set('sz',str(round(int(pr.get('sz'))*.88)))
 data['ppt/slides/slide1.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
 dest=D/'.build'/f'Figure{i:02}_Signal_grouped.pptx'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as f:
  for n,b in data.items():f.writestr(n,b)
 report[i]={'source':src,'native_signal_shapes':changed,'time_axes':sorted(axes[i]),'comic_labels':fonts,'groups':len(t.xpath('//p:grpSp',namespaces=NS))}
(D/'changes04.json').write_text(json.dumps(report,indent=2))
