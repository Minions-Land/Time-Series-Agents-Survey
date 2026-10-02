import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {pathToFileURL} from 'node:url';
const SKILL_DIR='/Users/mjm/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const workspaceDir='/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey';
const buildDir=path.join(workspaceDir,'.ppt-build');
const finalPath=path.join(workspaceDir,'artifacts','RSI_Reference_Figures_PixelFaithful_Components.pptx');
const {finalizePresentation,resolvePresentationFont}=await import(pathToFileURL(path.join(SKILL_DIR,'container_tools/artifact_tool_utils.mjs')).href);
const refs=[
 ['03514d1b-0ebc-4946-8261-3b775509d1f7.png','Module-level contributions'],
 ['250411b2-1d1f-4bba-a7bd-241fd0ec6be1.png','Organization of the survey'],
 ['2ee58a4a-5ea6-43c1-b6cd-fa97801e2762.png','Landscape'],
 ['473be8a2-e4eb-4cca-bfdd-97302b50480b.png','Open problems'],
 ['70181ba7-3a8e-4452-9f50-ffa240cc6655.png','Coverage table'],
 ['7572f4b2-a5e3-4239-800f-b94ac30e4317.png','Four perspectives'],
 ['93b9b499-6e13-4dd0-bbe2-28235f020bfe.png','Recursive loop'],
 ['a5f5d981-2117-48b5-8cb6-bcbbbbe0f3e6.png','Update mechanisms'],
 ['cc759328-3690-4186-9986-fe51794f5931.png','Perspectives synthesis'],
 ['ded9e63e-c562-44fb-941d-7de354ae4c7d.png','Research routes'],
 ['c4471a69-b143-4c54-8d60-2b3909aec7b0.png','Dark text panel'],
];
const p=Presentation.create({slideSize:{width:1280,height:720}});
for (let si=0; si<refs.length; si++){ const [file,label]=refs[si];
 const bytes=new Uint8Array(await fs.readFile(`/var/folders/00/cjpqgxnj1ln8ghv0h48ct6rw0000gn/T/codex-clipboard-${file}`));
 const dims={'03514d1b-0ebc-4946-8261-3b775509d1f7.png':[1554,1054],'250411b2-1d1f-4bba-a7bd-241fd0ec6be1.png':[1378,1274],'2ee58a4a-5ea6-43c1-b6cd-fa97801e2762.png':[1426,1518],'473be8a2-e4eb-4cca-bfdd-97302b50480b.png':[1210,1526],'70181ba7-3a8e-4452-9f50-ffa240cc6655.png':[1114,850],'7572f4b2-a5e3-4239-800f-b94ac30e4317.png':[1254,1242],'93b9b499-6e13-4dd0-bbe2-28235f020bfe.png':[1758,1354],'a5f5d981-2117-48b5-8cb6-bcbbbbe0f3e6.png':[1294,1402],'cc759328-3690-4186-9986-fe51794f5931.png':[1102,682],'ded9e63e-c562-44fb-941d-7de354ae4c7d.png':[1114,1462],'c4471a69-b143-4c54-8d60-2b3909aec7b0.png':[1164,332]};
 const [sw,sh]=dims[file]||[1,1]; const scale=Math.min(1210/sw,680/sh); const W=sw*scale,H=sh*scale; const left=(1280-W)/2, top=(720-H)/2;
 const s=p.slides.add(); s.background.fill='#FFFFFF';
 const cols=4, rows=4;
 for(let r=0;r<rows;r++) for(let c=0;c<cols;c++){
   const x=left+(c/cols)*W, y=top+(r/rows)*H, w=W/cols+0.2, h=H/rows+0.2;
   const tile=new Uint8Array(await fs.readFile(path.join(buildDir,'rsi-tiles',`s${si+1}_r${r}_c${c}.png`))); s.images.add({blob:tile,contentType:'image/png',alt:`${label} component tile ${r+1}-${c+1}`,fit:'cover',position:{left:x,top:y,width:w,height:h},lockAspectRatio:true});
 }
 s.speakerNotes.textFrame.setText(`Pixel-faithful conversion of the user-provided screenshot ${file}. The visible figure is the original image split into sixteen independently movable image components (4 x 4). No redraw or generated artwork is used.`);
}
const candidate=path.join(buildDir,'candidate-rsi-reference-pixeldeck.pptx');await (await PresentationFile.exportPptx(p)).save(candidate);for(let i=0;i<p.slides.items.length;i++){const blob=await p.export({slide:p.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(buildDir,`rsi-pixel-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()))}
const res=await finalizePresentation({workspaceDir,candidatePath:candidate,finalPath,pythonExecutable:'/Users/mjm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000'],fontPolicy:{basis:'design',families:[resolvePresentationFont({fontFamily:'Times New Roman'})]},verifyArtifactToolImport:true,receiptPath:path.join(buildDir,'rsi-reference-pixeldeck.validation.json')});console.log(JSON.stringify(res));
