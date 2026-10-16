# Narrative and Sections 7–8 audit

Read Introduction through Conclusion and appendix introduction/schema/tables framing. Coverage is prose and LaTeX linkage, not rendered visual inspection or complete source verification of every method.

## Findings

### N1 — factual — main.tex:778
TimeSage-EV corpus is described as 1,485 instances over 24 periods; source says at least 24 per scenario and Feb 2023–May 2026.

Suggested change: The reported snapshot contains 60 scenarios across six domains and 1,485 scenario-period instances spanning February 2023 to May 2026.

### N2 — comparison_definition — main.tex:178
Lifecycle combines construction, learning/updating, evaluation, operational use, while caption allows any dedicated treatment. A cross may hide dedicated partial coverage. Root is independently source-checking this table.

Suggested change: Define each retained column with one observable organizing criterion; encode unverified full-text cells as not coded, not absence. If Lifecycle remains, state exactly which linked stages qualify and retain per-cell source locators.

### N3 — provenance — main.tex:215
Three adapted overview captions identify only an RSI-style survey template, with no bibliographic source or figure number. This is not a complete attribution.

Suggested change: Replace the vague last sentence with an actual verified work title/citation and source figure number, e.g. Visual organization adapted from [verified reference], Fig. X; content and hierarchy developed for this survey.

### N4 — organization — main.tex:659
Detailed TSEvol paragraph appears among TSK synthesis procedures although the contribution is LLM-specific instruction supervision. Existing Section3 cross-reference helps but source of scope ambiguity remains.

Suggested change: For language-model supervision, ChatAD \citep{chatad2026} constructs temporal instruction dialogues through TSEvol; this model-side use of synthesis is discussed in Section~3.

### N5 — repetition — main.tex:259
Section2 repeats scenario-first construction after the grid example and then again enumerates it; final roadmap repeats Section1 organization. These are coherent but consume space better used for comparison.

Suggested change: Let the five-step list carry the construction procedure. Delete the immediately preceding paragraph beginning The construction begins with the scenario, and condense the closing roadmap to a single forward link to Sections3–7.

### N6 — notation — main.tex:282
Unified notation includes omega_k, M_tau and C_task which are not used as common variables in main-text equations. This suggests a unified formalism beyond what methods actually share.

Suggested change: Keep symbols used across equations (x, t/tau/H, admissible information, state/action/observation, outputs); define method-specific symbols beside their equations. Remove unused typed-tool-call and memory notation unless actually used.

### N7 — case_analysis — main.tex:880
Focused ChatTS and ModernTSF cases are prospective design sketches, not empirical system case studies; headings already say analyses but much content repeats Sections3/7.

Suggested change: Rename subsection Design implications and retain one precise comparison per case: numerical representation interface for ChatTS, experience state for TimeClaw, fixed numerical substrate for ModernTSF. Avoid repeating pipeline descriptions.

### N8 — precision — main.tex:886
TimeClaw formula attribution is correct. The external state A_s is task-scoped in source; current phrase transferable result may be read too broadly when paired with cross-task reuse rhetoric.

Suggested change: The cleaned evidence updates the task-scoped experience state $A_s$. The update mechanism accepts different task losses; transfer of the retained content is assessed on held-out episodes.

### N9 — grammar — main.tex:865
TimeSage-EV and its next-period skill activation provides has subject–verb mismatch.

Suggested change: TimeSage-EV \citep{timesageev2026} provides a concrete availability rule through next-period skill activation.

### N10 — evidence_scope — main.tex:461
This criterion follows the temporal contracts emphasized in cited surveys may attribute the authors own GH/GTS boundary directly to prior taxonomies.

Suggested change: We use these temporal requirements to distinguish shared temporal modules from general runtime mechanisms, building on the task and reasoning perspectives in \citep{chen2026tsagentsurvey,changsurvey2026}.

## Section coverage

- 124: Introduction — Scenario → construction question → scopes → resources forms a clear chain. Counts agree with canonical JSON in prior live check. Avoid duplicating procedure later.

- 170: Position relative to existing surveys — Needs N2 binary comparison criterion audit; titles and name-adjacent citations are present.

- 199: Contributions — Four substantive contributions, with PaperCard in intro rather than abstract; appropriate. Figure provenance N3.

- 229: What Is a Time-Series Agent? — Coordinates are clearly distinguished. Grid expresses task/function reading view without multiplying layer counts. N5/N6 tighten.

- 298: LLM-Side Contributions for Time-Series Agents — Correctly starts from action/feedback role and treats temporal adaptation as optional intervention.

- 302: Temporal representation and alignment — Explicit frozen-backbone versus conversational-interface comparison and runtime obligations; not mere enumeration.

- 325: Temporal instruction and reasoning — Differentiates training signals and numerical/explanation/evidence/action metrics; necessary evidential distinctions, not defensive disclaimer.

- 357: Learning to operate temporal workflows — Compares judge, prescribed tool policy, preference-trained response. Good integration requirements.

