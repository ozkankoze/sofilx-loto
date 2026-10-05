# Sofilx LOTO – Yeni Site

Locksan sitesiyle aynı altyapı (statik HTML/CSS/JS), ama bu sefer **sayfalar bir üreteçle oluşturuluyor**:
ürün verisi `data/urunler.json` içinde, tasarım `templates/` içinde. Bir değişiklikten sonra tek komutla tüm site yeniden üretilir.

**`dist/` klasörü yayına alınacak klasördür.** (255 sayfa + 404)

## Önizleme
**En kolayı:** `onizleme/index.html` dosyasına çift tıklayın. Site tarayıcıda açılır, tüm sayfalar ve teklif sepeti çalışır (sunucu gerekmez).

Yayındaki haline birebir bakmak isterseniz (temiz adresler, yönlendirmeler) Terminal'de:
```
cd ~/Desktop/sofilx-site && python3 onizleme.py
```
→ http://localhost:8766 açılır. (`dist/index.html`'i doğrudan açmayın; o klasör sunucu için hazırlanmıştır.)

## Klasörler
| Klasör | İçerik |
|---|---|
| `dist/` | Yayına alınacak site |
| `onizleme/` | Çift tıklayarak açılabilen önizleme kopyası (yayına yüklenmez) |
| `templates/` | Sayfa şablonları (Jinja2) |
| `dist/assets/style.css`, `site.js` | Tasarım ve davranış |
| `data/urunler.json` | 231 ürün: kod, ad, kategori, özellikler, görseller |
| `data/blog.md` | Blog yazıları (Sofilx'in mevcut 4 yazısı) |
| `brand/` | Sofilx logosu (SVG + PNG, koyu/açık zemin, ikon) |
| `gorseller/` | Dönüştürülmüş ürün görselleri (orijinal boyut) |
| `tools/` | Üreteç ve görsel dönüştürme betikleri |

## Siteyi yeniden üretmek
```
pip install jinja2 pillow
python3 tools/build.py
```

## Neler yapıldı
- Locksan'daki 184 ürün sayfası çekildi, kod tekrarları birleştirildi → 181 ürün; eski Sofilx sitesinde olup Locksan kataloğunda olmayan **50 ürün eklendi → toplam 231 ürün**. Tüm kodlar `LS-` → `BD-`.
- **Tüm ürün açıklamaları özgün olarak yeniden yazıldı** (teknik değerler korunarak); her üründe Kullanım Alanları bölümü var.
- Ürün açıklamalarından Locksan marka adı temizlendi; açıklamalar "Teknik Özellikler / Öne Çıkanlar / Paket İçeriği" olarak yapılandırıldı.
- **822 ürün görseli** (eklenen ürünlerin görselleri de aynı Sofilx çerçevesine alındı): Locksan logosu → Sofilx logosu, köşe şeridi ve görsel içindeki tüm `LS-` kodları → `BD-`, set fotoğraflarındaki çanta etiketleri → Sofilx.
  Asma kilit gövdelerinde ürünün kendisine basılı LOCKSAN yazısı (üretici baskısı) bırakıldı.
- Renk seçenekli asma kilitler (G serisi) listelerde tek kartta, ürün sayfasında renk seçicisiyle.
- **Teklif sepeti**: ziyaretçi ürünleri adetleriyle ekler, talebi WhatsApp veya e-posta ile tek seferde gönderir.
- Kodla/adla anlık ürün arama, kategori filtresi.
- SEO: her sayfada başlık/açıklama/canonical, Product + Breadcrumb + FAQ yapısal verisi, `sitemap.xml`, `robots.txt`.
- **Eski Sofilx (Wix) adresleri korunuyor**: 155 eski ürün sayfası, kategori sayfaları, blog yazıları ve Hakkımızda/İletişim yeni adreslere 301 ile yönlendiriliyor (`vercel.json`, `_redirects`, `.htaccess` hazır).

## Referanslar sayfası (`/referanslar`)
Firmalar `data/referanslar.json` içindeki `firmalar` listesinden gelir:
```
{"ad": "Firma Adı", "sektor": "kimya", "logo": "firma-adi.png"}
```
- `sektor`: enerji, metal, cimento, kimya, otomotiv, gida, ambalaj, hizmet
- `logo`: `dist/assets/referanslar/` içine konan yatay PNG/SVG (şeffaf zemin). Yazılmazsa firma adı yazı olarak görünür.
- Liste boşken logo şeridi ve firma kartları gizlenir; sayfa sektörler + teklif bölümüyle yayınlanır.
- Tasarımı örnek verilerle görmek için: `REF_DEMO=1 python3 tools/build.py` (yayına bu şekilde almayın).
Firmalar eklendikten sonra `python3 tools/build.py && python3 tools/offline.py` çalıştırın.

## Yayına almadan önce
1. **Adres**: Altınşehir Mah. Ermiş Sk. No:12A, Ümraniye / İstanbul (müşteri tarafından iletildi).
2. **Formlar** e-posta uygulamasını veya WhatsApp'ı açar (sunucu gerekmez). Mesajların doğrudan gelmesi istenirse Formspree / Netlify Forms bağlanabilir.
3. Alan adının DNS kayıtlarını yeni hostinge yönlendirin; ardından Google Search Console'a `sitemap.xml` gönderin.
