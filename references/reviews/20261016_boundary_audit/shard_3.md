# Boundary audit — shard 3

Reviewed 46 assigned records and 100 existing module IDs. Decisions: {'keep': 95, 'change': 5}. No modules were added or deleted.

Review used primary-source method passages and adjacent context on the pages recorded for each module; these records do not claim code execution or empirical cross-task transfer. Official resource URLs were recovered from author availability statements and PDF hyperlink annotations. Links to cited baselines were excluded.

## Proposed changes

- **tsagent2025:intent-evidence-gate**: GTS → TSK. The implemented gate maps question keywords to fixed intent classes, required predicates and answer schemas, including MCQ anomaly-location options. This concrete validator is bound to temporal question answering, so its deepest scope is TSK.
- **hierarchicalmeteorologist2025:multiscale-context**: GTS → TSK. The recorded context mode includes weather-specific aggregate choices and a forecast-lead-time rule that adds or omits hourly grids at five days. As recorded, this is a forecast-report context policy, not only a generic resampling primitive.
- **siren2026:case-analogy**: TSK → GH. Appendix K.2 supplies the actual instruction: inspect a collection, rank by task intent/conditions and case metadata, retain at most six question-answer examples, then resume solving. Target task and historical collection are placeholders; no warning-specific score or temporal eligibility calculation is implemented in this retrieval template. Retain temporal/event fields as case metadata and task tags, while classifying this concrete orchestration pattern as GH.
- **siren2026:warning-skill-rehearsal**: TSK → GH. The complete rehearsal/refinement prompts hide the reference answer, execute a selected example, reveal the answer, compare reasoning/tool choices, and retain short procedures while excluding event-specific answers and facts. These are task-placeholder instructions with a reusable procedural-update contract; the implemented update pattern is GH. Unlike FinCon’s fixed investment analyst outputs, this prompt does not require a financial/weather decision variable or task score.
- **fincon2024:manager-analyst**: GH → TSK. The concrete seven analyst roles deliver investment insights to a sole trading manager, including stock selection and risk feedback. The recorded manager-analyst module is task-bound; a generic delegation pattern is an abstraction, not a separate implemented module here.

## Resource checks

25 records have source-linked resources; 21 have no work-specific URL found in the inspected source. {'reachable': 26, 'landing_shell_reachable': 3, 'http_error': 1}

WorldReasoner’s author-provided GitHub URL returned HTTP 404. Anonymous GitHub links returned the application shell only; content availability remains unverified. HydroAgent publishes research artifacts rather than its full execution codebase.

## Per-record review

### tessa2024

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `tessa2024:temporal-features` — **keep**, GTS → GTS; source pages [4]. The numerical extractor computes per-channel features and Pearson inter-variable correlations before annotation selection. Those measurements have no annotation acceptance objective; retain GTS for the numerical extractor only, not the text-feature selection pipeline.
- `tessa2024:annotation-review` — **keep**, TSK → TSK; source pages [6]. The reviewer compares domain terms and generated annotations and feeds corrections to the term extractor and annotator. Its output and acceptance criterion are annotation-specific.
- Resources: `not_found_in_source`.

### timexl2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `timexl2025:prototype-fusion` — **keep**, TSK → TSK; source pages [6]. The fused output is a future discrete-label prediction weighted by a validation-selected alpha; this is a prediction procedure, not a generic modality interface.
- `timexl2025:context-refinement` — **keep**, TSK → TSK; source pages [6]. Reflection explicitly sees prediction ground truth and refines context before encoder retraining; testing uses saved validation-selected reflections. The task-bound feedback warrants TSK.
- Resources: `not_found_in_source`.

### timer12025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `timer12025:grip-forecast-reasoner` — **keep**, LLM → LLM; source pages [5]. GRIP optimizes the LLM policy over reasoning trajectories using forecast rewards and policy gradients. The changed object is model parameters, so retain LLM despite the forecasting objective.
- Resource (repository): https://github.com/ustc-time-series/Time-R1 — reachable; PDF p.1 hyperlink annotation.

