import fs from 'node:fs/promises';
import path from 'node:path';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';
import { pathToFileURL } from 'node:url';

const SKILL_DIR='/Users/mjm/.codex/plugins/cache/openai-primary-runtime/presentations/26.1007.11041/skills/presentations';
const workspaceDir='/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey';
const sourcePath=path.join(workspaceDir,'artifacts/active/skill_reference_figures/RSI_reference_figures_editable.pptx');
const buildDir=path.join(workspaceDir,'.ppt-build');
const finalPath=path.join(workspaceDir,'artifacts/active/TimeSeriesAgent_Figures_RSI_template_working_copy_v6.pptx');
const candidatePath=path.join(buildDir,'candidate-timeseries-from-rsi-template.pptx');
const { finalizePresentation }=await import(pathToFileURL(path.join(SKILL_DIR,'container_tools/artifact_tool_utils.mjs')).href);

const p=await PresentationFile.importPptx(await FileBlob.load(sourcePath));
const replacements=new Map([
  // Slide 1: construction loop
  ['Task-system inheritance','Time-Series Agent construction'],
  ['Retain capability for future tasks','Modules compose across tasks'],
  ['Task system S_t','Time-Series Agent'],
  ['Model, code,\nmemory, tools','LLM + harness\nand temporal data'],
  ['Experience','Paper cards'],
  ['Traces, outcomes,\nfailures','claims, evidence,\nmodule tags'],
  ['Updated system S_{t+1}','New task agent'],
  ['Accepted and\nretained state','Reusable harness\nconfiguration'],
  ['Improvement process I_t','General Harness'],
  ['Diagnose, propose,\nsearch','tools, memory,\ncontrol, planning'],
  ['Candidate changes','Time-Series Harness'],
  ['System or\nimprovement process','temporal state,\noperations, validation'],
  ['Validate & select','Task contract'],
  ['Gains, regressions,\ncost','forecasting, anomaly,\naugmentation, decisions'],
  ['execute','instantiate'],
  ['inspect\nstate','observe'],
  ['feedback','evaluate'],
  ['propose','adapt'],
  ['test','benchmark'],
  ['accept system\nupdate','select module'],
  ['Meta-improvement: in bevit I_{t+1}','Module-level paper card'],
  ['Accepted changes govern how the next improvements are produced','One paper may contribute several modules'],
  ['Declared external anchors: task goals, protected evaluation, and resource budgets','Task semantics and benchmark protocols remain explicit'],
  ['Recursive self-improvement','Time-Series Agent system'],
  ['A mechanism-level view','A module-level construction view'],
  ['Figure 1. A mechanism-level view of recursive self-improvement. Experience informs candidate changes.\nValidation determines what is retained: the upper loop carries task-system state into later tasks; the dashed lower loop carries changes to the process that produce later improvements.\nExternal anchors specify the conditions outside the update scope. The diagram describes possible dependencies, rather than a guarantee of gains.',''],
  // Slide 2: organization
  ['Sections','Survey organization'],
  ['Core topics','Sections'],
  ['RSI\nSurvey','Time-Series\nAgent'],
  ['§ 1    Introduction','§ 1    Introduction'],
  ['§ 2    Scope and Review\nMethodology','§ 2    What Is a\nTime-Series Agent?'],
  ['§ 3    Foundations and\nProblem Formulation','§ 3    LLM-Side\nContributions'],
  ['§ 4    Taxonomy of RSI','§ 4    General\nHarness'],
  ['§ 5    Automated Design of\nAI Infrastructure','§ 5    General Time-Series\nHarness'],
  ['§ 6    Repair and\nOptimization of\nExisting Systems','§ 6    Task-Specific\nHarness'],
  ['§ 7    Benchmarks and\nEvaluation','§ 7    Infrastructure and\nBenchmarks'],
  ['§ 8    Challenges and\nFuture Directions','§ 8    Open Problems and\nCase Studies'],
  ['§ 9    Conclusion','§ 9    Conclusion'],
  ['Two engineering goals\nCentral questions','System definition\nConstruction questions'],
  ['Inclusion and evidence\nRelated-review tree','Review scope\nPaper-card evidence'],
  ['AutoML and meta-learning\nDesign / repair objectives\nTask, retention, improver gains','Temporal representation\nAlignment and reasoning\nLLM-side methods'],
  ['Engineering goal          Update target\nFeedback                  Persistence\nEditable scope             Fixed anchors','Tools and memory          Control and execution\nTemporal state             Provenance and validation'],
  ['Learning pipelines        Agent workflows\nAlgorithm search           Research loops\nUseful design              Better designer','Time-series harnesses     Reusable modules\nTask contracts             Benchmark protocols'],
  ['Weights                    Memory and skills\nPrompts and code           Feedback\nImprover revision          Regression checks','Forecasting                Augmentation\nAnomaly diagnosis          Decision support'],
  ['Goal-matched tests        Sealed audit\nBudget controls            Paired improvers\nRetention / transfer      Accept / roll back','ModernTSF                  TimeSeriesGym\nTraces and episodes        Reproducible evaluation'],
  ['External feedback         Coverage\nUpdate stability           Integrity\nCost / transfer            Scientific validity','Paper-card database        Module-level counts\nOpen tasks                 Evidence gaps'],
  ['Demonstrated gains\nOpen limits and next tests','System map\nOpen problems'],
  // Slide 3: landscape labels around the retained reference visual
  ['The landscape of recursive self-improvement','The Time-Series Agent landscape'],
  ['Foundations, enabling mechanisms and emerging systems','LLM, Harness modules, task contracts, and evaluation infrastructure'],
  ['Figure 3. Landscape of mechanisms relevant to recursive self-improvement. The map connects update targets','Figure 3. Landscape of mechanisms relevant to Time-Series Agents. The map connects the LLM side, reusable Harness modules, temporal Harness modules, and task-specific contracts.'],
  ['in the inner band, improvement mechanisms in the middle band, and representative studies in the outer band.','The inner band denotes the four contribution layers; the middle band denotes reusable mechanisms; the outer band denotes representative works.'],
  ['The six sectors cover weights, tasks, memory, programs, feedback, and the improvement process. A work may','The sectors cover language capability, runtime control, temporal grounding, task contracts, evaluation, and paper-card evidence. A work may'],
  ['involve several targets; its placement highlights one connection. The map includes historical foundations, enabling','contribute to several sectors; its placement highlights one module-level connection. The map includes LLM-side methods, Harness modules,'],
  ['methods, and RSI-oriented systems. Logos denote selected author or work-done affiliations, rather than base','time-series systems, and benchmark infrastructure. Logos denote selected affiliations or project homes, rather than base'],
  ['models; other collaborating institutions may be omitted. The accompanying source register records each selection.','models; other collaborating institutions may be omitted. The accompanying paper-card register records each selection.'],
  // Slide 4: route columns and labels
  ['Research routes toward recursive self-improvement','Research routes in Time-Series Agent systems'],
  ['Selected milestones by first public year | Historical roots and the foundation-model era','Representative module contributions by first public year | LLM and Harness layers'],
  ['Data &\ntraining','LLM\nside'],
  ['Synthetic data\nPersistent updates','Representation\nAlignment'],
  ['Tasks &\ncurricula','General\nHarness'],
  ['Task generation\nEnvironment feedback','Tools and memory\nControl and planning'],
  ['Memory &\nskills','General Time-Series\nHarness'],
  ['Reflective memory\nReusable knowledge','Temporal state\nOperations and grounding'],
  ['Code &\nworkflows','Task-Specific\nHarness'],
  ['Prompts and code\nAgent architectures','Forecasting and prediction\nAnomaly and diagnosis'],
  ['Feedback &\njudges','Infrastructure\nand benchmarks'],
  ['Learned rewards\nEvaluator learning','Episodes, traces\nTimeSeriesGym and ModernTSF'],
  ['Meta-level\nimprovement','Paper-card\ndatabase'],
  ['Update strategies\nResearch automation','Claim, evidence\nmodule-level counts'],
  ['SEAL','ChatTS'],['TTRL','Time-LLM'],['SCoRe','LLM4TS'],['RISE','TimeMaster'],['Quiet-Star','TS-Agent'],['SPIN','TimeART'],['ReSTEM','AION'],['ReST','TimeClaw'],['Self-Instruct','Memory Bank'],['StAR','Reflection'],['AgentEvolver','TimeCAP'],['R-Zero','Temporal grounding'],['Absolute Zero','Forecasting'],['AgentGym','Anomaly diagnosis'],['MetaClaw','Augmentation'],['Dynamic Cheatsheet','Decision support'],['A-MEM','ModernTSF'],['Expel','TimeSeriesGym'],['Voyager','TFRBench'],['Reflection','TSQBench'],
  // Slide 5: task contracts
  ['Answer','Forecasting'],
  ['Revise within one task','origin, horizon,\ncalibration'],
  ['Memory','Augmentation'],
  ['Accumulate experience','fidelity, diversity,\nutility'],
  ['Parameters','Anomaly diagnosis'],
  ['Learn weights $\\theta_t$','event, window,\ncause'],
  ['Improver','Decision support'],
  ['Revise the update process','action, cost,\nuncertainty'],
  ['y_k','forecast y_t'],['y_{k+1}','forecast y_{t+h}'],['check → revise','check → revise'],
  ['Same solver','same harness'],['Future task','new task'],
  ['(a) Local revision','(a) Forecasting'],['(b) Memory retention','(b) Augmentation'],['(c) Parameter learning','(c) Anomaly diagnosis'],['(d) Improver update','(d) Decision support'],
  ['M_t → M_{t+1}','H_t → H_{t+1}'],['Solver + memory','Agent + temporal state'],['M_{t+1}','temporal memory'],['θ_{t+1}','task output'],['Updated model','updated forecast'],['I_t','task contract'],['revise / test','plan / verify'],['Next update process','next task episode'],['I_{t+1}    ΔS_{t+1}','new module record'],['retain','retain'],['⊥  local only','task-bound'],['later reuse','cross-task reuse'],
  ['Figure 6. What survives a round of improvement? Four patterns distinguished by the state carried forward. (a) Local checking ',''],
  ['and revision change an answer without retaining a change to the solver. (b) Memory M is retained while the model parameters a',''],
  ['nd the chosen update procedure are held fixed. (c) Parameters θ are updated under a fixed training procedure. (d) An accepted',''],
  [' change to the improver I is retained and governs a subsequent task-system update ΔS_{t+1}. The horizontal gray dashed line s',''],
  ['eparates current-task or current-round processing from later reuse. Black dashed enclosures group components. Colored arrows ',''],
  ['denote retained updates, and a capped line denotes a change that is not carried forward. Networks, memory stacks, and procedu',''],
  ['re graphs are schematic representations. Solver and improver are functional roles that may share an implementation. These ana',''],
  ['lytical patterns may coexist and do not form a capability ranking; persistent or meta-level changes alone do not establish su',''],
  ['stained recursive gains.',''],
  ['Prime Agent','TS-Agent'],['GEPA','TimeART'],['DGM','AION'],['SICA','TimeClaw'],['AFlow','TimeCAP'],['ADAS','TFRBench'],['TextGrad','TSQBench'],['DSPy','ModernTSF'],['OPRO','TimeSeriesGym'],['Process Self-Rewarding','TraceBench'],['CREAM','Bench'],['Self-Taught Evaluators','Verify'],['Meta-Rewarding','Calib.'],['Self-Rewarding','Audit'],['CRITIC','Audit'],['Constitutional AI','Reproducibility'],['Meta^n','Paper card'],['Bilevel Autoresearch','Ledger'],['Hyperagents','Module tags'],['AlphaEvolve','Open tasks'],['AI Scientist-v2','Case studies'],['AI Scientist','Surveys'],['STOP','BibTeX'],['Promptbreeder','Claims'],
]);

