# Shard 2: source-level module and resource review

46 records; 88 modules. Read module evidence and adjacent method text; deeper page review for boundary cases. Source PDFs/README and source-linked resource pages were inspected, with no repository cloning or code download.

## Decisions

{'keep': 83, 'change': 3, 'exclude': 2}

## tsreasoner2026

- **tsreasoner2026:execution-feedback**: keep (GH → GH); pages [5]. The revised plan is triggered by an execution error and uses the previous program and error message; this retry mechanism does not require a forecasting loss or temporal representation.
- **tsreasoner2026:temporal-toolkit**: keep (GTS → GTS); pages [4]. Section 3 groups 57 model, numerical, retrieval and generated operators behind a common interface, covering imputation and anomaly analysis as well as forecasts. The record denotes the shared temporal tool suite, not a particular forecast operator.
- **tsreasoner2026:forecast-holdout**: keep (TSK → TSK); pages [5]. The last 10% pseudo-holdout provides prediction-quality feedback for choosing forecasters; its acceptance criterion is explicitly tied to a future forecast horizon.
- Resources: source_reviewed
  - repository: https://github.com/wen-ye-xwz/TS-Reasoner — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## timecap2025

- **timecap2025:event-context-retrieval**: keep (TSK → TSK); pages [4]. Nearest neighbours supply paired summaries and event outcomes to the prediction agent; the final output fuses label predictions with encoder logits. Those label and forecast contracts are essential to this module.
- Resources: source_reviewed
  - dataset: https://github.com/geon0325/TimeCAP — reachable; PDF p.2; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.
- PDF pp.2,8 describe the linked repository as dataset release and say code is available upon request; the current fetched GitHub title identifies source code, so preserve the paper-era dataset provenance and current availability separately.

## competitionagents2025

- **competitionagents2025:competitive-news-selection**: keep (TSK → TSK); pages [3]. Agents evolve news-selection logic using forecast MAPE rankings and previous competitive outcomes. The concrete search objective is prediction error, not a task-independent debate protocol.
- **competitionagents2025:llm-forecast-training**: keep (LLM → LLM); pages [3]. Each competitor explicitly fine-tunes its own LLM to predict the next value conditioned on selected news. The changed artifact is model parameters, independent of the surrounding selection harness.
- Resources: source_reviewed
  - repository: https://anonymous.4open.science/r/IA_news_model-D7D6/ — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## timera2025

- **timera2025:rats-sft**: keep (LLM → LLM); pages [4]. The paper maximizes log P_theta(y|x) on RATS40K to update the language model's anomaly labels and reasoning outputs; the module is supervised model adaptation.
- **timera2025:anomaly-evaluation**: keep (TSK → TSK); pages [4]. Binary anomaly labels, anomaly categories and explanation similarity are separately scored. The protocol's outputs and metrics depend on the anomaly-reasoning task.
- Resources: source_reviewed
  - repository: https://github.com/yyysjz1997/Time-RA — reachable; PDF p.1; author release statement or embedded hyperlink
  - dataset: https://huggingface.co/datasets/Time-RA/RATs40K — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## flairr2025

- **flairr2025:refinement**: keep (TSK → TSK); pages [2]. The stored prompt-error history, retrieved segment outcomes, early stopping and chosen best prompt all use MAE and a prediction horizon. General retrieval alone does not describe this coupled module.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## timeomni2026

- **timeomni2026:temporal-reasoning-training**: keep (LLM → LLM); pages [5, 6, 7]. Stage 1 SFT injects human-guided priors and Stage 2 GRPO changes the model policy using task-grounded rewards. This is parameter learning even when the tasks include decisions.
- **timeomni2026:tsr-suite**: change (GTS → LLM); pages [5, 6, 7]. TSR-SUITE is explicitly constructed to develop temporal reasoning models: hierarchical human-reviewed CoT examples become SFT and RL data. As a single existing data-construction record its primary contribution is training_data, consistent with ChatTS; multiple task labels alone do not make it a reusable runtime module. The test split remains recorded as evaluation evidence.
- Resources: source_reviewed
  - repository: https://github.com/AntonGuan/TimeOmni-1 — reachable; PDF p.1; author release statement or embedded hyperlink
  - model: https://huggingface.co/anton-hugging/TimeOmni-1-7B — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## feta2025

