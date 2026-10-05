"""Sofilx LOTO statik site üreteci: data/*.json -> dist/"""
import json, os, re, html, hashlib, datetime, urllib.parse, shutil
from jinja2 import Environment, FileSystemLoader

ROOT = '/home/claude/sofilx/'
DIST = ROOT + 'dist/'
D = json.load(open(ROOT + 'data/urunler.json'))
SITE = dict(url='https://www.sofilxloto.com', tel1='(0216) 606 32 06', tel1_raw='+902166063206',
            tel2='(0552) 350 84 46', tel2_raw='+905523508446', wa='905523508446', mail='info@sofilxloto.com',
            address='Esatpaşa Mah. Bingöl Sk. No:1 A, Ataşehir / İstanbul',
            linkedin='https://www.linkedin.com/in/sofilx-loto-ekipmanlari-081818226/')
V = hashlib.md5((open(DIST + 'assets/style.css').read() + open(DIST + 'assets/site.js').read()).encode()).hexdigest()[:8]
env = Environment(loader=FileSystemLoader(ROOT + 'templates'), autoescape=True, trim_blocks=True, lstrip_blocks=True)
env.filters['urlencode'] = lambda s: urllib.parse.quote(str(s))
from markupsafe import Markup
env.filters['boldify'] = lambda s: Markup(re.sub(r'\x00(.+?)\x00', r'<b>\1</b>', str(s)))
KAT = json.load(open(ROOT + 'data/kat/kategori_icerik.json'))
AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

# eski üretimden kalan sayfaları temizle
import glob as _g
for _f in _g.glob(DIST + '**/*.html', recursive=True):
    os.remove(_f)
for _d in sorted(_g.glob(DIST + '**/', recursive=True), key=len, reverse=True):
    if _d != DIST and 'assets' not in _d and not os.listdir(_d):
        os.rmdir(_d)

# ---------- kategoriler ----------
CAT_IMG = {'asma': 'BD-G01-RED', 'salter': 'BD-D11N', 'vana': 'BD-F01', 'kablo': 'BD-L41', 'coklandirici': 'BD-K61',
           'pnomatik': 'BD-D31', 'istasyon': 'BD-B102', 'kutu': 'BD-8771B', 'set': 'BD-X02C', 'etiket': 'BD-LT05'}
