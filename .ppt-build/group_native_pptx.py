from __future__ import annotations
import zipfile, shutil, os, re, sys, tempfile
from lxml import etree

NS_P='http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A='http://schemas.openxmlformats.org/drawingml/2006/main'
NS_R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P='{%s}'%NS_P; A='{%s}'%NS_A
SLIDE_W=15240000; SLIDE_H=8572500

def q(tag, ns=P): return ns+tag

def name_of(el):
    c=el.find('.//'+q('cNvPr'))
    return c.get('name','') if c is not None else ''

def add_group(children, gid, gname):
    g=etree.Element(q('grpSp'))
    nv=etree.SubElement(g,q('nvGrpSpPr'))
    etree.SubElement(nv,q('cNvPr'),id=str(gid),name=gname)
    etree.SubElement(nv,q('cNvGrpSpPr'))
    etree.SubElement(nv,q('nvPr'))
    gp=etree.SubElement(g,q('grpSpPr'))
    x=etree.SubElement(gp,q('xfrm',A))
    etree.SubElement(x,q('off',A),x='0',y='0')
    etree.SubElement(x,q('ext',A),cx=str(SLIDE_W),cy=str(SLIDE_H))
    etree.SubElement(x,q('chOff',A),x='0',y='0')
    etree.SubElement(x,q('chExt',A),cx=str(SLIDE_W),cy=str(SLIDE_H))
    for ch in children: g.append(ch)
    return g

def process_slide(xml, group_specs):
    root=etree.fromstring(xml)
    tree=root.find('.//'+q('spTree'))
    if tree is None: return xml, []
    elems=list(tree)
    content=[e for e in elems if etree.QName(e).localname not in ('nvGrpSpPr','grpSpPr')]
    name_map={name_of(e):e for e in content if name_of(e)}
    maxid=0
    for e in tree.xpath('.//*[@id]'):
        try:maxid=max(maxid,int(e.get('id')))
        except: pass
    report=[]
    used=set()
    for spec in group_specs:
        names=[n for n in spec if n in name_map and name_map[n] not in used]
        if len(names)<2: continue
        selected=[name_map[n] for n in names]
        indices=sorted(content.index(e) for e in selected)
        insert_at=min(indices)
        gid=maxid+1; maxid+=1
        g=add_group(selected,gid,'group-' + re.sub(r'[^A-Za-z0-9_-]+','-',names[0]))
        # remove selected then reinsert at first location among content order
        for e in selected:
            if e.getparent() is tree: tree.remove(e)
        # locate current element at content index after removals; use first surviving element originally after insert
        current=list(tree)
        # find next surviving content element with original index > insert_at
        nextel=None
        for e in content:
            if e in selected: continue
            if content.index(e)>insert_at and e.getparent() is tree:
                nextel=e; break
        if nextel is not None: tree.insert(list(tree).index(nextel),g)
        else: tree.append(g)
        used.update(selected); report.append({'name':g.get('name'),'children':names})
    # group remaining visible shapes into one group, preserving order
    remaining=[e for e in list(tree) if etree.QName(e).localname not in ('nvGrpSpPr','grpSpPr','grpSp')]
    if remaining:
        maxid+=1; g=add_group(remaining,maxid,'group-remaining-components')
        for e in remaining:
            if e.getparent() is tree: tree.remove(e)
        tree.append(g)
        report.append({'name':'group-remaining-components','children':[name_of(e) for e in remaining]})
    return etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=None), report

def group_pptx(src,dst,specs):
    os.makedirs(os.path.dirname(dst),exist_ok=True)
    fd,tmp=tempfile.mkstemp(suffix='.pptx'); os.close(fd)
    report=[]
    with zipfile.ZipFile(src,'r') as zin, zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data=zin.read(item.filename)
            if item.filename.startswith('ppt/slides/slide') and item.filename.endswith('.xml'):
                data,r=process_slide(data,specs); report.extend(r)
            zout.writestr(item,data)
    shutil.move(tmp,dst)
    return report

