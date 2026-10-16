"""Render the appendix profiles and snapshot from adjudicated module records."""
import json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'paper_classification_ledger.json').read_text());p=ROOT/'main.tex';s=p.read_text()
def escape(v):
 return v.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('–','--').replace('—','---')
bykey={r['citation']['key']:r for r in records}
lines=s.splitlines();new=[]
for line in lines:
 if '& \\textbf{' not in line:
  new.append(line);continue
 match=re.search(r'\\citep\{([^}]+)\}',line)
 key=match.group(1) if match else ('moiraiagent2026' if '\\RepoMoirai' in line else 'zhang2025llm' if '\\RepoLLMTSFD' in line else None)
 if key not in bykey:new.append(line);continue
 r=bykey[key];view=r['module_level_contributions'];mods=view.get('modules')
 if mods is None:raise ValueError('Unreviewed profile '+key)
 if view['review_status'] in ['out_of_scope','blocked']:continue
 first=line.split('& \\textbf{')[0]
 # Keep the printed Agent terminology marker aligned with the canonical record.
 first=first.replace(r'\selfclaim{}','')
 if not r['claimed_as_agent'] and match:
  first=first.replace(match.group(0),match.group(0)+r'\selfclaim{}',1)
 # Replace old inferred task label with the current contract description.
 first=first.split(r'\newline')[0]+r'\newline '+escape(r['tasks']['source_label'])+' '
 parts=[]
 for layer in ['GH','GTS','TSK','LLM']:
  names=[escape(m['name']) for m in mods if m['layer']==layer]
  if not names:continue
  parts.append('\\textbf{'+layer+':} '+'; '.join(names)+'.')
 new.append(first+'& '+r'\newline'.join(parts)+r'\\\midrule')
s='\n'.join(new)+'\n'
status=Counter(r['module_level_contributions']['review_status'] for r in records)
active=[r for r in records if r['module_level_contributions']['review_status'] in ['paper_verified','repository_verified']]
tasks=Counter(t for r in active for t in r['tasks']['axes'])
mods=[m for r in active for m in r['module_level_contributions']['modules']];layers=Counter(m['layer'] for m in mods)
snapshot=(r'\textbf{Current ledger snapshot.} The database contains \textbf{'+str(len(records))+r'} examined records: '
 +str(status['paper_verified'])+' paper-supported works, '+str(status['repository_verified'])+' repository-supported resources, and '+str(status['out_of_scope'])+' background records excluded from contribution counts. '
 +'The '+str(len(active))+' retained records contain '+str(len(mods))+' source-located modules: '+str(layers['LLM'])+' LLM-side, '+str(layers['GH'])+' General Harness, '+str(layers['GTS'])+' General Time-Series Harness, and '+str(layers['TSK'])+' Task-Specific Harness modules. '
 +'Task memberships comprise '+str(tasks['forecasting_reasoning'])+' forecasting/prediction, '+str(tasks['augmentation_synthesis'])+' augmentation/synthesis, '+str(tasks['anomaly_detection_diagnosis'])+' anomaly/diagnosis, and '+str(tasks['decision_support'])+' decision-support records; additional task values include classification, imputation, annotation, and question answering. Each module has one layer and may have several mechanism and task labels.')
s=re.sub(r'\\textbf\{Current ledger snapshot\.\}[^\n]*',lambda _:snapshot,s)
s=re.sub(r'Profiles of the \d+ reviewed works\.', 'Profiles of the '+str(len(active))+' retained works.',s)
p.write_text(s)
print('Snapshot:',len(records),'examined;',len(active),'retained;',len(mods),'modules;',dict(layers))
