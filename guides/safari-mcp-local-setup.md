# Yerel Safari MCP kurulumu — 11 Kasım 2026

## Kurulum

- Paket: achiya-automation/safari-mcp, npm sürümü **2.23.0**, exact dependency ve package-lock ile sabit.
- Dizin: `~/.local/share/safari-mcp/`
- Command: `/opt/homebrew/bin/node`
- Argüman: `/Users/teyfikoz/.local/share/safari-mcp/node_modules/safari-mcp/index.js`
- İstemci kayıt adı: `safari`; varsayılan stdio. İstemci açıldığında başlar; ek bir login service kurulmadı.
- Eski ayarların yedekleri: `~/.local/share/safari-mcp/backups/20261111-195908/`. Bu yedekler secret içerebilir; Git'e eklenmemeli.

## Yapılandırılan istemciler

Claude Code user config, Claude Desktop, Codex global config, Gemini CLI user settings, Antigravity global MCP config ve Antigravity IDE config. Önceki kayıtlar korundu. İstemciler yeniden başlatılmalı veya MCP listesi yenilenmeli. Perplexity ve ChatGPT sohbet uygulamasına bu değişiklikler otomatik aktarılmaz; bu iki arayüz için yapılandırma yapılmadı.

## Doğrulama

Node v24.6.0 ile MCP initialize + tools/list başarılı, **98 araç** keşfedildi. Bu, protokol testidir; her istemcinin arayüzü ve her araç ayrı ayrı canlı test edilmedi.

Safari 26.5.2 üzerinde Geliştirici → “Apple Olayları’ndan JavaScript’e izin ver” kapalı olarak gözlendi. Güvenlik erişimini açmak için kullanıcıya ayrıca onay soruldu. Onay gelmeden ayar değiştirilmedi; canlı sayfa testi bekliyor.

Automation → Safari izinleri uygulama başına macOS tarafından sorulabilir. Screen Recording ve Accessibility izinleri verilmedi; native input ve screenshot için gerektiğinde ayrıca ele alınır. İmzalanmamış eklenti izni açılmadı.

## Kullanım

“Safari MCP kullanarak yeni sekmede https://example.com aç, başlığını ve sayfa metnini doğrula.”

Antigravity'nin yerleşik browser aracı Safari'ye otomatik dönüşmez; görevde Safari MCP belirtilmeli. İstemci onayları devre dışı bırakılmadı.

## Veri

Tarayıcı araç çıktıları seçilen model sağlayıcısına gönderilebilir. Gerçek müşteri PII'si yerine localhost/sentetik test verisi kullanılmalı. Doğrudan gelir artışı ölçülmedi; amaç Safari QA ve Chrome gereksinimini azaltmak.

Deployment değişikliği yok. NotebookLM için bu rehber kaynak olarak hazır; notebook'a yüklenmedi.

## Canlı test sonucu

Kullanıcının izin ayarı sonrasında sandbox dışında MCP testi başarılı: safari_doctor **5/6**, Apple Events/Automation OK, native helper ve Accessibility kontrolü başarılı. `safari_new_tab` ile https://example.com/ yeni sekmede açıldı; `safari_read_page` başlığı **Example Domain** ve sayfa metnini döndürdü. Safari üzerinde JavaScript/DOM okuma canlı doğrulandı.

Screen Recording izni eksik; ekran görüntüsü/PDF doğrulanmadı. Safari eklentisi bağlı değil, çalışan yol AppleScript. Her istemcinin kendi macOS izin zinciri ayrıca sorulabilir; tüm istemcilerin arayüzleri tek tek canlı denenmedi. Sandbox içindeki süreç kontrolü yanlış şekilde Safari çalışmıyor sonucu verdi; sandbox dışı test gerçek durumu doğruladı.