- **feta2025:channel-classification**: keep (TSK → TSK); pages [6]. Channel reasoners compare labelled DTW neighbours, emit a class and confidence, and fuse class decisions. Both the candidates and aggregation require a classification label space.
- Resources: source_reviewed
  - repository: https://github.com/SongyuanSui/FETATSC — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## aimeteorologist2025

- **aimeteorologist2025:weather-report**: keep (TSK → TSK); pages [2]. The meteorologist outputs a fixed weather summary, meteorological explanation, confidence and hazard warning, and the writer compiles a bulletin; this output contract defines the specialised procedure.
- **aimeteorologist2025:plot-code**: keep (GH → GH); pages [2]. The illustrator generates matplotlib code for requested parameters and the report renderer compiles plots. The described mechanism is code-generated illustration, with no temporal-specific execution or validation rule of its own.
- Resources: source_reviewed
  - repository: https://anonymous.4open.science/r/ai-meteorologist/ — reachable; PDF p.1; Code link below abstract
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## chatad2026

- **chatad2026:tsevol**: change (TSK → LLM); pages [3, 4, 5]. Sections 4.1.2–4.2 explicitly describe generating time-text instructions for the target MTSLLM, knowledge distillation, and subsequent LoRA SFT. The supervisor's alignment check filters training QA, so the existing module is LLM training_data rather than a deployed anomaly-detection harness.
- **chatad2026:training**: keep (LLM → LLM); pages [3, 4, 5]. LoRA SFT and TKTO alter the model using quality-weighted preferences; they change inference capability through training rather than external runtime state.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## mas4ts2026

- **mas4ts2026:temporal-carriers**: keep (GTS → GTS); pages [3, 4, 5]. Plot anchors contain time indices, values and rising/stable/falling indicators, then condition a continuous latent trajectory. The paper shares this temporal carrier across forecasting, imputation, classification and anomaly tasks while leaving the VLM unchanged.
- **mas4ts2026:shared-memory**: keep (GH → GH); pages [3, 4, 5]. The module's operative update is a confidence-gated fusion of agent hidden states into shared memory. Its equation uses generic embeddings and confidence, not a forecast horizon, temporal validity predicate or task output schema.
- **mas4ts2026:temporal-tools**: keep (TSK → TSK); pages [3, 4, 5]. Section 3.4 routes tools conditioned on task type and checks task-specific shapes, normalisation and output constraints; optimisation uses L_task. This record is the specialised output-producing chain, not the reusable tools in isolation.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## anomamind2026

- **anomamind2026:anomaly-workflow**: keep (TSK → TSK); pages [5]. Coarse localisation narrows suspicious intervals, actors construct interval evidence, and the detector emits anomalous intervals that the evaluator refines. Its intermediate state and stopping judgments are bound to anomaly localisation.
- **anomamind2026:detector-rl**: keep (LLM → LLM); pages [6]. Only the detector policy is fine-tuned with reasoning traces and RL rewards for parsing, F1 and false positives; the surrounding evidence workflow remains separately represented.
- Resources: source_reviewed
  - repository: https://github.com/Xiaoyu-Tao/AnomaMind-TS — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## artist2026

- **artist2026:joint-policy**: keep (LLM → LLM); pages [7]. The same model implements controller and reasoner roles and receives LoRA SFT followed by full-parameter collaborative RL. Segment-selection actions are learned model outputs.
- **artist2026:segment-selection**: keep (TSK → TSK); pages [4]. At each round the controller observes the question, previously selected segments, reasoning and provisional answer, and chooses CONTINUE or ACCEPT. The concrete acquisition policy is tied to answering the current temporal question.
- Resources: source_reviewed
  - repository: https://github.com/mims-harvard/ARTIST — reachable; PDF p.2; author release statement or embedded hyperlink
  - project: https://zitniklab.hms.harvard.edu/ARTIST/ — reachable; PDF p.2; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## tfrbench2026

