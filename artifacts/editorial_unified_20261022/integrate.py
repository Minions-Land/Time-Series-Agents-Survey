from pathlib import Path
import re
p=Path('main.tex');s=p.read_text()
s=s.replace('artifacts/active/Figure2_organization_rsi_adapted.pdf','artifacts/editorial_unified_20261022/pdf/Figure01_Editorial.pdf').replace('artifacts/paper_figures/Overvieww.pdf','artifacts/editorial_unified_20261022/pdf/Figure03_Editorial.pdf')
s=re.sub(r'artifacts/signal_revision_20261022/pdf/Figure(\d+)_Signal_grouped.pdf',r'artifacts/editorial_unified_20261022/pdf/Figure\1_Editorial.pdf',s)
p.write_text(s)
