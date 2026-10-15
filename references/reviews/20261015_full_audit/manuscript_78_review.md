# Sections 7–8 manuscript review

Reviewed `main.tex` lines 672–827 on 2026-10-15. Read current text, all relevant shard-review records and initial-nine records; rechecked source pages for AION, TimeSeriesGym, TimeClaw exploratory execution learning, ChatTS, TSAQA and MMTS-Bench. Extracted text from all five figures used in these sections and visually inspected Figure7/Figure8. This report does not modify the manuscript.

## Overall assessment

The revised prose has a coherent construction → evaluation → future questions sequence. Existing time-series Agent benchmarks are now acknowledged with concrete protocols rather than dismissed as QA. Most benchmark counts and method descriptions agree with the source audit. The main remaining problems are **old figure content paired with new captions**, an underexplained distinction between the two TimeClaw papers, and insufficiently precise separation of ModernTSF's documented infrastructure from the proposed Agent integration.

## Required corrections

### 1. TimeClaw figure is attributed to the wrong paper

- Location: lines 762–767, `support_pdf/timeclaw_runtime_native.pdf`.
- Sentence: “The TimeClaw experience workflow ... adds a maintenance question ... Alternative trajectories are executed and scored, then useful experience is distilled into an external state.” Caption cites `timeclaw2026explore`.
- Actual figure text: “Contextual series”, “Time-series runtime / server-side numerical execution state and tools”, “Capability evolution / evaluate, update, retain, release”, “Multimodal memory / retrieve and reuse”. These depict the **TIMECLAW Harness** narrative, not Explore–Compare–Distill–Reinject. There are no alternative executions, comparison scores, distilled rules or inference reinjection in this figure.
- Recommended fix: keep the current figure with `timeclaw2026harness` and introduce it immediately after line 758. Describe its numerical workspace, temporal tools and multimodal memory. In the case-analysis prose, cite `timeclaw2026explore` under its full distinguishing title. If retaining an explore figure here, replace its editable PPT contents with the actual four-stage procedure and re-export; changing the caption alone cannot fix the mismatch.
- Source: `timeclaw2026explore.pdf`, pp.3–6, Fig.1/Eqs.1–4; `initial_9_review.json` provides separate Harness evidence.

### 2. Figure8 contradicts the new section and conflates the TimeClaw papers

- Location: lines 797–803, `Figure8_open_problems_native.pdf`.
- Sentence: “The path from model-side understanding through state, tools, and task outputs shows where a new capability must connect ...”. The figure has no such path; it has a five-row issue list, three case cards and a Paper Card schema strip.
- Actual card: “TimeClaw — GTS runtime — Temporal tools, auditable trajectories, memory, and capability evolution become executable.” The section's case is now the **GH experience-update** contribution from `timeclaw2026explore`.
- Actual issue rows (“Temporal and numerical faithfulness”, “Interface standardization”, “Safe component evolution”, etc.) differ from the five revised open-problem paragraphs.
- Actual ModernTSF card says “Models, datasets, artifacts, budgets, and recoverable execution”. No checked source supports attributing budgets and recoverable execution to ModernTSF.
- Recommended fix: edit the PPT to match the five present paragraphs and label the middle case “TimeClaw: exploratory execution learning — GH experience update”. Use “Forecasting models and data interfaces” for ModernTSF unless additional repository evidence is obtained. Remove the Paper Card/schema strip from this main-text overview, consistent with moving card documentation to the appendix. Describe the resulting diagram as a map, not a path unless arrows are actually drawn.

### 3. Figure7 reading guide and aggregation imply unsupported structure

