from pathlib import Path
from lxml import etree as E
import zipfile,json,re,shutil
D=Path(__file__).resolve().parent;R=D.parents[1]
N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def add(p,tag,**kw):return E.SubElement(p,'{'+N[tag.split(':')[0]]+'}'+tag.split(':')[1],**{k:str(v) for k,v in kw.items()})
def gradient(p,light='F8FAFB',dark='DCE5EB',angle=5400000):
 for c in list(p):
  if E.QName(c).localname in ['solidFill','gradFill','noFill']:p.remove(c)
 g=E.Element('{'+N['a']+'}gradFill',rotWithShape='1');ls=add(g,'a:gsLst')
 for pos,col in [(0,light),(100000,dark)]:add(add(ls,'a:gs',pos=pos),'a:srgbClr',val=col)
 add(g,'a:lin',ang=angle,scaled=1);p.insert(0,g)
def shadow(p):
 for c in p.findall('a:effectLst',N):p.remove(c)
 sh=add(add(p,'a:effectLst'),'a:outerShdw',blurRad=18000,dist=11000,dir=5400000,algn='ctr',rotWithShape=0)
 add(add(sh,'a:srgbClr',val='333333'),'a:alpha',val=11000)
def mapcolor(v,fill=False):
 if len(v)!=6:return v
 a,b,c=[int(v[i:i+2],16) for i in (0,2,4)]
 if min(a,b,c)>248:return 'FFFFFF'
 if max(a,b,c)<45:return '000000'
 if min(a,b,c)>175:return 'F1F1EE' if fill else 'D8D8D4'
 if a>b*1.18 and a>c*1.18:return 'A65F48'
 if c>a*1.12 or b>a*1.12:return '304B63'
 return '767670'
