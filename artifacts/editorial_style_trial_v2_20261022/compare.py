from pathlib import Path
import pymupdf as f
D=Path(__file__).resolve().parent
out=f.open()
for n in [4,7,9]:
 old=f.open(D.parent/f'editorial_style_trial_20261022/pdf/Figure{n:02}_Editorial_trial.pdf')
 new=f.open(D/f'pdf/Figure{n:02}_Editorial_v2.pdf')
 p=out.new_page(width=1640,height=560)
 p.insert_text((28,34),f'Figure {n}: typography and depth refinement',fontsize=21,fontname='hebo')
 p.insert_text((28,67),'V1 / restrained palette, Arial, flat fills',fontsize=13,color=(.35,.35,.35))
 p.insert_text((844,67),'V2 / Comic Sans headings, selective gradients and soft shadows',fontsize=13,color=(.19,.29,.39))
 p.show_pdf_page(f.Rect(20,86,808,480),old,0)
 p.show_pdf_page(f.Rect(836,86,1624,480),new,0)
 p.insert_text((28,524),'Black data signals retained. Same scientific content and grouped components. Production manuscript unchanged.',fontsize=12,color=(.35,.35,.35))
out.save(D/'Figures_04_07_09_V1_vs_V2.pdf')
for i,p in enumerate(out):p.get_pixmap(matrix=f.Matrix(.8,.8)).save(D/f'.build/comparison{i}.png')
