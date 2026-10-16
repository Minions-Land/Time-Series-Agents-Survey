# Shard 1: module-boundary and official-resource review

Reviewed 46 assigned works and all 104 assigned module IDs. Read the existing evidence in its original method context, expanding source pages for ambiguous boundaries. This is a module-boundary audit, not an independent reproduction of reported results.

## Decisions

- Two layer corrections: Agentic RAG prompt pool GTS → LLM; TimeSeriesExamAgent question-template generator GTS → TSK.
- Four same-layer metadata corrections: TimeSeriesGym anomaly task; all three TSQ modules gain canonical data_quality_assessment task.
- All module IDs retained. No new module contribution is invented.

## Author resources

Searched extracted full-paper text and PDF URI annotations. Manually rejected third-party repositories appearing only as citations. 35 author-designated links across 26 works; 20 works have no author-designated URL in inspected sources. 32 links returned HTTP 2xx; VeriTime anonymous repository returned 401; two TimeCopilot documentation/evaluation deep links returned 404. Root TimeCopilot project remains reachable. HTTP reachability is not code reproducibility.

## Per-work audit

### agenticrag2024

- **agenticrag2024:slm-adaptation** — keep; LLM → LLM. PEFT/QLoRA and preference optimization explicitly update Gemma/Llama parameters; retain model-side training. Source: PDF p.4; passage beginning "We perform instruction-tuning".
- **agenticrag2024:master-router** — keep; GH → GH. The ReAct master routes requests to isolated specialists. Routing itself has no timestamp or outcome-specific acceptance rule; GH remains appropriate. Do not claim demonstrated chained subagents. Source: PDF p.2; passage beginning "The master agent for sub-agent".
- **agenticrag2024:pattern-prompt-pool** — change; GTS → LLM. The pool supplies continuous prompt embeddings, concatenated with the numerical input and projected by a learnable W; this is a differentiable model-facing adaptation, not an external episodic store. Move to LLM. Source: PDF p.3; Section 3.1, prompt concatenation and learnable projection equations.

Resources: not_found_in_source

### argos2025

- **argos2025:python-rule-synthesis** — keep; TSK → TSK. The generated inference function returns anomaly labels and is reviewed against detection accuracy; it is a detection procedure. Source: PDF p.6; passage beginning "The Detection Agent is tasked".
- **argos2025:syntax-repair** — keep; GH → GH. Dummy-input execution and traceback-guided repair stop when syntax/runtime errors disappear; that acceptance criterion is independent of anomaly labels. Source: PDF p.6; passage beginning "Repair Agent. Upon receiving".
- **argos2025:detector-fusion** — keep; TSK → TSK. The aggregator separately corrects false-negative and false-positive anomaly labels; its semantics are detector-specific. Source: PDF p.7; passage beginning "Aggregator. Algorithm 1".

Resources: not_found_in_source

### finarena2025

- **finarena2025:adaptive-retrieval** — keep; GH → GH. Unfamiliar knowledge triggers an adaptive retrieval decision; the mechanism is text-knowledge acquisition rather than financial return optimization. Source: PDF p.5; passage beginning "On this basis, we design".
- **finarena2025:risk-aware-report** — keep; TSK → TSK. Human risk preferences condition predicted stock movement and investment advice; outputs and feedback bind it to financial decisions. Source: PDF p.7; passage beginning "Report Agent provide".

