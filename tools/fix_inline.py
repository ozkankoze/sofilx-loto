import sys,json,os,re; sys.argv=['x']
exec(open('/home/claude/sofilx/tools/fix_sets.py').read().split("if __name__")[0])
import pytesseract
H=json.load(open(ROOT+'data/text_hits.json')); L=json.load(open(ROOT+'data/convert_log.json'))
def find_words(img):
    big=img.convert('L').resize((img.width*2,img.height*2))
    out=[]
    for cfg in ('--psm 11','--psm 6','--psm 12'):
        d=pytesseract.image_to_data(big,config=cfg,output_type=pytesseract.Output.DICT)
        for k,w in enumerate(d['text']):
            if re.match(r'^[\(\[|_‘/]?[Ll][Ss5][-–]',w.strip()):
                b=(d['left'][k]//2,d['top'][k]//2,(d['left'][k]+d['width'][k])//2,(d['top'][k]+d['height'][k])//2)
                if b[0]+b[1]+b[2]+b[3]>2*1700: continue
                if not any(abs(b[0]-o[0])<10 and abs(b[1]-o[1])<10 for o in out): out.append(b)
    return out
rep={}
EXTRA={'9b17c1b1':[(430,800,580,858)],'00568eba':[(676,874,800,915),(158,234,232,256)]}
ITAL=['9b17c1b1','00568eba','a147560b']
for i in H:
    out=L[i]['out']; img=Image.open(ROOT+'data/bak_inline/'+os.path.basename(out)).convert('RGBA'); res=[]
    ital=0.22 if any(x in out for x in ITAL) else 0.0
    words=[(w[1],w[2],w[1]+w[3],w[2]+w[4]) for w in H[i]]
    for b in find_words(img):
        if not any(min(b[2],o[2])-max(b[0],o[0])>0 and min(b[3],o[3])-max(b[1],o[1])>0 for o in words): words.append(b)
    for k2,bx in EXTRA.items():
        if k2 in out: words+=bx
    for b in words:
        box=(max(0,b[0]-6),max(0,b[1]-6),b[2]+6,b[3]+6)
        try: res.append((box,replace_ls(img,box,italic=ital)))
        except Exception as e: res.append((box,'ERR '+repr(e)))
    img.convert('RGB').save(out); rep[out]=res
for k,v in rep.items(): print(k,[ (b, r if isinstance(r,str) else r['font']) for b,r in v])