CAT_LONG = {
 'asma': '<h2>Emniyet asma kilidi nasıl seçilir?</h2><p>LOTO asma kilitleri, kişisel kilitleme için tasarlanmış ve her çalışanın yalnızca kendi anahtarıyla açabildiği kilitlerdir. Elektrik işlerinde iletken olmayan <b>plastik kelepçeli</b> modeller, mekanik ve genel kullanımda <b>çelik kelepçeli</b> modeller tercih edilir. 38 mm kelepçe çoğu şalter ve vana kilidine uyarken, 76 mm kelepçe çoklandırıcı ve geniş kilitleme noktaları için uygundur.</p><p>Kilitler 8 renkte sunulur; renkleri departmana, vardiyaya veya yetki seviyesine göre kodlayabilirsiniz. Farklı anahtar (KD), aynı anahtar (KA) ve master anahtar seçenekleri için bizimle iletişime geçin.</p>',
 'salter': '<h2>Hangi şalter kilidi uygun?</h2><p>Minyatür devre kesicilerde (MCB) kolun hareketini engelleyen pim tipi veya klips tipi kilitler, kompakt şalterlerde (MCCB) kelepçeli kilitler kullanılır. Doğru modeli seçmek için şalterin marka/modelini veya kolun ölçüsünü bize iletmeniz yeterli; fotoğraf üzerinden de yardımcı oluyoruz.</p>',
 'vana': '<h2>Vana tipine göre kilitleme</h2><p>Küresel vanalarda kolu kapalı konumda sabitleyen kilitler, sürgülü (şiber) vanalarda volanı tamamen kapatan kapaklar, kelebek vanalarda kol kilitleri kullanılır. Ölçü aralıklarını ürün sayfalarındaki teknik tablolarda bulabilirsiniz.</p>',
 'kablo': '<h2>Kablo kilitleri ne zaman kullanılır?</h2><p>Birden fazla vanayı veya standart kilitlerin uymadığı düzensiz noktaları tek bir kilitleme cihazıyla güvenceye almak için ayarlanabilir kablo kilitleri idealdir. Kablo boyu ve çapı ürün sayfalarında belirtilmiştir.</p>',
 'coklandirici': '<h2>Grup kilitleme için çoklandırıcı</h2><p>Aynı enerji kaynağında birden fazla kişi çalışıyorsa, çoklandırıcı sayesinde her çalışan kendi kilidini takar; son kilit sökülmeden ekipman enerjilendirilemez. Elektrik işleri için iletken olmayan naylon modelleri öneririz.</p>',
 'pnomatik': '<h2>Fiş ve pnömatik bağlantılar</h2><p>Fişli cihazların prize takılmasını ve pnömatik hatların bağlanmasını engelleyen kilitler, taşınabilir makinelerde LOTO uygulamasının en kolay yoludur.</p>',
 'istasyon': '<h2>LOTO istasyonu neden gerekli?</h2><p>İstasyonlar kilit, etiket ve ekipmanları kullanım noktasının yakınında, görünür ve düzenli tutar. Kapaklı modeller tozlu ortamlar için, metal kabinler ağır sanayi için uygundur.</p>',
 'kutu': '<h2>Grup kilit kutusu ve çantalar</h2><p>Çok sayıda izolasyon noktası olan bakımlarda anahtarlar grup kilit kutusuna konur ve her çalışan kutuyu kendi kilidiyle kilitler. Bel çantaları ve taşınabilir çantalar ise sahada kişisel ekipmanı bir arada tutar.</p>',
 'set': '<h2>Hazır set mi, tek tek ürün mü?</h2><p>Yeni bir LOTO programı başlatıyorsanız setler, ihtiyaç duyulan kilit, etiket ve kilitleme cihazlarını tek seferde ve uyumlu şekilde sağlar. Setlerin içeriğini ihtiyacınıza göre değiştirebiliriz.</p>',
 'etiket': '<h2>Etiketleme neden önemli?</h2><p>Etiket, kilidin kime ait olduğunu, neden ve ne zaman takıldığını gösterir. Kilit fiziksel engeli, etiket ise bilgilendirmeyi sağlar; ikisi birlikte kullanılmalıdır.</p>',
}
products = D['products']
by_code = {p['code']: p for p in products}
cats = []
for key, lsname, name, slug, short in D['cats']:
    ps = [p for p in products if p['cat'] == key]
    img = by_code.get(CAT_IMG[key], ps[0])['images'][0]
    cats.append(dict(key=key, name=name, slug=slug, short=short, count=len(ps), img=img, long=CAT_LONG.get(key, ''), lsname=lsname))
cat_by_key = {c['key']: c for c in cats}

# ---------- ürünleri zenginleştir ----------
groups = {}
for p in products:
    p['catname'] = cat_by_key[p['cat']]['name']
    if p['variant']:
        groups.setdefault(p['variant']['group'], []).append(p)
for g, ps in groups.items():
    order = ['RED', 'YLW', 'BLUE', 'GRN', 'BLK', 'WHITE', 'ORJ', 'PRP']
    ps.sort(key=lambda p: order.index(p['variant']['color']))
    sw = [dict(code=p['code'], path=p['path'], hex=p['variant']['color_hex'], name=p['variant']['color_name']) for p in ps]
    for p in ps:
        p['group'] = sw
        p['swatches'] = sw
