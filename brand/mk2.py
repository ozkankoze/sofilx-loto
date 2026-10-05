import json, cairosvg
T=json.load(open('trace.json')); B=json.load(open('trace_bb.json'))
ix0,iy0,ix1,iy1=B['icon']; wx0,wy0,wx1,wy1=B['word']
iw,ih=ix1-ix0,iy1-iy0; ww,wh=wx1-wx0,wy1-wy0
def stacked(c):
    pad=2; x0=min(ix0,wx0)-pad; y0=iy0-pad; W=max(ix1,wx1)-x0+pad; H=wy1-y0+pad
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {W:.2f} {H:.2f}" role="img" aria-label="Sofilx"><path fill="{c}" fill-rule="evenodd" d="{T["icon"]}"/><path fill="{c}" fill-rule="evenodd" d="{T["word"]}"/></svg>'
def horiz(c):
    s=(wh*1.32)/ih  # ikon yüksekliği
    gap=wh*0.32
    Hh=wh*1.32
    ity=( Hh-ih*s)/2; wty=(Hh-wh)/2
    W=iw*s+gap+ww
    g1=f'<g transform="translate({-ix0*s:.3f} {ity-iy0*s:.3f}) scale({s:.5f})"><path fill="{c}" fill-rule="evenodd" d="{T["icon"]}"/></g>'
    g2=f'<g transform="translate({iw*s+gap-wx0:.3f} {wty-wy0:.3f})"><path fill="{c}" fill-rule="evenodd" d="{T["word"]}"/></g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {Hh:.2f}" role="img" aria-label="Sofilx">{g1}{g2}</svg>', W, Hh
def icon(c):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{ix0-2:.2f} {iy0-2:.2f} {iw+4:.2f} {ih+4:.2f}"><path fill="{c}" fill-rule="evenodd" d="{T["icon"]}"/></svg>'
INK='#141414'
open('sofilx-logo-dikey.svg','w').write(stacked(INK)); open('sofilx-logo-dikey-beyaz.svg','w').write(stacked('#ffffff'))
h,W,H=horiz(INK); open('sofilx-logo.svg','w').write(h); print('yatay oran',W/H)
open('sofilx-logo-beyaz.svg','w').write(horiz('#ffffff')[0])
open('sofilx-ikon.svg','w').write(icon(INK)); open('sofilx-ikon-beyaz.svg','w').write(icon('#ffffff'))
for n,bg in [('sofilx-logo','white'),('sofilx-logo-beyaz','#141414'),('sofilx-logo-dikey','white'),('sofilx-logo-dikey-beyaz','#141414'),('sofilx-ikon','white')]:
    cairosvg.svg2png(url=n+'.svg',write_to=n+'.png',output_width=1200 if 'ikon' not in n else 512)
    cairosvg.svg2png(url=n+'.svg',write_to='/tmp/claude-0/t/'+n+'.png',output_width=700,background_color=bg)