- **tfrbench2026:reasoning-reference**: keep (TSK → TSK); pages [8]. The evaluator compares forecasting trajectories to future-event-informed reference reasoning using forecast correctness and logic-to-number consistency. The benchmark is defined by a forecasting output and information boundary.
- Resources: source_reviewed
  - benchmark: https://tfrbench.github.io/ — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## tsag2026

- **tsag2026:temporal-tool-interface**: keep (GTS → GTS); pages [2, 3]. The interface specifies temporal analysis functions for patterns, volatility, correlation and valid time units. It is a reusable temporal-tool specification; paper Sections 3.1–3.3 clarify that evaluated functions are hard-coded stubs, so it is not evidence of implemented numerical tool accuracy.
- **tsag2026:stub-evaluation**: keep (GH → GH); pages [2, 3]. Hard-coded responses isolate tool choice and argument extraction from live data and tool computation. Deterministic response checking is a generic tool-calling evaluation technique.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.
- Sections 3.1–3.3 explicitly evaluate deterministic stubs rather than real financial tool implementations; retain as interface specification with no claim of live numerical execution validation.

## timeclaw2026explore

- **timeclaw2026explore:explore-distill**: keep (GH → GH); pages [4]. Exploration generates alternative executions, compares them through a supplied evaluator, removes answer-specific material, and distils external experience. The algorithm's object is execution strategy and it accepts different task losses without changing model parameters.
- **timeclaw2026explore:rule-injection**: keep (GH → GH); pages [6]. Rules store applicability, preferred/avoided tools, evidence, confidence and an injection flag; conflict handling changes runtime guidance. None of those fields prescribes temporal data semantics or a specific answer type.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## drcik2026

- **drcik2026:forecast-research-testbed**: keep (TSK → TSK); pages [4]. Tasks require discovering evidence that improves a contextual forecast, with separate evidence and prediction scoring. The known-support documents and forecast target define this evaluation environment.
- **drcik2026:distractor-construction**: keep (TSK → TSK); pages [6]. Evidence chains and distractors are generated from forecast-supporting context with retained causal/time relationships; chain length controls difficulty for context-aided forecasting, rather than a general corpus-retrieval module.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## lastmile2026

- **lastmile2026:forecast-workspace**: keep (TSK → TSK); pages [3]. Only the future forecast is editable; history and baseline are immutable and edits must remain within the horizon. These state transitions are intrinsically forecast revision.
- **lastmile2026:revision-memory**: keep (TSK → TSK); pages [5]. Memory is written after actual outcomes arrive and records whether an intervention improved the baseline prediction and how its magnitude should change. Its feedback and retrieved lesson are forecast-revision specific.
- **lastmile2026:event-mapreduce**: keep (TSK → TSK); pages [4]. Local reasoners produce edits for event windows of a forecast horizon, then merge them through the constrained forecast workspace. The plans are forecast-edit actions, not generic task decomposition.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## timeclaw2026harness

- **timeclaw2026harness:workspace-tools**: keep (GTS → GTS); pages [4]. Full numerical time-series objects reside in workspace W and temporal tools operate directly on them while returning compact observations. The paper explicitly shares these primitives across tasks.
- **timeclaw2026harness:memory**: keep (GTS → GTS); pages [4]. Memory separately indexes numerical temporal structure and contextual text to avoid scale and token-similarity distortions. This retrieval assumption follows the signal modality and supports different task traces.
- **timeclaw2026harness:tool-promotion**: keep (GH → GH); pages [4]. A candidate executable tool is admitted when held-out execution success exceeds a threshold. The gate operates on externally supplied task results and does not itself encode a temporal or task-specific metric.
- Resources: source_reviewed
  - repository: https://github.com/iDEA-iSAIL-Lab-UIUC/TimeClaw — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## topobrick2026

- **topobrick2026:topology-routing**: keep (TSK → TSK); pages [4]. The sampler selects exogenous predictors for a target building sensor using topology and physical driver categories; its downstream use is zero-shot forecasting of that target.
- **topobrick2026:availability-contract**: keep (TSK → TSK); pages [5]. Past-known covariates are masked over the prediction horizon while schedules/calendar/weather forecasts can be future-known. The concrete masking contract is defined around forecast origin and horizon.
- Resources: source_reviewed
  - repository: https://github.com/Dawnlxc/TopoBrick.git — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## plotstowords2026

