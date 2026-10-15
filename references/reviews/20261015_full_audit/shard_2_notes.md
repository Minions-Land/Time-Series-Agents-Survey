# Shard 2 source audit

43 records / 87 module claims: GH 23, GTS 11, TSK 42, LLM 11. 42 records have local PDF evidence; LLM-TSFD has repository evidence only. This is source verification of identity and selected method/evaluation passages, not independent reproduction of experimental results. Every evidence quote is a contiguous 20–80-word passage from its recorded source page or repository snapshot.

## Manuscript corrections supported by this audit

- **TimeCAP:** the contextualizer-summary/predictor equation describes preliminary TIMECP (§3.2), not full TimeCAP. Full TimeCAP adds a multimodal encoder, nearest-neighbor summary/label retrieval, and weighted fusion of LLM and multimodal predictions (PDF p.4). The LLM is frozen; encoder training is not LLM weight training.
- **TimeClaw Explore:** explore/compare/distill and memory injection are GH mechanisms. Runtime-native temporal object tools and signal/text memory belong to the separate TimeClaw Harness paper. Do not merge their attributed innovations.
- **TSAG:** its PDF p.3 states that tools contain expected benchmark outputs. Its 100-query evaluation establishes routing/arguments/output-hallucination behavior with stubs; it does not establish numerical forecasting performance.
- **TFRBench:** reference creation uses oracle future events (PDF p.8). The evaluated forecaster sees historical information only. The reference-generation loop is not an ex-ante operational forecasting procedure.
- **TraceBench and TimeSeriesGym:** both supply actual agent-oriented time-series evaluation. A blanket claim that no such benchmark exists is false. TraceBench measures simulator-grounded causal answers and execution traces; TimeSeriesGym provides 34 artifact/validator challenges across 23 sources and 8 problem types.
- **FinMem:** temporal decay/promotion is coupled to news, financial filings and trading success. This module is TSK financial decision memory, not GTS merely because it has timestamps.
- **AnomaMind:** PDF pp.5–6 supports trajectory state update, interval detector, parser/F1/false-positive reward, and expected-return training. The detector is trained; surrounding general-purpose reasoning is not shown to receive the same update.
- **TRACE:** PDF issue is February 2026, while the user-supplied Bib reports 2025. Preserve separate publication/online dates. Prompt instruction tuning alone does not establish weight updates; p.7 says no retraining.
- **LLM-TSFD:** source snapshots in `shard_2_sources/llm-tsfd/` confirm partial code and mock data. With `_max_retries=1`, the shown loop does not execute its newly repaired code after the first failure. Do not claim robust repair or journal-result reproduction from this repository.

## Initial nine records

`initial_9_review.json` was additionally rechecked for all 19 existing module IDs. Interleaved old two-column extracts were replaced by contiguous page-text evidence; module IDs/layers retained. ScenarioDiff's preliminary DDPM objective was replaced as module evidence with the actual Section IV.A conditional denoising and Anchor Blended Sampling description. Each record has `evidence_recheck` provenance and inspected pages.
