import json, os, sys, numpy as np, cairosvg, io
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
ROOT='/home/claude/sofilx/'
med=np.array(Image.open(ROOT+'data/template_median.png').convert('RGB')).astype(int)
rf=np.load(ROOT+'data/redfrac.npy')
INK=np.array([20,20,20]); RED=np.array([192,38,45])
H=W=1000
yy,xx=np.mgrid[0:H,0:W]; S=xx+yy
ZONE_LOGO=(xx>=470)&(yy<145)
ZONE_SW=(S<420)|((yy<40)&(xx<420))
BAND=(S>=1772)&(S<=1892)
CORNER=S>1892
def overlay_png():
    logo=open(ROOT+'brand/sofilx-logo.svg').read()
    inner=logo.split('>',1)[1].rsplit('</svg>',1)[0]
    lw=450; k=lw/381.6
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">
<polygon points="0,0 150,0 0,150" fill="#141414"/>
<polygon points="168,0 192,0 0,192 0,168" fill="#C0262D"/>
<g transform="translate(523 24) scale({k})">{inner}</g></svg>'''
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGBA')
OVL=overlay_png()
FONT=ImageFont.truetype(ROOT+'fonts/Montserrat-700.ttf',100)
COLORS={'RED','YLW','BLUE','GRN','BLK','WHITE','ORJ','PRP'}
def base_code(c):
    c=c.replace(' ','')
    p=c.split('-'); return '-'.join(p[:-1]) if p[-1] in COLORS else c
def draw_ribbon(out_img, text):
    # out_img: RGBA PIL. draw full Sofilx ribbon with text
    d=ImageDraw.Draw(out_img)
    d.polygon([(778,1000),(1000,778),(1000,886),(886,1000)],fill=(20,20,20,255))
    d.polygon([(778,1000),(1000,778),(1000,784),(784,1000)],fill=(192,38,45,255))
    avail=228; size=40
    while True:
        f=ImageFont.truetype(ROOT+'fonts/Montserrat-700.ttf',size)
        tb=f.getbbox(text); tw=tb[2]-tb[0]
        if tw<=avail or size<=14: break
        size-=1
    cap=f.getbbox('H'); ch=cap[3]-cap[1]
    layer=Image.new('RGBA',(tw+20,ch+20),(0,0,0,0))
    ImageDraw.Draw(layer).text((10-tb[0],10-cap[1]),text,font=f,fill=(255,255,255,255))
    rot=layer.rotate(45,resample=Image.BICUBIC,expand=True)
    vc=(1784+1886)/2
    cx=vc/2; cy=vc/2
    out_img.alpha_composite(rot,(int(round(cx-rot.width/2)),int(round(cy-rot.height/2))))
def process(src,dst,report=None,code=None):
    im0=Image.open(src).convert('RGB')
    if im0.size!=(1000,1000): im0=im0.resize((1000,1000),Image.LANCZOS)
    a=np.array(im0).astype(int)
    out=a.copy()
    diff=np.abs(a-med).max(-1)
    nearwhite=a.min(-1)>200
    # 1) erase logo + swoosh where template present
    tm=ndi.binary_dilation((rf>0.2)&ZONE_LOGO,iterations=5)|(ndi.binary_dilation((rf>0.03)&ZONE_SW,iterations=6)&ZONE_SW)
    redish=(a[...,0]-np.maximum(a[...,1],a[...,2]))>40
    erase=tm&(redish|(a.min(-1)>150)|(diff<90))
    out[erase]=255
    # 2) ribbon recolor: t = redness amount
    r,g,b=a[...,0],a[...,1],a[...,2]
    t=np.clip((r-np.maximum(g,b))/ (190.0),0,1)
    band=BAND
    # text pixels (white inside band) detection before recolor
    white_in_band=band&(a.min(-1)>170)&ndi.binary_erosion(BAND,iterations=6)
    newc=(255*(1-t[...,None])+INK*t[...,None])
    # inside band interior everything not white is band color -> keep antialias via t; white text stays white
    out[band]=newc[band].astype(int)
    # band edges: thin red line along inner edge (S=1772..1778)
    edge=(S>=1772)&(S<1779)&(t>0.5)
    out[edge]=RED
    # corner triangle beyond band: if template white keep
    # 3) find L and S components in text
    lab,n=ndi.label(white_in_band)
    comps=[]
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(xs)<40: continue
        u=(xs-ys); v=(xs+ys)
        comps.append(dict(i=i,umin=u.min(),umax=u.max(),vmin=v.min(),vmax=v.max(),n=len(xs)))
    if comps:
        hmax=max(c['vmax']-c['vmin'] for c in comps if c['vmin']>1790 and c['vmax']<1880) if any(c['vmin']>1790 and c['vmax']<1880 for c in comps) else 0
        inner=[c for c in comps if c['vmin']>1780 and c['vmax']<1880 and c['vmax']-c['vmin']>=10]
        cen=[(c['vmin']+c['vmax'])/2 for c in inner]
        twoline=bool(cen) and (max(cen)-min(cen))>25
        comps=[c for c in inner if (c['vmax']-c['vmin'])>=0.75*hmax]
    else: twoline=False
    comps.sort(key=lambda c:c['umin'])
    core=ndi.binary_erosion(BAND,iterations=8)
    redcore=(t>0.6)[core].mean()
    oneline=len(comps)>=3 and (max(c['vmin'] for c in comps)-min(c['vmin'] for c in comps))<=8
    capc=(comps[0]['vmax']-comps[0]['vmin'])/np.sqrt(2) if comps else 0
    if len(comps)<3 or twoline or not oneline or redcore<0.55 or not (14<=capc<=32.5):
        # fallback: wipe corner from ORIGINAL and redraw
        out=a.copy(); out[erase]=255
        red2=(a[...,0]-np.maximum(a[...,1],a[...,2]))>30
        wipe=(S>1700)&(red2|nearwhite|(S>1765))
        wipe=ndi.binary_dilation(wipe,iterations=2)&(S>1695)
        out[wipe]=255
        img=Image.fromarray(out.astype(np.uint8)).convert('RGBA')
        txt=base_code(code or 'BD-?')
        draw_ribbon(img,txt)
        img.alpha_composite(OVL); img.convert('RGB').save(dst)
        if report is not None: report.update(mode='redraw',text=txt,redcore=float(redcore),ncomp=len(comps))
        return 'redraw'
    L,Sx=comps[0],comps[1]
    m=(lab==L['i'])|(lab==Sx['i'])
    m=ndi.binary_dilation(m,iterations=3)&ndi.binary_erosion(BAND,iterations=3)
    out[m]=INK
    # draw BD: cap height along v (perp) = L vmax-vmin (in x+y units -> /sqrt2)
    cap=(L['vmax']-L['vmin'])/np.sqrt(2)
    ulen_left=L['umin']/np.sqrt(2); uright=Sx['umax']/np.sqrt(2)
    vc=(L['vmin']+L['vmax'])/2/np.sqrt(2)
    # font size so cap height matches
    bb=FONT.getbbox('B'); capf=bb[3]-bb[1]
    size=max(8,int(round(100*cap/capf)))
    f=ImageFont.truetype(ROOT+'fonts/Montserrat-700.ttf',size)
    tb=f.getbbox('BD'); tw=tb[2]-tb[0]; th=tb[3]-tb[1]
    layer=Image.new('RGBA',(tw+20,th+20),(0,0,0,0))
    ImageDraw.Draw(layer).text((10-tb[0],10-tb[1]),'BD',font=f,fill=(255,255,255,255))
    rot=layer.rotate(45,resample=Image.BICUBIC,expand=True)
    # target: right edge of BD at uright, centre at vc. rotated coords: u=(x-y)/√2, v=(x+y)/√2
    ucen=uright-tw/2
    cx=(ucen+vc)/np.sqrt(2); cy=(vc-ucen)/np.sqrt(2)
    img=Image.fromarray(out.astype(np.uint8)).convert('RGBA')
    img.alpha_composite(rot,(int(round(cx-rot.width/2)),int(round(cy-rot.height/2))))
    img.alpha_composite(OVL)
    img.convert('RGB').save(dst)
    if report is not None: report.update(n_comp=len(comps),cap=float(cap))
    return True
if __name__=='__main__':
    a=sys.argv[1:]
    for k in range(0,len(a),3): print(process(a[k],a[k+1],code=a[k+2]))
