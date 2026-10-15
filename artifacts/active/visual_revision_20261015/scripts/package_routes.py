from pathlib import Path
import zipfile,json
from lxml import etree as E
# Reuse the verified native OOXML group helper.
exec((Path(__file__).parent/'group_existing.py').read_text().split('reports=[]')[0])
repo=R.parents[2]
src=repo/'artifacts/editppt_runs/rsi_routes_20261015/final/5b50e258253031c1f9657a3d2da3be46_edited.pptx'
with zipfile.ZipFile(src) as z:blobs={n:z.read(n) for n in z.namelist()}
root=E.fromstring(blobs['ppt/slides/slide1.xml']);tree=root.find('p:cSld/p:spTree',NS)
kids=[x for x in tree if E.QName(x).localname not in ['nvGrpSpPr','grpSpPr','extLst']]
manifest=json.loads((repo/'artifacts/editppt_runs/rsi_routes_20261015/pages/page_001/manifest.json').read_text())
boxes=[]
for s in manifest['shapes']:
 if s['id'].startswith(('method-border-','header-border-')):boxes.append((s['id'],s['box_px']))
def xy(c):
 xf=c.find('.//a:xfrm',NS);a=xf.find('a:off',NS);b=xf.find('a:ext',NS)
 return (int(a.get('x'))/9525,int(a.get('y'))/9525,int(b.get('cx'))/9525,int(b.get('cy'))/9525)
uid=max(int(v) for v in root.xpath('//p:cNvPr/@id',namespaces=NS))+1
assigned={};unassigned=[];caption=[]
for c in kids:
 x,y,w,h=xy(c)
 if y>=1430:caption.append(c);continue
 target=None
 for name,(bx,by,bw,bh) in boxes:
  if x>=bx-1 and y>=by-1 and x+w<=bx+bw+1 and y+h<=by+bh+1:target=name;break
 if target:assigned.setdefault(target,[]).append(c)
 else:unassigned.append(c)
# Structural lines first, independent headings next, grouped labels last.
for c in kids:tree.remove(c)
outer=unassigned
for name,cs in assigned.items():outer.append(group(cs,name,uid));uid+=1
root_group=group(outer,'RSI research routes — individual editable components',uid);tree.append(root_group)
# Repair one extracted green logo that conflicted with the first sheet key color.
import posixpath
pics=root.findall('.//p:pic',NS)
# Find original picture by its source manifest index before grouping changes order.
orig=E.fromstring(blobs['ppt/slides/slide1.xml'])
index=next(i for i,v in enumerate(manifest['images']) if v['id']=='method-logo-19')
original_pic=orig.findall('.//p:pic',NS)[index]
relid=original_pic.find('.//a:blip',NS).get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
rels=E.fromstring(blobs['ppt/slides/_rels/slide1.xml.rels'])
rel=next(r for r in rels if r.get('Id')==relid)
media=posixpath.normpath(posixpath.join('ppt/slides',rel.get('Target')))
blobs[media]=(repo/'artifacts/editppt_runs/rsi_routes_20261015/pages/page_001/assets/repaired/nvidia.png').read_bytes()
blobs['ppt/slides/slide1.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
pr=E.fromstring(blobs['ppt/presentation.xml']);pr.find('p:sldSz',NS).set('cy',str(1425*9525));blobs['ppt/presentation.xml']=E.tostring(pr,xml_declaration=True,encoding='UTF-8',standalone=True)
out=R/'editable_ppt/03_RSI_Research_Routes_template_grouped.pptx'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,b in blobs.items():z.writestr(n,b)
print(out)
print('groups',len(root.findall('.//p:grpSp',NS)),'native',len(root.findall('.//p:sp',NS)),'logos',len(root.findall('.//p:pic',NS)))
