# Kaynak → uygulama karar tablosu

17Kasım2026. Bu tablo kaynak değerlendirmesidir; satırların tamamı kurulmuş entegrasyon değildir. GitHub lisansı, veri/model/görsel lisansıyla aynı şey değildir. Ayrıntılı repo satırları [metadata matrisinde](portfolio-source-matrix-20261116.md), servis koşulları [API defterinde](api-and-non-github-source-registry-20261116.md).

| Uygulama | İlk kullanılabilecek sınırlı set | Daha sonra / ayrı modül | Uygulanmayacak varsayım | Doğrulama kapısı |
|---|---|---|---|---|
| LayOverKit | MapLibre mevcut entegrasyonu; OSM+OurAirports temel konum; resmî işletmeci POI bilgisi | PMTiles/Protomaps çevrimdışı paket, MapWarper/Rumsey tarihî katman, yerel kamera birleştirme | OSM sınırsız ücretsiz karo değildir; lounge üyelik/ücret bilgisi açık haritadan kesinleşmez | HerPOI kaynak/verified_at/confidence; terminal/erişim ayrımı, atıf ve çevrimdışı paket testi |
| SmartBlock | Yerel Android CallScreening; numara normalizasyonu için libphonenumber, izinli liste ve yerel kural yönetimi | Matrix/Element, Jami, Briar, bitchat iletişim araştırması; WireGuard/mesh ayrı ürün bileşeni | Mesajlaşma/VPN normal aramayı filtrelemez; iOS’a Android davranışı veya dakik zamanlı native filtre vaat edilmez | Android gerçek çağrı/rol testi, eski-native uyumluluğu; Apple API sınırı; kişiler/ses cihaz dışına gönderilmez |
| Enuma (önceki mağaza adı Alamet) | Mevcut native/test ve mağaza kimliği korunur; bu katalog yeni bağımlılık gerektirmez | Yeni araç ancak somut hata/özellik ihtiyacıyla | Hazır repo eklemek AppStore4.3 reddini kendiliğinden çözmez | Doğru bundle/appID, açıklama/özgünlük kanıtı ve platform testleri |
| HomeLab | Mevcut cihaz içi localStorage PWA; kaynak/birim/referans aralığı gösterimi | OpenCV/MediaPipe yalnız cihaz içi olasılığı ayrıca incelenir; MONAI/OHIF/nnUNet araştırma kaynakları | FHIR/PACS/backend, PostHog, bulut depolama veya genel AI API’sine hasta verisi gönderilmez; selfie’den hastalık/psikiyatrik risk puanı yok | Ağ çıkışı engeli, veri silme/onam ve offline test; klinik doğrulama olmayan sonuç tanı diye sunulmaz |
| B2BLife | Mevcut FastAPI+Hetzner PostgreSQL; kaynaklı şirket profili, tenant erişimi ve PostgreSQL araması | İhtiyaç olursa PostGIS/pgvector, Meilisearch veyaTypesense; dar yetkiliMCP/LangGraph | Next/Nest/ORM/CRM seçeneklerinin hepsi birden eklenmez; Supabase kullanılmaz; lookupAPI kuruluş başvurusu değildir | Kaynak+son kontrol, ekip/tenant yetkileri, şirket doğrulama, onaylı taslak iletişim |
| Scuplan | MapLibre+doğrulanmış dalış noktası, kayıt/günlük; OpenDiveMap/DiveVibe/Subsurface referansları | OpenMeteo/NOAA/Copernicus hava/deniz katmanı; ticari sağlayıcı lisansı uygunsa | Ücretsiz yazılım sınırsız ticariAPI veya güvenli dalış garantisi değildir; doğrulanmamış dekompresyon motoru canlı öneri vermez | Nokta kaynağı/tarih, yanlışPOI ayıklama, medya lisansı, datum/timezone, bağımsız güvenlik doğrulaması |
| ScreenMesh | Mevcut ürün mimarisi incelendikten sonra, yalnız sahip olunan/izinli uçların envanter ve durum gözlemi için NetBox/OpenWISP/Zeek/Suricata adayları | İzinli kamera için MediaMTX/go2rtc; bilimsel veri farklı modül | İnternet genelindeki rastgele kamera/TV/drone erişimi; C2/kimlik bilgisi toplama araçlarının ürün bağımlılığı olması | Sahiplik/yetki, veri minimizasyonu, kaynaklı olay kaydı; mevcut ürün işlevi bu katalogdan varsayılmaz |
| RoboCheckIn | Nuclei/ZAP/Trivy gibi araçlar yalnız açık yetkili kapsamda inceleme adayı; Prometheus/OpenTelemetry izleme | CUE yapılandırma doğrulaması; pasif ağ/varlık araştırması ayrı | Katalogdaki C2/AD/phishing araçlarını otomatik kurup müşteri hedeflerine çalıştırma yok | Kapsam/izin, test ortamı, yalancı pozitif incelemesi, performans sınırı |
| SciBreak | USGS/NASA EONET/FIRMS+ObsPy/PySTAC/xarray; kaynaklı olay taslağı | Copernicus/Astroquery/SatNOGS; yalnız yeniden yayın izni olan kamera | Otomatik analiz resmî alarm değildir; herkese açık görüntü yeniden yayın izni değildir | Kaynak/zaman/konum, bağımsız teyit, hak kontrolü; haber/kurum bildirimi için insan incelemesi |
| Grimfiles / LearnLingOz / TheMrOz / ciaoariabella | Mevcut ücretsiz yerel içerik/ses/montaj hattı; FFmpeg/Blender/ComfyUI araştırma | Diffusers/LTX/OpenSora ancak donanım, model lisansı ve gerçek maliyet uygunsa | Rakip transkripti kopyalamak, ses/kişilik taklidi, ücretli servisi ücretsiz repo sanmak yok | Özgün kaynak defteri, dil/ASR+dinleme, görsel hakları, doğru hesap/kanal ve yayın makbuzu |
| TSA / KredimPlus / How2TakeOff | Mevcut stack ve HetznerPostgreSQL; CUE/izleme/veri araçları gerçek ihtiyaca göre | Kaynaklı araştırma/raporlama, dar yetkiliMCP | İptal edilen FundPilot yeniden açılmaz; trading botu kâr garantisi veya canlıhesap entegrasyonu yapılmaz | Mevcut test/deploy kapıları; hassas veri loglanmaz, API maliyeti ayrı doğrulanır |