heads={
5:{'Representation & alignment','Instruction & reasoning','Workflow learning','LLM'},
6:{'Planning & Orchestration','Interface & Interaction','Tools & Execution','Memory & Context','LLM','Optimization & Evolution'},
8:{'Task-Specific Time-Series Harness','Forecasting and prediction','Data augmentation and synthesis','Anomaly detection and diagnosis','Decision Support'},
10:{'1  Acquire','2  Construct','3  Detect','4  Refine','Detector training'},
11:{'Contract','Resources','Execution','Artifact','Task performance','Artifact validity','Execution record'},
12:{'Task requirements','Challenge package','Task description','Workspace','Challenge grader','Validity','Task score'},
13:{'1. Question and series','2. Numerical tools','3. Evidence review','4. Grounded answer','Provenance of the answer'},
14:{'Numerical workspace','Temporal tools','Multimodal memory','From execution to reusable tools','Execution traces','Candidate tool','Held-out tests','Registration'},
15:{'Open question','Controlled comparison','Evidence to record','Perception or execution','Memory under change','Procedure transfer','Evidence sensitivity','Prediction to decision'}}
effects={8:{21,26,67,69,126,129,178,179,182},10:{16,17,18},11:{2,3,4,5},12:{20,29,30,31},15:{10538,10542}}
regions={8:{14,15,64,119,120,171},10:{2,28,38,59},13:set(range(2,10)),14:{15}}
report={}
for num in [1,3,*range(4,16)]:
 if num in [4,7,9]:
  src=R/f'artifacts/editorial_style_trial_v2_20261022/pptx/Figure{num:02}_Editorial_v2.pptx'
  shutil.copyfile(src,D/'.build'/f'Figure{num:02}_Editorial.pptx');report[num]={'source':str(src.relative_to(R)),'action':'approved v2 preserved'};continue
 src=R/(f'artifacts/signal_revision_20261022/pptx/Figure{num:02}_Signal_grouped.pptx' if num>3 else 'artifacts/active/Figure3_construction_rsi_adapted_grouped.pptx')
 with zipfile.ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
 sn=(2 if num==1 else 3) if num<4 else 1
 # Keep one referenced slide and remove other slide parts and their relationships.
 if num<4:
  pres=E.fromstring(data['ppt/presentation.xml']);lst=pres.find('p:sldIdLst',N);ids=list(lst)
  rel=E.fromstring(data['ppt/_rels/presentation.xml.rels'])
  rid=next(x.get('Id') for x in rel if x.get('Target','').endswith(f'slides/slide{sn}.xml'))
  for x in list(lst):lst.remove(x)
  add(lst,'p:sldId',id=256).set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id',rid)
  for x in list(rel):
   if x.get('Type','').endswith('/slide') and x.get('Id')!=rid:rel.remove(x)
  data['ppt/presentation.xml']=E.tostring(pres);data['ppt/_rels/presentation.xml.rels']=E.tostring(rel)
  for k in list(data):
   m=re.match(r'ppt/(?:slides/(?:_rels/)?slide|notesSlides/(?:_rels/)?notesSlide)(\d+)\.xml(?:\.rels)?$',k)
   if m and int(m[1])!=sn:del data[k]
  ct=E.fromstring(data['[Content_Types].xml'])
  for x in list(ct):
   if x.get('PartName','').startswith(('/ppt/slides/slide','/ppt/notesSlides/notesSlide')) and x.get('PartName')[1:] not in data:ct.remove(x)
  data['[Content_Types].xml']=E.tostring(ct)
 name=f'ppt/slides/slide{sn}.xml';t=E.fromstring(data[name]);beforetexts=t.xpath('//a:t/text()',namespaces=N)
 changed=[]
 for s in t.xpath('//p:sp|//p:cxnSp|//p:pic',namespaces=N):
  n=s.find('.//p:cNvPr',N);sid=int(n.get('id'));sp=s.find('p:spPr',N);txt=' '.join(s.xpath('.//a:t/text()',namespaces=N))
  if sp is not None:
   for ef in sp.findall('a:effectLst',N):sp.remove(ef)
   for c in sp.xpath('./a:ln/a:solidFill/a:srgbClr',namespaces=N):c.set('val',mapcolor(c.get('val')))
   for c in sp.xpath('./a:solidFill/a:srgbClr',namespaces=N):c.set('val',mapcolor(c.get('val'),True))
   for ln in sp.findall('a:ln',N):
    if ln.find('a:gradFill',N) is not None:
     gradient(ln,'A5AAA9','555D61',0);ln.set('w','19000')
   for g in sp.findall('a:gradFill',N):
    vals=g.xpath('.//a:srgbClr/@val',namespaces=N)
    if vals and any(v=='000000' for v in vals):
     sp.remove(g);add(add(sp,'a:solidFill'),'a:srgbClr',val='000000')
   if sid in effects.get(num,set()):gradient(sp,'FFFFFF','EEF2F4');shadow(sp);changed.append(sid)
   if sid in regions.get(num,set()):gradient(sp);changed.append(sid)
  for pr in s.xpath('.//a:rPr|.//a:defRPr|.//a:endParaRPr',namespaces=N):
   heading=txt in heads.get(num,set()) or (num==1 and txt.startswith('§')) or (num==3 and txt in {'LLM side','General Harness','General Time-Series Harness','Task-Specific Harness','Evaluation and evidence','Time-Series Agent'})
   lat=pr.find('a:latin',N)
   if lat is None:lat=add(pr,'a:latin',typeface='Arial')
   lat.set('typeface','Comic Sans MS' if heading else 'Arial')
   for c in pr.xpath('./a:solidFill/a:srgbClr',namespaces=N):
    if c.get('val')!='FFFFFF':c.set('val','222222')
  blip=s.find('.//a:blip',N)
  if blip is not None and num!=14:
   for ef in list(blip):
    if E.QName(ef).localname in ['duotone','grayscl','lum']:blip.remove(ef)
   warm=any(x in n.get('name','').lower() for x in ['fail','reject','review'])
   du=add(blip,'a:duotone');add(du,'a:srgbClr',val='6B3020' if warm else '10283B');add(du,'a:srgbClr',val='FFFFFF')
 # Normalize native table text without changing mathematics or values.
 for pr in t.xpath('//a:tbl//a:rPr',namespaces=N):
  lat=pr.find('a:latin',N)
  if lat is not None:lat.set('typeface','Arial')
 for c in t.xpath('//a:tbl//a:tcPr//a:srgbClr',namespaces=N):
  if c.get('val')!='FFFFFF':c.set('val','D8D8D4')
 if num==3:
  for tx in t.xpath('//a:t',namespaces=N):
   if tx.text=='tools · memory · control · planning · coordination':tx.text='interaction · tools · memory · planning · evolution'
   if tx.text=='module-level counts':tx.text='module-level evidence'
 order={'xfrm':0,'prstGeom':1,'custGeom':1,'noFill':2,'solidFill':2,'gradFill':2,'ln':3,'effectLst':4}
 for sp in t.xpath('//p:spPr',namespaces=N):sp[:]=sorted(sp,key=lambda c:order.get(E.QName(c).localname,8))
 data[name]=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
 with zipfile.ZipFile(D/'.build'/f'Figure{num:02}_Editorial.pptx','w',zipfile.ZIP_DEFLATED) as z:
  for k,b in data.items():z.writestr(k,b)
 report[num]={'source':str(src.relative_to(R)),'source_slide':sn,'groups':len(t.xpath('//p:grpSp',namespaces=N)),'native_tables':len(t.xpath('//a:tbl',namespaces=N)),'selected_depth_shapes':changed,'text_unchanged':beforetexts==t.xpath('//a:t/text()',namespaces=N)}
(D/'manifest.json').write_text(json.dumps(report,indent=2))
