from pathlib import Path
import re
p=Path('main.tex');s=p.read_text()
s=s.replace('artifacts/editorial_unified_20261022/pdf/Figure03_Editorial.pdf','artifacts/paper_figures/Overvieww.pdf')
for n in range(4,16):s=s.replace(f'artifacts/editorial_unified_20261022/pdf/Figure{n:02}_Editorial.pdf',f'artifacts/editorial_accent_20261022/pdf/Figure{n:02}_Accent.pdf')
old=r'In Figure~\ref{fig:overview}, the left branch is the independent LLM-side contribution; the nested right branch shows increasing temporal and task specificity. The layers distinguish domain-independent execution, reusable temporal mechanisms, and procedures bound to a task contract. This figure supplies the hierarchy used in the subsequent sections and in the exclusive module-level statistics.'
new=r'Figure~\ref{fig:overview} maps representative LLM-side contributions, Harness mechanisms, and evaluation resources. Read the upper band for model contributions, the middle band for runtime mechanisms and their implementations, and the lower band for evaluation and infrastructure. Section~\ref{sec:general-harness} synthesizes these mechanisms into five runtime functions, with control, verification, and coordination discussed within planning and orchestration. The subsequent temporal and task-specific sections examine how these functions acquire domain and task requirements.'
s=s.replace(old,new)
old=r'Contribution layers in a Time-Series Agent. The LLM side remains independent of the nested Harness stack: General Harness contains reusable runtime mechanisms, General Time-Series Harness contains temporal mechanisms that transfer across tasks, and Task-Specific Harness instantiates a task contract. The evaluation panel connects the hierarchy to benchmark requirements and module-level evidence. Visual styling follows a prior survey \citep{rsi2026survey}.'
new=r'Representative contributions and resources for Time-Series Agents. The upper band covers model-side interfaces and learning; the middle band connects runtime mechanisms to example implementations; the lower band identifies benchmarks and infrastructure. The mechanism labels support the five-function synthesis in Section~\ref{sec:general-harness}. Visual styling follows a prior survey \citep{rsi2026survey}.'
s=s.replace(old,new)
s=s.replace('The schematic series show retrieved examples and generated views.','The schematic series show retrieved examples and generated views; document symbols denote sample records, and checkmarks or crosses show review decisions.')
s=re.sub(r'\\paragraph\*?\{([^{}]*)\}',r'\\noindent\\textbf{\1}',s)
s=s.replace('\n\\textbf{Current ledger snapshot.}', '\n\\noindent\\textbf{Current ledger snapshot.}')
p.write_text(s)
