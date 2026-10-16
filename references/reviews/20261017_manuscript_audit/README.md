# Manuscript method, equation and final-reading audit — 2026-10-17

Baseline: `40062642e809e4a1faa7a5ea64d17502404957c9`.

## Coverage

- All 29 labeled equation environments have audit entries: 9 in Sections 2–5, 17 in Section 6, and 3 in Sections 7–8. Three are survey definitions; the remainder are checked against the relevant original-paper equations, algorithms or method descriptions.
- Sections 2–5: 45 method/source entries. Section 6: all 24 cited methods. Sections 7–8: formula checks and benchmark factual spot checks. Counts overlap across sections and are not a unique-paper total.
- Final reading: 39 section/subsection units and all 21 figure/table captions and body-reference relationships; appendix framing included. Method-level primary-source audit is distinct from a full verification of every bibliography item or experimental reproduction.
- The original before-edit findings are retained in the section reports. The implemented corrections below resolve those findings; baseline line numbers in reports are not current line numbers.

## Implemented corrections

1. TimeCAP: convert the LLM's discrete class to one-hot before mixing with encoder logits.
2. FLAIRR: define a resolved H-step refinement window; clarify when target feedback becomes available.
3. TSci and MetaCaster: distinguish optimization/validation feedback from final evaluation, including independent MetaCaster evaluation datasets.
4. CastFSR, ScenarioDiff, AnomaMind and FinCon: define local quantities, diffusion steps, candidate intervals, prompt parameters and feedback conditions. CoLLMLight's full equation is identified as its complex-coordination mode.
5. AD-Agent: separate the paper's optional evaluation agents from our held-out evaluation recommendation.
6. TimeSage-EV: correct the corpus description to 1,485 scenario-period instances spanning February 2023–May 2026; the 24-instance minimum is per scenario.
7. Time-LLM: define attention dimension. Seven-dimensional organization and GH/GTS boundary are identified as our synthesis with concrete mechanism support. Remove one redundant taxonomy citation whose primary source was unavailable.
8. Condense repeated construction roadmaps, remove unused notation, and focus the final system analyses on design implications. Retain substantive assumptions and evaluation requirements. Move detailed model-side synthesis exposition back to its Section 3 cross-reference.
9. Narrow the comparison-table coding criterion to explicit review organization and record its sources. The From Prompts to Agents organization is verified from the author repository; its full PDF remains unavailable.
10. Correct four figure assets in their native editable PPTs: current section organization, four contribution layers and LLM action selection, AION's nine source-specific descriptions, and task-appropriate symbols/title spacing. Preserve group structures. Regenerate actual manuscript assets and corresponding source copies.
11. Replace vague RSI template attribution with its title/URL bibliography reference and verified screenshot figure numbers for the organization and task layouts. Figure 3 credits styling, not faithful reproduction. Unverified author/DOI fields are omitted.

## Validation

- All 29 baseline equation labels remain and occur in the audit reports.
- 11 existing repository tests pass; `git diff --check` passes.
- LaTeX builds successfully; no undefined citations/references or overfull boxes. Remaining warnings concern existing template column names and repeated hyperref color settings.
- Changed formula pages and all four corrected figures were rendered and inspected. Overview PDF whitespace is cropped at export while the editable source retains its slide canvas.
- Sections 2–5 received an independent post-edit cross-check (`sections_2_5_crosscheck.json`).

The unrelated pre-existing RSI landscape PPT edit is excluded from this revision.