### yeh2025empowering

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `yeh2025empowering:dataset-proposal-loop` — **keep**, TSK → TSK; source pages [2]. Dataset proposals are ranked by forecaster validation performance and refined until no candidate improves it. This makes the dataset-selection loop forecast-specific rather than general data management.
- Resource (project): https://sites.google.com/view/ts-agent — reachable; PDF p.1 source availability statement.

### calm2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `calm2025:event-windowing` — **keep**, GTS → GTS; source pages [6]. Per-key ordered buffers and watermark timers preserve event order and completeness for downstream windows. They do not depend on a forecast loss or anomaly decision.
- `calm2025:stream-model-swap` — **keep**, GH → GH; source pages [8]. Artifact-path monitoring and callbacks reload weights in flight. This is generic deployment/state coordination; temporal prediction determines the loaded model, not the swapping mechanism.
- `calm2025:drift-curation` — **keep**, TSK → TSK; source pages [8]. Detected forecast outliers are judged KEEP/REMOVE to select fine-tuning examples. The decision is bound to adaptive forecasting under drift, rather than generic reflection.
- Resources: `not_found_in_source`.

### counts2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `counts2025:rvq-tokenization` — **keep**, LLM → LLM; source pages [5]. The tokenizer extends the LLM vocabulary with temporal and scale tokens, and trains their embeddings. This modifies the model-facing representation.
- `counts2025:dapo-reasoning` — **keep**, LLM → LLM; source pages [5]. DAPO changes the LLM policy after SFT to generate temporal reasoning traces. An optimization algorithm applied to model weights is LLM-side, not external Harness evolution.
- Resources: `not_found_in_source`.

### tsagent2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `tsagent2025:evidence-loop` — **keep**, GH → GH; source pages [4]. The state consists of query, action history and evidence log, and each returned tool observation drives the next action. No temporal predicate is required for this reusable loop.
- `tsagent2025:analytical-operators` — **keep**, GTS → GTS; source pages [4]. The APIs summarize, slice, resample and query native series with structured numerical outputs. The temporal operations are separable from the question-answering acceptance gate.
- `tsagent2025:intent-evidence-gate` — **change**, GTS → TSK; source pages [5]. The implemented gate maps question keywords to fixed intent classes, required predicates and answer schemas, including MCQ anomaly-location options. This concrete validator is bound to temporal question answering, so its deepest scope is TSK.
- Resources: `not_found_in_source`.

### epidemicagent2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `epidemicagent2026:hfmd-context-interface` — **keep**, TSK → TSK; source pages [6]. The context interface returns a transmission-impact score and confidence under a disease-specific evidence hierarchy and lag policy. Its semantics are HFMD forecasting, not a general timestamp interface.
- `epidemicagent2026:hfmd-probabilistic-forecast` — **keep**, TSK → TSK; source pages [7]. The forecast maps a one-week HFMD mean and uncertainty into a calibrated count distribution using epidemic volatility. Its horizon and distributional output fix the task.
- Resources: `not_found_in_source`.

### timeart2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `timeart2026:react-runtime` — **keep**, GH → GH; source pages [3]. The Query/Thought/Action/Observation/Final transition is a ReAct interface controlled by tool descriptions and parsers. Temporal contents enter through separately recorded tools.
- `timeart2026:atomic-time-tools` — **keep**, GTS → GTS; source pages [3]. The atomic inventory includes temporal statistics and correlations with composable parameters. Retain GTS for these shared numerical operations; forecasting and anomaly-tool outputs should not be interpreted as generic task-independent results.
- `timeart2026:tool-reasoner-training` — **keep**, LLM → LLM; source pages [5]. Qwen3 LoRA learns expert and contrastive self-reflection trajectories; the parameter update changes tool-use behavior in the LLM.
- Resources: `not_found_in_source`.

### temporalbench2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `temporalbench2026:event-conditioned-evaluation` — **keep**, GTS → GTS; source pages [4]. The dataset transformation fixes historical/future exposure and event boundaries across understanding and forecasting tasks. Retain GTS as a shared evaluation protocol, with role=evaluation; individual task label/scoring rules are task-bound and must not be claimed as reusable operations.
- Resource (dataset): https://huggingface.co/datasets/Melady/TemporalBench — reachable; PDF p.1 hyperlink annotation.
- Resource (leaderboard): https://huggingface.co/spaces/Melady/TemporalBench_Leaderboard — reachable; PDF p.1 hyperlink annotation.

