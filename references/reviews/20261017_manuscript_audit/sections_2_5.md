# Sections 2–5 evidence audit

main.tex Sections 2–5, lines 229–537 of reviewed working snapshot

Paragraph reading plus targeted primary-source PDF pages. Verdicts concern manuscript assertions, not reproduction of reported experiments or full-paper validity.

## Findings

- **taxonomy_attribution**, line [461]: Chen and Chang motivate temporal considerations but do not establish this survey's GH/GTS boundary. Current criterion-follows wording overattributes the proposed classification. Suggested: We organize these requirements around the temporal-grounding and runtime-native mechanisms developed in AION \citep{aion2026} and TIMECLAW \citep{timeclaw2026harness}.

- **seven_dimension_provenance**, line [377]: Sources include framework papers and differently organized surveys. The seven labels are a survey synthesis, not seven original labels common verbatim to every cited source. Suggested: Retain drawing-on wording, remove unverified agentcybernetics2026 citation, and describe the table as synthesized comparison vocabulary.

- **calm_lateness**, line [492]: Ordered buffering supports out-of-order arrivals under configured event-time/watermark processing, not arbitrary unlimited lateness. Suggested: Optional precision: CALM buffers observations per key and uses event-time timers to emit ordered sliding windows.

- **modern_tsf_local_citation**, line [256]: ModernTSF is named without a local citation or repository footnote in this paragraph; later infrastructure section may provide it. Suggested: Use the already verified ModernTSF citation or existing repository footnote at this first design example, without inventing a paper.

## Method/source coverage

| Source | TeX lines | PDF pages | Checked content |
|---|---|---|---|
| timeseriesscientist2025 | 247,456,501 | 5,6 | Curator diagnostic tuple, preprocessing, visualization; planning before forecasting |
| sagead2026 | 247,490 | 4 | Original numerical series separated from compressed prompting summary |
| merit2025 | 247 | 2 | Retrieval and augmentation agents construct positive contrastive views |
| finmem2023 | 247,525 | 3,7,9 | Financial relevance/recency/importance ranking and deeper-layer retention |
| drcik2026 | 256 | 1,2 | External-context retrieval plus forecasting benchmark |
| timeseriesgym2025 | 256 | 1,2 | ML engineering tasks include code/model artifacts and diverse graders |
| jin2024timellm | 304,323 | 5 | Frozen backbone, text prototypes, Q/K/V patch cross-attention and Prompt-as-Prefix |
| chang2024llm4ts | 311 | 2,3 | Two-stage time-series alignment and forecasting adaptation |
| chatts2025 | 313,323,327,332,353 | 5 | Five-layer patch MLP, interleaved sequence/text, min-max plus scaling/offset, attribute-guided instruction evolution |
| agenticrag2024 | 321 | 3 | Continuous prompt embedding pool and learned projection, model-side mechanism |
| chow2024tsreasoning | 336 | 3 | Encoder warmup then joint LoRA adaptation on reasoning tasks |
| timer12025 | 336,341,353 | 4,5 | Eq3 bounded normalized MSE reward; structural rewards; nonuniform sampling and adaptive weighting in GRIP |
| stride2026 | 343,353 | 4,5,6,11 | Algorithm1 mean pooling/projection/fusion/joint loss and train/inference separation |
| conversationaltsfm2025 | 359,372 | 3,5 | Numerical optimizer plus LLM accept/continue judge, SFT boundary cases and GRPO feedback |
| castfsr2026 | 361,372 | 4,11,12 | Fast-Slow-Reflect SFT and complete-trajectory RL; training filters illegal calls, wrong stage order, leakage, invalid timestamps, incomplete forecasts |
| timeart2026 | 361,499 | 1,2 | Tool-augmented temporal reasoner and four-stage training |
| chatad2026 | 363,370,372 | 4,5,6,25 | CRL target training; LoRA then TKTO Eqs4–5; judged reasoning and parsed format distinct from AD metrics |
| anomamind2026 | 370 | 3,5 | General reasoning/tool invocation separated from RL detection decisions |
| ning2026codeharness | 377 | 1,2 | Reasoning/action/environment; planning/memory/tools; feedback/control/optimization and multi-agent scaling |
| lee2026metaharness | 377 | 1 | Outer-loop search over harness code using source, scores and traces; supporting optimization example rather than seven-way taxonomy |
| lin2026agenticharness | 377 | 1 | Tools, middleware, long-term memory and observability-driven harness evolution; supporting mechanism example |
| changsurvey2026 | 377,461 | 1,3,7 | Reasoning topologies/objectives with grounding, memory, control/tool-use themes; not original GH/GTS boundary |
| chen2026tsagentsurvey | 377,461 | 1 | Four problem families with architecture, tool and memory analysis; not original GH/GTS boundary |
| xu2026forecastagentsurvey | 377 | 1,3,6 | Three architecture groups and runtime policy/action/tools/memory tuple; adjacent support, not identical seven-way taxonomy |
| tsagent2025 | 418,424,442,499,534 | 3,4 | Iterative ReAct actions, structured observations, evidence log and question-intent gate |
| aion2026 | 418,424,436,444,454,463,472,477,486,530 | 1,4,5 | Task/workspace/validator; six groups; three temporal principles; validity distinct from task score |
| tradingagents2024 | 426,454 | 8 | Structured state and completed report communication protocol |
| timesagemt2026 | 430,509 | 7 | Six-stage runtime, two LLM stages and four deterministic stages; 226 skills/36 categories |
| metacaster2026 | 432 | 5 | Trainer job triplets, queue, GPU assignment, error/restart recovery |
| tsreasoner2026 | 436,442,499 | 2,3,5 | Ordered operator plan, error-triggered end-to-end replanning and bounded retries |
| flairr2025 | 438,525 | 2,3 | Retrieved historical segments and refinement against supplied current-window true targets |
| timeclaw2026explore | 448 | 1,2 | Explore/compare/distill/reinject; frozen base model, reusable experience |
| timeclaw2026harness | 448,463,490,518 | 4 | Native workspace/tools, held-out tool admission and Eq10 episodic memory tuple |
| fincon2024 | 456 | 1,2 | Manager-analyst aggregation for investment tasks |
| batterylake2026 | 488 | 3 | Canonical sample fields, units and charge/discharge current sign |
| ji2025lemad | 488 | 8 | Timestamp alignment, format normalization and missing-value preprocessing |
| calm2025 | 492 | 6,7 | Per-key stateful ordered buffering and gap placeholder insertion |
| mas4ts2026 | 509 | 5,18,22 | Task-indexed candidate chains; shared operators are distinct from task-conditioned routing |
| nexus2026 | 516 | 4,15 | Historical numerical/textual evidence chronological timeline |
| worldreasoner2026 | 532 | 1,2 | Simulated date bounds accessible evidence; post-resolution scoring separated |
| tiem2026 | 532 | 3,5 | Evidence timestamps and resolved provenance ancestors bound skill eligibility |
| timesageev2026 | 532 | 22,23 | Saved skills become callable from the next period |
| duan2025factormad | 534 | 6 | Prompt gate excludes future timestamps and requires rolling rather than full-series statistics |
| tsqbench2026 | 536 | 1,2 | Perceiver dimension selection, Inspector evidence acquisition, Adjudicator pairwise judgment |

