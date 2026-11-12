# AG/OG Elektrik Güvenlik Ekipmanları kategorisini ve 5 ürünü data/urunler.json'a ekler (tekrar çalıştırılabilir)
import json, os, re, unicodedata
from PIL import Image
ROOT = '/home/claude/sofilx/'
OUT_ASSETS = ROOT + 'dist/assets/urunler/'
SRC = ROOT + 'out_elektrik/'

CAT = ['elektrik', 'AG/OG Elektrik Güvenlik Ekipmanları', 'AG/OG Elektrik Güvenlik Ekipmanları', 'ag-og-elektrik-guvenlik-ekipmanlari',
       'Hayat kurtarma ıstankası, OG kontrol kalemi, izole pense ve kablo makası gibi alçak ve orta gerilim güvenlik ekipmanları.']


def slugify(s):
    s = s.replace('ı', 'i').replace('İ', 'i').replace('–', '-')
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def export_img(src, stem):
    big, small, tiny = OUT_ASSETS + stem + '.webp', OUT_ASSETS + stem + '-k.webp', OUT_ASSETS + stem + '-s.webp'
    im = Image.open(src).convert('RGB')
    b = im.copy(); b.thumbnail((1200, 1200)); b.save(big, quality=86, method=5)
    s = im.copy(); s.thumbnail((520, 520)); s.save(small, quality=74, method=6)
    t = im.copy(); t.thumbnail((280, 280)); t.save(tiny, quality=64, method=6)
    return dict(src='/assets/urunler/' + stem + '.webp', thumb='/assets/urunler/' + stem + '-k.webp', w=b.size[0], h=b.size[1])