### castr12026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `castr12026:state-memory` — **keep**, GH → GH; source pages [4]. Incremental state summarization and retention separate what is stored from the action chosen. The state mechanism accepts tool outputs and history without requiring a particular forecast score.
- `castr12026:forecast-workflow` — **keep**, TSK → TSK; source pages [5]. Preparation, forecast generation and refinement form an output-bound numerical forecasting workflow; model selection and stopping depend on that contract.
- `castr12026:forecast-policy-training` — **keep**, LLM → LLM; source pages [5]. SFT on tool trajectories followed by reinforcement learning updates the forecasting policy itself, rather than only prompts or stored experience.
- Resource (repository): https://github.com/Xiaoyu-Tao/Cast-R1-TS — reachable; PDF p.1 hyperlink annotation.

### sagesleep2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `sagesleep2026:temporal-query` — **keep**, GTS → GTS; source pages [2, 3]. Source pages 2–3 normalize timestamps/types and generate period/comparison/metric queries over precise records. Retain GTS for the queryable time-series layer, excluding the sleep-specific fields and notification policy from the reusable claim.
- `sagesleep2026:sleep-monitor` — **keep**, TSK → TSK; source pages [2, 3]. Daily templates trigger notifications from personal-baseline deviations and sleep debt. These thresholded health-monitoring decisions are task-specific.
- Resources: `not_found_in_source`.

### treeofevidence2026

No counted modules in assignment snapshot; preserve exclusion and do not add a contribution. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- Resources: `not_found_in_source`.

### sagead2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `sagead2026:dual-representation` — **keep**, GTS → GTS; source pages [4]. Raw values remain accessible to numerical tools while the LLM receives statistics, samples and extrema-preserving indices. This representation split has no detector-specific output predicate.
- `sagead2026:anomaly-evidence` — **keep**, TSK → TSK; source pages [5]. The detector combines anomaly-family analyses, visualizations and confidence rubrics into anomaly intervals/types. Those output requirements bind it to anomaly detection.
- `sagead2026:synthetic-icl` — **keep**, TSK → TSK; source pages [5]. The ICL bank is built from normal segments plus perturbations representing nine anomaly types, and retrieves contrastive anomaly examples. This is not generic experience memory.
- Resources: `not_found_in_source`.

### nexus2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `nexus2026:chronological-context` — **keep**, GTS → GTS; source pages [4]. The Historical Context Agent maps observed values and contemporaneous documents into an indexed timeline before forecasting. The mapping produces historical context without a future target or score.
- `nexus2026:dual-resolution-forecast` — **keep**, TSK → TSK; source pages [4]. Macro and micro agents both produce trajectories over the forecast horizon before synthesis; differing resolution does not make the procedure task-independent.
- `nexus2026:backtest-calibration` — **keep**, TSK → TSK; source pages [5]. Guidelines are generated from forecast errors across chronological folds and admitted by hidden-fold forecast improvement. Keep the complete calibration loop at TSK.
- Resources: `not_found_in_source`.

### kairosagent2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `kairosagent2026:reasoner-training` — **keep**, LLM → LLM; source pages [5]. SFT optimizes assistant tokens including tool calls; later RL assigns credit to the reasoner. These are explicit model-policy changes.
- `kairosagent2026:morphology-fusion` — **keep**, TSK → TSK; source pages [5]. A morphology description is fused into the TSFM hidden space and optimized under quantile forecast loss. The recorded module is numerical forecasting fusion, not an independent generic LLM encoder.
- Resource (project): https://foundation-model-research.github.io/KairosAgent — reachable; PDF p.1 hyperlink annotation.

### timefore2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `timefore2026:sql-repair` — **keep**, GH → GH; source pages [6]. SQL execution errors are returned to the retriever until execution succeeds or a retry cap is reached. This repair loop requires no temporal score.
- `timefore2026:forecast-tool` — **keep**, TSK → TSK; source pages [6]. The predefined tool imputes a history with TimesNet and forecasts twelve months with TimeXer. Its combined input/output contract is forecasting-specific.
- `timefore2026:future-table-evaluation` — **keep**, TSK → TSK; source pages [7]. ODTQA-FoRe grades forecasts and forecast-derived table answers using numerical error and item-level answer metrics. Keep the evaluation module tied to those tasks.
- Resource (repository): https://github.com/jensenw1/ODTQA-FoRe — reachable; PDF p.1 hyperlink annotation.