- Location: lines 690–695, `Figure7_infrastructure_native.pdf`.
- Sentence: “Figure ... connects the three construction layers to their observable evidence. Read it from the final task result back to the operations and data that produced it.”
- Actual figure columns: “Inputs and skills”, “Challenge suite”, “Outputs and evidence”. These are an evaluation workflow, not GH/GTS/TSK construction layers. The lower strip ends in “Holistic score / task outcome + executable artifact + episode record”, suggesting an undefined combined score.
- Recommended replacement prose: “Figure ... follows an evaluation episode from accessible resources, through the challenge specification and grader, to the submitted artifacts and execution record. Numerical scores describe task performance; traces and artifact checks explain how the result was obtained.”
- PPT edits: replace “Holistic score” with “Evaluation report”; retain the three evidence types as separately reported observations. Replace “Skill simulators” with “Analytical operations” unless a simulator really exists. Add a caption attribution that this is the survey's synthesis informed by AION and TimeSeriesGym. The numerical/textual score is not a new unified metric.

### 4. TimeSeriesGym figure adds trace grading not established by the cited protocol

- Location: lines 701–707, `timeseriesgym_benchmark_native.pdf`.
- Figure says “Qualitative grader: trace and artifact review”. Source p.6 defines valid submission as any non-null grader score and reasonable submission using challenge-specific conditions; source p.5 describes quantitative/qualitative artifact grading. It does not establish routine full Agent trace review as the defining qualitative criterion.
- Fix figure label to “Qualitative grader: task-specific artifact checks”, or reproduce the source's actual artifact examples. Caption and current prose about “validity and task performance” can remain.
- Change prose “default budget of four hours **or** 50 steps” to “default limits of four hours and 50 steps”; source p.6 reports joint resource setting `4 / 50`, not alternative configurations.

### 5. ModernTSF case should explicitly present the Agent-facing use as the survey's design application

- Locations: lines 760, 827; duplicate repository footnote.
- Sentences: “ModernTSF ... supplies a forecasting infrastructure case around callable model and dataset resources and reproducible runs.” “The Agent selects a model, configuration, and data window; the numerical substrate executes that request and returns results and artifacts.”
- Evidence level: repository/infrastructure only; no verified Agent benchmark or native autonomous workflow. The second sentence can read as an implemented ModernTSF Agent interface.
- Suggested integrated wording: “ModernTSF provides a forecasting software substrate. An Agent integration can expose its model and data routines as tools with explicit model, configuration, and window arguments. Recording these calls and their resulting artifacts supports comparisons between direct forecasting and context-informed revision.” Use present tense for documented repository features and “can” for the proposed integration; no defensive disclaimer paragraph is needed. Keep one repository footnote and cross-reference that case later.
- Remove the unsupported “budgets and recoverable execution” claim in Figure8 and the appendix illustrative row (currently line 935) as part of cross-manuscript consistency.

### 6. TimeClaw equations are source-faithful, but the explanation omits essential symbols and learning stage

- Location: lines 810–825.
- Confirmed: `q=-L_tau`, best valid execution, Summarize, Clean, Distill exactly match source pp.3–4, Eqs.1–4.
- Add immediately with first equation: “During exploration, `y*` is the observed task target, `L_tau` is the task loss, and `Pi_valid(x)` contains executions satisfying the output contract.” This makes clear why target-based scoring is available without implying target access during deployment.
- Define `A_s^(m)` as task-local retained experience, `s` as the task and `m` as update index. Follow with the source-supported fact: “At inference, the system retrieves applicable rules from the fixed learned state.” Source p.6 explicitly separates exploration from inference.
- Replace “is recorded as General Harness” with “The reusable contribution is the execution-comparison and experience-update procedure.” The current ledger wording interrupts the method explanation with administrative classification.
- Distinguish names at first occurrence: “TIMECLAW (Harnessing Generalist Agents for Contextualized Time Series)” versus “TimeClaw: A Time-Series AI Agent with Exploratory Execution Learning”. Capitalization alone does not reliably tell the reader these are different works.

### 7. Add missing local citation for next-period skill activation

- Location: line 791, last sentence: “TimeSage-EV's next-period skill activation provides ...”.
- Fix: “TimeSage-EV \\citep{timesageev2026} activates accepted skills from the following period, providing a concrete way to test when acquired procedures become available.”
- Source: TimeSage-EV PDF p.24, “Chronological registration.” This claim is correct but deserves its citation directly after the method name.