P = [
 dict(code='BD-E01', name='Hayat Kurtarma Istankası', n_img=2,
      summary='BD-E01 Hayat Kurtarma Istankası: elektrik çarpmasına maruz kalan kişiyi enerjili kısımdan güvenle uzaklaştırmak için 70 kV yalıtımlı, 1,75 m kurtarma çubuğu.',
      intro=['BD-E01 Hayat Kurtarma Istankası, elektrik çarpması anında kazazedeye dokunmadan onu akım kaynağından ayırmak için kullanılan yalıtımlı bir kurtarma çubuğudur. Ucundaki geniş kanca; kola, bacağa veya bele takılarak kişinin güvenli mesafeden çekilmesini sağlar.',
             'Cam elyaf takviyeli, sarı renkli gövdesi 70 kV kullanım gerilimine kadar yalıtım sağlar ve EN 60243-1 standardına göre test edilmiştir. Trafo merkezleri, OG hücreleri ve dağıtım panolarının yakınında görünür bir noktada hazır bulundurulması önerilir.'],
      feats=[['70 kV yalıtım', 'Orta gerilim tesislerinde güvenli kurtarma mesafesi sağlar.'],
             ['Geniş kanca ucu', 'Kazazedeyi kol, bacak veya gövdeden kavrayarak hızlıca çekmeye uygundur.'],
             ['Hafif gövde', '1,60 kg ağırlığıyla acil durumda tek kişi tarafından rahatça kullanılır.'],
             ['Yüksek görünürlük', 'Sarı gövde, istasyonda veya duvarda kolayca fark edilir.']],
      specs=[['Kullanım gerilimi', '70 kV'], ['Toplam boy', '1,75 m'], ['Gövde çapı', '34 mm'], ['Ağırlık', '1,60 kg'],
             ['Ürün standardı', 'EN 60243-1'], ['Kalite standardı', 'ISO 9001:2015']],
      usage=['Trafo merkezleri', 'OG / AG hücreleri', 'Dağıtım panoları', 'Enerji santralleri', 'Elektrik bakım ekipleri']),
 dict(code='BD-E02', name='AG/OG İkaz Bandı', n_img=1,
      summary='BD-E02 AG/OG İkaz Bandı: yer altı enerji kablolarının üzerine serilen, 15 cm genişliğinde, yaklaşık 500 m uzunluğunda kırmızı uyarı bandı.',
      intro=['BD-E02 AG/OG İkaz Bandı, alçak ve orta gerilim kablo güzergâhlarını işaretlemek için kablo kanalına, kablonun üzerine serilen kırmızı uyarı bandıdır. Sonraki bir kazı çalışmasında bant kablodan önce ortaya çıkar ve operatörü enerji hattına karşı uyarır.',
             'Üzerinde yıldırım sembolü ve “DİKKAT ELEKTRİK KABLOSU HATTI” baskısı bulunur. Yüksek dayanımlı plastikten üretilmiştir; toprak altında ve dış ortamda uzun süre bozulmadan kalır, rulodan kolayca serilir.'],
      feats=[['Kazı güvenliği', 'Yer altındaki enerji hattını kazı sırasında önceden fark ettirir.'],
             ['Uzun rulo', 'Yaklaşık 500 m uzunluk, uzun kablo güzergâhlarında ek yapmadan serilir.'],
             ['Dayanıklı malzeme', 'Toprak altında nem ve ısı değişimlerine karşı dirençlidir.'],
             ['Net uyarı', 'Kırmızı zemin ve elektrik sembolü uzaktan okunur.']],
      specs=[['Genişlik', '15 cm'], ['Uzunluk', 'yaklaşık 500 m'], ['Renk', 'Kırmızı, siyah baskılı'],
             ['Baskı', 'DİKKAT ELEKTRİK KABLOSU HATTI'], ['Malzeme', 'Yüksek dayanımlı plastik']],
      usage=['Yer altı kablo güzergâhları', 'Elektrik dağıtım projeleri', 'Altyapı çalışmaları', 'Kazı alanları ve şantiyeler']),
 dict(code='BD-E03', name='10–36 kV Kontrol Kalemi', n_img=2,
      summary='BD-E03 10–36 kV Kontrol Kalemi: orta gerilim hatlarında enerji varlığını güvenli mesafeden kontrol eden, teleskopik gövdeli gerilim dedektörü.',
      intro=['BD-E03 10–36 kV Kontrol Kalemi, orta gerilim hücrelerinde ve hatlarında çalışmaya başlamadan önce iletkende gerilim olup olmadığını doğrulamak için kullanılan teleskopik bir gerilim dedektörüdür. LOTO sürecinin “enerjisizliği doğrula” adımında kilitlemeden sonra mutlaka kullanılmalıdır.',
             'Teleskopik gövdesi kapalıyken 1,24 m, açıkken 1,68 m boya ulaşır; böylece kullanıcı iletkenle arasında güvenli mesafeyi korur. Kullanmadan önce kalemin çalıştığını bilinen enerjili bir noktada veya test cihazında kontrol edin.'],
      feats=[['10–36 kV aralığı', 'Dağıtım şebekelerindeki orta gerilim seviyelerine uygundur.'],
             ['Teleskopik gövde', 'Taşırken kısa, kullanırken uzun; 1,24 m’den 1,68 m’ye açılır.'],
             ['Güvenli mesafe', 'Uzun izole sap ile iletkene yaklaşmadan kontrol yapılır.'],
             ['LOTO doğrulaması', 'Kilitleme sonrası “sıfır enerji” kontrolü için kullanılır.']],
      specs=[['Kullanım gerilimi', '10–36 kV'], ['Kapalı boy', '1,24 m'], ['Açık boy', '1,68 m'], ['Ağırlık', '1,50 kg'],
             ['Kalite standardı', 'ISO 9001:2015']],
      usage=['OG hücreleri', 'Trafo merkezleri', 'Havai hatlar', 'Dağıtım şirketleri', 'Elektrik bakım ekipleri']),
 dict(code='BD-E04', name='Acil Durum Kablo Kesme Makası', n_img=1,
      summary='BD-E04 Acil Durum Kablo Kesme Makası: 15 kV kullanım gerilimi, 250 mm² kesme kapasitesi ve izole kollara sahip acil durum kablo makası.',
      intro=['BD-E04 Acil Durum Kablo Kesme Makası, yangın, sel veya kaza gibi acil durumlarda enerjiyi hızla kesmek gerektiğinde kabloyu güvenli şekilde kesmek için tasarlanmış izole kollu bir makastır. Kollarının yalıtımı 20 kV’ta test edilmiştir, 15 kV kullanım gerilimine uygundur.',
             'Ağzı 250 mm² kesite kadar bakır ve alüminyum kabloları keser. 55 cm boyundaki uzun kollar az kuvvetle yüksek kesme gücü sağlar; EN 60243-1 standardına göre test edilmiştir.'],
      feats=[['İzole kollar', '20 kV’ta test edilmiş yalıtım, 15 kV kullanım gerilimi.'],
             ['250 mm² kapasite', 'Kalın enerji kablolarını tek hamlede keser.'],
             ['Uzun kol', '55 cm kol boyu ile az kuvvetle güçlü kesim.'],
             ['Acil müdahale', 'İtfaiye, kurtarma ve enerji ekipleri için uygundur.']],
      specs=[['Kullanım gerilimi', '15 kV'], ['Test gerilimi', '20 kV'], ['Kesme kapasitesi', '250 mm²'], ['Boy', '55 cm'],
             ['Ağırlık', '3,40 kg'], ['Ürün standardı', 'EN 60243-1'], ['Kalite standardı', 'ISO 9001:2015']],
      usage=['Acil durum ve kurtarma ekipleri', 'İtfaiye', 'Enerji dağıtım ekipleri', 'Sanayi tesisleri']),
 dict(code='BD-E05', name='İzole Sigorta Çıkartma Pensesi 36 kV', n_img=1,
      summary='BD-E05 İzole Sigorta Çıkartma Pensesi 36 kV: orta gerilim hücrelerinde YG/OG sigortalarını güvenle takıp çıkarmak için 85 cm izole pense.',
      intro=['BD-E05 İzole Sigorta Çıkartma Pensesi, orta gerilim hücrelerinde ve trafo merkezlerinde YG/OG sigortalarını yuvasından güvenle çıkarmak ve yerine takmak için kullanılan izole bir pensedir. 36 kV kullanım gerilimine uygundur.',
             'Sarı yalıtımlı kolları ve 85 cm toplam boyu sayesinde kullanıcı sigortaya güvenli mesafeden müdahale eder; 40 mm çaplı gövdesi sigortayı sıkıca kavrar. Bakım öncesi enerji izolasyonunda ve sigorta değişimlerinde kullanılır.'],
      feats=[['36 kV', 'Orta gerilim hücreleri ve trafo merkezleri için uygundur.'],
             ['İzole kollar', 'Sarı yalıtımlı kollar ve kaymaz uç tutamaklar.'],
             ['Güvenli mesafe', '85 cm toplam boy ile sigortaya uzaktan müdahale.'],
             ['Sağlam kavrama', '40 mm gövde çapı sigortayı kaydırmadan tutar.']],
      specs=[['Kullanım gerilimi', '36 kV'], ['Toplam boy', '0,85 m'], ['Gövde çapı', '40 mm'], ['Ağırlık', '1,50 kg'],
             ['Kalite standardı', 'ISO 9001:2015']],
      usage=['OG hücreleri', 'Trafo merkezleri', 'Sigorta değişimi', 'Elektrik bakım ekipleri']),
]