### dast2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `dast2026:oran-profile` — **keep**, GTS → GTS; source pages [3]. Stage 1 creates aligned multichannel plots and summaries of labels, axes and segment behavior before O-RAN semantic judgment. The extraction operation is temporal; O-RAN anomaly criteria enter the separately recorded second stage.
- `dast2026:oran-semantic-detection` — **keep**, TSK → TSK; source pages [3]. Expected interface traffic behavior and a certainty threshold determine which metrics receive visual anomaly localization. The domain knowledge and output interval are detection-specific.
- Resources: `not_found_in_source`.

### neuroagentic2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `neuroagentic2026:counterfactual-control` — **keep**, TSK → TSK; source pages [4]. The control loop simulates magnitude/duration interventions against a safety threshold and chooses an action reducing peak risk. The physical intervention model and safety objective make it TSK.
- Resources: `not_found_in_source`.

### hydroagent2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. Source explicitly says artifact release excludes the full HydroAgent codebase and live execution environment; link is research_artifacts, not runnable code.

- `hydroagent2026:skill-orchestration` — **keep**, GH → GH; source pages [10]. The skill layer stores procedures, the LLM interprets instances, and deterministic tools score and emit artifacts. Retain the execution/responsibility separation as GH, not the flood rules contained in skills.
- `hydroagent2026:flood-prior-skill` — **keep**, TSK → TSK; source pages [10]. Analog flood events, peak-flow/volume intervals, expert rules and physical feasibility define prior flood judgments with human review. The actual skill contract is hydrological forecasting.
- `hydroagent2026:hydrological-scheme` — **keep**, TSK → TSK; source pages [8]. Flood-type thresholds select separately calibrated Xinanjiang parameter sets. This scheme is tied to a specific hydrological model and target.
- Resource (research_artifacts): https://github.com/BaoyingShan0/Open-Research-Data-for-HydroAgent-flood-forecast-paper — reachable; PDF p.26 source availability statement.

### timerlm2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `timerlm2026:recursive-sandbox` — **keep**, GH → GH; source pages [3]. Python REPL observations and recursive sub-model calls operate on externally stored inputs. These control and execution affordances are generic even though the context file contains a series.
- `timerlm2026:anomaly-benchmark` — **keep**, TSK → TSK; source pages [4]. AnomalyXL defines anomaly presence, onset, type, magnitude/channel and localization scores. These validators require anomaly labels and intervals.
- `timerlm2026:anomaly-rl` — **keep**, LLM → LLM; source pages [5]. Full-parameter GRPO updates Qwen using anomaly outcomes and token/failure penalties. It is model-side learning, not a separately learned external tool.
- Resource (repository): https://github.com/OpenTSLM/TimeRLM — reachable; PDF p.1 source availability statement.

### quantimedai2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `quantimedai2026:clinical-feature-loop` — **keep**, TSK → TSK; source pages [9]. The agent revises clinical features and severity weights using proxy-network AUROC/AUPRC, loss and importance. The feedback explicitly optimizes the clinical prediction task.
- Resources: `not_found_in_source`.

### tiem2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `tiem2026:ancestry-gate` — **keep**, GTS → GTS; source pages [3]. The ancestry gate requires every retained skill ancestor to resolve before the decision cutoff. Provenance-time eligibility can be checked independently of financial prediction scoring.
- `tiem2026:catalyst-skill-memory` — **keep**, TSK → TSK; source pages [4]. The skill record includes outcome-revealed catalyst rules, EMA advantage and lifecycle updates after resolution. The memory policy uses catalyst prediction outcomes and remains task-specific.
- Resource (project): https://qwenqking.github.io/Fin_TIEM/ — reachable; PDF p.1 hyperlink annotation.
- Resource (repository): https://github.com/QwenQKing/Fin_TIEM — reachable; PDF p.1 hyperlink annotation.
- Resource (dataset): https://huggingface.co/datasets/QwenQKing/TIEM-dataset — reachable; PDF p.1 hyperlink annotation.
- Resource (dataset): https://huggingface.co/datasets/QwenQKing/TIEM-databases — reachable; PDF p.1 hyperlink annotation.

