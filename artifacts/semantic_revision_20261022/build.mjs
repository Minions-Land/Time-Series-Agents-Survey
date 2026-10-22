import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const D=path.resolve('artifacts/semantic_revision_20261022');
await fs.mkdir(path.join(D,'.build'),{recursive:true});
const icons=JSON.parse(await fs.readFile(D+'/assets/icons.json','utf8'));
const C={ink:'#24272A',muted:'#626A6F',rule:'#D8DDDF',soft:'#F3F4F2',blue:'#3F6C85',blueP:'#EAF0F3',teal:'#328372',tealP:'#E9F2EE',rust:'#B76C4D',rustP:'#F7EDE7',plum:'#836780',plumP:'#F1ECF2',gold:'#AF853D'};
let P,S,G='base',id=0;
function nm(v){return G+'//'+v+'-'+(++id)}
function box(x,y,w,h,fill='none',stroke='none',sw=0,name='box',shadow=false){return S.shapes.add({geometry:'rect',name:nm(name),position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:sw,style:'solid'},...(shadow?{shadow:'1px 2px 4px #000000/10'}:{})});}
function text(t,x,y,w,h=28,size=21,{bold=false,color=C.ink,align='left',font='Arial',italic=false}={}){
 const a=box(x,y,w,h);a.text=t;a.text.insets=0;a.text.style={typeface:font,fontSize:size,bold,italic,color,alignment:align,verticalAlignment:'middle',wrap:false};return a;
}
function head(t,x,y,w,size=25){return text(t,x,y,w,34,size,{bold:true,font:'Comic Sans MS'});}
function line(points,color=C.ink,width=1.8,name='path',fill='none',close=false){
 const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);const x=Math.min(...xs),y=Math.min(...ys),w=Math.max(0.01,Math.max(...xs)-x),h=Math.max(0.01,Math.max(...ys)-y);
 const commands=points.map((p,i)=>({[i?'lineTo':'moveTo']:{x:p[0]-x,y:p[1]-y}}));if(close)commands.push({close:{}});
 return S.shapes.add({geometry:'custom',name:nm(name),position:{left:x,top:y,width:w,height:h},fill,line:{fill:color,width,style:'solid'},customPaths:[{width:w,height:h,commands}]});
}
function ellipse(x,y,w,h,fill,stroke='none',sw=0,name='dot'){return S.shapes.add({geometry:'ellipse',name:nm(name),position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:sw,style:'solid'}});}
function flow(points,color=C.blue,name='flow'){
 let a=line(points,color,2.7,name);a.shadow='0px 1px 2px #000000/10';
 const p=points.at(-1),q=points.at(-2),theta=Math.atan2(p[1]-q[1],p[0]-q[0]),L=8,W=4.3;
 line([p,[p[0]-L*Math.cos(theta)+W*Math.sin(theta),p[1]-L*Math.sin(theta)-W*Math.cos(theta)],[p[0]-L*Math.cos(theta)-W*Math.sin(theta),p[1]-L*Math.sin(theta)+W*Math.cos(theta)]],color,0.1,name+'-tip',color,true);
}
function icon(name,x,y,size=34,color=C.blue){
 const old=G;G=G+'/icon-'+name+'-'+id;
 for (const cmds of icons[name].paths) S.shapes.add({geometry:'custom',name:nm(name),position:{left:x,top:y,width:size,height:size},fill:'none',line:{fill:color,width:1.7,style:'solid'},customPaths:[{width:24,height:24,commands:cmds}]});
 G=old;
}
function tag(t,x,y,w,color=C.blue){box(x,y,w,27,C.blueP);text(t,x+7,y,w-14,27,16,{color,bold:true});}
function check(x,y,color=C.teal){line([[x,y+5],[x+5,y+10],[x+15,y]],color,2.6,'check');}
function cross(x,y){line([[x,y],[x+10,y+10]],C.rust,2.4);line([[x,y+10],[x+10,y]],C.rust,2.4);}
function curve(values,x,y,w,h,{col=C.ink,sw=2,min=0,max=1,name='series'}={}){
 return line(values.map((v,i)=>[x+w*i/(values.length-1),y+h*(1-(v-min)/(max-min))]),col,sw,name);
}
function axes(x,y,w,h,{ylabel='',xlabel='Time',labels=true}={}){
 line([[x,y],[x,y+h],[x+w,y+h]],'#8D969B',1.1,'axes');
 if(labels&&xlabel)text(xlabel,x+w-70,y+h+4,70,21,15,{align:'right',color:C.muted});
 if(ylabel)text(ylabel,x,y-24,w,20,15,{color:C.muted});
}
function bracket(x1,x2,y,color=C.blue,h=7){line([[x1,y-h],[x1,y],[x2,y],[x2,y-h]],color,1.7,'interval-bracket');}
function titleStep(n,t,x,w,ic,color=C.blue){ellipse(x,16,26,26,color);text(String(n),x,15,26,27,17,{color:'#FFFFFF',align:'center',bold:true});head(t,x+37,11,w-37,25);if(ic)icon(ic,x+w-35,15,28,color);}
function panelRule(x,y,w,color=C.rule){line([[x,y],[x+w,y]],color,1);}
function group(g,fn){const old=G;G=g;fn();G=old;}
async function begin(w,h){P=Presentation.create({slideSize:{width:w,height:h}});S=P.slides.add();S.background.fill='#FFFFFF';id=0;}
async function save(n,notes){S.speakerNotes.text=notes+'\nIcons: Lucide, ISC license, original source SVGs and license in assets/. All curves are schematic didactic examples, not experimental data.';await(await PresentationFile.exportPptx(P)).save(D+'/.build/Figure'+n+'_draft.pptx');}
const anchor=Array.from({length:63},(_,i)=>.23+.55*Math.exp(-(((i-19)/5.0)**2))+.31*Math.exp(-(((i-43)/5.5)**2))+.015*Math.sin(i*.9));

