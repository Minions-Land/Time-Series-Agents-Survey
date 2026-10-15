# 可编辑综述图件（2026-10-15）

此目录保存参考图的组件化版本与本综述现有图的分组副本。原始桌面文件保留不变。

## 文件

| 文件 | 内容 | 本次处理 |
|---|---|---|
| `editable_ppt/01_TimeSeries_Overview_grouped.pptx` | 桌面的 Time-Series Agent 总览 | 保留全部 206 个原生对象、16 个独立图片对象，增加 25 个组合。 |
| `editable_ppt/02_TimeSeries_Research_Landscape_grouped.pptx` | 桌面的研究版图 | 保留全部 241 个原生对象、11 个独立图片对象，增加 15 个组合。 |
| `editable_ppt/03_RSI_Research_Routes_template_grouped.pptx` | 用户新发的 RSI Figure 4 | 按原图位置拆成 141 个原生文字/形状对象、53 个独立图标实例，52 个组合；去掉下方论文 caption。 |

对应 PDF 位于 `edited_previews/`。RSI 图保留参考论文内容，尚未替换为时序论文。前两份是现有时序图的组件管理副本，本次未重新审核其中每篇工作的分类。

## 编辑方式

首先取消最外层组合，再选择局部组合继续取消组合。方法标签的边框、名称和 logo 可以分别选中；时间路线是连续原生路径，可以单独修改颜色和粗细。文字可直接修改。

小 logo 和桌面图的部分插图是独立位图对象，图内笔画不属于原生矢量。RSI 图的少量 logo 细节与原图有差异，手绘边框规整化；这不是像素级一比一复刻。没有整图截图充当可编辑图。

## 验证

- 两份桌面图分组前后，经 LibreOffice 导出的图像逐像素一致。
- 总览图已在 Microsoft PowerPoint 打开，实际执行“取消组合”，观察到“组合/重新组合”菜单可用，并撤销测试操作恢复组合。
- RSI 图通过 editppt 的 manifest、文字覆盖、资产和关系结构校验，已检查 PDF 渲染。GUI 验证状态单独记录，不将结构校验冒充 PowerPoint 操作验证。
- 源文件与可编辑副本分开；后续改写基于副本。正文仅引用最终导出的 PDF/SVG，caption 写在 LaTeX。
- 数量统计图保留 Python 数据绘图流程。

## 参考资料与用途

| 资料 | 本次已核对的图 | 适合借鉴的位置 |
|---|---|---|
| Recursive Self-Improvement in AI: A Survey | 网页 Figure 1–4 说明、用户提供的 Figure 4 图像 | 总览的机制层次、研究版图和发展路线 |
| Co-Evolution in Agentic Systems: Toward Self-Directed Evolution Beyond Human Design (2608.10299) | 第 1 页 Figure 1、第 2 页 Figure 2 | 概念比较、逐层展开的总览 |
| Graph Engineering in the Era of LLM Agents: From Individual Intelligence to System Intelligence (2608.21156) | PDF 标题及第 4 页 Figure 1、第 7 页 Figure 2、第 8 页 Figure 3 的文字说明 | 模型侧、运行机制与系统能力的连接；视觉细节待进一步逐图检查 |
| Graphs Meet AI Agents: Taxonomy, Progress, and Future Opportunities (2506.18019) | 第 2 页 Figure 1、第 5 页 Figure 3 | 总览中的具体机制、章节内的方法对照 |
| Self-Improvements in Modern Agentic Systems: A Survey (2607.13104) | 第 1 页 Figure 1 | 模型侧与系统侧并列结构 |
| OpenReview IUltZSgLMm | PDF 返回 HTTP 403，网页未取得正文 | 暂不作为已核验的绘图来源 |

四份 arXiv PDF 已下载到本目录 `reference_papers/`，仅供本地参考。Preprints 下载接口返回 403，但网页及用户图像可用。其他参考论文尚未逐图转成 PPT。

## 后续改写规则

每幅图先记录目标章节、读者问题、原图图号、原文依据、可编辑组件清单，再复制模板改写。机构 logo 采用对应论文真实机构来源；不能沿用参考图的机构标志指代另一篇工作。方法名、年份、模块归属从 Paper Card 对照原文核验后填写。发展路线表示研究方向，不能无证据地画成技术继承。