- **plotstowords2026:plan-execute**: keep (GH → GH); pages [4]. The executor invokes MCP tools, passes intermediate outputs and obtains knowledge in a stepwise plan. This is general orchestration; the forecast explanation signals are in the separate specialised module.
- **plotstowords2026:model-aware-explanation**: keep (TSK → TSK); pages [5]. SHAP attributions, temporal importance and uncertainty from a specific predictive model ground the generated forecast explanation. Interpretation depends on that forecast and model behaviour.
- Resources: source_reviewed
  - repository: https://zenodo.org/records/19710740 — reachable; PDF p.7; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## oilwellagent2026

- **oilwellagent2026:metric-profile-diagnosis**: keep (TSK → TSK); pages [7]. Observed sensor metrics are compared against known fault-class profiles to output top-three diagnoses, evidence, confidence and novelty names. These required labels and fault profiles determine the module's scope.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.
- PDF p.20 Data availability states code and raw outputs will be released in GitHub with Zenodo DOI upon acceptance; no concrete release URL is given. The 3W dataset is an externally cited source, not this work's code release.

## crafter2026

- **crafter2026:residual-feature-search**: keep (TSK → TSK); pages [3]. Candidate features are accepted only when they explain residual validation error left by the forecast corrector. Both generation and gating are targeted at forecast correction.
- **crafter2026:corrector-selection**: keep (TSK → TSK); pages [5]. An identity, additive or multiplicative corrector is selected by validation wMAPE. Its choices and output are explicitly post-hoc forecast correction.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## aqua2026

- **aqua2026:manager-handoffs**: keep (GH → GH); pages [6]. Every specialist receives a concrete task from the Manager and returns through it; the auditable handoff mechanism is separate from financial factor scoring.
- **aqua2026:sealed-search**: keep (GH → GH); pages [5]. Immutable evaluator/configuration boundaries and validation-only feedback prevent the search from reading final test scores. This generic search-evaluation separation does not require temporal operators; their causal grammar is another module.
- **aqua2026:causal-factor-grammar**: keep (TSK → TSK); pages [5]. The expression-tree registry defines formulaic alpha factors using finance fields, trailing-window operations and cross-sectional ranks. The output and validity contract are financial factor discovery.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## reasoncast2026

- **reasoncast2026:reasoner-posttraining**: keep (LLM → LLM); pages [3]. Schema SFT and semantic-field/forecast-utility RL update Qwen reasoning and routing outputs while the final numerical forecaster is held fixed. The learned object is the language-model policy.
- **reasoncast2026:selective-fusion**: keep (TSK → TSK); pages [3]. Skip/Basic/Tool routing emits event relevance, demand direction, shape and amplitude for fusion into a numerical forecast. Those semantic fields and selective intervention are forecast-specific.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## agenticactivelearning2026

- **agenticactivelearning2026:active-anomaly-ranking**: keep (TSK → TSK); pages [5]. A top-100 anomaly queue is visually labelled and used to update subsequent anomalous-source ranking; metadata and checks target astronomical light-curve anomalies.
- **agenticactivelearning2026:class-conditioned-outliers**: keep (TSK → TSK); pages [4]. Isolation forests are conditioned on variability class, with period/amplitude features and minimum percentile scoring across forests to identify truly unusual sources. This module is an anomaly-ranking method, not a general feature extractor.
- Resources: source_reviewed
  - repository: https://github.com/milanpesta/aal_anomalies_asassn — reachable; PDF p.21; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## moiraiagent2026

- **moiraiagent2026:context-expert-forecast**: keep (TSK → TSK); pages []. The README's two advertised operations refine contextual forecasts and choose among forecasting experts. Both terminate in a forecast; the repository evidence does not establish an independent task-agnostic runtime.
- Resources: source_reviewed
  - repository: https://github.com/SalesforceAIResearch/uni2ts/tree/main/project/moirai-agent — reachable; README paragraphs 1–2; fetched 2026-10-15
  - project: https://www.salesforce.com/blog/moiraiagent — reachable; README release links
  - benchmark: https://huggingface.co/spaces/Salesforce/gift-eval — reachable; README benchmark links
  - dataset: https://huggingface.co/datasets/Salesforce/GIFT-CTX — fetch_failed; README contextual benchmark link
