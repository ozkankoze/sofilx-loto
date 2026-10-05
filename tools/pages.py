# build.py içinden exec ile çalışır (render, SITE, cats, products, by_code, crumbs_ld, ORG kullanılabilir)
def _img(code, i=0):
    p = by_code.get(code)
    return p['images'][i]['src'] if p and p['images'] else '/assets/sofilx-ikon.svg'

ABOUT = f'''
<section class="sec"><div class="wrap split">
 <div class="prose">
  <div class="eyebrow">2010'dan beri</div>
  <h2 style="margin-top:0">Endüstride güvenli çalışmanın kilidi</h2>
  <p>SOFİLX LOTO olarak 2010 yılından bu yana endüstri sektörüne güvenlik çözümleri sunuyoruz. Kuruluşumuzdan bu yana birçok firmanın güvenlik ihtiyaçlarına yanıt vererek sektörde önemli bir yer edindik. Müşterilerimizden aldığımız olumlu geri dönüşler, kendimizi sürekli geliştirmemiz ve hizmet kalitemizi artırmamız için bize ilham veriyor.</p>
  <p>Ürünlerimiz OSHA standartlarına uygun olup en yüksek kalite ve güvenlik gereksinimlerini karşılayacak şekilde tedarik edilmektedir. Amacımız, müşterilerimizin beklentilerinin ötesinde çözümler sunarak iş yerlerinde güvenli bir çalışma ortamı oluşturmak.</p>
  <p>LOTO / EKED konusundaki uzmanlığımız ve yenilikçi yaklaşımımızla firmalara sürekli destek sağlayarak kaza ve olayları en aza indirmek için çalışıyoruz. Güvenlik kilitlerimiz ve diğer ekipmanlarımız; bakım, onarım, temizlik ve kurulum gibi süreçlerde enerjisiz çalışmayı güvenli hale getirerek çalışanlarınızın ve makinelerinizin korunmasına yardımcı olur.</p>
  <p>Siz değerli müşterilerimizin memnuniyeti ve güvenliği bizim için her zaman önceliklidir.</p>
 </div>
 <div class="hero-art" style="max-width:480px" aria-hidden="true">
  <div class="card c1"><img src="{_img('BD-X07S')}" alt="" loading="lazy"></div>
  <div class="card c2"><img src="{_img('BD-G21-RED')}" alt="" loading="lazy"></div>
  <div class="card c3"><img src="{_img('BD-D11N')}" alt="" loading="lazy"></div>
 </div>
</div></section>
<section class="stats"><div class="wrap">
 <div class="stat"><b>2010</b><span>kuruluş yılı</span></div>
 <div class="stat"><b>{len(products)}+</b><span>ürün çeşidi</span></div>
 <div class="stat"><b>OSHA</b><span>1910.147 uyumlu ürünler</span></div>
 <div class="stat"><b>Aynı gün</b><span>stoktan sevkiyat</span></div>
</div></section>
<section class="sec sec-paper"><div class="wrap">
 <div class="sec-head"><div><div class="eyebrow">Çalışma şeklimiz</div><h2>Ekipmanı seçmenize de yardım ediyoruz</h2></div></div>
 <div class="why">
  <div><svg><use href="#i-chat"/></svg><h3>1. İhtiyacı dinleriz</h3><p>Tesisinizdeki enerji kaynaklarını ve kilitleme noktalarını birlikte değerlendiririz.</p></div>
  <div><svg><use href="#i-tool"/></svg><h3>2. Doğru ekipman</h3><p>Şalter, vana ve bağlantı tiplerine uygun kilitleri ölçü ve modele göre öneririz.</p></div>
  <div><svg><use href="#i-tag"/></svg><h3>3. Net teklif</h3><p>Adetlere göre fiyat ve termin bilgisini yazılı olarak iletiriz.</p></div>
  <div><svg><use href="#i-truck"/></svg><h3>4. Hızlı teslim</h3><p>Stoktaki ürünleri aynı gün veya ertesi iş günü kargoya veririz.</p></div>
 </div>
</div></section>'''
render('page.html', '/hakkimizda', title='Hakkımızda | Sofilx LOTO', desc="2010'dan bu yana endüstriyel tesislere OSHA uyumlu LOTO / EKED kilitleme ve etiketleme ekipmanları sağlıyoruz.",
       active='about', h1='Hakkımızda', crumb='Hakkımızda', intro='Sofilx LOTO, kilitleme ve etiketleme (LOTO / EKED) ekipmanlarında uzmanlaşmış bir iş güvenliği tedarikçisidir.',
       body=ABOUT, jsonld=[ORG, crumbs_ld([('Anasayfa', '/'), ('Hakkımızda', '/hakkimizda')])])

