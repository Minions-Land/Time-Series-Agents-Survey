# From Prompts to Agents: A Comprehensive Survey of LLM-Driven Time Series Analysis

<p align="center">
  <img src="figure/pipeline.png" alt="Unified design space for LLM-driven time series analysis" width="1000"/>
</p>
<p align="center">Unified design space for LLM-driven time series analysis</p>

## About This Project

This repository is a continuously updated collection of papers and resources dedicated to **From Prompts to Agents: A Comprehensive Survey of LLM-Driven Time Series Analysis**.

For in-depth knowledge, check out our survey paper: [*From Prompts to Agents: A Comprehensive Survey of LLM-Driven Time Series Analysis*](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6614598).

If you find this project helpful, we kindly ask you to consider citing our work:

```bibtex
@article{zhang2025prompts,
  title={From Prompts to Agents: A Comprehensive Survey of LLM-Driven Time Series Analysis},
  author={Zhang, Regina and Goh, Si Qi and Chen, Xingsheng and Li, Zongru and Wen, Honggang and Guo, Jiale and Yang, Menglin and Yin, Hongzhi and Yang, Qiang and Yiu, SM and others},
  journal={Available at SSRN 6614598},
  year={2025}
}
```

## Contributions of This Survey

The motivation for this survey is anchored in three research gaps:

- The need for a unified taxonomy connecting time-series representation, language-model adaptation, workflow autonomy, and analytical task.
- The need to distinguish frozen-backbone prompting from backbone-updating instruction tuning while tracing the transition from fixed pipelines to observation-dependent agent workflows.
- The need to evaluate LLM-driven time series systems across forecasting, anomaly detection, classification, and imputation while considering workflow-level capabilities beyond predictive accuracy.

## Table of Contents

