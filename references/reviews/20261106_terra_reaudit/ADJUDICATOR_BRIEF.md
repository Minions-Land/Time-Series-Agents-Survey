# Paper Card re-audit: adjudicator brief

Each work was re-audited by a model (Codex gpt-6.1-sol, or a Haiku fallback) following `CODER_BRIEF.md` and
`rubric_tree.yaml`. Some results need a second judgment: the coder flagged them, a module changed layer relative to the
published card, or Codex and Haiku produced different records. You adjudicate those works. Your record is final.

## Inputs (all in this folder; read only the keys you are given)

- `rubric_tree.yaml` - binding classification rules (R0-R10). Read it first.
- `CODER_BRIEF.md` - the record schema and the evidence rules. Your output uses the same schema.
- `packets/<key>.txt` - the work's text, lines prefixed `L<n>: `. The only evidence.
- `cards/<key>.json` - the currently published card (the "old" layers and module ids).
- `out_merged/<key>.json` - the candidate record chosen so far.
- `out/<key>.json` (Codex) and `out_haiku/<key>.json` (Haiku) - both exist when the two models disagreed.

## What to do for each key

1. Read the rubric, the reasons the key was sent to you, the candidate record(s) and the card, then the packet sections
   each disputed item depends on (method and experiments, not only the abstract).
2. Decide every disputed item from the packet and the rubric: each flagged module, each layer move (old card layer ->
   candidate layer), each Codex/Haiku difference that matters (role of work, module split, layer, task family). Apply the
   R3 layer tests literally (TSK, then GTS, then GH) and choose the most specific layer whose condition is met. Fix any
   other error you see in the candidate.
3. Write the adjudicated record to `out_sonnet/<key>.json`: the `final` schema of `CODER_BRIEF.md` (with
   `reconciliation` against `cards/<key>.json`), plus:

```json
"adjudication": {
  "reviewer": "sonnet-5.5",
  "base": "codex | haiku | merged | rewritten",
  "items": [{"item": "what was disputed", "verdict": "accept | reject | modify",
             "result": "the final decision", "reason": "packet-grounded reason", "line": 123}],
  "summary": "two sentences"
}
```

4. Run `python3 check_outputs.py out_sonnet/<key>.json` and fix the record until it prints `OK` (quotes must be
   verbatim from the packet; harness modules need a dimension; GTS needs a function; LLM needs an llm_route).
5. Set `needs_human_review: true` only if the packet cannot decide an item; say why in `notes`.

## Rules

- Write only `out_sonnet/<key>.json` for your keys. Do not modify any other file. No network access.
- Do not read other works' packets, cards or records.
- Fewer, well-evidenced modules are better than many weak ones; keep existing module ids when the mechanism is the same.
- Final message: for each key, one line per disputed item (`item: verdict -> result`), then the check result.
