# 第 3–6 章独立对齐审查

审查对象：2026-10-15 工作目录中的 `main.tex`。第 4–5 章正在由主审修订；本报告优先处理第 3、6 章，并只记录第 4–5 章仍值得核对的边界。未修改共享正文。

证据：本轮三个 shard 的逐论文记录，以及对 Time-LLM、ChatTS、Towards Time-Series Reasoning with LLMs、ChatAD、STRIDE、TSOrchestra、MERIT、AnomaMind、CastFSR、FLAIRR-TS、FinCon 等原文方法段的复查。此报告核对写作与来源的一致性，不声称独立复现实验。

## 必须优先修正的事实与定义

### 1. MERIT 的正文与图解互相矛盾

位置：§6.2 图前 `Why the augmentation example matters` 与 `fig:merit-augmentation` caption。

当前前段已准确写出 retrieval → augmentation → review，且区分构造期 review 与下游实验。但图前短段又写成“generation is followed by retrieval, review, and downstream-utility checks”，caption 则称 review 使 downstream utility 成为在线生成契约。

原文：`references/pdfs/merit2025.pdf`，PDF p.3 Fig.2 和 pp.4–5 §§3.2–3.4。检索相邻序列、选择增强策略、review 正样本，合格样本进入 memory bank，拒绝后回到检索。下游表征任务评价是后续实验；没有证据表明 review agent 每次运行下游训练评估。

处理：合并图前短段进方法段，按上述顺序解释图；caption 写清“semantic quality review of positive views for contrastive learning”。以 MetaCaster 展示真正由下游预测误差驱动的生成更新，这样两篇方法形成有内容的比较。

### 2. AnomaMind 被写成了 root-cause diagnosis 系统

位置：§6.3 图前“diagnose a cause”、caption 的“anomaly-diagnosis workflow”和“diagnosis ... distinct TSK modules”。

原文：`references/pdfs/anomamind2026.pdf`，PDF p.5 §IV.C。四阶段为 coarse evidence acquisition、adaptive evidence construction、anomaly detection、iterative refinement。输出为异常区间集合及二元标签，Eq.(6) 为二元区间检测。这里的 diagnostic context 是辅助异常判定的证据，不等于经过评价的根因输出。

处理：正文与 caption 统一回原文四阶段。若要介绍根因诊断，以 LEMAD/SAGE-AD 等确有对应输出的工作另起实质方法段，说明输出对象、证据链和评价；不能把 AnomaMind 图改名后用于证明根因诊断。

### 3. §3.3 的参数相加公式不能代表全部 model-side adaptation

位置：`eq:llm-adaptation`，`theta_adapt = theta_0 + Delta_phi`。

Time-LLM 原文 p.4 明确只更新输入变换及输出投影，LLM 主体冻结；STRIDE pp.5–6 包含独立投影、TSFM 参数以及 LLM LoRA。新接模块不一定与基础模型参数有相同维度，不能统一写为基础参数加一个增量。

处理：删去该泛化公式与重复边界段，将材料按具体学习对象组织。Time-LLM 展示其原文 p.5 Eq.(1) 的 patch-to-text-prototype attention；STRIDE 展示原文 p.6 Eq.(1) 的语言/分位数联合目标；TSOrchestra 展示 judge 的 SFT/GRPO。这样每个公式解释实际创新，而不是为整个 subsection 填公式。

### 4. 预测输入契约与前章可用信息定义冲突

位置：§6 开头 `eq:forecast-contract` 的 `f(y_{<=tau}, x_{<=tau})`。

§5 已用 availability time 定义 I_tau，并明确允许提前公布的未来日历事件。按事件索引写 `x_{<=tau}` 会把这类 known-at-origin future covariates 排除。CastFSR 原文 p.4 正使用 calendar、weather、context 等 horizon-relevant 信息。

处理：统一写 `Yhat_{tau+1:tau+H}=f_theta(I_tau; H)`，正文说明 I_tau 包含已观测目标历史与预测时点已经可得的外生信息。后面的 contextual forecasting 例子沿用同一边界。

## 最有价值的章节逻辑重组

### 5. 第 3 章应按“训练出什么能力、怎么接入 Agent”展开

目前 §3.1 把 Time-LLM、LLM4TS、视觉模型、TSOrchestra、STRIDE 连续列名，但主公式只是 MSE；§3.2 又汇集数据、对话、工具 RL；§3.3 用抽象公式重复分类边界。读者不容易据此选择能力。

建议使用三个连续问题组织原有材料，不增加另一套贡献分类：

1. **Temporal representation and alignment**：Time-LLM、LLM4TS、ChatTS 的输入编码/对齐。讲清输入时间序列如何进入 LLM，哪些参数更新。用 Time-LLM 原文 cross-attention 解释 learned prototypes；MSE 可作为同段末尾的训练目标，不承担创新解释。
2. **Temporal instruction and reasoning**：ChatTS 的合成属性与指令；Towards Time-Series Reasoning with LLMs 的 encoder warm-up → LoRA/CoT；STRIDE 的 reasoning distillation → latent fusion。用两三种实际训练路径比较数据与模型输出。
3. **Learning to operate temporal workflows**：TSOrchestra 的 ensemble judge、CastFSR 的整轨迹策略、ChatAD 的 preference optimization、AnomaMind 的局部 detector。逐个明确被训练的是哪个角色，以及推理时仍由哪些外部工具工作。

这些是叙述次序，不应在 ledger 中新建排他的顶级类别。GH/GTS/TSK 与独立 LLM 维度保持唯一。

