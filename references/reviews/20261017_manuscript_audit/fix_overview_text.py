from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json
base=Path('artifacts/active')
changes={2:{
'System definition':'Motivation and scope','Review scope':'Agent interaction loop','Paper-card evidence':'Tasks and module reuse',
'Temporal representation':'Model interfaces','Alignment and reasoning':'Temporal adaptation','LLM-side methods':'Workflow policies',
'Tools and memory          Control and execution':'Tools and memory        Control and execution',
'Temporal state             Provenance and validation':'Planning and learning    Coordination',
'Time-series harnesses     Reusable modules':'Data management         Temporal processing',
'Task contracts             Benchmark protocols':'Context and memory      Temporal validation',
'Case Studies':'System Analyses',
'Paper-card database        Module-level counts':'Transfer and memory      Evidence quality',
'Open tasks                 Evidence gaps':'Decision feedback        Design implications',
'System map':'Construction choices','Open problems':'Evaluation and reuse'},3:{
'Paper cards record module-level contributions across the LLM, Harness, temporal, task, and evaluation layers.':'LLM capabilities combine with three Harness scopes to support temporal tasks.',
'Language capability':'LLM interaction',
'representation':'interpret observations','alignment':'select tool actions','temporal reasoning':'use returned feedback','ChatTS lineage':'temporal adaptation',
'Paper card fields':'Model contribution','claim · evidence · BibTeX':'interfaces and training',
'LLM component':'Action-selection model',
'Evaluation and ledger':'Evaluation and evidence'}}
files=[base/'TimeSeriesAgent_Figures_RSI_template_working_copy_grouped.pptx',base/'Figure2_organization_rsi_adapted_grouped.pptx',base/'Figure3_construction_rsi_adapted_grouped.pptx',base/'survey_ppt_figures/Figure2_organization_rsi_adapted_grouped.pptx',base/'survey_ppt_figures/Figure3_construction_rsi_adapted_grouped.pptx']
log=[]
for f in files:
 with ZipFile(f) as z: data={n:z.read(n) for n in z.namelist()}
 for n,mapping in changes.items():
  name=f'ppt/slides/slide{n}.xml';r=etree.fromstring(data[name]);groups=len(r.xpath('//*[local-name()="grpSp"]'));count=0
  for t in r.xpath('//*[local-name()="t"]'):
   if t.text in mapping:t.text=mapping[t.text];count+=1
  assert count==len(mapping),(f,n,count,len(mapping))
  assert len(r.xpath('//*[local-name()="grpSp"]'))==groups
  data[name]=etree.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
  log.append({'file':str(f),'slide_part':name,'changed_text_runs':count,'native_groups_preserved':groups,'changes':mapping})
 tmp=f.with_suffix('.tmp.pptx')
 with ZipFile(tmp,'w') as z:
  for n,d in data.items():z.writestr(n,d)
 tmp.replace(f)
Path('references/reviews/20261017_manuscript_audit/overview_text_changes.json').write_text(json.dumps(log,indent=2)+'\n')
