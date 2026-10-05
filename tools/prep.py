"""Locksan ham verisinden Sofilx ürün verisini ve görsellerini hazırlar."""
import json, os, re, html, unicodedata
from PIL import Image

ROOT = '/home/claude/sofilx/'
RAW = json.load(open(ROOT + 'data/urunler_ham.json'))
LOG = json.load(open(ROOT + 'data/convert_log.json'))
OUT_ASSETS = ROOT + 'dist/assets/urunler/'
os.makedirs(OUT_ASSETS, exist_ok=True)

COLORS = {
    'RED': ('Kırmızı', '#d32f2f'), 'YLW': ('Sarı', '#f2c200'), 'BLUE': ('Mavi', '#1e5bd8'),
    'GRN': ('Yeşil', '#2e9d4b'), 'BLK': ('Siyah', '#1d1d1d'), 'WHITE': ('Beyaz', '#ffffff'),
    'ORJ': ('Turuncu', '#f07a1a'), 'PRP': ('Mor', '#7b3fb5'),
}
G_SERIES = {
    '0': ('Çelik Kelepçeli Emniyet Asma Kilit 38 mm', 'G01–G08'),
    '1': ('Plastik Kelepçeli Emniyet Asma Kilit 38 mm', 'G11–G18'),
    '2': ('Çelik Kelepçeli Emniyet Asma Kilit 76 mm', 'G21–G28'),
    '3': ('Naylon Gövdeli Emniyet Asma Kilit 76 mm', 'G31–G38'),
}
# Locksan kategorisi -> Sofilx kategorisi
CATS = [
    # key, Locksan adı, Sofilx adı, slug, kısa açıklama
    ('asma', 'Emniyet Asma Kilitler', 'Emniyet Asma Kilitler', 'emniyet-asma-kilitler',
     'Çelik ve plastik kelepçeli, 8 renk seçenekli LOTO asma kilitleri.'),
    ('salter', 'Şalter Kilitleme Ekipmanları', 'Şalter ve Devre Kesici Kilitleri', 'salter-kilitleme-ekipmanlari',
     'Minyatür, kompakt ve kalıplı devre kesiciler için kilitleme ekipmanları.'),
    ('vana', 'Vana Kilitleme Ekipmanları', 'Vana Kilitleme Ekipmanları', 'vana-kilitleme-ekipmanlari',
     'Küresel, kelebek, sürgülü ve tapa vanalar için kilitler.'),
    ('kablo', 'Kablo Kilitleme Ekipmanları', 'Kablo Kilitleme Ekipmanları', 'kablo-kilitleme-ekipmanlari',
     'Birden fazla noktayı tek kilitle güvenceye alan ayarlanabilir kablolar.'),
    ('coklandirici', 'Çoklandırıcılar', 'Kilit Çoklandırıcılar', 'kilit-coklandiricilar',
     'Grup kilitleme için çelik, alüminyum ve iletken olmayan çoklandırıcılar.'),
    ('pnomatik', 'Pnömatik Bağlantı Kilitleme Ekipmanları', 'Elektrik ve Pnömatik Kilitleme', 'elektrik-pnomatik-kilitleme-ekipmanlari',
     'Fiş, priz ve pnömatik bağlantılar için kilitleme ekipmanları.'),
    ('istasyon', 'Eked İstasyon Modelleri', 'LOTO İstasyonları', 'lockout-istasyon-canta',
     'Kilit, etiket ve ekipmanları bir arada tutan duvar ve taşınabilir istasyonlar.'),
    ('kutu', 'Grup Kilitleme Kutuları ve Eked Çantaları', 'Grup Kilit Kutuları ve Çantalar', 'grup-kilit-kutusu',
     'Grup kilitleme kutuları ve sahada taşınabilir LOTO çantaları.'),
    ('set', 'Eked Setleri', 'LOTO Setleri', 'set-urunler',
     'Kişisel, elektriksel, mekanik ve vana kilitleme için hazır setler.'),
    ('etiket', 'Eked Uyarı Etiketleri', 'Tehlike Uyarı Etiketleri', 'tehlike-etiketleri',
     'Kilitleme noktalarını işaretleyen dayanıklı uyarı etiketleri.'),
]
CAT_BY_LS = {c[1]: c for c in CATS}


def slugify(s):
    s = s.replace('–', '-').replace('—', '-')
    tr = str.maketrans('çğıöşüÇĞİÖŞÜ', 'cgiosuCGIOSU')
    s = s.translate(tr)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
    return s


def debrand(t):
    t = re.sub(r'\bLocksan(?:\s+Safety)?\s+(?=(?:LS|BD)-)', '', t)
    t = re.sub(r'\bLocksan Safety\b', 'Sofilx LOTO', t)
    t = re.sub(r'\bLocksan\b', 'Sofilx', t)
    t = re.sub(r'\bLS-', 'BD-', t)
    t = re.sub(r'\bls-', 'bd-', t)
    return t


