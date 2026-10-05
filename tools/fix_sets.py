import json,os,numpy as np, io, cairosvg
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
ROOT='/home/claude/sofilx/'
def render_bd(cap, width, color, heavy):
    font=ROOT+('fonts/ArchivoBlack.ttf' if heavy else 'fonts/Montserrat-700.ttf')
    f=ImageFont.truetype(font,200); bb=f.getbbox('BD')
    lay=Image.new('L',(bb[2]-bb[0]+10,bb[3]-bb[1]+10),0)
    ImageDraw.Draw(lay).text((5-bb[0],5-bb[1]),'BD',font=f,fill=255)
    lay=lay.crop(lay.getbbox())
    lay=lay.resize((max(1,int(width)),max(1,int(cap))),Image.LANCZOS)
    col=Image.new('RGBA',lay.size,tuple(int(c) for c in color)+(255,)); col.putalpha(lay)
    return col
import pytesseract
def replace_ls(img, box, skip=0, dbg=None, lsx=None, italic=0.0):
    x0,y0,x1,y1=box; a=np.array(img.convert('RGB')).astype(int); c=a[y0:y1,x0:x1]
    border=np.concatenate([c[0],c[-1],c[:,0],c[:,-1]]); bg=np.median(border,axis=0)
    m=(np.abs(c-bg).max(-1)>90)
    t=Image.fromarray(np.where(m,0,255).astype(np.uint8)).resize((c.shape[1]*3,c.shape[0]*3))
    H=t.height
    ch=[(l.split()[0],int(l.split()[1])//3,(H-int(l.split()[4]))//3,int(l.split()[3])//3,(H-int(l.split()[2]))//3) for l in pytesseract.image_to_boxes(t,config='--psm 7').strip().splitlines()]
    if lsx:
        L=('L',lsx[0]-x0,0,lsx[0]-x0,c.shape[0]); S=('S',lsx[1]-x0,0,lsx[1]-x0,c.shape[0])
    else:
        idx=next((k for k in range(len(ch)-1) if ch[k][0] in 'L' and ch[k+1][0] in 'S5'),None)
        if idx is not None: L,S=ch[idx],ch[idx+1]
        else:
            lab,n=ndi.label(m,structure=np.ones((3,3))); comps=[]
            for k,sl in enumerate(ndi.find_objects(lab)):
                if (lab[sl]==k+1).sum()<12: continue
                comps.append((sl[1].start,sl[0].start,sl[1].stop,sl[0].stop))
            hmax=max(cc[3]-cc[1] for cc in comps)
            comps=sorted([cc for cc in comps if cc[3]-cc[1]>=0.6*hmax],key=lambda cc:cc[0])
            if comps and (comps[0][2]-comps[0][0])<0.35*hmax and len(comps)>2: comps=comps[1:]  # skip paren
            L=('L',)+comps[0]; S=('S',)+comps[1]
    # refine using mask: columns from L.x0 to S.x1, rows where mask present in that span
    lx0=L[1]; sx1=S[3]
    sub=m[:,lx0:sx1]; rows=np.where(sub.any(1))[0]
    # restrict rows to the text line: rows overlapping L box
    ty0=max(rows.min(),min(L[2],S[2])-2); ty1=min(rows.max()+1,max(L[4],S[4])+2)
    sub=m[ty0:ty1,lx0:sx1]; rr=np.where(sub.any(1))[0]; cc=np.where(sub.any(0))[0]
    ty0,ty1=ty0+rr.min(),ty0+rr.max()+1; lx0,sx1=lx0+cc.min(),lx0+cc.max()+1
    cap=ty1-ty0; width=sx1-lx0
    tc=np.median(c[ty0:ty1,lx0:sx1][m[ty0:ty1,lx0:sx1]],axis=0)
    dens=m[ty0:ty1,lx0:sx1].mean()
    ratio=width/cap
    if ratio<1.12: font='fonts/BarlowCondensed-700.ttf'
    elif dens>0.47: font='fonts/ArchivoBlack.ttf'
    elif dens>0.36: font='fonts/Montserrat-700.ttf'
    else: font='fonts/Barlow-500.ttf'
    d=ImageDraw.Draw(img)
    d.rectangle([x0+lx0-2,y0+ty0-2,x0+sx1+1,y0+ty1+1],fill=tuple(int(v) for v in bg))
    f=ImageFont.truetype(ROOT+font,200); bb=f.getbbox('BD')
    lay=Image.new('L',(bb[2]-bb[0]+10,bb[3]-bb[1]+10),0)
    ImageDraw.Draw(lay).text((5-bb[0],5-bb[1]),'BD',font=f,fill=255)
    lay=lay.crop(lay.getbbox())
    if italic:
        sh=italic; w0,h0=lay.size; extra=int(h0*sh)
        lay=lay.transform((w0+extra,h0),Image.AFFINE,(1,sh,-extra,0,1,0),resample=Image.BICUBIC)
    lay=lay.resize((width,cap),Image.LANCZOS)
    col=Image.new('RGBA',lay.size,tuple(int(v) for v in tc)+(255,)); col.putalpha(lay)
    img.alpha_composite(col,(x0+lx0,y0+ty0))
    return dict(font=font.split('/')[1],ratio=round(ratio,2),dens=round(float(dens),2))
LOGO_W=open(ROOT+'brand/sofilx-logo-beyaz.svg').read()
def patch(img, box, kind='bag'):
    x0,y0,x1,y1=box; w=x1-x0; h=y1-y0
    d=ImageDraw.Draw(img)
    if kind=='bag':
        d.rounded_rectangle([x0,y0,x1,y1],radius=max(3,h//8),fill=(200,200,204,255))
        p=max(3,h//10); d.rounded_rectangle([x0+p,y0+p,x1-p,y1-p],radius=max(2,h//10),fill=(22,22,22,255))
        iw=w-4*p; ih=h-4*p
        svg=LOGO_W.replace('<svg ',f'<svg width="{iw*3}" height="{ih*3}" preserveAspectRatio="xMidYMid meet" ',1)
        lg=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGBA').resize((iw,ih),Image.LANCZOS)
        img.alpha_composite(lg,(x0+2*p,y0+2*p))
    else: # printed text on surface
        a=np.array(img.convert('RGB'))[y0:y1,x0:x1].reshape(-1,3)
        bg=tuple(int(v) for v in np.median(a,axis=0)); d.rectangle([x0,y0,x1,y1],fill=bg+(255,))
        f=ImageFont.truetype(ROOT+'fonts/ArchivoBlack.ttf',int(h*0.45))
        d.text((x0+2,y0+1),'SOFİLX',font=f,fill=(30,30,30,255))
        f2=ImageFont.truetype(ROOT+'fonts/Barlow-500.ttf',int(h*0.38)); d.text((x0+2,y0+int(h*0.52)),'Safety',font=f2,fill=(30,30,30,255))
JOBS={
 '8773d':dict(codes=[((470,82,925,130),1)],patches=[(620,330,808,404,'bag')]),
 '8812s':dict(codes=[((381,73,721,126),1)]),
 'b1100s':dict(codes=[((410,55,650,112),1)]),
 'eb-s10v':dict(codes=[((525,68,875,122),0)],patches=[(680,293,842,357,'bag')]),
 'ek-s1100vv':dict(codes=[((475,72,920,116),0)],patches=[(445,305,525,339,'text')]),
 'ekm-l040':dict(codes=[((1065,60,1370,125),0)],patches=[(358,323,549,402,'bag')]),
 'gkv-s500':dict(codes=[((518,63,875,112),0)]),
 'l1010bd':dict(patches=[(292,208,453,272,'bag')]),
 'm-e07':dict(codes=[((343,31,665,91),0)],patches=[(252,1001,406,1050,'bag')]),
 'mn-u80':dict(codes=[((1015,84,1351,161),0)],patches=[(343,437,557,510,'bag')]),
 'pe-e010s':dict(codes=[((305,290,615,345),0)]),
 'pe-e09s':dict(codes=[((296,345,656,392),0)]),
 'pr-u07':dict(codes=[((298,24,615,68),0,(298,372))]),
 'ps02s':dict(codes=[((60,118,632,237),0,(91,219))]),
 'vk-u067s':dict(codes=[((255,5,600,85),0)]),
 'vn-02':dict(codes=[((523,81,836,128),1)]),
 'x02-elk':dict(codes=[((430,71,847,116),1)]),
 'x07s-metal-loto-istasyon-seti-1':dict(codes=[((300,15,700,72),0)]),
 'x07s-metal-loto-istasyon-seti-2':dict(codes=[((40,38,380,115),0)]),
 'x07un':dict(codes=[((72,112,605,237),0)]),
 'zs030c':dict(codes=[((320,5,600,90),0)]),
}
if __name__=='__main__':
    import glob,sys
    os.makedirs(ROOT+'out_set',exist_ok=True)
    rep={}
    for key,job in JOBS.items():
        fs=[f for f in glob.glob(ROOT+'src_img/ls-*'+key+'*.webp') if not f.endswith('-k.webp')]
        if key.startswith('x07s-metal'): fs=[ROOT+'src_img/ls-'+key+'.webp']
        assert len(fs)==1,(key,fs)
        img=Image.open(fs[0]).convert('RGBA'); r=[]
        for cd in job.get('codes',[]):
            box,skip=cd[0],cd[1]; lsx=cd[2] if len(cd)>2 else None
            try: r.append(replace_ls(img,box,skip,lsx=lsx))
            except Exception as e: r.append('ERR '+repr(e))
        for p in job.get('patches',[]): patch(img,p[:4],p[4])
        out=ROOT+'out_set/'+os.path.basename(fs[0]).replace('.webp','.png'); img.convert('RGB').save(out); rep[key]=r
    for k,v in rep.items(): print(k,v)
