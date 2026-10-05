from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
F='/home/claude/sofilx/fonts/'
def text_path(fontfile, text, size, x0, y0, track=0):
    f=TTFont(fontfile); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; s=size/upm
    pen=SVGPathPen(gs); x=x0
    for ch in text:
        gn=cmap[ord(ch)]; tp=TransformPen(pen,(s,0,0,-s,x,y0)); gs[gn].draw(tp); x+=gs[gn].width*s+track
    return pen.getCommands(), x-track
RED='#C0262D'; INK='#141414'
ICON='''<g transform="translate({x} {y}) scale({k})"><g transform="rotate(45 50 50)" fill="none" stroke="{c}" stroke-width="7.5" stroke-linejoin="round">
<path d="M8.4 43.5 A42 42 0 0 1 91.6 43.5 Z"/><path d="M91.6 56.5 A42 42 0 0 1 8.4 56.5 Z"/>
<path d="M37 43.5 A20 20 0 0 1 77 43.5"/><path d="M63 56.5 A20 20 0 0 1 23 56.5"/></g></g>'''
def build(ink=INK, red=RED, name='sofilx-logo'):
    # horizontal: icon 100 + wordmark
    d1,x1=text_path(F+'ArchivoBlack.ttf','SOFİLX',64,118,66)
    d2,x2=text_path(F+'BarlowCondensed-700.ttf','LOTO EKİPMANLARI',22.5,120,96,track=4.2)
    W=max(x1,x2)+4
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 104" role="img" aria-label="Sofilx LOTO">
{ICON.format(x=2,y=2,k=1,c=ink)}
<path fill="{ink}" d="{d1}"/><path fill="{red}" d="{d2}"/></svg>'''
    open(name+'.svg','w').write(svg); return W
print(build())
print(build('#FFFFFF','#FF4D4F','sofilx-logo-beyaz'))
open('sofilx-ikon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 104 104">'+ICON.format(x=2,y=2,k=1,c=INK)+'</svg>')
