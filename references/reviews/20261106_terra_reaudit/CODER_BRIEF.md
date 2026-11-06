# Paper Card re-audit: coder brief (one paper per run)

You re-audit ONE work of the survey "Time Series Agents: A Survey of LLMs, Harness Architectures, and Evaluation".
The survey classifies each concrete module a work contributes. Its rules changed since the current Paper Cards were
written (five mechanism dimensions instead of seven, explicit layer tests, temporal functions, reuse evidence,
evaluation evidence). Your job is a careful, source-grounded reclassification.

## Files (all inside this folder)

- `rubric_tree.yaml` - the classification rules. They are binding. Apply nodes R0-R10 in order.
- `packets/<key>.txt` - the work's text. Every line is prefixed `L<n>: `. This is your ONLY evidence.
- `cards/<key>.json` - the CURRENT Paper Card. Do not open it until Step A is written.

## Step A - blind classification

Read `rubric_tree.yaml`, then the whole packet (method, setup and experiments, not only the abstract).
Write `out/<key>.blind.json` with the schema below but WITHOUT `reconciliation`.

## Step B - reconcile with the current card

Now read `cards/<key>.json`. For every existing module decide `keep`, `change`, `merge`, `split` or `drop`, and
explain from the packet. Keep an existing `id` whenever the mechanism is the same (even if its layer or labels change);
give new modules ids `<key>:<short-slug>`. Revisit Step A if the card shows something you missed, but do not copy the
card: every module and label must be supported by the packet and the rubric. Write the final `out/<key>.json`.

## Output schema (JSON object, UTF-8)

```json
{
  "citation_key": "<key>",
  "status": "paper_verified | repository_verified | out_of_scope | blocked",
  "role_of_work": "llm_side_technique | fixed_workflow | feedback_driven_agent | resource | background",
  "claim_summary": "One sentence: what the work contributes, in the survey's terms.",
  "claim_evidence": [{"line": 12, "quote": "..."}],
  "task_memberships": ["forecasting_prediction"],
  "other_tasks": [],
  "modules": [
    {
      "id": "<key>:<slug>",
      "name": "Short noun phrase",
      "layer": "LLM | GH | GTS | TSK",
      "dimensions": ["Planning and Orchestration"],
      "functions": ["context_memory"],
      "view_status": "mapped | task_procedure | general_runtime | model_side | resource_level",
      "llm_route": [],
      "tasks": ["forecasting_prediction"],
      "other_tasks": [],
      "role": "method | model_training | training_data | infrastructure | evaluation",
      "scope_reason": "Why this layer: cite the R3 test that decided it (and the counterfactual for TSK/GTS).",
      "rubric_path": ["R1:contributed", "R2:Harness", "R3_1_TSK:no - ...", "R3_2_GTS:yes - ..."],
      "reuse_evidence": {"level": "demonstrated | inferred | not_applicable", "tasks": [], "basis": "module | work"},
      "evidence": [{"line": 240, "quote": "..."}],
      "confidence": "high | medium | low"
    }
  ],
  "evaluation_evidence": {
    "process_validity":  {"present": false, "line": null, "quote": null},
    "temporal_validity": {"present": true,  "line": 512, "quote": "..."},
    "task_performance":  {"present": true,  "line": 530, "quote": "..."},
    "decision_utility":  {"present": false, "line": null, "quote": null}
  },
  "reconciliation": [
    {"existing_id": "<old id>", "decision": "keep | change | merge | split | drop", "new_ids": ["<id>"],
     "changes": ["layer GH->GTS", "dimensions: Control, Verification, and Feedback -> Planning and Orchestration"],
     "reason": "..."}
  ],
  "needs_human_review": false,
  "notes": "Anything a human adjudicator should know (ambiguities, missing pages, disagreements with the card)."
}
```

## Rules

1. Vocabulary is closed: layers, the five dimensions, functions, view_status, llm_route, task families, roles and
   statuses exactly as in `rubric_tree.yaml`. Never output a retired seven-dimension label.
2. Harness modules (GH/GTS/TSK) need >= 1 dimension. GTS needs >= 1 function. LLM modules need >= 1 llm_route and
   no dimensions. TSK needs >= 1 task or other task.
3. Evidence: every module, the claim and every `present: true` evaluation item needs at least one quote. Copy the
   quote verbatim from the packet, without the `L<n>: ` prefix, at most 300 characters; it may continue over at most
   the next 4 lines. `line` is the first line it comes from. Quotes are checked by script; an unverifiable quote
   invalidates the record.
4. Prefer fewer, well-evidenced modules over many weak ones. Do not count baselines, unchanged off-the-shelf
   components or future work (R1).
5. When unsure between two layers, apply the R3 tests literally, choose one, set `confidence: low` and
   `needs_human_review: true`, and explain in `notes`.
6. Write only `out/<key>.blind.json` and `out/<key>.json`. Do not read other papers' outputs or modify any other file.