def specs_for(src):
    base=os.path.basename(src)
    specs=[]
    def add(*names): specs.append(list(names))
    add('figure-title','figure-subtitle')
    if base.startswith('Figure2_'):
        add('survey-label-box','survey-label','survey-sublabel','survey-leader')
        for i in range(1,10): add(f'rail-dot-{i}',f'section-box-{i}',f'section-number-{i}',f'section-title-{i}',f'topic-leader-{i}',f'topic-box-{i}',f'topic-text-{i}')
        add('paper-card-strip','paper-card-title','paper-card-fields','paper-card-note')
    elif base.startswith('Figure3_'):
        for pfx in ('llm-side','runtime','general-harness','general-ts-harness','task-specific-harness','paper-card'):
            add(*[n for n in ('%s-frame'%pfx,'%s-title'%pfx,'%s-modules'%pfx,'%s-tasks'%pfx,'%s-fields'%pfx,'%s-note'%pfx) if n])
        add('llm-runtime-link','llm-plus','nesting-note')
    elif base.startswith('Figure4_'):
        add('general-harness-core','core-title','core-subtitle','general-harness-note','general-harness-note-text')
        for i in range(1,8): add(f'dimension-{i}',f'dimension-title-{i}',f'dimension-body-{i}',f'dimension-link-{i}')
    elif base.startswith('Figure5_'):
        add('temporal-semantics-frame','temporal-semantics-title','gts-frame','gts-title','task-contract-frame','task-contract-title','semantics-to-gts','gts-to-task-contract','gts-criterion','gts-criterion-text')
        for i in range(1,6): add(f'gts-row-{i}',f'gts-row-title-{i}',f'gts-row-body-{i}')
        for i in range(1,5): add(f'task-contract-{i}',f'task-contract-title-{i}',f'task-contract-body-{i}')
        for i in range(1,4): add(f'temporal-semantics-{i}',f'temporal-semantics-title-{i}',f'temporal-semantics-body-{i}')
    elif base.startswith('Figure6_'):
        add('shared-lens','shared-lens-title','shared-lens-subtitle','shared-lens-rail')
        for i in range(1,8): add(f'shared-module-{i}',f'shared-module-text-{i}')
        for i in range(1,5):
            add(f'task-frame-{i}',f'shared-rail-drop-{i}',f'task-header-{i}',f'task-title-{i}',f'task-contract-{i}',f'task-contract-label-{i}')
            for j in range(1,5): add(f'task-item-{i}-{j}',f'task-item-text-{i}-{j}')
    elif base.startswith('Figure7_'):
        add('evaluation-layers','evaluation-layers-title','evaluation-layers-subtitle')
        for i in range(1,4): add(f'layer-{i}',f'layer-title-{i}',f'layer-body-{i}',f'layer-connector-{i}')
        add('episode-record','episode-title','episode-subtitle')
        for i in range(1,6): add(f'episode-step-{i}',f'episode-step-title-{i}',f'episode-step-body-{i}',f'episode-connector-{i}')
        for i in range(1,5): add(f'evidence-field-{i}',f'evidence-field-title-{i}',f'evidence-field-body-{i}')
    elif base.startswith('Figure8_'):
        add('open-problems-panel','open-problems-title','open-problems-subtitle')
        for i in range(1,6): add(f'problem-{i}',f'problem-title-{i}',f'problem-body-{i}',f'problem-layer-{i}',f'problem-layer-text-{i}')
        add('system-cases-panel','system-cases-title','system-cases-subtitle','paper-card-strip','paper-card-title')
        for i in range(1,4): add(f'case-{i}',f'case-title-{i}',f'case-layer-{i}',f'case-body-{i}')
        for i in range(1,5): add(f'paper-card-field-{i}',f'paper-card-field-text-{i}')
        add('case-rule')
    elif base.startswith('Figure_LLM_'):
        add('model-side-label','llm-side-rule','llm-side-rule-text')
        for i in range(1,6): add(f'node-{i}',f'node-title-{i}',f'node-body-{i}')
        add('selector-to-generator','selector-to-evol','generator-to-training-data','evol-to-training-data','data-to-training')
    elif base.startswith('Figure1_'):
        add('plot-surface','x-axis','y-axis','y-axis-title','x-axis-title')
    return specs

if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]
    print(group_pptx(src,dst,specs_for(src)))
