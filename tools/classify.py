import json, os, numpy as np
from PIL import Image
P=json.load(open('data/urunler_ham.json'))
S='src_img/'
def path(i): return S+(os.path.basename(i)+'.webp' if i.startswith('/assets') else i)
ref=np.array(Image.open(S+'ls-d11n-1.webp').convert('L').resize((1000,1000))).astype(float)
def region(a,box): x0,y0,x1,y1=box; return a[y0:y1,x0:x1]
LOGO=(480,0,1000,135); RIB=(780,780,1000,1000); SW=(0,0,330,230)
res={}
for p in P:
    for i in p['images']:
        if i in res: continue
        f=path(i)
        if not os.path.exists(f): res[i]=('missing',); continue
        im=Image.open(f); w,h=im.size
        a=np.array(im.convert('L').resize((1000,1000))).astype(float)
        sc=[float(np.abs(region(a,b)-region(ref,b)).mean()) for b in (LOGO,RIB,SW)]
        res[i]=(w,h,*[round(s,1) for s in sc])
json.dump(res,open('data/img_class.json','w'))
from collections import Counter
print(Counter((v[0],v[1]) for v in res.values() if len(v)>1).most_common(8))
tm=[k for k,v in res.items() if len(v)>1 and v[2]<12]
print('template-like logo', len(tm), 'of', len(res))
print(sorted(round(v[2]) for v in res.values() if len(v)>1)[::25])
