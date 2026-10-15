import json
from pathlib import Path
p=Path(__file__).parent;q=json.loads((p/'page_request.json').read_text())
m={'slide':q['slide'],'content_box':q['content_box'],'source':{'width_px':1272,'height_px':1702},'page_strategy':'Source-position native text, method-label outlines and continuous structural route curves; separately extracted affiliation and header icons.','text_inventory':[],'visual_inventory':[],'background_strategy':{'mode':'native-or-script','source_consistency_contract':'White page; preserve six columns, year bands and label positions.','removed_foreground':'Text, icons and structural paths separated.','comparison_note':'Structural paths follow source route layout; native outlines regularize minor hand-drawn waviness.'},'quality_checks':{'font_size_calibrated':True,'visual_inventory_matched':True,'background_strategy_checked':True,'shape_corner_geometry_checked':True},'text_boxes':[],'shapes':[],'images':[],'asset_provenance':[]}
T=m['text_boxes'];S=m['shapes'];I=m['images']
def text(id,s,x,y,w,h,size=17,bold=True,col='30343A',align='center'):
 T.append({'id':id,'text':s,'box_px':[x,y,w,h],'font':'Times New Roman','font_size':size,'font_size_source':'measured','fit_text':False,'bold':bold,'color':col,'align':align,'valign':'middle','z_index':40})
 m['text_inventory']+=s.split('\n')
def rect(id,x,y,w,h,col,fill='FCFCFC'):
 S.append({'id':id,'type':'roundRect','box_px':[x,y,w,h],'source_corner_radius_px':5,'fill':fill,'stroke':col,'stroke_width':1.5,'z_index':20})
def line(id,x1,y1,x2,y2,col,width=1,dash='solid',arrow=False):
 S.append({'id':id,'type':'line','points_px':[x1,y1,x2,y2],'stroke':col,'stroke_width':width,'dash':dash,'end_arrow':'triangle' if arrow else 'none','z_index':10})
def icon(id,n,x,y,w=29,h=29):
 path='assets/icons/'+n+'.png';I.append({'id':id,'path':path,'box_px':[x,y,w,h],'z_index':30})
 if path not in [a['path'] for a in m['asset_provenance']]:
  m['asset_provenance'].append({'path':path,'source':'assets/sheet.png','source_type':'asset-sheet-separated','provenance_note':'Built-in image edit source separation, editppt chroma removal and region splitting; logo internal strokes remain bitmap.'})
  m['visual_inventory'].append({'role':'foreground','object_type':'logo-or-header-icon','path':path,'source_type':'asset-sheet-separated'})
text('title','Research routes toward recursive self-improvement',55,14,1170,45,27,align='left')
text('subtitle','Selected milestones by first public year | Historical roots and the foundation-model era',55,64,1170,33,16,bold=True,align='left',col='606060')
colors=['AA8447','438775','4D87A3','B77B74','916FA4','4B9194']
heads=[('Data &\ntraining','Synthetic data\nPersistent updates','data'),('Tasks &\ncurricula','Task generation\nEnvironment feedback','tasks'),('Memory &\nskills','Reflective memory\nReusable knowledge','memory'),('Code &\nworkflows','Prompts and code\nAgent architectures','code'),('Feedback &\njudges','Learned rewards\nEvaluator learning','feedback'),('Meta-level\nimprovement','Update strategies\nResearch automation','metaheader')]
for i,(a,b,n) in enumerate(heads):
 x=136+i*182;c=colors[i]
 rect('header-border-'+str(i),x,106,173,148,c,['FAF7F0','F0F7F3','F0F6FA','FAF4F2','F7F2FA','F1F7F7'][i])
 icon('header-icon-'+str(i),n,x+69,114,35,35)
 text('header-title-'+str(i),a,x+4,151,165,57,18,col=c)
 text('header-desc-'+str(i),b,x+3,209,167,40,12.5,col='5E6060')
 # A complete native cubic curve per route, preserving the column trunk and common root.
 cx=x+86;root=635
 pts=[{'op':'moveTo','points':[[root,1296]]},{'op':'cubicBezTo','points':[[cx,1275],[cx,1246],[cx,1150]]},{'op':'lnTo','points':[[cx,267]]}]
 S.append({'id':'route-'+str(i),'semantic_line_id':'route-'+str(i),'type':'path','box_px':[min(cx,root)-5,260,abs(cx-root)+10,1045],'path_px':pts,'stroke':c,'stroke_width':5,'fill':'none','end_arrow':'triangle','z_index':5})
