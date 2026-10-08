# Citation review (read-only)

审查对象：当前 `main.tex`、`TS_AGENT_HARNESS_SURVEY.bib` 及已有审计报告。本文档只记录问题，不修改正文或 Bib。

## 已确认的结构性结果

- `main.tex` 当前引用 161 个 Bib key，314 次引用；已有 deterministic audit 表明 161/161 key 可解析，Bib 中无未使用条目。
- 160 个条目通过官方 DOI/arXiv identity match，`chen2025trace` 仍需核对 online-first 与 issue year。
- 本地 PDF 状态：157 present，4 个缺失或待合法获取：`aminikhanghahi2017changepoint`、`promptstoagents2026`、`agentcybernetics2026`、`prophets2026`。
-  claim-level evidence 只有 13 张 card 标为 full-text verified，125 张仍是 survey-coded；因此这些 card 可用于 corpus 组织，但不应在正文中写成逐篇全文核验后的事实。
- Scholar receipts 仍有 135 pending、5 review、21 verified。Scholar 未验证本身不等于幻觉，但不能写成 “Google Scholar verified”。

## 需优先修正或复核的引用/表述

1. **Figure 1 的 GH/GTS 统计口径与当前 deepest-layer 规则冲突。** `main.tex:196` 写明 “GH and GTS overlap when the same capability is recorded at both ... layers”。用户当前确认的规则是按模块粒度保留最细适用层级，已归入 TSK 的模块不再占 GTS/GH；若该规则继续使用，Figure 1 caption 和生成脚本应改为 mutually exclusive deepest applicable module counts，或明确这是另一种 inclusive secondary-label 统计。当前二者不能同时作为唯一口径。

2. **Appendix caption 也保留了跨层重复的表述。** `main.tex:1223` 写 “one work may contribute modules at more than one level”。这句话只有在“module-level multi-label、每个模块单独取最深层”语义下成立；若读者按同一模块跨 GH/GTS/TSK 重复理解，会与 Figure 1 和分类规则混淆。建议在 caption 中明确 “different modules of one work may occupy different levels; the same module is plotted only at its deepest applicable level”。

3. **Figure 2/3 是本综述自行重绘的框架图，不能把图中所有框当成外部文献事实。** 当前 Figure 2 caption (`main.tex:265`) 只说明组织结构和 ledger evidence，属于作者设计，未标外部来源，结构上可接受；Figure 3 (`main.tex:274`) 同样是 framework claim。若图中保留具体外部系统名称或外部机制标签，应在对应节点旁加原始工作引用，而不是仅靠总 caption。

4. **ChatTS 图的来源写法是充分的，但需确保原文图号准确。** `main.tex:379` 明确写 “adapted from the ChatTS training pipeline in Fig. 3” 并引用 `chatts2025`；`main.tex:343` 也单独引用。建议最后一次 PDF 逐字核对 ChatTS 原文图号及 pipeline 名称，避免图号错配。

5. **支持图的 source caption 普遍具备引用。** 已看到 TS-Agent、AION、TimeClaw、AnomaMind、MERIT 等 source/adapted captions；这些图的正文段落也有对应引用。若图是“adapted/redrawn”，应保留原始图号（当前多数已保留），并避免使用“source”描述完全自行绘制的综合图。

6. **General Harness 七维度是作者归一化层，引用方式基本正确。** `main.tex:399,405,407` 同时引用 Harness/agent surveys，并明确 “author-normalized comparison layer”。这能支持“文献共性抽象”，但不能写成任何单篇综述原样采用了七维度；正文应保留 synthesized/author-normalized 这类措辞。

7. **Section 4/5 中若把单篇工作作为机制定义，应把引用紧贴工作名。** 当前如 `TS-Agent ... \\citep{tsagent2025}`、`TimeART ... \\citep{timeart2026}` 的形式是合适的；需要继续避免把多个工作堆在一句末尾后再给一个无法对应的总引用。

8. **缺失 PDF 的方法性强 claim 应降为 identity-level 或 survey-coded。** 尤其 `promptstoagents2026` 同时用于 related-survey scope 与 Figure 2/Section 1 叙述；在 PDF 补齐前可保留其 bibliographic/abstract-level组织信息，但不应声称已完成全文逐段核验。`agentcybernetics2026` 用于 General Harness 动机，同理应以综述/摘要层证据表述。

9. **`prophets2026` 在当前片段中未见正文引用位置，需确认它是否仍在 Bib/附录中。** 审计将其列为缺失 PDF；若它只用于附录 ledger，保留即可并标 pending；若正文没有引用，应考虑从 production Bib 移到候选清单，避免缺失材料影响审计指标。

10. **ModernTSF 是仓库型基础设施引用。** `main.tex:1136` 通过 footnote 给出 GitHub URL，适合 repository-only claim；不要把仓库地址误写成论文出版信息，也不要补造 Bib 条目。

## 当前未发现的直接幻觉证据

- 没有发现未解析 citation key、重复 arXiv identity、缩写作者列表或“引用不存在”的确定性证据。
- 现有 audit 也没有把任何 production citation 判定为 fabricated identity。
- 仍不能据此宣称全部 161 篇都已全文核验：125 个 card 尚未达到 `paper_verified`，4 个 PDF 缺失，5 个 Scholar receipt 有作者或年份 mismatch。

## 建议的下一步顺序

1. 先统一 Figure 1 与 Appendix 的 inclusive/deepest-layer 统计口径，并重新生成图及 caption。
2. 补齐四个缺失 PDF，优先 `promptstoagents2026`、`agentcybernetics2026`，然后复核其正文 claim。
3. 对 Section 4–6 每个方法段落做“方法名—紧邻引用—原文证据”三项检查；没有全文证据的条目保留较窄的描述。
4. 最后重新编译 PDF，再运行已有 `full_citation_audit.py` 与 figure/table audit。