for p in products:
    p.setdefault('group', None); p.setdefault('swatches', None)
    if not p['intro']:
        n = p['name']
        if p['cat'] == 'set':
            p['intro'] = [f'{p["code"]} {n}, sahada ihtiyaç duyulan kilitleme ve etiketleme ekipmanlarını tek pakette toplayan hazır bir LOTO setidir.',
                          'Set içeriği ürün görsellerinde gösterilmiştir. Kilit adedi, renk ve anahtar sistemi gibi içerik değişiklikleri için bizimle iletişime geçebilirsiniz.']
        else:
            p['intro'] = [f'{p["code"]} {n}, {p["catname"].lower()} kategorisinde yer alan bir LOTO / EKED ekipmanıdır.',
                          'Ölçü, uyumluluk ve stok bilgisi için bizimle iletişime geçebilirsiniz.']
    p['summary'] = p['summary'] if p['summary'] and p['summary'] != p['name'] else p['intro'][0]

# ---------- blog ----------
def md(t):
    out, lst = [], None
    for line in t.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        def inl(s):
            s = html.escape(s)
            return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
        m = re.match(r'^(#{2,3})\s+(.*)', line)
        lm = re.match(r'^(?:-|\d+\.)\s+(.*)', line)
        if lm:
            tag = 'ol' if line[0].isdigit() else 'ul'
            if lst != tag:
                if lst: out.append(f'</{lst}>')
                out.append(f'<{tag}>'); lst = tag
            out.append(f'<li>{inl(lm.group(1))}</li>'); continue
        if lst:
            out.append(f'</{lst}>'); lst = None
        if m:
            n = len(m.group(1)); out.append(f'<h{n}>{inl(m.group(2))}</h{n}>')
        else:
            out.append(f'<p>{inl(line)}</p>')
    if lst: out.append(f'</{lst}>')
    return '\n'.join(out)

posts = []
raw = open(ROOT + 'data/blog.md').read().split('=== ')[1:]
COVERS = {'eked-loto-egitimi-rehberi': 'EKED – LOTO eğitimi', 'dogru-eked-ekipmaninin-onemi': 'Doğru ekipman seçimi',
          'emniyet-asma-kilitler': 'Emniyet asma kilitleri', 'is-guvenligi-temel-tasi': 'İş güvenliğinin temeli'}
for chunk in raw:
    head, body = chunk.split('\n', 1)
    slug, title, date, mins, old = [x.strip() for x in head.split('|')]
    d = datetime.date.fromisoformat(date)
    plain = re.sub(r'[#*\-]', '', body)
    posts.append(dict(slug=slug, title=title, date=date, date_tr=f'{d.day} {AYLAR[d.month-1]} {d.year}', mins=mins, old=old,
                      html=md(body), cover=COVERS.get(slug, title), desc=re.sub(r'\s+', ' ', plain.strip().split('\n')[0])[:155]))
posts.sort(key=lambda b: b['date'], reverse=True)

FAQ = [
 ('LOTO (EKED) nedir?', 'Lockout/Tagout ya da Türkçe adıyla Enerji Kontrolü Etiketleme ve Kilitleme; bakım, onarım ve temizlik sırasında makinelerin enerjisinin kesilip kilitlenerek beklenmedik şekilde çalışmasının önlendiği güvenlik prosedürüdür.'),
 ('Hangi asma kilidi seçmeliyim?', 'Elektrik işlerinde iletken olmayan plastik kelepçeli kilitler, genel kullanımda çelik kelepçeli kilitler önerilir. 38 mm kelepçe çoğu kilitleme cihazına uyar; çoklandırıcılarda 76 mm kelepçe daha rahat kullanım sağlar.'),
 ('Kilitler aynı anahtarla açılabilir mi?', 'Evet. Farklı anahtarlı (her kilit kendi anahtarı), aynı anahtarlı (bir grup kilit tek anahtar) ve master anahtarlı sistemler hazırlayabiliyoruz.'),
 ('Şalterime uygun kilidi nasıl bulurum?', 'Şalterin marka/modelini ya da net bir fotoğrafını WhatsApp üzerinden göndermeniz yeterli; uygun kilitleme ekipmanını size bildiriyoruz.'),
 ('Teslimat süresi ne kadar?', 'Stokta bulunan ürünler genellikle aynı gün veya ertesi iş günü kargoya verilir. Toplu siparişlerde termin bilgisini teklifle birlikte iletiyoruz.'),
 ('Fatura ve toplu alım yapıyor musunuz?', 'Kurumsal faturalı satış yapıyoruz; toplu alımlarda ve setlerde size özel fiyat teklifi hazırlıyoruz.'),
]