KAT = {
 'lead': 'Sofilx LOTO; hayat kurtarma ıstankası, 10–36 kV kontrol kalemi, izole sigorta pensesi, acil durum kablo makası ve AG/OG ikaz bandı ile alçak ve orta gerilim tesislerinde LOTO sürecini tamamlayan elektrik güvenlik ekipmanlarını sunar.',
 'chips': ['36 kV’a kadar OG ekipmanı', 'Yalıtımlı ve test edilmiş', 'Gerilim kontrolü', 'Acil durum kurtarma', 'Kablo güzergâhı işaretleme'],
 'rule_title': 'Altın kural',
 'rule': 'Kilitledikten sonra mutlaka kontrol kalemiyle enerjinin kesildiğini doğrulayın; doğrulanmamış bir hat enerjili kabul edilir.',
 'nedir_title': 'AG/OG Elektrik Güvenlik Ekipmanları Nedir?',
 'nedir': ['**AG/OG elektrik güvenlik ekipmanları**, alçak gerilim (AG) ve orta gerilim (OG) tesislerinde çalışan personeli elektrik çarpmasına karşı koruyan, güvenli mesafeden müdahale imkânı veren yalıtımlı ekipmanlardır. Trafo merkezleri, OG hücreleri, dağıtım panoları ve yer altı kablo hatları bu ekipmanların başlıca kullanım alanlarıdır.',
           '**LOTO (EKED)** sürecinde enerji kesilip kilitlendikten sonra hattın gerçekten enerjisiz olduğu bir **kontrol kalemi** ile doğrulanır; sigortalar **izole sigorta pensesi** ile güvenle çıkarılır. Bir kaza anında ise **hayat kurtarma ıstankası** kazazedeyi akımdan uzaklaştırmak, **acil durum kablo makası** enerjiyi hızla kesmek için kullanılır.',
           'Sofilx LOTO, kilitleme ve etiketleme ürünlerinin yanında bu tamamlayıcı ekipmanları da tedarik ederek elektrik bakım ekiplerinin ihtiyaçlarını tek noktadan karşılar.'],
 'cesitler_title': 'AG/OG Elektrik Güvenlik Ekipmanı Çeşitleri',
 'cesitler': [
   {'title': 'Hayat kurtarma ıstankası', 'text': 'Elektrik çarpmasına maruz kalan kişiyi enerjili kısımdan güvenli mesafeden ayırmak için kullanılan yalıtımlı kancalı çubuk.', 'codes': ['BD-E01']},
   {'title': 'Gerilim kontrol kalemi', 'text': 'Orta gerilim iletkenlerinde enerji varlığını teleskopik izole sapla güvenli mesafeden kontrol eder.', 'codes': ['BD-E03']},
   {'title': 'İzole sigorta pensesi', 'text': 'OG hücrelerinde YG/OG sigortalarını güvenle takıp çıkarmak için kullanılır.', 'codes': ['BD-E05']},
   {'title': 'Acil durum kablo makası', 'text': 'Acil durumlarda enerji kablolarını izole kollarla güvenle kesmeye yarar.', 'codes': ['BD-E04']},
   {'title': 'Kablo güzergâhı ikaz bandı', 'text': 'Yer altı enerji kablolarının üzerine serilerek kazı sırasında hattı önceden fark ettirir.', 'codes': ['BD-E02']}],
 'secim_intro': 'Yapacağınız işe ve çalıştığınız gerilim seviyesine göre uygun ekipmanı tablodan seçebilirsiniz.',
 'secim_head': ['Ürün', 'Gerilim', 'Ölçü', 'Ne için kullanılır?'],
 'secim_rows': [
   ['BD-E01 – Hayat kurtarma ıstankası', '70 kV', '1,75 m', 'Kazazedeyi akımdan ayırma'],
   ['BD-E03 – 10–36 kV kontrol kalemi', '10–36 kV', '1,24 / 1,68 m', 'Enerjisizliği doğrulama'],
   ['BD-E05 – İzole sigorta çıkartma pensesi', '36 kV', '0,85 m', 'OG sigortası takma / çıkarma'],
   ['BD-E04 – Acil durum kablo kesme makası', '15 kV', '55 cm, 250 mm²', 'Acil durumda kablo kesme'],
   ['BD-E02 – AG/OG ikaz bandı', '–', '15 cm × 500 m', 'Yer altı kablo hattı işaretleme']],
 'nasil_title': 'Doğru elektrik güvenlik ekipmanı nasıl seçilir?',
 'nasil': [['Gerilim seviyesi', 'Ekipmanın kullanım gerilimi, çalıştığınız tesisin en yüksek geriliminden düşük olmamalıdır.'],
           ['Standart ve test', 'EN 60243-1 gibi standartlara göre test edilmiş, test gerilimi belirtilmiş ürünleri tercih edin.'],
           ['Güvenli mesafe', 'Sap boyu, iletkenle aranızda yeterli emniyet mesafesi bırakmalıdır.'],
           ['Periyodik kontrol', 'Yalıtımlı ekipmanları her kullanımdan önce çatlak, kir ve nem açısından gözle kontrol edin.'],
           ['Saklama', 'Ekipmanları kuru, temiz ve kolay ulaşılabilir bir noktada, tercihen duvar askısında saklayın.'],
           ['LOTO ile birlikte', 'Bu ekipmanlar kilitleme ve etiketlemenin yerine geçmez; LOTO prosedürünü tamamlar.']],
 'kullanim_title': 'AG/OG Elektrik Güvenlik Ekipmanları Nerelerde Kullanılır?',
 'kullanim': [['Trafo merkezleri ve OG hücreleri', 'Sigorta değişimi, gerilim kontrolü ve bakım öncesi enerji izolasyonu.'],
              ['Elektrik dağıtım şebekeleri', 'Havai hat ve kablo bakımlarında gerilim kontrolü ve güvenli müdahale.'],
              ['Sanayi tesisleri', 'Fabrika içi OG/AG dağıtım merkezlerinde bakım ve acil durum hazırlığı.'],
              ['Altyapı ve kazı çalışmaları', 'Yer altı kablo güzergâhlarının ikaz bandıyla işaretlenmesi.']],
 'faq': [['Kontrol kalemi LOTO sürecinde ne zaman kullanılır?', 'Enerji kesilip kilitlendikten sonra, çalışmaya başlamadan önce hattın enerjisiz olduğunu doğrulamak için kullanılır. Kalemin çalıştığı kullanımdan önce bilinen enerjili bir noktada kontrol edilmelidir.'],
         ['Hayat kurtarma ıstankası nereye konmalı?', 'Trafo merkezi, OG hücresi ve yüksek gerilim panolarının girişinde, herkesin görebileceği ve hemen ulaşabileceği bir noktada asılı tutulmalıdır.'],
         ['AG/OG ekipmanlarının fiyatları nedir?', 'Fiyat; ürüne ve sipariş adedine göre değişir. Güncel teklif ve stok bilgisi için ürün kodunu ve adedi WhatsApp hattımıza yazabilir veya teklif sepetini kullanabilirsiniz.'],
         ['Yalıtımlı ekipmanlar ne sıklıkla kontrol edilmeli?', 'Her kullanımdan önce gözle kontrol edilmeli; yalıtım testleri ise üretici önerisi ve işletmenin bakım planına göre periyodik olarak yaptırılmalıdır.'],
         ['Bu ekipmanlar kilitleme yerine kullanılabilir mi?', 'Hayır. Bu ekipmanlar LOTO sürecini tamamlar; enerji kaynağı yine kilit ve uyarı etiketiyle güvenceye alınmalıdır.']],
 'seo_title': 'AG/OG Elektrik Güvenlik Ekipmanları Fiyatları ve Modelleri',
 'seo': ['Orta gerilim tesislerinde güvenli çalışma; doğru kilitleme kadar doğru ölçüm ve müdahale ekipmanına da bağlıdır. **Hayat kurtarma ıstankası**, **OG kontrol kalemi**, **izole sigorta çıkartma pensesi** ve **acil durum kablo kesme makası**, elektrik bakım ekiplerinin temel güvenlik donanımları arasındadır.',
         'Sofilx LOTO; 36 kV’a kadar orta gerilim için yalıtımlı ekipmanları, yer altı kablo güzergâhları için **AG/OG ikaz bandını** ve tüm LOTO kilitleme ürünlerini tek noktadan tedarik eder. Toplu alımlarda kurumsal faturalı teklif hazırlıyoruz.']}

if __name__ == '__main__':
    D = json.load(open(ROOT + 'data/urunler.json'))
    D['cats'] = [c for c in D['cats'] if c[0] != 'elektrik'] + [CAT]
    D['products'] = [p for p in D['products'] if p['cat'] != 'elektrik']
    for n in P:
        stem = slugify(n['code'] + '-' + n['name'])
        imgs = [export_img(SRC + f'{n["code"].lower()}-{k}.png', f'{stem}-{k}') for k in range(1, n['n_img'] + 1)]
        D['products'].append(dict(code=n['code'], name=n['name'], path='/' + stem, ls_path=None, cat='elektrik', images=imgs, variant=None,
                                  summary=n['summary'], intro=n['intro'], feats=n['feats'], specs=n['specs'], pack=[], notes=[], usage=n['usage']))
    json.dump(D, open(ROOT + 'data/urunler.json', 'w'), ensure_ascii=False, indent=1)
    K = json.load(open(ROOT + 'data/kat/kategori_icerik.json'))
    K['elektrik'] = KAT
    json.dump(K, open(ROOT + 'data/kat/kategori_icerik.json', 'w'), ensure_ascii=False, indent=1)
    print(len(D['products']), 'ürün')