## Öncelik ve maliyet

İlk öncelik mevcut hata/test/doğru veri akışıdır. Aynı işi yapan alternatiflerden birini ancak somut açık ortaya çıkarsa seçmek, bakım ve sunucu maliyetini azaltır. Bu katalog için yeni ücretli servis, sunucu, API hesabı veya gerçek işlem hesabı açılmadı. Gelir artışı için ölçüm olmadan MRR tahmini üretilmedi.

## Yanlış veya eski adresler

- `nestjs/nestjs` yerine doğrulanan kaynak `nestjs/nest`.
- AzureMCP için `microsoft/azure-mcp` doğrulanmadı; Microsoft dokümanı `microsoft/mcp` içindeki Azure sunucusunu gösteriyor.
- `joplin/joplin` doğrulanmadı; proje kaynağı `laurent22/joplin` olarak doğrulandı.
- CopernicusMarine için önceki aday doğrulanmadı; resmîFAQ `mercator-ocean/copernicus-marine-toolbox` bağlantısını gösteriyor.
- SatNOGS istemcisi resmîWiki’de GitLab’a bağlı; yanlış GitHub adayı repo sayılmadı.
- Atlasr `atlasr-org/atlasr`, DiveVibeCommunity `jbunderwater/dive-vibe-community` olarak birinci taraf kaynaklarla çözümlendi.
- EvrenAPI, Mantis, ShopClass ve belli sağlayıcı belirtilmeyen global kuruluşAPIleri için kesin karşılık uydurulmadı.

API defterindeki HTTP403/timeout, kaynağın kesin kapandığı anlamına gelmez. HTTP200 de lisans, güvenlik veya üretime hazır entegrasyon garantisi değildir.

## Son iletilen OpenAI Agents Python SDK — 17 Kasım

Mevcut katalog kaydı güncellendi; duplicate satır eklenmedi. MIT, aktif; 30.735 yıldız GitHub API anlık doğrulaması. B2BLife/TSA Python iş akışları ve SciBreak taslak/QA için aday. LayOverKit mobil uygulamasına ek runtime bağımlılığı getirmeden ancak ihtiyaç varsa sunucu worker katmanında değerlendirilir. HomeLab'a bağlanmaz. Model maliyeti ve tracing yoluyla hassas veri aktarımı için ayrı doğrulama gerekir. Kurulum/entegrasyon yapılmadı.