### scenariodiff2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `scenariodiff2026:scenario-guidance` — **keep**, TSK → TSK; source pages [3]. The recorded hierarchy includes scenario outlooks over the future horizon and anchor values for forecast refinement. Do not relabel the entire compound module GTS merely because its initial historical summaries could be reused.
- `scenariodiff2026:diffusion` — **keep**, TSK → TSK; source pages [3]. Conditional diffusion generates the future target horizon and applies anchor-blended sampling. It is a numerical forecasting component, not LLM adaptation or general training-data synthesis.
- Resource (repository): https://anonymous.4open.science/r/ScenarioDiff_ICDM-2C4C — landing_shell_reachable; PDF p.1 hyperlink annotation.

### metacaster2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `metacaster2026:job-execution` — **keep**, GH → GH; source pages [5]. The queue schedules model/configuration/dataset jobs, monitors processes and recovers failures until empty. The scheduler can operate independently of forecast selection loss.
- `metacaster2026:generation` — **keep**, TSK → TSK; source pages [2]. MGAgent synthesizes training series from a support set and context to train lightweight forecasters. The generated artifact and downstream learner define the synthesis task.
- `metacaster2026:harness-optimization` — **keep**, TSK → TSK; source pages [5]. Harness edits optimize a hinge discrepancy of forecaster errors on authentic versus generated data. The meta-loop is bound to this synthesis/forecasting objective despite using a general editing pattern.
- Resource (repository): https://github.com/D2I-Group/metacaster — reachable; PDF p.1 hyperlink annotation.

### hierarchicalmeteorologist2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `hierarchicalmeteorologist2025:multiscale-context` — **change**, GTS → TSK; source pages [3]. The recorded context mode includes weather-specific aggregate choices and a forecast-lead-time rule that adds or omits hourly grids at five days. As recorded, this is a forecast-report context policy, not only a generic resampling primitive.
- `hierarchicalmeteorologist2025:weather-report` — **keep**, TSK → TSK; source pages [3]. Meteorologist and Writer must return weather summaries, proofs, keywords and warnings grounded in forecast tables. The report schema and meteorological interpretation define the task.
- `hierarchicalmeteorologist2025:api-reliability` — **keep**, GH → GH; source pages [4]. Caching payloads, retrying external APIs, validating JSON and reporting degraded fallback status are generic execution reliability operations. Weather providers instantiate them without changing their control structure.
- Resources: `not_found_in_source`.

### fromnewstoforecast2024

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `fromnewstoforecast2024:news-conditioned-lora` — **keep**, LLM → LLM; source pages [5]. Supervised instruction tuning with LoRA updates the forecasting LLM on series/news input-output pairs. This is a model change despite contextual retrieval elsewhere.
- `fromnewstoforecast2024:news-reflection` — **keep**, TSK → TSK; source pages [7]. The evaluator receives forecast ground truth and errors on validation windows and updates news-selection logic. The relevance policy is optimized for forecasting, not general document retrieval.
- Resource (repository): https://github.com/ameliawong1996/From_News_to_Forecast — reachable; PDF p.1 hyperlink annotation.