function textOf(sh){try{return sh.text?.toString?.() ?? '';}catch{return '';}}
let edits=0;
for (let si=0; si<p.slides.items.length; si++) {
  const slide=p.slides.items[si];
  for (const sh of (slide.shapes?.items||[])) {
    const old=textOf(sh);
    if (replacements.has(old)) { sh.text=replacements.get(old); edits++; }
  }

  // Replace the inherited radial image on slide 3 with a native, paper-specific layer map.
  if (si === 3) {
    for (const sh of (slide.shapes?.items||[])) {
      const nm=String(sh.name||'');
      if (/^TextBox (138|139|140|141)$/.test(nm) || nm==='TextBox 120' || nm==='TextBox 123') { try { sh.text=''; } catch {} }
    }
  }

  if (si === 2) {
    const oldShapes=[...(slide.shapes?.items||[])];
    for (const sh of oldShapes) { try { sh.delete(); } catch {} }
    const oldImages=[...(slide.images?.items||[])];
    for (const im of oldImages) { try { im.delete(); } catch {} }
    const C={ink:'#20242B',muted:'#687078',line:'#45505A',blue:'#DCEFF1',teal:'#4F8F89',green:'#E1EEDC',green2:'#6B9F80',yellow:'#F5F0CE',gold:'#B47B24',purple:'#E8E0F0',violet:'#6D6396',white:'#FFFFFF'};
    const addText=(x,y,w,h,txt,size=18,color=C.ink,bold=false,italic=false,align='left')=>{const q=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});q.text=txt;q.text.style={typeface:'Cambria',fontSize:size,color,bold,italic,align,verticalAlign:'mid',autoFit:'shrink'};return q;};
    const addBox=(x,y,w,h,fill,line=C.line,dash=false)=>slide.shapes.add({geometry:'roundRect',position:{left:x,top:y,width:w,height:h},fill,line:{style:dash?'dashed':'solid',fill:line,width:1.5}});
    const addLine=(x,y,w,h,color=C.line)=>slide.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:color,line:{style:'solid',fill:color,width:0}});
    addText(70,28,1460,44,'Contribution layers in Time-Series Agents',34,C.ink,true,false,'left');
    addText(70,76,1460,28,'Paper cards record module-level contributions across the LLM, Harness, temporal, task, and evaluation layers.',16,C.muted,false,true,'left');
    addText(80,138,300,28,'LLM side',22,C.violet,true,false,'center');
    const llm=addBox(80,180,300,660,C.purple,C.violet,true);
    addText(105,220,250,30,'Language capability',20,C.violet,true,false,'center');
    addText(108,292,244,145,'representation\nalignment\ntemporal reasoning\nChatTS lineage',18,C.ink,false,false,'center');
    addBox(125,505,210,95,C.white,C.violet,false); addText(140,526,180,48,'LLM component',19,C.ink,true,false,'center');
    addText(105,650,250,72,'Paper card fields\nclaim · evidence · BibTeX',15,C.muted,false,true,'center');
    addText(472,120,620,38,'Time-Series Agent',28,C.ink,true,false,'center');
    const gh=addBox(430,170,700,720,C.blue,C.teal,true);
    addText(465,208,630,30,'General Harness',24,C.teal,true,false,'center');
    addText(465,246,630,30,'tools · memory · control · planning · coordination',15,C.muted,false,true,'center');
    const gts=addBox(535,330,490,470,C.green,C.green2,true);
    addText(565,365,430,30,'General Time-Series Harness',22,C.green2,true,false,'center');
    addText(570,405,420,48,'temporal state · operations\nprovenance · validation',17,C.ink,false,false,'center');
    const tsk=addBox(650,500,260,220,C.yellow,C.gold,true);
    addText(670,530,220,28,'Task-Specific Harness',18,C.gold,true,false,'center');
    addText(678,580,204,76,'forecasting\naugmentation\nanomaly · decisions',16,C.ink,false,false,'center');
    addText(1180,138,300,28,'Evaluation and ledger',20,C.teal,true,false,'center');
    const ev=addBox(1180,180,300,660,C.white,C.teal,true);
    addText(1205,220,250,30,'Benchmark contract',20,C.teal,true,false,'center');
    addText(1205,292,250,126,'episodes\nchronology\nheld-out tests\nreproducible traces',17,C.ink,false,false,'center');
    addBox(1220,500,220,100,C.blue,C.teal,false); addText(1238,522,184,52,'module-level\ncounts',19,C.ink,true,false,'center');
    addText(1200,650,260,72,'Each paper can contribute\nseveral modules',15,C.muted,false,true,'center');
    // hierarchy connectors
    slide.shapes.connect(llm,gh,{kind:'straight',fromSide:'right',toSide:'left',line:{style:'solid',fill:C.violet,width:2.5},head:{type:'arrow',width:'sm',length:'sm'}});
    slide.shapes.connect(gh,gts,{kind:'straight',fromSide:'bottom',toSide:'top',line:{style:'solid',fill:C.teal,width:2.5},head:{type:'arrow',width:'sm',length:'sm'}});
    slide.shapes.connect(gts,tsk,{kind:'straight',fromSide:'bottom',toSide:'top',line:{style:'solid',fill:C.gold,width:2.5},head:{type:'arrow',width:'sm',length:'sm'}});
    slide.shapes.connect(tsk,ev,{kind:'straight',fromSide:'right',toSide:'left',line:{style:'solid',fill:C.teal,width:2.5},head:{type:'arrow',width:'sm',length:'sm'}});
    addLine(430,930,700,2,C.line);
    addText(460,948,640,26,'General Harness ⊃ General Time-Series Harness ⊃ Task-Specific Harness',16,C.ink,true,false,'center');
  }

  if (slide.speakerNotes?.textFrame) {
    slide.speakerNotes.textFrame.setText(`Time-Series Agent survey figure adapted from the user-supplied RSI visual template. The layout, typography, and visual hierarchy are retained while the content is rewritten for the LLM + General Harness + Time-Series Harness Module framework. Editable PowerPoint objects remain available for later grouping and revision.`);
  }
}
await fs.mkdir(path.dirname(finalPath),{recursive:true});
await (await PresentationFile.exportPptx(p)).save(candidatePath);
const result=await finalizePresentation({
  workspaceDir,candidatePath,finalPath,
  pythonExecutable:'/Users/mjm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
  integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','16668750,12782550','--validate-heading-fit'],
  sourceTemplatePath:sourcePath,
  requiredTemplateReferenceSlides:[1,2,3,4,5],
  minimumTemplateCoverageRatio:0.9,
  fontPolicy:{basis:'reference',families:['Cambria','PingFang SC'],referencePath:sourcePath,referenceSha256:'5e2e378aa2d6a89fcd5c48a4ecaf22f5508058938b53bb1e96a714452a9c928b'},
  verifyArtifactToolImport:true,
  receiptPath:path.join(buildDir,'timeseries-from-rsi-template-v6.validation.json')
});
console.log(JSON.stringify({edits,result},null,2));
