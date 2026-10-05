import json,os,re,pytesseract
from PIL import Image
L=json.load(open('data/convert_log.json'))
hits={}
for n,(i,v) in enumerate(L.items()):
    im=Image.open(v['out']).convert('L')
    d=pytesseract.image_to_data(im,config='--psm 11',output_type=pytesseract.Output.DICT)
    hs=[]
    for k,w in enumerate(d['text']):
        w=w.strip()
        if not w: continue
        x,y,ww,hh=d['left'][k],d['top'][k],d['width'][k],d['height'][k]
        if x+y+ww+hh>1700 or (y<150 and x>480) : continue
        if re.search(r'(^|[^A-Z])LS[-–]|LOCKSAN|LOCKSAN|L[O0]CKSAN',w.upper()):
            hs.append((w,x,y,ww,hh))
    if hs: hits[i]=hs
    if n%100==0: print(n,len(hits),flush=True)
json.dump(hits,open('data/text_hits.json','w'),indent=0)
print('DONE',len(hits))
