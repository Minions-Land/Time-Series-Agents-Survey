# Re-audit check report

Records: 165 (valid 154, with errors 11, invalid JSON 0).
Module decisions: add 2, change 250, drop 7, keep 23, merge 2, split 93.
Layer moves: {'GH->TSK': 15, 'TSK->GTS': 15, 'GH->GTS': 8, 'TSK->GH': 3, 'GTS->TSK': 7, 'GH->LLM': 4, 'GTS->GH': 1, 'TSK->LLM': 1, 'LLM->GTS': 1}. New module ids: 250.
Final modules by layer: GH 74, GTS 98, LLM 92, TSK 333.
Dimensions used: {'Planning and Orchestration': 280, 'Tools and Execution': 229, 'Memory and Context': 122, 'Interface and Interaction': 85, 'Optimization and Evolution': 50}.
Evaluation evidence present: process_validity 64, temporal_validity 104, task_performance 158, decision_utility 31.
Needs human review: 6. Blind vs final layer profile: {'same_layer_profile': 155, 'different_layer_profile': 10}.

## Records with errors

- `agenticrag2024`: claim quote L59
- `aqua2026`: eval decision_utility quote
- `hydroagent2026`: hydroagent2026:flood-prior-skill no dimension; hydroagent2026:hydrological-scheme no dimension
- `lastmile2026`: lastmile2026:forecast-workspace no dimension; lastmile2026:revision-memory no dimension; lastmile2026:event-mapreduce no dimension
- `reasoncast2026`: reasoncast2026:structured-reasoning-data quote L2241
- `scenariodiff2026`: eval temporal_validity quote
- `streasoner2026`: streasoner2026:sde-synthesis no dimension
- `timeseriesscientist2025`: timeseriesscientist2025:reporter quote L325
- `wawer2025integrating`: wawer2025integrating:investment-synthesis quote L321
- `zephyrusr12026`: zephyrusr12026:verifiable-analysis-verifier no dimension; zephyrusr12026:grounded-report-reward no dimension; zephyrusr12026:report-grounding-gate no dimension
- `zhang2025llm`: zhang2025llm:prompted-ts-procedure no dimension