Resources: [dataset](https://huggingface.co/datasets/Illogicaler/FinArena-low-cost-dataset) [200]

### timemaster2025

- **timemaster2025:sft-grpo** — keep; LLM → LLM. SFT followed by token-level GRPO updates the time-series multimodal model; output-format/class rewards supervise model parameters. Source: PDF p.6; passage beginning "To enable TimeMaster".

Resources: [code](https://github.com/langfengQ/TimeMaster) [200]

### zara2025

- **zara2025:activity-evidence** — keep; TSK → TSK. The evidence bank encodes pairwise activity discriminants and sensor-specific examples. Reusing it for another output requires replacing class priors, hence TSK. Source: PDF p.3; passage beginning "ZARA addresses this by decoupling".

Resources: [code](https://github.com/zechenli03/ZARA) [200]

### timecopilot2025

- **timecopilot2025:forecast-orchestration** — keep; TSK → TSK. The three-stage flow explicitly chooses forecasters using temporal diagnostics, cross-validation, and forecast metrics; retain forecast-specific orchestration. Source: PDF p.3; 2.1 TimeCopilot Agent.
- **timecopilot2025:forecaster-hub** — keep; TSK → TSK. The unified API and ensemble operate on forecasting models/outputs; interface uniformity does not remove the horizon/output restriction. Source: PDF p.3; 2.2 TimeCopilot Forecaster.

Resources: [project](https://timecopilot.dev) [200]; [documentation](https://timecopilot.dev/model-hub/) [404]; [evaluation](https://timecopilot.dev/experiments/gift-eval) [404]

### timeseriesscientist2025

- **timeseriesscientist2025:curator** — keep; GTS → GTS. The Curator emits statistics, missingness, preprocessing strategies, transformed series and temporal diagnostics before any forecast-loss comparison. Retain GTS for that delimited preparation module; cross-task efficacy is not experimentally established here. Source: PDF p.5; Section 3.2, Quality Diagnostics & Preprocessing.
- **timeseriesscientist2025:selection** — keep; TSK → TSK. Validation MAPE ranks model configurations and a subsequent ensemble strategy is fixed before test access; retain forecast-specific selection. Source: PDF p.6; Section 3.3, Model Ranking.

Resources: [code](https://github.com/Y-Research-SBU/TimeSeriesScientist) [200]; [project](https://y-research-sbu.github.io/TimeSeriesScientist/) [200]

### alphacast2025

- **alphacast2025:forecast-case-context** — keep; TSK → TSK. Each retrieved case pairs history with its optimal forecast model and target trajectory; this is not generic historical-context retrieval. Source: PDF p.4; method passage beginning Case Library..
- **alphacast2025:forecast-reasoning** — keep; TSK → TSK. The generator changes a forecast trajectory through case, scale, shape and contextual reasoning, then evaluates that forecast; TSK. Source: PDF p.4; method passage beginning Given the consolidated context.

Resources: [code](https://github.com/echo01-ai/AlphaCast) [200]

### streasoner2026

- **streasoner2026:sde-synthesis** — keep; TSK → TSK. Agents synthesize controlled numerical trajectories from graph/SDE/scenario specifications; retain synthesis-task procedure even though resulting pairs train a language model. Source: PDF p.3; method passage beginning Network SDEs-based multi-agent.
- **streasoner2026:spatial-tslm** — keep; LLM → LLM. A learned TS encoder, alignment pretraining, SFT and spatial-reward GRPO directly alter the TS-LM; LLM. Source: PDF p.5; method passage beginning Model Architecture.

Resources: [code](https://github.com/LingFengGold/STReasoner) [200]

### multimodaldebate2026

- **multimodaldebate2026:modality-debate** — keep; GH → GH. Modality-isolated first reports followed by structured cross-report refinement is a generic evidence-coordination protocol; the numerical/spectral interfaces are separately recorded. Source: PDF p.4; passage beginning "Modality-Specialized Analysts".
- **multimodaldebate2026:temporal-views** — keep; GTS → GTS. Time-domain, spectral and statistical views expose measured temporal structure; their construction does not depend on a particular requested answer class. Source: PDF p.3; passage beginning "Time-Frequency Views".
- **multimodaldebate2026:temporal-verification** — keep; GTS → GTS. VCC distinguishes verifiability of observed-time claims from future claims and retains uncertainty for unobserved outcomes; that temporal scope check is distinct from selecting a task answer. Source: PDF p.5; passage beginning "Temporal scope further modulates".

Resources: [code](https://github.com/DeepAuto-AI/TS-Debate) [200]

### veritime2026

- **veritime2026:process-labelled-data** — keep; LLM → LLM. TSRgen generates process labels expressly for RFT supervision. Retain LLM as training-data contribution, not deployment-time evidence verification; only selected steps receive labels. Source: PDF p.3; passage beginning "Verifiable Process Annotation Extraction.".
- **veritime2026:scheduled-rft** — keep; LLM → LLM. Warmup SFT, learnability split, normal-sample SFT and hard-sample GRPO update the reasoning policy; LLM. Source: PDF p.4; passage beginning "Two-stage RFT Training.".

Resources: [code](https://anonymous.4open.science/r/VeriTime-E017) [401]

### agriworld2026

- **agriworld2026:reflective-execution** — keep; GH → GH. Execute-observe-refine patches code using diagnostic feedback and a validator result; the loop can accept an external task checker without requiring agricultural mathematics. Source: PDF p.4; passage beginning "We introduce AGRO-REFLECTIVE".
- **agriworld2026:typed-world** — keep; GTS → GTS. Typed raster/weather/event state and units constitute a temporal data interface across the environment tasks. Domain specificity alone does not make this a single-task procedure. Source: PDF p.3; passage beginning "Unified Tool Interface and Artifacts".
- **agriworld2026:intervention-checker** — keep; TSK → TSK. The checker compares a specified intervention with baseline simulation and a required effect direction/magnitude; this decision-support contract makes it TSK. Source: PDF p.4; passage beginning "Counterfactual Consistency:".
- **agriworld2026:domain-lora** — keep; LLM → LLM. LoRA on Qwen training splits is parameter adaptation, separate from the execution loop. Source: PDF p.5; passage beginning "We finetune the Qwen3".

Resources: not_found_in_source

### weathertgd2026

- **weathertgd2026:caption-feedback** — keep; TSK → TSK. Statistical, physical and meteorological feedback revises weather captions under a caption-quality/length output contract. Source: PDF p.7; passage beginning "The Statistical Analyst Agent".
- **weathertgd2026:consensus-fusion** — keep; GH → GH. The consensus operation clusters semantic feedback fragments and preserves distinct views by embedding similarity; this delimited fusion operation is independent of weather physics. Source: PDF p.8; passage beginning "We address this limitation".

Resources: not_found_in_source

### timeseriesexamagent2026

- **timeseriesexamagent2026:exam-template-generation** — change; GTS → TSK. Templates encode question logic, options, selection of instances and answer computation. The produced artifact is a QA exam, so multiple concept/domain coverage does not make it task-independent; move GTS to TSK. Source: PDF p.5; passage beginning "We propose TimeSeriesExamAgent".
- **timeseriesexamagent2026:capability-filter** — keep; GH → GH. The retained submodule filters items by relative solver capability, without using time-index semantics. Retain GH as generic benchmark-item quality control, with its exam-generation role explicit. Source: PDF p.6; passage beginning "Capability-Aligned Filtering".

Resources: [code](https://github.com/magwiazda/TimeSeriesExamAgent) [200]; [dataset](https://huggingface.co/datasets/AutonLab/TimeSeriesExam) [200]; [code](https://github.com/moment-timeseries-foundation-model/TimeSeriesExam) [200]

### marstsc2026

- **marstsc2026:class-knowledge-bank** — keep; TSK → TSK. The Generator/Reflector/Modifier alter class-specific feature bullets using labeled train/validation classification errors; TSK. Source: PDF p.5; passage beginning "To dynamically refine the knowledge bank".
- **marstsc2026:test-time-knowledge** — keep; TSK → TSK. Two-pass pseudo-label agreement and deferred updates modify class-specific knowledge. The acceptance rule depends on classification outputs. Source: PDF p.6; passage beginning "Refine on Pseudo Label.".

Resources: not_found_in_source

### aion2026

- **aion2026:lifecycle** — keep; GH → GH. Agent roles, skills, rules, progress memory and protocols organize general executable work; the temporal interfaces are isolated in other modules. Source: PDF p.4; Section 3.2, Overview.
- **aion2026:validation** — keep; GTS → GTS. The validator separates alignment/leakage admissibility from forecast/profit/report scores. This record concerns the temporal admissibility part only, so GTS. Source: PDF p.4; Section 3.1, Validation interface, Eq. (3).
- **aion2026:grounding** — keep; GTS → GTS. Observation granularity, history cutoff, output frequency and evidence coverage define temporal meaning across forecast tables and analytical answers; GTS. Source: PDF p.5; Section 3.3.1, Temporal Grounding.

Resources: [code](https://github.com/ztxtech/aion) [200]

### timesagemt2026

- **timesagemt2026:workflow-evaluation** — keep; GTS → GTS. Visible slices, numerical references and traceable multi-turn analysis span exploratory, synthesis and decision stages. Retain GTS as cross-task evaluation infrastructure, not a deployed solving policy. Source: PDF p.4; 3 TimeSage-MT Benchmark.
- **timesagemt2026:orchestrated-runtime** — keep; GH → GH. Planner/Reporter plus deterministic Validator/Profiler/Executor/Evaluator provide generic orchestration; individual TS skills are a separate record. Source: PDF p.7; 4.2 Agentic system settings.
- **timesagemt2026:temporal-skill-library** — keep; GTS → GTS. The shared 226-skill library covers temporal analysis, forecasting, generation, imputation and causal diagnostics. GTS denotes the library interface/collection, not every contained skill as a universal contribution. Source: PDF p.7; 4.2 Agentic system settings.

Resources: [code](https://github.com/TimeSage-Series/TimeSage-MT) [200]; [dataset](https://huggingface.co/datasets/TimeSage-Series/TimeSage-MT) [200]

### tsqbench2026

- **tsqbench2026:quality-assessment** — change; GTS → GTS. Pairwise quality judgments assess missingness, noise and temporal structure before downstream use. Retain GTS as data-quality validation with an explicit quality-comparison output, not general QA. Add the existing canonical data_quality_assessment task label to reflect the actual output/training target. Source: PDF p.4; 3.1 Overview.
- **tsqbench2026:perceiver-training** — change; LLM → LLM. Quality-dimension selection is trained with GRPO and dimension-set reward; retain LLM adaptation. Add the existing canonical data_quality_assessment task label to reflect the actual output/training target. Source: PDF p.5; 3.2 Perceiver.
- **tsqbench2026:quality-benchmark** — change; GTS → GTS. Controlled degradations test intrinsic temporal-data quality independent of forecast/classifier accuracy; retain GTS evaluation resource rather than runtime module. Add the existing canonical data_quality_assessment task label to reflect the actual output/training target. Source: PDF p.3; 2 Measuring LLM Capabilities.

Resources: [code](https://github.com/clsr1008/TSQualityAgent) [200]

### batterylake2026

- **batterylake2026:quoted-metadata** — keep; GH → GH. Verbatim span checks, abstention and selective human verification govern document extraction regardless of signal type; GH. Source: PDF p.3; method passage beginning An evidence-grounded extractor.
- **batterylake2026:temporal-schema** — keep; GTS → GTS. Time samples, physical units and sign conventions form a reusable ingestion schema for multiple battery analyses; keep GTS with battery-domain scope stated, not universal plug-and-play. Source: PDF p.3; method passage beginning Time series T:.
- **batterylake2026:soh-rul-benchmark** — keep; TSK → TSK. SOH/RUL labels, end-of-life thresholds and split/metric protocol target health prediction; TSK. Source: PDF p.6; method passage beginning Benchmark Design.

Resources: [project](https://tianwen1209.github.io/batterylake/) [200]

### finanalyst2026

- **finanalyst2026:specialist-trading** — keep; TSK → TSK. Specialists aggregate dated disclosures into BUY/HOLD/SELL under recency/confidence overrides; task-bound decision support. Source: PDF p.3; method passage beginning We propose a hierarchical agent.
- **finanalyst2026:inference-cache** — keep; GH → GH. Identical-prompt hash caching avoids repeated calls; cache identity and retrieval do not require trading semantics. Source: PDF p.4; method passage beginning To bound latency and cost.

Resources: not_found_in_source

### castfsr2026

- **castfsr2026:forecast-revision** — keep; TSK → TSK. Fast/slow/reflect actions construct and revise a numerical horizon from forecast priors and context; TSK even though several tool functions are reusable. Source: PDF p.2; Introduction, framework overview.
- **castfsr2026:policy-training** — keep; LLM → LLM. SFT and multi-turn GRPO internalize executable workflows into a compact language policy; LLM. Source: PDF p.4; Model-Agnostic Instantiation of CastFSR, training paragraph.

Resources: [code](https://github.com/Xiaoyu-Tao/CastFSR) [200]

### tracemas2026

- **tracemas2026:cld-forecast-lineage** — keep; TSK → TSK. Document-factor/proxy/lag/model lineage is the shared artifact used to construct and revise a forecast; retain TSK. Source: PDF p.3; passage beginning "Definition 2 (Data-Grounded CLD).".
- **tracemas2026:temporal-risk-review** — keep; GTS → GTS. The delimited checks for leakage, timestamp mismatch, units and provenance are temporal admissibility checks. Retain GTS without counting the broader forecast reviewer twice. Source: PDF p.3; passage beginning "The Risk Reviewer checks".

Resources: not_found_in_source

### agentictwin2026

- **agentictwin2026:dt-residual-event** — keep; TSK → TSK. Digital-twin residuals feed trained fault labels and structured anomaly events; this numerical detector is a task component, not LLM training. Source: PDF p.4; passage beginning "The proposed anomaly classifier".
- **agentictwin2026:fault-retrieval-mitigation** — keep; TSK → TSK. Retrieval explicitly filters by predicted fault types and produces diagnosis/mitigation; task-specific evidence routing. Source: PDF p.5; passage beginning "At the core of the AgenticTwin".

Resources: not_found_in_source

### timesageev2026

- **timesageev2026:evolving-cutoff-benchmark** — keep; GTS → GTS. Release-by-release evidence expansion with the current release withheld defines a reusable chronological evaluation interface across analytical questions. Source: PDF p.4; passage beginning "As the benchmark progresses".
- **timesageev2026:skill-library** — keep; GH → GH. Induct/retrieve reusable Python routines and callable/interface checks are generic skill management; activation timing is separately recorded. Source: PDF p.24; passage beginning "Skill-library tools.".
- **timesageev2026:chronological-skill-registration** — keep; GTS → GTS. Activation only at the next evidence release enforces chronological causality. This temporal registration restriction is GTS rather than generic skill storage. Source: PDF p.24; passage beginning "Chronological registration.".

Resources: [code](https://github.com/TimeSage-Series/TimeSage-EV) [200]; [dataset](https://huggingface.co/datasets/TimeSage-Series/TimeSage-EV) [200]

### evotsagent2026

- **evotsagent2026:trajectory-evolution** — keep; GH → GH. Revision, strategy switch and recombination accept external validation scores and preserve an incumbent executable trajectory; no change-point equation is required for this controller. Source: PDF p.4; 4 Orchestration.
- **evotsagent2026:cp-model-selection** — keep; TSK → TSK. The selection record includes change-sensitive adjacent-window statistics and a CP detector bank; TSK. Source: PDF p.4; 4.1 EDA-based Model Selection.

Resources: not_found_in_source

### tracebench2026

- **tracebench2026:root-cause-evaluation** — keep; TSK → TSK. The target is the intervened simulator parameter or no change; root-cause attribution determines ground truth and scoring. Source: PDF p.3; method passage beginning TraceBench is a simulation-based.
- **tracebench2026:execution-trace-metrics** — keep; GH → GH. Tokens, elapsed time, tool counts, plots and console exposure measure generic execution behavior; retain GH evaluation role. Source: PDF p.5; method passage beginning From the agentic log traces.

Resources: [project](https://tracebench.github.io) [200]; [code](https://github.com/TommasoBendinelli/TraceBench) [200]; [dataset](https://huggingface.co/datasets/eth-siplab/tracebench) [200]

### timeseriesgym2025

- **timeseriesgym2025:challenge-environment** — keep; GH → GH. Resource bundles, executable submission artifacts and graders form a generic ML-engineering challenge interface. Source: PDF p.4; method passage beginning Each challenge in TimeSeriesGym.
- **timeseriesgym2025:temporal-challenges** — change; GTS → GTS. The collection spans temporal ML problem types; retain GTS as a cross-task benchmark collection, not a claim that each challenge is task-independent. Add the omitted anomaly-detection task explicitly included among original engineering challenges. Source: PDF p.4; Section 3, original challenge examples.

Resources: [code](https://github.com/moment-timeseries-foundation-model/TimeSeriesGym) [200]

### grammarwave2026

- **grammarwave2026:event-logic-grounding** — keep; TSK → TSK. Event-description logic is instantiated into interval evidence and root confidence; temporal operators are governed by a specific event-detection contract. Source: PDF p.4; method passage beginning Agent workflow..

Resources: [code](https://github.com/cw-wan/SELA) [200]

### bridge2025

- **bridge2025:description-refinement** — keep; TSK → TSK. The multi-agent template refinement is evaluated for text-conditioned TS generation, fixing the task output despite domain-general templates. Source: PDF p.5; method passage beginning Stage 2 Intra-group Discussion.
- **bridge2025:text-diffusion** — keep; TSK → TSK. Text/prototype-conditioned diffusion generates numerical series; TSK numerical generator component. It is not an LLM-parameter contribution or independently an agent. Source: PDF p.4; method passage beginning The latter, i.e..

Resources: [code](https://github.com/microsoft/TimeCraft/tree/main/BRIDGE) [200]

### agentfm2025

- **agentfm2025:role-management** — keep; GH → GH. Role assignment follows changing distributed-node configuration/status; generic coordination independent of temporal diagnostics. Source: PDF p.3; method passage beginning To handle this, we designed.
- **agentfm2025:metric-description** — keep; GTS → GTS. Denoising, missingness handling and interval/trend descriptions expose temporal evidence before detection/diagnosis/mitigation; retain GTS. Source: PDF p.3; method passage beginning Metric Agent: The overall.
- **agentfm2025:failure-management** — keep; TSK → TSK. Labeled historical failures and trace evidence guide anomaly detection, root-cause labels and mitigation; TSK. Source: PDF p.4; method passage beginning After system agents collect.

Resources: not_found_in_source

### openti2024

- **openti2024:conversational-execution** — keep; GH → GH. Intent extraction, augmentation-tool matching and multimedia output wrapping define generic conversational execution. Source: PDF p.9; method passage beginning When a user requirement.
- **openti2024:traffic-meta-control** — keep; TSK → TSK. Natural-language traffic requirements alter traffic-light actions through ChatLight; the action space fixes decision-support scope. Source: PDF p.9; method passage beginning Third, our method leverages.

Resources: [code](https://github.com/DaRL-LibSignal/OpenTI.git) [200]

### gruver2023llmtime

- **gruver2023llmtime:decimal-representation** — keep; LLM → LLM. Digit serialization, tokenizer-specific spacing and continuous-density interpretation alter the language-model interface without finetuning; LLM-side representation is the appropriate independent axis. Source: PDF p.4; method passage beginning To remedy the tokenization.

Resources: [code](https://github.com/ngruver/llmtime) [200]

### ji2025lemad

- **ji2025lemad:stream-normalization** — keep; GTS → GTS. Timestamp alignment, format normalization and missing values are upstream temporal ingestion operations; retain GTS. Source: PDF p.8; method passage beginning Data Preprocessing Module:.
- **ji2025lemad:stream-checkpoint** — keep; GH → GH. Log compression and offsets support restart consistency without a temporal-analysis objective; GH. Source: PDF p.7; method passage beginning Compression and Checkpointing Module:.
- **ji2025lemad:anomaly-diagnosis** — keep; TSK → TSK. Service-window anomaly alerts, root-cause diagnosis and operational recommendations are task outputs; TSK. Source: PDF p.5; method passage beginning Second, the real-time analysis agent.

Resources: not_found_in_source

### zhang2025llm

- **zhang2025llm:dataframe-execution** — keep; GH → GH. Repository class LLM_TSFD wraps a DataFrame, emits and executes Python, and refines responses; this delimited execution wrapper is GH. Cleaning/labeling instructions in its prompt should not be mistaken for proven new temporal algorithms. Source: src/__init__.py lines 30-36; LLM_TSFD.run/run_code.

Resources: [code](https://github.com/zq300/LLM-TSFD) [200]

### finagent2024

- **finagent2024:vector-memory** — keep; GH → GH. The isolated vector-store mechanism uses query fields/summaries and similarity matching; market-dependent reflection is separately recorded, so retain GH for storage/retrieval plumbing. Source: PDF p.5; method passage beginning To realize the 3A superiority.
- **finagent2024:market-reflection** — keep; TSK → TSK. Low/high reflection explicitly associates news and technical evidence with realized price changes and trading actions; TSK. Source: PDF p.5; method passage beginning The reflection framework.

Resources: not_found_in_source

### structuredagenticworkflows2025

- **structuredagenticworkflows2025:code-search** — keep; GH → GH. Round-robin warmup/search accepts code by external validation loss and rolls back failed candidates; generic code-agent controller. Source: PDF p.5; method passage beginning Stage 2 employs a two-phase.
- **structuredagenticworkflows2025:temporal-model-bank** — keep; GTS → GTS. The bank combines forecasting and generative model implementations and evaluation measures. Retain GTS as shared temporal modeling infrastructure; each model/metric is not separately counted as task-independent. Source: PDF p.4; method passage beginning The code base includes.

Resources: not_found_in_source

### virtualtrafficpolice2026

- **virtualtrafficpolice2026:hierarchical-control** — keep; TSK → TSK. The upper LLM changes traffic-control parameters and lower controller executes traffic actions; task-specific control hierarchy. Source: PDF p.6; method passage beginning This hierarchical framework consists.
- **virtualtrafficpolice2026:traffic-experience** — keep; TSK → TSK. Retrieved event-to-capacity-to-control Q/A pairs are validated to refine traffic strategies; memory acceptance depends on traffic action utility. Source: PDF p.12; method passage beginning The system retrieves.

Resources: not_found_in_source

### finmem2023

- **finmem2023:layered-financial-memory** — keep; TSK → TSK. Layer horizons track financial news/report cadence and promotions depend on investment success. This is trading-conditioned memory, not generic vector storage. Source: PDF p.9; method passage beginning Furthermore, an access counter.
- **finmem2023:trade-character** — keep; TSK → TSK. Trader character, risk preferences and ranked memories choose daily stock actions; TSK. Source: PDF p.9; method passage beginning In its daily trading decisions.

Resources: [code](https://github.com/pipiku915/FinMem-LLM-StockTrading/) [200]

### tradingagents2024

- **tradingagents2024:structured-report-state** — keep; GH → GH. The module is explicitly a structured global-report/state communication mechanism; domain content is supplied by roles, so GH. Source: PDF p.8; method passage beginning Our model introduces.
- **tradingagents2024:investment-debate** — keep; TSK → TSK. Bullish/bearish debate and risk approval evaluate investment positions, fixing the decision objective; TSK. Source: PDF p.6; method passage beginning The Researcher Team.

Resources: [code](https://github.com/TauricResearch/TradingAgents) [200]

### merit2025

- **merit2025:positive-views** — keep; TSK → TSK. Retrieved and augmented sequences are accepted as contrastive positive views. The construction target is augmentation for representation learning, despite evaluation across several downstream tasks. Source: PDF p.3; Figure 2 caption.

Resources: not_found_in_source

### pandaai2026

- **pandaai2026:regime-conditioned-cq2** — keep; LLM → LLM. Learned soft tokens plus CQ2 SFT/preference training alter the language policy. Retain LLM; proposed continuous adaptation should not be equated with independently validated deployment. Source: PDF p.17; passage beginning "Regime-Conditioned Instruction Tuning".
- **pandaai2026:constrained-alpha-mcts** — keep; TSK → TSK. MCTS candidate values and constraints use financial backtests, factor redundancy and turnover; TSK alpha search. Source: PDF p.6; passage beginning "We conceptualize Alpha Mining".
- **pandaai2026:regime-portfolio-execution** — keep; TSK → TSK. Regime-conditioned risk aversion, portfolio allocation and liquidity-sensitive execution optimize financial actions; TSK. Source: PDF p.7; passage beginning "Portfolio Optimization (P)".
- **pandaai2026:feedback-rule-induction** — keep; TSK → TSK. The fast update induces factor constraints from profitable/unprofitable cases within market regimes. Keep TSK for symbolic rule induction; the separate slow LoRA loop is not part of this module. Source: PDF p.7; passage beginning "Fast Loop (Symbolic Rule Induction)".

Resources: not_found_in_source

### genautoml2026

- **genautoml2026:dynamic-architecture-registry** — keep; GH → GH. Dynamic class discovery, AST loading and runtime registration integrate generated neural code; general execution machinery. Source: PDF p.5; passage beginning "3.3 Just-In-Time (JIT) Architectural Integration".
- **genautoml2026:forecast-shape-contract** — keep; TSK → TSK. Forward validation fixes lookback/horizon/feature tensor dimensions for forecasts; TSK output contract. Source: PDF p.4; passage beginning "In order to ensure the generated code is compatible".
- **genautoml2026:revin-wrapper** — keep; GTS → GTS. Instance statistics normalize temporal channels and restore scale around generated models across forecast/reconstruction pipelines; GTS adoption/integration of RevIN, not invention of RevIN or a guarantee of stationarity. Source: PDF p.5; passage beginning "To address this, we integrate a Dynamic Reversible Instance Normalization".

Resources: not_found_in_source

### mosaic2026

- **mosaic2026:blueprint-composition** — keep; GH → GH. Case/code-bank retrieval and blueprint realization construct executable modeling programs under an external loss; generic workflow construction. Source: PDF p.4; passage beginning "Knowledge banks.".
- **mosaic2026:failure-aware-refinement** — keep; GH → GH. Checkpoint rollback and invalid-action masks depend on execution errors or deteriorating loss, not temporal mathematics. Retain GH for this guardrail component; learned refinement-policy training is distinct. Source: PDF p.6; passage beginning "Offline trajectory construction.".
- **mosaic2026:temporal-semantic-eda** — keep; GTS → GTS. ADF, temporal plots and regime/volatility summaries provide shared temporal EDA before choosing forecasting or generation programs; GTS. Source: PDF p.15; passage beginning "C Semantic-aware EDA with Multimodal Support".

Resources: not_found_in_source

### duan2025factormad

- **duan2025factormad:factor-debate** — keep; TSK → TSK. Debate starts from alpha-factor code/performance and critiques return-prediction factors; task-specific search. Source: PDF p.3; passage beginning "3.2 Agent Debate Framework".
- **duan2025factormad:factor-validation** — keep; TSK → TSK. Factor-specific dimension/comparability rules plus IC/ICIR/correlation determine acceptance; TSK. Generic execution checks are implementation ingredients, not extra modules. Source: PDF p.5; passage beginning "3.3.2 Validation.".
- **duan2025factormad:causal-window-check** — keep; GTS → GTS. The delimited causal-window rule forbids future timestamps and full-series statistics; temporal availability is independent of financial utility, hence GTS. Source: PDF p.6; passage beginning "LOOK-AHEAD BIAS".

Resources: not_found_in_source

### conversationaltsfm2025

- **conversationaltsfm2025:forecast-judge-adaptation** — keep; LLM → LLM. SFT and GRPO train a Qwen ensemble-decider policy from forecast optimization trajectories; LLM. Source: PDF p.5; passage beginning "3.4 R1-Style Fine-tuning for Reasoning and Decision Capability".
- **conversationaltsfm2025:forecast-ensemble-control** — keep; TSK → TSK. SLSQP convex weights and accept/continue decisions optimize an ensemble forecast metric; task-bound control. Source: PDF p.4; passage beginning "Therefore, we employ Sequential Least Squares Programming".
- **conversationaltsfm2025:ensemble-audit-reflection** — keep; TSK → TSK. Audit records forecast weights, error, confidence and acceptance explanations; its content and faithfulness procedure are ensemble-specific. Source: PDF p.6; passage beginning "3.5 Interpretability Through Reflective Explanation".

Resources: [evaluation_submission](https://github.com/SalesforceAIResearch/gift-eval/pull/51) [200]

### stride2026

- **stride2026:reasoning-distillation** — keep; LLM → LLM. Teacher access to training pseudo-future creates supervision; student causal language modeling learns reasoning from history. LLM distillation, not future access at inference. Source: PDF p.5; passage beginning "3.3. Reference Reasoning Generation and Distillation".
- **stride2026:latent-fusion** — keep; LLM → LLM. LLM hidden states, learned projection, TSFM training and LoRA form model-side cross-modal fusion; retain LLM rather than numerical-tool orchestration. Source: PDF p.5; passage beginning "3.4. Cross-Modal Fusion and End-to-End Training".

Resources: not_found_in_source
