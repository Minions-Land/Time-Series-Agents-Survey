# VibeWriting skill applicability

Reviewed against the current survey repository on 2026-09-08. Skills are
adopted only when their assumptions match this repository and the current work.

| Skill | Decision | Reason |
|---|---|---|
| collaboration-workflow | Conditional | Use only when section ownership or an author review round is being coordinated. |
| conflict-resolver | Conditional | Use only if GitHub and Overleaf produce a real LaTeX merge conflict. |
| figure-workflow | Later | Use when a figure is generated or revised from verified data. |
| final-audit | Later | Run before submission, after the bibliography and manuscript are stable. |
| gemini-figure-craft | Not now | No conceptual-figure generation is part of the reference-management task. |
| github-integration | Use | Git commits and remote synchronization apply; issue and PR machinery is unnecessary for this local batch. |
| latex-compile | Use | A clean `latexmk` build verifies bibliography and cross-reference resolution. |
| material-manager | Adapt | Its provenance principle applies, but its fixed directory tree and SHA-256 manifest conflict with the existing repository and `AGENTS.md`; the Git-tracked reference manifest is used instead. |
| mock-review-workflow | Later | Argument-level review belongs after source verification and prose revision. |
| overleaf-sync | Use | The paper has an existing Overleaf project and must be synchronized without overwriting newer edits. |
| quality-check | Use | Citation existence, metadata completeness, claim support, and unresolved-reference checks apply now. |
| revision-tracker | Later | Activate when an internal or external review round begins. |
| submission-packager | Later | The manuscript is not yet at submission packaging. |
| table-formatter | Later | Use when the taxonomy and competitor tables are revised, especially for vertical page layout. |
| venue-formatter | Later | Apply only after the current IJCAI author kit and page rules are fixed. |
| workspace-setup | Do not apply | This is an established 45-page repository; restructuring it into a new `paper/` tree would create churn and break existing paths. |
| writing-orchestrator | Partial | Its evidence-first and citation-first ordering applies; its new-workspace assumptions and section dispatch are unnecessary here. |

The active sequence for this stage is: reference inventory, official-source
identity checks, lawful PDF acquisition, Google Scholar receipt review, clean
LaTeX compilation, then GitHub and Overleaf synchronization.