CONTACT = f'''
<section class="sec"><div class="wrap contact">
 <div class="cinfo">
  <a href="tel:{SITE['tel1_raw']}"><svg><use href="#i-phone"/></svg><span><b>Telefon</b>{SITE['tel1']}</span></a>
  <a href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg><span><b>WhatsApp / GSM</b>{SITE['tel2']}</span></a>
  <a href="mailto:{SITE['mail']}"><svg><use href="#i-mail"/></svg><span><b>E-posta</b>{SITE['mail']}</span></a>
  <a href="https://www.google.com/maps/search/?api=1&query={'Altınşehir Mahallesi Ermiş Sokak No:12A Ümraniye İstanbul'.replace(' ', '+')}" target="_blank" rel="noopener"><svg><use href="#i-pin"/></svg><span><b>Adres</b>{SITE['address']}<br><small style="color:var(--muted)">Haritada aç →</small></span></a>
 </div>
 <div class="box" style="margin-top:0"><h2>Bize yazın</h2><div class="in">
  <form id="contact-form" class="form">
   <label>Ad Soyad<input name="ad" required autocomplete="name"></label>
   <label>Firma<input name="firma" autocomplete="organization"></label>
   <label>Telefon<input name="tel" type="tel" autocomplete="tel"></label>
   <label>E-posta<input name="eposta" type="email" autocomplete="email"></label>
   <label class="full">Mesajınız<textarea name="mesaj" rows="5" required placeholder="İhtiyacınız olan ürünler, adetler veya sorunuz…"></textarea></label>
   <div class="full" style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn btn-red" type="submit" value="mail"><svg><use href="#i-mail"/></svg>E-posta ile gönder</button><button class="btn btn-wa" type="submit" value="wa"><svg><use href="#i-wa"/></svg>WhatsApp ile gönder</button></div>
   <p class="full" style="color:var(--muted);font-size:.9rem;margin:0">Form, e-posta uygulamanızı veya WhatsApp'ı mesajınız hazır şekilde açar.</p>
  </form>
 </div></div>
</div></section>'''
render('page.html', '/iletisim', title='İletişim | Sofilx LOTO', desc='Sofilx LOTO iletişim: telefon, WhatsApp, e-posta ve adres bilgileri. LOTO / EKED ürünleri için teklif alın.',
       active='contact', h1='İletişim', intro='İhtiyacınıza en uygun çözümü sunmak ve sorularınızı yanıtlamak için buradayız.', body=CONTACT, no_cta=True,
       jsonld=[ORG, crumbs_ld([('Anasayfa', '/'), ('İletişim', '/iletisim')])])