async function fig09(){
 await begin(1400,650);
 group('retrieval',()=>{
  titleStep(1,'Retrieve references',24,350,'list-filter');
  text('Target sequence x',35,65,300,25,21,{bold:true});axes(48,122,282,103,{ylabel:'Value'});curve(anchor,48,122,282,103);
  icon('list-filter',41,267,34);text('Similarity shortlist',88,264,245,30,21,{bold:true});
  flow([[181,246],[181,263]]);
  text('LLM relevance review',43,306,285,28,20);
  box(40,350,290,103,C.blueP,'none',0,'selected-reference',true);
  text('Selected neighbor',52,356,240,23,18,{bold:true,color:C.blue});
  curve(anchor.map((v,i)=>.88*v+.025*Math.sin(i*.3)),54,391,187,45);check(277,405);
  text('Reference set R',45,463,282,25,20,{bold:true});
 });
 group('augmentation',()=>{
  titleStep(2,'Construct positive views',397,521,'sliders-vertical',C.plum);
  text('Choose a transformation using x and R',412,65,485,27,21,{bold:true});
  icon('audio-lines',418,112,29,C.plum);text('Jittering',455,111,118,28,18);
  icon('crop',594,112,29,C.gold);text('Time masking',632,111,159,28,18);
  icon('shuffle',792,112,29,C.rust);text('Permutation',830,111,130,28,18);
  text('Example candidates',412,162,420,24,17,{color:C.muted});
  box(408,203,479,111,C.tealP,'none',0,'candidate-positive');
  text('A',422,218,30,25,21,{bold:true,color:C.teal});
  text('Small jitter',458,210,220,25,20,{bold:true});
  curve(anchor.map((v,i)=>v+.026*Math.sin(i*2.1)),458,249,266,50,{sw:2});
  text('Peak order\nretained',743,246,130,48,17,{color:C.muted});
  box(408,339,479,111,C.rustP,'none',0,'candidate-reject');
  text('B',422,354,30,25,21,{bold:true,color:C.rust});
  text('Block permutation',458,345,275,25,20,{bold:true});
  const perm=[...anchor.slice(32),...anchor.slice(0,32)];curve(perm,458,383,266,50);
  text('Peak order\nchanged',743,382,130,48,17,{color:C.muted});
  bracket(458,724,457,C.muted,5);text('Same time axis',515,464,180,22,15,{color:C.muted,align:'center'});
 });
 group('review',()=>{
  titleStep(3,'Review each view',947,420,'file-check-2',C.teal);
  icon('scan-eye',968,80,34,C.teal);text('Compare with x',1013,79,318,30,22,{bold:true});
  text('LLM judgment + rationale',968,126,370,25,20);
  check(972,248);text('“Correct”',1000,236,220,32,22,{bold:true,color:C.teal});
  text('Retain in memory M',1000,273,320,28,20);
  cross(975,385);text('“Error”',1000,372,220,32,22,{bold:true,color:C.rust});
  text('Refine retrieval',1000,409,300,28,20);
 });
 group('routes',()=>{
  flow([[337,401],[382,401],[382,236],[399,236]],C.blue,'references-inform-choice');
  flow([[893,257],[947,257]],C.teal,'candidate-A-to-review');
  flow([[893,394],[947,394]],C.rust,'candidate-B-to-review');
  flow([[1230,402],[1357,402],[1357,507],[17,507],[17,285],[34,285]],C.rust,'rejection-retrieval-loop');
  box(516,493,465,28,'#FFFFFF');text('Rejected view: repeat reference selection',516,493,465,28,18,{color:C.rust,align:'center'});
 });
 group('representation',()=>{
  box(24,544,1343,87,C.soft,'none',0,'representation-band',true);
  icon('combine',43,565,35,C.blue);head('Contrastive learning',92,561,283,24);
  text('x',400,568,50,35,24,{bold:true,align:'center'});text('+',452,568,27,35,25,{align:'center'});
  text('M ∪ R',491,568,125,35,24,{bold:true,align:'center'});
  text('Positive samples',489,603,165,20,15,{color:C.muted});
  flow([[640,587],[696,587]]);
  box(711,564,188,47,'#E0E8EB','#AABAC2',1,'encoder',true);text('Shared encoder',724,571,163,30,20,{bold:true,align:'center'});
  flow([[916,587],[968,587]]);icon('waypoints' in icons?'waypoints':'combine',984,565,34,C.plum);
  text('Learn representations',1032,557,310,30,21,{bold:true});text('Bring positive pairs together',1032,591,310,25,18,{color:C.muted});
 });
 await save('09','MERIT. Source: https://aclanthology.org/2025.findings-acl.1231/ Sections 3.2-3.5, equations 1-11, Figure 2. Coarse similarity retrieval then LLM relevance refinement; context-dependent strategy selection; review returns Correct/Error and rationale; accepted views enter M; rejected views restart retrieval; positives are M plus retrieved neighbors R. The two transformation outcomes are illustrative, not source-reported acceptance rules or results.');
}