- 374: General Harness — Seven dimensions stable, figure and table explained. Intro+post-figure roadmap mildly repetitive.

- 416: Interface and Interaction — Exploratory loop versus task-file submission comparison is concrete.

- 422: Memory and Context — Evidence log/progress record/role report comparison yields inspection and persistence choices.

- 428: Tools and Execution — Planner/executor separation and MetaCaster job scheduling give distinct reusable mechanisms.

- 434: Control, Verification, and Feedback — Execution feedback versus delayed task outcome correctly distinguishes feedback schedules.

- 440: Planning and Workflow — Incremental choice versus whole executable plan, then acceptance checkpoints: coherent.

- 446: Optimization and Evolution — Experience state versus promoted tool registry is a useful comparison; equations correctly deferred.

- 452: Coordination and Scaling — Artifact handoffs are clear; FinCon objective is now explicitly TSK in Section6. Cross-example acceptable.

- 458: General Time-Series Harness — Four function reading view is explained relative to seven mechanisms; N10 attribution wording.

- 483: Temporal Data Management — Schema, numerical workspace and ordered buffer address three distinct ambiguities; closing tests concrete.

- 494: Temporal Processing — Atomic operators versus composed task-indexed chains differentiated; no blanket GTS assignment.

- 511: Temporal Context and Memory — Timeline, signal/text retrieval and task-bound policy separated; closes with meaningful evidence checks.

- 527: Temporal Validation — Availability, skill activation, data quality and answer predicates separated; TS-Agent gate explicitly TSK.

- 538: Task-Specific Time-Series Harness — Four families plus secondary task labels makes actual coverage clear; no claim these exhaust all tasks.

- 561: Forecasting and Prediction — Rich method equations and output distinctions. Three bold blocks are long enough; keep.

- 632: Data Augmentation and Synthesis — BRIDGE/MERIT/MetaCaster comparison meaningful; N4 TSEvol cross-layer placement.

- 670: Anomaly Detection and Diagnosis — Evidence acquisition, exemplar retrieval, detector-program construction and diagnosis differentiated. Bold blocks sufficiently substantive.

- 704: Decision Support — Financial memory, portfolio policy and traffic control connect predictions to actions and utility.

- 740: Infrastructure and Benchmarks for Time-Series Agents — AION task specification formula matches primary source; values and checks separated.

- 752: Evaluation contract — Stub versus execution protocol contrasted, trace purpose explained.

- 767: Existing benchmark landscape — Detailed protocol-specific text. N1 TimeSage-EV count wording must fix. Numeric spot checks detailed below.

- 811: Temporal question answering — QA positioned as measurable capability and connected to larger output contracts, no blanket dismissal.

- 825: Infrastructure for reproducible evaluation — Different boundaries identified; ModernTSF described modestly as infrastructure not benchmark.

- 840: Selecting a benchmark for a new scenario — Concrete resource composition plus synthesis/decision metrics. Some demand example repetition from Section2 but purposeful application.

- 851: Open Problems and Focused System Analyses — Research agenda follows construction logic; no claim to final exhaustive survey.

- 853: Reusable temporal infrastructure — Explicit proposed transfer and replay tests rather than inferred empirical generality.

- 859: Open problems — Five evidence-linked questions with controlled tests; N9 grammar. Single bold paragraphs are substantive, not fragmentary headings.

- 880: Focused system analyses — TimeClaw source equations verified; N7 case duplication and N8 task scope precision.

- 903: Conclusion — Three positive paragraphs summarize construction, evaluation and research agenda; no defensive narrowing or unsupported finality.

- 918: Module-Level Contribution Ledger — Clear fields, resource links and function-view semantics. Background count now fixed to three.

- 922: Paper Card schema — Four-pass procedure and deepest-module scope clear. Sample and complete tables both have body explanations.

## Figure and table coverage