def collapse(ps):
    out, seen = [], set()
    for p in ps:
        if p['group']:
            g = p['variant']['group']
            if g in seen: continue
            seen.add(g)
            members = [by_code[s['code']] for s in p['group']]
            first = members[0]
            q = dict(first)
            q['name'] = first['variant']['group_title']
            q['code'] = first['variant']['group_range'].replace('–', '–BD-').join(['BD-', '']) if False else 'BD-' + first['variant']['group_range'].replace('–', '/')
            q['search'] = ' '.join(m['code'] + ' ' + m['variant']['color_name'] for m in members)
            q['add_code'] = first['code']; q['add_name'] = first['name']
            out.append(q)
        else:
            out.append(p)
    return out

# ---------- render yardımcıları ----------
pages = []
def render(tpl, path, **ctx):
    base = dict(site=SITE, cats=cats, total=len(products), v=V, year=datetime.date.today().year, path=path, jsonld=[], active=None)
    base.update(ctx)
    base['jsonld'] = [json.dumps(x, ensure_ascii=False) for x in base['jsonld']]
    out = env.get_template(tpl).render(**base)
    fn = DIST + ('index.html' if path == '/' else path.strip('/') + '.html')
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, 'w').write(out)
    pages.append(path)

ORG = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Sofilx LOTO', 'url': SITE['url'],
       'logo': SITE['url'] + '/assets/icon-512.png', 'email': SITE['mail'], 'telephone': SITE['tel1_raw'], 'foundingDate': '2010',
       'address': {'@type': 'PostalAddress', 'streetAddress': 'Esatpaşa Mah. Bingöl Sk. No:1 A', 'addressLocality': 'Ataşehir',
                   'addressRegion': 'İstanbul', 'addressCountry': 'TR'}, 'sameAs': [SITE['linkedin']]}
def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE['url'] + u} for i, (n, u) in enumerate(items)]}

# ---------- anasayfa ----------
def pick(codes):
    return [by_code[c] for c in codes if c in by_code]
hero = [by_code['BD-G01-RED']['images'][0]['thumb'], by_code['BD-K61']['images'][0]['thumb'], by_code['BD-B102']['images'][0]['thumb']]
sets = pick(['BD-X02C', 'BD-8773D', 'BD-X07UN', 'BD-PR-U07'])
featured = pick(['BD-G11-RED', 'BD-D11N', 'BD-F01', 'BD-L41', 'BD-K45/K46', 'BD-8812S', 'BD-LT05', 'BD-D31'])
if len(featured) < 8:
    featured += [p for p in products if p not in featured and p not in sets][:8 - len(featured)]
render('home.html', '/', title='Sofilx LOTO | LOTO / EKED Kilitleme ve Etiketleme Ekipmanları',
       desc='Emniyet asma kilitleri, şalter, vana ve kablo kilitleri, LOTO istasyonları ve setleri. 2010\'dan beri OSHA uyumlu LOTO / EKED ekipmanları, hızlı teslimat.',
       active='home', hero=hero, sets=sets, featured=featured, posts=posts, faq=FAQ,
       jsonld=[ORG, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Sofilx LOTO', 'url': SITE['url'],
                     'potentialAction': {'@type': 'SearchAction', 'target': SITE['url'] + '/urunler?q={q}', 'query-input': 'required name=q'}},
               {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
                   {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}])

# ---------- listeler ----------
def link(code):
    c = re.split(r'\s*[–-]\s*(?=[A-Z]?\d*\s*$)|\s+[–]\s+', code.strip())[0].strip()
    c = code.split(' – ')[0].split(' ')[0].strip().rstrip(',')
    if c in by_code: return by_code[c]['path']
    for p in products:
        if p['code'].startswith(c + '-') or p['code'].startswith(c + '/') or c in p['code'].split('/'):
            return p['path']
        if ('BD-' + p['code'][3:]).split('/')[0] == c: return p['path']
    return None
