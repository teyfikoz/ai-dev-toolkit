# API ve GitHub dışı kaynak defteri — 16 Kasım 2026

HTTP erişimi, entegrasyon testi veya kullanım lisansı onayı değildir. Tam şartları incelenmemiş kaynaklar açıkça sınırlandırıldı. Kimlik bilgisi, hasta/konum/kişi verisi gönderilmedi.

| Kaynak | Uygulama | Değerlendirme | Erişim |
|---|---|---|---|
| [OpenStreetMap data](https://www.openstreetmap.org/copyright) | LayOverKit,Scuplan,B2BLife | ODbL attribution/share-alike requirements differ from software; public tile service is not unlimited production hosting. | REACHABLE / 200 |
| [OSM public tiles policy](https://operations.osmfoundation.org/policies/tiles/) | LayOverKit,Scuplan,B2BLife | Use suitable provider/selfhost; offline bulk downloads and production traffic must follow provider policy. | REACHABLE / 200 |
| [Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API) | LayOverKit | POI ingestion candidate, not guaranteed live opening/access status; public endpoints need limits/cache. | REACHABLE / 200 |
| [OurAirports](https://ourairports.com/data/) | LayOverKit,How2TakeOff | Airport catalog, not licensed complete lounge or terminal services database; GitHub dataset verified separately. | NOT_VERIFIED_IN_THIS_ENVIRONMENT / — |
| [Wikidata Query Service](https://query.wikidata.org/) | LayOverKit,B2BLife | Public structured facts vary; retain provenance and verification date. | REACHABLE / 200 |
| [Wikimedia Commons reuse](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia) | LayOverKit,Scuplan,SciBreak | Per-file license and attribution; public availability is not unrestricted image reuse. | REACHABLE / 200 |
| [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/) | SciBreak | Official event data with timestamp/source; draft editorial queue, no automatic emergency assertion. | REACHABLE / 200 |
| [USGS Volcano Hazards](https://www.usgs.gov/programs/VHP) | SciBreak | Official US monitoring resource; not universal global alarm coverage. | HTTP_RESTRICTED_OR_NOT_FOUND / 403 |
| [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) | SciBreak | Thermal anomalies are not independently confirmed incidents or a substitute for official local alerts. | REACHABLE / 200 |
| [NASA EONET](https://eonet.gsfc.nasa.gov/docs/v3) | SciBreak | Event metadata with sources; corroborate before content publishing. | REACHABLE / 200 |
| [NASA Worldview](https://worldview.earthdata.nasa.gov/) | SciBreak | Earth observation visualization, not arbitrary camera access. | REACHABLE / 200 |
| [NOAA Tides & Currents](https://tidesandcurrents.noaa.gov/api/) | Scuplan | Geographical/station coverage and datum/timezone matter; no automatic dive safety decision. | REACHABLE / 200 |
| [Copernicus Marine](https://help.marine.copernicus.eu/en/articles/8630590-copernicus-marine-toolbox-faq) | Scuplan,SciBreak | Official source identifies mercator-ocean/copernicus-marine-toolbox. Dataset conditions and credentials evaluated separately; no data downloaded. | REACHABLE / 200 |
| [OpenMeteo](https://open-meteo.com/) | Scuplan,SciBreak | API docs state noncommercial free tier; commercial use may require subscription. Data CC-BY4 differs from software AGPL. Do not assume unlimited commercial free service. | REACHABLE / 200 |
| [StormGlass](https://stormglass.io/) | Scuplan | Official page free tier10requests/day, NOT commercial use. Paid plan limits vary; no paid request/registration made. | REACHABLE / 200 |
| [WorldTides](https://www.worldtides.info/) | Scuplan | Credits/API plan required; trial credits do not establish perpetually free production use. | REACHABLE / 200 |
| [OpenCorporates](https://api.opencorporates.com/) | B2BLife | Company lookup/data access with licensing/pricing options; not company-incorporation filing API. | REACHABLE / 200 |
| [Companies House](https://developer.company-information.service.gov.uk/) | B2BLife | Official overview supports company information retrieval. Public lookup API does not by itself authorize incorporation filing. | REACHABLE / 200 |
| [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html) | B2BLife | Only employers using that ATS; ingestion/republication conditions and updates need review. | REACHABLE / 200 |
| [Lever Postings API](https://github.com/lever/postings-api) | B2BLife | Employer-specific postings, not all jobs; consent/reuse conditions separate. | REACHABLE / 200 |
| [FHIR standard](https://hl7.org/fhir/) | HomeLab reference only | DO NOT add remote patient server: HomeLab must stay100%device-local localStorage. Standard/repo presence is not approval for clinical diagnosis. | REACHABLE / 200 |
| [DICOM standard](https://www.dicomstandard.org/) | HomeLab reference only | No remote PACS/data upload; research reference outside current local-only MVP. | REACHABLE / 200 |
| [LOINC](https://loinc.org/) | HomeLab reference only | Terminology/license conditions separate; preserve original units/reference intervals, no personal diagnostic score. | HTTP_RESTRICTED_OR_NOT_FOUND / 403 |
| [Android CallScreeningService](https://developer.android.com/reference/android/telecom/CallScreeningService) | SmartBlock | Local call decisions with user-granted role; messaging/VPN does not replace carrier call screening. | REACHABLE / 200 |
| [Apple Call Directory](https://developer.apple.com/documentation/callkit/cxcalldirectoryprovider) | SmartBlock | iOS list extension differs from Android. No new timed native blocking engine claimed. | REACHABLE / 200 |
| [Apple Live Caller ID](https://developer.apple.com/documentation/identitylookup/getting-up-to-date-calling-and-blocking-information-for-your-app) | SmartBlock | Official identitylookup documentation requires relay/server infrastructure; old /documentation/livecalleridlookup returned404. Not assumed equivalent to ondevice timed filtering. | REACHABLE / 200 |
| [Briar source](https://code.briarproject.org/briar/briar) | SmartBlock separate research | Actual nonGitHub hosting; no app installed. Published F-Droid fingerprint verified separately, not independent APK signature verification. | REACHABLE / 200 |
| [SatNOGS source](https://gitlab.com/librespacefoundation/satnogs/satnogs-client) | SciBreak | Official SatNOGS wiki identifies GitLab source; guessed GitHub owner was unresolved and is not treated as canonical. | REACHABLE / 200 |
| [Jami source](https://git.jami.net/savoirfairelinux/jami) | SmartBlock separate research | User-provided actual nonGitHub hosting, not CallScreening dependency. | REACHABLE / 200 |
| [Tor Browser source](https://gitlab.torproject.org/tpo/applications/tor-browser) | SmartBlock separate research | Privacy browser source; no anonymity guarantee or installation made. | HTTP_RESTRICTED_OR_NOT_FOUND / 403 |
| [Tails source](https://gitlab.tails.boum.org/tails/tails) | Security research reference | Operating system source, not a mobile SDK to embed. | REACHABLE / 200 |
| [Postmark](https://postmarkapp.com/) | B2BLife,RoboCheckIn | Transactional mail service, not a free open-source drop-in; no message sent. | REACHABLE / 200 |
| [Hetzner Object Storage](https://www.hetzner.com/storage/object-storage/overview/) | B2BLife,TSA | Corrected official URL; old /cloud/storage/object-storage returned404. For permitted product files; HomeLab health data stays ondevice. | REACHABLE / 200 |
| [Groq docs](https://console.groq.com/docs/overview) | B2BLife,TSA,content | Optional provider only; no contacts/call audio/health images sent and no new paid call performed. | REACHABLE / 200 |
| [MCP official introduction](https://modelcontextprotocol.io/introduction) | Development tools | Tool protocol, not a map/medical/registry data source or permission bypass. | REACHABLE / 200 |
| [OpenDiveMap](https://opendivemap.com/docs) | Scuplan | Official docs describe GeoJSON RESTAPI and versioned changes; databaseODbL from officialAbout. Do not assume every point is verifiedsafe; no liveAPIquery performed. | REACHABLE / 200 |
| [OpenDeepMap](https://opendeepmap.com/) | Scuplan | Separate project from OpenDiveMap. Official page claims ODbL database and per-media CC-BY/BY-SA; validate individualrecord/source before import. | REACHABLE / 200 |
| [Dive Vibe Community](https://divevibe.io/faqs) | Scuplan | OfficialFAQ links jbunderwater/dive-vibe-community; admits AI-assisted seeds and some nondivesite markers. Verificationandrights gate before ingestion. | REACHABLE / 200 |
| [David Rumsey collection permissions](https://www.davidrumsey.com/about/copyright-and-permissions) | LayOverKit,Grimfiles | Collection and georeferencing are not a universally reusable API license. Image/item permissions checked separately; no historical map image copied. | REACHABLE / 200 |
| [Nominatim](https://nominatim.org/release-docs/latest/api/Overview/) | B2BLife,LayOverKit | Geocoding documentation only; public service usage policy and addressprivacy need review. | REACHABLE / 200 |
| [Stripe Connect](https://docs.stripe.com/connect) | B2BLife | Commercial payment platform; country, onboarding and marketplace flow verified separately before contracting; no payment or account created. | REACHABLE / 200 |
| [iyzico](https://docs.iyzico.com/) | B2BLife | Commercial payment platform; no universalfree payment service or authorization inferred from docs. | REACHABLE / 200 |
| [F-Droid documentation](https://f-droid.org/en/docs/) | SmartBlock separate research | Official docs link project components on GitLab and describe signing/reproducibility. Wrong GitHub path is not an install source; nothing installed. | REACHABLE / 200 |
| [UnifiedPush](https://unifiedpush.org/) | SmartBlock separate research | Push ecosystem with distributor choice, not call screening or free carrier connectivity; official site links Codeberg. No arbitrary GitHub repository invented. | REACHABLE / 200 |

## Açık kalan kapsam

Evren API, Mantis, ShopClass, Runway/open-source ecosystems ve sağlayıcısı belirtilmemiş ülke kuruluş APIleri için kesin ürün/kanonik adres belirlenmedi. Atlasr, GitHub metadata tablosunda artık atlasr-org/atlasr olarak doğrulandı. İsimden entegrasyon uydurulmadı. LoungeBuddy/PriorityPass/DragonPass üyelik ve görsel verileri lisanslı anlaşma olmadan kopyalanmadı. Devlet portalları ve ticari sağlayıcılar için kurulum/ödeme/kayıt/başvuru yapılmadı.

MERSIS/Estonya/ABD kuruluş süreçleri hukukî uygunluk ve temsil yetkisi gerektirir; burada ülke bazında dosyalama izni doğrulandığı iddia edilmez. Önce yalnız kaynaklı rehber ve resmî yönlendirme kapsamı uygundur.

Son kontrol UTC: 2026-11-17T03:07:07.644532+00:00
