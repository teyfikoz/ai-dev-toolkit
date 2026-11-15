# How2TakeOff — havacılık repo/API/MCP değerlendirmesi

15 Kasım 2026. Araştırma teslimi; bağımlılık kurulmadı, uygulama mimarisi değiştirilmedi, production deploy/migration yapılmadı.

## Karar ve mevcut kod

Mevcut React/Vite + Express + Drizzle + self-hosted PostgreSQL korunur. `package.json`, `server/services/airportService.ts`, `airportCatalogService.ts` ve `server/data/airportCatalog.ts` incelendi. OurAirports kullanan servis/katalog zaten var; ikinci bağımsız havaalanı veri katmanı kurmak yerine provenance, güncellik ve tekilleştirme mevcut servis üzerinden geliştirilmelidir. Next.js/FastAPI/NestJS/Prisma alternatif teknoloji adaylarıdır; topluca geçiş için gerekçe yok. Keycloak/Ory/Zitadel birlikte kurulmaz; mevcut kimlik/yetki düzeni ve OIDC gereksinimi önce değerlendirilir.

60 adres kontrol edildi: 59 erişilebilir repo, 15 mevcut kayıt, 44 yeni katalog kaydı. Hatalı `nestjs/nestjs` yerine `nestjs/nest` doğrulandı. GitHub ayrıca Prisma→`prisma/orm`, Prophet→`meta/prophet`, LightGBM→`lightgbm-org/LightGBM`, dbt-core→`dbt-labs/dbt` yönlendirmelerini döndürdü. Kaynak adres ve kanonik adres ham JSON'da birlikte korunur. Bu bir metadata ve tasarım değerlendirmesidir; tüm kaynak kodların güvenlik veya lisans denetimi değildir.

## Öncelikler, süre ve gelir etkisi

| Öncelik | Teslim | Tahmini geliştirme | Kabul ölçütü / gelir ilişkisi |
|---|---|---|---|
| 1 | Mevcut veri laboratuvarında provenance, örnek CSV ve açık sentetik etiketi | 2–4 geliştirici günü | Kaynak/lisans/tarih görünür; bozuk CSV ve sınır aşımı reddi; eğitim ve organik trafik potansiyeli, ölçülmüş MRR yok |
| 2 | NetworkX rota bağlantılılığı ve basit istatistik karşılaştırması için izole offline pilot | 3–5 gün | Küçük sabit fixture ile hesaplar; gerçek kapasite/pazar payı iddiası yok; eğitim içeriği ve B2B demo değeri |
| 3 | Mevcut uygulama API'sine bağlı üç salt okunur MCP aracı | 3–5 gün | Makale arama, kaynak listeleme, havaalanı profili; yetki/red/limit testleri; araştırma erişimi |
| 4 | OpenAP/BlueSky eğitim senaryosu pilotu | 4–8 gün | Lisans ve veri modeli incelemesi, düşük CPU/bellek sınırı, senaryo etiketi; operasyonel tavsiye değildir |

Süreler planlama tahminidir, tamamlanma sözü değildir. Önceki AeroTrain CORE ve kurum kabulü açıklarını bu araştırma kapatmaz. Gerçek satış/talep verisi olmadan fiyat optimizasyonu veya gelir artışı yüzdesi üretilmez. Darts/Prophet/XGBoost/LightGBM önce basit statsmodels/sklearn baseline ile zaman sıralı geri testte karşılaştırılır; veri sızıntısı ve mevsimsellik kontrol edilir. Dask, PostGIS, pgvector, Meilisearch/Typesense ve BI servisi yalnız ölçülmüş ihtiyaç olduğunda eklenir. OR-Tools/Pyomo/PuLP sentetik kapasite tahsis laboratuvarı adaylarıdır.

## Lisans ve bakım kapıları

