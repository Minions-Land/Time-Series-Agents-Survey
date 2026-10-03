# Figure overlay and native-source audit

Date: 2026-10-03

The audit compares each active PNG with the decoded pixel output produced by its native PowerPoint source. PNG metadata is ignored. It also checks that the active PNG is referenced by `main.tex` and counts native PowerPoint shape, connector, picture, and graphic-frame objects in the source package.

| Figure | Export preview | Active PNG | Pixel result | Size | Native objects | LaTeX reference |
|---|---|---|---:|---:|---:|---|
| Figure 1 | `.ppt-build/figure1-active/figure1-timeline.png` | `artifacts/active/Figure1_module_timeline_native.png` | exact | (1600, 900) | 252 | yes |
| Figure 2 | `.ppt-build/figure2-active/figure2-organization.png` | `artifacts/active/Figure2_organization_native_v2.png` | exact | (1600, 900) | 74 | yes |
| Figure 3 | `.ppt-build/figure3-active/figure3-construction.png` | `artifacts/active/Figure3_construction_native.png` | exact | (1600, 900) | 26 | yes |
| Figure 4 | `.ppt-build/figure4-active/figure4-general-harness.png` | `artifacts/active/Figure4_general_harness_native_v2.png` | exact | (1600, 900) | 35 | yes |
| Figure 5 | `.ppt-build/figure5-active/figure5-general-ts-harness.png` | `artifacts/active/Figure5_general_ts_harness_native.png` | exact | (1600, 900) | 48 | yes |
| Figure 6 | `.ppt-build/figure6-active/figure6-task-specific.png` | `artifacts/active/Figure6_task_specific_native_v2.png` | exact | (1600, 900) | 78 | yes |
| Figure 7 | `.ppt-build/figure7-active/figure7-infrastructure.png` | `artifacts/active/Figure7_infrastructure_native.png` | exact | (1600, 900) | 65 | yes |
| Figure 8 | `.ppt-build/figure8-active/figure8-open-problems.png` | `artifacts/active/Figure8_open_problems_native.png` | exact | (1600, 900) | 56 | yes |
| LLM-side | `.ppt-build/figure-llm-active/figure-llm-side.png` | `artifacts/active/Figure_LLM_side_native_v3.png` | exact | (1600, 900) | 25 | yes |
| Supporting: AION | `.ppt-build/redrawn-2.png` | `artifacts/active/Figure_support_aion.png` | exact | (2560, 1440) | 165 | yes |
| Supporting: MERIT | `.ppt-build/redrawn-3.png` | `artifacts/active/Figure_support_merit.png` | exact | (2560, 1440) | 165 | yes |
| Supporting: AnomaMind | `.ppt-build/redrawn-4.png` | `artifacts/active/Figure_support_anomamind.png` | exact | (2560, 1440) | 165 | yes |
| Supporting: TS-Agent | `.ppt-build/redrawn-7.png` | `artifacts/active/Figure_support_tsagent.png` | exact | (2560, 1440) | 165 | yes |

Overall status: **pass**.

All current pairs are expected to report `exact`; this is the source-to-PNG gate before a figure is used in LaTeX. The PowerPoint Group -> Ungroup -> single-component edit test is recorded separately in `artifacts/VISUAL_QA_20261002.md`.
