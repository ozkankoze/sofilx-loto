# Yeni set görselleri: başlıktaki LS- kodunu BD- olarak yeniden yazar (metni siler, aynı yere yeni kodu çizer)
import numpy as np, cv2, sys
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
ROOT = '/home/claude/sofilx/'

# (dosya, metin kutusu, yeni kod, font)
JOBS = [
    (0, (40, 60, 425, 134), 'BD-X02CY', 'Montserrat-800.ttf', 'light'),
    (1, (42, 58, 358, 116), 'BD-LG033', 'Montserrat-800.ttf', 'light'),
    (2, (14, 53, 336, 114), 'BD-B102C', 'Montserrat-800.ttf', 'yellow'),
    (3, (400, 20, 670, 92), 'BD-MC-C051', 'BarlowCondensed-700.ttf', None),
    (4, (325, 32, 735, 110), 'BD-PR-UV07', 'Montserrat-800.ttf', None),
    (5, (345, 22, 745, 94), 'BD-VM-K05', 'Montserrat-800.ttf', None),
]


def recode(img, box, text, font, mode=None):
    a = np.array(img.convert('RGB'))
    x0, y0, x1, y1 = box
    c = a[y0:y1, x0:x1].astype(int)
    border = np.concatenate([c[0], c[-1], c[:, 0], c[:, -1]])
    bg = np.median(border, axis=0)
    if mode == 'light':
        m = c.min(-1) > 150
    elif mode == 'yellow':
        m = (c[..., 1] > 120) & (c[..., 0] > 180)
    else:
        m = np.abs(c - bg).max(-1) > 70
    lab, n = ndi.label(m)
    hh, ww = m.shape
    ok = []
    for i, sl in enumerate(ndi.find_objects(lab)):
        if (lab[sl] == i + 1).sum() <= 15: continue
        if sl[0].start == 0 or sl[1].start == 0 or sl[0].stop == hh or sl[1].stop == ww: continue
        ok.append(i + 1)
    keep = np.isin(lab, ok)
    halo = np.abs(c - bg).max(-1) > 40
    ys, xs = np.where(keep)
    ty0, ty1, tx0, tx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    # metin rengi: satır satır (degrade metinler için)
    rowcol = []
    for r in range(ty0, ty1):
        px = c[r][keep[r]]
        rowcol.append(np.median(px, axis=0) if len(px) else None)
    last = next(v for v in rowcol if v is not None)
    rowcol = [last := (v if v is not None else last) for v in rowcol]
    # sil (inpaint)
    full = np.zeros(a.shape[:2], np.uint8)
    full[y0:y1, x0:x1] = (ndi.binary_dilation(keep, iterations=4) | (ndi.binary_dilation(keep, iterations=6) & halo)).astype(np.uint8) * 255
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), full, 5, cv2.INPAINT_TELEA)
    out = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).convert('RGBA')
    # yeni metni çiz: aynı yükseklik, aynı genişlik
    f = ImageFont.truetype(ROOT + 'fonts/' + font, 300)
    bb = f.getbbox(text)
    lay = Image.new('L', (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), 0)
    ImageDraw.Draw(lay).text((10 - bb[0], 10 - bb[1]), text, font=f, fill=255)
    lay = lay.crop(lay.getbbox())
    W, H = tx1 - tx0, ty1 - ty0
    lay = lay.resize((W, H), Image.LANCZOS)
    grad = np.zeros((H, W, 4), np.uint8)
    for r in range(H):
        grad[r, :, :3] = rowcol[r].astype(np.uint8)
    grad[..., 3] = np.array(lay)
    out.alpha_composite(Image.fromarray(grad, 'RGBA'), (int(x0 + tx0), int(y0 + ty0)))
    return out


if __name__ == '__main__':
    for i, box, text, font, mode in JOBS:
        im = Image.open(ROOT + f'src_yeni/{i}.png')
        recode(im, box, text, font, mode).convert('RGB').save(ROOT + f'out_yeni/{i}.png')
    print('ok')


def extra_fixes():
    import io, cairosvg
    # BD-B102C: istasyon başlığındaki LOCKSAN logosu -> Sofilx logosu
    p = ROOT + 'out_yeni/2.png'
    a = np.array(Image.open(p).convert('RGB'))
    x0, y0, x1, y1 = 228, 170, 480, 234
    c = a[y0:y1, x0:x1].astype(int)
    red = (c[..., 0] - np.maximum(c[..., 1], c[..., 2])) > 60
    red &= c[..., 1] < 150
    msk = np.zeros(a.shape[:2], np.uint8)
    msk[y0:y1, x0:x1] = ndi.binary_dilation(red, iterations=3).astype(np.uint8) * 255
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), msk, 5, cv2.INPAINT_TELEA)
    out = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).convert('RGBA')
    svg = open(ROOT + 'brand/sofilx-logo.svg').read()
    h = 50; w = int(h * 356.09 / 76.56)
    lg = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=w * 3, output_height=h * 3))).convert('RGBA').resize((w, h), Image.LANCZOS)
    out.alpha_composite(lg, (472 - w, 178))
    out.convert('RGB').save(p)
    # BD-MC-C051: etiketteki küçük LS-LT02 yazısı -> BD-LT02
    p = ROOT + 'out_yeni/3.png'
    a = np.array(Image.open(p).convert('RGB'))
    x0, y0, x1, y1 = 748, 546, 786, 557
    c = a[y0:y1, x0:x1].astype(int)
    dark = (c.max(-1) < 110)
    ys, xs = np.where(dark)
    ty0, ty1, tx0, tx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    msk = np.zeros(a.shape[:2], np.uint8)
    msk[y0:y1, x0:x1] = ndi.binary_dilation(dark, iterations=2).astype(np.uint8) * 255
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), msk, 3, cv2.INPAINT_TELEA)
    out = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).convert('RGBA')
    f = ImageFont.truetype(ROOT + 'fonts/Montserrat-700.ttf', 200)
    bb = f.getbbox('BD-LT02'); lay = Image.new('L', (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), 0)
    ImageDraw.Draw(lay).text((10 - bb[0], 10 - bb[1]), 'BD-LT02', font=f, fill=255)
    lay = lay.crop(lay.getbbox()).resize((tx1 - tx0, ty1 - ty0), Image.LANCZOS)
    col = Image.new('RGBA', lay.size, (35, 35, 35, 255)); col.putalpha(lay)
    out.alpha_composite(col, (x0 + tx0, y0 + ty0))
    out.convert('RGB').save(p)


extra_fixes()
