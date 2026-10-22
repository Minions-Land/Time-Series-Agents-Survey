from pathlib import Path
from lxml import etree as E
import zipfile,json,copy
D=Path(__file__).resolve().parent;R=D.parents[1];N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def tag(k):return '{'+N[k.split(':')[0]]+'}'+k.split(':')[1]
def add(p,k,**kw):return E.SubElement(p,tag(k),**{k:str(v) for k,v in kw.items()})
def gradient(ln,c1,c2):
 for c in list(ln):
  if E.QName(c).localname in ['solidFill','gradFill','noFill']:ln.remove(c)
 g=E.Element(tag('a:gradFill'),rotWithShape='1');ls=add(g,'a:gsLst')
 for pos,col in [(0,c1),(100000,c2)]:add(add(ls,'a:gs',pos=pos),'a:srgbClr',val=col)
 add(g,'a:lin',ang=0,scaled=1);ln.insert(0,g)
def shadow(sp):
 for c in sp.findall('a:effectLst',N):sp.remove(c)
 sh=add(add(sp,'a:effectLst'),'a:outerShdw',blurRad=15000,dist=9000,dir=5400000,algn='ctr',rotWithShape=0);add(add(sh,'a:srgbClr',val='333333'),'a:alpha',val=12000)
def iconcolor(name):
 s=name.lower()
 if any(v in s for v in ['reject','fail','false','cart','cost','order','package','x-']):return 'C16A4A'
 if any(v in s for v in ['check','review','memory','database','storage','data','learn']):return '258B79'
 if any(v in s for v in ['brain','bot','agent','workflow','operation-code','requirements']):return '7A659B'
 if any(v in s for v in ['wrench','tool','sliders','gear','refresh']):return 'B9862E'
 return '287EA6'
# Native icon paths already present in Figure 15, reused as editable groups.
src=E.fromstring(zipfile.ZipFile(R/'artifacts/editorial_unified_20261022/pptx/Figure15_Editorial.pptx').read('ppt/slides/slide1.xml'))
def native_icon(t,prefix,x,y,h,label):
 shapes=[copy.deepcopy(s) for s in src.xpath('//p:sp',namespaces=N) if s.find('.//p:cNvPr',N).get('name','').startswith(prefix+'-')]
 # file-text appears twice in source; use first instance only.
 if prefix=='file-text':shapes=shapes[:5]
 coords=[]
 for s in shapes:
  xf=s.find('p:spPr/a:xfrm',N);o=xf.find('a:off',N);e=xf.find('a:ext',N);coords.append([int(o.get('x')),int(o.get('y')),int(e.get('cx')),int(e.get('cy'))])
 xmin=min(c[0] for c in coords);ymin=min(c[1] for c in coords);w=max(c[0]+c[2] for c in coords)-xmin;oh=max(c[1]+c[3] for c in coords)-ymin
 nextid=max(map(int,t.xpath('//p:cNvPr/@id',namespaces=N)))+1
 g=E.Element(tag('p:grpSp'));nv=add(g,'p:nvGrpSpPr');add(nv,'p:cNvPr',id=nextid,name=label);add(nv,'p:cNvGrpSpPr');add(nv,'p:nvPr');xf=add(add(g,'p:grpSpPr'),'a:xfrm')
 add(xf,'a:off',x=x,y=y);add(xf,'a:ext',cx=round(w*h/oh),cy=h);add(xf,'a:chOff',x=xmin,y=ymin);add(xf,'a:chExt',cx=w,cy=oh)
 for i,s in enumerate(shapes):
  s.find('.//p:cNvPr',N).set('id',str(nextid+i+1))
  for c in s.xpath('./p:spPr/a:ln/a:solidFill/a:srgbClr',namespaces=N):c.set('val','C16A4A' if prefix=='x' else '258B79')
  g.append(s)
 t.find('p:cSld/p:spTree',N).append(g)
