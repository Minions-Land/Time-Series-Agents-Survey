"""Generate a human-readable intermediary to author-provided external resources."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'paper_classification_ledger.json').read_text())
rows=[]
for record in records:
 for link in record['official_resources']:
  p=link['provenance'];a=link['availability']
  rows.append({'citation_key':record['citation']['key'],'work':record['work'],'kind':link['kind'],'url':link['url'],'availability':a['status'],'http_status':a.get('http_status',''),'source_path':p['source_path'],'source_locator':p['locator'],'checked_at':a['checked_at']})
path=ROOT/'references/official_resources.csv'
with path.open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
lines=['# Official resource index','',f"{len(rows)} author-attributed links across {sum(bool(r['official_resources']) for r in records)} works. Links lead to the original resources; this repository does not repackage implementations. Availability was checked on {' and '.join(sorted({r['checked_at'] for r in rows}))}. Full attribution and fetch results are retained in the JSON cards.",'','| Work | Resource | Availability | Source |','|---|---|---|---|']
for r in rows:
 lines.append(f"| {r['work'].replace('|','/')} | [{r['kind']}]({r['url']}) | {r['availability']} | {r['source_locator'].replace('|','/')} |")
lines+=['','## Sources without a located author resource','','The following records have no author-attributed external resource located in the inspected paper text and PDF hyperlinks. Their paper and bibliographic links remain in the ledger.','']
lines += ['- '+r['work']+' (`'+r['citation']['key']+'`)' for r in records if r['resource_review_status']=='not_found_in_source']
(ROOT/'docs/official-resources.md').write_text('\n'.join(lines)+'\n')
print('Exported',len(rows),'resource links')
