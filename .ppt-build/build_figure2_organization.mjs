import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = "/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey";
const SKILL_DIR = "/Users/mjm/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations";
const TMP_DIR = path.join(workspaceDir, ".ppt-build", "figure2-active");
const outDir = path.join(workspaceDir, "artifacts", "active");
await fs.mkdir(TMP_DIR, { recursive: true });
await fs.mkdir(outDir, { recursive: true });
const { resolvePresentationFont } = await import(pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href);
const family = resolvePresentationFont({ fontFamily: "Times New Roman" });

const C = {
  ink: "#1E2F47",
  muted: "#6B7280",
  paper: "#FBFBF8",
  line: "#26384A",
  llmFill: "#EEEAF7",
  llmLine: "#7058A6",
  ghFill: "#E4EFF4",
  ghLine: "#2D6E8F",
  gtsFill: "#E8F2EA",
  gtsLine: "#3E8167",
  tskFill: "#F8F1DF",
  tskLine: "#B78324",
  evidenceFill: "#E9F0F4",
  evidenceLine: "#467A92",
  white: "#FFFFFF",
};

const p = Presentation.create({ slideSize: { width: 1600, height: 900 } });
const slide = p.slides.add();
slide.background.fill = C.paper;

function box({ left, top, width, height, fill, line = C.line, radius = 18, dashed = false, name }) {
  return slide.shapes.add({
    geometry: "roundRect",
    name,
    position: { left, top, width, height },
    fill,
    line: { style: dashed ? "dashed" : "solid", fill: line, width: 2 },
    borderRadius: radius,
  });
}
function text({ left, top, width, height, value, size = 18, color = C.ink, bold = false, italic = false, align = "left", name }) {
  const s = slide.shapes.add({
    geometry: "textbox",
    name,
    position: { left, top, width, height },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  s.text = value;
  s.text.style = { typeface: family, fontSize: size, color, bold, italic, alignment: align, autoFit: "shrinkTextOnOverflow" };
  return s;
}
function line({ left, top, width, height, color = C.line, widthPx = 2, dashed = false, name }) {
  return slide.shapes.add({
    geometry: "line",
    name,
    position: { left, top, width, height },
    fill: "none",
    line: { style: dashed ? "dashed" : "solid", fill: color, width: widthPx },
  });
}

text({ left: 82, top: 42, width: 1436, height: 42, value: "Organization of the survey", size: 34, color: C.ink, bold: true, name: "figure-title" });
text({ left: 84, top: 87, width: 1420, height: 28, value: "The sections follow the construction of a Time-Series Agent and the evidence needed to evaluate it.", size: 17, color: C.muted, italic: true, name: "figure-subtitle" });

const railX = 268;
line({ left: railX, top: 164, width: 0, height: 652, color: C.line, widthPx: 3, name: "section-rail" });
const leftSurvey = box({ left: 42, top: 382, width: 224, height: 194, fill: C.ghFill, line: C.ghLine, radius: 18, dashed: true, name: "survey-label-box" });
text({ left: 54, top: 410, width: 200, height: 90, value: "Time-Series\nAgent\nSurvey", size: 25, color: C.ink, bold: true, align: "center", name: "survey-label" });
text({ left: 54, top: 510, width: 200, height: 28, value: "reader's map", size: 16, color: C.muted, italic: true, align: "center", name: "survey-sublabel" });
line({ left: 248, top: 479, width: 44, height: 0, color: C.ghLine, widthPx: 3, name: "survey-leader" });

const rows = [
  ["§ 1", "Introduction", "Scope, motivation, and central questions", C.tskFill, C.tskLine],
  ["§ 2", "What Is a Time-Series Agent?", "Construction layers and the paper-card unit", C.tskFill, C.tskLine],
  ["§ 3", "LLM-Side Contributions", "Temporal representation, alignment, and language reasoning", C.llmFill, C.llmLine],
  ["§ 4", "General Harness", "Seven reusable runtime dimensions", C.ghFill, C.ghLine],
  ["§ 5", "General Time-Series Harness", "Temporal contracts that transfer across tasks", C.gtsFill, C.gtsLine],
  ["§ 6", "Task-Specific Harness", "Forecasting, augmentation, anomaly, and decision support", C.tskFill, C.tskLine],
  ["§ 7", "Infrastructure and Benchmarks", "Episodes, traces, tools, and task outcomes", C.evidenceFill, C.evidenceLine],
  ["§ 8", "Open Problems and Case Studies", "Where modules and evaluation remain incomplete", C.llmFill, C.llmLine],
  ["§ 9", "Conclusion", "A reusable map for future systems", C.llmFill, C.llmLine],
];
const y0 = 136, rowH = 63, gap = 12;
for (let i = 0; i < rows.length; i++) {
  const [sec, title, topic, fill, accent] = rows[i];
  const y = y0 + i * (rowH + gap);
  const dot = slide.shapes.add({ geometry: "ellipse", name: `rail-dot-${i+1}`, position: { left: railX - 7, top: y + rowH / 2 - 7, width: 14, height: 14 }, fill: C.paper, line: { style: "solid", fill: accent, width: 2 } });
  const left = box({ left: 320, top: y, width: 470, height: rowH, fill, line: accent, radius: 16, dashed: true, name: `section-box-${i+1}` });
  text({ left: 344, top: y + 21, width: 62, height: 24, value: sec, size: 19, color: C.ink, bold: true, name: `section-number-${i+1}` });
  text({ left: 416, top: y + 18, width: 350, height: 30, value: title, size: title.length > 30 ? 19 : 21, color: C.ink, bold: true, name: `section-title-${i+1}` });
  line({ left: 790, top: y + rowH / 2, width: 34, height: 0, color: accent, widthPx: 2, name: `topic-leader-${i+1}` });
  const right = box({ left: 824, top: y, width: 700, height: rowH, fill: C.paper, line: accent, radius: 16, name: `topic-box-${i+1}` });
  text({ left: 852, top: y + 20, width: 640, height: 28, value: topic, size: 18, color: C.ink, name: `topic-text-${i+1}` });
}

const cardY = 820;
const card = box({ left: 320, top: cardY, width: 1204, height: 48, fill: C.white, line: C.ink, radius: 14, name: "paper-card-strip" });
text({ left: 344, top: cardY + 14, width: 200, height: 22, value: "Paper card fields", size: 18, color: C.ink, bold: true, name: "paper-card-title" });
text({ left: 566, top: cardY + 14, width: 920, height: 22, value: "claim  ·  evidence locator  ·  module layer  ·  task family  ·  BibTeX  ·  review status", size: 16, color: C.muted, name: "paper-card-fields" });
text({ left: 320, top: 874, width: 1204, height: 18, value: "Each card records modules independently, while the survey organizes them by the deepest applicable Harness layer.", size: 13, color: C.muted, italic: true, align: "center", name: "paper-card-note" });

slide.speakerNotes.textFrame.setText("Layout reference: user-supplied Recursive Self-Improvement in AI survey organization map. Content follows the current Time-Series Agent survey section plan. All visual elements are native editable PowerPoint shapes and text.");

const candidatePath = path.join(TMP_DIR, "candidate-figure2-organization.pptx");
await (await PresentationFile.exportPptx(p)).save(candidatePath);
const preview = await p.export({ slide, format: "png", scale: 1 });
await fs.writeFile(path.join(TMP_DIR, "figure2-organization.png"), new Uint8Array(await preview.arrayBuffer()));

const stagingDir = path.join(workspaceDir, ".codex-finalizer", "figure2-organization");
await fs.mkdir(stagingDir, { recursive: true });
const { finalizePresentation } = await import(pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href);
const FINAL_PPTX = path.join(outDir, "Figure2_organization_native_v2.pptx");
const result = await finalizePresentation({
  workspaceDir,
  candidatePath,
  finalPath: FINAL_PPTX,
  pythonExecutable: "/Users/mjm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
  integrityValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "15240000,8572500", "--validate-heading-fit"],
  fontPolicy: { basis: "user_request", families: ["Times New Roman"] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir, "Figure2_organization_native_v2.validation.json"),
});
console.log(JSON.stringify({ candidatePath, FINAL_PPTX, result }, null, 2));
