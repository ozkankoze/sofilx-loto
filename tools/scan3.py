import json,os,re,pytesseract,sys
from PIL import Image, ImageOps
from concurrent.futures import ProcessPoolExecutor
L=json.load(open('data/convert_log.json'))
files=[v['out'] for v in L.values()]+['out_eksik/'+f for f in os.listdir('out_eksik')]
PAT=re.compile(r'(^|[^A-Z0-9])[L1I][S5$]\s?[-–_~]\s?[A-Z0-9]|L[O0]CKS[A4]N',re.I)
def scan(f):
    im=Image.open(f).convert('L'); hits=[]
    for sc,inv in ((2,False),(2,True)):
        big=im.resize((im.width*sc,im.height*sc)); 
        if inv: big=ImageOps.invert(big)
        d=pytesseract.image_to_data(big,config='--psm 11',output_type=pytesseract.Output.DICT)
        for k,w in enumerate(d['text']):
            w=w.strip()
            if not w or not PAT.search(w): continue
            x,y,ww,hh=d['left'][k]//sc,d['top'][k]//sc,d['width'][k]//sc,d['height'][k]//sc
            if x+y+ww+hh>1720 or (y<150 and x>480): continue
            hits.append((w,x,y,ww,hh))
    return f,hits
with ProcessPoolExecutor(4) as ex:
    res={f:h for f,h in ex.map(scan,files) if h}
json.dump(res,open('data/scan3.json','w'),indent=0,ensure_ascii=False); print('DONE',len(res))
