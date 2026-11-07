# Big Tech SDK'ları & API İstemcileri

Google, Meta ve Microsoft'un resmi SDK ve API istemci kütüphaneleri.

| # | Repo | Stars | Ne İşe Yarar? | GitHub |
|---|------|-------|--------------|--------|
| 1 | **google-api-python-client** | 7,500 | Google API'lerine Python ile erişim (Drive, Gmail, Calendar, YouTube vb.) | [link](https://github.com/googleapis/google-api-python-client) |
| 2 | **google-api-nodejs-client** | 11,000 | Google API'lerine Node.js ile erişim; OAuth2 dahil | [link](https://github.com/googleapis/google-api-nodejs-client) |
| 3 | **google-api-go-client** | 4,000 | Google API'lerine Go ile erişim | [link](https://github.com/googleapis/google-api-go-client) |
| 4 | **google-api-php-client** | 9,000 | Google API'lerine PHP ile erişim | [link](https://github.com/googleapis/google-api-php-client) |
| 5 | **google-api-ruby-client** | 2,500 | Google API'lerine Ruby ile erişim | [link](https://github.com/googleapis/google-api-ruby-client) |
| 6 | **google-api-javascript-client** | 3,200 | Tarayıcı tabanlı Google API JavaScript istemcisi (GAPI) | [link](https://github.com/google/google-api-javascript-client) |
| 7 | **google-cloud-python** | 5,500 | Google Cloud (BigQuery, GCS, Pub/Sub, Firestore vb.) Python istemcileri | [link](https://github.com/googleapis/google-cloud-python) |
| 8 | **google-cloud-go** | 3,800 | Google Cloud Go istemcileri — production-grade, context.Context tabanlı | [link](https://github.com/googleapis/google-cloud-go) |
| 9 | **google-cloud-java** | 2,200 | Google Cloud Java istemcileri (60+ servis) | [link](https://github.com/googleapis/google-cloud-java) |
| 10 | **google-cloud-node** | 2,400 | Google Cloud Node.js istemcileri | [link](https://github.com/googleapis/google-cloud-node) |
| 11 | **googleapis** | 7,200 | Google API'lerinin resmi protobuf/OpenAPI tanımları (kaynak of truth) | [link](https://github.com/googleapis/googleapis) |
| 12 | **google-services** | 9,500 | Firebase + Google servislerini Android/iOS uygulamalarına entegre etme rehberi ve json örnekleri | [link](https://github.com/googlesamples/google-services) |
| 13 | **google-map-react** | 6,200 | React için Google Maps bileşeni; marker, overlay, cluster desteği | [link](https://github.com/google-map-react/google-map-react) |
| 14 | **google-maps-services-python** | 4,100 | Google Maps Platform Python istemcisi (Directions, Geocoding, Places vb.) | [link](https://github.com/googlemaps/google-maps-services-python) |
| 15 | **facebook-python-business-sdk** | 1,200 | Meta (Facebook) Business API Python SDK — kampanya yönetimi, insights | [link](https://github.com/facebook/facebook-python-business-sdk) |
| 16 | **facebook-php-business-sdk** | 1,100 | Meta (Facebook) Business API PHP SDK | [link](https://github.com/facebook/facebook-php-business-sdk) |
| 17 | **microsoft-authentication-library-for-js** | 4,200 | Microsoft MSAL.js — Azure AD / Entra ID ile OAuth2/OIDC kimlik doğrulama | [link](https://github.com/AzureAD/microsoft-authentication-library-for-js) |
| 18 | **Microsoft365DSC** | 2,100 | Microsoft 365'i kod olarak yönet (Infrastructure as Code); Intune, Teams, SharePoint dahil | [link](https://github.com/Microsoft365DSC/Microsoft365DSC) |
| 19 | **azure-docs** | 10,500 | Azure dokümantasyonu kaynak dosyaları; örnekler ve hızlı başlangıç rehberleri | [link](https://github.com/MicrosoftDocs/azure-docs) |
| 20 | **microsoft-365-docs** | 1,300 | Microsoft 365 resmi dokümantasyonu | [link](https://github.com/MicrosoftDocs/microsoft-365-docs) |
| 21 | **api-guidelines** | 24,000 | Microsoft REST API tasarım rehberi — naming, versioning, pagination, error format standartları | [link](https://github.com/microsoft/api-guidelines) |
| 22 | **public-apis** | 320000 | 14.000+ ücretsiz public API'nin küratörlü listesi — her kategori için ücretsiz veri kaynağı | [link](https://github.com/public-apis/public-apis) |
| 23 | **gemini-api-cli** | ~1,200 | Google Gemini CLI — terminal üzerinden Gemini'ye prompt at, dosya analiz et, multimodal görev çalıştır. **Kullanım:** Mevcut Groq/HF pipeline'larına Gemini alternatif olarak ekle; içerik pipeline research görevi için. | [link](https://github.com/google-gemini/gemini-api-cli) |

## Kasım 2026 — xAI Grok SDK & API Araçları

## xai-org/grok-build
**Repo:** [xai-org/grok-build](https://github.com/xai-org/grok-build) | ★600+ | Apache-2.0
xAI'ın resmi Grok uygulama geliştirme araç takımı — Grok Bot kurulumu, multi-agent desk şablonları, skill tanımları.
- **API Key gerekli mi?** EVET — `XAI_API_KEY` (console.x.ai, ilk $5-25 ücretsiz kredi)
- **Kullanım:** Grok'u XAI_API_KEY ile Astra konseyi 5. üyesi olarak eklemek için; ayrıca B2BLife/TSA agent pipeline'ları için Grok Bot şablonları.

## chenyme/grok2api
**Repo:** [chenyme/grok2api](https://github.com/chenyme/grok2api) | ★2,000+ | MIT
⚠️ **ToS Uyarısı:** xAI web arayüzünü ters-mühendislikle API'ye çeviren resmi olmayan köprü. xAI kullanım koşullarını ihlal eder, hesap askıya alınma riski taşır, her an kırılabilir.
- **API Key gerekli mi?** HAYIR — grok.com oturumu/cookie kullanır
- **Pratiklik:** Tutarsız, güncellemelerde bozulur. Üretim sistemine (Astra) BAĞLANMAZ.
- **Kullanım:** Yalnızca araştırma/test ortamında Grok yeteneklerini keşfetmek için. Canlı trading'de kullanma.

---

**Repo:** [linkedapi-mcp](https://github.com/Linked-API/linkedapi-mcp) | ★63 | MIT | TypeScript
- **Ne yapar?** Claude/Cursor/VS Code üzerinden LinkedIn hesabını programatik kontrol eder. Gönderi paylaşma, profil bilgisi çekme, B2B büyüme otomasyonu.
- **Gerekli:** LINKED_API_TOKEN + IDENTIFICATION_TOKEN (LinkedIn hesabına özgü)
- **Kullanım:** B2BLife ve TechSyncAnalytica için LinkedIn lead generation; cold outreach otomasyonu; haftalık şirket analiz paylaşımı. OCC paneline LinkedIn metrik entegrasyonu.
