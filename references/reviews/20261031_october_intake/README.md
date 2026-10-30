# October 2026 corpus intake

Search and review: 31 October 2026. Scope: works whose first public version (arXiv v1) is dated October 2026.

## Search

The official arXiv API was queried with `submittedDate:[202610010000 TO 202610312359]` and the following conditions (all fields): "time series" or abs:"time-series" with agent/agents/agentic; forecasting, forecast, anomaly detection, root cause, sensor, telemetry/monitoring/predictive maintenance, ECG/EEG/wearable/physiological, spatiotemporal, trading/stock/portfolio, each with agent terms and LLM/language model; "time series" with LLM/language model, reasoning, harness, benchmark, reinforcement learning/GRPO/RLVR, foundation model, multimodal, and question answering/captioning/classification; energy/load/weather/climate forecasting with agent terms; fault diagnosis, sensor data/IoT, and clinical/ICU forecasting with LLM terms; forecasting with tools/workflow and LLM terms. The 28 queries returned 379 unique records. The API index was last updated on 30 October 2026, so submissions announced after that date are not covered.

## Screening and review

Titles and abstracts were screened against the precedents in `time_series_agent_screening_audit.csv`. Thirty-one records were excluded at abstract level and 38 were read in full. `october_review.json` holds the full-text records: decision and reason, claim, task memberships, evaluation summary, cautions, inspected pages, author-attributed resources with availability checks, and, for included works, source-located modules. Every module quotation and resource provenance quotation matches its declared PDF page under the normalization in `scripts/audit_review_evidence.py`.

Reviewer decisions were adjudicated before integration; `adjudication_note` records each change. FairAMO, the LLM-written anomaly detector, Vendster and WxCrop were retained as boundary works; the execution-assumption trading study was excluded; one minor Zephyrus-R1 interface module was removed.

## Outcome

28 works were retained (19 new public corpus, 9 boundary) with 67 modules: 4 LLM, 12 GH, 8 GTS and 43 TSK. Ten full-text candidates were excluded. Event forecasting from news or prediction markets (AlphaBet, EvoForesight, Do Your Own Research, JockeyBench) follows the existing exclusion of InfoDelphi and ForeDreamer, although the ledger also retains several event-forecasting works added during the Zotero integration; this boundary remains open for editorial review.
