# Survey-comparison basis

Checked 2026-10-15 against the local PDFs and the original companion repository. Marks describe an explicit organizing role, not whether a topic is ever mentioned.

- From Prompts to Agents: companion README A1 representation, A2 model adaptation, A3 workflow autonomy, A4 analytical task. Adaptation and multi-task organization are explicit; lifecycle is not an organizing axis. Snapshot: `prompts_survey_README.md`.
- A Survey of Reasoning and Agentic Systems in Time Series with Large Language Models: PDF p.1 and contents pp.2–3; Sections 2.4 primary objectives and 2.5.4 LLM adaptation regimes; the main organization is reasoning topology. Adaptation and multiple tasks are explicit; lifecycle is not the organizing sequence.
- LLM Agents for Time-Series: A Survey: PDF pp.2–3 Section 3 defines architecture, tools, memory; Section 4 uses four task families. Model-adaptation regimes and lifecycle are not separate organizing axes.
- LLM-based Agents for Forecasting and Prediction: Methods, Training, Evaluation, and Applications: PDF pp.1–3 states architectures, training, evaluation and deployment around scored prediction. Dedicated adaptation and lifecycle coverage; several applications share the prediction task family.

ModernTSF snapshot documents model and dataset resources, TOML configs, seeds, profiled outputs and an executable entry point. Main-text statements use these documented infrastructure features. Agent integration examples describe design use, not independently reproduced benchmark performance.
