from pathlib import Path
import pymupdf as f
D=Path(__file__).resolve().parent;R=D.parents[1];out=f.open()
for n in [4,7,9]:
 old=f.open(R/f'artifacts/signal_revision_20261022/pdf/Figure{n:02}_Signal_grouped.pdf');new=f.open(D/f'pdf/Figure{n:02}_Editorial_trial.pdf')
 p=out.new_page(width=1640,height=560)
 p.insert_text((28,34),f'Figure {n}: visual style comparison',fontsize=21,fontname='hebo')
 p.insert_text((28,67),'CURRENT  /  Comic Sans, colored headings, shaded signals',fontsize=13,color=(.35,.35,.35))
 p.insert_text((844,67),'TRIAL  /  Arial, black labels, navy + terracotta accents',fontsize=13,color=(.19,.29,.39))
 p.show_pdf_page(f.Rect(20,86,808,480),old,0);p.show_pdf_page(f.Rect(836,86,1624,480),new,0)
 p.insert_text((28,524),'Same content and grouped components. Production manuscript unchanged. Each trial is also supplied as a one-slide editable PPTX.',fontsize=12,color=(.35,.35,.35))
 new[0].get_pixmap().save(D/f'.build/Figure{n:02}_Editorial_trial.png')
out.save(D/'Figures_04_07_09_Style_Comparison.pdf')
for i in range(3):out[i].get_pixmap(matrix=f.Matrix(.8,.8)).save(D/f'.build/comparison{i}.png')
