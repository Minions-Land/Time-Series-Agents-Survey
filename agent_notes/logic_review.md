# Logic review: construction spine and section organization

**Scope.** Read-only review of `main.tex` and the current module ledger. No manuscript files were modified.

## Overall assessment

The manuscript now has a coherent construction spine: scenario and task contract → LLM-side capability → General Harness → temporal Harness semantics → task-specific contract → benchmark/infrastructure → open problems. This is substantially closer to a tutorial for designing a Time-Series Agent than to a paper-by-paper catalogue. The strongest evidence is the explicit workflow in the Introduction (lines 153–159), the five-step construction sequence in Section 2 (lines 293–303), and the evaluation vector that mirrors the hierarchy (lines 933–949).

The remaining logical risk is that the manuscript uses two different coding views without always naming the switch: an **inclusive hierarchy** for explaining how a system is built, and an **exclusive deepest-module view** for counting contributions. Both are defensible, but the distinction must be stated once, early, and then used consistently. At present, the Introduction says that GH contains GTS and GTS contains TSK (lines 181–187), while the appendix later introduces the deepest-layer rule (line 1168 onward). Without an early rule, readers may interpret the cumulative curves and Paper Cards as paper-level or multiply counted layer assignments.

## Section-by-section findings

### 1. Introduction

The opening answers the right practical question and correctly connects prediction to downstream decision (lines 153–159). The construction recipe is clear and should remain the Introduction's organizing claim.

The formula box is useful, but it appears before Section 2 and is repeated conceptually in Section 2. Keep the formula in the Introduction as the thesis statement, then let Section 2 define its terms and the state transition. The Introduction should avoid re-explaining every temporal obligation immediately afterward; the current paragraph at lines 181–187 can be shortened to the three boundary rules: LLM-side contribution; GH if domain-independent; GTS/TSK if temporal, with TSK taking precedence for exclusive counting.

The related-survey comparison is aligned with the manuscript's purpose: it asks what each survey organizes and what question that organization answers. The table currently uses broad columns (`Model`, `Tasks`, `Reasoning`, `Lifecycle`, `Coverage`, `Evaluation`, `Deployment`). These dimensions are readable, but the prose should explicitly say that they are comparison dimensions for surveys, not the Paper Card taxonomy for reviewed works. Otherwise the table can be mistaken for a second classification system.

The contribution list is strong (lines 250–257), especially the Paper Card and evaluation-path items. The claim should be phrased as a reusable coordinate system, supported by the ledger, rather than as an absolute “last survey” claim. The current evidence supports extensibility and coverage; it does not by itself prove that future surveys can only be increments.

### 2. What Is a Time-Series Agent?

This section has the correct job: define the object, specify the runtime transition, and give the construction procedure. The five steps (scenario, contract, runtime, temporal semantics, evaluation) are the most useful part of the paper for practitioners.

The state transition equation at lines 285–291 is appropriate here. It makes clear that the Harness is the transition mechanism and that temporal modules add typed temporal state/action/observation semantics. The notation table is also well placed because later method equations use the same symbols.

One terminology issue needs attention: the paragraph at lines 281–283 says “Time-Series Harness Module preserves temporal state, operations, context, and validation,” while the next paragraph treats GTS and TSK as its two levels. Use this exact relation consistently throughout: `Time-Series Harness Module` is the umbrella; `General Time-Series Harness` and `Task-Specific Harness` are nested levels inside it.

### 3. LLM-Side Contributions

Making LLM-side work a standalone section is logically correct and preserves the independent branch of the hierarchy. The section distinguishes learned temporal representation/alignment/reasoning from runtime mechanisms (lines 334–336, 372–374). ChatTS is therefore placed in the right conceptual location.

The main check needed here is attribution granularity. A method paragraph should name the concrete method before its citation and state which model capability changes. The current text generally does this well (Time-LLM, LLM4TS, ChatTS). Keep the equation adjacent to the method it formalizes; do not add section-level equations that are disconnected from a specific method.

### 4. General Harness

The chapter correctly treats GH as the reusable runtime and uses the seven dimensions as a common comparison vocabulary (lines 394–405). The table and figure are useful if they are read as co-occurring mechanism families, not mutually exclusive agent types (lines 405–437).

The chapter's subsection pattern is logically sound: define the general runtime mechanism, then show how a Time-Series Agent instantiates it. The temporal details should remain deferred to Section 5. This prevents GH from absorbing temporal semantics too early.

A recurring sentence pattern should be watched: “X is a GH contribution; temporal semantics belong to GTS.” This boundary is useful, but it should be stated once at the beginning of the chapter and then used only when a paper genuinely has a mixed contribution. Repeating it after every method risks making the chapter defensive and mechanical.

### 5. General Time-Series Harness

