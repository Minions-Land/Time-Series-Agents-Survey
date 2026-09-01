# Blind component-matrix coding notes (v1)

## Blind conditions

- I coded only from `GTS_COMPONENT_MATRIX_PROTOCOL.md` and `GTS_COMPONENT_MATRIX_BLIND_PACKET_v1.csv`.
- I did not inspect the canonical matrix, any prior cell values or distributions, session logs, or earlier reviews.
- The 84 obligation-component pairs were evaluated independently in packet order. For each pair I wrote a Q1 object judgment, a Q2 local-decision judgment, and a Q3 carrier judgment before deriving `code`.
- I did not target a marginal distribution or agreement rate. The resulting blind counts are: bullet=23, open=55, blank=6.
- `open` requires an explicitly typed obligation-specific object in the rationale. A generic plan, message, trace, file, handoff, discussion, or feedback signal would not qualify.

## Boundary decisions and difficult cells

1. **Tool use was coded bullet across the six obligations.** The packet expressly includes verification tools in this component role. Each bullet therefore names a concrete tool-side predicate and failure event; it is not based on adding an unspecified checker to a generic tool label.
2. **Control and Verification were coded bullet across the six obligations.** Their supplied roles explicitly include constraint enforcement, transition acceptance or rejection, and evaluation against explicit criteria. The rationales still require an obligation-specific object and predicate rather than relying on the component names.
3. **Memory was a close boundary for Temporal causality and Temporal grounding of context.** I coded bullet only in these two cells because time-filtered retrieval is local to maintaining and retrieving memory: a cutoff or validity-window predicate can exclude an item before it is returned. I coded Memory open for the other four obligations because storage alone does not establish schema, tolerance, operation-semantics, or audit criteria.
4. **Execution environment was split rather than coded uniformly.** I used bullet for Temporal causality and Temporal grounding when a sandbox or source snapshot can deny post-boundary data, and for Numerical fidelity when declared dtype/precision/tolerance assertions fail locally. I used open for Time-indexed state integrity, Temporal operation semantics, and Output auditability: files, versions, interpreters, and replay facilities expose the evidence, but they do not by themselves know the intended state schema, distinguish a wrong-but-valid temporal operation, reconstruct a metric, or evaluate conditional calibration.
5. **Planning, Lifecycle, and Multi-agent scaling were coded open only under a strict structured-carrier reading.** Their rows name concrete fields in a workflow step, stage handoff, shared state, or review packet. If those artifacts were merely generic orchestration, generic handoff, or unstructured discussion, the relevant instance would fail Q1 or Q3 and downgrade to blank.
6. **Harness optimization was coded blank across obligations.** Its supplied role is feedback-driven improvement. Without a direct obligation-specific object and a direct store/transport/schedule/expose mechanism, its influence is mediated through changed prompts, policies, memories, interfaces, traces, or skills; the protocol explicitly excludes generic learning effects.
7. **Output uncertainty was treated conditionally.** Every analytical output retains the evidence-chain and reconstructability branch. Calibration appears in bullet criteria only when probability, confidence, coverage, or interval semantics and a reference population are declared; deterministic outputs are not failed solely for lacking calibration.

## Self-check

The published CSV was parsed back with Python's `csv` module and checked for exactly 84 data rows, unique obligation-component keys, 14 rows per obligation, 6 rows per component, the code domain {bullet, open, blank}, and nonempty rationales and Q1-Q3 fields.
