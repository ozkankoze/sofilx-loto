import json,os,re,pytesseract
from PIL import Image
L=json.load(open('data/convert_log.json')); H=json.load(open('data/text_hits.json'))
hits={}
for n,(i,v) in enumerate(L.items()):
    if i in H: continue
    im=Image.open(v['out']).convert('L'); big=im.resize((2000,2000))
    hs=[]
    for cfg in ('--psm 11','--psm 6'):
        d=pytesseract.image_to_data(big,config=cfg,output_type=pytesseract.Output.DICT)
        for k,w in enumerate(d['text']):
            x,y,ww,hh=d['left'][k]//2,d['top'][k]//2,d['width'][k]//2,d['height'][k]//2
            if x+y+ww+hh>1700 or (y<150 and x>480) or (x+y<200): continue
            if re.search(r'(^|[^A-Z])[L][S5][-–]|L[O0]CKSAN',w.strip().upper()): hs.append((w,x,y,ww,hh))
    if hs: hits[i]=hs
    if n%50==0: print(n,len(hits),flush=True); json.dump(hits,open('data/text_hits2.json','w'))
json.dump(hits,open('data/text_hits2.json','w')); print('DONE',len(hits))
