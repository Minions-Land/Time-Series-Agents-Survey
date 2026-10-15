from pathlib import Path
import json,csv,shutil,math
import pymupdf as fitz
ROOT=Path('/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey');B=ROOT/'artifacts/figure_collection_20261015';OUT=Path('/Users/mjm/Desktop/Survey Figures/全部图件_单页去重')
r=json.loads((B/'collection_report.json').read_text());pdfdir=OUT/'PDF预览';pdfdir.mkdir(exist_ok=True)
index=fitz.open();rows=[]
for i,item in enumerate(r['kept']):
 p=Path(item['file']);pdf=B/'rendered'/(p.stem+'.pdf');d=fitz.open(pdf);assert len(d)==1,(p,len(d));assert d[0].get_text().strip(),p
 shutil.copy2(pdf,pdfdir/pdf.name)
 if i%8==0:
  pg=index.new_page(width=1000,height=1400);pg.insert_text((25,25),f'Survey figure collection | {i//8+1} / {math.ceil(len(r["kept"])/8)}',fontsize=15)
 x=25+(i%2)*490;y=48+((i%8)//2)*335
 pg.insert_text((x,y+14),p.stem,fontsize=9)
 box=fitz.Rect(x,y+24,x+465,y+315);pg.show_pdf_page(box,d,0,keep_proportion=True)
 rows.append({'PPT':item['relative'],'原生对象':item['native'],'独立图片':item['pictures'],'组合':item['groups'],'页数':1,'原文件':item['source'],'原页码':item['source_slide']})
index.save(OUT/'图件总览.pdf')
for i,pg in enumerate(index):pg.get_pixmap(matrix=fitz.Matrix(.8,.8)).save(B/f'contact_{i+1}.png')
with (OUT/'图件清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (OUT/'未收录问题稿.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['source','slide','reason']);w.writeheader();w.writerows(r['excluded'])
text='''# 综述图件：单页去重收纳

共 44 份 PPT，每份只有 1 张幻灯片。

- 01_时序综述图件：24 张。
- 02_RSI参考模板：6 张。
- 03_历史不同构图：14 张。保留与当前图明显不同的构图，供选择，不代表正文采用版本。
- PDF预览：44 个对应单页 PDF。
- 图件总览.pdf：6 页缩略图目录。
- 图件清单.csv：逐图来源、原始页码、对象和组合数量。
- 来源与去重清单.csv：原有副本、旧版与保留图的对应关系。
- 未收录问题稿.csv：未完成组件化的整图截图、图片切片和纯分组测试文件。

整理规则：同一图的重复副本、带标题/不带标题副本和连续修订稿只保留适用的较新版本；保留不同内容或不同构图的历史图。优先保留无 caption 的组件版。原始文件均保留，没有删除或覆盖。

所有保留 PPT 均通过包结构、单页数量、内部关系及文字/原生对象保留检查；44 份均成功导出为单页 PDF。原有组合保留，无组合的图增加外层组合。小 logo 和部分插图仍为独立图片，其内部笔画不能进一步作为原生形状编辑。

本次只整理和拆页，没有重写图内方法名称、公式、年份、统计或分类；历史图中的内容不能视为本次已重新核验。
'''
(OUT/'README.md').write_text(text);(B/'README.md').write_text(text)
print('Verified 44 one-slide PPTs and 44 one-page PDFs; index',len(index),'pages')