report={}
for num in range(4,16):
 p=R/f'artifacts/editorial_unified_20261022/pptx/Figure{num:02}_Editorial.pptx'
 with zipfile.ZipFile(p) as z:data={k:z.read(k) for k in z.namelist()}
 t=E.fromstring(data['ppt/slides/slide1.xml']);arrows=[];icons=[];removed=[]
 for s in list(t.xpath('//p:sp|//p:pic|//p:cxnSp',namespaces=N)):
  nv=s.find('.//p:cNvPr',N);name=nv.get('name','');sid=int(nv.get('id'));sp=s.find('p:spPr',N)
  if num==9 and (name in ['review-wave0','review-wave1','review-wave2','learn-memview1','learn-memview2','learn-neighbors'] or name.startswith('review-evidence')):
   removed.append(name);s.getparent().remove(s);continue
  if sp is None:continue
  # Flow arrows only. Do not modify series, chart axes, interval bounds or plain rules.
  ln=sp.find('a:ln',N)
  excluded=any(v in name.lower() for v in ['axis','axes','time','wave','series','candidate','interval','performance-key','reference','signal','rule'])
  ends=ln.xpath('./a:headEnd|./a:tailEnd',namespaces=N) if ln is not None else []
  arrow=any(e.get('type','none')!='none' for e in ends)
  if arrow and not excluded:
   old=ln.xpath('./a:solidFill/a:srgbClr/@val',namespaces=N);warm=bool(old and old[0] in ['A65F48','C16A4A']) or 'reject' in name
   ln.set('w',str(min(26000,max(17000,round(int(ln.get('w','10000'))*1.5)))))
   gradient(ln,'D3A18B' if warm else '87A1B1','A65F48' if warm else '3E6178');shadow(sp);arrows.append(name)
  # Recolor isolated icon images and existing native icon components only.
  blip=s.find('.//a:blip',N)
  if blip is not None and num!=14:
   for ef in list(blip):
    if E.QName(ef).localname in ['duotone','lum','grayscl']:blip.remove(ef)
   col=iconcolor(name);du=add(blip,'a:duotone');add(du,'a:srgbClr',val=col);add(du,'a:srgbClr',val='FFFFFF');icons.append(name)
  native=any(name.startswith(v+'-') for v in ['layers','file-text','brain-circuit','list-checks','wrench','messages-square','bot','target','scan-search','book-open','circle-check','workflow','database','refresh-cw','braces','sliders-horizontal','search-check','git-branch','shield-check','calculator','check','x','package'])
  if native:
   col=iconcolor(name)
   for c in sp.xpath('./a:ln/a:solidFill/a:srgbClr|./a:solidFill/a:srgbClr',namespaces=N):
    if c.get('val')!='FFFFFF':c.set('val',col)
   icons.append(name)
 if num==9:
  for i,y in enumerate([2750000,4070000,5400000]):
   native_icon(t,'file-text',8900000,y,650000,'review-record-'+str(i))
   native_icon(t,'check' if i<2 else 'x',9680000,y+300000,280000,'review-status-'+str(i))
  for i,x in enumerate([12900000,14800000]):native_icon(t,'file-text',x,2450000,650000,'accepted-view-record-'+str(i))
  for i,x in enumerate([12500000,13500000]):native_icon(t,'file-text',x,5900000,460000,'retrieved-neighbor-record-'+str(i))
 order={'xfrm':0,'prstGeom':1,'custGeom':1,'noFill':2,'solidFill':2,'gradFill':2,'ln':3,'effectLst':4}
 for sp in t.xpath('//p:spPr',namespaces=N):sp[:]=sorted(sp,key=lambda c:order.get(E.QName(c).localname,8))
 data['ppt/slides/slide1.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
 with zipfile.ZipFile(D/'.build'/f'Figure{num:02}_Accent.pptx','w',zipfile.ZIP_DEFLATED) as z:
  for k,v in data.items():z.writestr(k,v)
 report[num]={'source':str(p.relative_to(R)),'accent_icons':icons,'strengthened_arrows':arrows,'removed_repeated_traces':removed,'groups':len(t.xpath('//p:grpSp',namespaces=N))}
(D/'changes.json').write_text(json.dumps(report,indent=2))
