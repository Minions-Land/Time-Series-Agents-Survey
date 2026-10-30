# Table 1 grading evidence (2026-10-30)

Scale 0–4 (Harvey balls): 0 not addressed; 1 mentioned in passing; 2 dedicated discussion, not organizing; 3 organizing axis for part of the review or systematic but incomplete; 4 organizing axis with systematic coverage.
Resources: 1 representative tables; 2 per-paper annotations in paper; 3 maintained repo with per-paper codes; 4 machine-readable records with source-evidence locators.

| Survey | Adapt | Tasks | Runtime | Reuse | Eval | Res | (Leakage, not in table) |
|---|---|---|---|---|---|---|---|
| Zhang (promptstoagents2026) | 4 | 4 | 3? | 0? | 2? | 3 | ? |
| Chang (changsurvey2026) | 3 | 4 | 3 | 0 | 2 | 3 | 1 |
| Chen (chen2026tsagentsurvey) | 1 | 4 | 3 | 1 | 3 | 2 | 0 |
| Xu (xu2026forecastagentsurvey) | 3 | 1 | 3 | 0 | 4 | 1 | 4 |
| Ours | 3 | 4 | 4 | 4 | 4 | 4 | 3 |

Zhang: SSRN full text returned 403; grades come from the author repo CoderPowerBeyond/Agent-Prompt-TS-Survey (README, data/coded_papers.csv with A1–A4 codes, provenance/search_log.csv). "?" = uncertain. Re-check if the PDF becomes available.

- Zhang: A1 Representation + A2 Model Adaptation coded per paper (D1=4); A4 forecasting/anomaly/classification/imputation (D2=4); A3 Workflow Autonomy L1–L4, no memory/self-improvement axis visible (D3=3?); no reuse-scope axis (D4=0?); README promises workflow-level evaluation, depth unknown (D6=2?); maintained repo with coded CSV, no locators (D7=3).
- Chang: §2.5.4 adaptation regimes tagged per paper (D1=3); §2.4 Primary Objective × §3–5 topologies, 11 tasks (D2=4); §2.5.1–2.5.3 control flow, actors, knowledge access (D3=3); attributes are cross-cutting, not reuse scope (D4=0); leakage only in §6.1/§6.3 (D5=1); §6.1 datasets + Table 1 reporting requirements (D6=2); repo per-paper tag tables + App. Tables 3–5 (D7=3).
- Chen: training only in §2 and §6 Online Adaptation (D1=1); §4.1–4.4 four families organize the survey (D2=4); §3 Architecture/Tools/Memory applied in Tables 3–4 (D3=3); shared dimensions but no module reuse classification (D4=1); no look-ahead treatment (D5=0); §5 Resources, Tables 5–7, §6 benchmarking workflows (D6=3); Table 3 annotates 47 systems, no repo found (D7=2).
- Xu: §3.1 serialization/tokenization + §4 training incl. RL (D1=3); scope forecasting/prediction only §2.1 (D2=1); §3.2–3.5 orchestration/tools/evidence/hybrid (D3=3); grouping by LLM coupling, not reuse scope (D4=0); §2.3 admissibility, §5.2 contamination/leakage incl. revisions, Table 4 leakage column (D5=4); §5.1–5.5 + Table 5 + §4.3 ablations (D6=4); "living snapshot" mentioned without URL (D7=1).
- Ours: §3 LLM-side, not organizing elsewhere (D1=3); §6 four families + §7 temporal QA (D2=4); §4 five mechanism dims reused across layers (D3=4); module unit + §4–6 + ledger appendix (D4=4); §5.4 temporal validation, availability equation, §7 evaluation contract, but benchmarks not graded by leakage control (D5=3); §7 evaluation contract, benchmark families, infrastructure, benchmark selection (D6=4); Paper Card schema + JSON ledger with locator/quote/source_path (D7=4).

D5 (leakage) was left out of the table only because Zhang cannot be verified; the main text credits Xu's stronger treatment. Swap in D5 if the Zhang PDF is obtained.
