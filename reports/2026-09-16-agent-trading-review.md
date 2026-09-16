# Ajan, trading ve bellek içerikleri — kaynak kontrolü

Kontrol tarihi: **16 Eylül 2026**. Kapsam: kullanıcı tarafından iletilen makale metinleri, Claude değerlendirmesi, seçilmiş resmi dokümanlar ve repo README'leri. Bu çalışma yatırım tavsiyesi, kârlılık doğrulaması, kod güvenlik sertifikası veya canlı işlem sistemi değildir. Ekran görüntüsü, takipçi sayısı ve GitHub yıldızı performans kanıtı sayılmadı. Görsel yer tutucularından içerik çıkarılmadı; gizli bilgiler rapora alınmadı.

## Kısa karar

**Kullan:** görev başına sahiplik, dar izinler, kaynak+zaman kaydı, bağımsız test, bütçe/retry sınırı, deterministik risk kapısı, başarısız deneylerin belleği.

**Doğrulamadan kullanma:** sabit Sharpe/t-istatistiği eşikleri, kalibre edilmemiş confidence, LLM tarafından yazılan kodun doğrudan çalıştırılması, tarihsel veriye tekrar tekrar ayar yapıp bunu ilerleme saymak.

**Reddet:** kusursuz strateji/garanti kazanç, ekran görüntüsünden doğrulanmış PnL, büyük ajan sayısını yatırım avantajı saymak, açığa çıkmış anahtarlarla otomasyon, modelin risk sınırını kendi kararıyla gevşetmesi.

## 1. Model ve maliyet iddiaları

