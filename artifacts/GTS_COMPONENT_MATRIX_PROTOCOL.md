# GTS Component Matrix Coding Protocol

**Artifact:** `GTS_COMPONENT_MATRIX_v1.csv`  
**Matrix version:** `GTS-CM-v1.0`  
**Source snapshot:** `main.tex`, using Table `tab:component-vocab`, Table `tab:gts-invariants`, and Table `tab:gts-obligation-protocol`. Stable table labels, rather than mutable line numbers, define provenance.  
**Status:** auditable normative architecture coding, not an empirical prevalence estimate.

## 1. Purpose and coding unit

The matrix crosses six General Time-Series Harness obligations with 14 General Harness components. One CSV data row is one **obligation × component** unit. The component identifies *where* a runtime responsibility lives; the obligation identifies *what* temporal-correctness object or condition must be preserved.

The unit is not a paper, product, implementation, feature count, or assertion that every architecture uses the same locus. A code asks whether the catalogued responsibility can directly handle an obligation-specific object in the stated way. Several components may receive `bullet` for one obligation because prevention and detection are not assumed to have a unique architectural home.

## 2. Fixed component vocabulary

The component names and groups come from `main.tex`:

- **Mechanism:** Planning, Memory, Tool use, Control, Harness optimization.
- **Interface:** Reasoning, Acting, Environment modeling, Execution environment, State artifacts.
- **Operation:** Lifecycle, Verification, Observability, Multi-agent scaling.

Coding must remain within the catalogued responsibility. Imagining an arbitrary checker added to any component is not enough.

## 3. Fixed obligation vocabulary

The first five obligations preserve the paper definitions:

1. Temporal causality.
2. Numerical fidelity.
3. Time-indexed state integrity.
4. Temporal operation semantics.
5. Temporal grounding of context.

The sixth is coded as **Output auditability with conditional uncertainty validation**:

- **Auditability always applies:** an analytical output needs a declared validation route and traceable evidence links; exact reconstruction is required only for deterministic or executable artifacts.
- **Uncertainty validation is conditional:** it applies only if the output asserts probability, confidence, coverage, or interval semantics, and may combine calibration or reliability diagnostics with proper scoring rules. A deterministic point estimate or categorical answer with no uncertainty claim is not penalized for lacking this subtest, although its declared validation route and evidence links must remain auditable.

This prevents calibration from being applied where no probabilistic meaning has been asserted.

## 4. Three-question decision rule

Apply the questions in order for every cell and stop at the first decisive answer.

### Q1 — Obligation-specific object

Within the component's catalogued responsibility, does it directly **consume or produce an obligation-specific object**?

Examples include an allowed-context manifest, a typed numeric value with units, a versioned temporal-state record, a typed operation specification, an interval-grounded context record, or an output/evidence bundle.

- **No:** code `blank`.
- **Yes:** continue to Q2.

A generic trace, file, plan, message, or feedback signal does not pass Q1 unless it contains fields specific to the obligation. A merely possible future specialization is hypothetical and does not pass Q1.

### Q2 — Direct local enforcement or detection

Can the component apply an **explicit local criterion** to prevent, reject, block, fail, quarantine, or detect a violation?

Examples are a cutoff predicate, schema check, numeric tolerance, temporal pre/postcondition, re-execution assertion, grounding-compatibility test, evidence-completeness gate, or applicable calibration test.

- **Yes:** code `bullet`.
- **No:** continue to Q3.

`bullet` does not mean “primary,” “exclusive,” or “unique.” Each bullet row must name the criterion and include a concrete failure or gate example.

### Q3 — Direct support or carrying

Does the component directly **store, transport, schedule, or expose** obligation-specific information for a bullet-coded component to use, while applying no criterion itself?

- **Yes:** code `open`.
- **No:** code `blank`.

An open cell requires a concrete carrying object and mechanism. Generic orchestration, learning, discussion, or an effect mediated entirely through another component is blank.

## 5. Symbols and CSV encoding

| CSV code | Symbol | Operational meaning |
|---|---:|---|
| `bullet` | ● | Direct component-local prevention, rejection, or detection using an explicit criterion. |
| `open` | ○ | Direct store/transport/schedule/expose role for obligation-specific information, without a local criterion. |
| `blank` | — | No qualifying direct relation; the possible effect is generic, hypothetical, or mediated. |

