import sys,json,os
os.chdir('/home/claude/sofilx'); sys.argv=['x']
exec(open('tools/convert.py').read().split("if __name__")[0])
P=json.load(open('data/urunler_ham.json')); C=json.load(open('data/img_class.json'))
os.makedirs('out_img',exist_ok=True)
code_of={}
for p in P:
    for i in p['images']: code_of.setdefault(i,p['code'])
log={}
todo=[i for i,v in C.items() if len(v)>1 and v[2]<12]
for n,i in enumerate(todo):
    src='src_img/'+(os.path.basename(i)+'.webp' if i.startswith('/assets') else i)
    name=os.path.basename(i).split('~')[0].replace('.webp','')
    dst=f'out_img/{name}.png'
    r={}
    try: res=process(src,dst,report=r,code=code_of[i]); r['res']=str(res)
    except Exception as e: r['err']=repr(e)
    r['code']=code_of[i]; r['out']=dst; log[i]=r
    if n%50==0: print(n,flush=True); json.dump(log,open('data/convert_log.json','w'),indent=0)
json.dump(log,open('data/convert_log.json','w'),indent=0)
print('DONE',len(log))