async function fig13(){
 await begin(1400,600);
 group('question',()=>{
  head('Question and numerical input',24,13,480,25);icon('circle-help',25,63,33,C.plum);
  text('In which part does the anomaly occur?',72,61,472,33,23,{bold:true});
  text('Head, middle, or end?',72,100,420,27,20,{color:C.muted});
  const x=57,y=185,w=441,h=147;
  box(x+w/3,y,w/3,h,C.rustP);axes(x,y,w,h,{ylabel:'Value',xlabel:'Time'});
  const v=Array.from({length:110},(_,i)=>.22+.035*Math.sin(i*.9)+.62*Math.exp(-(((i-54)/3.2)**2)));curve(v,x,y,w,h,{sw:2.3});
  for(let j=0;j<3;j++){bracket(x+j*w/3+3,x+(j+1)*w/3-3,361,j===1?C.rust:C.muted);text(['Head','Middle','End'][j],x+j*w/3,368,w/3,25,18,{align:'center',bold:j===1,color:j===1?C.rust:C.muted});}
  text('Illustrative sequence',56,415,400,24,16,{color:C.muted});
 });
 group('reasoner',()=>{
  head('Iterative analysis',564,13,344,25);icon('route',566,67,32,C.blue);text('Reasoner',609,68,231,28,23,{bold:true});
  text('Choose the next analytical action',565,111,341,26,19);
  box(575,162,316,82,C.blueP,'none',0,'detect-operation',true);
  icon('scan',593,180,34,C.blue);text('Detect',641,172,210,27,22,{bold:true});text('Anomaly presence and interval',592,210,282,24,17);
  flow([[732,248],[732,278]]);
  box(575,286,316,101,C.soft,'none',0,'evidence-log',true);
  icon('clipboard-list',591,306,31,C.gold);text('Evidence log',635,297,218,27,21,{bold:true});
  text('Anomaly found in the middle',594,342,274,25,18);
 });
 group('verification',()=>{
  head('Evidence gate and answer',955,13,425,25);
  icon('list-check',961,67,31,C.teal);text('Required evidence',1006,67,330,30,22,{bold:true});
  check(966,128);text('has_anomaly = true',997,116,355,30,20);
  check(966,172);text('anomaly_segment = middle',997,160,360,30,20);
  panelRule(961,215,386);
  text('Both requirements covered',963,232,382,29,21,{bold:true,color:C.teal});
  flow([[1156,273],[1156,309]],C.teal,'complete-to-answer');
  box(962,320,385,78,C.tealP,'none',0,'answer',true);icon('circle-check-big',978,342,30,C.teal);text('Answer: middle',1024,339,295,36,25,{bold:true,color:C.teal});
 });
 group('routes',()=>{
  flow([[512,221],[560,221]],C.blue,'series-to-tool');flow([[899,337],[938,337],[938,194],[957,194]],C.blue,'logged-evidence-to-gate');
  line([[1348,194],[1375,194],[1375,461],[548,461],[548,231]],C.rust,2.7,'evidence-gap-return');
  S.shapes.add({geometry:'custom',name:nm('feedback-crossover'),position:{left:539,top:211,width:9,height:20},fill:'none',line:{fill:C.rust,width:2.7,style:'solid'},customPaths:[{width:9,height:20,commands:[{moveTo:{x:9,y:20}},{cubicBezTo:{x1:-3,y1:18,x2:-3,y2:2,x:9,y:0}}]}]});
  flow([[548,211],[548,91],[561,91]],C.rust,'evidence-gap-return-tip');
  box(677,446,381,30,'#FFFFFF');text('Missing evidence: select another action',677,446,381,30,18,{color:C.rust,align:'center'});
 });
 group('trace',()=>{
  panelRule(24,503,1325);
  icon('binary',29,533,29,C.blue);text('Native series',69,528,186,28,20,{bold:true});
  flow([[248,544],[291,544]]);icon('square-function',308,531,29,C.plum);text('Tool + arguments',348,528,232,28,20,{bold:true});
  flow([[590,544],[635,544]]);icon('table-properties',653,531,30,C.gold);text('Structured observation',694,528,306,28,20,{bold:true});
  flow([[1007,544],[1055,544]]);icon('list-check',1071,531,29,C.teal);text('Answer evidence',1113,528,243,28,20,{bold:true});
 });
 await save('13','TS-Agent: https://arxiv.org/abs/2510.07432. Sections 4.1-4.3, pp.4-6. The question and required predicates follow Section 4.3, MCQ_anomaly_location. Numerical waveform and middle outcome are explanatory examples. Analytical tools act on native series; observations accumulate in a log; critic and final gate compare evidence against required predicates. A missing predicate drives further action.');
}

