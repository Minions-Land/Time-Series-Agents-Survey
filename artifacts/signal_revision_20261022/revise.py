from pathlib import Path
from lxml import etree as E
import zipfile,json,copy,re
R=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def el(tag,**kw):return E.Element('{'+NS[tag.split(':')[0]]+'}'+tag.split(':')[1],**{k:str(v) for k,v in kw.items()})
def add(parent,tag,**kw):e=el(tag,**kw);parent.append(e);return e
sources=json.loads((D/'sources.json').read_text())
ids={5:{10061,*range(10002,10008),*range(10074,10080)},6:set(),7:{111,119,123,125,127,128,134,138,139,*range(2,14),*range(18,81),*range(84,110)},8:{4,31,32,33,34,76,86,87,88,89,90,135,136,184,185,186},9:{10,11,12,13,16,17,18,19,23,27,33,34,37},10:{30,40},11:{22,33,34,35,36,*range(9,18)},12:{36,37,66,67,68,69},13:{12,16,21,22,32,38,39,45,52},14:{17,*range(27,40)},15:{10550,10554,10585}}
axes={5:set(),6:set(),7:{110},8:{16,18,19,65,123,124,172,173,174},9:set(),10:{29,39},11:{18,21,32,37},12:{65},13:{10,14,19,30,36,43,50},14:set(),15:{10549,10553,10584}}
dash={8:{33,186},11:{34,36},12:{37,67,69},13:{21,38}}
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
    if i==7 or i==15:
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
 data['ppt/slides/slide1.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
 dest=D/'.build'/f'Figure{i:02}_Signal_grouped.pptx'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as f:
  for n,b in data.items():f.writestr(n,b)
 report[i]={'source':src,'native_signal_shapes':changed,'time_axes':sorted(axes[i]),'comic_labels':fonts,'groups':len(t.xpath('//p:grpSp',namespaces=NS))}
(D/'changes.json').write_text(json.dumps(report,indent=2))
# Digitize the four small waveform examples from their existing source pixels.
# Coordinates preserve the source glyphs; no new experimental data are introduced.
from PIL import Image
import io,numpy as np
path=D/'.build/Figure10_Signal_grouped.pptx'
with zipfile.ZipFile(path) as z:data={n:z.read(n) for n in z.namelist()}
t=E.fromstring(data['ppt/slides/slide1.xml']);rels=E.fromstring(data['ppt/slides/_rels/slide1.xml.rels']);rm={a.get('Id'):a.get('Target') for a in rels}
nextid=50000
for pic in list(t.xpath('//p:pic',namespaces=NS)):
 n=pic.find('.//p:cNvPr',NS);name=n.get('name')
 if name not in ['pattern0','pattern1','pattern2','false-alert']:continue
 rel=pic.find('.//a:blip',NS).get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed');im=np.array(Image.open(io.BytesIO(data[rm[rel].replace('../','ppt/')])).convert('RGBA'))
 rgb=im[:,:,:3].astype(float);mask=(rgb[:,:,2]>rgb[:,:,0]*1.12)&(rgb[:,:,0]<150)&(im[:,:,3]>80)
 points=[]
 for x in range(im.shape[1]):
  ys=np.where(mask[:,x])[0]
  if len(ys):points.append((x,float(np.median(ys))))
 sp=el('p:sp');nv=add(sp,'p:nvSpPr');nextid+=1;add(nv,'p:cNvPr',id=nextid,name=name+'-editable-waveform');add(nv,'p:cNvSpPr');add(nv,'p:nvPr');prop=add(sp,'p:spPr');prop.append(copy.deepcopy(pic.find('p:spPr/a:xfrm',NS)));geom=add(prop,'a:custGeom')
 for q in ['avLst','gdLst','ahLst','cxnLst']:add(geom,'a:'+q)
 add(geom,'a:rect',l='0',t='0',r='r',b='b');pl=add(geom,'a:pathLst');pa=add(pl,'a:path',w=im.shape[1]*100,h=im.shape[0]*100,fill='none',stroke=1)
 for j,(x,y) in enumerate(points):cmd=add(pa,'a:moveTo' if j==0 else 'a:lnTo');add(cmd,'a:pt',x=round(x*100),y=round(y*100))
 add(prop,'a:noFill');ln=add(prop,'a:ln',w=14000,cap='rnd');solid(ln,'000000');effect(prop)
 parent=pic.getparent();idx=parent.index(pic);parent.insert(idx,sp)
 if name=='false-alert':
  # Keep the original alert annotation as a separate cropped picture above the native waveform.
  red=(rgb[:,:,0]>rgb[:,:,2]*1.3)&(rgb[:,:,0]>rgb[:,:,1]*1.25)&(rgb[:,:,1]<180)&(im[:,:,3]>80)
  yy,xx=np.where(red);x0,x1=int(xx.min()),int(xx.max()+1);y0,y1=int(yy.min()),int(yy.max()+1)
  # Original crop in PowerPoint; raster bytes stay unchanged.
  xf=pic.find('p:spPr/a:xfrm',NS);off=xf.find('a:off',NS);ext=xf.find('a:ext',NS);ox,oy,cx,cy=map(int,[off.get('x'),off.get('y'),ext.get('cx'),ext.get('cy')]);off.set('x',str(ox+round(cx*x0/im.shape[1])));off.set('y',str(oy+round(cy*y0/im.shape[0])));ext.set('cx',str(round(cx*(x1-x0)/im.shape[1])));ext.set('cy',str(round(cy*(y1-y0)/im.shape[0])))
  bf=pic.find('p:blipFill',NS);bl=bf.find('a:blip',NS)
  for c in list(bl):bl.remove(c)
  cr=el('a:srcRect',l=round(x0/im.shape[1]*100000),r=round((1-x1/im.shape[1])*100000),t=round(y0/im.shape[0]*100000),b=round((1-y1/im.shape[0])*100000));bf.insert(1,cr)
  # Blue pixels in the crop would reintroduce a colored trace; replace alert with editable annotation.
  parent.remove(pic)
  alert=copy.deepcopy(sp);nextid+=1;alert.find('.//p:cNvPr',NS).set('id',str(nextid));alert.find('.//p:cNvPr',NS).set('name','false-alert-annotation');ap=alert.find('p:spPr',NS);ag=ap.find('a:custGeom',NS);ap.remove(ag);ag=el('a:prstGeom',prst='ellipse');add(ag,'a:avLst');ap.insert(1,ag);ax=ap.find('a:xfrm',NS);ax.find('a:off',NS).set('x',str(ox+round(cx*x0/im.shape[1])));ax.find('a:off',NS).set('y',str(oy+round(cy*y0/im.shape[0])));ax.find('a:ext',NS).set('cx',str(round(cx*(x1-x0)/im.shape[1])));ax.find('a:ext',NS).set('cy',str(round(cy*(y1-y0)/im.shape[0])));al=ap.find('a:ln',NS);solid(al,'AA625E');add(al,'a:prstDash',val='dash');parent.insert(idx+1,alert)
 else:parent.remove(pic)
data['ppt/slides/slide1.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
 for n,b in data.items():z.writestr(n,b)