def parse_prose(h):
    h = re.sub(r'<br\s*/?>', '\n', h)
    h = re.sub(r'</(p|li|h\d|div)>', '\n', h)
    h = re.sub(r'<li[^>]*>', '\n• ', h)
    t = html.unescape(re.sub(r'<[^>]+>', '', h))
    t = debrand(t)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in t.split('\n')]
    intro, feats, specs, pack, notes = [], [], [], [], []
    mode = None
    for l in lines:
        if not l or l in ('•',):
            if mode == 'pack':
                continue
            continue
        if l.startswith('🔒'):
            continue
        if re.match(r'^(Özellikler|Teknik Özellikler|Ürün Özellikleri)\s*:?$', l.strip('•').strip()):
            mode = 'spec'; continue
        if l.startswith('📦') or re.match(r'^Paket İçeriği', l):
            mode = 'pack'
            rest = re.sub(r'^📦\s*Paket İçeriği\s*:?', '', l).strip()
            if rest:
                pack.append(rest)
            continue
        if l.startswith('⚠'):
            notes.append(l.lstrip('⚠').strip()); mode = None; continue
        if l.startswith('✔') or l.startswith('✅'):
            x = l.lstrip('✔✅').strip()
            if ':' in x:
                k, v = x.split(':', 1); feats.append((k.strip(), v.strip()))
            else:
                feats.append(('', x))
            mode = None if mode != 'spec' else mode
            continue
        l2 = l.lstrip('•').strip()
        if mode == 'pack' and (re.match(r'^\d+\s*[xX×]', l2) or l2.startswith('-')):
            pack.append(l2.lstrip('-').strip()); continue
        if mode == 'spec' and ':' in l2 and len(l2.split(':', 1)[0]) < 45:
            k, v = l2.split(':', 1)
            if v.strip():
                specs.append((k.strip(), v.strip()))
            else:
                specs.append((k.strip(), ''))
            continue
        if mode == 'spec' and specs and l.startswith('•'):
            # alt madde: bir önceki özelliğe ekle
            k, v = specs[-1]; specs[-1] = (k, (v + ', ' if v else '') + l2); continue
        mode = None
        intro.append(l2)
    # boş değerli spec başlıklarını temizle
    specs = [(k, v) for k, v in specs if v]
    return dict(intro=intro, feats=feats, specs=specs, pack=pack, notes=notes)


def clean_name(p):
    code = re.sub(r'\s*Serisi$', '', p['code']).replace(' ', '')
    name = p['name'].replace(' ', ' ')
    m = re.match(r'^BD-G(\d)(\d)-([A-Z]+)$', code)
    if m:
        series, _, col = m.groups()
        title, rng = G_SERIES[series]
        cname = COLORS.get(col, (col, '#999'))[0]
        return f'{title} – {cname}', code, dict(group='G' + series, group_title=title, group_range=rng,
                                               color=col, color_name=cname, color_hex=COLORS[col][1])
    # "BD-XXX Ürün Adı" -> "Ürün Adı"
    n = re.sub(r'^' + re.escape(code) + r'\s*', '', name)
    n = re.sub(r'^BD-[A-Z0-9\-/]+\s+', '', n) if n == name else n
    n = n.strip(' -|') or name
    return n, code, None


def img_source(i):
    if i in LOG:
        return ROOT + LOG[i]['out']
    base = os.path.basename(i)
    s = ROOT + 'out_set/' + base + '.png'
    if os.path.exists(s):
        return s
    for cand in (ROOT + 'src_img/' + base + '.webp', ROOT + 'src_img/' + i):
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError(i)


def export_img(src, stem):
    big, small = OUT_ASSETS + stem + '.webp', OUT_ASSETS + stem + '-k.webp'
    if not (os.path.exists(big) and os.path.exists(small)) or os.path.getmtime(src) > os.path.getmtime(big):
        im = Image.open(src).convert('RGB')
        b = im.copy(); b.thumbnail((1200, 1200)); b.save(big, quality=86, method=5)
        s = im.copy(); s.thumbnail((520, 520)); s.save(small, quality=82, method=5)
        w, h = b.size
    else:
        w, h = Image.open(big).size
    return dict(src='/assets/urunler/' + stem + '.webp', thumb='/assets/urunler/' + stem + '-k.webp', w=w, h=h)


# --- Kod değişiklikleri (müşteri talebi) ---
RENAME = {'BD-D2394': 'BD-D200'}
# Aynı fotoğrafı paylaşan ürünler: köşe şeridine her ürünün kendi kodu yazılır
OWN_RIBBON = {'BD-D200', 'BD-D17'}