- Reviewed official README, including its blog, benchmark and contextual dataset links; no paper PDF is claimed.

## tsskill2026

- **tsskill2026:skill-qa-benchmark**: keep (TSK → TSK); pages [3]. Timestamp-aware questions and skill-labelled answers define a temporal QA benchmark. Broad signal skills do not change the answer-evaluation task contract.
- **tsskill2026:qa-verification**: keep (TSK → TSK); pages [6]. Verification checks generated QA answers against executable numerical evidence, units and statistics, with human repair of mismatches. It is tied to constructing valid QA pairs.
- Resources: source_reviewed
  - dataset: https://huggingface.co/datasets/Anonymous-Dataset-H/TS-Skill — reachable; PDF p.3; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## forecastcompass2026

- **forecastcompass2026:factor-memory**: keep (TSK → TSK); pages [4]. Resolved forecasting questions update predictive-factor and probability-calibration memory for later unresolved questions. The module's feedback and use are event probability forecasting.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## adagent2025

- **adagent2025:code-review**: keep (GH → GH); pages [3]. Generator/reviewer dry runs repair execution failures using synthetic samples. This correctness loop is applicable to other code-generation domains independently of detector accuracy.
- **adagent2025:documentation-memory**: keep (GH → GH); pages [3]. A shared workspace stores task configurations while long-term cache stores model documentation with periodic refresh. This is documentation/state management rather than time-indexed signal memory.
- **adagent2025:detector-pipeline**: keep (TSK → TSK); pages [2]. Library selection chooses PyOD, PyGOD or TSLib for anomaly detection and produces a detection script. This output procedure is task-specific even though the libraries span modalities.
- Resources: source_reviewed
  - repository: https://github.com/USC-FORTIS/AD-AGENT — reachable; PDF p.2; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## llmlight2025

- **llmlight2025:traffic-controller**: keep (TSK → TSK); pages [3]. Queue and approaching-vehicle counts are converted to prompts whose selected action changes a traffic signal. The observation and action spaces are bound to traffic control.
- **llmlight2025:lightgpt-training**: keep (LLM → LLM); pages [4]. LoRA imitation training learns GPT-4 actions/rationales and critic-guided refinement improves the model control policy. The learned parameters are on the model side.
- Resources: source_reviewed
  - repository: https://github.com/usail-hkust/LLMTSCS — reachable; PDF p.1; author release statement or embedded hyperlink
  - model: https://huggingface.co/lightgpt — reachable; PDF p.1; author release statement or embedded hyperlink
  - project: https://lightgpt2024.github.io/LLMLight_Demo/ — reachable; PDF p.8; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## chatts2025

- **chatts2025:temporal-alignment**: keep (LLM → LLM); pages [5]. A five-layer MLP maps numerical patches into the language embedding space with contextual token insertion. This directly adapts the model's multimodal input representation.
- **chatts2025:synthetic-instruction**: keep (LLM → LLM); pages [5]. Attribute-guided QA evolution and elimination construct the alignment/SFT corpus described in Sections 3.3–3.4. The module contributes training data for the model rather than a deployment-time controller.
- Resources: source_reviewed
  - repository: https://github.com/NetManAIOps/ChatTS — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## jin2024timellm

- **jin2024timellm:patch-reprogramming**: keep (LLM → LLM); pages [4]. The input reprogramming and output projection are trained around a frozen backbone. Model-side adaptation includes these interfaces and does not require changing backbone weights.
- Resources: source_reviewed
  - repository: https://github.com/KimMeen/Time-LLM — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## wawer2025integrating

- **wawer2025integrating:wave-tools**: keep (TSK → TSK); pages [7]. Elliott wave reader, charting and backtesting tools form a technical-market-analysis procedure; the chart tool is explicitly connected to wave detection rather than generic visualisation.
- **wawer2025integrating:investment-synthesis**: keep (TSK → TSK); pages [6]. The investment adviser combines wave analysis and backtests into buy/sell signals, price targets and contingency plans. Those action outputs fix the decision-support scope.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## joshi2025using