GUIDE = f'''
<section class="sec-sm"><div class="wrap" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:48px" id="postgrid">
<article class="prose">
<p>LOTO (Lockout/Tagout), Türkçede <b>EKED – Enerji Kontrolü Etiketleme ve Kilitleme</b>, bakım ve onarım sırasında makinenin enerjisinin kesilip kilitlenmesini ve bu durumun etiketle duyurulmasını sağlayan güvenlik prosedürüdür. Bu rehberde prosedürün adımlarını ve her adımda hangi ekipmana ihtiyaç duyulduğunu özetledik.</p>
<h2>LOTO neden zorunlu?</h2>
<p>Bakım sırasında yaşanan ciddi kazaların önemli bir kısmı, kapatıldığı düşünülen bir makinenin başkası tarafından yeniden çalıştırılması ya da sistemde kalan enerjinin (basınç, yay, yerçekimi, kapasitör) beklenmedik şekilde açığa çıkmasıyla olur. ABD'de OSHA 29 CFR 1910.147 standardı, Türkiye'de ise iş ekipmanlarının kullanımına ilişkin mevzuat, işverenden bu riskleri kontrol altına alan yazılı bir enerji kontrol prosedürü bekler.</p>
<h2>Enerji kaynakları</h2>
<ul><li><b>Elektrik:</b> panolar, şalterler, devre kesiciler, fişler.</li><li><b>Mekanik:</b> dönen parçalar, yaylar, volanlar.</li><li><b>Hidrolik ve pnömatik:</b> basınçlı yağ ve hava hatları.</li><li><b>Kimyasal ve termal:</b> buhar, sıcak akışkan ve gaz hatları.</li><li><b>Yerçekimi:</b> askıda kalan yükler, presler.</li></ul>
<h2>6 adımda LOTO prosedürü</h2>
<ol>
<li><b>Hazırlık:</b> Ekipmanın tüm enerji kaynaklarını ve izolasyon noktalarını belirleyin.</li>
<li><b>Bildirim:</b> Operatörleri ve etkilenecek çalışanları duruş hakkında bilgilendirin.</li>
<li><b>Kapatma:</b> Ekipmanı normal durdurma prosedürüyle kapatın.</li>
<li><b>İzolasyon:</b> Şalterleri açın, vanaları kapatın, fişleri çekin; enerjiyi kaynağından kesin.</li>
<li><b>Kilitleme ve etiketleme:</b> Her çalışan izolasyon noktasına kendi kişisel kilidini ve üzerinde adı yazan etiketi takar.</li>
<li><b>Doğrulama:</b> Kalan enerjiyi boşaltın ve ekipmanı çalıştırmayı deneyerek sıfır enerji durumunu teyit edin.</li>
</ol>
<p>Çalışma bittiğinde kilitler yalnızca takan kişi tarafından sökülür; alan kontrol edilir ve çalışanlar bilgilendirildikten sonra enerji verilir.</p>
<h2>Hangi adımda hangi ekipman?</h2>
<ul>
<li><b>Kişisel kilit:</b> <a href="/emniyet-asma-kilitler">Emniyet asma kilitleri</a> – her çalışana kendi anahtarı olan bir kilit.</li>
<li><b>İzolasyon cihazı:</b> <a href="/salter-kilitleme-ekipmanlari">şalter kilitleri</a>, <a href="/vana-kilitleme-ekipmanlari">vana kilitleri</a>, <a href="/elektrik-pnomatik-kilitleme-ekipmanlari">fiş ve pnömatik kilitler</a>, <a href="/kablo-kilitleme-ekipmanlari">kablo kilitleri</a>.</li>
<li><b>Grup çalışması:</b> <a href="/kilit-coklandiricilar">çoklandırıcılar</a> ve <a href="/grup-kilit-kutusu">grup kilit kutuları</a>.</li>
<li><b>Bilgilendirme:</b> <a href="/tehlike-etiketleri">tehlike uyarı etiketleri</a>.</li>
<li><b>Düzen:</b> <a href="/lockout-istasyon-canta">LOTO istasyonları</a> ve <a href="/set-urunler">hazır setler</a>.</li>
</ul>
<h2>Renk kodlaması</h2>
<p>Asma kilitlerin rengi tesis içinde bir anlam taşımalıdır: örneğin kırmızı kişisel kilit, sarı bakım ekibi, mavi elektrikçiler, yeşil üretim. Önemli olan, kodlamanın yazılı prosedürde tanımlanması ve herkes tarafından bilinmesidir. Emniyet asma kilitlerimiz 8 renkte sunulur.</p>
<h2>Sık yapılan hatalar</h2>
<ul><li>Sadece etiket kullanıp kilit takmamak.</li><li>Bir kilidin anahtarının birden fazla kişide bulunması.</li><li>Doğrulama adımını atlamak.</li><li>Grup çalışmasında herkesin kendi kilidini takmaması.</li></ul>
<p>Tesisiniz için doğru ekipmanı seçmekte zorlanıyorsanız <a href="/iletisim">bize ulaşın</a>; şalter veya vana fotoğrafı üzerinden de yardımcı oluyoruz.</p>
</article>
<aside><div class="box" style="margin-top:0;position:sticky;top:100px"><h2>Hızlı başlangıç</h2><div class="in" style="display:grid;gap:10px">
<a href="{by_code['BD-X02C']['path']}" style="display:flex;gap:10px;align-items:center"><img src="{by_code['BD-X02C']['images'][0]['thumb']}" alt="" width="56" height="56" style="border:1px solid var(--line);border-radius:3px" loading="lazy"><span><b>BD-X02C</b><br><small>Kişisel güvenlik seti</small></span></a>
<a href="{by_code['BD-G01-RED']['path']}" style="display:flex;gap:10px;align-items:center"><img src="{by_code['BD-G01-RED']['images'][0]['thumb']}" alt="" width="56" height="56" style="border:1px solid var(--line);border-radius:3px" loading="lazy"><span><b>BD-G01</b><br><small>Emniyet asma kilidi</small></span></a>
<a href="{by_code['BD-K61']['path']}" style="display:flex;gap:10px;align-items:center"><img src="{by_code['BD-K61']['images'][0]['thumb']}" alt="" width="56" height="56" style="border:1px solid var(--line);border-radius:3px" loading="lazy"><span><b>BD-K61</b><br><small>Çoklandırıcı</small></span></a>
<a class="btn btn-red btn-sm" href="/urunler">Tüm ürünler</a>
</div></div></aside>
</div></section>
<style>@media(max-width:900px){{#postgrid{{grid-template-columns:1fr!important}}}}</style>'''
render('page.html', '/loto-rehberi', title='LOTO (EKED) Rehberi: 6 Adımda Kilitleme ve Etiketleme | Sofilx LOTO',
       desc='LOTO / EKED nedir, neden zorunludur ve nasıl uygulanır? 6 adımlık prosedür, enerji kaynakları, renk kodlaması ve doğru ekipman seçimi.',
       active='guide', h1='LOTO (EKED) Rehberi', intro='Kilitleme ve etiketleme prosedürünü adım adım, ihtiyaç duyacağınız ekipmanlarla birlikte anlattık.', body=GUIDE,
       og_type='article', jsonld=[crumbs_ld([('Anasayfa', '/'), ('LOTO Rehberi', '/loto-rehberi')]),
              {'@context': 'https://schema.org', '@type': 'Article', 'headline': 'LOTO (EKED) Rehberi', 'author': {'@type': 'Organization', 'name': 'Sofilx LOTO'}, 'publisher': ORG}])

