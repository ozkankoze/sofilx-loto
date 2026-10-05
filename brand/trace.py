import numpy as np, potrace
from PIL import Image, ImageFilter
im=Image.open('kaynak-logo.png').convert('RGBA')
bg=Image.new('RGBA',im.size,(0,0,0,255)); bg.alpha_composite(im)
g=bg.convert('L')
S=8
big=g.resize((g.width*S,g.height*S),Image.LANCZOS).filter(ImageFilter.GaussianBlur(S*0.35))
a=np.array(big)>128
# rows for split
rows=np.where(a.any(1))[0]; cols=np.where(a.any(0))[0]
prof=a.any(1); gaps=[]
y=rows[0]
for i in range(rows[0],rows[-1]):
    if not prof[i] and prof[i-1]: start=i
    if prof[i] and not prof[i-1] and i>rows[0]: gaps.append((start,i))
print('bbox',cols[0]/S,rows[0]/S,cols[-1]/S,rows[-1]/S,'gaps',[(x/S,y/S) for x,y in gaps])
def trace(mask):
    bm=potrace.Bitmap(~mask)
    path=bm.trace(turdsize=20,turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,alphamax=1.0,opticurve=True,opttolerance=0.2)
    d=[]
    for c in path:
        s=c.start_point; d.append(f'M{s.x/S:.2f},{s.y/S:.2f}')
        for seg in c.segments:
            if seg.is_corner: d.append(f'L{seg.c.x/S:.2f},{seg.c.y/S:.2f}L{seg.end_point.x/S:.2f},{seg.end_point.y/S:.2f}')
            else: d.append(f'C{seg.c1.x/S:.2f},{seg.c1.y/S:.2f} {seg.c2.x/S:.2f},{seg.c2.y/S:.2f} {seg.end_point.x/S:.2f},{seg.end_point.y/S:.2f}')
        d.append('Z')
    return ''.join(d)
split=gaps[0][0]+ (gaps[0][1]-gaps[0][0])//2
icon=a.copy(); icon[split:]=False
word=a.copy(); word[:split]=False
import json
json.dump(dict(icon=trace(icon),word=trace(word),split=split/S),open('trace.json','w'))
def bb(m):
    r=np.where(m.any(1))[0]; c=np.where(m.any(0))[0]; return [c[0]/S,r[0]/S,(c[-1]+1)/S,(r[-1]+1)/S]
json.dump(dict(icon=bb(icon),word=bb(word)),open('trace_bb.json','w')); print(bb(icon),bb(word))
