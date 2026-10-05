import sys,json,os,re; sys.argv=['x']
exec(open('/home/claude/sofilx/tools/fix_sets.py').read().split("if __name__")[0])
exec(open('/home/claude/sofilx/tools/convert.py').read().split("def process(")[0].split("FONT=")[0].replace("OVL=overlay_png()",""))
exec('def draw_ribbon'+open('/home/claude/sofilx/tools/convert.py').read().split('def draw_ribbon')[1].split('def process(')[0])
OVL=overlay_png()
COLORS={'RED','YLW','BLUE','GRN','BLK','WHITE','ORJ','PRP'}
def base_code(c):
    return c.replace(' ','')
import pytesseract
N=json.load(open(ROOT+'data/eksik_urunler.json'))
os.makedirs(ROOT+'out_eksik',exist_ok=True)
rep={}
def words(img):
    sc=3 if max(img.size)<900 else 2
    big=img.convert('L').resize((img.width*sc,img.height*sc))
    out=[]
    for cfg in ('--psm 11','--psm 6','--psm 12'):
        d=pytesseract.image_to_data(big,config=cfg,output_type=pytesseract.Output.DICT)
        for k,w in enumerate(d['text']):
            w=w.strip()
            if re.match(r'^[\(\[|_‘/]?[Ll][Ss5][-–]',w) or re.search(r'L[O0]CKSAN',w.upper()):
                b=(d['left'][k]//sc,d['top'][k]//sc,(d['left'][k]+d['width'][k])//sc,(d['top'][k]+d['height'][k])//sc)
                if not any(abs(b[0]-o[1][0])<8 and abs(b[1]-o[1][1])<8 for o in out): out.append((w,b))
    return out
ONLY=os.environ.get('ONLY')
for n in N:
    if ONLY and n['code']!=ONLY: continue
    for k,i in enumerate(n['imgs'],1):
        img=Image.open(ROOT+'src_eksik/'+i).convert('RGBA'); r=[]
        for w,b in words(img):
            if 'CKSAN' in w.upper():
                x0,y0,x1,y1=b; a=np.array(img.convert('RGB'))[max(0,y0-3):y1+3,max(0,x0-3):x1+3].reshape(-1,3)
                bg=tuple(int(v) for v in np.median(np.concatenate([a]),axis=0))
                ImageDraw.Draw(img).rectangle([x0-2,y0-2,x1+2,y1+2],fill=bg+(255,)); r.append('patch:'+w)
            else:
                try: replace_ls(img,(max(0,b[0]-6),max(0,b[1]-6),b[2]+6,b[3]+6)); r.append('ls:'+w)
                except Exception as e: r.append('ERR:'+w)
        # çerçeve
        W=1000; can=Image.new('RGBA',(W,W),(255,255,255,255))
        im=img.copy(); f=min(900/im.width,700/im.height); im=im.resize((int(im.width*f),int(im.height*f)),Image.LANCZOS)
        can.alpha_composite(im,((W-im.width)//2,165+(700-im.height)//2))
        draw_ribbon(can,base_code(n['code']))
        can.alpha_composite(OVL)
        out=ROOT+f'out_eksik/{n["code"].lower().replace("/","-")}-{k}.png'
        can.convert('RGB').save(out); rep[out]=r
for k,v in rep.items():
    if v: print(os.path.basename(k),v)
print(len(rep))
