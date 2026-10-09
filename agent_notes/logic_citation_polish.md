# `main.tex` 前置逻辑与引用审查

审查范围：Introduction、What Is a Time-Series Agent、LLM-Side、General Harness、General Time-Series Harness、Task-Specific Harness 的定义与方法段落；同时对照 `paper_classification_ledger.json`、`references/CLASSIFICATION_LEDGER.md`、既有 citation audit。本文档只记录问题和修正建议，不修改正文。

## 总结判断

主线已经成立：场景与任务契约 → LLM-side 能力 → General Harness → 时间序列语义 → 任务契约 → 评测与基础设施。最需要优先处理的是两个统计/分类口径没有在正文一开始说清楚，以及摘要中的 corpus 数量与附录数据库不一致。引用 key 本身目前没有发现确定性的虚构身份，但不少 Paper Card 仍是 `survey_coded`，不能把它们写成已经逐篇全文核验的证据。

## P0：必须先修正

### 1. 摘要的记录数与 Paper Card 数据库不一致

- `main.tex:144` 写的是 “We review **130** in-scope records”。
- 当前 `paper_classification_ledger.json` 有 **138** 条记录；正文附录 `main.tex:1207` 也写明 138 Paper Cards，其中 136 条 production-Bib、2 条 repository-only。
- 现有 module timeline 和分类审计也按 138 条 Paper Card 生成。摘要的 130 没有给出排除规则，读者会把它理解成数据库数量。

建议统一为当前可复核的 138，或明确 130 是某个经过筛选的子集并给出筛选条件。不能同时保留 130 与 138 而不解释。

### 2. inclusive hierarchy 与 deepest-only 统计口径冲突

正文前段（`main.tex:181--187`）把关系写成 LLM 独立、GH 包含 GTS、GTS 包含 TSK；这是适合解释系统如何构建的 **inclusive hierarchy**。但 `main.tex:196` 又写：

> “GH and GTS overlap when the same capability is recorded at both ... layers”

这与 Paper Card schema 和分类审计中的 deepest-layer 规则不一致：同一个细粒度模块若已经是 TSK，就不应再被 GTS/GH 的独占统计重复计数；不同模块可以分别落在不同层级。

建议在第一次公式之后加入一条固定规则，并在 Figure 1、Figure 3、附录 caption 中复用：

> The hierarchy is inclusive when explaining construction. For module-level plots, each fine-grained module is assigned to its deepest applicable layer (TSK over GTS over GH); different modules from one work may occupy different layers, but the same module is counted once.

随后把 Figure 1 caption 改为 deepest-applicable module counts；如果确实要保留 inclusive secondary labels，必须把它明确命名为另一种统计，而不能再称为唯一的 module-level trend。当前图注里的 “hollow markers keep the GH curve visible” 会让读者误以为 GH/GTS 是同一模块的两条统计线。

### 3. TSK 任务列表与全文四任务结构不一致

`main.tex:181` 在 TSK 定义中列出 forecasting、anomaly detection、classification、QA、imputation、benchmark generation 等；`main.tex:801--815` 又明确全文只用四个 task families：forecasting/prediction、augmentation/synthesis、anomaly detection/diagnosis、decision support。

`classification`、`QA`、`imputation` 可以作为具体输出或子任务，`benchmark generation` 甚至是资源构建活动，不能与四个 task families 并列。建议 TSK 定义只写“a concrete task contract”，随后列出全文采用的四个 family；具体子任务放入对应 Paper Card 的 task-contract 字段。还应说明：一个 work 可以有多个 task contracts，但每一个细粒度 TSK module 绑定一个具体 contract。

## P1：分类边界和正文逻辑

### 4. GH/GTS/TSK 的判定标准应该在 Introduction 先出现

`main.tex:183` 已给出 GH “domain-independent”、GTS “reusable across temporal tasks”、TSK “bound to one task contract”，`main.tex:620--629` 又给出了很好的 counterfactual 和 availability-set formalization。但 deepest-only 统计规则直到附录才容易被找到。

建议把三条判定与“两种 coding view”合并成一段，放在 Figure 1 前；Section 4/5 只引用这段规则。这样可以避免读者把 GH/GTS/TSK 理解成 paper-level mutually exclusive classes，也能解释一个 work 的多个模块为什么可以跨层。

### 5. General Harness 章的 corpus 表述过宽

`main.tex:397` 写 “The reviewed Time-Series Agent corpus instantiates this runtime”。数据库中还包括 benchmark、model-side contribution、以及作者没有自称 agent 的记录。更精确的说法应是：in-scope systems instantiate or extend the runtime, while benchmark and model-side records provide evaluation or LLM-side evidence. 这样不会把所有 138 条 Paper Card 都声称成完整 GH 实现。

### 6. GTS 的七维映射要强调“子集”，不能暗示每篇都覆盖七维

`main.tex:620` 说 GTS specializes the seven GH dimensions，这个方向正确；但需要补一句“a work may instantiate any subset of these dimensions”。否则读者会把 Table 1 的七行误读成每篇 GTS 论文都必须有七个 temporal modules。当前 Paper Card schema 允许空数组，正文应与此一致。

