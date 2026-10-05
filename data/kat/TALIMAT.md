# Kategori sayfası içeriği – yeniden yazma

Sofilx LOTO (LOTO/EKED kilitleme-etiketleme ekipmanı satan Türk firma, 2010'dan beri, İstanbul Ataşehir) için kategori sayfası içeriklerini **Türkçe ve özgün** yazıyorsun. `source` alanı başka bir sitede yayında olan metindir; Google kopya içerik saymasın diye **cümleleri, sıralamayı ve ifadeleri belirgin şekilde değiştir**, ama teknik gerçekleri (ölçüler, standartlar, ürün kodları, malzemeler) koru. Kaynakta olmayan teknik iddia, sertifika, "yerli üretim", "Ankara deposu", fiyat **uydurma** (Sofilx bir bayi/tedarikçidir, üretici değildir — "üretiyoruz" deme, "sunuyoruz/tedarik ediyoruz" de). "Locksan" asla geçmez. Ürün kodları BD- ile, sadece `products` listesinde var olan kodlar kullanılmalı (seri aralıkları "BD-G01 – G08" gibi yazılabilir).

## Girdi
`in_N.json` → `{kategori_anahtarı: {sofilx_category_name, sofilx_short, source:{...}, products:[[kod, ad], ...]}}`

## Çıktı
`out_N.json` → aynı anahtarlarla, her kategori için:
```json
{
 "lead": "hero açıklaması, 1-2 cümle, 25-45 kelime",
 "chips": ["4-5 kısa özellik, 2-5 kelime"],
 "rule_title": "kısa vurgu başlığı (ör. 'Altın kural', 'Kritik nokta')",
 "rule": "tek cümlelik altın kural/ipucu",
 "nedir_title": "X Nedir?",
 "nedir": ["2-3 paragraf, toplam 120-200 kelime; önemli terimleri **kalın** yazabilirsin"],
 "cesitler_title": "X Çeşitleri",
 "cesitler": [{"title":"…","text":"1-2 cümle","codes":["BD-…", "…"]}],   // 4-6 kart; codes: products listesinden 0-3 örnek kod
 "secim_intro": "1 cümle",
 "secim_head": ["Seri / Model", "…", "…", "Önerilen kullanım"],   // 3-4 sütun
 "secim_rows": [["BD-… veya BD-… – …", "…", "…", "…"]],  // 4-7 satır, ilk sütun ürün kodu(ları)
 "nasil_title": "Doğru X nasıl seçilir?",
 "nasil": [["Kriter", "açıklama cümlesi"]],   // 5-6 madde
 "kullanim_title": "X Nerelerde Kullanılır?",
 "kullanim": [["Alan", "1 cümle"]],    // tam 4 madde
 "faq": [["Soru?", "Cevap 1-3 cümle"]],  // 6-7 soru; fiyat sorusu varsa 'teklif için WhatsApp/telefon' de, rakam verme
 "seo_title": "kategori adıyla SEO başlığı (ör. 'Emniyet Asma Kilit Fiyatları ve Modelleri')",
 "seo": ["SEO paragrafları: 2-3 paragraf, 100-170 kelime, doğal anahtar kelimeler (EKED, LOTO, kilitleme, fiyat, model)"]
}
```
JSON'u Python ile yaz (`json.dump(..., ensure_ascii=False, indent=1)`), sonra `json.load` ile doğrula: anahtarlar tam, `codes` ve `secim_rows` ilk sütunundaki her `BD-` kodu (seri aralığının ilk kodu) products listesinde var, metinlerde "Locksan" ve "LS-" yok.
