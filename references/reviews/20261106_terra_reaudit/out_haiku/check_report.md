# Re-audit check report

Records: 13 (valid 12, with errors 1, invalid JSON 0).
Module decisions: change 17, keep 1, split 12.
Layer moves: {'GH->TSK': 3, 'GH->GTS': 1, 'TSK->GTS': 4, 'TSK->LLM': 3, 'GTS->TSK': 1, 'TSK->GH': 1}. New module ids: 29.
Final modules by layer: GH 11, GTS 10, LLM 10, TSK 27.
Dimensions used: {'Planning and Orchestration': 22, 'Tools and Execution': 20, 'Memory and Context': 9, 'Interface and Interaction': 9, 'Optimization and Evolution': 6}.
Evaluation evidence present: process_validity 6, temporal_validity 9, task_performance 12, decision_utility 2.
Needs human review: 13. Blind vs final layer profile: {'same_layer_profile': 9, 'different_layer_profile': 4}.

## Records with errors

- `zhang2025llm`: zhang2025llm:labeling-cleaning-procedure no dimension
