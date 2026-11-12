# AG/OG elektrik güvenlik ürünleri: kaynak fotoğrafı Sofilx çerçevesine oturtur (logo + köşe şeridi + kod)
import io, os, sys, cairosvg, numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = '/home/claude/sofilx/'
SRC = ROOT + 'src_elektrik/'
OUT = ROOT + 'out_elektrik/'


def overlay():
    logo = open(ROOT + 'brand/sofilx-logo.svg').read()
    inner = logo.split('>', 1)[1].rsplit('</svg>', 1)[0]
    k = 450 / 381.6
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">
<polygon points="0,0 150,0 0,150" fill="#141414"/>
<polygon points="168,0 192,0 0,192 0,168" fill="#C0262D"/>
<g transform="translate(523 24) scale({k})">{inner}</g></svg>'''
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGBA')


def ribbon(img, text):
    d = ImageDraw.Draw(img)
    d.polygon([(778, 1000), (1000, 778), (1000, 886), (886, 1000)], fill=(20, 20, 20, 255))
    d.polygon([(778, 1000), (1000, 778), (1000, 784), (784, 1000)], fill=(192, 38, 45, 255))
    size = 40
    while True:
        f = ImageFont.truetype(ROOT + 'fonts/Montserrat-700.ttf', size)
        tb = f.getbbox(text); tw = tb[2] - tb[0]
        if tw <= 228 or size <= 14: break
        size -= 1
    cap = f.getbbox('H'); ch = cap[3] - cap[1]
    lay = Image.new('RGBA', (tw + 20, ch + 20), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((10 - tb[0], 10 - cap[1]), text, font=f, fill=(255, 255, 255, 255))
    rot = lay.rotate(45, resample=Image.BICUBIC, expand=True)
    c = (1784 + 1886) / 4
    img.alpha_composite(rot, (int(round(c - rot.width / 2)), int(round(c - rot.height / 2))))


def compose(src, dst, code, box=720):
    im = Image.open(src).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    a = np.array(bg.convert('RGB')).astype(int)
    m = a.min(-1) < 235
    ys, xs = np.where(m)
    prod = bg.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    r = min(box / prod.width, box / prod.height)
    prod = prod.resize((round(prod.width * r), round(prod.height * r)), Image.LANCZOS)
    can = Image.new('RGBA', (1000, 1000), (255, 255, 255, 255))
    can.alpha_composite(prod, ((1000 - prod.width) // 2, 560 - prod.height // 2))
    can.alpha_composite(overlay())
    ribbon(can, code)
    can.convert('RGB').save(dst)


JOBS = [  # (kaynak, kod, sıra)
    ('hayat-kurtarma-istankasi.png', 'BD-E01', 1),
    ('gorsel-2026-03-17-093129319.png', 'BD-E01', 2),
    ('ag-og-ikaz-banti.png', 'BD-E02', 1),
    ('36kv-kontrol-kalemi.png', 'BD-E03', 1),
    ('gorsel-2026-03-17-093048057.png', 'BD-E03', 2),
    ('acil-durum-kablo-kesme-makasi.png', 'BD-E04', 1),
    ('izole-sigorta-pensesi.png', 'BD-E05', 1),
]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for f, code, k in JOBS:
        compose(SRC + f, OUT + f'{code.lower()}-{k}.png', code)
    print('ok', len(JOBS))
