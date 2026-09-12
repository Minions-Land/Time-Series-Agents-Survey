# Remaining Full-Text Evidence Handoff

> Scope: papers with abstract/classification records but no readable PDF evidence in `paper_classification_ledger.json`. Do not treat a URL or BibTeX receipt as full-text evidence.

## Required workflow

1. Open the official URL and download the paper or accepted manuscript.
2. Confirm the file starts with `%PDF` and `pdftotext` can read it.
3. Rename it to `<citation_key>.pdf` and place it in `references/source_snapshots/candidate_pdfs/`.
4. Record page/section/table/figure locators and exact quotations in `source_evidence_json`.
5. Keep the existing abstract claim and GH/GTS/TSK/task-axis labels unless the full paper justifies a correction.

## Queue

| citation key | title | official URL | acquisition note |
|---|---|---|---|
| `moiraiagent2026` | MoiraiAgent: Context-Aware Time Series Forecasting Agent | https://github.com/SalesforceAIResearch/uni2ts/tree/main/project/moirai-agent | ACL/PMLR/open repository: download and validate |
| `fromnewstoforecast2024` | From News to Forecast: Integrating Event Analysis in LLM-Based Time Series Forecasting with Reflection | https://arxiv.org/pdf/2409.17515 | arXiv/open PDF: download and validate |
| `grammarwave2026` | Grammar of the Wave: Towards Explainable Multivariate Time Series Event Detection via Neuro-Symbolic VLM Agents | https://arxiv.org/pdf/2603.11479 | arXiv/open PDF: download and validate |
| `forecastcompass2026` | ForecastCompass: Guiding Agentic Forecasting with Adaptive Factor Memory | https://arxiv.org/pdf/2605.30858 | arXiv/open PDF: download and validate |
| `siren2026` | SIREN: Towards End-to-End Extreme-Weather Early Warning with Experience-Grounded LLM Agents | https://arxiv.org/pdf/2607.24588 | arXiv/open PDF: download and validate |
| `alphacast2026` | AlphaCast: A Human Wisdom-LLM Intelligence Co-Reasoning Framework for Interactive Time Series Forecasting | https://arxiv.org/pdf/2511.08947 | arXiv/open PDF: download and validate |
| `newscompetition2025` | Can Competition Enhance the Proficiency of Agents Powered by Large Language Models in the Realm of News-driven Time Series Forecasting? | https://arxiv.org/pdf/2504.10210 | arXiv/open PDF: download and validate |
| `dcats2025` | Empowering Time Series Forecasting with LLM-Agents | https://arxiv.org/pdf/2508.04231 | arXiv/open PDF: download and validate |
| `timecopilot2025` | TimeCopilot | https://arxiv.org/pdf/2509.00616 | arXiv/open PDF: download and validate |
| `bridge2025` | {BRIDGE}: Bootstrapping Text to Control Time-Series Generation via Multi-Agent Iterative Optimization and Diffusion Modeling | https://proceedings.mlr.press/v267/li25ah.html | ACL/PMLR/open repository: download and validate |
| `adagent2025` | AD-AGENT: A Multi-agent Framework for End-to-end Anomaly Detection | https://aclanthology.org/2025.findings-ijcnlp.11.pdf | ACL/PMLR/open repository: download and validate |
| `agentfm2025` | AgentFM: Role-Aware Failure Management for Distributed Databases with LLM-Driven Multi-Agents | https://arxiv.org/pdf/2504.06614 | arXiv/open PDF: download and validate |
| `llmlight2025` | LLMLight: Large Language Models as Traffic Signal Control Agents | https://arxiv.org/pdf/2312.16044 | arXiv/open PDF: download and validate |
| `collmllight2026` | CoLLMLight: Cooperative Large Language Model Agents for Network-Wide Traffic Signal Control | https://arxiv.org/pdf/2503.11739 | arXiv/open PDF: download and validate |
| `openti2024` | Open-TI: Open Traffic Intelligence with Augmented Language Model | https://arxiv.org/pdf/2401.00211 | arXiv/open PDF: download and validate |
| `chow2024tsreasoning` | Towards Time-Series Reasoning with LLMs | https://arxiv.org/pdf/2409.11376 | arXiv/open PDF: download and validate |
| `chang2024llm4ts` | LLM4TS: Aligning Pre-trained LLMs as Data-Efficient Time-Series Forecasters | https://arxiv.org/pdf/2308.08469 | arXiv/open PDF: download and validate |
| `ji2025lemad` | LEMAD: LLM-Empowered Multi-Agent System for Anomaly Detection in Power Grid Services | https://mdpi-res.com/d_attachment/electronics/electronics-14-03008/article_deploy/electronics-14-03008.pdf | Publisher or institutional access may be required |
| `wang2025agentic` | Agentic Large Language Models for day-to-day Route Choices | https://research.monash.edu/files/778079903/766251603-oa.pdf | Publisher or institutional access may be required |
| `zhang2025llm` | LLM-TSFD: An Industrial Time Series Human-in-the-Loop Fault Diagnosis Method Based on a Large Language Model | https://github.com/zq300/LLM-TSFD | ACL/PMLR/open repository: download and validate |
| `lastmileforecast2026` | Bridging the Last Mile of Time Series Forecasting with LLM Agents | https://arxiv.org/pdf/2606.02497 | arXiv/open PDF: download and validate |
| `multimodaltsad2026` | Can Multimodal LLMs Perform Time Series Anomaly Detection? | https://arxiv.org/pdf/2502.17812 | arXiv/open PDF: download and validate |
| `multimodaldebate2026` | Multimodal Collaborative Debate for Zero-Shot Time Series Reasoning | https://arxiv.org/pdf/2601.19151 | arXiv/open PDF: download and validate |
| `physiologicalagent2025` | An LLM-Powered Agent for Physiological Data Analysis: A Case Study on PPG-based Heart Rate Estimation | https://arxiv.org/pdf/2502.12836 | arXiv/open PDF: download and validate |
| `flairrts2025` | FLAIRR-TS: Forecasting LLM-Agents with Iterative Refinement and Retrieval for Time Series | https://arxiv.org/pdf/2508.19279 | arXiv/open PDF: download and validate |
| `structuredagenticworkflows2025` | Structured Agentic Workflows for Financial Time-Series Modeling with LLMs and Reflective Feedback | https://arxiv.org/pdf/2508.13915 | arXiv/open PDF: download and validate |
| `tradetonottrade2025` | To Trade or Not to Trade: An Agentic Approach to Estimating Market Risk Improves Trading Decisions | https://arxiv.org/pdf/2507.08584 | arXiv/open PDF: download and validate |
| `heraldlight2025` | A Dual Large Language Models Architecture with Herald Guided Prompts for Parallel Fine Grained Traffic Signal Control | https://arxiv.org/pdf/2511.00136 | arXiv/open PDF: download and validate |
| `virtualtrafficpolice2026` | Virtual Traffic Police: Large Language Model-Augmented Traffic Signal Control for Unforeseen Incidents | https://arxiv.org/pdf/2601.15816 | arXiv/open PDF: download and validate |
| `gridagent2025` | Grid-Agent: An LLM-Powered Multi-Agent System for Power Grid Control | https://arxiv.org/pdf/2508.05702 | arXiv/open PDF: download and validate |
| `elliottagents2025` | ElliottAgents: A Natural Language-Driven Multi-Agent System for Stock Market Analysis and Prediction | https://arxiv.org/pdf/2507.03435 | arXiv/open PDF: download and validate |
| `finmem2023` | FinMem: A Performance-Enhanced LLM Trading Agent with Layered Memory and Character Design | https://arxiv.org/pdf/2311.13743 | arXiv/open PDF: download and validate |
| `trafficr12025` | Traffic-R1: Reinforced LLMs Bring Human-Like Reasoning to Traffic Signal Control Systems | https://arxiv.org/pdf/2508.02344 | arXiv/open PDF: download and validate |
| `curalight2026` | CuraLight: Debate-Guided Data Curation for LLM-Centered Traffic Signal Control | https://arxiv.org/pdf/2604.05663 | arXiv/open PDF: download and validate |
| `tradingagents2024` | TradingAgents: Multi-Agents LLM Financial Trading Framework | https://arxiv.org/pdf/2412.20138 | arXiv/open PDF: download and validate |
| `atlas2025` | ATLAS: Adaptive Trading with LLM AgentS Through Dynamic Prompt Optimization and Multi-Agent Coordination | https://arxiv.org/pdf/2510.15949 | arXiv/open PDF: download and validate |
| `finrldeepseek2025` | FinRL-DeepSeek: LLM-Infused Risk-Sensitive Reinforcement Learning for Trading Agents | https://arxiv.org/pdf/2502.07393 | arXiv/open PDF: download and validate |
| `merit2025` | MERIT: Multi-Agent Collaboration for Unsupervised Time Series Representation Learning | https://aclanthology.org/2025.findings-acl.1231.pdf | ACL/PMLR/open repository: download and validate |
| `climateagent2025` | CLIMATEAGENT: Multi-Agent Orchestration for Complex Climate Data Science Workflows | https://arxiv.org/pdf/2511.20109 | arXiv/open PDF: download and validate |
| `hydroagentcalibration2026` | HydroAgent: Closing the Gap Between Frontier LLMs and Human Experts in Hydrologic Model Calibration via Simulator-Grounded RL | https://arxiv.org/pdf/2605.17792 | arXiv/open PDF: download and validate |
| `pandaai2026` | PandaAI: A Practical Agent CQ2 for Neuro-symbolic Data Analysis And Integrated Decision-Making in Quantitative Finance | https://arxiv.org/pdf/2606.06823 | arXiv/open PDF: download and validate |
| `genautoml2026` | GenAutoML: An Agentic Framework for Dynamic Architecture Generation and Optimization in Time-Series Analysis | https://arxiv.org/pdf/2606.05860 | arXiv/open PDF: download and validate |
| `s2sfdd2026` | S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis | https://arxiv.org/pdf/2603.08048 | arXiv/open PDF: download and validate |
| `memcast2026` | MemCast: Memory-Driven Time Series Forecasting with Experience-Conditioned Reasoning | https://arxiv.org/pdf/2602.03164 | arXiv/open PDF: download and validate |
| `mosaic2026` | MOSAIC: Modular Orchestration for Structured Agentic Intelligence and Composition | https://arxiv.org/pdf/2606.00708 | arXiv/open PDF: download and validate |

## Evidence JSON template
```json
{"source_evidence": [{"locator_type": "page|section|table|figure", "locator": "PDF p.X, Section Y", "quote": "Exact quotation", "supports": "Claim or classification supported"}]}
```