This is the key conceptual chapter. The criterion at lines 617–622 is strong: GTS is defined by temporal semantics that remain meaningful when the downstream task changes. The availability-set equation (lines 625–629) gives the criterion a formal anchor.

The seven-subsection mapping is defensible because GTS is a specialization of the same GH dimensions. Each subsection should answer two questions in this order: (1) what temporal object or obligation is added, and (2) why it survives a task change. A paragraph that only names a temporal feature belongs in the method description or Paper Card, not in the GTS definition.

The AION example and the GTS landscape figure provide a useful bridge to Section 6. Keep the cross-task test explicit: if changing the task contract requires rewriting the temporal mechanism, the module belongs in TSK; if the temporal state or operation survives, it belongs in GTS.

### 6. Task-Specific Time-Series Harness

The chapter is correctly organized by four task families (lines 798–815). The seven-module lens is reused within each family, which makes task-specific specialization comparable without turning tasks into the top-level taxonomy.

The important distinction is that the four task families define output contracts, not four exclusive paper classes. The forecasting equation at lines 803–808 is a good model: it exposes the contract and its information boundary. Each of the other three task subsections should similarly state the output object, temporal constraints, and verification target before listing representative methods.

### 7. Infrastructure and Benchmarks

This chapter supports the construction goal rather than serving as a bibliography of benchmark names. The three evaluation levels and the episode record (lines 924–949) align with the hierarchy and should remain the chapter's central structure.

The current benchmark table is useful because it maps resources to evidence they can establish. The surrounding paragraphs correctly explain the complementarity of forecasting, trace, diagnosis, QA, executable-artifact, and data-quality resources. The benchmark-selection equation at lines 1037–1045 turns the chapter into a practical design guide.

One consistency point: the coverage vector uses `GH`, `GTS`, `TSK`, and `resource` as coordinates. The first three are construction layers, while `resource` is a behavior category. Rename the fourth coordinate conceptually to `cost/failure` or state that it is a cross-cutting evaluation axis. Otherwise the vector appears to mix ontology levels.

### 8. Open Problems and Focused System Analyses

The open-problem section is correctly derived from missing or weakly evidenced Paper Card fields (lines 1065 onward). This makes open problems a consequence of the framework rather than a generic list of future work. The focused cases then demonstrate how the framework reads concrete systems: ChatTS for LLM-side change, TimeClaw for executable temporal semantics, and ModernTSF for infrastructure/reproducibility.

The section should keep each case tied to one construction question: what layer changed, what evidence supports the claim, and what evaluation obligation remains. This avoids turning the cases into mini related-work summaries.

### 9. Conclusion and appendix

The conclusion is concise and returns to the construction and evaluation paths (lines 1142–1146). The reference placement and clear pages are implemented correctly in the current source (lines 1147–1153).

The appendix is the right location for the full Paper Card ledger. Its description makes the database contribution explicit and records bibliographic identity, claim, source locator, modules, task contract, evaluation evidence, and review status (lines 1154–1168). The appendix should be treated as the auditable data layer; the main text should show only selected human-readable cards and aggregate results.

## Priority fixes for the next manuscript pass

1. **State the two coding views early.** Add one compact sentence in the Introduction or Section 2: the hierarchy is inclusive for explaining construction, while aggregate plots use the deepest applicable module for each concrete contribution. This resolves the GH/GTS/TSK overlap ambiguity before the timeline and Paper Card discussion.
2. **Use one hierarchy sentence everywhere.** Keep `LLM` as the independent branch; `General Harness` contains reusable runtime mechanisms; `Time-Series Harness Module` contains GTS and TSK; TSK is the most specific temporal level. Avoid alternating between “General Harness contains GTS” and “Time-Series Agent has three layers” without clarifying that one is a nested view.
3. **Keep the four task families as instantiation contracts.** They should never read as four top-level categories competing with the Harness hierarchy. The current Section 6 opening mostly achieves this; repeat the contract language in each subsection.
4. **Make every benchmark claim answer an evaluation question.** For each resource, state which layer or evidence it measures and which layer it leaves unmeasured. The current table supports this; the prose should preserve that mapping.
5. **Align ledger statistics with the exclusive rule.** The JSON has both per-layer fields and `primary_locus`; aggregate scripts and figure captions should clearly indicate whether a count is inclusive evidence or exclusive deepest-module contribution.
6. **Reduce repeated boundary disclaimers.** Define the boundary once per chapter, then let concrete method descriptions carry the evidence. This will make the prose more direct and reduce defensive phrasing.

## Verdict

The current section organization supports the intended survey: it teaches readers how to assemble a Time-Series Agent and how to choose an evaluation stack. The core structure is sound. The main unresolved issue is representational consistency between the inclusive construction hierarchy and exclusive module-level statistics; making that rule explicit near the first formula will prevent confusion in the figures, tables, and Paper Card appendix.
