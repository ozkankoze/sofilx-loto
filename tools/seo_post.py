# Son SEO dokunuşları (tüm diller): dış linklere nofollow, linklere title
import glob, re, sys
from lxml import html as LH, etree
DIST = '/home/claude/sofilx/dist/'
n = 0
for f in glob.glob(DIST + '**/*.html', recursive=True):
    s = open(f, encoding='utf-8').read()
    doc = LH.fromstring(s)
    ch = False
    for a in doc.iter('a'):
        href = a.get('href') or ''
        if href.startswith(('http://', 'https://')) and 'sofilxloto.com' not in href:
            rel = set((a.get('rel') or '').split()) | {'nofollow', 'noopener'}
            a.set('rel', ' '.join(sorted(rel))); ch = True
        if not a.get('title'):
            t = a.get('aria-label') or re.sub(r'\s+', ' ', a.text_content()).strip()
            if not t:
                im = a.find('.//img')
                t = im.get('alt') if im is not None else ''
            if t:
                a.set('title', t[:90]); ch = True
    if ch:
        out = etree.tostring(doc, encoding='unicode', method='html', doctype='<!doctype html>')
        open(f, 'w', encoding='utf-8').write(out); n += 1
print('seo_post:', n, 'sayfa')
