import json, os, io, cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT='/home/claude/sofilx/'
L=json.load(open(ROOT+'data/convert_log.json'))
RAW=json.load(open(ROOT+'data/urunler_ham.json'))
def src(code):
    p=next(p for p in RAW if p['code'].replace(' ','')==code)
    return ROOT+L[p['images'][0]]['out']
POSTS={
 'eked-loto-egitimi-rehberi':(['BD-G01-RED','BD-K61','BD-LT05'],'EĞİTİM REHBERİ','EKED – LOTO\nEĞİTİMİ'),
 'dogru-eked-ekipmaninin-onemi':(['BD-D11N','BD-F01','BD-K61'],'EKİPMAN SEÇİMİ','DOĞRU EKİPMAN,\nDOĞRU KİLİT'),
 'emniyet-asma-kilitler':(['BD-G21-RED','BD-G01-RED','BD-G13-BLUE'],'ASMA KİLİTLER','EMNİYET\nASMA KİLİTLERİ'),
 'is-guvenligi-temel-tasi':(['BD-B102','BD-D11N','BD-G11-RED'],'İŞ GÜVENLİĞİ','GÜVENLİĞİN\nTEMEL TAŞI'),
}
W,H=1200,630
FH=ROOT+'fonts/BarlowCondensed-800.ttf'; FS=ROOT+'fonts/BarlowCondensed-600.ttf'
logo_svg=open(ROOT+'brand/sofilx-logo-beyaz.svg').read()
logo=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=logo_svg.encode(),output_width=380))).convert('RGBA'); logo=logo.resize((190,int(logo.height*190/logo.width)),Image.LANCZOS)
def product(code,size):
    import numpy as np
    im=Image.open(src(code)).convert('RGB'); a=np.array(im).astype(int)
    m=(a.min(-1)<235); m[:160,:]=False; yy,xx=np.mgrid[0:1000,0:1000]; m[(xx+yy)>1700]=False; m[(xx+yy)<330]=False
    ys,xs=np.where(m); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    cx,cy=(x0+x1)/2,(y0+y1)/2; r=max(x1-x0,y1-y0)/2*1.18
    return im.crop((int(cx-r),int(cy-r),int(cx+r),int(cy+r))).resize((size,size),Image.LANCZOS)
def card(im,rot):
    pad=16; c=Image.new('RGBA',(im.width+2*pad,im.height+2*pad),(255,255,255,255)); c.paste(im,(pad,pad))
    m=Image.new('L',c.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,c.width-1,c.height-1],14,fill=255); c.putalpha(m)
    return c.rotate(rot,resample=Image.BICUBIC,expand=True)
def shadowed(base,c,xy):
    sh=Image.new('RGBA',c.size,(0,0,0,0)); sh.putalpha(c.split()[-1].point(lambda v:int(v*.55)))
    sh=sh.filter(ImageFilter.GaussianBlur(18)); base.alpha_composite(sh,(xy[0]+8,xy[1]+22)); base.alpha_composite(c,xy)
os.makedirs(ROOT+'dist/assets/blog',exist_ok=True)
for slug,(codes,eyebrow,title) in POSTS.items():
    im=Image.new('RGBA',(W,H),(20,20,20,255)); d=ImageDraw.Draw(im)
    # kırmızı ışık + nokta deseni
    glow=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(glow).ellipse([640,-160,1320,520],fill=(192,38,45,120)); glow=glow.filter(ImageFilter.GaussianBlur(120)); im.alpha_composite(glow)
    for x in range(0,W,24):
        for y in range(0,H,24): d.point((x,y),fill=(255,255,255,22))
    d.polygon([(560,H),(720,0),(744,0),(584,H)],fill=(192,38,45,255))
    shadowed(im,card(product(codes[1],230),7),(900,40))
    shadowed(im,card(product(codes[2],210),-6),(950,340))
    shadowed(im,card(product(codes[0],300),-3),(680,165))
    d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(FS,30); d.rectangle([64,92,104,96],fill=(255,107,111)); d.text((118,76),eyebrow,font=f1,fill=(255,107,111),spacing=4)
    f2=ImageFont.truetype(FH,92); y=160
    for line in title.split('\n'):
        d.text((64,y),line,font=f2,fill=(255,255,255)); y+=96
    im.alpha_composite(logo,(64,H-70-logo.height//2))
    d.rectangle([0,H-14,W,H],fill=(242,183,5))
    for x in range(-20,W,28): d.polygon([(x,H),(x+14,H-14),(x+28,H-14),(x+14,H)],fill=(20,20,20))
    out=im.convert('RGB'); out.save(ROOT+f'dist/assets/blog/{slug}.webp',quality=86)
    out.resize((600,315),Image.LANCZOS).save(ROOT+f'dist/assets/blog/{slug}-k.webp',quality=82)
print('ok')
