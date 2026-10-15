from pathlib import Path
import zipfile,json,posixpath,re,csv,copy
from lxml import etree as E
REPO=Path('/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey');BUILD=REPO/'artifacts/figure_collection_20261015'
OUT=Path('/Users/mjm/Desktop/Survey Figures/全部图件_单页去重');OUT.mkdir(exist_ok=True)
D=json.loads((BUILD/'inventory.json').read_text());NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
P=NS['p'];A=NS['a'];R=NS['r']
# Explicit supersession of caption-only copies and successive revisions of the same figure.
merge={26:5,27:6,28:7,29:8,30:9,31:10,32:11,39:34,40:34,43:34,45:34,41:33,42:17,44:20,57:13,62:12,63:3,37:3}
names={1:'TimeSeries_Overview',2:'TimeSeries_Research_Landscape',3:'RSI_Research_Routes',4:'RSI_Landscape_User_Edited',12:'RSI_Landscape_QuarterCircle',5:'ChatTS_Alignment',6:'AION_Three_Principles',7:'MERIT_Augmentation',8:'AnomaMind_Diagnosis',9:'TimeClaw_Runtime',10:'TimeSeriesGym_Benchmark',11:'TSAgent_Tool_Trace',13:'Module_Contribution_Timeline',14:'Survey_Organization',15:'Survey_Organization_RSI_Layout',16:'Agent_Construction',17:'Contribution_Layers',18:'General_Harness_Seven_Dimensions',19:'General_TimeSeries_Harness',20:'Task_Contracts_RSI_Layout',21:'TaskSpecific_Harness',22:'Infrastructure_Benchmarks',23:'Infrastructure_RSI_Layout',24:'Open_Problems',25:'LLM_Alignment_Alternative',33:'TimeSeries_Construction_RSI_Layout',34:'TimeSeries_Research_Routes',35:'RSI_Task_System_Inheritance',36:'RSI_Survey_Organization',38:'RSI_Four_Perspectives',46:'Old_Module_Timeline',47:'Old_Survey_Organization',48:'Old_RSI_Landscape',49:'Old_RSI_Open_Problems',50:'Old_Survey_Comparison',51:'Old_RSI_Four_Perspectives',52:'Old_RSI_Mechanism_Overview',53:'Old_RSI_Evidence_Map',54:'Old_RSI_Perspectives',55:'Old_RSI_Research_Routes',56:'Old_Scenario_Panel',58:'Old_TimeSeries_Architecture',59:'Old_TimeSeries_Organization',60:'Old_TimeSeries_Harness_Landscape',61:'Old_TimeSeries_Research_Routes'}
# Reuse native group builder, without executing its earlier delivery work.
helper={'__file__':str(REPO/'artifacts/active/visual_revision_20261015/scripts/group_existing.py')};exec((REPO/'artifacts/active/visual_revision_20261015/scripts/group_existing.py').read_text().split('reports=[]')[0],helper);group=helper['group']
def xml(b):return E.fromstring(b)
def pack(r,target):
 with zipfile.ZipFile(r['source']) as z:b={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
 pr=xml(b['ppt/presentation.xml']);ids=pr.find('p:sldIdLst',NS);chosen=list(ids)[r['slide']-1]
 for el in list(ids):
  if el is not chosen:ids.remove(el)
 # Discard navigation metadata that refers to other slides.
 for el in list(pr):
  if E.QName(el).localname in ('custShowLst','extLst'):pr.remove(el)
 b['ppt/presentation.xml']=E.tostring(pr,xml_declaration=True,encoding='UTF-8',standalone=True)
 root=xml(b[r['part']]);tree=root.find('p:cSld/p:spTree',NS)
 if not root.findall('.//p:grpSp',NS):
  kids=[c for c in tree if E.QName(c).localname not in ('nvGrpSpPr','grpSpPr','extLst')]
  if len(kids)>1:
   uid=max(int(v) for v in root.xpath('//p:cNvPr/@id',namespaces=NS))+1
   for c in kids:tree.remove(c)
   tree.append(group(kids,names[r['id']]+' — editable components',uid))
 b[r['part']]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 # Keep only OPC parts reachable from the selected single-slide presentation.
 keep=set();todo=['']; dropped_links=0
 while todo:
  part=todo.pop()
  if part in keep:continue
  if part:keep.add(part)
  rp=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels') if part else '_rels/.rels'
  if rp not in b:continue
  rels=xml(b[rp]);removed=[]
  for rel in list(rels):
   if rel.get('TargetMode')=='External':continue
   t=rel.get('Target');dest=posixpath.normpath(posixpath.join(posixpath.dirname(part),t)).lstrip('/')
   if re.fullmatch(r'ppt/slides/slide\d+\.xml',dest) and dest!=r['part']:
    removed.append(rel.get('Id'));rels.remove(rel);continue
   if dest not in b:raise RuntimeError('Missing part '+dest)
   todo.append(dest)
  if removed and part in b and part.endswith('.xml'):
   doc=xml(b[part]);changed=False
   for el in list(doc.iter()):
    if E.QName(el).localname in ('hlinkClick','hlinkHover') and el.get('{'+R+'}id') in removed:
     el.getparent().remove(el);changed=True;dropped_links+=1
   if changed:b[part]=E.tostring(doc,xml_declaration=True,encoding='UTF-8',standalone=True)
  b[rp]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True);keep.add(rp)
 ct=xml(b['[Content_Types].xml'])
 for el in list(ct):
  if E.QName(el).localname=='Override' and el.get('PartName','').lstrip('/') not in keep:ct.remove(el)
 b['[Content_Types].xml']=E.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True);keep.add('[Content_Types].xml')
 if 'docProps/app.xml' in keep:
  app=xml(b['docProps/app.xml'])
  for el in app.iter():
   if E.QName(el).localname=='Slides':el.text='1'
  b['docProps/app.xml']=E.tostring(app,xml_declaration=True,encoding='UTF-8',standalone=True)
 target.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
  for name in sorted(keep):z.writestr(name,b[name])
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  assert len([x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',x)])==1
  assert len(xml(z.read('ppt/presentation.xml')).findall('p:sldIdLst/p:sldId',NS))==1
  now=xml(z.read(r['part']));assert now.xpath('//a:t/text()',namespaces=NS)==r['texts']
  assert len(now.findall('.//p:sp',NS))==r['native']
 return {'native':r['native'],'pictures':r['pictures'],'groups':len(now.findall('.//p:grpSp',NS)),'links_to_removed_slides':dropped_links}
kept=[];mapping=[]
for r in D['unique']:
 if r['id'] in merge or r['id']==56:continue
 bucket='02_RSI参考模板' if r['id'] in (3,4,12,35,36,38) else '03_历史不同构图' if r['id']>=46 else '01_时序综述图件'
 filename=f"{r['id']:02d}_{names[r['id']]}.pptx";target=OUT/bucket/filename
 result=pack(r,target);kept.append({'id':r['id'],'file':str(target),'relative':str(target.relative_to(OUT)),'source':r['source'],'source_slide':r['slide'],**result})
for r in D['unique']:
 if r['id']==56:
  D['excluded'].append({'source':r['source'],'slide':r['slide'],'reason':'未完成的空白占位草稿'});continue
 dest=merge.get(r['id'],r['id']);chosen=next(x for x in kept if x['id']==dest)
 for source in [{'source':r['source'],'slide':r['slide']}]+r['duplicates']:
  mapping.append({**source,'output':chosen['relative'],'decision':'同图旧版/标题副本合并' if r['id'] in merge else '保留或同内容副本去重'})
report={'source_file_count':D['source_files'],'candidate_slide_count':D['slides'],'output_count':len(kept),'kept':kept,'source_mapping':mapping,'excluded':D['excluded']}
(BUILD/'collection_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));(OUT/'整理记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
with (OUT/'来源与去重清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['source','slide','output','decision']);w.writeheader();w.writerows(mapping)
print('OUTPUTS',len(kept))
for b in sorted(set(Path(x['relative']).parts[0] for x in kept)):print(b,sum(Path(x['relative']).parts[0]==b for x in kept))
