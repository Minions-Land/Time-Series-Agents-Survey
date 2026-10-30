# Table 1 grading evidence (revised 2026-10-30)

Scale (3 levels): ● treated systematically in a dedicated part of the review; ◐ discussed without systematic treatment; ○ absent or mentioned only in passing.
Records: ● per-work records linked to source passages; ◐ per-work codes or annotations without such links; ○ neither.
Borderline cells for prior surveys were given the higher grade.

| Survey | Unit | LLM | Runtime | Temporal validity | Evaluation | Records |
|---|---|---|---|---|---|---|
| Zhang (promptstoagents2026) | Paper | ● | ● | ○ | ● | ◐ |
| Chang (changsurvey2026) | Paper | ● | ● | ◐ | ◐ | ◐ |
| Chen (chen2026tsagentsurvey) | System | ◐ | ● | ○ | ● | ◐ |
| Xu (xu2026forecastagentsurvey) | System | ● | ● | ● | ● | ○ |
| Ours | Module | ● | ● | ● | ● | ● |

Zhang full text: Zenodo record 17492801 v2 (2025-10-31), 36 pages. Earlier repo-only grades were wrong on Runtime (memory and self-refinement are §5.3–5.4).

- Zhang: §2.6 LLMs for TS, §4 Prompts (4.1 direct prompts, 4.2 instruction tuning) → LLM ●; §5 Agents (5.1 planning and reasoning, 5.2 tool use, 5.3 memory, 5.4 self-refinement) → Runtime ●; zero matches for leak/look-ahead/cut-off/contamination in the full text → Temporal validity ○; §7 Benchmarks and Evaluation (7.1 datasets, 7.2 comparative analysis) + §8.4 evaluation gap → Evaluation ●; GitHub repo with coded CSV (A1–A4) but no source locators → Records ◐.
- Chang: §2.5.4 adaptation regimes tagged per paper → LLM ●; §2.5.1–2.5.3 control flow, actors, knowledge access → Runtime ●; leakage raised about six times as an evaluation pitfall in §6 (lines on leakage-aware splits, explicit leakage checks), no dedicated treatment → ◐; §6.1 datasets and benchmarks + Table 1 reporting requirements → Evaluation ◐; repo per-paper tag tables + appendix Tables 3–5 → Records ◐.
- Chen: training mentioned in §2 and the §6 online-adaptation paragraph (5 lines on fine-tuning/SFT/RL) → LLM ◐ (borderline, graded up); §3 architecture/tools/memory applied to every family in Tables 3–4 → Runtime ●; one line on contamination → Temporal validity ○; §5 resources by problem type, Tables 5–7, §6 benchmarking agent workflows → Evaluation ●; Table 3 annotates 47 systems, no repo → Records ◐.
- Xu: §3.1 serialization/tokenization + §4 training and adaptation incl. RL → LLM ●; §3.2–3.5 orchestration, tools, live evidence, hybrid → Runtime ●; §2.3 admissibility, §5.2 contamination and leakage incl. revisions, Table 4 leakage column → Temporal validity ●; §5.1–5.5 + Table 5 + §4.3 ablations → Evaluation ●; "living snapshot" mentioned without URL → Records ○. Table 6 is component-level but catalogs failure modes, not a classification of works.
- Ours: §3 LLM-side contributions → ●; §4 five mechanism dimensions → ●; §5.4 temporal validation, availability equation, §7 evaluation contract → ●; §7 benchmarks, infrastructure, benchmark selection → ●; Paper Card schema + JSON ledger with locator/quote/source_path → Records ●.

Distinctive, non-circular differences: unit of analysis (module, one paper can span layers) and source-linked records. Shared strengths are shown as ties; Xu matches ours on four of five graded columns.
