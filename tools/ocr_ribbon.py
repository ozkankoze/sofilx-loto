import json, os, re, numpy as np, pytesseract
from PIL import Image, ImageOps
res=json.load(open('data/img_class.json'))
def p(i): return 'src_img/'+(os.path.basename(i)+'.webp' if i.startswith('/assets') else i)
def ocr(i):
    im=Image.open(p(i)).convert('RGB').resize((1000,1000))
    c=im.crop((760,760,1000,1000)).rotate(-45,resample=Image.BICUBIC,expand=True,fillcolor=(255,255,255))
    a=np.array(c).astype(int); white=(a.min(-1)>200)
    red=(a[...,0]>150)&(a[...,1]<100)
    # keep only white pixels that lie in rows containing red (the band)
    m=np.zeros_like(white)
    for y in range(red.shape[0]):
        xs=np.where(red[y])[0]
        if len(xs)>20: m[y,xs.min()+3:xs.max()-3]=white[y,xs.min()+3:xs.max()-3]
    ys=np.where(m.any(1))[0]
    if len(ys)==0: return ''
    xs=np.where(m.any(0))[0]
    m=m[max(ys.min()-2,0):ys.max()+3, max(xs.min()-2,0):xs.max()+3]
    m=np.pad(m,20)
    # remove white columns beyond band edges
    t=Image.fromarray(np.where(m,0,255).astype(np.uint8))
    t=t.resize((t.width*2,t.height*2))
    s=pytesseract.image_to_string(t,config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/').strip()
    return s
import sys
ids=[k for k,v in res.items() if len(v)>1 and v[2]<12]
out={}
for n,i in enumerate(ids):
    out[i]=ocr(i)
json.dump(out,open('data/ribbon_ocr.json','w'),indent=0)
P=json.load(open('data/urunler_ham.json'))
ok=bad=0; bads=[]
for pr in P:
    base=pr['ls_code']
    for i in pr['images']:
        if i in out:
            o=out[i]
            if o and (o in base or base.startswith(o)): ok+=1
            else: bad+=1; bads.append((base,o))
print(ok,bad); print(bads[:40])
