import io, glob, numpy as np, cairosvg, sys
from PIL import Image
from scipy import ndimage as ndi
ROOT='/home/claude/sofilx/'
old=open(ROOT+'brand/eski-logo-tasarim.svg').read(); inner=old.split('>',1)[1].rsplit('</svg>',1)[0]
k=450/381.6
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000"><g transform="translate(523 24) scale({k})">{inner}</g></svg>'
om=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).split()[-1])>8
om=ndi.binary_dilation(om,iterations=3)
new=open(ROOT+'brand/sofilx-logo.svg').read()
LW=410
png=cairosvg.svg2png(bytestring=new.encode(),output_width=LW*2)
logo=Image.open(io.BytesIO(png)).convert('RGBA'); logo=logo.resize((LW,int(logo.height*LW/logo.width)),Image.LANCZOS)
POS=(965-LW, 30+(118-logo.height)//2)
def apply(f):
    im=Image.open(f).convert('RGB'); a=np.array(im)
    if im.size!=(1000,1000): return False
    a[om]=255
    im=Image.fromarray(a).convert('RGBA'); im.alpha_composite(logo,POS); im.convert('RGB').save(f); return True
if __name__=='__main__':
    n=0
    for d in sys.argv[1:]:
        for f in glob.glob(d+'/*.png'): n+=apply(f)
    print('güncellendi',n, 'logo',logo.size,POS)