CART = '''
<section class="sec"><div class="wrap split" style="align-items:start">
 <div>
  <div id="cart-empty" style="display:none;padding:28px;border:1px dashed var(--line);border-radius:var(--r);text-align:center">
   <p style="font-size:1.1rem;margin-bottom:14px">Teklif sepetiniz henüz boş.</p><a class="btn btn-red" href="/urunler">Ürünlere göz at</a></div>
  <div class="cart-list" id="cart-list"></div>
 </div>
 <div class="box" style="margin-top:0" id="cart-form-box"><h2>Teklif bilgileri</h2><div class="in">
  <form id="cart-form" class="form" onsubmit="return false">
   <label>Ad Soyad<input name="ad" autocomplete="name"></label>
   <label>Firma<input name="firma" autocomplete="organization"></label>
   <label>Telefon<input name="tel" type="tel" autocomplete="tel"></label>
   <label>E-posta<input name="eposta" type="email" autocomplete="email"></label>
   <label class="full">Not<textarea name="not" rows="3" placeholder="Teslimat yeri, anahtar sistemi, renk tercihi…"></textarea></label>
   <div class="full" style="display:flex;gap:10px;flex-wrap:wrap">
    <button class="btn btn-wa" id="send-wa" type="button"><svg><use href="#i-wa"/></svg>WhatsApp ile gönder</button>
    <button class="btn btn-ink" id="send-mail" type="button"><svg><use href="#i-mail"/></svg>E-posta ile gönder</button>
   </div>
   <button class="full" id="cart-clear" type="button" style="border:0;background:none;color:var(--muted);text-decoration:underline;justify-self:start;padding:0">Sepeti temizle</button>
  </form>
 </div></div>
</div></section>'''
render('page.html', '/teklif', title='Teklif Sepeti | Sofilx LOTO', desc='Seçtiğiniz LOTO ürünleri için tek seferde fiyat teklifi isteyin.',
       h1='Teklif sepeti', intro='Ürünleri ve adetleri kontrol edin, bilgilerinizi ekleyip talebinizi WhatsApp veya e-posta ile gönderin.', body=CART, no_cta=True)

