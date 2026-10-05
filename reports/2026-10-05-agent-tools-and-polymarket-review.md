# 5 Ekim 2026 — kaynak incelemesi ve kullanım kararı

GitHub/HF API metrikleri bu tarihte sorgulandı; zamanla değişir. Makalelerdeki yıldızlar kopyalanmadı. Kanıt ve güncelleme listesi: [repo-intake JSON](2026-10-05-repo-intake.json). Excel ana listeye dört yeni repo, HF Models'a bir adaptör eklendi; Agency Agents ve SoL-Pi mevcut kayıtları güncellendi. Kategori özeti ve 10K+ görünümü ana listeden yenilendi. Model indirilmedi, üçüncü taraf kod çalıştırılmadı, canlı trading değişmedi.

| Kaynak | Kullanım kararı | Açık sınır |
|---|---|---|
| [Brewery](https://github.com/empero-org/brewery-ai) | Veri hazırlama/fine-tuning deneyi için aday | GitHub lisansı NOASSERTION; ticari uygunluk README'den varsayılmaz. GPU/sağlayıcı maliyeti ölçülmeli. |
| [Grandma's Kitchen](https://huggingface.co/empero-ai/Homebrew-Qwen3.5-2B-Grandmas-Kitchen) | İçerik üslubu demo adaptörü | HF: Qwen3.5-2B, PEFT/LoRA, Apache-2.0. Finans tahmin modeli değildir. |
| [Awesome AI Agents](https://github.com/slavakurilyak/awesome-ai-agents) | Kategoriye göre araç keşfi | Katalog, benchmark veya üretim yeterlilik belgesi değil. İçindeki her projenin lisansı ayrı. |
| [Cutter](https://github.com/rizinorg/cutter) | Yetkili ikili dosya incelemesi | GPL-3.0; dağıtım/entegrasyon lisans değerlendirmesi gerekli. Kötü niyetli dosya izole ortamda incelenmeli. |
| [LiveKit Agents](https://github.com/livekit/agents) | Sesli erişilebilir arayüz prototipi | Metin alternatifi korunmalı. Self-hosting, uzaktaki STT/LLM/TTS sağlayıcılarına ses gönderilmesini kendiliğinden önlemez. |
| [Agency Agents](https://github.com/msitarzewski/agency-agents) | Kod inceleme görevlerini rol şablonlarıyla standardize etme | Rol dosyaları çalışan bir şirket veya bağımsız doğrulanmış uzmanlık değildir. |
| [SoL-Pi](https://github.com/NVlabs/SoL-Pi) | Öncelikli çevrimdışı harness maliyet kıyası | Pi uzantısı; doğrudan Codex yaması değil. Kurulmadı, tasarruf bizim sistemimizde ölçülmedi. |

## Yerel PDF ve SoL-Pi

`2609.20519v1.pdf` metni çıkarıldı ve [arXiv kaydı](https://arxiv.org/abs/2609.20519) ile başlık/yazar/özet karşılaştırıldı. Metin çıkarıcı font uyarıları verdi; grafiklerden yeni nicel sonuç türetilmedi. Özet 51 EdgeBench görevi, Pi karşısında %44,7–49 token trafiği azalması ve yaklaşık üçte bir API maliyet düşüşü bildiriyor. Native harness ve Pi karşılaştırmaları aynı taban değildir; reklamın “yarı maliyet” ifadesi bütün iş yüklerine taşınamaz. Finansal getiri ölçülmüyor.

Uygulanabilir deney: 20 sabit, secrets içermeyen kod/log görevi; baseline ve tek mekanizma aynı model/sürümde eşlenmiş olarak çalıştırılsın. Görev başarısı, test sonucu, maliyet, gecikme ve kaybolan kanıt ölçülsün. Ham log tutulmalı; ucuz modelin alıntıları aslına göre kontrol edilmeli; doğrulama başarısızsa tam log kullanılmalı. Ayrı görülmemiş görev kümesi olmadan birden fazla optimizasyon birleştirilmesin. Bu bir deney önerisidir, tamamlanmış benchmark değildir.

## Polymarket yazılarının teknik değerlendirmesi

Paylaşılan yazılar ham veri kümesi, tarih aralığı, tüm işlem dökümü veya yeniden üretilebilir analiz sunmuyor. “50+ botun her biri ayda $100K+” ve %55/%75 gibi hesap istatistikleri bu incelemede doğrulanmadı. Cüzdanların net kazancı, yatırma/çekme, redeem/merge, komisyon, açık envanter ve teşviklerle uzlaştırılmadan kabul edilemez. İşlem geçmişi tek başına botun gizli tahmin algoritmasını kanıtlamaz.

Yararlı fikirler: fiyat seviyeleri üzerinden VWAP; kısmi dolum; aynı BTC hareketinden türeyen sinyallerin bağımlılığı; eşlenmiş/eşlenmemiş envanter; gerçek çözümleme kaynağı; sözleşme başına ücret. [Resmî ücret belgesi](https://docs.polymarket.com/trading/fees) piyasa parametreleriyle ücret hesaplanmasını açıklar; yazıdaki sabit maliyet tüm piyasalara uygulanamaz.

Matematik kontrolleri:
- Odds güncellemesindeki 1,62 ancak kalibre edilmiş likelihood ratio ise Bayesian kanıt olarak yorumlanabilir; keyfî çarpan güvenilir olasılık üretmez.
- `0.55-0.49-0.012-0.008=0.04`: pay başına 4 cent beklenen avantaj; sermaye getirisi olarak doğrudan %4 değildir. VWAP zaten spread/slippage içeriyorsa bunlar ikinci kez düşülmez.
- Aynı condition'ın birbirini tamamlayan iki outcome'u için eşlenmiş miktar `min(q_up,q_down)`; ücret öncesi eşlenmiş ödeme avantajı bu miktar × `(1-p_up-p_down)` olur. Farklı vadeler/condition'lar complete set değildir.
- İkinci bacak daha sonra alınacaksa o ana kadar arbitraj değil yön riski vardır. İki tarafta miktar tutmak kâr garantisi değildir; $1,08 maliyetli eşlenmiş set $0,08 kaybeder (diğer maliyetlerden önce).
- 98,7 cent girişte ücret öncesi başa baş kazanma olasılığı %98,7'dir. Tek tam kayıp yaklaşık 76 adet 1,3 cent kazancı siler; son saniye ve oracle riskleri belirleyicidir.
- Verilen Kelly örneği p=0,60, fiyat=0,49 ve kesir=0,20 için yaklaşık %4,31 sermaye verir; formül ücret, model belirsizliği ve korelasyonu içermez. Canlı boyut önerisi olarak benimsenmedi.

Öncelik: gerçek olay tanımı ve ücret/VWAP içeren ileri paper test. Sinyali sonuçtan önce kaydet, piyasa olasılığı baseline'ına karşı Brier ve ekonomik sonuçları ayrı ölç, veri gecikmesini ve ikinci bacak başarısızlığını simüle et. LLM'nin her tick için fiyatlama yapması yerine deterministik hesap ve sonradan kanıt incelemesi tercih edilir. Bu kaynaklar canlı risk kapılarını atlama gerekçesi değildir.

## Portföye aktarım ve gizlilik

En yakın değer: SoL-Pi ilkelerinin offline log işlerinde maliyet deneyi ve Agency Agents inceleme şablonları. LiveKit daha sonra erişilebilir destek arayüzünde denenebilir. Brewery yalnız eğitim verisi ve ölçülebilir ihtiyaç olduğunda anlamlı. Hiçbiri için gelir artışı hesaplanmış değildir. Ses, müşteri metni ve hesap logları uzak modellere gönderilmeden önce veri minimizasyonu ve sağlayıcı değerlendirmesi gerekir; bu tur yalnız herkese açık metadata kaydedildi.