async function fig14(){
 await begin(1400,670);
 group('policy',()=>{
  icon('route',29,24,34,C.plum);head('Generalist LLM',78,18,300,26);text('Task + context + observations',407,23,473,29,22,{color:C.muted});
  box(24,68,876,64,C.plumP,'none',0,'policy-lane',true);
  text('Select operation and parameters',43,86,404,30,22,{bold:true});
  flow([[446,100],[500,100]],C.plum);text('Use the returned evidence',525,86,345,30,22,{bold:true});
 });
 group('workspace',()=>{
  head('Numerical workspace',31,193,351,25);icon('binary',36,241,32,C.blue);
  text('Full-precision series',82,241,275,29,21,{bold:true});
  const sx=38,sy=289,cw=101,ch=37;
  for(let i=0;i<3;i++)for(let j=0;j<3;j++)box(sx+j*cw,sy+i*ch,cw,ch,i===0?'#DFE7EB':'#F4F6F5','#CED6DB',.8,'numerical-array');
  ['Time','Channel 1','Channel 2','t₁','x₁,₁','x₁,₂','t₂','x₂,₁','x₂,₂'].forEach((v,i)=>text(v,sx+(i%3)*cw+5,sy+Math.floor(i/3)*ch+5,cw-10,ch-10,17,{bold:i<3,align:'center'}));
  text('Windows and metadata remain addressable',37,419,334,48,18,{color:C.muted});
 });
 group('tools',()=>{
  head('Runtime-native tools',430,193,402,25);icon('square-function',436,241,33,C.gold);
  text('Execute directly on the workspace',484,240,376,30,21,{bold:true});
  [['crop','Slice',C.blue],['sliders-vertical','Transform',C.plum],['chart-spline','Analyze',C.teal]].forEach(([ic,t,c],i)=>{icon(ic,454+i*130,307,37,c);text(t,423+i*130,358,104,27,19,{align:'center',bold:true});});
  text('Compact structured observations',435,417,422,29,20,{color:C.blue,bold:true});
 });
 group('memory',()=>{
  box(930,17,445,453,C.soft,'none',0,'episodic-memory',true);
  head('Episodic memory',951,27,385,25);
  icon('fingerprint',951,91,35,C.blue);text('Signal key',1000,89,310,28,22,{bold:true});text('Shape and statistical structure',1000,123,345,25,18,{color:C.muted});
  icon('text-search',951,175,35,C.plum);text('Context key',1000,174,310,28,22,{bold:true});text('Task and textual context',1000,209,345,25,18,{color:C.muted});
  line([[1341,104],[1356,104],[1356,256],[1164,256]],C.teal,1.7,'match-both-keys');
  line([[1341,189],[1356,189]],C.teal,1.7,'context-key-join');
  flow([[1164,256],[1164,272]],C.teal);
  text('Retrieve a successful episode',953,283,394,31,21,{bold:true,color:C.teal});
  panelRule(951,330,396);
  icon('snowflake',956,350,34,C.blue);text('Snowstorm',1002,351,136,25,17);
  flow([[1137,367],[1165,367]],C.blue);icon('zap',1178,351,31,C.gold);text('Demand ↑',1220,351,126,25,18,{bold:true});
  text('Stored rationale and analytical trace',955,410,393,26,18,{color:C.muted});
 });
 group('interaction',()=>{
  flow([[505,137],[505,180]],C.plum,'operation-request');text('Operation + parameters',253,145,238,25,17,{color:C.plum,align:'right'});
  flow([[870,415],[892,415],[892,153],[742,153],[742,137]],C.blue,'observation-return');
  flow([[415,328],[365,328]],C.blue,'tools-read-workspace');
  flow([[926,306],[915,306],[915,100],[902,100]],C.teal,'memory-retrieval');
 });
 group('evolution',()=>{
  panelRule(25,492,1349);head('Experience-driven tool evolution',26,502,593,24);
  const xs=[32,372,704,1041];
  const items=[['clipboard-list','Executed traces','Cluster recurring procedures',C.blue],['code-xml','Candidate tool','Program + invocation description',C.plum],['flask-conical','Held-out tasks','Success rate exceeds threshold',C.rust],['package-check','Registered tool','Available to later episodes',C.teal]];
  items.forEach(([ic,h,b,c],i)=>{icon(ic,xs[i],561,34,c);text(h,xs[i]+49,554,266,31,22,{bold:true});text(b,xs[i]+49,594,269,46,18,{color:C.muted});if(i<3)flow([[xs[i]+284,578],[xs[i+1]-14,578]],C.blue,'promotion-step-'+i);});
  flow([[1344,552],[1344,515],[865,515],[865,385],[824,385]],C.teal,'registered-tools-return');
  box(990,500,292,26,'#FFFFFF');text('Add to the runtime tool set',990,500,292,26,17,{color:C.teal,align:'center'});
 });
 await save('14','TIMECLAW: Harnessing Generalist Agents for Contextualized Time Series. https://arxiv.org/abs/2606.05404 Sections 3.1-3.4, pp.4-5, Table 10. Policy specifies operation+parameters; tools operate on full-precision W and return compact observations. Signal and context keys retrieve successful trajectories with rationale. Candidate tools distilled from clustered traces are tested on held-out similar tasks and registered when success exceeds a threshold. Do not conflate with a separate TimeClaw exploratory-learning paper.');
}