PRIV = '''<section class="sec-sm"><div class="wrap prose">
<p>Sofilx LOTO olarak kişisel verilerinizin güvenliğine önem veriyoruz. Bu sayfa, web sitemizi kullanırken hangi bilgilerin işlendiğini açıklar.</p>
<h2>Toplanan bilgiler</h2><p>Sitemizde üyelik veya çevrim içi ödeme bulunmaz. İletişim ve teklif formları, girdiğiniz bilgileri sunucumuza kaydetmez; bilgileriniz yalnızca sizin onayınızla açılan e-posta uygulamanız veya WhatsApp üzerinden bize iletilir.</p>
<h2>Teklif sepeti</h2><p>Teklif sepetine eklediğiniz ürünler yalnızca kendi tarayıcınızda (yerel depolama) tutulur ve bize siz gönderene kadar iletilmez.</p>
<h2>Bilgilerin kullanımı</h2><p>Bize ilettiğiniz iletişim bilgileri yalnızca talebinizi yanıtlamak, teklif hazırlamak ve satış sonrası iletişim amacıyla kullanılır; üçüncü kişilerle paylaşılmaz.</p>
<h2>Haklarınız</h2><p>6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamındaki talepleriniz için <a href="mailto:info@sofilxloto.com">info@sofilxloto.com</a> adresine yazabilirsiniz.</p>
</div></section>'''
render('page.html', '/gizlilik-politikasi', title='Gizlilik Politikası | Sofilx LOTO', desc='Sofilx LOTO web sitesi gizlilik politikası ve kişisel verilerin işlenmesi.',
       h1='Gizlilik Politikası', body=PRIV, no_cta=True)

NF = '''<section class="sec"><div class="wrap" style="text-align:center">
<p style="font-family:var(--head);font-weight:800;font-size:6rem;line-height:1;color:var(--red);margin:0">404</p>
<p style="font-size:1.15rem">Aradığınız sayfa taşınmış veya kaldırılmış olabilir. Ürün kodunu arayarak bulabilirsiniz.</p>
<form action="/urunler" style="display:flex;gap:8px;justify-content:center;max-width:460px;margin:22px auto"><label class="search" style="margin:0;max-width:none"><span class="sr">Ürün ara</span><svg><use href="#i-search"/></svg><input name="q" type="search" placeholder="Ör. BD-G01"></label><button class="btn btn-red" type="submit">Ara</button></form>
<a class="btn btn-line" href="/">Anasayfaya dön</a></div></section>'''
render('page.html', '/404', title='Sayfa bulunamadı | Sofilx LOTO', desc='Aradığınız sayfa bulunamadı.', h1='Sayfa bulunamadı', body=NF)

# ---------- Referanslar ----------
_REF = json.load(open(ROOT + 'data/referanslar.json', encoding='utf-8'))
_firm = _REF['firmalar']
if os.environ.get('REF_DEMO'):  # yalnızca tasarım önizlemesi için: REF_DEMO=1 python3 tools/build.py
    _firm = [{'ad': f'Örnek Firma {i+1}', 'sektor': s['key']} for i, s in enumerate(_REF['sektorler'] * 2)]
if not _firm:
    print('UYARI: data/referanslar.json içinde firma yok – referanslar sayfasında logo bölümü gizlendi.')
render('referanslar.html', '/referanslar', title='Referanslarımız | Sofilx LOTO',
       desc='Sofilx LOTO referansları: enerji, metal, çimento, kimya, otomotiv, gıda ve ambalaj sektörlerinde LOTO / EKED kilitleme ve etiketleme çözümleri.',
       active='refs', firmalar=_firm, sektorler=_REF['sektorler'], sekmap={s['key']: s for s in _REF['sektorler']},
       jsonld=[ORG, crumbs_ld([('Anasayfa', '/'), ('Referanslar', '/referanslar')])])
