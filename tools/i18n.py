# Çok dilli site üreteci
#   python3 tools/i18n.py extract  -> data/i18n/units.json (çevrilecek tüm metin birimleri)
#   python3 tools/i18n.py apply    -> dist/<dil>/... sayfalarını data/i18n/<dil>.json çevirileriyle üretir
import json, os, re, sys, hashlib, glob, copy, html as H
from lxml import html as LH, etree

ROOT = '/home/claude/sofilx/'
DIST = ROOT + 'dist/'
I18N = ROOT + 'data/i18n/'
LANGS = [('tr', 'tr', 'Türkçe'), ('en', 'gb', 'English'), ('fa', 'ir', 'فارسی'), ('he', 'il', 'עברית'), ('ar', 'sa', 'العربية'),
         ('fr', 'fr', 'Français'), ('de', 'de', 'Deutsch'), ('es', 'es', 'Español'), ('ru', 'ru', 'Русский'), ('it', 'it', 'Italiano'),
         ('nl', 'nl', 'Nederlands'), ('ka', 'ge', 'ქართული'), ('mk', 'mk', 'Македонски'), ('az', 'az', 'Azərbaycanca')]
READY = {'tr', 'en', 'fr', 'de', 'es', 'ru', 'it'}
LANGS = [l for l in LANGS if l[0] in READY]
CODES = [c for c, _, _ in LANGS if c != 'tr']
RTL = {'ar', 'fa', 'he'}
FONTS = {
    'ru': 'family=Fira+Sans:wght@400;500;600&family=Fira+Sans+Condensed:wght@600;700;800',
    'mk': 'family=Fira+Sans:wght@400;500;600&family=Fira+Sans+Condensed:wght@600;700;800',
    'ka': 'family=Noto+Sans+Georgian:wght@400;500;600;700;800',
    'ar': 'family=Noto+Kufi+Arabic:wght@500;700;800&family=Noto+Sans+Arabic:wght@400;500;600',
    'fa': 'family=Vazirmatn:wght@400;500;600;700;800',
    'he': 'family=Heebo:wght@400;500;600;700;800',
}
JS_STRINGS = ['teklif sepetine eklendi', 'Sepete git', 'Eklendi', 'Azalt', 'Adet', 'Arttır', 'Kaldır',
              'Merhaba, aşağıdaki ürünler için fiyat teklifi rica ediyorum:', 'Ad Soyad', 'Firma', 'Telefon', 'E-posta', 'Not',
              'Teklif talebi', 'ürün', 'Web sitesi mesajı', 'Dil']

INLINE = {'a', 'b', 'strong', 'i', 'em', 'span', 'small', 'br', 'code', 'sup', 'sub', 'mark', 'u', 's', 'abbr', 'img', 'time', 'svg', 'label'}
ATOMIC = {'svg', 'img', 'br', 'input', 'select', 'textarea'}
SKIP = {'script', 'style', 'noscript', 'svg', 'template'}
ATTRS = ('alt', 'title', 'placeholder', 'aria-label', 'data-name')
META = {'description', 'og:title', 'og:description', 'twitter:title', 'twitter:description', 'og:image:alt'}
LD_KEYS = {'name', 'description', 'text', 'headline', 'alternateName', 'category', 'articleSection'}
WORD = re.compile(r'[a-zçğıöşüâîû]', re.I)
LOWER = re.compile(r'[a-zçğıöşüâîû]')


def translatable(t):
    t = t.strip()
    return bool(t) and bool(LOWER.search(t)) and not t.startswith(('http', '/', '#', 'mailto:', 'tel:'))


def uid(s):
    return hashlib.sha1(s.encode()).hexdigest()[:12]


def pages():
    out = []
    for f in sorted(glob.glob(DIST + '**/*.html', recursive=True)):
        rel = f[len(DIST):]
        if rel.split('/')[0] in CODES:
            continue
        out.append(rel)
    return out