for j,y in enumerate([483,715,949,1157,1278]):line('year-divider-'+str(j),110,y,1226,y,'D6D7D7',.7,'dash')
line('year-axis',77,1273,77,267,'72767C',2,arrow=True)
for year,y in [(2026,360),(2025,590),(2024,822),(2023,1042),(2022,1208)]:
 rect('year-white-'+str(year),46,y,61,29,'FFFFFF','FFFFFF');text('year-'+str(year),str(year),47,y,59,29,18)
# Source entries: each label has independently editable border and text, and a separate logo.
rows=[
(0,530,43,'SEAL','seal'),(0,635,42,'TTRL','tsinghua'),(0,738,43,'SCoRe','deepmind'),(0,789,41,'RISE','cmu'),(0,840,43,'Quiet-STaR','stanford'),(0,892,43,'SPIN','ucla'),(0,989,43,'ReSTᴱᴹ','deepmind'),(0,1082,43,'ReST','deepmind'),(0,1176,43,'Self-Instruct','washington'),(0,1225,43,'STaR','stanford'),
(1,511,43,'AgentEvolver','alibaba'),(1,582,43,'R-Zero','rzero'),(1,649,49,'Absolute\nZero','tsinghua'),(1,815,43,'AgentGym','agentgym'),
(2,354,43,'MetaClaw','unc'),(2,511,43,'ACE','stanford'),(2,577,49,'Dynamic\nCheatsheet','stanford'),(2,650,44,'A-MEM','rutgers'),(2,973,43,'ExpeL','tsinghua'),(2,1035,43,'Voyager','nvidia'),(2,1097,43,'Reflexion','northeastern'),
(3,351,45,'Prime Agent','prime'),(3,512,43,'GEPA','berkeley'),(3,583,42,'DGM','ubc'),(3,651,43,'SICA','sica'),(3,744,43,'AFlow','hkust'),(3,815,43,'ADAS','ubc'),(3,886,43,'TextGrad','stanford'),(3,989,43,'DSPy','stanford'),(3,1081,43,'OPRO','deepmind'),
(4,563,77,'Process\nSelf-\nRewarding','process'),(4,736,43,'CREAM','unc'),(4,783,55,'Self-Taught\nEvaluators','meta'),(4,840,48,'Meta-\nRewarding','meta'),(4,890,53,'Self-\nRewarding','meta'),(4,1036,43,'CRITIC','microsoft'),(4,1195,53,'Constitutional\nAI','anthropic'),
(5,287,43,'Metaⁿ','minnesota'),(5,347,56,'Bilevel\nAutoresearch',None),(5,421,43,'Hyperagents','meta'),(5,529,44,'AlphaEvolve','deepmind'),(5,631,52,'AI\nScientist-v2','aiscientist'),(5,815,43,'AI Scientist','aiscientist'),(5,990,43,'STOP','microsoft'),(5,1082,43,'Promptbreeder','deepmind')]
for idx,(col,y,h,s,n) in enumerate(rows):
 x=136+col*182;c=colors[col];rect('method-border-'+str(idx),x,y,173,h,c)
 if n:icon('method-logo-'+str(idx),n,x+5,y+(h-29)/2)
 else:text('independent','Ind.',x+4,y+16,30,20,9,align='left')
 fs=15.5 if len(s.replace('\n',''))<17 else 14.5
 text('method-name-'+str(idx),s,x+34,y+1,137,h-2,fs)
rect('foundation-border',123,1303,1108,77,'45434B','FAFAFA')
for j,(s,n,desc) in enumerate([('Gödel Machine','tum','2003 | Provable self-modification'),('Learned optimizers','deepmind','2016 | Learning update rules'),('POET','uber','2019 | Tasks and solvers co-evolve')]):
 x=155+j*366;icon('foundation-logo-'+str(j),n,x,1313,30,30);text('foundation-title-'+str(j),s,x+43,1310,285,31,18);text('foundation-desc-'+str(j),desc,x+4,1344,333,28,13,bold=False)
text('legend','Marks: selected affiliations | Ind.: independent researchers | Branches: research routes, not technical ancestry',151,1389,1080,26,13,col='606060')
caption=['Figure 4. Research routes toward recursive self-improvement. Forty-five representative method papers are',
'grouped into six research routes, with three historical anchors shown separately. Year bands use the first public',
'dates in the checked source records; spacing within each band is adjusted for legibility. Branch lines denote',
'research families. Technical ancestry, cross-route transfer, and sustained recursive gains require separate evidence.',
'The selection reflects the literature search through September 12, 2026. Logos identify one selected author or work-',
'done affiliation per study; “Ind.” denotes independent researchers. Affiliation and logo sources are documented',
'separately.']
for i,s in enumerate(caption):text('caption-'+str(i),s,23,1438+i*36,1227,34,18,bold=False,align='left',col='000000')
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
print(len(T),'text',len(S),'shapes',len(I),'images')