## Coverage and detail improvements

### QA subsection can be concrete without becoming another benchmark taxonomy

Line 745 currently compresses TSAQA/MMTS-Bench to one general sentence. Rechecked the first three PDF pages:

- TSAQA includes six analytical tasks (anomaly detection, classification, characterization, comparison, data transformation, temporal relationship), 210k examples, thirteen domains and TF/MC/puzzling output formats.
- MMTS-Bench has 2,424 QA pairs in Base, InWild, Match and Align; it tests structural/feature perception, temporal reasoning, sequence matching and cross-modal alignment.

Two or three source-specific sentences would show exactly what a designer learns from each. Avoid the claim that QA cannot test time-series tasks at all: it tests selected task capabilities via a constrained answer format. The current revised concluding interpretation of QA as a measurable capability in a larger workflow is appropriate.

### Benchmark coverage is strongest for forecasting/analysis, weaker for synthesis/decisions

The selection table covers engineering, contextual forecasting, recurring analysis, diagnosis and data quality. It does not directly cover the synthesis or decision-support task families introduced in Section6. This is a selection coverage gap, not evidence that the existing table is false. Add a short selection paragraph grounded in already reviewed methods: synthesis requires fidelity/diversity and downstream utility; control/trading requires sequential action utility under constraints. If the corpus offers no independent benchmark for a family, use its source-specific evaluation protocol and identify the protocol as such. Do not relabel a method's experiment as a standalone benchmark. FutureSim/WorldReasoner can support an adjacent event-forecasting discussion if needed, but are not substitutes for numerical sequence synthesis or deployed control evaluation.

### ChatTS case is correct but can teach a more concrete design decision

Line808 is faithful to ChatTS pp.4–5. One concrete mechanism helps: its five-layer MLP encodes fixed-size temporal patches into the text embedding space, then inserts them at the corresponding series positions among text tokens. That makes the relationship between architecture, temporal context and analytical interaction tangible. Keep normalization metadata alongside this mechanism. The current generic “A suitable comparison...” sentence could be shortened to make room. No ChatTS/TimeClaw source conflation found in the current prose itself.

## Checked claims that can stay

- AION tuple and validator equations: source pp.3–4, Eqs.1–3; the `T_access` notation disambiguates access scope from task tuple appropriately.
- TimeSeriesGym 34 challenges / 23 sources / eight problem types: p.4.
- TimeSage-MT 240 tasks / four levels / eight domains and 226 skills / 36 categories: audited source pp.3–7.
- TimeSage-EV 60 scenarios / six domains / 1,485 instances / snapshot of 24 periods: shard2 evidence. Do not extend this to a guarantee that every externally retrieved webpage is archived pre-cutoff.
- Dr-CiK 240 tasks / 8,849 documents and separation of evidence recovery from forecast quality: shard2, source pp.4–6.
- TFRBench ten datasets / five domains, future-conditioned reference generation and four judge dimensions: shard1, source p.8.
- TraceBench simulator intervention, direct/programmatic submission and exploratory resource metrics: shard1, source pp.3–5.
- TSAG hard-coded function stubs: shard1, source p.3.
- TSQBench quality identification/comparison and downstream subset-selection utility: shard3.
- No blanket “there is no time-series Agent benchmark” claim remains in Sections7–8.

## Writing diagnosis

No pervasive defensive writing remains. The statements explaining what a benchmark measures (e.g. TFRBench's outcome-conditioned references) are necessary interpretation, not defensive caveats. Retain them but state measured quantities positively. The more substantial remaining issue is **figure/text synchronization** and repeated generic evaluation advice in the cases. Give each case its distinctive mechanism, one consequence for construction, and one source-grounded evaluation setting. Do not add another taxonomy or a fresh layer of section-specific labels.