### siren2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `siren2026:guarded-code-server` — **keep**, GH → GH; source pages [4, 5, 6, 8]. An isolated code server validates tool calls and path access and returns structured observations. These are domain-independent execution boundaries.
- `siren2026:case-analogy` — **change**, TSK → GH; source pages [4, 5, 6, 8, 16, 17]. Appendix K.2 supplies the actual instruction: inspect a collection, rank by task intent/conditions and case metadata, retain at most six question-answer examples, then resume solving. Target task and historical collection are placeholders; no warning-specific score or temporal eligibility calculation is implemented in this retrieval template. Retain temporal/event fields as case metadata and task tags, while classifying this concrete orchestration pattern as GH.
- `siren2026:warning-chain-benchmark` — **keep**, TSK → TSK; source pages [4, 5, 6, 8]. The benchmark decomposes operational warning chains and grades MC/NR/GL/OG outputs plus completion/execution. Its acceptance contract is warning-procedure evaluation.
- `siren2026:warning-skill-rehearsal` — **change**, TSK → GH; source pages [4, 5, 6, 8, 16, 17]. The complete rehearsal/refinement prompts hide the reference answer, execute a selected example, reveal the answer, compare reasoning/tool choices, and retain short procedures while excluding event-specific answers and facts. These are task-placeholder instructions with a reusable procedural-update contract; the implemented update pattern is GH. Unlike FinCon’s fixed investment analyst outputs, this prompt does not require a financial/weather decision variable or task score.
- `siren2026:hazard-model-development` — **keep**, TSK → TSK; source pages [4, 5, 6, 8]. Historical weather cases become train/validation samples for a predictor consumed by operational warning decisions. The task-specific sample construction and target bind this module to TSK.
- Resource (repository): https://anonymous.4open.science/r/SIREN-5CE8/ — landing_shell_reachable; PDF p.2 hyperlink annotation.

### gridmind2025

No counted modules in assignment snapshot; preserve exclusion and do not add a contribution. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- Resources: `not_found_in_source`.

### collmllight2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `collmllight2026:traffic-coordination` — **keep**, TSK → TSK; source pages [3]. The graph/history contains lanes, queues and activated signals, and the output is a signal chosen for network flow. Both state and action semantics are traffic-control specific.
- `collmllight2026:complexity-routing` — **keep**, TSK → TSK; source pages [4]. Reasoning depth is routed by the number of congested neighboring lanes. This is a traffic-risk condition, not a generic cost-based router.
- `collmllight2026:simulation-sft` — **keep**, LLM → LLM; source pages [4]. Simulation generates future traffic states and selected signals; SFT minimizes token loss and feedback refines the LLM. The changed artifact is the model policy.
- Resource (repository): https://github.com/usail-hkust/CoLLMLight — reachable; PDF p.1 hyperlink annotation.

### chow2024tsreasoning

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `chow2024tsreasoning:ts-encoder` — **keep**, LLM → LLM; source pages [2]. Patch self-attention and a linear projection map numerical inputs to Mistral embeddings, with scale metadata in text. The interface is a learned model component.
- `chow2024tsreasoning:cot-sft` — **keep**, LLM → LLM; source pages [3]. End-to-end LoRA tunes encoder/projection/LLM on reasoning tasks and chain-of-thought supervision. This is LLM-side adaptation.
- Resources: `not_found_in_source`.

### chang2024llm4ts

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `chang2024llm4ts:temporal-embeddings` — **keep**, LLM → LLM; source pages [7]. Patched series use trainable convolutional token encoding plus temporal/position encodings to match a pretrained LLM. The contribution modifies model representations.
- `chang2024llm4ts:two-stage-adaptation` — **keep**, LLM → LLM; source pages [6]. Autoregressive time-series alignment and forecasting fine-tuning optimize the pretrained backbone and adapters. The training target does not turn parameter adaptation into a Harness module.
- Resource (repository): https://github.com/blacksnail789521/LLM4TS — reachable; PDF p.2 hyperlink annotation.

### wang2025agentic

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `wang2025agentic:route-cost-memory` — **keep**, TSK → TSK; source pages [4]. Memory stores route-specific experienced costs and EWMATT, then conditions the next route choice. The retrieval quantities are bound to travel decisions.
- `wang2025agentic:route-simulation` — **keep**, TSK → TSK; source pages [6]. The day-to-day loop loads chosen routes, computes network travel costs and replans. Its environment transition and action space define a transportation decision simulator.
- Resource (repository): https://github.com/georgewanglz2019/LLMTraveler — reachable; PDF p.1 hyperlink annotation.