render('category.html', '/urunler', K=None, total_in=len(products), posts=posts, link=lambda c: None, title='Tüm LOTO / EKED Ürünleri | Sofilx LOTO',
       desc=f'{len(products)} LOTO / EKED ürünü: emniyet asma kilitleri, şalter ve vana kilitleri, çoklandırıcılar, istasyonlar ve setler.',
       h1='Tüm ürünler', intro='Kategoriye göre filtreleyin ya da ürün kodu ile arayın. Beğendiğiniz ürünleri teklif sepetine ekleyerek tek seferde fiyat isteyebilirsiniz.',
       products=collapse(products), cat=None, jsonld=[crumbs_ld([('Anasayfa', '/'), ('Ürünler', '/urunler')])])
for c in cats:
    ps = [p for p in products if p['cat'] == c['key']]
    render('category.html', '/' + c['slug'], K=KAT[c['key']], total_in=len(ps), posts=posts, link=link, title=f'{c["name"]} | Sofilx LOTO',
           desc=f'{c["short"]} {len(ps)} ürün, OSHA uyumlu, stoktan hızlı teslimat.',
           h1=c['name'], intro=c['short'] + ' Ürünleri teklif sepetine ekleyerek tek seferde fiyat isteyebilirsiniz.',
           products=collapse(ps), cat=c, og_image=c['img']['src'],
           jsonld=[crumbs_ld([('Anasayfa', '/'), ('Ürünler', '/urunler'), (c['name'], '/' + c['slug'])]),
                   {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [
                       {'@type': 'ListItem', 'position': i + 1, 'url': SITE['url'] + p['path'], 'name': f'{p["code"]} {p["name"]}'} for i, p in enumerate(ps)]}])

# ---------- ürün sayfaları ----------
for p in products:
    c = cat_by_key[p['cat']]
    same = [r for r in products if r['cat'] == p['cat'] and r is not p and not (p['group'] and r.get('group') is p['group'])]
    # benzer kodları öne al
    pre = re.match(r'BD-[A-Z]+', p['code']).group(0) if re.match(r'BD-[A-Z]+', p['code']) else 'BD-'
    same.sort(key=lambda r: (not r['code'].startswith(pre), r['code']))
    title = f'{p["code"]} {p["name"]} | Sofilx LOTO'
    if len(title) > 62: title = f'{p["code"]} {p["name"]} | Sofilx'
    if len(title) > 62: title = f'{p["code"]} {p["name"]}'
    desc = re.sub(r'\s+', ' ', p['summary'])[:150].rsplit(' ', 1)[0] + '…' if len(p['summary']) > 155 else p['summary']
    ld = {'@context': 'https://schema.org', '@type': 'Product', 'name': f'{p["code"]} {p["name"]}', 'sku': p['code'], 'mpn': p['code'],
          'category': c['name'], 'description': ' '.join(p['intro'])[:500], 'image': [SITE['url'] + im['src'] for im in p['images']],
          'brand': {'@type': 'Brand', 'name': 'Sofilx LOTO'}}
    render('product.html', p['path'], title=title, desc=desc, p=p, catobj=c, related=collapse(same)[:8], posts=posts, og_type='product',
           og_image=p['images'][0]['src'] if p['images'] else None,
           jsonld=[ld, crumbs_ld([('Anasayfa', '/'), ('Ürünler', '/urunler'), (c['name'], '/' + c['slug']), (p['code'], p['path'])])])

# ---------- blog ----------
render('blog.html', '/blog', title='Blog | Sofilx LOTO', desc='LOTO / EKED, emniyet asma kilitleri ve iş güvenliği üzerine yazılar.', active='blog', posts=posts)
for b in posts:
    render('post.html', '/blog/' + b['slug'], title=f'{b["title"]} | Sofilx LOTO', desc=b['desc'], active='blog', b=b, og_type='article', og_image='/assets/blog/' + b['slug'] + '.webp',
           others=[x for x in posts if x is not b][:3],
           jsonld=[{'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': b['title'], 'datePublished': b['date'],
                    'author': {'@type': 'Organization', 'name': 'Sofilx LOTO'}, 'publisher': ORG, 'mainEntityOfPage': SITE['url'] + '/blog/' + b['slug']},
                   crumbs_ld([('Anasayfa', '/'), ('Blog', '/blog'), (b['title'], '/blog/' + b['slug'])])])

