"""Preserve native editable shapes, group by semantic module, and round line joins."""
from pathlib import Path
from lxml import etree as E
from collections import OrderedDict
import zipfile,sys,json
D=Path(__file__).resolve().parent
N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def q(s):p,t=s.split(':');return '{'+N[p]+'}'+t
def sub(e,t,**attrs):return E.SubElement(e,q(t),**{k:str(v) for k,v in attrs.items()})
reports={}
for n in sys.argv[1:] or ['04','09','13','14']:
 with zipfile.ZipFile(D/'.build'/f'Figure{n}_draft.pptx') as z:data={k:z.read(k) for k in z.namelist()}
 root=E.fromstring(data['ppt/slides/slide1.xml']);st=root.find('p:cSld/p:spTree',N)
 pres=E.fromstring(data['ppt/presentation.xml']);size=pres.find('p:sldSz',N);cx,cy=int(size.get('cx')),int(size.get('cy'))
 count=max(int(i) for i in root.xpath('//p:cNvPr/@id',namespaces=N))+1
 def new_group(name):
  global count
  g=E.Element(q('p:grpSp'));nv=sub(g,'p:nvGrpSpPr');sub(nv,'p:cNvPr',id=count,name=name);count+=1;sub(nv,'p:cNvGrpSpPr');sub(nv,'p:nvPr')
  xf=sub(sub(g,'p:grpSpPr'),'a:xfrm');sub(xf,'a:off',x=0,y=0);sub(xf,'a:ext',cx=cx,cy=cy);sub(xf,'a:chOff',x=0,y=0);sub(xf,'a:chExt',cx=cx,cy=cy)
  return g
 groups={};outer=new_group('Figure '+n+' - ungroup to edit modules')
 for s in list(st):
  if E.QName(s).localname in ['nvGrpSpPr','grpSpPr','extLst']:continue
  name=s.find('.//p:cNvPr',N).get('name','')
  tree=name.split('//')[0].split('/');par=outer;prefix=''
  for token in tree:
   prefix=prefix+'/'+token
   if prefix not in groups:groups[prefix]=new_group(token);par.append(groups[prefix])
   par=groups[prefix]
  st.remove(s);par.append(s)
  for lock in s.xpath('.//a:spLocks',namespaces=N):lock.attrib.pop('noGrp',None)
  for ln in s.xpath('./p:spPr/a:ln',namespaces=N):
   ln.set('cap','rnd')
   if ln.find('a:round',N) is None:sub(ln,'a:round')
 def bounds(g):
  boxes=[]
  for child in g:
   if E.QName(child).localname=='grpSp':boxes.append(bounds(child));continue
   xf=child.find('p:spPr/a:xfrm',N)
   if xf is not None:
    o=xf.find('a:off',N);e=xf.find('a:ext',N);x,y=int(o.get('x')),int(o.get('y'));boxes.append((x,y,x+int(e.get('cx')),y+int(e.get('cy'))))
  x=min(b[0] for b in boxes);y=min(b[1] for b in boxes);x2=max(b[2] for b in boxes);y2=max(b[3] for b in boxes)
  xf=g.find('p:grpSpPr/a:xfrm',N)
  for k in ['a:off','a:chOff']:xf.find(k,N).set('x',str(x));xf.find(k,N).set('y',str(y))
  for k in ['a:ext','a:chExt']:xf.find(k,N).set('cx',str(max(1,x2-x)));xf.find(k,N).set('cy',str(max(1,y2-y)))
  return x,y,x2,y2
 bounds(outer);st.append(outer)
 data['ppt/slides/slide1.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 out=D/'.build'/f'Figure{n}_grouped.pptx'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for k,v in data.items():z.writestr(k,v)
 reports[n]={'native_shapes':len(root.xpath('//p:sp',namespaces=N)),'groups':len(groups)+1,'images':len(root.xpath('//p:pic',namespaces=N)),'slide_size':[cx,cy]}
(D/'.build/group_report.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports))
