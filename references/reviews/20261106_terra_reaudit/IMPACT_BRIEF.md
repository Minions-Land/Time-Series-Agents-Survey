# Task-impact coding brief (rubric node R11)

The survey asks what Time Series Agents actually change for their downstream tasks. For one work, the question is
whether it (a) automates analytical steps, (b) raises a score on an existing protocol, or (c) addresses a concrete
time series obstacle, such as leakage, drift, missing data, context, decision costs, verifiability or deployment, and
tests that it does. Your job is to code this from the source, conservatively.

## Inputs (this folder; only the keys you are given)

- `rubric_tree.yaml`, node `R11_task_impact`. It is binding, and its values are a closed vocabulary.
- `out_final/<key>.json` - the adjudicated Paper Card record: claim, modules (with ids), task memberships and
  evaluation evidence. Start here.
- `packets/<key>.txt` - the source text with `L<n>: ` line prefixes. It is the only evidence. Use it to confirm each
  quote and to read the experiments section.

## Output: `impact/<key>.json`

```json
{
  "citation_key": "<key>",
  "primary_gain": "automation | metric_gain | practical_problem | measurement",
  "tasks": [
    {"task": "forecasting_prediction",
     "automates": true,  "automation_evidence": {"line": 12, "quote": "..."},
     "metric_gain": true, "metric_evidence": {"line": 300, "quote": "..."},
     "practical_problems": [
       {"problem": "information_availability", "modules": ["<key>:<slug>"], "tested": true,
        "evidence": {"line": 410, "quote": "..."}, "note": "what the experiment varies or measures"}
     ]}
  ],
  "summary": "One sentence: what the work changes for the task, and what its evaluation shows.",
  "confidence": "high | medium | low"
}
```

## Rules

1. Add one entry to `tasks` for each of the four task families in the record's `task_memberships`. If the record
   has none, use `other:<name>`, for example `other:temporal_question_answering`.
2. `automates` and `metric_gain` are booleans. When either is true, quote the passage that supports it.
3. List a practical problem only if the work names it and a module or procedure targets it. Set `tested: true` only if
   an experiment varies, isolates or measures that obstacle: a leakage-controlled split, a shift or out-of-domain test,
   a missing-rate sweep, an ablation of the context source, an evaluation of costs or utility, a faithfulness or
   operator study, or a deployment report. A better average score on a standard split is `metric_gain`, not a tested
   problem. The quote for a tested problem must come from the experiment that tests it.
4. `primary_gain` is the strongest gain the evaluation supports. Use `practical_problem` only if at least one problem
   is tested. Use `measurement` for benchmarks, datasets and environments.
5. Quotes must be verbatim from the packet, at most 300 characters, and may run over at most 4 lines. `line` is the
   line the quote starts on.
6. Run `python3 check_impact.py impact/<key>.json` and fix the record until it prints `OK`.
7. Write only `impact/<key>.json` for your keys. No network.
8. Final message: one line per key, in the form `key: primary_gain; tested problems; untested problems`.