# ---------- kurumsal sayfalar ----------
exec(open(ROOT + 'tools/pages.py').read())

# ---------- yönlendirmeler ----------
redir = [(a, b) for a, b in D['redirects']]
for a, b in [('/hakkımızda', '/hakkimizda'), ('/i-letişim', '/iletisim'), ('/ürünler', '/urunler'), ('/ürünlerimiz', '/salter-kilitleme-ekipmanlari'),
             ('/category/all-products', '/urunler'), ('/category/elektrik-devre-kesiciler', '/salter-kilitleme-ekipmanlari'),
             ('/category/kilit-çoklandırıcılar', '/kilit-coklandiricilar'), ('/category/set-ürünler', '/set-urunler'),
             ('/category/emniyetli-asma-kilitler', '/emniyet-asma-kilitler'), ('/category/elektrik-ve-pnömatik-kilitleme-ekipmanları', '/elektrik-pnomatik-kilitleme-ekipmanlari'),
             ('/category/tehlike-uyarı-etiketleri', '/tehlike-etiketleri'), ('/category/grup-kilit-kutusu', '/grup-kilit-kutusu'),
             ('/category/vana-kilitleme-ekipmanları', '/vana-kilitleme-ekipmanlari'), ('/category/lockout-i̇stasyon-çanta', '/lockout-istasyon-canta'),
             ('/category/kablo-kilitleme-ekipmanları', '/kablo-kilitleme-ekipmanlari')]:
    redir.append((a, b))
for b in posts:
    redir.append((b['old'], '/blog/' + b['slug']))
# eski Sofilx ürün sayfaları -> yeni ürün (SKU eşleştirme)
old = json.load(open(ROOT + 'data/sofilx-icerik.json'))
norm = lambda s: re.sub(r'[^A-Z0-9]', '', s.upper().replace('LS-', 'BD-').replace('BD-', ''))
code_idx = {norm(p['code']): p for p in products}
base_idx = {}
for p in products:
    base_idx.setdefault(norm(re.sub(r'-(RED|YLW|BLUE|GRN|BLK|WHITE|ORJ|PRP)$', '', p['code'])), p)
    for part in p['code'].replace('BD-', '').split('/'):
        base_idx.setdefault(norm(part), p)
KW = [('istasyon', 'lockout-istasyon-canta'), ('kutu', 'grup-kilit-kutusu'), ('asma kilit', 'emniyet-asma-kilitler'), ('vana', 'vana-kilitleme-ekipmanlari'), ('çoklandırıcı', 'kilit-coklandiricilar'),
      ('çoklayıcı', 'kilit-coklandiricilar'), ('kablo', 'kablo-kilitleme-ekipmanlari'), ('istasyon', 'lockout-istasyon-canta'),
      ('dolab', 'lockout-istasyon-canta'), ('kutu', 'grup-kilit-kutusu'), ('çanta', 'grup-kilit-kutusu'), ('torba', 'grup-kilit-kutusu'),
      ('set', 'set-urunler'), ('kit', 'set-urunler'), ('etiket', 'tehlike-etiketleri'), ('şalter', 'salter-kilitleme-ekipmanlari'),
      ('kesici', 'salter-kilitleme-ekipmanlari'), ('pnömatik', 'elektrik-pnomatik-kilitleme-ekipmanlari'), ('fiş', 'elektrik-pnomatik-kilitleme-ekipmanlari'),
      ('silindir', 'elektrik-pnomatik-kilitleme-ekipmanlari'), ('emniyet kilidi', 'emniyet-asma-kilitler')]
