# 2026 Agent-survey handoff

这份清单只包含本轮尚未同时取得“全文 PDF + Google Scholar 原始 BibTeX”的综述。Meng et al. 的 Harness 综述已经完成，不需要重复补。

## 你需要为每篇论文补什么

对每一篇：

1. 下载论文 PDF，并按下表的文件名保存。
2. 在 Google Scholar 中复制下表的精确标题（建议加英文双引号）。
3. 打开与题目、作者和年份完全匹配的条目，选择 **Cite → BibTeX**。
4. 将 Scholar 页面导出的原始内容保存为同名 `.bib` 文件。
5. 如果 Scholar 没有精确条目，直接记为 `no_exact_scholar_result`；不要用 Crossref、OpenAlex、出版社 BibTeX 或自己改写的 BibTeX 代替。

建议把所有文件放在一个临时目录后压缩交回，例如：

```text
agent-survey-handoff/
  lumer2026toolselection.pdf
  lumer2026toolselection.bib
  zhang2026generalizability.pdf
  zhang2026generalizability.bib
  ...
```

## 优先级 A：直接支撑 Harness 分类

| 文件名 | 精确题目 | 作者 | DOI / 下载入口 | Scholar 搜索词 | 预期用途 |
|---|---|---|---|---|---|
| `lumer2026toolselection.pdf` / `.bib` | *Tool and Agent Selection for Large Language Model Agents in Production: A Survey* | Elias Lumer, Anmol Gulati, Faheem Nizar, Dzmitry Hedroits, Atharva Mehta, Henry Hwangbo, Vamse Kumar Subbiah, Pradeep Honaganahalli Basavaraju, James A. Burke | [Preprints v2](https://doi.org/10.20944/preprints202512.1050.v2); Scholar 结果曾显示 IEEE Xplore 版本 | `"Tool and Agent Selection for Large Language Model Agents in Production: A Survey"` | Tools and Execution；Memory and Context；Coordination；Evaluation |
| `zhang2026generalizability.pdf` / `.bib` | *Generalizability of Large Language Model-Based Agents: A Comprehensive Survey* | Minxing Zhang, Yi Yang, Roy Xie, Bhuwan Dhingra, Shuyan Zhou, Jian Pei | [ACM DOI](https://doi.org/10.1145/3794858) | `"Generalizability of Large Language Model-Based Agents: A Comprehensive Survey"` | GH/GTS/TSK 复用范围；Generalizable Frameworks vs. Agents；Evaluation |
| `zhu2026llmmas.pdf` / `.bib` | *A Survey on Large Language Model-based Multi-Agent Systems: Paradigms, Applications, and Challenges* | Mingjie Zhu et al. | [TechRxiv v1](https://doi.org/10.36227/techrxiv.177160638.89229642/v1) | `"A Survey on Large Language Model-based Multi-Agent Systems: Paradigms, Applications, and Challenges"` | Structure；Interaction；Evolution；Coordination and Scaling |

## 优先级 B：多智能体与决策支持的交叉依据

| 文件名 | 精确题目 | 作者 | DOI / 下载入口 | Scholar 搜索词 | 预期用途 |
|---|---|---|---|---|---|
| `gong2026mas.pdf` / `.bib` | *A Survey of Large Language Models in Multi-Agent Systems: Advancing Coordination and Intelligence* | Zhongzhi Gong | [DOI](https://doi.org/10.54254/2755-2721/2026.ch34641) | `"A Survey of Large Language Models in Multi-Agent Systems: Advancing Coordination and Intelligence"` | Communication and Interaction；System Architecture and Coordination；Evaluation and Benchmarking；Learning and Evolution |
| `liu2026financialmas.pdf` / `.bib` | *Large language model-based multi-agent systems for financial markets simulation: a survey* | Qin-Yuan Liu, Lihang Yao, Zidong Wang, Yu-Fan Yang, Yifei Tang, Dawei Cheng, Changjun Jiang | [Springer DOI](https://doi.org/10.1007/s11432-026-4986-x) | `"Large language model-based multi-agent systems for financial markets simulation: a survey"` | Decision Support / Trading；领域特定多智能体架构。注意不要把 arXiv:2408.06361 当作同一条出版记录。 |

## 优先级 C：时间序列任务与 LLM 角色

| 文件名 | 精确题目 | 作者 | DOI / 下载入口 | Scholar 搜索词 | 预期用途 |
|---|---|---|---|---|---|
| `yu2026llmts.pdf` / `.bib` | *Large Language Models for Time Series Analysis: Methodologies, Applications, and Emerging Challenges* | Wangzhi Yu, Dawei Cheng, Lizhao Zhu, Changjun Jiang | [TechRxiv v2](https://doi.org/10.36227/techrxiv.176703979.99494698/v2) | `"Large Language Models for Time Series Analysis: Methodologies, Applications, and Emerging Challenges"` | LLM roles：fine-tune-based inference engines；TSA-methods-based enhancers；hybrid collaborators |
| `li2026tsad.pdf` / `.bib` | *A Survey of Large Language Models for Time Series Anomaly Detection: Methods, Challenges, and Future Directions* | Kunqi Li, Thomas Pitts, Bin Liang, Chenya Huang, Yuxi Lu | [SSRN DOI](https://doi.org/10.2139/ssrn.6033215) | `"A Survey of Large Language Models for Time Series Anomaly Detection: Methods, Challenges, and Future Directions"` | Anomaly Detection and Diagnosis 任务分支；不用于定义 General Harness |

## 已完成，不需要补

| 文件名 | 题目 | 状态 |
|---|---|---|
| `meng2026agentharness.pdf` / `.bib` | *Agent Harness for Large Language Model Agents: A Survey* | PDF、Scholar Cite 页面和原始 BibTeX receipt 已保存 |

## 交回后的处理规则

- PDF 与 Scholar Bib 的题目、作者和年份必须能相互对应。
- 只收到 PDF、没有 Scholar Bib：保留为 `pdf_only`，不进入正式 Bib。
- 只收到 Bib、没有 PDF：保留为 `bib_only`，不进行 claim-level 编码。
- Scholar 没有精确条目：记录 `no_exact_scholar_result`，不猜测、不替换版本。
- 全部通过后，才会进入正式 bibliography、notable table 和正文 claim。

