# Safari MCP incelemesi — 11 Kasım 2026

Yerel sürüm: Safari 26.5.2; yerleşik `safaridriver --mcp` desteklenmiyor. Aşağıdaki iki proje yerleşik sunucudan bağımsızdır. Bu inceleme statiktir: kurulmadı, Safari üzerinde çalıştırılmadı, bağımlılıkların tamamı denetlenmedi. Güvenlik sertifikası değildir.

## Karşılaştırma

| Proje | Gözlenen metadata | Yöntem | Karar |
|---|---|---|---|
| [Epistates/MCPSafari](https://github.com/Epistates/MCPSafari) | 64 yıldız, MIT, son push 6 Kasım; son yayın v0.3.2 / 14 Eylül | Swift + Safari MV3 extension; macOS 14+, Safari 17+ | Site bazlı izin yaklaşımı iyi. İncelenen main v0.4.0 içeriyor; yeni HMAC handshake ve diğer korumalar v0.3.2 yayınının özelliği sayılmamalı. |
| [achiya-automation/safari-mcp](https://github.com/achiya-automation/safari-mcp) | 241 yıldız, MIT, son push 10 Kasım; yayın v2.23.0 / 28 Ekim | Node 20+, AppleScript/JXA, Swift helper, isteğe bağlı extension/HTTP | Mevcut Safari için pilot adayı. Daha geniş erişim yüzeyi; yayımlanan sürüm sabitlenerek ve test sayfalarında denenmeli. |

Yıldız sayıları güvenlik kanıtı değildir. Achiya'nın %60 CPU tasarrufu iddiası bağımsız ölçülmedi; RAM tasarrufu garantisi yoktur.

## Kaynak kod bulguları

- Epistates `MCPServer/Sources/mcp-safari/WebSocketBridge.swift`: loopback bind, origin kontrolü, authentication akışı. `BridgeHandshake.swift`: HMAC tabanlı karşılıklı challenge. `SECURITY.md`: v0.4 protokolünün 0.3.x ile uyumsuzluğu açıkça yazılı. Yayın ile main farkı kritik.
- Epistates manifest `<all_urls>` istiyor; Safari site izinleri localhost ve test alanlarıyla sınırlandırılmalı. Native input için Accessibility gerekebilir.
- Achiya `transport.js`: varsayılan stdio; isteğe bağlı HTTP 127.0.0.1 ve Host/Origin kontrolleri. SECURITY.md'nin “port açılmaz” genellemesi mevcut kodu tam anlatmıyor.
- Achiya `scripts/postinstall.cjs`: paket içindeki Swift helper için ad-hoc codesign çalıştırıyor. Kaynak incelendi; prebuilt binary'nin kaynakla birebir eşleştiği doğrulanmadı.
- Achiya JavaScript from Apple Events ister; native input ve ekran görüntüsü yolları ek macOS izinleri gerektirebilir. Tab ownership guard mevcut, güvenlik izolasyonunun tamamı değildir.
- Her ikisinin kaynak ağacında testler mevcut. Bu incelemede testler ve live Safari senaryoları çalıştırılmadı.

## İstemciler

Ayrı bir “Anthropic Safari” veya “OpenAI Safari” sunucusu gerekmez: uyumlu MCP istemcisi aynı sunucuyu kullanabilir. Claude Code ve Codex yerel stdio destekler. Claude Desktop yerel MCP/extension yolunu destekler; Claude web bağlantısı aynı mekanizma değildir.

- [Claude yerel MCP belgesi](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [Codex MCP belgesi](https://learn.chatgpt.com/docs/extend/mcp)
- [Perplexity resmî MCP açıklaması](https://www.perplexity.ai/en-GB/hub/blog/mcp-tools): Mac uygulamasında yerel MCP; plan ve sürüm uygunluğu ayrıca kontrol edilir.
- [Perplexity resmî MCP deposu](https://github.com/perplexityai/modelcontextprotocol): arama/araştırma API araçları sunar, Safari kontrol sunucusu değildir.

Resmî Anthropic/OpenAI/Perplexity Safari denetim deposu bu araştırmada doğrulanmadı. İlave topluluk adayları: handlecusion/agent-safari ve tszaks/safari-mcp; kodları incelenmedi, öneri/kurulum onayı verilmedi.

## KVKK/GDPR ve uygulama

Yerel MCP işlemesi, verinin cihazdan hiç çıkmadığı anlamına gelmez. DOM, form, ağ ve ekran görüntüsü çıktıları seçilen AI sağlayıcısına gönderilebilir. Müşteri PII'si, yönetici oturumları ve ödeme sayfalarıyla pilot yapılmamalı; sentetik veri ve localhost kullanılmalı. Sunucuyu internete açmayın. Sürümü sabitleyin; iki Safari sunucusunu birden etkinleştirmeyin.

Portföy entegrasyonu: B2BLife/RoboCheckIn/TSA/KredimPlus için yerel Safari form ve responsive QA. HomeLab için yalnızca sentetik veri; gerçek kullanıcı verisi cihazdan çıkmamalı. İçerik fikri: “Chrome açmadan Claude/Codex ile Safari testi”. Doğrudan MRR artışı ölçülmedi; ilk pilot planlama tahmini 30–60 dakika, macOS izinlerine bağlı.

Dağıtım değişikliği yok. NotebookLM'e eklenmek üzere bu rapor hazırlandı; uzaktan notebook güncellemesi yapılmadı.
