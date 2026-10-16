"""Read-only coverage and quotation checks for the boundary review files."""
import json
from pathlib import Path
from collections import Counter
from audit_review_evidence import normalize
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'references/reviews/20261016_boundary_audit'

def check():
    issues=[];counts=Counter();seen=set()
    for i in range(1,4):
        path=FOLDER/f'shard_{i}.json'
        if not path.exists():issues.append(f'{path.name}: missing');continue
        assignment=json.loads((FOLDER/f'assignment_{i}.json').read_text())
        expected={m['id'] for r in assignment for m in r['module_level_contributions']['modules']}
        reviews=json.loads(path.read_text());actual=set()
        if {r['citation_key'] for r in reviews}!={r['citation']['key'] for r in assignment}:issues.append(f'shard {i}: work coverage')
        for row in reviews:
            for module in row['modules']:
                mid=module['id'];actual.add(mid)
                if mid in seen:issues.append(f'{mid}: duplicate')
                seen.add(mid);counts[module['decision']]+=1
                if not module.get('rationale'):issues.append(f'{mid}: missing rationale')
                source=module.get('source_path','');quote=normalize(module.get('supporting_quote',''))
                cache=ROOT/'tmp/full_audit_sources'/(Path(source).stem+'.json')
                if cache.exists():
                    pages=json.loads(cache.read_text())['pages'];numbers=module.get('pages_read',[])
                    if not numbers:issues.append(f'{mid}: no pages')
                    elif quote and not any(quote in normalize(pages[n-1]) for n in numbers if isinstance(n,int) and 0<n<=len(pages)):
                        issues.append(f'{mid}: quote not found on declared pages')
                elif source and (ROOT/source).is_file() and not source.endswith('.pdf'):
                    if quote and quote not in normalize((ROOT/source).read_text()):issues.append(f'{mid}: quote not found in repository source')
                else:issues.append(f'{mid}: source cache unavailable')
                if not quote:issues.append(f'{mid}: missing quotation')
        if actual!=expected:issues.append(f'shard {i}: module coverage missing={expected-actual}, extra={actual-expected}')
    return {'reviewed_modules':len(seen),'decisions':dict(counts),'issues':issues}
if __name__=='__main__':
    result=check();print(json.dumps(result,indent=2,ensure_ascii=False));raise SystemExit(bool(result['issues']))
