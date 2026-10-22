from pathlib import Path
from lxml import etree as E
import zipfile,json
D=Path(__file__).resolve().parent;R=D.parents[1]
N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def add(p,tag,**kw):return E.SubElement(p,'{'+N[tag.split(':')[0]]+'}'+tag.split(':')[1],**{k:str(v) for k,v in kw.items()})
INK='222222';NAVY='304B63';RUST='A65F48';GRAY='767670';RULE='D8D8D4';FILL='F1F1EE'
report={}
for num in [4,7,9]:
 src=R/f'artifacts/signal_revision_20261022/pptx/Figure{num:02}_Signal_grouped.pptx'
 with zipfile.ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
 t=E.fromstring(data['ppt/slides/slide1.xml'])
 for s in t.xpath('//p:sp|//p:cxnSp|//p:pic',namespaces=N):
  n=s.find('.//p:cNvPr',N);sid=int(n.get('id'));name=n.get('name','');sp=s.find('p:spPr',N)
  # Neutral structures; two accents used only for information boundaries and feedback.
  accent=GRAY
  if num==4 and sid in [38,39,72,100]:accent=NAVY
  if num==4 and sid in [43,44,80,81,82,106,107,108]:accent=RUST
  if num==7 and sid in [14,16,113,81,82,135,136]:accent=NAVY
  if num==7 and sid in [15,114,144]:accent=RUST
  if num==9 and (name in ['flow-accepted','learn-memory-encoder','learn-neighbor-encoder']):accent=NAVY
  if num==9 and name=='flow-rejected':accent=RUST
  if sp is not None:
   for ef in sp.findall('a:effectLst',N):sp.remove(ef)
   for ln in sp.findall('a:ln',N):
    old=ln.find('a:solidFill/a:srgbClr',N);v=old.get('val','') if old is not None else ''
    if ln.find('a:gradFill',N) is not None:
     ln.remove(ln.find('a:gradFill',N));sf=E.Element('{'+N['a']+'}solidFill');add(sf,'a:srgbClr',val=GRAY);ln.insert(0,sf)
     ln.set('w',str(min(int(ln.get('w','16000')),19000)))
    elif old is not None:
     if v in ['000000','222222']:old.set('val','000000')
     elif all(int(v[k:k+2],16)>175 for k in [0,2,4]):old.set('val',RULE)
     else:old.set('val',accent)
   fill=sp.find('a:solidFill/a:srgbClr',N)
   if fill is not None:
    v=fill.get('val');fill.set('val','FFFFFF' if v=='FFFFFF' else ('000000' if v=='000000' else (FILL if sum(int(v[k:k+2],16) for k in [0,2,4])>600 else accent)))
   grad=sp.find('a:gradFill',N)
   if fill is not None and ((num==4 and sid in [28,36]) or (num==7 and sid in [17,83]) or (num==9 and name=='learn-encoder')):fill.set('val','E8EEF2')
   if grad is not None:
    sp.remove(grad);sf=E.Element('{'+N['a']+'}solidFill');add(sf,'a:srgbClr',val='000000');sp.insert(2,sf)
  # Recolor each existing icon using editable PowerPoint image effects; retain pixels/crop.
  blip=s.find('.//a:blip',N)
  if blip is not None:
   for ef in list(blip):
    if E.QName(ef).localname in ['duotone','grayscl']:blip.remove(ef)
   col='353A3D'
   if num==4 and name in ['calendar']:col=NAVY
   if num==4 and name in ['stock','order','cart','cost']:col=RUST
   if num==7 and name in ['source-database','version-document','available-document','accepted-check']:col=NAVY
   if num==7 and name in ['late-report','late-document','rejected-cross']:col=RUST
   if num==9 and name in ['retrieve-icon','retrieve-search','learn-memory']:col=NAVY
   if num==9 and name in ['review-icon','review-agent']:col=RUST
   if col=='353A3D':add(blip,'a:lum',bright=0,contrast=45000)
   if col==NAVY:col='10283B'
   elif col==RUST:col='6B3020'
   du=add(blip,'a:duotone');add(du,'a:srgbClr',val=col);add(du,'a:srgbClr',val='FFFFFF')
 for pr in t.xpath('//a:rPr|//a:defRPr|//a:endParaRPr',namespaces=N):
  lat=pr.find('a:latin',N)
  if lat is None:lat=add(pr,'a:latin',typeface='Arial')
  lat.set('typeface','Arial')
  for f in pr.findall('a:solidFill',N):pr.remove(f)
  sf=E.Element('{'+N['a']+'}solidFill');add(sf,'a:srgbClr',val=INK);pr.insert(0,sf)
  if pr.get('sz'):pr.set('sz',str(round(int(pr.get('sz'))*1.04)))
 for c in t.xpath('//a:tbl//a:tcPr//a:srgbClr',namespaces=N):
  if c.get('val')!='FFFFFF':c.set('val',RULE)
 order={'xfrm':0,'prstGeom':1,'custGeom':1,'noFill':2,'solidFill':2,'gradFill':2,'ln':3,'effectLst':4}
 for prop in t.xpath('//p:spPr',namespaces=N):prop[:]=sorted(prop,key=lambda c:order.get(E.QName(c).localname,8))
 data['ppt/slides/slide1.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
 with zipfile.ZipFile(D/'.build'/f'Figure{num:02}_Editorial_trial.pptx','w',zipfile.ZIP_DEFLATED) as z:
  for n,b in data.items():z.writestr(n,b)
 report[num]={'source':str(src.relative_to(R)),'groups':len(t.xpath('//p:grpSp',namespaces=N)),'native_tables':len(t.xpath('//a:tbl',namespaces=N))}
(D/'provenance.json').write_text(json.dumps(report,indent=2))