### fincon2024

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `fincon2024:manager-analyst` — **change**, GH → TSK; source pages [5, 6]. The concrete seven analyst roles deliver investment insights to a sole trading manager, including stock selection and risk feedback. The recorded manager-analyst module is task-bound; a generic delegation pattern is an abstraction, not a separate implemented module here.
- `fincon2024:risk-aware-portfolio` — **keep**, TSK → TSK; source pages [3, 5, 6]. Portfolio weights solve mean-variance allocation constrained by buy/sell/hold decisions. The risk objective, exposure constraints and output are explicit financial decisions.
- `fincon2024:verbal-reinforcement` — **keep**, TSK → TSK; source pages [5, 6]. Conceptual verbal reinforcement compares profitable and losing trading episodes and adjusts prompts using overlap of trading actions. This external update is task-specific, not LLM weight training.
- Resource (repository): https://github.com/The-FinAI/FinCon — reachable; PDF p.1 hyperlink annotation.

### physiologicalagent2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `physiologicalagent2025:orchestrator` — **keep**, GH → GH; source pages [3]. The planner/executor/data-pipe/response generator support dynamic replanning and arbitrary domain tools. The source explicitly separates this openCHA orchestrator from predefined health tasks.
- `physiologicalagent2025:ppg-pipeline` — **keep**, TSK → TSK; source pages [4]. The PPG processing stages estimate heart rate using signal-quality and reconstruction operations. The adopted pipeline remains a task-specific component; its presence is not evidence of a newly invented HR estimator.
- Resource (repository): https://github.com/mohammadfeli/CHA-PPGHR — reachable; PDF p.1 source availability statement.

### heraldlight2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `heraldlight2025:herald-timing` — **keep**, TSK → TSK; source pages [3]. Queue release-time and approaching-vehicle calculations choose phase duration under traffic constraints. These are task-specific control calculations.
- `heraldlight2025:critic-score-training` — **keep**, LLM → LLM; source pages [4]. The critic scores erroneous/corrected actions and Lscore updates the LLM-Agent. The training module is LLM-side even though data originate from a control environment.
- Resource (repository): https://github.com/BUPT-ANTlab/HeraldLight — reachable; PDF p.1 source availability statement.

### elliottagents2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `elliottagents2025:wave-analysis` — **keep**, TSK → TSK; source pages [3]. The analyst detects Elliott wave structures in stock histories and the backtester checks prediction behavior. This domain-specific pattern procedure supports trading/forecasting.
- `elliottagents2025:hierarchical-delegation` — **keep**, GH → GH; source pages [5]. The source describes hierarchical decomposition, asynchronous delegation and return of results in domain-independent terms. Retain GH as an instantiated coordination pattern, but do not assert that generic scaling claims are measured innovations.
- Resources: `not_found_in_source`.

### curalight2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `curalight2026:priority-lora` — **keep**, LLM → LLM; source pages [3]. Priority-scored interactions train Gemma LoRA adapters with an autoregressive objective. This is explicit model adaptation.
- `curalight2026:traffic-debate-curation` — **keep**, TSK → TSK; source pages [4]. The critic filters phase-duration candidates and defender/consensus LLMs assess congestion consequences. This orchestration is bound to traffic-control actions and training-data curation.
- Resource (repository): https://anonymous.4open.science/r/CuralightCode-6437/ — landing_shell_reachable; PDF p.1 source availability statement.

### finrldeepseek2025

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `finrldeepseek2025:news-action-modulation` — **keep**, TSK → TSK; source pages [2]. LLM stock recommendations multiply PPO trading actions using fixed factors tied to signal and action direction. This external integration is a task-specific decision rule.
- `finrldeepseek2025:risk-return-modulation` — **keep**, TSK → TSK; source pages [2]. Daily stock risk scores are portfolio-weighted and alter the financial risk-sensitive policy. No LLM parameter update is established by this module.
- Resource (repository): https://github.com/benstaf/FinRL_DeepSeek — reachable; PDF p.1 hyperlink annotation.

### hydroagentcalibration2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `hydroagentcalibration2026:calibration-tools` — **keep**, TSK → TSK; source pages [4, 5]. The tool environment edits hydrological parameters, runs EF5 and stops by NSE improvement/thresholds or budget. These tool contracts are calibration-specific.
- `hydroagentcalibration2026:simulator-rl` — **keep**, LLM → LLM; source pages [4, 5]. SFT and full-parameter GRPO train Qwen using simulation error rewards. Numerical simulation is the verifier for a model-policy update.
- Resources: `not_found_in_source`.