- [Representation (A1)](#representation-a1)
  - [Numeric Serialization](#numeric-serialization)
  - [Symbolic Discretization](#symbolic-discretization)
  - [Patching and Reprogramming](#patching-and-reprogramming)
  - [Cross-Modal Alignment](#cross-modal-alignment)
  - [TS-Native Foundation Model Tool](#ts-native-foundation-model-tool)
- [Model Adaptation (A2)](#model-adaptation-a2)
  - [Direct Prompting](#direct-prompting)
    - [Numeric Serialization](#direct-prompting-numeric-serialization)
    - [Symbolic Discretization](#direct-prompting-symbolic-discretization)
    - [Retrieval-Augmented ICL](#direct-prompting-retrieval-augmented-icl)
    - [Learned Projection and Reprogramming](#direct-prompting-learned-projection-and-reprogramming)
  - [Instruction Tuning](#instruction-tuning)
    - [Domain or Task Tuning](#instruction-tuning-domain-or-task-tuning)
    - [Synthetic-Data Alignment](#instruction-tuning-synthetic-data-alignment)
    - [Reasoning-Incentivized Tuning](#instruction-tuning-reasoning-incentivized-tuning)
    - [Native Multimodal TSLM](#instruction-tuning-native-multimodal-tslm)
- [Workflow Autonomy (A3)](#workflow-autonomy-a3)
  - [L1 Predictor](#l1-predictor)
  - [L2 Augmenter](#l2-augmenter)
  - [L3 Orchestrator](#l3-orchestrator)
  - [L4 Multi-Agent Collaboration](#l4-multi-agent-collaboration)
- [Analytical Tasks (A4)](#analytical-tasks-a4)
  - [Forecasting](#forecasting)
  - [Anomaly Detection](#anomaly-detection)
  - [Classification](#classification)
  - [Imputation](#imputation)

## Paper

| Axis | Design question | Example choices | Illustrative systems |
| --- | --- | --- | --- |
| **A1 — Representation** | How is the series represented? | Numeric serialization; symbolic discretization; patching with learned projection; cross-modal alignment; time-series-native foundation model used as a tool | LLMTime; Time-LLM; ChatTS; Chronos |
| **A2 — Model Adaptation** | How is the model adapted? | Direct prompting with a frozen backbone; instruction tuning through PEFT, full SFT, or reinforcement learning | LLMTime; Time-LLM; ChatTS; OpenTSLM-SP |
| **A3 — Workflow Autonomy** | How autonomous is the runtime workflow? | L1 Predictor; L2 Augmenter; L3 Orchestrator; L4 Multi-Agent Collaboration | LLMTime; News-conditioned FC; TimeClaw; TradingAgents |
| **A4 — Analytical Task** | What task is addressed? | Forecasting; anomaly detection; classification; imputation | TradingAgents; Argos; SIGLLM; TRACE |

### Representation (A1)

Axis A1 records the route by which temporal signals enter the LLM-driven system.

#### Numeric Serialization

Raw values are represented as numeric tokens or text sequences.

Representative methods:

- [Large Language Models Are Zero-Shot Time Series Forecasters](https://arxiv.org/abs/2310.07820)
- [EVIL: Evolving Interpretable Algorithms for Zero-Shot Inference on Event Sequences and Time Series with LLMs](https://arxiv.org/abs/2604.15787)
- [TradingAgents: Multi-Agents LLM Financial Trading Framework](https://openreview.net/forum?id=4QPrXwMQt1)
- [Time Series Forecasting as Reasoning: A Slow-Thinking Approach with Reinforced LLMs](https://arxiv.org/abs/2506.10630)

#### Symbolic Discretization

Continuous values are mapped to symbolic alphabets or discrete temporal patterns.

Representative methods:

- [MultiCast: Zero-Shot Multivariate Time Series Forecasting Using LLMs](https://doi.org/10.1109/ICDEW61823.2024.00022)
- [From Numbers to Prompts: A Cognitive Symbolic Transition Mechanism for Lightweight Time-Series Forecasting](https://arxiv.org/abs/2602.00088)
- [S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis](https://doi.org/10.1109/SAFEPROCESS67117.2025.11268252)
- [TS2Lang: A Co-occurrence Pattern-Driven Translation Mechanism for Zero-Shot Time Series Forecasting with LLMs](https://doi.org/10.1007/s10844-025-01015-6)

#### Patching and Reprogramming

Temporal patches are projected or reprogrammed into the model's embedding space.

Representative methods:

- [Time-LLM: Time Series Forecasting by Reprogramming Large Language Models](https://openreview.net/forum?id=Unb5CVPtae)
- [S²IP-LLM: Semantic Space Informed Prompt Learning with LLM for Time Series Forecasting](https://openreview.net/forum?id=qwQVV5R8Y7)
- [One Fits All: Power General Time Series Analysis by Pretrained LM](https://proceedings.neurips.cc/paper_files/paper/2023/hash/86c17de05579cde52025f9984e6e2ebb-Abstract-Conference.html)
- [U-STS-LLM: A Unified Spatio-Temporal Steered Large Language Model for Traffic Prediction and Imputation](https://arxiv.org/abs/2605.11735)

#### Cross-Modal Alignment

Time series are aligned with language or another modality through paired representations or multimodal interfaces.

Representative methods:

- [ChatTS: Aligning Time Series with LLMs via Synthetic Data for Enhanced Understanding and Reasoning](https://arxiv.org/abs/2412.03104)
- [OpenTSLM: Time-Series Language Models for Reasoning over Multivariate Medical Text- and Time-Series Data](https://openreview.net/forum?id=FHDRzhKm0f)
- [TimeOmni-1: Incentivizing Complex Reasoning with Time Series in Large Language Models](https://openreview.net/forum?id=kOIclg7muL)
- [TimeOmni-VL: Unified Models for Time Series Understanding and Generation](https://openreview.net/forum?id=uUnIAtZUfX)

#### TS-Native Foundation Model Tool

A time-series-native foundation model processes the series as a callable analytical tool within an LLM-driven workflow.

Representative methods:

- [TimeClaw: A Time-Series AI Agent with Exploratory Execution Learning](https://arxiv.org/abs/2605.10038)
- [TimeART: Towards Agentic Time Series Reasoning via Tool-Augmentation](https://arxiv.org/abs/2601.13653)
- [Reasoning through Verifiable Forecast Actions: Consistency-Grounded RL for Financial LLMs](https://arxiv.org/abs/2605.21975)
- [Conversational Time Series Foundation Models: Towards Explainable and Effective Forecasting](https://arxiv.org/abs/2512.16022)

### Model Adaptation (A2)

<p align="center">
  <img src="figure/a2_model_adaptation_boundary.png" alt="Decision rule separating direct prompting from instruction tuning on axis A2" width="760"/>
</p>
<p align="center">Formal model-adaptation boundary on axis A2</p>

Axis A2 is assigned by whether any language-backbone parameter is updated. Direct prompting keeps the backbone frozen, including methods that train auxiliary modules outside the backbone. Instruction tuning updates at least one backbone parameter.

#### Direct Prompting

Direct prompting keeps the language backbone frozen. It includes both training-free inference and learned auxiliary interfaces trained outside the backbone.

##### Direct Prompting: Numeric Serialization

Raw values are supplied as digit tokens without updating the language backbone.

Representative methods:

- [Large Language Models Are Zero-Shot Time Series Forecasters](https://arxiv.org/abs/2310.07820)
- [Univariate to Multivariate: LLMs as Zero-Shot Predictors for Time-Series Forecasting](https://arxiv.org/abs/2506.02389)
- [EVIL: Evolving Interpretable Algorithms for Zero-Shot Inference on Event Sequences and Time Series with LLMs](https://arxiv.org/abs/2604.15787)

##### Direct Prompting: Symbolic Discretization

Symbolic or alphabet-based encodings are processed by a frozen language backbone.

Representative methods:

- [From Numbers to Prompts: A Cognitive Symbolic Transition Mechanism for Lightweight Time-Series Forecasting](https://arxiv.org/abs/2602.00088)
- [S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis](https://doi.org/10.1109/SAFEPROCESS67117.2025.11268252)
- [TS2Lang: A Co-occurrence Pattern-Driven Translation Mechanism for Zero-Shot Time Series Forecasting with LLMs](https://doi.org/10.1007/s10844-025-01015-6)

##### Direct Prompting: Retrieval-Augmented ICL

Retrieved domain knowledge or historical segments are supplied as in-context exemplars.

Representative methods:

- [TimeClaw: A Time-Series AI Agent with Exploratory Execution Learning](https://arxiv.org/abs/2605.10038)
- [ZARA: Training-Free Motion Time-Series Reasoning via Evidence-Grounded LLM Agents](https://aclanthology.org/2026.acl-long.684/)
- [RAAD-LLM: Adaptive Anomaly Detection Using LLMs and RAG Integration](https://arxiv.org/abs/2503.02800)

##### Direct Prompting: Learned Projection and Reprogramming

Projection or reprogramming modules are trained outside the frozen language backbone.

Representative methods:

- [Time-LLM: Time Series Forecasting by Reprogramming Large Language Models](https://openreview.net/forum?id=Unb5CVPtae)
- [TimeCMA: Towards LLM-Empowered Multivariate Time Series Forecasting via Cross-Modality Alignment](https://ojs.aaai.org/index.php/AAAI/article/view/34067)
- [PaP-NF: Probabilistic Long-Term Time Series Forecasting via Prefix-as-Prompt Reprogramming and Normalizing Flows](https://doi.org/10.1007/978-3-032-31930-2_7)

#### Instruction Tuning

Instruction tuning updates at least one language-backbone parameter through partial tuning, PEFT, full SFT, reward-based optimization, or native multimodal training.

##### Instruction Tuning: Domain or Task Tuning

Partial, parameter-efficient, or full updates specialize the backbone for temporal tasks or domains.

Representative methods:

- [TRACE: Unlocking the Potential of LLMs in Time Series Forecasting for Distributed Energy Resources](https://doi.org/10.1109/TAI.2025.3572853)
- [One Fits All: Power General Time Series Analysis by Pretrained LM](https://proceedings.neurips.cc/paper_files/paper/2023/hash/86c17de05579cde52025f9984e6e2ebb-Abstract-Conference.html)
- [S²IP-LLM: Semantic Space Informed Prompt Learning with LLM for Time Series Forecasting](https://openreview.net/forum?id=qwQVV5R8Y7)

##### Instruction Tuning: Synthetic-Data Alignment

Paired series-language corpora align temporal inputs with language representations.

Representative methods:

- [ChatTS: Aligning Time Series with LLMs via Synthetic Data for Enhanced Understanding and Reasoning](https://arxiv.org/abs/2412.03104)
- [Time-RA: Towards Time Series Reasoning for Anomaly Diagnosis with LLM Feedback](https://aclanthology.org/2026.findings-acl.562/)
- [TimeART: Towards Agentic Time Series Reasoning via Tool-Augmentation](https://arxiv.org/abs/2601.13653)

##### Instruction Tuning: Reasoning-Incentivized Tuning

Reward-based objectives encourage multi-step temporal reasoning.

Representative methods:

- [Time Series Forecasting as Reasoning: A Slow-Thinking Approach with Reinforced LLMs](https://arxiv.org/abs/2506.10630)
- [Reasoning through Verifiable Forecast Actions: Consistency-Grounded RL for Financial LLMs](https://arxiv.org/abs/2605.21975)
- [Conversational Time Series Foundation Models: Towards Explainable and Effective Forecasting](https://arxiv.org/abs/2512.16022)

##### Instruction Tuning: Native Multimodal TSLM

The language or multimodal backbone is updated to process time series as a native modality.

Representative methods:

- [OpenTSLM: Time-Series Language Models for Reasoning over Multivariate Medical Text- and Time-Series Data](https://openreview.net/forum?id=FHDRzhKm0f)
- [From Recognition to Understanding: Unlocking Cognitive Time Series Reasoning with LLMs](https://arxiv.org/abs/2606.22126)
- [SciTS: Scientific Time Series Understanding and Generation with LLMs](https://openreview.net/forum?id=5YXccEP6uc)

### Workflow Autonomy (A3)

<p align="center">
  <img src="figure/agent_pipeline.png" alt="Pipeline of temporal agents" width="1000"/>
</p>
<p align="center">Pipeline of temporal agents</p>

Axis A3 records runtime, observation-dependent workflow autonomy.

#### L1 Predictor

The LLM produces the analytical output directly from the represented time series.

Representative methods:

- [Large Language Models Are Zero-Shot Time Series Forecasters](https://arxiv.org/abs/2310.07820)
- [Time-LLM: Time Series Forecasting by Reprogramming Large Language Models](https://openreview.net/forum?id=Unb5CVPtae)
- [ChatTS: Aligning Time Series with LLMs via Synthetic Data for Enhanced Understanding and Reasoning](https://arxiv.org/abs/2412.03104)
- [OpenTSLM: Time-Series Language Models for Reasoning over Multivariate Medical Text- and Time-Series Data](https://openreview.net/forum?id=FHDRzhKm0f)

#### L2 Augmenter

The LLM supplies semantic features, contextual signals, or explanations to a fixed predictive pipeline.

Representative methods:

- [RAAD-LLM: Adaptive Anomaly Detection Using LLMs and RAG Integration](https://arxiv.org/abs/2503.02800)
- [PaP-NF: Probabilistic Long-Term Time Series Forecasting via Prefix-as-Prompt Reprogramming and Normalizing Flows](https://doi.org/10.1007/978-3-032-31930-2_7)
- [FSTLLM: Spatio-Temporal LLM for Few Shot Time Series Forecasting](https://proceedings.mlr.press/v267/jiang25a.html)
- [Reasoning through Verifiable Forecast Actions: Consistency-Grounded RL for Financial LLMs](https://arxiv.org/abs/2605.21975)

#### L3 Orchestrator

A single stateful agent uses intermediate observations to plan the workflow and invoke models or tools.

Representative methods:

- [TimeClaw: A Time-Series AI Agent with Exploratory Execution Learning](https://arxiv.org/abs/2605.10038)
- [TimeART: Towards Agentic Time Series Reasoning via Tool-Augmentation](https://arxiv.org/abs/2601.13653)
- [Conversational Time Series Foundation Models: Towards Explainable and Effective Forecasting](https://arxiv.org/abs/2512.16022)
- [S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis](https://doi.org/10.1109/SAFEPROCESS67117.2025.11268252)

#### L4 Multi-Agent Collaboration

Multiple specialized agents exchange intermediate results and close the loop through validation and refinement.

Representative methods:

- [TradingAgents: Multi-Agents LLM Financial Trading Framework](https://openreview.net/forum?id=4QPrXwMQt1)
- [FLAIRR-TS - Forecasting LLM-Agents with Iterative Refinement and Retrieval for Time Series](https://aclanthology.org/2025.findings-emnlp.834/)
- [ZARA: Training-Free Motion Time-Series Reasoning via Evidence-Grounded LLM Agents](https://aclanthology.org/2026.acl-long.684/)
- [TRACE: Unlocking the Potential of LLMs in Time Series Forecasting for Distributed Energy Resources](https://doi.org/10.1109/TAI.2025.3572853)

### Analytical Tasks (A4)

Axis A4 records the core analytical objective addressed by the system.

#### Forecasting

The system predicts future values or trajectories.

Representative methods:

- [TradingAgents: Multi-Agents LLM Financial Trading Framework](https://openreview.net/forum?id=4QPrXwMQt1)
- [Time-LLM: Time Series Forecasting by Reprogramming Large Language Models](https://openreview.net/forum?id=Unb5CVPtae)
- [TRACE: Unlocking the Potential of LLMs in Time Series Forecasting for Distributed Energy Resources](https://doi.org/10.1109/TAI.2025.3572853)
- [TimeOmni-1: Incentivizing Complex Reasoning with Time Series in Large Language Models](https://openreview.net/forum?id=kOIclg7muL)

#### Anomaly Detection

The system identifies unusual observations, segments, or temporal behavior.

Representative methods:

- [Can Large Language Models be Anomaly Detectors for Time Series?](https://doi.org/10.1109/DSAA61799.2024.10722786)
- [Time-RA: Towards Time Series Reasoning for Anomaly Diagnosis with LLM Feedback](https://aclanthology.org/2026.findings-acl.562/)
- [RAAD-LLM: Adaptive Anomaly Detection Using LLMs and RAG Integration](https://arxiv.org/abs/2503.02800)
- [S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis](https://doi.org/10.1109/SAFEPROCESS67117.2025.11268252)

#### Classification

The system assigns a time series or temporal segment to a class.

Representative methods:

- [OpenTSLM: Time-Series Language Models for Reasoning over Multivariate Medical Text- and Time-Series Data](https://openreview.net/forum?id=FHDRzhKm0f)
- [From Recognition to Understanding: Unlocking Cognitive Time Series Reasoning with LLMs](https://arxiv.org/abs/2606.22126)
- [SciTS: Scientific Time Series Understanding and Generation with LLMs](https://openreview.net/forum?id=5YXccEP6uc)
- [ZARA: Training-Free Motion Time-Series Reasoning via Evidence-Grounded LLM Agents](https://aclanthology.org/2026.acl-long.684/)

#### Imputation

The system estimates missing values in a temporal sequence.

Representative methods:

- [EVIL: Evolving Interpretable Algorithms for Zero-Shot Inference on Event Sequences and Time Series with LLMs](https://arxiv.org/abs/2604.15787)
- [U-STS-LLM: A Unified Spatio-Temporal Steered Large Language Model for Traffic Prediction and Imputation](https://arxiv.org/abs/2605.11735)
- [TimeOmni-VL: Unified Models for Time Series Understanding and Generation](https://openreview.net/forum?id=uUnIAtZUfX)
- [Time-MQA: Time Series Multi-Task Question Answering with Context Enhancement](https://aclanthology.org/2025.acl-long.1437/)