def ribbon_copy(src, code, stem):
    os.makedirs(ROOT + 'out_fix', exist_ok=True)
    dst = ROOT + 'out_fix/' + stem + '.png'
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst) or os.path.getmtime(__file__) > os.path.getmtime(dst):
        cs = open(ROOT + 'tools/convert.py').read()
        g = {}
        exec(cs.split('med=np.array')[0], g)
        exec('def draw_ribbon' + cs.split('def draw_ribbon')[1].split('def process(')[0], g)
        im = Image.open(src).convert('RGBA'); g['draw_ribbon'](im, code); im.convert('RGB').save(dst)
    return dst


def rename_text(o, old, new):
    if isinstance(o, str):
        return o.replace(old, new)
    if isinstance(o, list):
        return [rename_text(x, old, new) for x in o]
    if isinstance(o, dict):
        return {k: rename_text(v, old, new) for k, v in o.items()}
    return o


def main():
    seen, products, redirects = {}, [], []
    # Kod tekrarları: BD-K04 (3 sayfa), BD-B41 (2 sayfa) -> en dolu sayfayı tut
    order = sorted(RAW, key=lambda p: (not p['images'], -len(p['prose_ls'])))
    keep = {}
    for p in order:
        c = re.sub(r'\s*Serisi$', '', p['code']).replace(' ', '')
        if c not in keep:
            keep[c] = p
    for p in RAW:
        c = re.sub(r'\s*Serisi$', '', p['code']).replace(' ', '')
        if keep[c] is not p:
            redirects.append((p['path'], keep[c]['path']))
    for p in RAW:
        c = re.sub(r'\s*Serisi$', '', p['code']).replace(' ', '')
        if keep[c] is not p:
            continue
        name, code, var = clean_name(p)
        cat = CAT_BY_LS[p['category']]
        path = p['path'].replace(' ', '')
        orig = code
        if code in RENAME:
            code = RENAME[code]
            newpath = '/' + slugify(code + '-' + name)
            redirects.append((path, newpath)); path = newpath
        if path == '/g-17/orj':
            redirects.append(('/g-17/orj', '/bd-g17/orj')); path = '/bd-g17/orj'
        stem0 = slugify(path.strip('/').replace('/', '-'))
        imgs = []
        for n, i in enumerate(p['images'], 1):
            src = img_source(i)
            if code in OWN_RIBBON:
                src = ribbon_copy(src, code, f'{stem0}-{n}')
            imgs.append(export_img(src, f'{stem0}-{n}'))
        d = parse_prose(p['prose_ls'])
        intro = ' '.join(d['intro'])
        summary = re.split(r'(?<=[.!?])\s', intro)[0] if intro else name
        products.append(dict(code=code, name=name, path=path, ls_path=p['ls_path'], cat=cat[0],
                             images=imgs, variant=var, summary=summary[:200], orig_code=orig, **d))
    # --- yeniden yazılmış metinler ---
    import glob
    RW = {}
    for f in sorted(glob.glob(ROOT + 'data/rewrite/out_*.json')):
        for x in json.load(open(f)):
            RW[re.sub(r'\s*Serisi$', '', x['code']).replace(' ', '').replace('Serisi', '')] = x
    for p in products:
        r = RW.get(p.pop('orig_code', p['code']))
        if not r:
            print('METİN YOK', p['code']); continue
        p['intro'] = r['intro']; p['feats'] = r['feats']; p['summary'] = r['summary']; p['usage'] = r.get('usage', [])
        p['notes'] = []
        for o, n2 in RENAME.items():
            if p['code'] == n2:
                for k in ('intro', 'feats', 'summary', 'usage', 'pack', 'specs', 'name'):
                    if k in p:
                        p[k] = rename_text(p[k], o, n2)
    # --- eski Sofilx'te olup Locksan kataloğunda olmayan ürünler ---
    CK = {c[0] for c in CATS}
    for n in json.load(open(ROOT + 'data/eksik_urunler.json')):
        r = RW[n['code']]
        stem = slugify(n['code'] + '-' + r['name'])
        imgs = []
        for k in range(1, len(n['imgs']) + 1):
            src = ROOT + f'out_eksik/{n["code"].lower().replace("/", "-")}-{k}.png'
            imgs.append(export_img(src, f'{stem}-{k}'))
        assert n['cat'] in CK
        products.append(dict(code=n['code'], name=r['name'], path='/' + stem, ls_path=None, cat=n['cat'], images=imgs, variant=None,
                             summary=r['summary'], intro=r['intro'], feats=r['feats'], specs=r.get('specs', []), pack=[], notes=[],
                             usage=r.get('usage', []), old_url=n['old_url']))
    json.dump(dict(products=products, cats=CATS, redirects=redirects),
              open(ROOT + 'data/urunler.json', 'w'), ensure_ascii=False, indent=1)
    print(len(products), 'ürün,', sum(len(p['images']) for p in products), 'görsel,', len(redirects), 'yönlendirme')


if __name__ == '__main__':
    main()