- **joshi2025using:scenario-query**: keep (TSK → TSK); pages [5]. The actual proposed setup produces external-scenario questions for revising an interest-rate model. This is a human-mediated forecast-refinement procedure; the source does not demonstrate an autonomous executable Agent loop.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.
- The source describes ChatGPT-generated questions saved in CSV/TSV and human model refinement. Do not describe automated execution, online learning or an autonomous agent as demonstrated.

## multimodaltsad2026

- **multimodaltsad2026:granularity-evaluation**: keep (TSK → TSK); pages [4]. Synthetic point, range and variate anomalies are injected at controlled ratios to compare detection F1. The evaluation depends on anomaly granularity and label definitions.
- **multimodaltsad2026:adaptive-detector**: keep (TSK → TSK); pages [7]. A scanner identifies anomaly type, a planner selects detection methods, and a checker refines anomaly predictions. The adaptive route is determined by the detection task's type and prediction quality.
- Resources: source_reviewed
  - repository: https://github.com/mllm-ts/VisualTimeAnomaly — reachable; PDF p.2; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## tradetonottrade2025

- **tradetonottrade2025:stochastic-discovery**: keep (TSK → TSK); pages [6]. The builder turns SDE candidates into calibrated simulators of stochastic price paths and the critic evaluates that simulation. Its generated artifact is a time-series simulator for subsequent market use.
- **tradetonottrade2025:risk-trading**: keep (TSK → TSK); pages [11]. Recent prices calibrate the SDE, simulated risk/trend metrics and news feed buy/sell/hold decisions, and cash/position updates include costs. This is a concrete trading procedure.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## gridagent2025

Record disposition: background_reference
- **gridagent2025:grid-action-plan**: exclude (TSK → TSK); pages [1, 2, 3, 4, 5, 6, 7]. The planner and power-flow sandbox implement grid-violation remediation, so TSK is locally appropriate. Corpus inclusion is unsupported: Sections III and V use static network states and injected violation scenarios, with no time-series input, forecast horizon or temporally coupled dispatch. Recommend background disposition like GridMind, confirmed by root review.
- **gridagent2025:rollback**: exclude (GH → GH); pages [1, 2, 3, 4, 5, 6, 7]. Snapshot restoration on a failed validator is a general transactional mechanism. However, the underlying paper's experiments are static power-flow violation repair; retaining it as a Time-Series Agent contribution requires a scope decision. Recommend background disposition rather than changing the mechanism's layer.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.
- Sections III and V formulate static network violations and evaluate injected contingency scenarios. The iteration index tracks agent workflow rather than a time-series task; retain as a background comparison consistently with GridMind.

## trafficr12025

- **trafficr12025:traffic-policy-training**: keep (LLM → LLM); pages [4, 5, 6]. Expert-validated action data and offline/online RL fine-tune the LLM traffic policy. Learned control remains a model-side contribution despite its specialised task.
- **trafficr12025:asynchronous-intersections**: keep (TSK → TSK); pages [4, 5, 6]. Road intersections are partitioned by positional parity and neighbouring messages alternate within each traffic-control step. The schedule and communication neighbourhood are tied to the road-control setting.
- Resources: source_reviewed
  - model: https://huggingface.co/Season998/Traffic-R1 — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## atlas2025

- **atlas2025:adaptive-opro**: keep (GH → GH); pages [3]. Adaptive-OPRO optimises instruction text from delayed scalar feedback while retaining runtime interfaces and prompt templates. The update rule is explicitly formulated for interactive settings; financial orders are represented separately.
- **atlas2025:trading-execution**: keep (TSK → TSK); pages [2]. Market/news/fundamental analyses are combined by a trading agent that issues and executes orders. The execution state and reward are financial decisions.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## climateagent2025

