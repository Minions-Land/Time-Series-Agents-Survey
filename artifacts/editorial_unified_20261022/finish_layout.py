from pathlib import Path
from lxml import etree as E
import zipfile
D=Path(__file__).resolve().parent
N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
for num in [1,3,11,12,13]:
 p=D/'.build'/f'Figure{num:02}_Editorial.pptx'
 with zipfile.ZipFile(p) as z:data={k:z.read(k) for k in z.namelist()}
 sn=2 if num==1 else 3 if num==3 else 1;key=f'ppt/slides/slide{sn}.xml';t=E.fromstring(data[key])
 for s in t.xpath('//p:sp',namespaces=N):
  sid=int(s.find('.//p:cNvPr',N).get('id'));txt=' '.join(s.xpath('.//a:t/text()',namespaces=N));factor=1
  if num==1:factor=.80 if txt.startswith('§') else .85
  if num==11 and sid in [78,85]:factor=.78
  if num==11 and sid in [83,90]:
   for x in s.xpath('.//a:latin',namespaces=N):x.set('typeface','Arial')
  if num==12 and sid in [19,24,26,28,47,48,49,61,62,63,73,74]:factor=.76
  if num==12 and sid==56:factor=.85
  for pr in s.xpath('.//a:rPr|.//a:defRPr|.//a:endParaRPr',namespaces=N):
   if pr.get('sz'):pr.set('sz',str(round(int(pr.get('sz'))*factor)))
  if num==3:
   # Existing layout contains captions within the graphic: remove those and compact the canvas.
   if sid in [33,2,31,32]:s.getparent().remove(s);continue
   if sid==25:
    ts=s.xpath('.//a:t',namespaces=N)
    for x in ts:
     if x.text=='counts':x.text='evidence'
   for c in s.xpath('./p:spPr/a:solidFill/a:srgbClr',namespaces=N):
    if sid in [4,11]:c.set('val','F7F8F9')
    if sid==14:c.set('val','E8EEF2')
    if sid==17:c.set('val','F4EAE5')
   x=s.find('p:spPr/a:xfrm/a:off',N)
   if x is not None:x.set('y',str(int(x.get('y'))-800000))
 if num==3:
  for s in t.xpath('//p:cxnSp',namespaces=N):
   x=s.find('p:spPr/a:xfrm/a:off',N)
   if x is not None:x.set('y',str(int(x.get('y'))-800000))
  pres=E.fromstring(data['ppt/presentation.xml']);pres.find('p:sldSz',N).set('cy','8050000');data['ppt/presentation.xml']=E.tostring(pres)
 if num==13:
  for c in t.xpath('//a:tbl//a:rPr/a:solidFill/a:srgbClr',namespaces=N):c.set('val','222222')
 data[key]=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
  for k,v in data.items():z.writestr(k,v)
# Reuse existing native icon components from the approved General Harness layout.
import copy
p=D/'.build/Figure03_Editorial.pptx'
with zipfile.ZipFile(p) as z:data={k:z.read(k) for k in z.namelist()}
t=E.fromstring(data['ppt/slides/slide3.xml'])
with zipfile.ZipFile(D/'pptx/Figure06_Editorial.pptx') as z:src=E.fromstring(z.read('ppt/slides/slide1.xml'))
ns=lambda key:'{'+N[key.split(':')[0]]+'}'+key.split(':')[1]
nextid=200000
specs=[('messages-square',4500000,1900000,220000),('wrench',5650000,1900000,220000),('database',6800000,1900000,220000),('workflow',7950000,1900000,220000),('refresh-cw',9100000,1900000,220000),('bot',1800000,3500000,330000)]
for prefix,x,y,h in specs:
 shapes=[copy.deepcopy(s) for s in src.xpath('//p:sp',namespaces=N) if s.find('.//p:cNvPr',N).get('name','').startswith(prefix+'-')]
 coords=[]
 for s in shapes:
  xf=s.find('p:spPr/a:xfrm',N);o=xf.find('a:off',N);e=xf.find('a:ext',N);coords.append(tuple(int(q) for q in [o.get('x'),o.get('y'),e.get('cx'),e.get('cy')]))
 xmin=min(c[0] for c in coords);ymin=min(c[1] for c in coords);w=max(c[0]+c[2] for c in coords)-xmin;oh=max(c[1]+c[3] for c in coords)-ymin
 g=E.Element(ns('p:grpSp'));nv=E.SubElement(g,ns('p:nvGrpSpPr'));E.SubElement(nv,ns('p:cNvPr'),id=str(nextid),name='reused-'+prefix);nextid+=1;E.SubElement(nv,ns('p:cNvGrpSpPr'));E.SubElement(nv,ns('p:nvPr'))
 xf=E.SubElement(E.SubElement(g,ns('p:grpSpPr')),ns('a:xfrm'))
 for tag,attrs in [('off',{'x':x,'y':y}),('ext',{'cx':round(w*h/oh),'cy':h}),('chOff',{'x':xmin,'y':ymin}),('chExt',{'cx':w,'cy':oh})]:E.SubElement(xf,ns('a:'+tag),**{k:str(v) for k,v in attrs.items()})
 for s in shapes:s.find('.//p:cNvPr',N).set('id',str(nextid));nextid+=1;g.append(s)
 t.find('p:cSld/p:spTree',N).append(g)
data['ppt/slides/slide3.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
 for k,v in data.items():z.writestr(k,v)