GPT-6 Astra model sayfası 1.050.000 token bağlam, 128.000 token azami çıktı ve low/medium/high/xhigh/max seviyelerini listeliyor. Standart milyon token fiyatları input 10 USD, cached input 1 USD, output 50 USD. 272.000 input üzerindeki isteklerde tüm isteğin input/cache fiyatı 2, output fiyatı 1,5 ile çarpılıyor. Bunlar API özellikleri; yatırım kabiliyeti veya aylık sabit işletim maliyeti değildir. [OpenAI model sayfası](https://developers.openai.com/api/docs/models/gpt-6-astra).

Makalelerdeki maliyet kodunun iki hatası var:

- `penalty = usd - usd/2` doğru değildir: output çarpanı 2 değil 1,5. Ceza, aynı token kullanımının eşik altı tarifesiyle hesaplanan bedeli çıkarılarak bulunmalı; cache-write/tool bedelleri ayrıca izlenmeli.
- `len(prompt)//4` kesin önkontrol değildir. Dil ve içerik türüne göre sapar; input, araç tanımları, çıktı rezervi ve kalan hesap kotası birlikte değerlendirilmelidir. TPM, modelin bağlam kapasitesiyle aynı şey değildir.

Abonelik kotasını API token fiyatına çeviren anekdotlar, “258K her kullanıcıda değişmez”, “10.000 kat ucuz aynı hedge fund” ve tüm benchmark/AGI alıntıları bu incelemede bağımsız doğrulanmadı. Güncel ürün/hesap dokümanı ve ölçülen kullanım esas alınmalı. [OpenAI model kullanım rehberi](https://developers.openai.com/api/docs/guides/latest-model).

Kimi'nin kendi duyurusu K3 için 2,8 trilyon parametre, 1M context, 3 USD uncached input / 0,30 USD cached input / 15 USD output tarifesini destekliyor. Bu, 300 ajanın bütün piyasa geçmişini eksiksiz tuttuğunu, tüm veri lisanslarının dahil olduğunu veya 24/7 sistemin 300–500 USD'ye mal olacağını kanıtlamaz. [Moonshot duyurusu](https://forum.moonshot.ai/t/kimi-k3-is-here-our-most-capable-model/480).

Derin muhakeme / geniş tarama ayrımı yararlı bir iş bölümü olabilir. Önce gerçek workload üzerinde tek ajan + normal veri işleyici tabanı ölçülmeli. Fiyat taramak çoğunlukla akış tüketimi ve hesaplama işidir; her sembol için sürekli LLM çağrısı gerektirmez. Sermaye küçükken sabit altyapı gideri ekonomik avantajı kolayca yok edebilir.

## 2. Money Heist, graph, loop ve Claude yorumu

10 rol bir organizasyon şablonudur; 10 dakikada güvenilir üretim sistemi kurulmuş olmaz. Özgün metinde **Berlin planlama, Palermo adversarial review/veto** sahibidir. Claude notunda Berlin'i risk veto, Palermo'yu meta-loop olarak yeniden adlandırmak aynı rol haritası değildir. İki şema karıştırılmamalı; bir çıktı için tek sorumlu belirlenmeli.

Harness izin ve çalıştırma sınırlarıdır; loop kontrollü tekrar; graph bağımlılık/dallanma yapısıdır. Bu ayrım yararlı. İlgili cloud-engineering preprint'i gerçektir; bir makalenin var olması uygulamaların üretim güvenilirliğini tek başına kanıtlamaz. [Zero-trust graph/loop çalışması](https://arxiv.org/abs/2609.00050).

“Fake-edge” testi yalnız veri bağımlılığına bakarsa eksik kalır: aynı dosya, rate limit, kilit, cihaz veya bütçe paylaşımı da bağımlılıktır. Hatalı işçiyi `null` diye atıp başarı raporu üretmek güvenli değildir; beklenen/tamamlanan/başarısız işler sayılmalı. Orkestrasyon grafiği kalıcı checkpoint tutabilir; “yalnız çalışma süresince vardır, hiçbir şey saklanmaz” genel kural değildir.

Bağımsız bağlamlı verifier yararlı ama aynı model ailesinin ortak kör noktalarını yok etmez. Test, kaynak ve veri mutabakatı gibi dış kanıt gerekir. **Güvenlik/yetki ihlali çoğunluk oyu ile geçersiz kılınmamalı.** Reviewer'a gizli düşünce zinciri değil, eser, gereksinim, kaynaklar ve gözlenebilir test çıktısı verilmeli.

IAL-Scan'in özeti 6.549 repo, 74 aday bulgu, 47 projede doğrulanmış 68 hata ve %91,9 precision rakamlarını destekliyor. Bu istatistikler tüm ajanların hata oranı değildir. Makalenin pratik mesajı: dış geri-besleme döngüsü de süre, çağrı ve kaynak limiti taşımalı. [IAL-Scan](https://arxiv.org/abs/2607.01641). Diğer 36 bin repo taraması, 6.290 boş çalışma ve tarihsel “terimi kim buldu” rakamlarının tamamı bu kontrolde yeniden üretilmedi.

**AIRA_2 düzeltmesi:** %81,5 araştırma benchmark'ında ortalama yüzdelik sıralamadır; trading getirisi veya genel doğruluk değildir. HCE yalnızca ayrı reviewer ajanı değildir: arama değerlendirme etiketleri ve nihai seçim verisi arama yapan işçiden ayrılır. Finansal zaman serisine rastgele eğitim/test bölme taşınamaz. [AIRA_2 yöntemleri](https://arxiv.org/html/2603.26499v2).

**SoL-Pi düzeltmesi:** NVIDIA reposunda Action Fusion, Online Context Compact, ObservationPack ve Evidence-Preserving Reducer gerçekten var. Bunlar Pi için isteğe bağlı mekanizmalar; her portföyde aynı tasarruf kanıtı değil. Orijinal observation saklanması ve alıntı doğrulaması önemli; özetin metne sadık olması sonucun doğru olduğunu garanti etmez. Reducer tanı günlüklerini harici servise gönderebildiğinden gizlilik incelemesi gerekir. [NVlabs/SoL-Pi](https://github.com/NVlabs/SoL-Pi).

## 3. “Sürekli strateji fabrikası” neden henüz tamamlanmış sistem değil?

Araştırma → kod → backtest → bağımsız doğrulama → izleme → post-mortem iyi bir süreç taslağıdır. Aşağıdaki eksikler, verilen 8-bot metnini doğrudan üretime taşımayı engeller:

1. 300 işçinin aynı `live.json` dosyasına yazması kayıp güncelleme ve yarım okuma üretir. Kuyruk, şemalı olaylar, benzersiz kimlik, atomik yayın ve tek sahip gerekir.
2. Üretilen `entry_condition` Python kodunu doğrudan çalıştırmak, araştırma girdisini kod yürütme yetkisine dönüştürür. Ağsız/kısıtlı sandbox, kaynak bütçesi, bağımlılık denetimi ve test olmadan kabul edilmemeli.
3. Telegram örneği, önceki JSON sözleşmesinde bulunmayan alanları kullanıyor. Timeout, kontrollü retry, hata kaydı ve gönderim/kayıt arasındaki çökme için idempotency yok. `.env` dosyası kendiliğinden process ortamına yüklenmez.
4. Günlük/saatlik mum verisi geçmiş order book, kuyruk önceliği, tüm delist olmuş varlıklar veya opsiyon yüzeyinin yerine geçmez. Verinin olay zamanı ve o tarihte bilinebilir olması ayrıca doğrulanmalı.
5. Sharpe > 1,5, drawdown < %15, hit rate > %55, t > 2 eşikleri tek başına anlamlı edge kanıtı değildir. Trend stratejisi düşük hit rate ile çalışabilir; çok sayıda deneme şans eseri iyi görünen aday üretir.
6. “Confidence %87” ancak tanımı ve bağımsız kalibrasyon testi varsa olasılık olabilir. Üç kaynak aynı ham veriyi kopyalıyorsa üç bağımsız doğrulama sayılmaz.
7. “İlk sinyal altı saatte”, “üç gündür çalışıyor” ve “beş parça çözüldü” ifadeleri işletim veya finansal performans garantisi değildir.

Deflated Sharpe, seçilim ve dağılım sorunlarını değerlendirmeye yardımcı olur; başka bir evrensel geçer/geçmez sihri değildir. Denenen tüm adaylar, bağımlılıkları ve başarısızlıkları kaydedilmeli. Holm–Bonferroni sabit `t > 3` değildir; sıralı p-değerlerine test sayısına bağlı eşikler uygular. “En az üç walk-forward pencere” tek başına yeterli veri şartı değildir. [Bailey ve López de Prado, DSR](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551).

Bir backtest'i sonuç iyi olana kadar değiştirmek, sonraki denemeleri öncekinin testine uydurabilir. Dokunulmamış final değerlendirme, işlem giderleri, parametre duyarlılığı, dönem etkisi, gerçekçi gecikme ve net performans karşılaştırması gerekir. Saklanan başarısız deneyler hafızadır; model ağırlıklarının fine-tune edildiği anlamına gelmez.

## 4. Finans matematiği: doğru çekirdek, yanlış kesinlik

| İddia | Değerlendirme |
|---|---|
| Coke/Pepsi daima %2 içinde ve ayrışınca kesin geri gelir | Kaynaklandırılmamış genelleme. Korelasyon, cointegration ve ekonomik işlem maliyeti farklı şeylerdir. Rejim kırılabilir. |
| IV gerçekleşmiş oynaklıktan büyükse arbitraj vardır | Risksiz arbitraj sonucu çıkmaz; volatilite risk primi, hedge hatası, sıçrama ve kuyruk riski vardır. Heston bir fiyatlama modeli; otomatik kazanç makinesi değildir. |
| Faktörlerden kalan %5 doğrudan alpha | Artık terim tek gözlemde alpha değildir. Model hatası, gürültü ve dışarıda kalmış riskler olabilir. |
| Insider cluster score > 3 ⇒ yılda %5,3 | Verilen skor formülü ve bu eşik/sonuç bağlantısı atıf yapılan çalışmayla doğrulanmadı. Cohen–Malloy–Pomorski rutin ve fırsatçı işlemleri ayırır; metindeki Nvidia örneğini kanıtlamaz. |
| 500 hisse aslında tam beş faktördür | “Beş” evrensel sayı değil. PCA risk sıkıştırma aracıdır; residual'ın geri döneceğini garanti etmez. |
| Markov modeli %68 geçiş olasılığıyla edge verir | Durum tanımı, örneklem, maliyet ve zaman içinde değişim olmadan böyle sabit bir olasılık yok. Medallion'ın kapalı stratejisinin kanıtı olarak sunulamaz. |
| HHI artışı yaklaşan dump'ı kesin gösterir | Borsa/LP/burn cüzdanları, köprüler ve çok cüzdanlı sahiplik sonucu değiştirebilir. Rug güvenlik sertifikası değildir. |
| ADX/Hurst iki formülle rejimi çözer | Wilder ADX yumuşatması basit hareketli ortalamayla aynı değil. Hurst çok ölçekli tahmindir; tek kısa pencere ciddi belirsizlik taşır. |

Insider kaynağı: [NBER — Decoding Inside Information](https://www.nber.org/papers/w16454). PCA/residual işlemleri için gerçek akademik başlangıç: [Avellaneda–Lee](https://math.nyu.edu/inmemoriam/avellaneda/AvellanedaLeeStatArb20090616.pdf). Bu çalışma tarihsel örnek ve maliyetlere duyarlı sonuçlar verir; bugünün net kârını kanıtlamaz.

500×501/2 = 125.250 sayısı doğrudur, köşegen varyanslar dahildir. Marchenko–Pastur üst sınırının yaklaşık 4 olması standardize varyans ve N/T≈1 gibi varsayımlar gerektirir. Bant içindeki her özdeğerin ekonomik olarak değersiz, bant dışındakinin işlem yapılabilir olduğu sonucu çıkmaz. PCA bileşenleri adlandırılmış Fama–French faktörleriyle birebir aynı değildir. Market-neutral residual stratejiler çoğu zaman short/hedge ister; short istemeyen kullanıcıya bunlar olduğu gibi uygulanamaz.

### Kelly örneğinin yeniden hesabı

Eşit kazanç/kayıp, bağımsız tekrar ve bilinen p varsayımı altında `g(f)=p·ln(1+f)+(1-p)·ln(1-f)`:

- p=0,55 için full Kelly f=0,10. Yarım Kelly yaklaşık büyümenin %74,93'ünü, çeyrek Kelly %43,69'unu verir; makaledeki %75/%44 yaklaşık olarak doğru.
- f=0,20 için g≈−0,000137742. “Tam iki Kelly'de büyüme kesin sıfır” tam formülde doğru değil; küçük avantaj yaklaşımıdır.
- Gerçek p=0,52 iken f=0,10 için g≈−0,001011754, yani işlem başına yaklaşık −%0,1012 **beklenen log büyüme**. Bu aritmetik beklenen getiriyle karıştırılmamalı.
- Hesabın yarılanma olasılıkları, başlangıç sermayesine mi zirveye mi göre ve hangi ufukta ölçüldüğü belirtilmeden genellenemez. Fractional Kelly, yanlış olasılık veya negatif edge'i güvenli yapmaz.

Rastlantı yazılarındaki örneklem, maliyet ve kuyruk riski vurgusu yararlı. CLT tekil hisse getirilerinin normal dağıldığını ya da her kuyruğun Poisson olduğunu söylemez. 10.000 bağımlı işlem 10.000 bağımsız deney değildir. Adil parada 10 atışta en az 8 yazı olasılığı %5,46875'tir: ne mucize ne de kesin beceri kanıtı.

## 5. Polymarket: fiyat, dolum ve envanter farklı katmanlar

Fair value / gerçekleşebilir ortalama dolum / envanter ayrımı iyi. Ancak “10 milyon işlemi analiz ettim” iddiası için veri seti, seçim yöntemi ve yeniden üretim kodu verilmemiş. Bir cüzdanın fill geçmişinden gizli stratejisi kesin çıkarılamaz.

Aynı ikili piyasada eşit sayıda iki sonuç payı, geçerli settlement şartları altında birleştirilebilir ekonomik yapı oluşturur. Ama ucuz bacağı önce almak, ikinci bacak dolana kadar risksiz arbitraj değildir. Toplam gider, derinlik, kısmi dolum, iptal, finalizasyon ve çözüm kuralları hesaba katılmalı. Kaldıraçsız bir sonuç payı da yatırılan bedelin tamamını kaybedebilir. [Polymarket çözüm kuralları](https://help.polymarket.com/en/articles/13364518-how-are-prediction-markets-resolved).

Public profil/API adresi cüzdan imzalama yetkisi değildir. Kullanıcıya “yatırma” denmiş API adresine para gönderilmemeli. Konum/kullanıcı uygunluğu ve geoblock aşılmamalı. [API başlangıcı](https://docs.polymarket.com/getting-started/api), [geoblock](https://docs.polymarket.com/api-reference/geoblock).

## 6. FlySwarm ve sinek beyni iddiaları

Bilimsel çekirdek gerçek: yetişkin dişi Drosophila için 139.255 nöron ve yaklaşık 54,5 milyon sinapsı içeren çalışma 2024'te yayımlandı. Bir bağlantı haritası finansal fiyatlama, işlem gecikmesi veya yatırım getirisi kanıtı değildir. [Nature — Neuronal wiring diagram of an adult brain](https://www.nature.com/articles/s41586-024-07558-y).

**FlySwarm README'si pazarlama hikâyesini desteklemiyor:** cohort profitability, geçmiş oluşumlar ve sinyal sonuçları üretim wallet indexer'ı bağlanana kadar prototip veri olarak tanımlanıyor. Mevcut build'de private-key girişi veya transaction broadcaster olmadığı belirtiliyor. Bu nedenle 55→8.740 USD ve benzeri bakiyeler bu repo ile doğrulanmış işlem performansı sayılamaz. Dolandırıcılık teşhisi koymuyoruz; eldeki kanıtın iddiayı desteklemediğini söylüyoruz. [semkazz1/FlySwarm](https://github.com/semkazz1/FlySwarm).

**flybrain-robot-bridge** sekiz elle tasarlanmış sanal popülasyonlu bir mühendislik prototipidir; tam connectome yürütmez. ESP32 yolu scaffold ve donanımda doğrulanmamış; UDP güvenlik sınırları var. Sentetik demo/arayüz ilhamı olabilir, drone emniyet katmanı veya trading edge değildir. [Frankweb33/flybrain-robot-bridge](https://github.com/Frankweb33/flybrain-robot-bridge).

35,47→37.269,52 USD hikâyesi de bağımsız fill kayıtları, yatırma/çekme mutabakatı, gerçekleşmiş/açık PnL ayrımı ve ücretler olmadan doğrulanamaz. Strateji tasarımında hedef veya kabul kriteri yapılmadı.

## 7. Hangi repo nerede işe yarar?

| Kaynak | Karar / sınır |
|---|---|
| [openai-agents-js](https://github.com/openai/openai-agents-js) | Evet: TypeScript ajan orkestrasyonu, araçlar, handoff, guardrail ve trace için aday. Broker, muhasebe motoru veya kârlı strateji değildir. Basit veri toplayıcıya sırf çok ajan görünsün diye eklenmedi. |
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Araştırma referansı. Changelog'daki point-in-time/lookahead düzeltmeleri tarihsel testlerin dikkatle denetlenmesi gerektiğini gösteriyor. Varsayılan sonuçları canlı performans sanma. |
| [beamnxw-mem](https://github.com/beamnxw/beamnxw-mem) | Repo erişimi doğrulandı: iki oturumluk OpenClaw/Mem0 karşılaştırma demosu. Tam enterprise memory ürünü, kapsamlı benchmark veya kusursuz hatırlama kanıtı değil. |
| [SoL-Pi](https://github.com/NVlabs/SoL-Pi) | Tekrarlanabilir workload ve veri gizliliği ölçümü sonrası deney adayı. Kendiliğinden kurulmadı. |
| [ClawRouter](https://github.com/BlockRunAI/ClawRouter) | Model routing adayı; x402/ödeme ve sağlayıcı davranışı mevcut zincirden farklı. Portföyde %40–50 tasarruf ölçülmedi. Yetki olmadan ödeme yolu eklenmez. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Yerel STT/al altyazı kalite deneyi için uygun. API ücreti olmayabilir, donanım/işletim maliyeti sıfır değildir; TTS'nin yerine geçmez. |
| [Docling](https://github.com/docling-project/docling) | Yerel belge ayrıştırma/RAG aday bileşeni. OCR/tablo doğruluğu müşteri örnekleriyle ölçülmeli; 2–5 bin EUR satış geliri henüz hipotez. |
| [Repomix](https://github.com/yamadashy/repomix) | Seçici repo paketi; secret ve gereksiz dosya filtreleri zorunlu. Tüm repo her istekte verilirse token tasarrufu sağlamayabilir. |
| [OpenPanel](https://github.com/Openpanel-dev/openpanel), [OpenReplay](https://github.com/openreplay/openreplay) | Kontrollü analitik/replay deneyi. Self-hosted olması otomatik KVKK/GDPR uygunluğu sağlamaz. HomeLab sağlık ekranına uygulanmaz. |
| [Authelia](https://github.com/authelia/authelia) | Gerekirse servisler arası SSO/MFA. OCC'de zaten API auth/CSRF var; “hiç auth yok” yerel kodla uyuşmuyor. |
| [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Binary tersine mühendislik için; OCC genel güvenlik özelliği veya mesh protokol kanıtı değildir. GhidraMCP yıldız/entegrasyon iddiaları ayrıca incelenmeli. |
| [open-code-review](https://github.com/alibaba/open-code-review) | İnceleme pipeline referansı; ayrı güvenlik/test kanıtının yerine geçmez. |

NautilusTrader, AlphaGPT, Horizon, AgenKit, PersonaLive ve diğer satış ortaklığı bağlantılarının tüm kodu/ürün performansı bu çalışmada denetlenmedi. Katalog girdisi ile güvenlik/işlev doğrulaması farklıdır. `02-multi-agent-frameworks.md` ve `16-quant-algo-trading.md` araştırma başlangıcı olarak okundu; buradaki eski yıldız/kazanç/“production-ready” etiketleri otomatik onaylanmadı.

## 8. Bellek, second brain ve portföy iş değeri

Sourced Markdown + ham kaynak arşivi + kısa AGENTS yönlendirme haritası iyi başlangıçtır. Ham kaynak/değiştirilebilir türev ayrımı, tarih, sahibi, çelişki ve geçerlilik süresi tutulmalı. Bellek gerçeğin kendisi değil, hatalı bilgi ve prompt injection taşıyabilen bir veri katmanıdır. Sırlar ve müşteri/sağlık verisi topluca wiki'ye veya uzak embedding servisine taşınmaz. Paylaşılan transcript doğrudan kaydedilmedi.

Mem0 extraction işi kaçırma olasılığını azaltabilir; sıfırladığını tek Beacon demosu kanıtlamaz. Konfigürasyon, model, tekrarlı görevler, yanlış hatırlama, silme/izin ve maliyet birlikte test edilmeli. [Demo README](https://github.com/beamnxw/beamnxw-mem).

Miles Deutscher revenue/flows ve sosyal momentum fikirleri araştırma iş listesi olarak kullanılabilir; görsellerdeki tam promptlar görülmedi. Fees / protokol geliri / token sahibine aktarım ayrılmalı; wash trading, sybil hesaplar ve unlock/dilution kontrolü olmadan mention artışı alım sinyali olmaz.

“Dört para çarpanı” yararlı anlatım modeli, matematiksel olarak tüm servet kaynaklarını sınırlayan teorem değil. Yazılımın bakım/altyapı/satış maliyeti sıfır olmaz; borçsuz yatırım da zarar edebilir. 300 USD/ay, aylık bileşik nominal %8 varsayımıyla 30 yılda yaklaşık 447.108 USD hesabı aritmetik olarak tutarlı; gerçekleşecek piyasa getirisi, vergi/enflasyon sonrası sonuç veya garanti değildir.

Portföy için en yakın ölçülebilir deneyler: yerel belge ayrıştırma kalitesi, içerik altyazı doğruluğu, kaynaklı rakip araştırma raporu ve mevcut ürünlerin erişim/işlem güvenliği. Bunların geliri satışla ölçülür; ajan sayısı ile değil. Yeni ücretli araç alınmadı, satış/mesaj gönderilmedi.

## 9. Uygulama sınırı ve devam kapıları

Bu incelemeye eşlik eden OCC değişikliği **halka açık gözlem + sabit sentetik eğitim defteri** kapsamındadır. Gerçek piyasa stratejisi, tarihsel backtest, borsa demo hesabı, canlı işlem botu, Earn yatırma, hisse alımı veya cüzdan imzalama değildir. Canlı işlem açma anahtarı yoktur. Üç kaynak manuel sorgulanır; 24/7 izleyici başlatılmadı.

Hesapta işlem yapabilen ve sohbette paylaşılmış anahtarlar iptal edilip yenilenmeli; yeni sırlar sohbete, rapora, repoya veya NotebookLM'e yazılmamalı. Bu inceleme anahtarları iptal etmedi. [Gate güvenlik uyarıları](https://www.gate.com/docs/developers/apiv4/en/).

Spot, Earn ve “stock” aynı risk sınıfı değildir. Earn kilit/karşı-taraf/itfa riski taşır; hisse etiketinin gerçek hisse, tokenizasyon veya türev olup olmadığı sözleşmeyle belirlenir. Kullanıcının short/kaldıraç/teminat istememesi bu ayrımı zorunlu kılar. Gate dokümanında stock/TradFi girdisi bulunması tek başına kullanıcının erişimini veya ürün uygunluğunu kanıtlamaz. [Gate API](https://www.gate.com/docs/developers/apiv4/en/).

Araştırmaya devam için sıra: kapsamı belirle → temiz point-in-time veri → tek ekonomik hipotez → maliyetli tarihsel test → çoklu-deneme kayıtları → dokunulmamış doğrulama → simülasyon/izleme. Daha çok ajan veya daha büyük context, bu kapıları kaldırmaz. Gerçek finansal işlem ve sermaye yönetimi bu asistanın yürüttüğü iş değildir.

## 10. Claude için kısa düzeltme listesi

- Berlin/Palermo rol haritasını düzelt; hard veto'yu model çoğunluğuna bırakma.
- AIRA_2, HCE ve Harness/Loop/Graph'i aynı kavram diye sunma; benchmark yüzdeliğini PnL sanma.
- “t>3 ve üç pencere”yi evrensel istatistik kuralı olarak yazma.
- OCC auth yok, self-hosted=KVKK uyumlu, STT=sıfır maliyet, router=%50 tasarruf iddialarını ölçüm olmadan tekrar etme.
- FreeMesh/BLE ve robot kontrolü ayrı mühendislik/tehdit modelleri ister. Bir robot repo README'si SmartBlock'ta offline mesh veya uçuş emniyeti oluşturmaz.
- Dört yeni skill yönlendirme ve sınır dokümanıdır; çalışan runtime veya kârlı trading ürünü olarak raporlama.
