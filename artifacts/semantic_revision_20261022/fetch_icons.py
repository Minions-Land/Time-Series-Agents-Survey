"""Source Lucide SVGs and preserve their paths as editable PPT geometry."""
from pathlib import Path
import concurrent.futures,json,urllib.request,sys,math
from lxml import etree as E
D=Path(__file__).resolve().parent
sys.path.insert(0,str(D/'.build/python_packages'))
from svgpathtools import parse_path,Line,QuadraticBezier,CubicBezier,Arc
names=['list-filter','shuffle','crop','binary','code-xml','flask-conical','file-check-2','square-function','brackets','table-properties','fingerprint','text-search','snowflake','package-check','circle-help','scan-eye','clipboard-list','list-check','circle-check-big','circle-x','warehouse','route','calendar-clock','hourglass','audio-lines','scan','combine','sliders-vertical','milestone','chart-spline','database-zap','zap']
base='https://raw.githubusercontent.com/lucide-icons/lucide/main/'
def get(name):
 real={'file-check-2':'file-check-corner','fingerprint':'fingerprint-pattern','circle-help':'circle-question-mark'}.get(name,name)
 url=base+'icons/'+real+'.svg'
 dest=D/'assets'/f'{name}.svg'
 if not dest.exists():
  try:data=urllib.request.urlopen(url,timeout=30).read()
  except Exception as ex:raise RuntimeError(f'{name}: {ex}') from ex
  dest.write_bytes(data)
 return name,url
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: urls=dict(pool.map(get,names))
(D/'assets/LICENSE-lucide').write_bytes(urllib.request.urlopen(base+'LICENSE',timeout=30).read())
def pt(z): return {'x':round(z.real,5),'y':round(z.imag,5)}
def convert_path(d):
 cmds=[];last=None
 for s in parse_path(d):
  if last is None or abs(s.start-last)>1e-6:cmds.append({'moveTo':pt(s.start)})
  if isinstance(s,Line):cmds.append({'lineTo':pt(s.end)})
  elif isinstance(s,QuadraticBezier):cmds.append({'quadBezTo':dict(x1=s.control.real,y1=s.control.imag,**pt(s.end))})
  elif isinstance(s,CubicBezier):cmds.append({'cubicBezTo':dict(x1=s.control1.real,y1=s.control1.imag,x2=s.control2.real,y2=s.control2.imag,**pt(s.end))})
  elif isinstance(s,Arc):
   for b in s.as_cubic_curves(curves=max(1,math.ceil(abs(s.delta)/60))):cmds.append({'cubicBezTo':dict(x1=b.control1.real,y1=b.control1.imag,x2=b.control2.real,y2=b.control2.imag,**pt(b.end))})
  last=s.end
 return cmds
out={}
for name in names:
 root=E.fromstring((D/'assets'/f'{name}.svg').read_bytes());paths=[]
 for e in root:
  tag=E.QName(e).localname;a=e.attrib;d=None
  if tag=='path':d=a['d']
  elif tag=='line':d=f"M {a['x1']} {a['y1']} L {a['x2']} {a['y2']}"
  elif tag in ['polyline','polygon']:
   nums=a['points'].replace(',',' ').split();d='M '+' '.join(nums[:2])+' L '+' '.join(nums[2:])+(' Z' if tag=='polygon' else '')
  elif tag in ['circle','ellipse']:
   x=float(a['cx']);y=float(a['cy']);rx=float(a.get('r',a.get('rx',0)));ry=float(a.get('r',a.get('ry',0)))
   d=f'M {x-rx} {y} A {rx} {ry} 0 1 0 {x+rx} {y} A {rx} {ry} 0 1 0 {x-rx} {y}'
  elif tag=='rect':
   x=float(a['x']);y=float(a['y']);w=float(a['width']);h=float(a['height']);r=float(a.get('rx',0))
   d=f'M {x+r} {y} L {x+w-r} {y} Q {x+w} {y} {x+w} {y+r} L {x+w} {y+h-r} Q {x+w} {y+h} {x+w-r} {y+h} L {x+r} {y+h} Q {x} {y+h} {x} {y+h-r} L {x} {y+r} Q {x} {y} {x+r} {y} Z'
  if d:paths.append(convert_path(d))
 out[name]={'paths':paths,'url':urls[name]}
(D/'assets/icons.json').write_text(json.dumps(out,indent=2))
print('Sourced',len(out),'Lucide icons as native path definitions')
