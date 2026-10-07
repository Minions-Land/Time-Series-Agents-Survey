import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
const workspaceDir='/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey';
const SKILL_DIR='/Users/mjm/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const buildDir=path.join(workspaceDir,'.ppt-build','figure7-rsi-style');
const outDir=path.join(workspaceDir,'artifacts','active');
await fs.mkdir(buildDir,{recursive:true}); await fs.mkdir(outDir,{recursive:true});
const {resolvePresentationFont}=await import(pathToFileURL(path.join(SKILL_DIR,'container_tools/artifact_tool_utils.mjs')).href);
const family=resolvePresentationFont({fontFamily:'Times New Roman'});
const C={navy:'#24324A',muted:'#687386',line:'#D4DAE2',teal:'#438B86',tealFill:'#D9EEF0',purple:'#78639F',purpleFill:'#E6E0F2',gold:'#B77F2B',goldFill:'#F4F0C9',green:'#5D9477',greenFill:'#DDEEDC',salmon:'#B86659',salmonFill:'#F3E2DE',white:'#FFFFFF'};
const p=Presentation.create({slideSize:{width:1600,height:900}}); const s=p.slides.add(); s.background.fill='#FFFFFF';
function txt(x,y,w,h,t,size=20,color=C.navy,b=false,it=false,align='left',name){const q=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});q.text=t;q.text.style={typeface:family,fontSize:size,color,bold:b,italic:it,alignment:align,autoFit:'shrinkTextOnOverflow'};return q}
function box(x,y,w,h,fill,line=C.line,r=16,dash=false,name){return s.shapes.add({geometry:'roundRect',name,position:{left:x,top:y,width:w,height:h},fill,line:{style:dash?'dashed':'solid',fill:line,width:2},borderRadius:r})}
function line(x,y,w,h,color=C.line,width=3,name){return s.shapes.add({geometry:'line',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:color,width}})}
function arrow(x,y,w,h,color=C.navy,name){return s.shapes.add({geometry:'line',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:color,width:3}})}
function panel(x,y,w,h,title,sub,fill,accent,prefix){box(x,y,w,h,fill,accent,20,true,`${prefix}-panel`);txt(x+22,y+18,w-44,30,title,21,accent,true,false,'left',`${prefix}-title`);txt(x+22,y+52,w-44,25,sub,14,C.muted,false,true,'left',`${prefix}-subtitle`)}
function item(x,y,w,h,title,body,fill,accent,name){box(x,y,w,h,fill,accent,12,false,`${name}-box`);txt(x+14,y+13,w-28,24,title,16,accent,true,false,'left',`${name}-title`);txt(x+14,y+42,w-28,h-48,body,13,C.navy,false,false,'left',`${name}-body`)}
// title and subtitle
 txt(78,38,1440,48,'Infrastructure and benchmark coverage',35,C.navy,true,false,'left','figure-title');
 txt(80,88,1430,28,'A benchmark must expose the data, tools, evidence, and outputs that make an Agent episode reproducible.',18,C.muted,false,true,'left','figure-subtitle');
// left sources and skills
panel(70,170,360,470,'Inputs and skills','what the episode can access',C.tealFill,C.teal,'inputs');
item(100,250,300,80,'Data sources','datasets · repositories · event context',C.white,C.teal,'data-sources');
item(100,360,300,80,'Skill simulators','data handling · tuning · code repair',C.white,C.teal,'skill-simulators');
item(100,470,300,80,'Task contract','horizon · authority · output format',C.white,C.teal,'task-contract');
// middle challenge stack
panel(485,170,470,470,'Challenge suite','shared interface for different Agents',C.purpleFill,C.purple,'challenges');
item(515,250,410,82,'Description','task statement and temporal scope',C.white,C.purple,'description');
item(515,355,410,82,'Resources','tools, APIs, models, and versions',C.white,C.purple,'resources');
item(515,460,410,82,'Graders','quantitative metrics and trace review',C.white,C.purple,'graders');
// right outputs
panel(1010,170,500,470,'Outputs and evidence','what a benchmark records',C.greenFill,C.green,'outputs');
item(1040,250,210,84,'Prediction files','point or probabilistic output',C.white,C.green,'prediction');
item(1270,250,210,84,'Model artifacts','weights, plots, intermediate state',C.white,C.green,'artifacts');
item(1040,365,210,84,'Tool trace','calls, failures, execution time',C.white,C.green,'trace');
item(1270,365,210,84,'Evidence log','checks, revisions, provenance',C.white,C.green,'evidence');
item(1155,480,210,84,'Code and config','replayable environment',C.white,C.green,'code');
// arrows and flow rail
arrow(430,405,55,1,C.teal,'inputs-to-challenges'); arrow(955,405,55,1,C.purple,'challenges-to-outputs');
line(125,690,1350,1,C.line,3,'evaluation-rail');
// lower evaluation blocks
item(110,720,390,95,'Quantitative evaluation','accuracy · error · calibration · runtime',C.goldFill,C.gold,'quantitative');
item(605,720,390,95,'Qualitative evaluation','trace quality · evidence grounding · revision',C.salmonFill,C.salmon,'qualitative');
item(1100,720,390,95,'Holistic score','task outcome + executable artifact + episode record',C.purpleFill,C.purple,'holistic');
line(500,767,105,1,C.line,2,'quant-to-qual'); line(995,767,105,1,C.line,2,'qual-to-holistic');
txt(110,842,1380,24,'The unit of evaluation is an episode: a result is interpretable only when its temporal and operational evidence can be replayed.',16,C.navy,true,false,'center','figure-conclusion');
s.speakerNotes.textFrame.setText('RSI-style visual grammar adapted for the Time-Series Agent survey. Content is a survey-level synthesis of infrastructure and benchmark requirements; the underlying benchmark systems are cited in the manuscript.');
const candidate=path.join(buildDir,'candidate-figure7-rsi-style.pptx'); await (await PresentationFile.exportPptx(p)).save(candidate); const preview=await p.export({slide:s,format:'png',scale:1}); await fs.writeFile(path.join(buildDir,'figure7-rsi-style.png'),new Uint8Array(await preview.arrayBuffer()));
console.log(JSON.stringify({candidate,preview:path.join(buildDir,'figure7-rsi-style.png')}));