- fig:contribution-trend (line 167; body refs [161]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- tab:direct-prior-comparison (line 196; body refs [178]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit. N2: binary coverage criterion needs source-bound adjudication.

- fig:survey-organization (line 216; body refs [210]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit. N3: exact adaptation source missing.

- fig:overview (line 225; body refs [219, 924]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit. N3: exact adaptation source missing.

- fig:task-function-grid (line 253; body refs [155, 247, 541, 844]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- tab:unified-notation (line 292; body refs [270]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit. N6: some entries unused in equations.

- fig:chatts-overview (line 333; body refs [327]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- tab:component-vocab (line 385; body refs [243, 377, 405, 481, 994]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:general-harness-seven-dimensions (line 411; body refs [405]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:aion-principles (line 478; body refs [472]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:task-specific-harness (line 558; body refs [552]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit. N3: exact adaptation source missing.

- fig:merit-augmentation (line 667; body refs [644, 661]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:anomamind-workflow (line 701; body refs [687]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:evaluation-stack (line 764; body refs [758]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:benchmark-landscape (line 775; body refs [769]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- tab:benchmark-families (line 808; body refs [788]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:benchmark-qa (line 822; body refs [816]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:benchmark-infrastructure (line 837; body refs [831]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- fig:open-problems-cases (line 877; body refs [871]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- tab:ledger-sample (line 977; body refs [975]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

- tab:agent-ledger (line 1009; body refs [1007]): Text supplies purpose, reading route or compared objects, and interpretation. Checked source text/caption linkage only; rendered visual not inspected in this audit.

## Primary-source formula checks

- eq:aion-task-contract: references/pdfs/aion2026.pdf pp3–4, Eqs1–3 — Tuple, file fields, and validity/score mapping match; survey disambiguates access T as T_access. Missing-value/hidden-column constraints supported.

- eq:timeclaw-compare: references/pdfs/timeclaw2026explore.pdf p3 Eq1 — Negative task loss and argmax over valid trajectories exact. Source also defines no-valid-candidate fallback; no need full algorithm in survey.

- eq:timeclaw-distill: references/pdfs/timeclaw2026explore.pdf p4 Eqs2–4 — Summarize/Clean/Distill sequence matches. Add task-scoped state clarification N8.

## Benchmark factual spot checks

- TimeSeriesGym, pp4,6: 34 challenges/23 sources/8 types and Docker/4h/50-step defaults confirmed.

- TimeSage-MT, pp1–2,7: 240 tasks/4 levels/8 domains and 226 skills/36 categories confirmed.

- TimeSage-EV, pp1,5,13–15: 60 scenarios/6 domains/1485 confirmed; 24 is minimum per scenario, not corpus total periods.

- Dr-CiK, pp2,4–5: 240 tasks/8849 documents confirmed.

- TFRBench, pp1–2,6: 10 datasets/5 domains and historical+future event reference construction confirmed.

## Resolution and actual-figure follow-up

N1, N7, N8, N9 applied to Sections7–8. Other textual recommendations handed to root. Figure2/3 original native grouped sources updated; single-page PDF/SVG refreshed and rendered.

- fig:survey-organization: Repaired stale Section2/4/5/8 content in original grouped PPT. Section3 now interfaces/adaptation/policies. Section4 seven functions summarized; Section5 four temporal functions. Exported PDF/SVG and inspected final render; text fits.

- fig:overview: Repaired subtitle implying five contribution layers; now LLM plus three Harness scopes. LLM panel now interpretation, tool action selection, returned feedback and temporal adaptation. Native nested shapes preserved. PDF/SVG refreshed; render inspected.

- fig:task-function-grid: Actual GTS examples SAGE-AD and TimeSeriesScientist match canonical boundaries; MERIT/FinMem TSK. Caption reading directions match row/function, column/task. At source scale TimeSeriesScientist label sits close to row bottom; recommend roomier label if editing later.

- fig:aion-principles: Actual PNG had repeated placeholder explanations: knowledge dependence and post-experiment analysis both described as declares task contract; several distinct subfunctions all adds inspectable check. Reported to root and assigned other agent for repair.

- fig:task-specific-harness: Actual panel borrowed RSI parameter-network and improver-graph graphics; top anomaly/decision titles overlapped subtitles. Reported to root and assigned other agent for repair.

- fig:general-harness-seven-dimensions: Actual seven labels match text. Footer duplicates caption but no taxonomy error.

- fig:chatts-overview: Actual attribute selector, generator, instruction evolution and training correspond to caption. Figure emphasizes representation/alignment; section prose adds workflow-role distinction.

- fig:evaluation-stack: Actual inputs/challenge/outputs plus quantitative/qualitative rows match caption purpose; generalized synthesis includes artifacts/traces rather than claiming all benchmark resources provide all observables.

- fig:benchmark-landscape: Actual source/challenge/agent/grader structure matches caption. Qualitative grader label means artifact checks; numerical performance separated.

- fig:benchmark-qa: Actual evidence log/tools/critic/answer path matches prose. Tool arrows visible in extraction labels; no stale layer markers.

- fig:benchmark-infrastructure: Actual workspace/evolution/multimodal memory matches TIMECLAW harness description; distinct from exploratory TimeClaw equations.

- fig:open-problems-cases: Actual five open-problem rows match subsection. ChatTS/TimeClaw/ModernTSF boxes match design examples; labels GH/GTS/TSK reflect research targets not new module counts.

- fig:merit-augmentation: Actual retrieval/augmentation/review/accepted-set labels match contrastive positive-view explanation.

- fig:anomamind-workflow: Actual four stages, training feedback and knowledge/numerical toolkit match body explanation.

- fig:contribution-trend: Actual four legend entries and logarithmic axis are present. Count verification performed against canonical JSON separately.

RSI screenshot provenance: source page002 caption explicitly identifies original Figure2; page005 original Figure6. Original page003 was the radial landscape, not the current rectangular hierarchy. Exact source PDF absent from original Downloads path.