The CSV uses ASCII words rather than glyphs for parser stability.

## 6. N/A and applicability

`N/A` is **not a fourth matrix code** and is not the same as `blank`.

- `blank` means the obligation is architecturally in scope but this component has no qualifying direct role under Q1–Q3.
- Instance-level `N/A` means that row's `applicability_precondition` is false for a particular artifact or run. Exclude that instance from the relevant denominator and document it separately; do not rewrite the architecture cell as blank.
- For obligation six, the declared-validation-route branch remains applicable to all analytical outputs. Only the uncertainty-validation subtest is N/A when the output asserts no probability, confidence, coverage, or interval semantics.

Because v1 is an architecture incidence artifact rather than an artifact-instance scoring sheet, `code` is restricted to `bullet`, `open`, and `blank`.

## 7. Conservative downgrade rule

Ambiguity is coded downward:

1. uncertain `bullet` → `open` when a specific object is clearly carried but no local criterion is established;
2. uncertain `open` → `blank` when the object or mechanism is generic, optional, hypothetical, or mediated;
3. never infer a criterion solely from a component label such as “Control,” “Verification,” or “Observability.”

The `downgrade_or_counterexample` field records the closest boundary condition that would lower or raise each cell.

## 8. Independent recoding and disagreement resolution

A replication coder should:

1. read the component role and obligation definition from `main.tex` independently;
2. apply Q1–Q3 without viewing prior matrix symbols and without treating any earlier 24-cell suggestion as truth;
3. write the object, mechanism, rationale, positive example, downgrade/counterexample, and source basis before comparing codes;
4. compare only after completing all 84 cells;
5. report raw agreement, a chance-corrected statistic for the three nominal codes, and a confusion table;
6. adjudicate disagreements by identifying the first question (Q1, Q2, or Q3) on which the coders differ;
7. preserve original coder artifacts and issue a new version for adjudicated changes rather than silently overwriting v1.

A recoder must not upgrade cells to reproduce an earlier distribution. Agreement is an outcome of protocol reproducibility, not a target.

## 9. Interpretation limits

- **Not empirical prevalence:** a bullet does not claim that surveyed systems implement the mechanism, implement it frequently, or implement it correctly.
- **Not a completeness claim:** the six obligations are recurring cross-task requirements, not an exhaustive theory of temporal correctness.
- **Not a unique architecture:** multiple components may enforce or detect one obligation, and a concrete system may allocate responsibility differently.
- **Not an effectiveness result:** a gate's existence does not establish sensitivity, specificity, robustness, or operational value.
- Open circles may be load-bearing information plumbing; they are not lower-importance components.

## 10. CSV field contract

- `matrix_version`: immutable matrix version.
- `obligation`: one of the six fixed obligations.
- `obligation_type`: semantic family of the obligation.
- `applicability_precondition`: condition under which an artifact-level check is meaningful.
- `component`: one of the 14 fixed components.
- `component_group`: Mechanism, Interface, or Operation.
- `code`: `bullet`, `open`, or `blank` only.
- `invariant_specific_object`: concrete object consumed/produced; required for nonblank cells and empty for blank cells.
- `component_local_mechanism`: concrete enforcement/detection or carrying mechanism; required for nonblank cells and empty for blank cells.
- `rationale`: mandatory component- and obligation-specific justification.
- `positive_example`: concrete qualifying example; bullet rows include failure/gate behavior.
- `downgrade_or_counterexample`: boundary distinguishing adjacent codes.
- `source_basis`: line-anchored component and obligation definitions in `main.tex`.
- `coder_role`: role label for the independent pass.

## 11. Release checks

Parse the CSV with Python's `csv` module and verify:

- exactly 84 data rows (6 × 14), plus one header row;
- exactly 14 rows per obligation;
- exactly 6 rows per component;
- only `bullet`, `open`, and `blank` codes;
- no empty rationale;
- every nonblank row has a nonempty specific object and mechanism;
- blank rows have concrete rationales and empty object/mechanism fields;
- bullet examples describe a rejection, failure, block, flag, or detection event.
