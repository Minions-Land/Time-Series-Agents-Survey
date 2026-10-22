# Figures 4, 9, 13, and 14

Revision started on 22 October and completed on 23 October 2026.

Each file in `pptx/` contains one slide. The outer group contains semantic module groups; icons are nested groups of native vector paths. Text, signal curves, interval marks, arrows, and icon paths remain editable. No screenshot or raster illustration is embedded in these four figures. The corresponding files in `pdf/` are the manuscript figures.

| Figure | Purpose | Primary source |
|---|---|---|
| 4 | Match tasks to temporal functions, then compose a demand-planning workflow | Survey taxonomy and cited examples in the manuscript |
| 9 | Explain reference selection, context-dependent augmentation, review, and the positive sample set used by the encoder | [MERIT](https://aclanthology.org/2025.findings-acl.1231/), Sections 3.2–3.5 and Figure 2 |
| 13 | Show how numerical evidence satisfies an anomaly-location question before an answer is accepted | [TS-Agent](https://arxiv.org/abs/2510.07432), Sections 4.1–4.3 |
| 14 | Locate numerical execution, multimodal retrieval, and the path from successful experience to registered tools | [TIMECLAW](https://arxiv.org/abs/2606.05404), Sections 3.1–3.4 |

The series in Figures 4, 9, and 13 are schematic explanatory examples. Figure 9's jitter and permutation cases illustrate possible review outcomes, rather than fixed acceptance criteria. Figure 13 uses the source paper's question and evidence predicates with an illustrative middle-region anomaly. Figure 14's snowstorm and electricity-demand example follows the source paper's discussion of a transferable rationale.

`assets/` retains the original [Lucide](https://github.com/lucide-icons/lucide) SVGs and ISC license. `assets/icons.json` records their URLs and native path definitions. Source citations also appear in the slide notes.

`build.mjs` authors native objects with `@oai/artifact-tool`; `group_native.py` groups those objects without rasterization and removes grouping locks. Run the builder from the repository root with the bundled presentation runtime available as `node_modules`. `fetch_icons.py` regenerates the source paths with `svgpathtools` and `svgwrite`. Private drafts and intermediate checks are under `.build/`. Production PPTX files passed the presentation finalizer and were exported to PDF with LibreOffice.

In PowerPoint, select the figure and use Arrange > Ungroup to access its modules. Ungroup a module again to edit its text, curves, or icon paths.

All four final files were opened in Microsoft PowerPoint and tested with Ungroup; Group and Regroup remained available. Figures 4, 9, 13, and 14 contain 214, 122, 98, and 149 native shapes respectively, organized into 47, 16, 16, and 21 groups.

Desktop editing copies: `~/Desktop/Survey Figures/Abel Guys/Revised_PPT/Semantic_20261023/`.
