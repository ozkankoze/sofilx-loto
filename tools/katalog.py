"""Sofilx ürün kataloğu (PDF) – Chromium ile HTML->PDF"""
import json, re, html, asyncio, datetime
ROOT='/home/claude/sofilx/'; DIST=ROOT+'dist/'
D=json.load(open(ROOT+'data/urunler.json')); P=D['products']
CATS=[(c[0],c[2],c[4]) for c in D['cats']]
K=json.load(open(ROOT+'data/kat/kategori_icerik.json'))
SITE=dict(tel1='(0216) 606 32 06',tel2='(0552) 350 84 46',mail='info@sofilxloto.com',web='www.sofilxloto.com',adr='Altınşehir Mah. Ermiş Sk. No:12A, Ümraniye / İstanbul')
e=html.escape
import os
from PIL import Image
os.makedirs('/tmp/kat_img',exist_ok=True)
def img(p,i=0):
    if not p['images']: return ''
    src=DIST+p['images'][i]['thumb'].lstrip('/'); dst='/tmp/kat_img/'+os.path.basename(src).replace('.webp','.jpg')
    if not os.path.exists(dst):
        im=Image.open(src).convert('RGB'); im.thumbnail((380,380)); im.save(dst,quality=78,optimize=True)
    return 'file://'+dst
# renk gruplarını tek kartta topla
def items(ps):
    out,seen=[],set()
    for p in ps:
        v=p.get('variant')
        if v:
            if v['group'] in seen: continue
            seen.add(v['group']); g=[x for x in ps if x.get('variant') and x['variant']['group']==v['group']]
            out.append(dict(code='BD-'+v['group_range'].replace('–','/'),name=v['group_title'],img=img(p),
                specs=[s for s in p['specs'] if s[0].lower() not in ('renk',)][:3],sw=[x['variant']['color_hex'] for x in g],url=p['path']))
        else:
            out.append(dict(code=p['code'],name=p['name'],img=img(p),specs=p['specs'][:3],sw=None,url=p['path'],
                            summary=p['summary']))
    return out
logo_w=open(ROOT+'brand/sofilx-logo-beyaz.svg').read(); logo=open(ROOT+'brand/sofilx-logo.svg').read()
css=open(DIST+'assets/fonts/../style.css').read().split(':root{')[0]  # @font-face kuralları
css=css.replace('url(fonts/','url(file://'+DIST+'assets/fonts/')
year=datetime.date.today().year
pages=[]
# kapak
pages.append(f'''<section class="page cover"><div class="cv-top">{logo_w}</div>
<div class="cv-mid"><span class="eb">LOTO / EKED KİLİTLEME VE ETİKETLEME EKİPMANLARI</span><h1>Ürün<br>Kataloğu {year}</h1>
<p>Emniyet asma kilitleri, şalter ve vana kilitleri, çoklandırıcılar, LOTO istasyonları ve hazır setler. {len(P)} ürün, tek katalogda.</p></div>
<div class="cv-imgs">{''.join(f'<div><img src="{img(next(p for p in P if p["code"]==c))}"></div>' for c in ['BD-G01-RED','BD-K61','BD-D11N','BD-B102'])}</div>
<div class="cv-foot"><span>{SITE['web']}</span><span>{SITE['tel1']}</span><span>{SITE['mail']}</span></div></section>''')
# içindekiler + hakkımızda
toc=''.join(f'<li><span class="n">{i+1:02d}</span><b>{e(n)}</b><small>{sum(1 for p in P if p["cat"]==k)} ürün</small></li>' for i,(k,n,s) in enumerate(CATS))
pages.append(f'''<section class="page intro"><div class="hd">{logo}</div>
<div class="cols"><div><span class="eb r">Hakkımızda</span><h2>2010'dan beri LOTO / EKED</h2>
<p>Sofilx LOTO, endüstriyel tesislere kilitleme ve etiketleme (LOTO / EKED) ekipmanları sağlar. Bakım, onarım ve temizlik sırasında makinelerin beklenmedik şekilde çalışmasını önleyen kilitler, izolasyon cihazları, istasyonlar ve hazır setler stoktan sevk edilir.</p>
<p>Doğru ekipmanın seçiminde teknik destek veriyor; renk, etiket ve anahtar sistemi gibi kişiye özel seçeneklerle LOTO programınızı kurmanıza yardımcı oluyoruz.</p>
<ul class="why"><li><b>OSHA uyumlu</b>29 CFR 1910.147'ye uygun LOTO ekipmanı</li><li><b>Hızlı sevkiyat</b>Stoktaki ürünler aynı gün kargoda</li><li><b>Kişiye özel</b>Renk, etiket ve anahtar seçenekleri</li><li><b>Teknik destek</b>Fotoğraftan doğru ürünü birlikte seçelim</li></ul></div>
<div><span class="eb r">İçindekiler</span><h2>Kategoriler</h2><ol class="toc">{toc}</ol>
<div class="howto"><b>Nasıl sipariş verilir?</b>Ürün kodlarını ve adetleri WhatsApp ({SITE['tel2']}) ya da e-posta ({SITE['mail']}) ile iletin; fiyat ve teslim bilgisini aynı gün gönderelim.</div></div></div></section>''')
for i,(k,n,s) in enumerate(CATS):
    its=items([p for p in P if p['cat']==k]); kk=K.get(k,{})
    per=9; chunks=[its[j:j+per] for j in range(0,len(its),per)]
    for ci,ch in enumerate(chunks):
        head=f'''<div class="cat-head"><span class="n">{i+1:02d}</span><div><h2>{e(n)}</h2><p>{e(kk.get('lead',s))}</p></div></div>''' if ci==0 else f'<div class="cat-head small"><span class="n">{i+1:02d}</span><h2>{e(n)} <small>(devam)</small></h2></div>'
        cards=''
        for it in ch:
            sp=''.join(f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a,b in it['specs'])
            if not sp and it.get('summary'): sp=f'<tr><td colspan="2" class="sm">{e(it["summary"][:120])}</td></tr>'
            sw=''.join(f'<i style="background:{h}"></i>' for h in (it['sw'] or []))
            cards+=f'''<div class="card"><div class="im"><img src="{it['img']}"></div><span class="code">{e(it['code'])}</span><h3>{e(it['name'])}</h3>{f'<div class="sw">{sw}</div>' if sw else ''}<table>{sp}</table></div>'''
        pages.append(f'<section class="page cat">{head}<div class="grid">{cards}</div></section>')