### 7. 四个 task families 是 output contracts，不是四种 paper 类别

`main.tex:801` 已经基本写对，但应在每个 task subsection 开头保持同一模式：先给 output object、可用信息边界、时间约束和验证目标，再列举方法。当前 forecasting、augmentation、anomaly、decision support 的公式已经形成这个模板，建议把文字模板也统一，避免任务名变成第二套顶层 ontology。

## P1：引用和公式核验

### 8. Citation identity 没有确定性幻觉，但 evidence coverage 仍不完整

已有 deterministic audit 的结果是：当前正文引用 key 可解析，160 个 identity match；没有发现确定性的 fabricated identity。与此同时，4 个外部引用缺本地 PDF（包括 `promptstoagents2026`、`agentcybernetics2026` 等），Paper Card 中约 125 条仍是 `survey_coded`，不是逐篇全文核验。

因此：

- `main.tex:157,212,246` 可以保留这些 surveys 的标题、范围和摘要级组织信息，但不要把它们写成已经逐段核对过的定义来源。
- `main.tex:397` 对 `agentcybernetics2026` 的系统性动机应维持综述/摘要级措辞，直到 PDF 证据补齐。
- Table 2 的每个 checkmark 当前只有总 citation，没有 source locator；如果要保留“explicit coverage”这个强表述，应给每个 survey 的 section/table/page 证据，或者将列名改成较窄的 “reported coverage”。

### 9. 方法公式要区分“原文公式”和“本综述 formalization”

当前公式旁边的工作名和引用位置整体合理，且 TimeSeriesScientist 的 Curator/Planner、MetaCaster 的 objective/hinge、FinCon 的 decision objective 都能在本地 PDF 找到对应内容。需要在文字上区分两类：

- `eq:agent-loop`、`eq:gh-*`、`eq:gts-*`、`eq:forecast-contract`、`eq:augmentation-contract`、`eq:decision-contract`、`eq:evaluation-vector` 等是本综述的统一 formalization，应写成 “we represent / we write” 或在 caption/正文中标明 “survey abstraction”。
- `eq:timellm-objective`、TimeSeriesScientist 的 Curator/Planner、MetaCaster、AnomaMind、FinCon 等若声称复现原文 objective，应逐一对照 PDF 的 equation number、变量定义和损失形式，并把 citation 紧跟在公式解释后。
- ChatTS 的 value-preserved normalization 由原文明确描述 min--max 与 scale/offset，但 `eq:llm-dialogue-objective` 更像统一的 SFT likelihood 写法；应标为本综述的 training abstraction，除非原文明确给出同一公式。

### 10. 图的外部来源和自绘框架需分开

支持图（TS-Agent、AION、TimeClaw、AnomaMind、MERIT、ChatTS 等）目前大多有原始工作名、图号和 citation，形式正确。Figure 2/3/5/6/7 等是本综述的框架图，caption 说明“specific to this survey”即可；若图中保留外部方法名或机制名，应在节点旁或正文对应工作后加 citation，不能只靠综合图 caption。

## P2：可读性与防御性写作

- Figure 1、Figure 2/3 前后的 “Why this figure matters / How to read ...” 有几处重复 caption 的句子；保留一段真正解释“读图后能得出什么结论”的文字，删除只复述图内标签的短段落。
- “not interchangeable”“rather than a list of methods”等边界句在 Introduction 只保留一次即可。分类规则明确后，Section 4/5 不需要反复防御 GH 与 GTS 的区别。
- `main.tex:305` 的 notation table 很有用，但 Layer 列同时写 GH/GTS/TSK，容易与 deepest-only plot 混淆。可将列名改为 “Applicable layer(s)” 或加一句“notation may be typed at multiple layers; module counts use the deepest rule”。

## 建议的修正顺序

1. 先统一摘要、附录和图表中的 corpus 数量（当前 JSON/附录为 138）。
2. 在第一次公式之后写出 inclusive construction / exclusive deepest-module counting 两种 view，并据此重写 Figure 1 caption 与 timeline 数据说明。
3. 将 TSK 的定义统一为四个 task families + concrete task contract，明确 multi-label work 与 single-contract module 的区别。
4. 给 Table 2 的 checkmark 增加 survey-level source locators，或收窄为已有证据能够支持的 coverage 表述。
5. 给方法公式标注 source formula 或 survey formalization，再做一次 equation-by-equation PDF 对照。
6. 最后删除重复的图注解释和防御性边界句，重新编译并跑 citation/figure audit。

## 当前结论

论文的 construction spine 已经能够支撑“教读者构建并评测自己的 Time-Series Agent”这一主旨。当前最关键的不是重写章节顺序，而是让 138 条 Paper Card、module-level timeline、GH/GTS/TSK 关系和四任务 contracts 使用同一套、可复核的统计语义。身份级引用目前没有确定性幻觉证据，但正文强 claim 的证据状态仍应服从 Paper Card 的 `paper_verified` / `survey_coded` 字段。