def is_inline_only(el):
    for d in el.iterdescendants():
        if not isinstance(d.tag, str):
            continue
        if d.tag not in INLINE and not any(a.tag == 'svg' for a in d.iterancestors()):
            return False
    return True


def own_text(el):
    return ''.join(el.itertext())


def encode(el):
    """innerHTML -> yer tutuculu metin; tags listesi orijinal öğeleri tutar"""
    tags = []

    def walk(e):
        s = H.escape(e.text or '', quote=False)
        for c in e:
            if not isinstance(c.tag, str):
                s += H.escape(c.tail or '', quote=False)
                continue
            tags.append(c)
            n = len(tags)
            if c.tag in ATOMIC:
                s += f'<x{n}/>'
            else:
                s += f'<t{n}>' + walk(c) + f'</t{n}>'
            s += H.escape(c.tail or '', quote=False)
        return s
    return walk(el), tags


def units_of(doc):
    """(tür, anahtar metin, konum) üretir"""
    res = []

    def visit(el):
        if not isinstance(el.tag, str) or el.tag in SKIP or el.get('data-i18n-skip') is not None:
            return
        for a in ATTRS:
            v = el.get(a)
            if v and translatable(v):
                res.append(('attr', v.strip(), (el, a)))
        if el.tag == 'meta' and (el.get('name') in META or el.get('property') in META):
            v = el.get('content')
            if v and translatable(v):
                res.append(('attr', v.strip(), (el, 'content')))
            return
        if el.tag in ('head',):
            for c in el:
                visit(c)
            return
        txt = own_text(el)
        direct = (el.text or '') + ''.join((c.tail or '') for c in el if isinstance(c.tag, str))
        has_direct = bool(WORD.search(direct)) or not any(isinstance(c.tag, str) and c.tag not in ATOMIC and WORD.search(own_text(c)) for c in el)
        if el.tag not in ('html', 'body') and translatable(txt) and is_inline_only(el) and has_direct:
            enc, tags = encode(el)
            core = enc.strip()
            if translatable(re.sub(r'<[^>]+>', '', core)):
                res.append(('html', core, (el, tags, enc)))
            # attributes inside inline children
            for d in el.iterdescendants():
                if isinstance(d.tag, str):
                    for a in ATTRS:
                        v = d.get(a)
                        if v and translatable(v):
                            res.append(('attr', v.strip(), (d, a)))
            return
        # karışık içerik: doğrudan metin düğümleri
        if el.text and translatable(el.text):
            res.append(('text', el.text.strip(), (el, 'text')))
        for c in el:
            visit(c)
            if isinstance(c.tag, str) and c.tail and translatable(c.tail) and el.tag not in SKIP:
                res.append(('text', c.tail.strip(), (c, 'tail')))
    visit(doc)
    for sc in doc.iter('script'):
        if sc.get('type') == 'application/ld+json' and sc.text:
            try:
                data = json.loads(sc.text)
            except Exception:
                continue
            for v in ld_strings(data):
                res.append(('ld', v, None))
    return res


