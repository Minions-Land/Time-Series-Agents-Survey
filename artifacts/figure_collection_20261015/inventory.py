from pathlib import Path
import zipfile,re,json,posixpath,unicodedata
from lxml import etree as E
ROOT=Path('/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey')
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
files=sorted(set(ROOT.rglob('*.pptx'))|set(Path('/Users/mjm/Desktop/Survey Figures').rglob('*.pptx')))
records=[];ex=[]
for p in files:
 if p.name.startswith('~$') or 'figure_collection_20261015' in str(p):continue
 if 'group_test' in str(p):ex.append({'source':str(p),'reason':'分组功能测试，不是论文图'});continue
 with zipfile.ZipFile(p) as z:
  pr=E.fromstring(z.read('ppt/presentation.xml')); rels=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));lookup={r.get('Id'):posixpath.normpath(posixpath.join('ppt',r.get('Target'))).lstrip('/') for r in rels}
  for index,sl in enumerate(pr.findall('p:sldIdLst/p:sldId',NS),1):
   part=lookup[sl.get('{'+NS['r']+'}id')];s=E.fromstring(z.read(part));texts=s.xpath('//a:t/text()',namespaces=NS);native=len(s.findall('.//p:sp',NS));pics=len(s.findall('.//p:pic',NS));groups=len(s.findall('.//p:grpSp',NS))
   if native==0 or (native<=8 and pics==1):ex.append({'source':str(p),'slide':index,'reason':'整图位图或图片切片，未完成组件化'});continue
   norm=lambda t:' '.join(re.findall(r'\w+',unicodedata.normalize('NFKC',t).lower()))
   sig='\n'.join(sorted(norm(t) for t in texts if norm(t)))
   # Grouped recent delivery > active sources > intermediate candidates.
   score=(100 if '/visual_revision_' in str(p) or '/Editable_' in str(p) else 70 if '/active/' in str(p) else 20)
   score+=10 if groups else 0
   score+=5 if 'notitle' in p.name or 'nocaption' in p.name else 0
   if 'all_elements' in p.name:score+=25
   if '/survey_ppt_figures/' in str(p):score+=2
   records.append({'source':str(p),'slide':index,'part':part,'texts':texts,'signature':sig,'native':native,'pictures':pics,'groups':groups,'score':score,'mtime':p.stat().st_mtime})
clusters={}
for r in records:clusters.setdefault(r['signature'],[]).append(r)
unique=[]
for sig,items in clusters.items():
 items.sort(key=lambda a:(a['score'],a['mtime']),reverse=True);r=dict(items[0]);r['duplicates']=[{'source':a['source'],'slide':a['slide']} for a in items[1:]];unique.append(r)
unique.sort(key=lambda r:(-r['score'],r['source'],r['slide']))
for i,r in enumerate(unique):r['id']=i+1
out=ROOT/'artifacts/figure_collection_20261015';(out/'inventory.json').write_text(json.dumps({'source_files':len(files),'slides':len(records),'unique':unique,'excluded':ex},ensure_ascii=False,indent=2))
print('source',len(files),'eligible slides',len(records),'exact content groups',len(unique),'excluded',len(ex))
for r in unique:print(r['id'],r['native'],r['pictures'],r['groups'],Path(r['source']).name,r['slide'],' | '.join(r['texts'][:2])[:160])