- **climateagent2025:persistent-workflow**: keep (GH → GH); pages [5, 6, 7, 8, 9]. JSON context snapshots after each subtask enable resume, reproducibility and debugging. These persistence operations are independent of temporal climate semantics.
- **climateagent2025:task-planning**: keep (GH → GH); pages [5, 6, 7, 8, 9]. The planner decomposes research queries and delegates through a persistent shared context, with retry/error recovery in Algorithm 1. This is general multi-agent workflow orchestration.
- **climateagent2025:climate-workflows**: change (GTS → TSK); pages [5, 6, 7, 8, 9]. CLIMATE-AGENT-BENCH-85 specifies scientific analysis/report workflows, including named phenomenon detectors, derived indices, visualisations and rubric-based outputs. It is an evaluation task suite, not a reusable cross-task temporal operation; domain diversity alone does not warrant GTS. Keep scientific_temporal_analysis as the explicit task value.
- Resources: source_reviewed
  - repository: https://github.com/Relaxed-System-Lab/ClimateAgent — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## smartenergyagent2026

- **smartenergyagent2026:appliance-diagnosis**: keep (TSK → TSK); pages [3]. The context agent must retrieve detector reliability and appliance baselines before routing an alert into inspect-now/normal/LLM diagnosis paths. Its conditions are specific to appliance anomaly interpretation.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## s2sfdd2026

- **s2sfdd2026:sensor-fault-summary**: keep (TSK → TSK); pages [3]. Sensor selection uses anomaly scores, earliest fault times and fault/base variance ratios before describing selected variables. The concrete processing is targeted at fault diagnosis.
- **s2sfdd2026:diagnostic-retrieval**: keep (TSK → TSK); pages [3]. Historical fault reports are retrieved from sensor descriptions, and additional sensors are inspected when diagnosis evidence is insufficient. The retrieval target and stopping purpose are fault identification.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## chen2025trace

- **chen2025trace:der-cot**: keep (TSK → TSK); pages [4]. A relevance selector chooses CoT steps for distributed-energy forecasting, then inserts them into a next-value prediction prompt. The module is forecast-directed reasoning selection, not generic planning.
- **chen2025trace:forecast-consensus**: keep (TSK → TSK); pages [5]. The Judge feeds predictor means and statistics back until forecast consistency converges, and checks summaries against predictor reasoning. Both the consensus object and termination condition are forecast-specific.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## aiaforecaster2025

- **aiaforecaster2025:adaptive-search**: keep (GH → GH); pages [8]. Each agent chooses whether and how to search, conditioning new queries on earlier results. The recorded mechanism is adaptive evidence acquisition; probability aggregation is the separate task-bound module.
- **aiaforecaster2025:forecast-reconciliation**: keep (TSK → TSK); pages [8]. A supervisor reconciles independent forecast probabilities and Platt scaling calibrates the final number. The concrete output contract is probabilistic event forecasting.
- Resources: not_found_in_source
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## auditforecast2026

- **auditforecast2026:auditable-odds**: keep (TSK → TSK); pages [4]. The scaffold requires base probability, external factors and odds updates with a structured final forecasting report. These stages encode a probability-forecasting computation.
- Resources: source_reviewed
  - repository: https://github.com/CaoYuanpu/AuditForecast — reachable; PDF p.12; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

## openforecaster2026

- **openforecaster2026:event-rl**: keep (LLM → LLM); pages [9]. GRPO updates Qwen3 using free-form accuracy/Brier and binary Brier rewards on resolved questions. Retrieval is supplied as context, while the policy itself is learned.
- **openforecaster2026:dated-news-retrieval**: keep (TSK → TSK); pages [9]. The static corpus excludes articles after one month before each question's resolution date and retrieves five chunks. Its information boundary is explicitly a forecasting-resolution contract.
- Resources: source_reviewed
  - project: https://openforecaster.github.io/ — reachable; PDF p.1; author release statement or embedded hyperlink
  - repository: https://github.com/OpenForecaster/scaling-forecasting-training — reachable; PDF p.1; author release statement or embedded hyperlink
  - model: https://huggingface.co/collections/nikhilchandak/openforecaster — reachable; PDF p.1; author release statement or embedded hyperlink
- Resource search inspected all extracted PDF pages and embedded hyperlink targets. Third-party baseline repositories and dataset citations were not treated as this work's official release.