agentcybernetics2026: primary source unavailable; remove the present taxonomy-support citation, without labeling the paper false.

## Formula provenance

| Formula | Type | Primary-source locator |
|---|---|---|
| eq:agent-loop | survey_defined | Survey abstraction, introduced explicitly as such |
| eq:timellm-reprogramming | author_formula | jin2024timellm:PDF5 Eq1 |
| eq:chatts-value-preserved | equivalent_survey_restatement | chatts2025:PDF5 Section3.4.2 |
| eq:timer1-reward | author_formula | timer12025:PDF4 Eq3 |
| eq:stride-fusion | author_formula_combination | stride2026:PDF4 Algorithm1; PDF5–6 Section3.4 |
| eq:chatad-tkto | author_formula | chatad2026:PDF5 Eqs4–5 |
| eq:temporal-availability | survey_defined | Survey abstraction, introduced explicitly as such |
| eq:tsci-curator | equivalent_survey_restatement | timeseriesscientist2025:PDF5 Eq1 and following text |
| eq:timeclaw-memory | author_formula_with_renamed_task_symbol | timeclaw2026harness:PDF4 Eq10 |

## Comparative paragraphs

Comparative endings in Sections 3–5 articulate design implications (choice of learned role, reuse object, action interface, timing of feedback, and validation location). They do not report new measured advantages. Retain this distinction: the source supports the mechanism; suitability for a new application is the survey synthesis. The evidence-grounding/faithfulness/action-quality paragraph is an evaluation recommendation, not a claimed experimental result.

## Limits

- No code execution or reproduction of the cited experiments.
- No new scientific claims verified solely from comparative synthesis prose.
- Illustration visual/source fidelity is assigned to the separate figure audit.
