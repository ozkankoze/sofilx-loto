import sys,json,os,re,shutil; sys.argv=['x']
exec(open('/home/claude/sofilx/tools/fix_sets.py').read().split("if __name__")[0])
H=json.load(open(ROOT+'data/text_hits2.json')); L=json.load(open(ROOT+'data/convert_log.json'))
os.makedirs(ROOT+'data/bak_inline2',exist_ok=True)
for i,ws in H.items():
    ws=[w for w in ws if 'LOCKSAN' not in w[0].upper()]
    if not ws: continue
    out=ROOT+L[i]['out']; bak=ROOT+'data/bak_inline2/'+os.path.basename(out)
    if not os.path.exists(bak): shutil.copy(out,bak)
    img=Image.open(bak).convert('RGBA'); boxes=[]
    for w,x,y,ww,hh in ws:
        b=(x,y,x+ww,y+hh)
        if any(abs(b[0]-o[0])<8 and abs(b[1]-o[1])<8 for o in boxes): continue
        boxes.append(b)
    res=[]
    for b in boxes:
        box=(max(0,b[0]-6),max(0,b[1]-6),b[2]+6,b[3]+6)
        try: r=replace_ls(img,box); res.append(r['font'])
        except Exception as e: res.append('ERR '+repr(e)[:40])
    img.convert('RGB').save(out); print(os.path.basename(out),res)
