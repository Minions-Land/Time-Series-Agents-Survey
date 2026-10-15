from pathlib import Path
import zipfile,copy,json
from lxml import etree as E
R=Path(__file__).resolve().parents[1]
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
P=NS['p'];A=NS['a']
def group(children,name,uid):
 g=E.Element('{%s}grpSp'%P);nv=E.SubElement(g,'{%s}nvGrpSpPr'%P)
 E.SubElement(nv,'{%s}cNvPr'%P,id=str(uid),name=name);E.SubElement(nv,'{%s}cNvGrpSpPr'%P);E.SubElement(nv,'{%s}nvPr'%P)
 gp=E.SubElement(g,'{%s}grpSpPr'%P);xf=E.SubElement(gp,'{%s}xfrm'%A)
 # Tight group bounds, with identity child mapping.
 boxes=[]
 for child in children:
  q=child.find('.//a:xfrm',NS)
  if q is not None:
   a=q.find('a:off',NS);b=q.find('a:ext',NS)
   if a is not None and b is not None:boxes.append((int(a.get('x')),int(a.get('y')),int(b.get('cx')),int(b.get('cy'))))
 left=min(b[0] for b in boxes);top=min(b[1] for b in boxes)
 width=max(b[0]+b[2] for b in boxes)-left;height=max(b[1]+b[3] for b in boxes)-top
 for tag,attrs in [('off',{'x':str(left),'y':str(top)}),('ext',{'cx':str(max(1,width)),'cy':str(max(1,height))}),('chOff',{'x':str(left),'y':str(top)}),('chExt',{'cx':str(max(1,width)),'cy':str(max(1,height))})]:E.SubElement(xf,'{%s}%s'%(A,tag),**attrs)
 for c in children:g.append(c)
 return g
reports=[]
for src,name in [(Path('/Users/mjm/Desktop/Survey Figures/Time_Series_Agents_final_v4_editable.pptx'),'01_TimeSeries_Overview'),(Path('/Users/mjm/Desktop/Survey Figures/Research_Landscape_of_Time_Series_Agent_Systems(1).pptx'),'02_TimeSeries_Research_Landscape')]:
 dest=R/'editable_ppt';dest.mkdir(exist_ok=True)
 with zipfile.ZipFile(src) as z:
  blobs={n:z.read(n) for n in z.namelist()}
 s=E.fromstring(blobs['ppt/presentation.xml']);sz=s.find('p:sldSz',NS);W=int(sz.get('cx'));H=int(sz.get('cy'))
 root=E.fromstring(blobs['ppt/slides/slide1.xml']);tree=root.find('p:cSld/p:spTree',NS)
 kids=[x for x in tree if E.QName(x).localname not in ['nvGrpSpPr','grpSpPr','extLst']]
 before={'text':root.xpath('//a:t/text()',namespaces=NS),'shapes':len(root.findall('.//p:sp',NS)),'pictures':len(root.findall('.//p:pic',NS))}
 def region(c):
  xf=c.find('.//a:xfrm',NS)
  if xf is None:return 'Background'
  off=xf.find('a:off',NS);ex=xf.find('a:ext',NS)
  x=(int(off.get('x'))+int(ex.get('cx'))/2)/W;y=(int(off.get('y'))+int(ex.get('cy'))/2)/H
  w=int(ex.get('cx'))/W;h=int(ex.get('cy'))/H
  if w>.7 or h>.8:return 'Frame and headings'
  if name.startswith('01'):
   if x<.17:return 'Scenario and task'
   if x>.82:return 'Evaluation'
   if x<.34:return 'LLM side'
   if y<.36:return 'General Harness'
   if y<.69:return 'Temporal Harness'
   return 'Task specific Harness'
  if y<.28:return 'LLM contributions'
  if y>.83:return 'Benchmarks and infrastructure'
  return 'Harness dimension '+str(min(7,max(1,int((x-.015)/.139)+1)))
 runs=[]
 for c in kids:
  label=region(c)
  if runs and runs[-1][0]==label:runs[-1][1].append(c)
  else:runs.append((label,[c]))
 uid=max(int(v) for v in root.xpath('//p:cNvPr/@id',namespaces=NS))+1
 outer=[]
 for label,cs in runs:
  for c in cs:tree.remove(c)
  if len(cs)>1:outer.append(group(cs,label,uid));uid+=1
  else:outer+=cs
 tree.append(group(outer,name+' — ungroup to edit',uid))
 assert root.xpath('//a:t/text()',namespaces=NS)==before['text']
 assert len(root.findall('.//p:sp',NS))==before['shapes']
 assert len(root.findall('.//p:pic',NS))==before['pictures']
 blobs['ppt/slides/slide1.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 target=dest/(name+'_grouped.pptx')
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
  for n,b in blobs.items():z.writestr(n,b)
 reports.append({'source':str(src),'output':str(target),'native_shapes':before['shapes'],'separate_pictures':before['pictures'],'groups':len(root.findall('.//p:grpSp',NS)),'all_text_and_objects_preserved':True,'powerpoint_gui_verified':False})
(R/'editability_audit.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
print(json.dumps(reports,indent=2))
