import re, json, html as H
from html.parser import HTMLParser
MAP={'emniyet-asma-kilitler':'asma','salter-kilitleme-ekipmanlari':'salter','kablo-kilitleme-ekipmanlari':'kablo','vana-kilitleme-ekipmanlari':'vana','coklandiricilar':'coklandirici','eked-uyari-etiketleri':'etiket','eked-istasyon-modelleri':'istasyon','grup-kilitleme-kutulari-ve-eked-cantalari':'kutu','eked-setleri':'set','pnomatik-baglanti-kilitleme-ekipmanlari':'pnomatik'}
def txt(s):
    s=re.sub(r'<svg.*?</svg>','',s,flags=re.S); s=re.sub(r'<br\s*/?>',' ',s)
    return re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>','',s))).strip()
def ls2bd(s): return re.sub(r'\bLS-','BD-',s).replace('Locksan Safety','Sofilx LOTO').replace('Locksan','Sofilx')
def sec(m,id_):
    i=m.find(f'id="{id_}"')
    if i<0: return ''
    j=m.find('</section>',i); return m[i:j]
out={}
for slug,key in MAP.items():
    h=open(f'/home/claude/locksan/{slug}.html').read(); m=h[h.index('<main'):h.index('</main>')]
    d={}
    d['lead']=txt(re.search(r'<p class="lead">(.*?)</p>',m,re.S).group(1))
    d['chips']=[txt(x) for x in re.findall(r'<span><svg.*?</svg>(.*?)</span>',re.search(r'class="cat-hero-x">(.*?)</div>',m,re.S).group(1),re.S)]
    # seo prose
    pr=re.search(r'<div class="prose rv">(.*?)</div>\s*</div></section>',m,re.S)
    d['seo_prose']=txt_blocks=[ (t, txt(c)) for t,c in re.findall(r'<(h2|h3|p|li)[^>]*>(.*?)</\1>',pr.group(1),re.S)] if pr else []
    n=sec(m,'nedir')
    d['def']=txt(re.search(r'<div class="def">(.*?)</div>',n,re.S).group(1)) if 'class="def"' in n else ''
    d['nedir_title']=txt(re.search(r'<h2[^>]*>(.*?)</h2>',n,re.S).group(1)) if n else ''
    d['nedir']=[txt(p) for p in re.findall(r'<p>(.*?)</p>',re.search(r'class="gtext">(.*?)</div>',n,re.S).group(1),re.S)] if n else []
    c=sec(m,'cesitler')
    d['cesitler_title']=txt(re.search(r'<h2[^>]*>(.*?)</h2>',c,re.S).group(1)) if c else ''
    d['cesitler']=[dict(title=txt(t),text=txt(p),mods=[ls2bd(txt(a)) for a in re.findall(r'<a [^>]*>(.*?)</a>',mods or '',re.S)]) for t,p,mods in re.findall(r'<div class="gc rv"><h3>(.*?)</h3><p>(.*?)</p>(?:<div class="mods">(.*?)</div>)?',c,re.S)]
    s=sec(m,'secim')
    if s:
        d['secim_intro']=txt(re.search(r'<p>(.*?)</p>',s.split('class="seltable')[0],re.S).group(1)) if '<p>' in s.split('class="seltable')[0] else ''
        d['secim_head']=[txt(x) for x in re.findall(r'<th>(.*?)</th>',s,re.S)]
        d['secim_rows']=[[ls2bd(txt(x)) for x in re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)] for r in re.findall(r'<tr>(.*?)</tr>',s.split('<tbody>')[1],re.S)] if '<tbody>' in s else []
        d['secim_note']=txt(re.search(r'class="tnote">(.*?)</p>',s,re.S).group(1)) if 'tnote' in s else ''
    ns=sec(m,'nasil-secilir')
    d['nasil_title']=txt(re.search(r'<h2[^>]*>(.*?)</h2>',ns,re.S).group(1)) if ns else ''
    d['nasil']=[(txt(b).rstrip(':'),txt(r)) for b,r in re.findall(r'<li><b>(.*?)</b>(.*?)</li>',ns,re.S)]
    k=sec(m,'kullanim')
    d['kullanim_title']=txt(re.search(r'<h2[^>]*>(.*?)</h2>',k,re.S).group(1)) if k else ''
    d['kullanim']=[(txt(t),txt(p)) for t,p in re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>',k,re.S)]
    f=sec(m,'sss')
    d['faq']=[(txt(q),txt(a)) for q,a in re.findall(r'<summary><h3>(.*?)</h3>.*?<div class="faq-a">(.*?)</div>',f,re.S)]
    out[key]=json.loads(ls2bd(json.dumps(d,ensure_ascii=False)))
json.dump(out,open('/home/claude/sofilx/data/kat/locksan_kat.json','w'),ensure_ascii=False,indent=1)
for k,v in out.items(): print(k,len(v['chips']),len(v['nedir']),len(v['cesitler']),len(v.get('secim_rows',[])),len(v['nasil']),len(v['kullanim']),len(v['faq']),len(v['seo_prose']))