def ld_strings(o, key=None):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from ld_strings(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from ld_strings(v, key)
    elif isinstance(o, str) and key in LD_KEYS and translatable(o):
        yield o.strip()


def parse(rel):
    return LH.fromstring(open(DIST + rel, encoding='utf-8').read())


def extract():
    os.makedirs(I18N, exist_ok=True)
    U = {}
    cnt = {}
    for rel in pages():
        doc = parse(rel)
        for kind, key, _ in units_of(doc):
            k = uid(key)
            U[k] = key
            cnt[k] = cnt.get(k, 0) + 1
    for s in JS_STRINGS:
        U[uid(s)] = s
    json.dump(U, open(I18N + 'units.json', 'w'), ensure_ascii=False, indent=0)
    words = sum(len(re.sub(r'<[^>]+>', ' ', v).split()) for v in U.values())
    print(len(U), 'birim,', words, 'kelime')


# ---------------- apply ----------------
TAG_RE = re.compile(r'<(/?)([tx])(\d+)(/?)>')


def decode(tr, tags, orig_enc):
    """çeviriyi (yer tutuculu) lxml parçalarına çevir"""
    used = set()

    def build(s):
        # s'yi metin + öğeler listesine dönüştür (özyinelemeli)
        out = []
        pos = 0
        while True:
            m = TAG_RE.search(s, pos)
            if not m:
                out.append(H.unescape(s[pos:]))
                break
            out.append(H.unescape(s[pos:m.start()]))
            closing, kind, n, selfc = m.groups()
            n = int(n)
            if kind == 'x' or selfc:
                if 1 <= n <= len(tags):
                    e = copy.deepcopy(tags[n - 1]); e.tail = None; out.append(e); used.add(n)
                pos = m.end()
                continue
            if closing:  # stray closing
                pos = m.end(); continue
            end = s.find(f'</t{n}>', m.end())
            if end < 0 or not (1 <= n <= len(tags)):
                pos = m.end(); continue
            inner = s[m.end():end]
            src = tags[n - 1]
            e = etree.Element(src.tag, dict(src.attrib))
            fill(e, build(inner))
            used.add(n)
            out.append(e)
            pos = end + len(f'</t{n}>')
        return out
    return build(tr), used


def fill(e, parts):
    e.text = ''
    last = None
    for p in parts:
        if isinstance(p, str):
            if last is None:
                e.text = (e.text or '') + p
            else:
                last.tail = (last.tail or '') + p
        else:
            e.append(p); last = p


def lead_trail(s):
    m = re.match(r'^(\s*)(.*?)(\s*)$', s, re.S)
    return m.group(1), m.group(3)


def apply_lang(lang, D, rels):
    miss = set()
    T = lambda s: D.get(uid(s.strip())) if s and s.strip() else None
    for rel in rels:
        doc = parse(rel)
        for kind, key, loc in units_of(doc):
            tr = T(key)
            if tr is None:
                miss.add(key); continue
            if kind == 'attr':
                el, a = loc; el.set(a, tr)
            elif kind == 'text':
                el, w = loc
                cur = getattr(el, w)
                a, b = lead_trail(cur)
                setattr(el, w, a + tr + b)
            elif kind == 'html':
                el, tags, enc = loc
                a, b = lead_trail(enc)
                parts, used = decode(tr, tags, enc)
                if len(used) < len(tags):  # eksik yer tutucu: atomik öğeleri (ikon) koru
                    for n, t in enumerate(tags, 1):
                        if n not in used and t.tag in ATOMIC and t.tag != 'br':
                            c = copy.deepcopy(t); c.tail = None; parts.insert(0, c)
                for c in list(el):
                    el.remove(c)
                fill(el, [a] + parts + [b])
        # JSON-LD
        for sc in doc.iter('script'):
            if sc.get('type') == 'application/ld+json' and sc.text:
                try:
                    data = json.loads(sc.text)
                except Exception:
                    continue
                sc.text = json.dumps(ld_tr(data, T, lang), ensure_ascii=False)
        fix_doc(doc, lang, rel, T)
        out = DIST + lang + '/' + rel
        os.makedirs(os.path.dirname(out), exist_ok=True)
        s = etree.tostring(doc, encoding='unicode', method='html', doctype='<!doctype html>')
        open(out, 'w', encoding='utf-8').write(s)
    return miss


def ld_tr(o, T, lang, key=None):
    if isinstance(o, dict):
        return {k: ld_tr(v, T, lang, k) for k, v in o.items()}
    if isinstance(o, list):
        return [ld_tr(v, T, lang, key) for v in o]
    if isinstance(o, str):
        if key in LD_KEYS and translatable(o):
            return T(o) or o
        if key in ('url', 'item', '@id') and o.startswith(SITE_URL):
            p = o[len(SITE_URL):] or '/'
            return SITE_URL + lpath(lang, p)
        if key == 'inLanguage':
            return lang
    return o


SITE_URL = 'https://www.sofilxloto.com'


def lpath(lang, p):
    return '/' + lang + ('' if p == '/' else p)


def fix_doc(doc, lang, rel, T):
    root = doc
    root.set('lang', lang)
    root.set('dir', 'rtl' if lang in RTL else 'ltr')
    # iç linkler
    for el in doc.iter():
        if not isinstance(el.tag, str):
            continue
        if el.get('data-l') or (el.tag == 'link' and el.get('rel') == 'alternate'):
            continue
        for a in ('href', 'data-url', 'action'):
            v = el.get(a)
            if v and v.startswith('/') and not v.startswith(('/assets/', '//')):
                el.set(a, lpath(lang, v.split('#')[0]) + (('#' + v.split('#', 1)[1]) if '#' in v else ''))
    # canonical / og:url
    for el in doc.iter('link'):
        if el.get('rel') == 'canonical':
            p = el.get('href')[len(SITE_URL):] or '/'
            el.set('href', SITE_URL + lpath(lang, p))
    for el in doc.iter('meta'):
        if el.get('property') == 'og:url':
            p = el.get('content')[len(SITE_URL):] or '/'
            el.set('content', SITE_URL + lpath(lang, p))
        if el.get('property') == 'og:locale':
            el.set('content', {'en': 'en_US', 'fa': 'fa_IR', 'he': 'he_IL', 'ar': 'ar_SA', 'fr': 'fr_FR', 'de': 'de_DE', 'es': 'es_ES',
                               'ru': 'ru_RU', 'it': 'it_IT', 'nl': 'nl_NL', 'ka': 'ka_GE', 'mk': 'mk_MK', 'az': 'az_AZ'}[lang])
    # dil seçici
    name = {c: n for c, _, n in LANGS}
    flag = {c: f for c, f, _ in LANGS}
    for el in doc.iter('a'):
        if el.get('data-l'):
            if el.get('data-l') == lang:
                el.set('aria-current', 'true')
            elif 'aria-current' in el.attrib:
                del el.attrib['aria-current']
    for b in doc.find_class('langbtn'):
        b.set('aria-label', (T('Dil') or 'Language') + ': ' + name[lang])
        img = b.find('img'); img.set('src', f'/assets/flags/{flag[lang]}.svg')
        b.find('b').text = lang.upper()
    # arama metinleri (kartlar)
    for card in doc.find_class('pc'):
        if card.get('data-s') is not None:
            t = ' '.join(card.itertext())
            card.set('data-s', re.sub(r'\s+', ' ', t).strip() + ' ' + card.get('data-s'))
    head = doc.find('head')
    # JS sözlüğü + yazı tipi
    D = {s: T(s) for s in JS_STRINGS if T(s)}
    sc = etree.SubElement(head, 'script'); sc.text = 'window.SFX_I18N=' + json.dumps(D, ensure_ascii=False) + ';'
    if lang in FONTS:
        l1 = etree.SubElement(head, 'link', rel='preconnect', href='https://fonts.gstatic.com', crossorigin='')
        l2 = etree.SubElement(head, 'link', rel='stylesheet', href=f'https://fonts.googleapis.com/css2?{FONTS[lang]}&display=swap')


def apply():
    rels = pages()
    tot = {}
    for lang in CODES:
        f = I18N + lang + '.json'
        if not os.path.exists(f):
            print('çeviri yok:', lang); continue
        D = json.load(open(f))
        miss = apply_lang(lang, D, rels)
        tot[lang] = len(miss)
        if miss:
            json.dump(sorted(miss), open(I18N + f'eksik_{lang}.json', 'w'), ensure_ascii=False, indent=0)
    print('eksik çeviri sayısı:', tot)


if __name__ == '__main__':
    {'extract': extract, 'apply': apply}[sys.argv[1]]()
