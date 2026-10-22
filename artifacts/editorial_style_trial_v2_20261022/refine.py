from pathlib import Path
from lxml import etree as E
import zipfile,json
D=Path(__file__).resolve().parent;R=D.parents[1]
N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def add(p,tag,**kw):return E.SubElement(p,'{'+N[tag.split(':')[0]]+'}'+tag.split(':')[1],**{k:str(v) for k,v in kw.items()})
def gradient(p,light,dark,angle=5400000):
 for c in list(p):
  if E.QName(c).localname in ['solidFill','gradFill','noFill']:p.remove(c)
 g=E.Element('{'+N['a']+'}gradFill',rotWithShape='1');ls=add(g,'a:gsLst')
 for pos,col in [(0,light),(100000,dark)]:add(add(ls,'a:gs',pos=pos),'a:srgbClr',val=col)
 add(g,'a:lin',ang=angle,scaled=1);p.insert(0,g)
def shadow(p,alpha=13000):
 for c in p.findall('a:effectLst',N):p.remove(c)
 sh=add(add(p,'a:effectLst'),'a:outerShdw',blurRad=18000,dist=11000,dir=5400000,algn='ctr',rotWithShape=0)
 add(add(sh,'a:srgbClr',val='333333'),'a:alpha',val=alpha)
headings={4:{'Forecasting','Synthesis','Diagnosis','Decision','Execute','Prepare','Forecast','Decide'},7:{'Information release','Data management','Temporal processing','Context and memory','Temporal validation','LLM'},9:{'Retrieval','Augmentation','Review','Representation','Positive memory','Shared encoder'}}
report={}
for num in [4,7,9]:
 src=R/f'artifacts/editorial_style_trial_20261022/pptx/Figure{num:02}_Editorial_trial.pptx'
 with zipfile.ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
 t=E.fromstring(data['ppt/slides/slide1.xml']);fonted=[];effected=[]
 for s in t.xpath('//p:sp|//p:cxnSp',namespaces=N):
  n=s.find('.//p:cNvPr',N);sid=int(n.get('id'));name=n.get('name','');sp=s.find('p:spPr',N);txt=' '.join(s.xpath('.//a:t/text()',namespaces=N))
  if txt in headings[num]:
   for pr in s.xpath('.//a:rPr|.//a:defRPr|.//a:endParaRPr',namespaces=N):
    lat=pr.find('a:latin',N)
    if lat is None:lat=add(pr,'a:latin',typeface='Comic Sans MS')
    lat.set('typeface','Comic Sans MS')
    if pr.get('sz'):pr.set('sz',str(round(int(pr.get('sz'))*.96)))
   fonted.append(txt)
  if sp is None:continue
  if (num==4 and sid in [28,36]) or (num==7 and sid in [17,83]):gradient(sp,'F8FAFB','DCE5EB');effected.append(name+' cool region')
  if num==4 and sid==78:gradient(sp,'FBF8F5','EBDDD6');effected.append(name+' warm region')
  if num==7 and sid==16:gradient(sp,'F8FAFB','E0E8ED');shadow(sp,11000);effected.append(name+' calendar')
  if num==9 and name=='learn-encoder':gradient(sp,'F4F7F9','D8E2E9');shadow(sp,15000);effected.append(name)
  if num==9 and name in ['retrieve-bar0','retrieve-bar1','retrieve-bar2']:
   gradient(sp,'94A5B0','304B63');shadow(sp,11000);effected.append(name)
  if (num==7 and sid==110) or (num==4 and sid==67):
   ln=sp.find('a:ln',N)
   if ln is not None:gradient(ln,'A5AAA9','555D61',0);ln.set('w','22000');shadow(sp,9000);effected.append(name+' axis')
 order={'xfrm':0,'prstGeom':1,'custGeom':1,'noFill':2,'solidFill':2,'gradFill':2,'ln':3,'effectLst':4}
 for prop in t.xpath('//p:spPr',namespaces=N):prop[:]=sorted(prop,key=lambda c:order.get(E.QName(c).localname,8))
 data['ppt/slides/slide1.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
 with zipfile.ZipFile(D/'.build'/f'Figure{num:02}_Editorial_v2.pptx','w',zipfile.ZIP_DEFLATED) as z:
  for n,b in data.items():z.writestr(n,b)
 report[num]={'source':str(src.relative_to(R)),'comic_headings':fonted,'selective_effects':effected,'groups':len(t.xpath('//p:grpSp',namespaces=N))}
(D/'changes.json').write_text(json.dumps(report,indent=2))