- GitHub SPDX, bağımlılıkların/veri dosyalarının veya ticari sürümlerin bütün koşullarını kapsamaz. NOASSERTION izin verilmiş anlamına gelmez; belirli sürümün LICENSE/NOTICE ve dağıtım biçimi incelenmeden ürün bağımlılığı kabul edilmez.
- pyModeS GPL-3.0; OpenAP LGPL-3.0; JSBSim LGPL-2.1; FlightGear/PostGIS GPL-2.0; FlightAirMap/DocuSeal/Graphsign/OpenCLM/Penpact/Grafana/Zitadel AGPL-3.0 metadata döndürdü. Bunların ayrı süreçte çalışması otomatik lisans muafiyeti değildir. İmza yazılımı, nitelikli elektronik imza veya hukuki geçerlilik sertifikası değildir.
- BlueSky ve BlueSky Gym MIT metadata döndürdü. Trafik/simülasyon araçları lisanslı pilot eğitimi veya gerçek operasyonel karar yetkisi sağlamaz.
- [n8n](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) Sustainable Use ve ayrı enterprise koşulları içerir; sınırsız SaaS gömme lisansı değildir. [Dify](https://github.com/langgenius/dify/blob/main/LICENSE) Apache tabanına ek çok kiracılı hizmet ve logo koşulları koyar. Bu nedenle mevcut worker yerine otomatik kurulum önerilmedi.
- [MinIO](https://github.com/minio/minio) arşivlenmiş ve AGPL-3.0: yeni varsayılan depolama katmanı seçilmedi. Mevcut yerel/Hetzner depolama, yedekleme ve erişim sınırları önce korunur. Hetzner Object Storage ücretli hizmettir; bu teslimde açılmadı.
- OpenTelemetry Go SDK, mevcut Node backend için doğrudan SDK seçimi değildir; dil uyumlu SDK kararı ayrı yapılır.

## API ve veri hakları kayıt planı

| Kaynak | Gerçek kullanım | Kabul öncesi kapı / durum |
|---|---|---|
| [OurAirports](https://ourairports.com/data/) | Mevcut havaalanı/pist referansı | İndirme tarihi, attribution ve kaynağın güncel koşulları kaydedilmeli; web erişimi bu tur timeout verdi, yeniden doğrulama açık |
| [AWC](https://aviationweather.gov/data/api/) | METAR/TAF meteoroloji | Güncel endpoint/schema, cache, hata/limit ve gözlem zamanı; yeni canlı entegrasyon yok |
| [OpenSky](https://openskynetwork.github.io/opensky-api/) | ADS-B state vectors | Resmi doküman araştırma/ticari olmayan kullanımı belirtir; ticari siteye yeniden yayın izni varsayılmaz. Tarifeler/gecikmeler/rezervasyon sağladığı iddia edilmez |
| [FAA](https://www.faa.gov/data_research) | ABD veri keşif portalı | Tek evrensel FAA API değildir; ürünün gerçek uç noktası ve yeniden yayın koşulu ayrı seçilir |
| [Eurocontrol](https://www.eurocontrol.int/data) | Avrupa trafik veri keşfi | Kaynak bazında kayıt/sözleşme/yeniden kullanım incelemesi açık |
| [Eurostat](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction) | Avrupa istatistikleri | Veri seti/kapsam/güncelleme/atıf seçimi açık; operasyonel canlı fiyat değildir |
| [UN Comtrade](https://comtradeapi.un.org/) | Ülke/ürün ticaret istatistikleri | Kota, plan ve yeniden yayın koşulları açık; hava kargo spot fiyatı veya kapasitesi değildir |
| [World Bank](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information) | Ekonomik göstergeler | Gösterge tanımı, dönem ve veri setine özgü koşullar ayrı kaydedilir |
| [OpenAlex](https://help.openalex.org/) | Yayın keşfi ve metadata | Güncel erişim/anahtar/kota koşulları ayrı doğrulanır; metadata izni makale tam metnini kopyalama hakkı vermez |

AWC/OpenSky/OpenAlex resmi sayfaları bu tur açıldı; diğer API'ler kaynak adaylarıdır, tüm koşulları doğrulanmış entegrasyonlar değildir. Her adaptör kaydında source_id, source_url, observed_at, retrieved_at, license_url, redistribution_status, coverage, cache_ttl ve synthetic alanları gerekir. Eksik/gecikmeli ADS-B tüm uçuşların kesin canlı konumu diye sunulmaz. Ticari rezervasyon, müşteri CRM, kapasite ve fiyat verileri için açık veri izni varsayılmaz.

## Salt okunur MCP tasarımı

İlk kapsam: `search_aviation_articles(query, category)`, `get_article_sources(article_id)`, `get_airport_profile(icao_or_iata)`. Mevcut uygulama izinlerinden geçen, yayınlanmış ve gerekli alanları döndüren API'ler kullanılır. PostgreSQL yönetici kimliği, arbitrary SQL, kullanıcı tarafından verilen URL fetch veya genel `query_public_aviation_data(source, query)` açılmaz. Kaynaklar allowlist ve tipli filtrelerle sınırlandırılır; zaman aralığı, sayfa/boyut, timeout ve rate limit zorunludur. Salt okunur annotation tek başına güvenlik değildir: token/issuer/audience/rol, tenant ve yayımlanma durumu sunucuda denetlenmelidir. Yazma, e-posta, rezervasyon, abonelik oluşturma ve operasyonel eylemler kapsam dışıdır. SDK sürümü ve transport/auth uyumu uygulama öncesinde resmi SDK dokümanıyla doğrulanır. DBHub yalnız ayrı düşük yetkili geliştirme/raporlama değerlendirmesidir.

## KVKK/GDPR ve ürün sınırı

Bu teslim kişisel veri toplamadı veya dış sağlayıcıya göndermedi. Yeni CRM/ürün analitiği kurulursa veri minimizasyonu, izin/saklama/silme ve AB/TR aktarım değerlendirmesi gerekir. PostHog oturum kaydı otomatik açılmaz. Öğrenci/personel verisi self-hosted PostgreSQL'de kalır. Eğitim içerikleri kaynak gösteren özgün özetler olmalı; IATA/ICAO tam metinlerini yeniden yayınlama hakkı varsayılmaz.

## Diğer portföyler için dar kapsamlı fikirler

B2BLife için NetworkX ile kaynakları belirtilmiş şirket ilişki grafiği; RoboCheckIn için OpenTelemetry ile PII içermeyen hata/latency ölçümü; TechSyncAnalytica için OR-Tools ile sentetik kapasite senaryosu; KredimPlus için statsmodels ile tarihli faiz serisi eğitimi değerlendirilebilir. Bunlar kurulmuş özellik veya gelir garantisi değildir. How2TakeOff içerik fikri: kaynaklı rota ağı eğitim serisi + indirilebilir sentetik CSV; simülasyon sonuçları gerçek uçuş tavsiyesi olarak sunulmaz.

## Tam repo eşlemesi

GitHub doğrulama tarihi ve ham metadata JSON raporunda. 44 yeni kayıt kategorisi araştırma amacıyla oluşturuldu; mevcut kayıtlar yerinde bırakıldı.

| İstenen repo | Güncel repo / lisans metadata | Katalog kararı |
|---|---|---|
| `vercel/next.js` | [vercel/next.js](https://github.com/vercel/next.js) / MIT | Mevcut: 04-browser-scraping-automation.md |
| `fastapi/fastapi` | [fastapi/fastapi](https://github.com/fastapi/fastapi) / MIT | Mevcut: 01-claude-code-ai-dev-tools.md |
| `nestjs/nest` | [nestjs/nest](https://github.com/nestjs/nest) / MIT | Yeni: 23-aviation-data-training.md |
| `nestjs/nestjs` | Erişilemedi | Eklenmedi; `nestjs/nest` kullanılır |
| `prisma/prisma` | [prisma/orm](https://github.com/prisma/orm) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `drizzle-team/drizzle-orm` | [drizzle-team/drizzle-orm](https://github.com/drizzle-team/drizzle-orm) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `postgres/postgres` | [postgres/postgres](https://github.com/postgres/postgres) / NOASSERTION | Yeni: 23-aviation-data-training.md |
| `postgis/postgis` | [postgis/postgis](https://github.com/postgis/postgis) / GPL-2.0 | Yeni: 23-aviation-data-training.md |
| `pgvector/pgvector` | [pgvector/pgvector](https://github.com/pgvector/pgvector) / NOASSERTION | Yeni: 23-aviation-data-training.md |
| `meilisearch/meilisearch` | [meilisearch/meilisearch](https://github.com/meilisearch/meilisearch) / NOASSERTION | Mevcut: 07-data-analytics-charts.md |
| `typesense/typesense` | [typesense/typesense](https://github.com/typesense/typesense) / GPL-3.0 | Yeni: 23-aviation-data-training.md |
| `xoolive/traffic` | [xoolive/traffic](https://github.com/xoolive/traffic) / MIT | Yeni: 23-aviation-data-training.md |
| `junzis/pyModeS` | [junzis/pyModeS](https://github.com/junzis/pyModeS) / GPL-3.0 | Yeni: 23-aviation-data-training.md |
| `junzis/openap` | [junzis/openap](https://github.com/junzis/openap) / LGPL-3.0 | Yeni: 23-aviation-data-training.md |
| `TUDelft-CNS-ATM/bluesky` | [TUDelft-CNS-ATM/bluesky](https://github.com/TUDelft-CNS-ATM/bluesky) / MIT | Yeni: 23-aviation-data-training.md |
| `TUDelft-CNS-ATM/bluesky-gym` | [TUDelft-CNS-ATM/bluesky-gym](https://github.com/TUDelft-CNS-ATM/bluesky-gym) / MIT | Yeni: 23-aviation-data-training.md |
| `Ysurac/FlightAirMap` | [Ysurac/FlightAirMap](https://github.com/Ysurac/FlightAirMap) / AGPL-3.0 | Yeni: 23-aviation-data-training.md |
| `JSBSim-Team/jsbsim` | [JSBSim-Team/jsbsim](https://github.com/JSBSim-Team/jsbsim) / LGPL-2.1 | Yeni: 23-aviation-data-training.md |
| `FlightGear/flightgear` | [FlightGear/flightgear](https://github.com/FlightGear/flightgear) / GPL-2.0 | Yeni: 23-aviation-data-training.md |
| `networkx/networkx` | [networkx/networkx](https://github.com/networkx/networkx) / NOASSERTION | Yeni: 23-aviation-data-training.md |
| `geopandas/geopandas` | [geopandas/geopandas](https://github.com/geopandas/geopandas) / BSD-3-Clause | Yeni: 23-aviation-data-training.md |
| `pandas-dev/pandas` | [pandas-dev/pandas](https://github.com/pandas-dev/pandas) / BSD-3-Clause | Yeni: 23-aviation-data-training.md |
| `pola-rs/polars` | [pola-rs/polars](https://github.com/pola-rs/polars) / MIT | Yeni: 23-aviation-data-training.md |
| `dask/dask` | [dask/dask](https://github.com/dask/dask) / BSD-3-Clause | Yeni: 23-aviation-data-training.md |
| `scikit-learn/scikit-learn` | [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) / BSD-3-Clause | Mevcut: 05-llm-infrastructure-local-ai.md |
| `statsmodels/statsmodels` | [statsmodels/statsmodels](https://github.com/statsmodels/statsmodels) / BSD-3-Clause | Yeni: 23-aviation-data-training.md |
| `unit8co/darts` | [unit8co/darts](https://github.com/unit8co/darts) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `facebook/prophet` | [meta/prophet](https://github.com/meta/prophet) / MIT | Yeni: 23-aviation-data-training.md |
| `dmlc/xgboost` | [dmlc/xgboost](https://github.com/dmlc/xgboost) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `microsoft/LightGBM` | [lightgbm-org/LightGBM](https://github.com/lightgbm-org/LightGBM) / MIT | Yeni: 23-aviation-data-training.md |
| `google/or-tools` | [google/or-tools](https://github.com/google/or-tools) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `Pyomo/pyomo` | [Pyomo/pyomo](https://github.com/Pyomo/pyomo) / NOASSERTION | Yeni: 23-aviation-data-training.md |
| `coin-or/pulp` | [coin-or/pulp](https://github.com/coin-or/pulp) / NOASSERTION | Yeni: 23-aviation-data-training.md |
| `jupyterlab/jupyterlab` | [jupyterlab/jupyterlab](https://github.com/jupyterlab/jupyterlab) / BSD-3-Clause | Yeni: 23-aviation-data-training.md |
| `metabase/metabase` | [metabase/metabase](https://github.com/metabase/metabase) / NOASSERTION | Mevcut: 07-data-analytics-charts.md |
| `apache/superset` | [apache/superset](https://github.com/apache/superset) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `dbt-labs/dbt-core` | [dbt-labs/dbt](https://github.com/dbt-labs/dbt) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `PostHog/posthog` | [PostHog/posthog](https://github.com/PostHog/posthog) / NOASSERTION | Mevcut: 07-data-analytics-charts.md |
| `keycloak/keycloak` | [keycloak/keycloak](https://github.com/keycloak/keycloak) / Apache-2.0 | Mevcut: 08-security-osint.md |
| `nextauthjs/next-auth` | [nextauthjs/next-auth](https://github.com/nextauthjs/next-auth) / ISC | Yeni: 23-aviation-data-training.md |
| `ory/hydra` | [ory/hydra](https://github.com/ory/hydra) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `zitadel/zitadel` | [zitadel/zitadel](https://github.com/zitadel/zitadel) / AGPL-3.0 | Yeni: 23-aviation-data-training.md |
| `langchain-ai/langgraph` | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) / MIT | Mevcut: 02-multi-agent-frameworks.md |
| `crewAIInc/crewAI` | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) / MIT | Mevcut: 02-multi-agent-frameworks.md |
| `langgenius/dify` | [langgenius/dify](https://github.com/langgenius/dify) / NOASSERTION | Mevcut: 17-nocode-visual-ai-builders.md |
| `n8n-io/n8n` | [n8n-io/n8n](https://github.com/n8n-io/n8n) / NOASSERTION | Mevcut: 04-browser-scraping-automation.md |
| `kestra-io/kestra` | [kestra-io/kestra](https://github.com/kestra-io/kestra) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
| `BerriAI/litellm` | [BerriAI/litellm](https://github.com/BerriAI/litellm) / NOASSERTION | Mevcut: 05-llm-infrastructure-local-ai.md |
| `modelcontextprotocol/typescript-sdk` | [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) / NOASSERTION | Yeni: 23-aviation-data-training.md |
| `modelcontextprotocol/python-sdk` | [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) / MIT | Yeni: 23-aviation-data-training.md |
| `github/github-mcp-server` | [github/github-mcp-server](https://github.com/github/github-mcp-server) / MIT | Mevcut: 01-claude-code-ai-dev-tools.md |
| `bytebase/dbhub` | [bytebase/dbhub](https://github.com/bytebase/dbhub) / MIT | Yeni: 23-aviation-data-training.md |
| `docusealco/docuseal` | [docusealco/docuseal](https://github.com/docusealco/docuseal) / AGPL-3.0 | Yeni: 23-aviation-data-training.md |
| `graphomy/graphsign.ink` | [graphomy/graphsign.ink](https://github.com/graphomy/graphsign.ink) / AGPL-3.0 | Yeni: 23-aviation-data-training.md |
| `bytecrunch-io/openclm` | [bytecrunch-io/openclm](https://github.com/bytecrunch-io/openclm) / AGPL-3.0 | Yeni: 23-aviation-data-training.md |
| `penpact/penpact` | [penpact/penpact](https://github.com/penpact/penpact) / AGPL-3.0 | Yeni: 23-aviation-data-training.md |
| `minio/minio` | [minio/minio](https://github.com/minio/minio) / AGPL-3.0 | Yeni: 23-aviation-data-training.md; yalnız tarihsel referans |
| `prometheus/prometheus` | [prometheus/prometheus](https://github.com/prometheus/prometheus) / Apache-2.0 | Mevcut: 07-data-analytics-charts.md |
| `grafana/grafana` | [grafana/grafana](https://github.com/grafana/grafana) / AGPL-3.0 | Mevcut: 07-data-analytics-charts.md |
| `open-telemetry/opentelemetry-go` | [open-telemetry/opentelemetry-go](https://github.com/open-telemetry/opentelemetry-go) / Apache-2.0 | Yeni: 23-aviation-data-training.md |
