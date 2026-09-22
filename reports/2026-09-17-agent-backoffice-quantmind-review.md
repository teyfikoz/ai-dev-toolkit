# Agent, backoffice ve QuantMind: kaynak doğrulama raporu

İnceleme tarihi: 17 Eylül 2026. Yöntem: birincil yayınlar, sabitlenmiş GitHub kaynakları ve belirtilen yerel uygulama dosyalarının salt okunur incelemesi. Üçüncü taraf kod kurulmadı veya çalıştırılmadı; hesap bağlantısı, finansal işlem ve üretim değişikliği yapılmadı. Bu rapor statik inceleme sonuçlarını aktarır; performans testi veya klinik doğrulama değildir.

Karar: QuantMind'in kaynaklı bilgi çıkarımı yaklaşımı araştırma ekranında kullanılabilir. Otonom işlem, kanıtlanmış alpha veya hazır backoffice güvenliği iddiaları mevcut kanıtı aşıyor. Yeni yerel skill dosyaları uygulama talimatıdır; dağıtılmış ve bütün araçlara uygulanan runtime güvenlik kapıları değildir.

## QuantMind: alınacak yaklaşım ve entegrasyon sınırı

İncelenen sürüm: [`LLMQuant/quant-mind@10e9dbd0c7254edc5a091b852122ebe72e06092a`](https://github.com/LLMQuant/quant-mind/tree/10e9dbd0c7254edc5a091b852122ebe72e06092a), 15 Ağustos 2026. `quantmind/` altındaki 63 Python dosyası statik olarak tarandı.

Depo makale/haber işleme, tipli ve kaynaklı bilgi üretimi, arama ve RAG sunuyor. `PaperFlow`, `collect_news` ve `batch_run` mevcut. Kendi konumlandırması finansal bilgi çıkarımı için coding-agent çalışma ortamı; hazır bir strateji, backtest veya broker yürütme motoru değil. `Factor` sınıfı açıkça stub ve PnL/IC/turnover alanları geleceğe bırakılmış. [Konumlandırma](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/contexts/design/positioning.md#L17), [Factor kodu](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/quantmind/knowledge/factor.py#L1).

Kaynak sürümü, içerik hash'i, sayfa referansı ve alıntı doğrulaması değerli tasarım örnekleri. Buna rağmen kaynakta bulunan bir alıntı, LLM yorumunun doğruluğunu kanıtlamaz. Bilgi kalitesi ve agent çalışma ortamı benchmark'ları tasarım aşamasında; güncel belge ölçülmüş değerlendirme sonucu iddia etmiyor. [Kaynak/artefakt modelleri](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/quantmind/knowledge/paper.py), [değerlendirme durumu](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/contexts/design/positioning.md#L40).

| Kod bulgusu | OCC için sonuç |
|---|---|
| SQLite kütüphanesinin varsayılan embedding sağlayıcısı metinleri OpenAI API'sine gönderiyor. | Yerel kayıt, çevrimdışı işleme garantisi vermez. İlk kapsam yalnızca izinli kamu verisi olmalı. [Embedding çağrısı](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/quantmind/library/_internal/index_embeddings.py#L33). |
| `tracing_disabled=False`, `trace_include_sensitive_data=True`. | Trace kapatılmadan kullanıcı veya özel şirket verisi bağlanmamalı. SDK varsayılan exporter'ı OpenAI backend'ine gönderir. [Config](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/quantmind/configs/base.py#L31), [SDK tracing](https://openai.github.io/openai-agents-python/tracing/#custom-tracing-processors). |
| `max_total_cost_usd`, `max_total_input_tokens`, `enable_default_guardrails` tanımlı; taranan runtime dosyalarında bu alanları uygulayan kullanım bulunmadı. | İsimleri maliyet veya güvenlik koruması olarak sunulamaz; sınırları çağıran uygulama uygular. [Alanlar](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/quantmind/configs/base.py#L38). |
| Trajectory arşivleme fonksiyonu no-op. | `archive_trajectory=True` kalıcı ve tamamlanmış denetim kaydı garantisi değildir. [Runner](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/quantmind/flows/_runner.py#L126). |
| HTTP fetcher serbest URL kabul ediyor ve redirect izliyor. | Public Express endpoint'ine bağlanırken izinli kaynaklar ve hedef IP/redirect kontrolü gerekir. Bu, mevcut depoda gösterilmiş bir istismar iddiası değildir. [Fetcher](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/quantmind/preprocess/fetch/http.py#L102). |
| `magic.py` tipli input/config çözümlüyor; taranan çekirdekte `eval`, `exec`, `subprocess` bulunmadı. | Kütüphaneyi kendiliğinden üretilen kodu çalıştıran bir motor diye tanımlamak hatalı. Harici coding-agent workflow'unda üretilen kodun yürütülmesi ayrı bir yetki ve izolasyon konusudur. [Magic](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/quantmind/magic.py#L70). |

Repo MIT ve Python ≥3.10 kullanıyor; OpenAI Agents, LiteLLM, LlamaIndex, LiteParse ve PyMuPDF bağımlılıkları var. Üst deponun MIT lisansı bağımlılık lisanslarını değiştirmez: zorunlu bağımlılık olarak listelenen PyMuPDF AGPL/ticari çift lisanslıdır. Kapalı SaaS'a paket halinde almadan önce hangi parser'ın gerçekten kullanılacağı ve dağıtım koşulları çözülmeli. [MIT](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/LICENSE), [bağımlılıklar](https://github.com/LLMQuant/quant-mind/blob/10e9dbd0c7254edc5a091b852122ebe72e06092a/pyproject.toml#L7), [PyMuPDF resmi lisans açıklaması](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright).

Önerilen OCC sınırı: React/Express araştırma ekranı → kontrollü kamu kaynağı toplama → kaynaklı JSON artefaktları → açıkça etiketlenmiş sentetik simülasyon. Gözlem, model tahmini, tarihsel backtest ve sentetik eğitim çıktısı ayrı veri türleri olmalı. LLM yorumu istatistiksel test sonucu değildir. Bu rapor böyle bir entegrasyonun kurulduğunu iddia etmez.

## Claude'un nicel iddialarındaki düzeltmeler

| İddia | Kanıta uygun düzeltme |
|---|---|
| `t > 3.0` DSR'dir. | Yanlış. 3.0 eşiği Harvey–Liu–Zhu'nun faktörlerde çoklu test çalışmasıyla ilişkilidir. DSR, Sharpe için deneme sayısı/bağımlılığı, denemeler arası dağılım, örneklem uzunluğu, çarpıklık ve basıklığı hesaba katar; tek sabit t eşiği değildir. [Harvey–Liu–Zhu](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF), [DSR](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf). |
| Üç test penceresi yeterli doğrulamadır. | Evrensel üç pencere kuralı yok. Veri miktarı, bağımlılık, rejimler, aranan aday sayısı ve holdout'un tekrar kullanılması sonucu değiştirir. Önceden ayrılmış bir holdout'u gördükten sonra yeniden ayarlamak bağımsız kanıt üretmez. [Backtest overfitting çalışması](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf). |
| Heston ile IV–RV farkı risksiz arbitrajdır. | Heston bir stokastik volatilite fiyatlama modelidir. Opsiyonların risk nötr beklentisi ile fiziksel ölçü altındaki beklenen/gerçekleşen varyans farklıdır; fark risk primi ve model/tahmin hatası içerebilir. İleri dönemde gerçekleşecek varyans işlem anında bilinmez. Maliyet, hedge ve kuyruk riskleri yok sayılarak arbitraj sonucu çıkarılamaz. [Volatilite risk primi araştırması](https://www.federalreserve.gov/pubs/feds/2004/200456/200456pap.pdf). |
| Hawkes `alpha/beta` doğrudan cascade veya alpha sinyalidir. | Parametrizasyona bağlıdır: `φ(t)=α exp(-βt)` için integral `α/β`, `φ(t)=αβ exp(-βt)` için `α`. Çok değişkenli modelde integral matrisinin spektral yarıçapı önemlidir. Olay yoğunluğu/kümelenmesi, fiyat yönü veya kârlılık kanıtı değildir. [Bacry–Mastromatteo–Muzy](https://arxiv.org/html/1502.04592). |

Araştırma raporunda adayların sayısı, zaman kesimi, kaynak erişilebilirlik zamanı, maliyet varsayımları ve örneklem dışı sonuçlar kaydedilmeden getiri iddiası yapılmamalı. Ölçülmüş MRR veya yatırım getirisi etkisi bu incelemeden çıkarılamaz.

## Fly-high: simülasyon örneği

İncelenen sürüm: [`immortalhowwl/fly-high@70b8a9ef6832f7b6ffab81980ee0047c8eaa1d4d`](https://github.com/immortalhowwl/fly-high/tree/70b8a9ef6832f7b6ffab81980ee0047c8eaa1d4d), 15 Eylül 2026. Güncel README cüzdan bağlantısı, private key veya canlı emir içermeyen yerel paper-trading laboratuvarı olarak tanımlar. Varsayılan demo sentetik; sabit arşiv oynatımı sürekli çalışan trading değildir. [README](https://github.com/immortalhowwl/fly-high/blob/70b8a9ef6832f7b6ffab81980ee0047c8eaa1d4d/README.md#L7).

Kod ücret, slippage, likidite sınırı ve son %30 kronolojik holdout içeriyor. Ancak README örneğinde sadece 351 mum bulunuyor; tarihsel likidite ölçülmemiş, açık bir varsayım. Champion örnek holdout'ta hiç işlem yapmıyor. Wallet-inspired retrospective yolunda `holdout` alanının gerçekten görülmemiş kanıt olmadığı ayrıca belirtiliyor. Soy ağacı ve finite replay arayüzü referans alınabilir; kârlı genelleme kanıtı olarak sunulamaz. [Veri sınırları](https://github.com/immortalhowwl/fly-high/blob/70b8a9ef6832f7b6ffab81980ee0047c8eaa1d4d/README.md#L58), [simülatör](https://github.com/immortalhowwl/fly-high/blob/70b8a9ef6832f7b6ffab81980ee0047c8eaa1d4d/flyhigh/engine.py#L35), [retrospective sınırlaması](https://github.com/immortalhowwl/fly-high/blob/70b8a9ef6832f7b6ffab81980ee0047c8eaa1d4d/flyhigh/hypothesis_replay.py#L26).

## Backoffice ve model güvenilirliği

| İddia/konu | Doğrulanan kapsam |
|---|---|
| Astra %88.0 / %99.2 başarı | Bir/dört denemedeki SRE-Bench binary reverse-engineering sonucudur; fatura veya CRM işlemlerinin başarı oranı değildir. [OpenAI model duyurusu](https://openai.com/index/gpt-6-astra/). |
| ARC %99.9 ve daha düşük maliyet | Provider Adapter/high için %99.9 ve $18,817; Standard/max için %62.7 ve $26,098 raporlanır. Hem harness hem effort farklıdır. Bunlar benchmark toplamlarıdır, sıradan görev fiyatı değildir. [ARC Prize](https://arcprize.org/blog/astra). |
| SMELT, Astra'nın iç döngülerini kanıtlar | SMELT çalışması belirli MoE training koşullarında %6.8–18.0 FLOP tasarrufu bildirir; Astra mimarisi veya inference tasarrufu kanıtı değildir. Resmi kaynaklarda Astra'nın 4–64 iç döngüsü doğrulanmadı. [SMELT](https://arxiv.org/abs/2609.01343), [Astra sistem kartı](https://deploymentsafety.openai.com/gpt-6-astra). |
| Prompt injection %23.6 → %11.2 | Claude in Chrome autonomous-mode pilotundaki 123 test/29 senaryoya aittir; Astra'ya veya tüm agent sistemlerine genellenemez. [Anthropic açıklaması](https://claude.com/blog/claude-for-chrome). |
| ChatDev %33.33; araçlarda genel %3–15 hata | ChatDev oranı MAST v2'deki ProgramDev bağlamına aittir; `ProgramDev²` üst simgesi dipnottur. Genel %3–15 araç hata oranı için birincil ölçüm doğrulanmadı. [MAST v2](https://arxiv.org/html/2503.13657v2). |
| SDK guardrail bütün yazmaları önler | Paralel input guardrail tamamlanmadan araç çalışabilir. Blocking kontrol ve her yazma sınırında deterministik yetkilendirme gerekir; output guardrail yapılmış yazmayı geri almaz. [SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/). |
| Sessions token maliyetini kendiliğinden düşürür | Varsayılan akış bütün geçmişi yeniden gönderebilir. Bağlam sınırı, seçme/özetleme ve gerçek kullanım ölçümü gerekir. [SDK sessions](https://openai.github.io/openai-agents-python/sessions/). |
| Temporal tekrar faturalamayı engeller | Kaydedilmiş tamamlanan activity tekrar yürütülmez; dış işlem başarılı olup acknowledgment kaybolursa retry aynı etkiyi yineleyebilir. Idempotency hedef servis veya transactional adapter tarafından uygulanmalıdır. [Temporal activities](https://docs.temporal.io/activity-definition). |
| Agent Builder/Evals 3 Haziran'da kapandı | Bu tarih deprecation duyurusudur. Evals read-only tarihi 31 Ekim, kapanış 30 Kasım 2026; SDK'nin kullanımdan kaldırıldığı sonucu çıkmaz. [Resmi deprecations](https://developers.openai.com/api/docs/deprecations). |
| Chalkline stopline tam güvenlik sağlar | README metinsel diff kapsam kontrolünü anlatır; doğruluk, test veya runtime yetkilendirme kanıtı değildir. [Chalkline](https://github.com/Gipppp121/chalkline). |

Uygulama kararı: belgeden çıkan aday kayıt → deterministik doğrulama → mevcut yetki kapsamı ve gerekiyorsa payload'a bağlı onay → sabit operation ID ile yazma → hedef sistem makbuzu ve mutabakat. Gönderim sonrası timeout `unknown` durumudur; kontrolsüz tekrar gerekçesi değildir. Bu tasarım önerisinin uygulandığını göstermek için zorunlu yürütme kodu ve failure-mode testleri gerekir.

## SmartBlock: kodun gösterdiği mevcut FreeMesh demo

Yerel kaynak `Projects/mobile/smartblock/src/freemesh/transport.ts:13` boş `iceServers` listeli `RTCPeerConnection` oluşturuyor; offer/answer ve DataChannel akışı var. `Projects/mobile/smartblock/src/freemesh/crypto.ts:28` libsodium `crypto_box` için X25519 oturum anahtarı, fingerprint ve `crypto_box_easy` kullanıyor; replay ID kümesi ve 1.000 mesaj sınırı mevcut. İncelenen demo manual pairing/WebRTC uygulamasıdır; BLE/LoRa taşıması, çok atlamalı mesh veya ratchet protokolü bu iki dosyada uygulanmış değildir.

Bu nedenle Bluetooth/LoRa üzerinden internetsiz çok atlamalı iletişim hazır özellik gibi sunulmamalı. Mevcut kod incelemesi kriptografik audit, cihazlar arası bağlantı başarısı veya yeni transport'un geliştirildiği anlamına gelmez. Yerel referanslar kişisel veri/anahtar içerikleri olmadan yalnızca kaynak dosya yollarını belirtir.

## HomeLab: protein modeli ile sağlık yorumu farklı görevler

`Synthyra/ESM2-650M`, aminoasit dizileri üzerinde çalışan ESM2 checkpoint'inin Transformers/FastPLMs paketidir. Model kartı `trust_remote_code=True` kullanımını ve sequence/token sınıflandırma başlıklarının yeni, eğitilmemiş olduğunu açıkça belirtir. Bu kart Ollama entegrasyonu, webcam/işitme testlerinden klinik yorum veya hastalık olasılığı için doğrulama sunmaz. Ağırlıkların indirilebilir olması bu ürün görevlerine hazır olma kanıtı değildir. [Model kartı](https://huggingface.co/Synthyra/ESM2-650M).

Yerel `Projects/saas/homelab/src/services/aiService.ts:14` yorum çağrısı yerine `offline-notice-no-inference` döndürüyor. `Projects/saas/homelab/src/lib/ai/nimConfig.ts:20` boş anahtar döndürüyor; legacy `nimVisionService.ts` çağrıları `fetch` öncesi eksik anahtarda duruyor. Bunlar incelenen akışın mevcut sınırlarıdır; bütün uygulama için ağ trafiği testi yapılmış değildir. Model ve Ollama entegrasyonu kurulmadı. HomeLab kullanıcı verisinin cihazdan çıkmaması kuralı korunmalı; sağlık verisinin dış sağlayıcıya aktarılması mevcut ürün sınırını ihlal eder.

## Yerel skill'lerin anlamı ve takip

`.codex/skills/backoffice-write-gate/SKILL.md`, kaynak doğrulama, tenant/resource yetkisi, idempotency ve `unknown` sonuçların mutabakatını tarif ediyor. `.codex/skills/evidence-driven-visualization/SKILL.md`, ölçüm/tahmin/simülasyon ayrımını, kaynak zamanını ve olayla bağlantılı animasyonu tarif ediyor. Bunlar metinsel talimat belgeleridir. Fatura alanı eksikliği, kayıp acknowledgment, hesap bulunmaması ve veri olmadan olay gösterilmesi gibi senaryolar için statik olarak incelendiler; evrensel runtime kapısı, test edilmiş entegrasyon veya canlı kâr kanıtı değiller.

Toolkit'in [quant kategorisi](../categories/16-quant-algo-trading.md) tarandı. Aynı isimli `qusong0627/QuantMind` ile bu rapordaki `LLMQuant/quant-mind` farklı depolardır. Somut içerik fikri: kaynaklı araştırma ekranında görünen bir simülasyon sonucunun neden alpha kanıtı olmadığını gösteren teknik demo. Entegrasyon adayı: B2BLife/TSA araştırma kartlarında kaynak URL'si, sürüm/hash, olay zamanı ve erişim zamanını ayrı taşımak. Bu fikirler uygulanmış değişiklik veya ölçülmüş gelir artışı olarak işaretlenmemeli.

Bu rapor dışında proje, deployment guide veya başka rapor değiştirilmedi. Commit/push ve NotebookLM aktarımı bu dosya hazırlama adımında yapılmadı.

## Ek: Monte Carlo, Markov ve Polymarket kazanç iddiaları

Bu ek de 17 Eylül 2026 tarihli salt okunur kontroldür. [w1nklerr paylaşımı](https://x.com/w1nklerr/status/2100257203055730842) ve [dan1ro0 paylaşımı](https://x.com/dan1ro0/status/2100313734480875579) tarayıcı araştırma aracında HTTP 403 döndürdü; indeks aramasında içerikleri bulunamadı. Aşağıdaki paylaşım rakamları kullanıcı tarafından aktarılan iddialar olarak değerlendirilmiştir; özgün gönderi içeriği veya strateji kodu doğrulanmış sayılmamalı.

| Aktarılan iddia | Hesap ve kanıt sınırı |
|---|---|
| 10.000 Monte Carlo yolunun 6.400'ü kazanıyor; %64 olasılık, piyasa 53 cent. | Oran %64'tür. Aynı sabit modelden bağımsız Bernoulli örnekleri varsayılırsa Monte Carlo standart hatası `sqrt(0.64×0.36/10000)=0.0048`, yani 0,48 yüzde puan; yaklaşık %95 normal aralık %63,06–%64,94. Bu yalnızca simülasyon örnekleme belirsizliğidir. Model yanlılığı, yanlış dağılım/parametre, rejim değişimi ve olasılık kalibrasyonu bu aralığa dahil değildir. Daha çok aynı-model simülasyonu bu hataları ortadan kaldırmaz. |
| %64 ile 53 cent arasında kesin kazanç var. | Aynı olay ve settlement kuralı için model olasılığı doğru kabul edilirse `0.64−0.53=0.11` dolar/hisse brüt beklenen değer hesabı yapılır. Bu gerçek kazanma olasılığının veya gerçekleşecek kârın ölçümü değildir. Ekrandaki son fiyatın uygulanabilir alış fiyatı olduğu da varsayılamaz. Kalibrasyon, ileri dönem veri, fill fiyatı ve maliyetler doğrulanmadan işlem sonucu çıkarılamaz. |
| Markov modeli >1,8 ATR koşulunda %71 başarı ve ortalama R/R 5,4 veriyor. | Koşulun yönü, ATR'nin hesaplandığı an, tahmin ufku, geçiş sayıları ve hedef/stop'a önce ulaşma sırası belirtilmeden %71 yorumlanamaz. Geçişleri öğrenen dönem ile test dönemi ayrılmalı; çakışan pencereler bağımsız gözlem sayılmamalı. “Ortalama R/R 5,4”, gerçekleşmiş ortalama kazanç/ortalama kayıp mı, planlanan hedef/stop oranı mı belirsizdir. Bu iki sayıdan güvenilir PnL veya gelecek başarı türetilemez. |
| Farklı anlarda YES+NO toplam 98,69 cent; risksiz 1,31 cent. | `100−98.69=1.31` cent brüt fark aritmetik olarak doğru. Aynı condition için eşit miktarda uyumlu YES+NO gerçekten edinildikten sonra complete set birleştirilebilir. İkinci bacak henüz dolmamışsa açık yön/enventory riski vardır; iki farklı zamanın fiyatını toplamak atomik işlem kanıtı değildir. |

Resmi Polymarket dokümanı `1 YES + 1 NO → 1 pUSD` birleştirmesini açıklıyor; işlem için eldeki dengeli token miktarı esas alınıyor. Birleştirmenin atomik olması, order book'taki iki ayrı alışın birlikte veya aynı fiyattan gerçekleşeceği anlamına gelmez. Tamamlanmış net sonuç için fiili fill miktarları, iki bacağın maliyetleri ve birleştirme makbuzu gerekir. [Merge açıklaması](https://docs.polymarket.com/trading/positions/manage#merge-positions).

17 Eylül'de erişilen ücret sayfası, ücretli piyasalarda taker için `fee=C×feeRate×p×(1−p)` formülünü ve crypto kategorisinde `feeRate=0.07` değerini gösteriyor; maker ücreti sıfır. Örnek olarak iki bacak da 50 cent civarında taker olarak dolarsa toplam ücret yaklaşık 3,5 cent/çift olabilir ve 1,31 cent brüt farkı aşar. Bu örnek kullanıcıdaki işlemin kesin ücreti değildir: gerçek piyasa parametresi, fiyat, maker/taker rolü ve kazanılmış rebate ayrı doğrulanmalı. Slippage, eksik fill ve geç kalan ikinci bacak ayrıca hesaplanmalı. [Resmi ücretler](https://docs.polymarket.com/trading/fees).

[`@trinity42` kamu profili](https://polymarket.com/@trinity42) kontrolde yaklaşık `+$145.3K Profit/Loss`, `$4.4M Volume` ve `60,427 Predictions` gösterdi. Bu, platformun gösterdiği anlık kamu özeti olarak doğrulandı; aktarılmış `$145,013 / 153 gün / %53 win rate` birleşimi sayfada doğrulanmadı. Kamu özeti tek başına başlangıç sermayesi, dış nakit akışları, tüm ücretler, pozisyon değerleme yöntemi ve risk alınan sermaye için mutabakat sağlamaz. Bu nedenle bağımsız denetlenmiş net getiri, önerilen dört modelin katkısı veya tekrarlanabilir alpha sonucu çıkarılamaz. Aynı markette parçalı fill'ler, pozisyon azaltmaları ve iki taraflı işlemler bulunabileceği için fill/“Predictions” sayısı bağımsız bahis sayısı değildir. Düşük/yüksek win rate de pozisyon boyutu ve kazanç/kayıp büyüklükleri olmadan kârlılığı açıklamaz.

NewRoan/AgenKit için aktarılan `$4.99` promosyonu ve “dört model en çok alpha üretir” iddiasına bu kontrolde doğrulanabilir birincil performans kanıtı bulunmadı. Ürün fiyatı, orkestrasyon özellikleri veya iyi yazılmış uygulama; maliyet sonrası ve örneklem dışı kazanç kanıtı değildir. Gerekli araştırma çıktısı, her modelin tek başına ve birlikte aynı veri/maliyet koşullarındaki sonuçları, önceden belirlenmiş test planı ve tüm denemelerin kaydıdır.

Bu ek için hesaba giriş, cüzdan bağlantısı, emir, token birleştirme veya para hareketi yapılmadı. Kamu profilinde görülen sonuçlar kullanıcı hesabının kârı olarak gösterilmedi; yeni bir finansal eylem yetkisi çıkarılmadı.

## 22 Eylül ek kontrolü: video ve ürün iddiası

[RetroChainer paylaşımının](https://x.com/retrochainer/status/2100554058683625782) 16 saniyelik kamu videosu oturum açmadan indirilebildi. `watch` skill'inin otomatik kare çıkarımı yerel FFmpeg'de kaldırılmış `-vsync` seçeneğine takıldı; yerel FFmpeg ile 0, 7 ve 15. saniyelerde üç kare çıkarılıp incelendi. Altyazı yok; ücretli ses transkripsiyonu kullanılmadı. Bu üç kare, bütün video ayrıntılarının okunabildiği anlamına gelmez.

7 ve 15. saniyede çok düğümlü, ışık izli bir yazılım/ajan operasyon ekranı; araç/denetim sayaçları ve görev-sıralama kartları görülüyor. Küçük metinlerin bir kısmı okunamıyor. Bu karelerden gerçek borsa emirleri, mutabakatlı hesap kazancı veya 300 çalışanın gerçekten yürütüldüğü doğrulanamaz. Grafik, tasarım referansı olabilir; gerçekleşmiş trading getirisi kanıtı değildir. Diğer erişilemeyen X bağlantıları görülmüş sayılmadı.

[ChatGPT for Financial Services resmi duyurusu](https://openai.com/index/introducing-chatgpt-financial-services/) 10 Eylül tarihli araştırma, finansal modelleme ve müşteri materyali iş akışlarını açıklıyor. Duyuru, belirli bir sosyal medya botunun kârlılığını veya perakende hesapta otonom kazanç garantisini doğrulamıyor.
