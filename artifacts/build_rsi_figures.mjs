import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
const SKILL_DIR='/Users/mjm/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const workspaceDir='/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey';
const buildDir=path.join(workspaceDir,'.ppt-build');
const finalPath=path.join(workspaceDir,'artifacts','TimeSeriesAgent_Figures_RSI_v2.pptx');
const {resolvePresentationFont, finalizePresentation}=await import(pathToFileURL(path.join(SKILL_DIR,'container_tools/artifact_tool_utils.mjs')).href);
const family=resolvePresentationFont({fontFamily:'Arial'});
const p=Presentation.create({slideSize:{width:1280,height:720}});
const C={navy:'#24324A',ink:'#303A4B',muted:'#687386',line:'#3D4652',yellow:'#F4F0C9',green:'#DDEEDC',blue:'#D9EEF0',purple:'#E6E0F2',white:'#FFFFFF',gold:'#B77F2B',teal:'#438B86',violet:'#78639F',red:'#B86659'};
function addText(slide,x,y,w,h,txt,size=18,color=C.ink,bold=false,italic=false,align='left'){
 const s=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}}); s.text=txt; s.text.style={typeface:family,fontSize:size,color,bold,italic,align,verticalAlign:'mid',autoFit:'shrink'}; return s;
}
function addBox(slide,x,y,w,h,fill,line=C.line,opts={}){
 const geometry=opts.geometry||'roundRect';
 const cfg={geometry,position:{left:x,top:y,width:w,height:h},fill,line:{style:opts.dash?'dashed':'solid',fill:line,width:opts.lw||1.4}};
 if (geometry==='roundRect' || geometry==='rect' || geometry==='textbox') cfg.borderRadius='rounded-lg';
 return slide.shapes.add(cfg);
}
function connector(slide,a,b,color=C.line,dash=false,arrow=true){return slide.shapes.connect(a,b,{kind:'straight',fromSide:'right',toSide:'left',line:{style:dash?'dashed':'solid',fill:color,width:2},head:arrow?{type:'arrow',width:'sm',length:'sm'}:{type:'none'}})}
// Slide 1: organization map
{
 const s=p.slides.add(); s.background.fill='#FFFFFF';
 addText(s,58,28,1160,42,'Organization of the survey',34,C.navy,true,false,'center');
 addText(s,58,73,1160,28,'Sections follow the construction of a Time-Series Agent and the evidence needed to evaluate it.',16,C.muted,false,true,'center');
 // left spine
 const spine=addBox(s,120,136,4,510,C.line,C.line,{geometry:'rect',lw:0});
 const rows=[
  ['§ 1','Introduction','Scope, motivation, and central questions',C.yellow,C.gold],
  ['§ 2','What Is a Time-Series Agent?','Construction layers and paper-card unit',C.yellow,C.gold],
  ['§ 3','LLM-Side Contributions','Temporal representation, alignment, reasoning',C.purple,C.violet],
  ['§ 4','General Harness','Seven reusable runtime dimensions',C.blue,C.teal],
  ['§ 5','General Time-Series Harness','Temporal contracts that transfer across tasks',C.green,C.teal],
  ['§ 6','Task-Specific Harness','Forecasting, augmentation, anomaly, decision support',C.green,C.teal],
  ['§ 7','Infrastructure and Benchmarks','Episodes, traces, tools, and task outcomes',C.blue,C.teal],
  ['§ 8','Open Problems and Case Studies','Where modules and evaluation remain incomplete',C.purple,C.violet],
  ['§ 9','Conclusion','A reusable map for future systems',C.purple,C.violet],
 ];
 const sectionShapes=[]; const topicShapes=[];
 rows.forEach((r,i)=>{const y=112+i*57; const dot=addBox(s,113,y+22,14,14,r[4],r[4],{geometry:'ellipse',lw:0}); const b=addBox(s,148,y,420,47,r[3],r[4],{dash:true,lw:1.4}); addText(s,168,y+5,54,35,r[0],16,C.ink,true); addText(s,222,y+4,325,37,r[1],18,C.ink,true,false,'center'); sectionShapes.push(b); const t=addBox(s,612,y,570,47,r[3],r[4],{lw:1.1}); addText(s,632,y+6,530,35,r[2],14,C.ink,false,false,'left'); topicShapes.push(t); const c=connector(s,b,t,r[4],false,false);});
 addBox(s,20,250,108,165,C.blue,C.teal,{dash:true,lw:1.3}); addText(s,30,275,88,90,'Time-Series\nAgent\nSurvey',21,C.navy,true,false,'center'); addText(s,30,367,88,32,'reader\'s map',12,C.muted,false,true,'center');
 // connect label to spine
 const root=addBox(s,94,326,22,4,C.teal,C.teal,{geometry:'rect',lw:0});
 addBox(s,148,666,1034,35,C.white,C.navy,{lw:1.4}); addText(s,168,672,990,23,'Paper card fields: claim  ·  evidence locator  ·  module layer  ·  task family  ·  BibTeX  ·  review status',13,C.navy,true,false,'center');
 s.speakerNotes.textFrame.setText('Figure synthesized for this survey. The visual organization follows the survey sections and the paper-card schema. The layout style is adapted from the user-supplied Recursive Self-Improvement survey reference.');
}
// Slide 2: GTS landscape
{
 const s=p.slides.add(); s.background.fill='#FFFFFF';
 addText(s,58,28,1160,42,'The General Time-Series Harness landscape',32,C.navy,true,false,'left');
 addText(s,58,73,1160,28,'Reusable temporal obligations sit between a general runtime and a task contract.',16,C.muted,false,true,'left');
 // left legend
 addText(s,64,132,180,28,'Read from the center outward',14,C.muted,false,true,'left');
 addBox(s,70,184,190,64,C.yellow,C.gold,{lw:1.2}); addText(s,86,198,158,24,'Temporal objects',16,C.gold,true,false,'center'); addText(s,86,222,158,16,'time, window, horizon, unit',11,C.muted,false,false,'center');
 addBox(s,70,266,190,64,C.green,C.teal,{lw:1.2}); addText(s,86,280,158,24,'Temporal operations',16,C.teal,true,false,'center'); addText(s,86,304,158,16,'align, aggregate, resample, split',11,C.muted,false,false,'center');
 addBox(s,70,348,190,64,C.blue,C.teal,{lw:1.2}); addText(s,86,362,158,24,'Temporal evidence',16,C.teal,true,false,'center'); addText(s,86,386,158,16,'provenance, availability, revision',11,C.muted,false,false,'center');
 // central bands
 addBox(s,300,116,620,470,C.white,C.navy,{lw:1.8}); addText(s,330,132,560,28,'Reusable across time-series tasks',20,C.navy,true,false,'center');
 const bands=[['Interface','as-of time · horizon · frequency · channels',C.yellow,C.gold],['Memory & context','point-in-time state · provenance · event history',C.green,C.teal],['Tools & execution','temporal query · forecasting model · simulator',C.blue,C.teal],['Control & verification','chronology guard · numerical check · revision',C.purple,C.violet],['Planning & coordination','workflow · delegation · review · stopping',C.green,C.teal]];
 bands.forEach((r,i)=>{const y=182+i*72; const b=addBox(s,345,y,530,51,r[2],r[3],{lw:1.2}); addText(s,365,y+5,175,24,r[0],16,r[3],true); addText(s,545,y+5,305,35,r[1],12,C.ink,false,false,'center');});
 // right task contracts
 addBox(s,963,116,250,470,C.white,C.teal,{lw:1.5}); addText(s,985,132,206,28,'Task contracts',20,C.teal,true,false,'center');
 const tasks=[['Forecasting','origin, horizon, calibration'],['Augmentation','fidelity, diversity, utility'],['Anomaly diagnosis','event, window, cause'],['Decision support','action, cost, uncertainty']];
 tasks.forEach((r,i)=>{const y=190+i*88; const b=addBox(s,985,y,206,60,C.green,C.teal,{lw:1.1}); addText(s,996,y+6,184,22,r[0],14,C.teal,true,false,'center'); addText(s,996,y+31,184,20,r[1],10,C.muted,false,false,'center'); connector(s,b,addBox(s,875,y+27,28,4,C.teal,C.teal,{geometry:'rect',lw:0}),C.teal,false,true);});
 // bottom rule
 addBox(s,300,615,913,55,C.white,C.navy,{lw:1.4}); addText(s,320,626,873,28,'A temporal mechanism is GTS when its contract survives a change of downstream task.',15,C.navy,true,false,'center');
 s.speakerNotes.textFrame.setText('Figure synthesized from the seven-dimension General Harness vocabulary and the temporal obligations discussed in Section 5. The layout is adapted from the layered landscape figures in the user-supplied RSI survey reference.');
}
// Slide 3: research routes
{
 const s=p.slides.add(); s.background.fill='#FFFFFF';
 addText(s,58,24,1160,42,'Research routes in Time-Series Agent systems',32,C.navy,true,false,'left');
 addText(s,58,67,1160,28,'Representative module contributions by first public year; placement follows the paper-card ledger.',16,C.muted,false,true,'left');
 const cols=[['LLM side',C.violet,C.purple,['Time-LLM 2024','LLM4TS 2024','ChatTS 2024','TimeMaster 2025']],['General Harness',C.teal,C.blue,['TradingAgents 2024','TS-Agent 2025','AION 2026','TimeClaw 2026']],['Temporal grounding',C.gold,C.yellow,['TimeCAP 2025','TimeART 2026','TFRBench 2026','TSQBench 2026']],['Forecasting',C.red,'#F3E2DE',['TimeSeriesScientist 2025','ForecastCompass 2026','FinArena 2025','CastFlow 2026']],['Anomaly',C.teal,C.green,['Argos 2025','LEMAD 2025','AnomaMind 2026','TraceBench 2026']],['Decision support',C.violet,C.purple,['FinCon 2024','CoLLMLight 2026','ClimateAgent 2025','Smart Energy 2026']]];
 const x0=110, gap=17, cw=177, top=135; const yearYs=[210,315,420,525]; const yearLabs=['2024','2025','2026','Current'];
 cols.forEach((c,j)=>{const x=x0+j*(cw+gap); addBox(s,x,110,cw,65,c[2],c[1],{lw:1.4}); addText(s,x+8,123,cw-16,28,c[0],15,c[1],true,false,'center'); addText(s,x+8,151,cw-16,16,'module route',10,C.muted,false,true,'center'); const spine=addBox(s,x+cw/2-2,185,4,390,c[1],c[1],{geometry:'rect',lw:0}); c[3].forEach((label,i)=>{const y=yearYs[i]; const b=addBox(s,x+12,y,cw-24,42,c[2],c[1],{lw:1.0}); addText(s,x+18,y+4,cw-36,32,label,11,C.ink,true,false,'center');});});
 yearLabs.forEach((lab,i)=>{addText(s,48,yearYs[i]+8,52,26,lab,12,C.muted,true,false,'right'); const l=addBox(s,90,yearYs[i]+21,1120,2,'#D7DCE4','#D7DCE4',{geometry:'rect',lw:0});});
 addBox(s,110,610,1100,58,C.white,C.navy,{lw:1.4}); addText(s,135,620,1050,22,'The same work can occupy more than one route because the ledger records module-level contributions.',15,C.navy,true,false,'center'); addText(s,135,643,1050,18,'Years are taken from the maintained bibliography and paper-card records.',11,C.muted,false,true,'center');
 s.speakerNotes.textFrame.setText('Representative works and dates are drawn from the maintained paper-classification ledger in this survey. Names are used as ledger labels; the chart is a synthesis rather than a citation-priority ranking.');
}
await fs.mkdir(path.dirname(finalPath),{recursive:true});
const candidate=path.join(buildDir,'candidate-rsi-figures.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
for (let i=0;i<p.slides.items.length;i++) { const blob=await p.export({slide:p.slides.items[i],format:'png',scale:2}); await fs.writeFile(path.join(buildDir,`figure-${i+1}.png`),new Uint8Array(await blob.arrayBuffer())); }
const result=await finalizePresentation({workspaceDir,candidatePath:candidate,finalPath,pythonExecutable:'/Users/mjm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],fontPolicy:{basis:'design',families:[family]},verifyArtifactToolImport:true,receiptPath:path.join(buildDir,'rsi-figures-v2.validation.json')});
console.log(JSON.stringify(result));
