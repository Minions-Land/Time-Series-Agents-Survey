"""Update the appendix's reviewed profiles and database snapshot from the ledger."""
import json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'paper_classification_ledger.json').read_text());p=ROOT/'main.tex';s=p.read_text()
def escape(v):
 return v.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
for r in records:
 mods=r['module_level_contributions'].get('modules')
 if mods is None:continue
 key=r['citation']['key']
 lines=s.splitlines()
 for i,line in enumerate(lines):
  if '\\citep{'+key+'}' in line and '& \\textbf{GH:}' in line:
   first=line.split('& \\textbf{GH:}')[0]
   parts=[]
   for layer in ['GH','GTS','TSK','LLM']:
    names=[escape(m['name']) for m in mods if m['layer']==layer]
    if layer=='LLM' and not names:continue
    parts.append('\\textbf{'+layer+':} '+('; '.join(names)+'.' if names else '--'))
   lines[i]=first+'& '+r'\newline'.join(parts)+r'\\\midrule'
 s='\n'.join(lines)+'\n'
claims=Counter(r['claim']['review_status'] for r in records);tasks=Counter(t for r in records for t in r['tasks']['axes'])
reviewed=[r for r in records if 'modules' in r['module_level_contributions']]
modules=sum(len(r['module_level_contributions']['modules']) for r in reviewed)
snapshot=(r'\textbf{Current ledger snapshot.} The database contains \textbf{'+str(len(records))+r'} Paper Cards, including 136 production-Bib records and 2 repository-only resources. '
 +str(claims['paper_verified'])+' records have paper-verified claim summaries. Module-level review currently covers '+str(len(reviewed))+' works and '+str(modules)+' individually located modules; the remaining records retain candidate classifications. '
 +'Task memberships comprise '+str(tasks['forecasting_reasoning'])+' forecasting/prediction, '+str(tasks['augmentation_synthesis'])+' augmentation/synthesis, '+str(tasks['anomaly_detection_diagnosis'])+' anomaly/diagnosis, and '+str(tasks['decision_support'])+' decision-support records. '+str(sum(r['llm_side_contribution']['present'] for r in records))+' records carry LLM-side annotations. A record may have several task memberships.')
s=re.sub(r'\\textbf\{Current ledger snapshot\.\}[^\n]*',lambda _:snapshot,s)
p.write_text(s)
print('Snapshot synchronized:',len(records),'cards;',len(reviewed),'module-reviewed works;',modules,'modules')