### castflow2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `castflow2026:temporal-profiler` — **keep**, GTS → GTS; source pages [5, 6]. The profiler computes statistics, spectral entropy, dropout ratios and boundaries on the observed series. Keep GTS for these independent measurements, not the downstream forecast-clipping policy.
- `castflow2026:forecast-strategies` — **keep**, TSK → TSK; source pages [5, 6]. Stored trajectories are selected by future-horizon MSE and retrieved to guide forecast planning. The experience criterion and final output are forecasting-specific.
- `castflow2026:forecast-reasoner` — **keep**, LLM → LLM; source pages [5, 6, 7]. The paper describes selective fine-tuning of the forecasting language-model module while freezing planning and reflection. This is model adaptation rather than only runtime routing.
- Resource (repository): https://github.com/Forever-Pan/CastFlow — reachable; PDF p.1 hyperlink annotation.

### memcast2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `memcast2026:forecast-experience` — **keep**, TSK → TSK; source pages [3]. Experiences encode forecast outcomes, reasoning and temporal features on training data and update confidence without weight training. Their semantics and validity are tied to forecasting.
- `memcast2026:forecast-reflection` — **keep**, TSK → TSK; source pages [5]. Retrieved validated forecast trajectories guide candidate forecasts and law-based reflection. Selection compares forecasting reasoning against stored experience, not a general memory interface.
- Resource (repository): https://github.com/Xiaoyu-Tao/MemCast-TS — reachable; PDF p.1 hyperlink annotation.

### wang2026large

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `wang2026large:temporal_preprocessing` — **keep**, GTS → GTS; source pages [4]. Differencing and window construction operate on numerical streams before detection prompting. Their transformations are independent of the anomaly acceptance rule.
- `wang2026large:reflection_library` — **keep**, GH → GH; source pages [5]. Stored self-evaluation suggestions modify later prompts via a general answer-quality/reflection request. Retain GH for this external prompt library, excluding task-specific enhancement policies.
- `wang2026large:detection_prompt` — **keep**, TSK → TSK; source pages [5]. The enhancement options and BRIDOR prompt direct anomaly detection on power-equipment series. The final instruction and evidence are detection-specific.
- Resources: `not_found_in_source`.

### auraforecaster2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer. No official work-specific implementation/project/dataset URL found in extracted full text or PDF hyperlink annotations; related-work URLs were excluded.

- `auraforecaster2026:market_sandbox` — **keep**, TSK → TSK; source pages [3]. The sandbox fixes stock/date/horizon and terminates with a return prediction; market-query parameters and observations support that contract. The whole sandbox is not a generic temporal data API.
- `auraforecaster2026:forecast_posttraining` — **keep**, LLM → LLM; source pages [7]. Assistant-token SFT followed by PPO with realized-return reward changes Qwen parameters and its tool policy. Keep LLM separate from the market environment.
- Resources: `not_found_in_source`.

### futuresim2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `futuresim2026:event_replay` — **keep**, TSK → TSK; source pages [4]. The environment advances dates and accepts probability forecasts for active resolving questions. Its temporal replay is inseparable from forecast registration/resolution in this recorded module.
- Resource (project): https://openforecaster.github.io/futuresim — reachable; PDF p.1 hyperlink annotation.
- Resource (repository): https://github.com/OpenForecaster/futuresim/tree/main — reachable; PDF p.1 hyperlink annotation.

### worldreasoner2026

Scope decisions concern the concrete recorded module; examples of use do not establish empirical cross-task transfer.

- `worldreasoner2026:forecast_evidence_evaluation` — **keep**, TSK → TSK; source pages [4]. Outcome accuracy, source overlap and hindsight-graph matching grade event forecasts. The evaluator is task-specific and reference alignment must not be renamed causal-ground-truth proof.
- `worldreasoner2026:temporal_gateway` — **keep**, GTS → GTS; source pages [5]. A dated-repository gateway excludes records after the query cutoff before forecast scoring. This is a reusable availability-time filter with role=infrastructure.
- Resource (repository): https://github.com/cyzus/worldreasoner/ — http_error; PDF p.1 hyperlink annotation.