pages.append(f'''<section class="page back"><div>{logo_w}</div><h2>Teklif ve bilgi için</h2>
<div class="cl"><p><b>Telefon</b>{SITE['tel1']}</p><p><b>WhatsApp</b>{SITE['tel2']}</p><p><b>E-posta</b>{SITE['mail']}</p><p><b>Web</b>{SITE['web']}</p><p><b>Adres</b>{SITE['adr']}</p></div>
<small>Ürün görselleri ve teknik değerler bilgilendirme amaçlıdır; üretici tarafından önceden haber verilmeksizin değiştirilebilir.</small></section>''')
STYLE=css+'''
@page{size:A4;margin:0}
*{box-sizing:border-box}body{margin:0;font-family:Barlow,sans-serif;color:#141414;-webkit-print-color-adjust:exact;print-color-adjust:exact}
h1,h2,h3{font-family:"Barlow Condensed";margin:0}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:16mm 14mm 18mm}
.page:not(.cover):not(.back)::after{content:"";position:absolute;left:0;right:0;bottom:0;height:9mm;background:#7a1015}
.page:not(.cover):not(.back)::before{content:"SOFİLX LOTO  ·  www.sofilxloto.com  ·  (0216) 606 32 06  ·  WhatsApp (0552) 350 84 46";position:absolute;left:14mm;bottom:2.6mm;color:#fff;font-size:8.5pt;letter-spacing:.06em;z-index:2;font-weight:500}
.cover,.back{background:linear-gradient(150deg,#c41d25 0%,#8e1218 55%,#4a0b0f 100%);color:#fff}
.cv-top svg{height:16mm;width:auto}
.cv-mid{margin-top:34mm}.eb{font-family:"Barlow Condensed";font-weight:700;letter-spacing:.2em;font-size:11pt;color:#ffd0d2}
.cv-mid h1{font-size:66pt;line-height:.92;font-weight:800;text-transform:uppercase;margin:6mm 0}
.cv-mid p{font-size:13pt;max-width:130mm;color:#ffe1e2}
.cv-imgs{position:absolute;left:14mm;right:14mm;bottom:34mm;display:grid;grid-template-columns:repeat(4,1fr);gap:5mm}
.cv-imgs div{background:#fff;border-radius:4mm;aspect-ratio:1;overflow:hidden;box-shadow:0 4mm 10mm rgba(0,0,0,.35)}.cv-imgs img{width:100%;height:100%;object-fit:cover}
.cv-imgs div:nth-child(odd){transform:rotate(-3deg)}.cv-imgs div:nth-child(even){transform:rotate(3deg)}
.cv-foot{position:absolute;left:14mm;right:14mm;bottom:14mm;display:flex;justify-content:space-between;font-family:"Barlow Condensed";font-weight:700;font-size:12pt;letter-spacing:.06em;border-top:1px solid rgba(255,255,255,.35);padding-top:4mm}
.intro .hd svg{height:11mm;width:auto}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12mm;margin-top:12mm}
.eb.r{color:#c0262d}.intro h2{font-size:26pt;text-transform:uppercase;margin:2mm 0 5mm}
.intro p{font-size:10.5pt;line-height:1.55;color:#3a3a3a}
.why{list-style:none;padding:0;margin:6mm 0 0;display:grid;gap:3mm}.why li{background:#fbf2f1;border-left:3px solid #c0262d;padding:3mm 4mm;font-size:9.5pt;color:#555}.why b{display:block;color:#141414;font-size:11pt}
.toc{list-style:none;padding:0;margin:0;display:grid;gap:2.2mm}.toc li{display:flex;align-items:center;gap:4mm;border-bottom:1px solid #ecd6d3;padding:2.2mm 0}
.toc .n{font-family:"Barlow Condensed";font-weight:800;color:#c0262d;font-size:15pt;width:9mm}.toc b{flex:1;font-size:11pt}.toc small{color:#777}
.howto{margin-top:7mm;background:#4a0b0f;color:#fff;border-radius:3mm;padding:5mm;font-size:9.5pt;line-height:1.5}.howto b{display:block;font-family:"Barlow Condensed";font-size:13pt;letter-spacing:.04em;margin-bottom:1mm}
.cat-head{display:flex;gap:5mm;align-items:center;background:linear-gradient(120deg,#c41d25,#7a1015);color:#fff;margin:-16mm -14mm 7mm;padding:10mm 14mm 8mm}
.cat-head .n{font-family:"Barlow Condensed";font-weight:800;font-size:40pt;line-height:1;opacity:.55}
.cat-head h2{font-size:24pt;text-transform:uppercase;font-weight:800}.cat-head p{margin:1mm 0 0;font-size:9.5pt;color:#ffe1e2;max-width:150mm;line-height:1.4}
.cat-head.small{padding:6mm 14mm 5mm}.cat-head.small .n{font-size:22pt}.cat-head.small h2{font-size:17pt}.cat-head small{font-weight:600;opacity:.75;font-size:11pt}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4.5mm}
.card{border:1px solid #ecd6d3;border-radius:3mm;padding:3mm;height:77mm;overflow:hidden;break-inside:avoid}
.card .im{height:33mm;display:flex;align-items:center;justify-content:center;margin-bottom:2mm}.card img{max-width:100%;max-height:33mm}
.code{display:inline-block;background:#c0262d;color:#fff;font-family:"Barlow Condensed";font-weight:700;font-size:9pt;letter-spacing:.05em;padding:.6mm 2mm;border-radius:1mm}
.card h3{font-family:Barlow;font-weight:600;font-size:8.8pt;line-height:1.22;margin:1.5mm 0 1mm;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.sw{display:flex;gap:1mm;margin-bottom:1mm}.sw i{width:3mm;height:3mm;border-radius:50%;border:1px solid rgba(0,0,0,.25)}
.card table{width:100%;border-collapse:collapse;font-size:7pt;line-height:1.25}.card td{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.card th{text-align:left;color:#777;font-weight:500;padding:.4mm 1mm .4mm 0;width:45%;vertical-align:top}.card td{padding:.4mm 0;vertical-align:top}.card td.sm{color:#555;line-height:1.3}
.back{display:flex;flex-direction:column;justify-content:center;padding:30mm 24mm}.back svg{height:16mm;width:auto}
.back h2{font-size:38pt;text-transform:uppercase;margin:14mm 0 8mm}.cl p{font-size:14pt;margin:0 0 4mm}.cl b{display:block;font-family:"Barlow Condensed";letter-spacing:.14em;font-size:10pt;color:#ffc2c5;text-transform:uppercase}
.back small{position:absolute;left:24mm;right:24mm;bottom:16mm;color:#ffc2c5;font-size:8pt}
'''
doc=f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{STYLE}</style></head><body>{"".join(pages)}</body></html>'
open(ROOT+'data/katalog.html','w').write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.goto('file://'+ROOT+'data/katalog.html'); await pg.wait_for_timeout(1500)
        await pg.pdf(path=DIST+'assets/sofilx-katalog.pdf',format='A4',print_background=True,margin=dict(top='0',bottom='0',left='0',right='0'))
        await b.close()
asyncio.run(main()); print('sayfa:',len(pages))