TSOrchestra 原文 pp.5–7 明确 SFT + GRPO 训练 Qwen-2.5-3B；当前只把它放在 representation 节、介绍其外部 ensemble 工作流，实际漏掉了它进入本章的主要证据。STRIDE 原文 pp.4–6 的联合训练同样值得一段具体介绍，优先级高于泛泛的参数增量公式。

### 6. 第 6 章后两节仍是“一串方法名 + 一篇展开”

§6.1 和 §6.2 已基本按输出对象及方法选择形成比较。§6.3 开头则一次列出 AnomaMind、ChatAD、SAGE-AD、LEMAD、power-system agent，随后只讲 AnomaMind；§6.4 同样列出 FinCon、TradingAgents、CoLLMLight、ClimateAgent、Smart Energy Agent，随后只讲 FinCon。

建议按构建问题展开每节：

- **异常任务**：先区分异常区间输出与根因/处置输出；AnomaMind 展示证据如何支撑区间判断；一篇服务/电网工作展示 incident evidence 如何形成 diagnosis；最后比较何时需要已训练 detector，何时主要依赖工具与领域记忆。threshold/false-alarm budget/remediation 只有在相应来源确有实现时，才归给具体方法。
- **决策任务**：FinCon 展示风险约束下的头寸；CoLLMLight 或 CuraLight 展示交通状态到相位/时长的控制及仿真反馈；再用一个运维例子连接诊断和建议。比较的是 action、feedback、constraints 如何不同，而不是把所有工作都称作“risk-aware agent”。

每个方法段按“场景需求 → 输入与动作 → 核心机制/原文公式 → 可观察结果 → 适用条件”写。章节内部仍用原七维理解机制，但不需每篇都强行复述全部七个名字。

### 7. 第 5 章后面三个维度还缺独立的具体模块证据

当前 §5.5 主要重述 AION 的 validation checkpoint；§5.6 重述 TIMECLAW generic tool promotion 及“如果生成的是 temporal procedure”；§5.7 引用 AION communication，再说明若 handoff 传递时间语义则属 GTS。

已核验 AION 模块记录仅把 lifecycle/protocols 归 GH，将 temporal input grounding 和 validity checks 归 GTS，没有另外核实一个 temporal coordination protocol。TIMECLAW 的通用抽取/测试/注册过程也属于 GH；必须展示具体生成工具及其时间语义，才能把它当成另一项 GTS 贡献。

处理优先级：先用已有证据加强 §5.1–5.4；§5.5–5.7 若保留，避免把同一 validator 或 memory 重新换标签计为新贡献。可合并成一段解释这些共享 temporal checks 如何贯穿流程，或寻找具有明确时间因果设计的独立例子。TimeSage-EV 的 next-period skill activation 是一个具体可核对候选（shard 1 已附页码），比泛泛 tool promotion 更能解释 temporal evolution。不要为了保持七个标题而声称已有七种独立模块实现。

### 8. 引用位置和管理语言尚未统一

第 3 章以下写法仍将引用放在整句末尾：multimodal systems 后 timevlm/timeomnivl；Conversational Time Series Foundation Models；STRIDE；OpenForecaster 与 AURA-4B 并列后一个 cite；LLMTime 后三篇引用合放。按用户要求，使用准确方法/论文名并紧邻引用，各篇的训练行为分开讲。

第 3 章两处“module ledger records ...”、§6.4 末尾“inclusive evidence fields and exclusive plotting labels”属于维护说明，打断构建逻辑。将数据库字段和计数规则放到附录；正文只需一句解释一个系统可组合多个模块。

`Why the augmentation example matters`、`Reading the General Harness figure` 这种小标题应并入实质正文，以论文阅读说明自然引出图；前者目前又很短，正是用户此前不喜欢的形式。

## 已确认正确、不要无谓重写的部分

- Time-LLM 当前 MSE 公式与原文 p.3 一致；问题是它不充分展示该方法的创新，而非公式造假。
- ChatTS min-max 与 scale/offset 还原是原文 §3.4.2 p.5 的合理数学重述。
- ChatAD TKTO 的 soft preference 与混合损失对应原文 p.5 Eqs.(4)–(5)。可以补一句 S 的组成让读者明白反馈来源。
- CastFSR 的 contextual retrieval、candidate revision、reflection 和 final forecast 对应原文 p.4 Eqs.(5)–(8)。当前没有再把该预测专属流程放到 GTS。
- FLAIRR-TS 当前公式按原文 Algorithm 1 的 prompt/error history 写；源算法本身使用 recent ground truth。正文明确其反馈来自已解决窗口，有助于交代机制。
- AnomaMind 两组公式与原文 pp.5–6 Eqs.(5)–(8) 一致；应纠正的是图与诊断措辞。
- FinCon 当前将 w 解读为 target exposure，hold=0、daily rebalance，符合源文；请勿再改为持仓增量。prompt-controlled policy objective 也不等于 LLM 参数微调。
- TimeCAP 当前归为 event prediction，且将 prompt augmentation 与合成训练数据区分，符合来源。

## 推荐执行顺序

1. 修正 MERIT/AnomaMind 图解事实和 forecast input 契约。
2. 重组第 3 章，取消通用增量公式，展开原文学习机制。
3. 用两到三个互补实例重写 §6.3–6.4；不在已有薄段后继续附加孤立公式。
4. 合并第 5 章证据薄弱、内容重复的维度说明；任何新增 GTS 模块先落到审读记录。
5. 全章统一“方法名紧邻引用”，将 ledger 管理语句移到附录，再核验 figure/caption 是否忠实于所述方法。