async function fig04(){
 await begin(1400,685);
 const v=[.3,.4,.25,.44,.54,.34,.6,.49,.55,.69,.55,.67];
 group('grid',()=>{
  head('(a)',17,12,56,23);const left=170,top=76,cw=300,rh=98;
  const cols=[['Forecasting','chart-spline',C.blue],['Synthesis','combine',C.plum],['Diagnosis','scan-eye',C.rust],['Decision','route',C.teal]];
  cols.forEach(([t,ic,col],j)=>{icon(ic,left+cw*j+27,19,31,col);head(t,left+cw*j+70,14,226,24);});
  ['Data','Processing','Context','Validation'].forEach((t,i)=>{text(t,29,top+i*rh+36,135,27,21,{bold:true});box(left,top+i*rh,4*cw,rh,i%2===0?'#FAFAF8':'#FFFFFF','#DEE2E3',.7);});
  for(let j=0;j<4;j++)line([[left+j*cw,top],[left+j*cw,top+rh*4]],C.rule,.7);
  function cell(r,c,fn){group('grid/cell-'+r+'-'+c,()=>fn(left+c*cw,top+r*rh));}
  cell(0,0,(x,y)=>{curve(v,x+17,y+27,132,43);text('History',x+169,y+35,121,28,20);});
  cell(0,1,(x,y)=>{icon('table-properties',x+27,y+27,43,C.plum);text('Samples',x+169,y+35,121,28,20);text('x₁  x₂  …',x+82,y+34,76,27,16,{color:C.muted});});
  cell(0,2,(x,y)=>{icon('audio-lines',x+27,y+27,43,C.rust);text('Streams',x+169,y+35,121,28,20);text('A   B   C',x+85,y+35,78,27,16,{color:C.muted});});
  cell(0,3,(x,y)=>{icon('warehouse',x+26,y+24,45,C.teal);text('State',x+169,y+35,121,28,20);text('stock, cost',x+82,y+36,79,27,14,{color:C.muted});});
  cell(1,0,(x,y)=>{box(x+91,y+22,56,49,C.blueP);curve(v.slice(0,8),x+18,y+29,73,39);curve([.49,.55,.69,.55,.67],x+91,y+22,56,49);bracket(x+91,x+147,y+77,C.blue,4);text('Horizon',x+169,y+35,121,28,20);});
  cell(1,1,(x,y)=>{icon('shuffle',x+26,y+28,39,C.plum);flow([[x+77,y+47],[x+102,y+47]],C.plum);icon('crop',x+113,y+28,38,C.gold);text('Transforms',x+169,y+35,121,28,19);});
  cell(1,2,(x,y)=>{box(x+71,y+20,41,54,C.rustP);curve([.2,.3,.23,.25,.4,.8,.65,.36,.2,.29,.24],x+19,y+23,130,48);bracket(x+71,x+112,y+78,C.rust,5);text('Intervals',x+169,y+35,121,28,20);});
  cell(1,3,(x,y)=>{icon('split' in icons?'split':'route',x+27,y+27,41,C.teal);icon('package-check',x+104,y+27,41,C.gold);flow([[x+75,y+49],[x+97,y+49]],C.teal);text('Actions',x+169,y+35,121,28,20);});
  cell(2,0,(x,y)=>{icon('calendar-clock',x+25,y+26,43,C.blue);icon('milestone',x+104,y+27,41,C.gold);text('Events',x+169,y+35,121,28,20);});
  cell(2,1,(x,y)=>{icon('fingerprint',x+27,y+27,42,C.plum);flow([[x+79,y+48],[x+102,y+48]],C.plum);icon('text-search',x+111,y+27,40,C.blue);text('References',x+169,y+35,127,28,19);});
  cell(2,2,(x,y)=>{icon('clipboard-list',x+27,y+27,42,C.rust);icon('milestone',x+107,y+27,40,C.gold);text('Incidents',x+169,y+35,121,28,20);});
  cell(2,3,(x,y)=>{icon('route',x+27,y+27,42,C.teal);icon('text-search',x+107,y+27,40,C.plum);text('Experience',x+169,y+35,127,28,19);});
  cell(3,0,(x,y)=>{box(x+97,y+24,49,46,'#EBEDEA');flow([[x+19,y+51],[x+148,y+51]],C.blue);line([[x+97,y+21],[x+97,y+75]],C.ink,1.6);text('t₀',x+86,y+72,31,20,14,{align:'center'});text('Cutoff',x+169,y+35,121,28,20);});
  cell(3,1,(x,y)=>{icon('scan-eye',x+24,y+24,44,C.plum);check(x+112,y+40,C.teal);text('Fidelity',x+169,y+35,121,28,20);});
  cell(3,2,(x,y)=>{icon('table-properties',x+26,y+27,42,C.rust);flow([[x+78,y+48],[x+100,y+48]],C.rust);icon('file-check-2',x+110,y+27,40,C.teal);text('Evidence',x+169,y+35,121,28,20);});
  cell(3,3,(x,y)=>{box(x+30,y+31,112,29,C.tealP);line([[x+30,y+24],[x+30,y+67]],C.teal,1.8);line([[x+142,y+24],[x+142,y+67]],C.teal,1.8);ellipse(x+88,y+40,10,10,C.ink);text('Constraints',x+169,y+35,127,28,19);});
 });
 group('workflow',()=>{
  head('(b)',17,488,56,23);const xs=[83,417,752,1087];
  ['Execute','Prepare','Forecast','Decide'].forEach((t,i)=>head(t,xs[i],490,274,24));
  icon('code-xml',88,552,42,C.blue);flow([[143,573],[182,573]],C.blue);icon('square-function',199,552,42,C.gold);
  icon('calendar-clock',421,549,42,C.blue);flow([[476,573],[514,573]],C.blue);icon('table-properties',530,550,42,C.teal);
  const x=744,y=542;curve(v.slice(0,8),x,y+16,104,57);box(x+105,y+3,94,71,C.blueP);line([[x+105,y],[x+105,y+82]],C.ink,1.2,'forecast-origin');
  line([[x+105,y+39],[x+127,y+25],[x+155,y+12],[x+199,y+5],[x+199,y+70],[x+155,y+61],[x+127,y+48]],'none',0,'prediction-range','#D8E3E9',true);
  curve([.49,.59,.58,.7,.72],x+105,y+3,94,71,{sw:2.1});
  text('History',x+14,y+85,85,21,15,{align:'center',color:C.muted});text('Forecast',x+108,y+85,94,21,15,{align:'center',color:C.muted});
  icon('warehouse',1092,551,42,C.teal);flow([[1148,573],[1182,573]],C.teal);icon('package-check',1201,551,42,C.rust);
  [['General Harness',83,261],['General Time-Series Harness',391,323],['Task-Specific Harness',729,286],['Task-Specific Harness',1063,286]].forEach(([t,x,w])=>text(t,x,646,w,25,18,{align:'center',color:C.muted}));
  [288,626,990].forEach(x=>flow([[x,573],[x+79,573]],C.blue,'workflow-step'));
 });
 await save('04','Survey task-function grid. Task columns and functional annotations are cross-cutting views of the same module taxonomy, not additional mutually exclusive classifications. Source examples: TimeSeriesScientist, SAGE-AD, MERIT, FinMem as cited in manuscript. Bottom demand-planning workflow illustrates general execution, shared temporal preparation, and task-specific forecasting and inventory. Filled regions mark future horizon, candidate interval, information unavailable after t0, or admissible action range. Curves are illustrative.');
}

const fns={'04':fig04,'09':fig09,'13':fig13,'14':fig14};
for(const n of process.argv.slice(2).length?process.argv.slice(2):['04','09','13','14']){await fns[n]();console.log('draft',n);}