base_idx[norm('L1010-ELK-SET')] = by_code['BD-8773D']
unmatched = []
for o in old:
    if '/product-page/' not in o['u']:
        continue
    sku, name = None, ''
    for l in o.get('ld', []):
        if '"Product"' in l:
            try:
                j = json.loads(l); sku = j.get('sku'); name = j.get('name', '')
            except Exception:
                pass
    cands = []
    for c0 in [sku or ''] + re.findall(r'BD-[A-Z0-9\-]+', name.upper()) + re.findall(r'bd-[a-z0-9\-]+$', o['u']):
        for part in c0.split('/'):
            part = part.strip()
            cands += [part, re.sub(r'DP$', '', part), re.sub(r'(-1|PLUS| PLUS)$', '', part)]
    target = None
    for cnd in cands:
        k = norm(cnd)
        if k and k in code_idx: target = code_idx[k]['path']; break
        if k and k in base_idx: target = base_idx[k]['path']; break
    if not target:
        low = name.lower()
        target = next(('/' + c for kw, c in KW if kw in low), '/urunler')
        unmatched.append((o['u'], sku, name, target))
    redir.append((o['u'], target))
json.dump(unmatched, open(ROOT + 'data/eslesmeyen_eski_urunler.json', 'w'), ensure_ascii=False, indent=1)

def enc(u):
    return urllib.parse.quote(u, safe='/-_.~')
seen = set(); R = []
for a, b in redir:
    if a in seen or a == b:
        continue
    seen.add(a); R.append((a, b))
vercel = {'cleanUrls': True, 'trailingSlash': False,
          'redirects': [{'source': enc(a), 'destination': b, 'permanent': True} for a, b in R],
          'headers': [{'source': '/assets/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=604800'}]}, {'source': '/assets/fonts/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=31536000, immutable'}]}]}
json.dump(vercel, open(DIST + 'vercel.json', 'w'), ensure_ascii=False, indent=1)
open(DIST + '_redirects', 'w').write('\n'.join(f'{enc(a)}  {b}  301' for a, b in R) + '\n')
ht = ['Options -MultiViews', 'RewriteEngine On', 'RewriteCond %{HTTPS} off [OR]', 'RewriteCond %{HTTP_HOST} !^www\\. [NC]',
      'RewriteRule ^ https://www.sofilxloto.com%{REQUEST_URI} [L,R=301]']
for a, b in R:
    ht.append(f'RewriteRule ^{re.escape(enc(a).lstrip("/"))}$ {b} [R=301,L,NE]')
ht += ['RewriteCond %{REQUEST_FILENAME} !-f', 'RewriteCond %{REQUEST_FILENAME}.html -f', 'RewriteRule ^(.+)$ $1.html [L]',
       'ErrorDocument 404 /404.html', '<IfModule mod_expires.c>', 'ExpiresActive On', 'ExpiresByType image/webp "access plus 1 year"',
       'ExpiresByType text/css "access plus 1 year"', 'ExpiresByType application/javascript "access plus 1 year"',
       'ExpiresByType font/woff2 "access plus 1 year"', '</IfModule>']
open(DIST + '.htaccess', 'w').write('\n'.join(ht) + '\n')

# ---------- sitemap / robots / manifest ----------
today = datetime.date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for pth in pages:
    if pth in ('/404', '/teklif'):
        continue
    sm.append(f'  <url><loc>{SITE["url"]}{"" if pth == "/" else enc(pth)}</loc><lastmod>{today}</lastmod></url>')
sm.append('</urlset>')
open(DIST + 'sitemap.xml', 'w').write('\n'.join(sm) + '\n')
open(DIST + 'robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /teklif\n\nSitemap: {SITE["url"]}/sitemap.xml\n')
json.dump({'name': 'Sofilx LOTO', 'short_name': 'Sofilx', 'start_url': '/', 'display': 'standalone', 'background_color': '#ffffff',
           'theme_color': '#141414', 'icons': [{'src': '/assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                               {'src': '/assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]},
          open(DIST + 'site.webmanifest', 'w'), ensure_ascii=False)
print(f'{len(pages)} sayfa, {len(R)} yönlendirme, eşleşmeyen eski ürün: {len(unmatched)}')
