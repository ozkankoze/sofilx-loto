# Sofilx LOTO web sitesi – çeviri talimatı

Sofilx LOTO, Türkiye'de (İstanbul) LOTO / EKED (Lockout–Tagout, kilitleme ve etiketleme) iş güvenliği ekipmanı satan bir firmadır:
emniyet asma kilitleri, şalter / devre kesici kilitleri, vana kilitleri, kablo kilitleri, çoklandırıcılar (lockout hasp), LOTO istasyonları,
grup kilit kutuları, LOTO setleri ve uyarı etiketleri. Çevireceğin metinler bu sitenin arayüzü, ürün açıklamaları, kategori yazıları ve blog yazılarıdır.

## Girdi / çıktı
- Girdi: `data/i18n/src/part-XX.json` → `{ "id": "Türkçe metin", ... }`
- Çıktı: `data/i18n/out/<dil>/part-XX.json` → **aynı id'ler**, değer = çeviri. Hiçbir id atlanmaz, yeni id eklenmez.
- Çıktı geçerli JSON olmalı (UTF-8, `ensure_ascii` kapalı). Dosyayı Python ile yaz (json.dump) ki kaçış hataları olmasın.

## Yer tutucular (çok önemli)
Metinlerde `<t1>…</t1>`, `<t2>…</t2>` gibi etiketler (kalın yazı, link vb.) ve `<x3/>` gibi tek etiketler (ikon, resim) bulunur.
- Her yer tutucuyu **aynen** koru: aynı numara, aynı sayıda, açılış/kapanış dengeli, iç içe yapı aynı.
- Cümle yapısı gerektiriyorsa sıralarını değiştirebilirsin; ama içeriklerini kendi içinde çevir.
- `&amp;`, `&lt;` gibi HTML varlıklarını olduğu gibi bırak.

## Çevrilmeyecekler
- Ürün kodları (BD-G01-RED, BD-X02CY …), ölçüler ve birimler (38 mm, DN50, 1/4"), sayılar, standart adları (OSHA 29 CFR 1910.147, ANSI, ISO/DIN, EN, IP67).
- Marka: **Sofilx**, **Sofilx LOTO**. Firma adları (referans firmalar: Tüpraş, Erdemir …), kişi adları, adresler, telefon, e-posta, alan adı.
- Ürün üzerinde basılı Türkçe yazılar (örn. "TEHLİKE – KİLİTLENDİ", "KİLİTLİ TUTMA") olduğu gibi kalabilir; gerekiyorsa yanına parantez içinde çevirisini ekle.
- "LOTO" kısaltması her dilde LOTO kalır. "EKED" Türkçe kısaltmadır (Enerji Kontrolü Etiketleme ve Kilitleme): diğer dillerde "LOTO" kullan
  (ör. "EKED / LOTO" → "LOTO"; "EKED uyarı etiketi" → "LOTO warning tag").

## Terim sözlüğü (İngilizce karşılık; diğer dillerde bu anlamı kullan)
- teklif sepeti → quote cart · teklif iste / teklif al → request a quote · fiyat al → get a price
- emniyet asma kilidi / güvenlik asma kilidi → safety padlock · kelepçe (asma kilit) → shackle
- çoklandırıcı / çoklayıcı → lockout hasp · şalter → circuit breaker / switch · devre kesici → circuit breaker · MCB → MCB
- kompakt şalter → moulded case circuit breaker (MCCB) · termik şalter → thermal overload / motor protection switch
- vana kilidi → valve lockout · küresel vana → ball valve · simit (sürgülü) vana → gate valve · kelebek vana → butterfly valve · flanşlı vana → flanged valve
- kablo kilidi → cable lockout · fiş kilidi → plug lockout · pnömatik → pneumatic
- LOTO istasyonu → lockout station · grup kilit kutusu → group lock box · uyarı etiketi → danger / warning tag
- enerji izolasyonu → energy isolation · kilitleme ve etiketleme → lockout and tagout
- stoktan aynı gün kargo → same-day shipping from stock

## Üslup
- Doğal, akıcı, profesyonel B2B satış dili; kelime kelime değil, anlam odaklı çevir. SEO için ürün/kategori adlarını o dilde aranan terimlerle yaz.
- Kısa arayüz metinlerini (buton, menü: "Anasayfa", "Ürünler", "İletişim", "Teklif sepeti", "İncele") kısa tut.
- Başlık büyük/küçük harfini kaynağa yakın tut (kaynakta Title Case ise o dilin kurallarına göre başlık biçimi).
- Arapça, Farsça, İbranice için sağdan sola dillerin doğal yazımını kullan; Latin harfli kodları olduğu gibi bırak.
- Gürcüce ve Makedonca için kendi alfabelerini kullan.
