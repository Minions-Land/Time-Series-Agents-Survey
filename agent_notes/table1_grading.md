# Table 1 grading evidence (revised 2026-10-30, five levels)

Scale: ● (4) systematic and complete, organizing the review or coded for every work; ◕ (3) systematic but covering only part of the dimension; ◑ (2) dedicated discussion without systematic treatment; ◔ (1) mentioned in passing; ○ (0) absent.
Records: ◔ representative examples; ◑ per-work annotations in the paper; ◕ maintained repository with per-work codes; ● per-work records linked to source passages.
Borderline cells for prior surveys were given the higher grade. Harvey balls are drawn in surveyBlue (#1F4E79).

| Survey | Unit | LLM | Runtime | Temporal validity | Evaluation | Records |
|---|---|---|---|---|---|---|
| Zhang (promptstoagents2026) | Paper | 4 | 4 | 0 | 3 | 3 |
| Chang (changsurvey2026) | Paper | 3 | 3 | 1 | 2 | 3 |
| Chen (chen2026tsagentsurvey) | System | 2 | 3 | 0 | 3 | 2 |
| Xu (xu2026forecastagentsurvey) | System | 4 | 3 | 4 | 4 | 1 |
| Ours | Module | 4 | 4 | 3 | 4 | 4 |

Five-level rationale beyond the notes below: Chang LLM 3 (adaptation regimes coded per paper, no representation axis); Chang/Chen/Xu Runtime 3 (no systematic memory or self-refinement axis); Chang Temporal validity 1 (leakage only in a related-work remark and a reporting recommendation); Chen LLM 2 (online-adaptation paragraph in §6, graded up); Chen Temporal validity 0 (its single "contamination" line concerns anomaly updates, not temporal leakage); Zhang Evaluation 3 (§7 datasets by primary task and a Weather-only comparison; components not linked); Xu LLM 4 (§3.1 representation plus §4 training and adaptation incl. RL); Ours LLM 4 (§3 plus llm_side_contribution coded for all 135 works with source evidence); Ours Temporal validity 3 (benchmarks not graded by leakage control; Xu is more complete).

Evidence by survey (grades on the five-level scale).

Zhang full text: Zenodo record 17492801 v2 (2025-10-31), 36 pages. Earlier repo-only grades were wrong on Runtime (memory and self-refinement are §5.3–5.4).

- Zhang: §2.6 LLMs for TS, §4 Prompts (4.1 direct prompts, 4.2 instruction tuning) → LLM 4; §5 Agents (5.1 planning and reasoning, 5.2 tool use, 5.3 memory, 5.4 self-refinement) → Runtime 4; zero matches for leak/look-ahead/cut-off/contamination in the full text → Temporal validity 0; §7 Benchmarks and Evaluation (7.1 datasets, 7.2 comparative analysis) + §8.4 evaluation gap → Evaluation 3; GitHub repo with coded CSV (A1–A4) but no source locators → Records 3.
- Chang: §2.5.4 adaptation regimes tagged per paper → LLM 3; §2.5.1–2.5.3 control flow, actors, knowledge access → Runtime 3; leakage raised about six times as an evaluation pitfall in §6 (lines on leakage-aware splits, explicit leakage checks), no dedicated treatment → 1; §6.1 datasets and benchmarks + Table 1 reporting requirements → Evaluation 2; repo per-paper tag tables + appendix Tables 3–5 → Records 3.
- Chen: training mentioned in §2 and the §6 online-adaptation paragraph (5 lines on fine-tuning/SFT/RL) → LLM 2; §3 architecture/tools/memory applied to every family in Tables 3–4 → Runtime 3; one line on contamination → Temporal validity 0; §5 resources by problem type, Tables 5–7, §6 benchmarking agent workflows → Evaluation 3; Table 3 annotates 47 systems, no repo → Records 2.
- Xu: §3.1 serialization/tokenization + §4 training and adaptation incl. RL → LLM 4; §3.2–3.5 orchestration, tools, live evidence, hybrid → Runtime 3; §2.3 admissibility, §5.2 contamination and leakage incl. revisions, Table 4 leakage column → Temporal validity 4; §5.1–5.5 + Table 5 + §4.3 ablations → Evaluation 4; "living snapshot" mentioned without URL → Records 1. Table 6 is component-level but catalogs failure modes, not a classification of works.
- Ours: §3 LLM-side contributions → 4; §4 five mechanism dimensions → 4; §5.4 temporal validation, availability equation, §7 evaluation contract → 3; §7 benchmarks, infrastructure, benchmark selection → 4; Paper Card schema + JSON ledger with locator/quote/source_path → Records 4.

Distinctive, non-circular differences: unit of analysis (module, one paper can span layers) and source-linked records. Shared strengths are shown as ties; Xu matches ours on four of five graded columns.
