import re, json, os, glob, html
SRC='/home/claude/locksan'
MID=re.compile(r'static\.wixstatic\.com/media/([a-z0-9_]+~mv2\.(?:png|jpe?g|webp))')
def ls2bd(s): return re.sub(r'\bLS-', 'BD-', re.sub(r'\bls-', 'bd-', s))
prods=[]
for f in sorted(glob.glob(SRC+'/**/*.html', recursive=True)):
    h=open(f,encoding='utf-8').read()
    m=re.search(r'<span class="code">(.*?)</span>',h)
    if not m: continue
    path='/'+os.path.relpath(f,SRC)[:-5]
    h1=html.unescape(re.search(r'<h1>(.*?)</h1>',h,re.S).group(1))
    cat=re.search(r'<p class="pcat">Kategori: <a href="([^"]+)"[^>]*>(.*?)</a>',h)
    gal=re.search(r'<div class="gallery.*?</div>\s*</div>',h,re.S)
    imgs=[]
    g=gal.group(0) if gal else ''
    for i in MID.findall(g)+re.findall(r'(/assets/urunler/[^"?]+?)(?:-k)?\.webp',g):
        if i not in imgs: imgs.append(i)
    prose=re.search(r'<h2 class="dt">Ürün Detayı</h2><div class="prose">(.*?)</div></div>\s*</div>\s*</div>',h,re.S)
    title=re.search(r'<title>(.*?)</title>',h).group(1)
    desc=re.search(r'<meta name="description" content="(.*?)"',h)
    prods.append(dict(ls_path=path, path=ls2bd(path), ls_code=m.group(1), code=ls2bd(m.group(1)),
      name=ls2bd(h1), category=cat.group(2) if cat else None, category_path=cat.group(1) if cat else None,
      images=imgs, prose_ls=prose.group(1).strip() if prose else '', title_ls=html.unescape(title), desc_ls=html.unescape(desc.group(1)) if desc else ''))
json.dump(prods,open('/home/claude/sofilx/data/urunler_ham.json','w'),ensure_ascii=False,indent=1)
print(len(prods))
from collections import Counter
print(Counter(p['category'] for p in prods))
print(sum(len(p['images']) for p in prods), len({i for p in prods for i in p['images']}))
print([p['code'] for p in prods if not p['images']])
print([p['code'] for p in prods if not p['prose_ls']][:20])
