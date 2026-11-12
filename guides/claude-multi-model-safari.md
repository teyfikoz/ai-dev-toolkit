# Claude yönetiminde çok modelli proje çalışması

Güncelleme: 12 Kasım 2026. Kullanıcının tercihi: tarayıcı işlemleri Safari; koordinatör Claude Code. Bu dosya talimat ve CLI bağlantı düzenidir, otomatik daemon veya mevcut Codex sohbetini uzaktan yöneten servis değildir.

## Rol dağılımı

| Araç | Görev | Erişim ve sınır |
|---|---|---|
| Claude Code | Kapsam, görev bölme, sonuçları birleştirme, son karar | Orkestratör; her işi tekrar kendi başına üretme |
| Codex CLI | Uygulama, hata düzeltme, test; gerektiğinde bağımsız kod inceleme | ChatGPT oturumu yerelde doğrulandı. Mevcut konuşma yerine yeni CLI oturumu başlar. |
| Gemini CLI | Uzun doküman, kaynaklı araştırma, alternatif teknik inceleme | CLI kurulu; görev özelinde auth/kota hatası dürüstçe raporlanmalı. |
| Kimi K3 | Karmaşık görevde ikinci görüş / alternatif çözüm | NVIDIA kataloğunda moonshotai/kimi-k3 doğrulandı; hesap erişimi/kota henüz canlı denenmedi. Web erişimi yanıtı bekleniyor. |
| NVIDIA NIM | Uygun küçük modelle özet, sınıflandırma; seçili modelle teknik inceleme | NVIDIA_NIM_API_KEY yalnızca ENV. Mevcut yerel secrets dosyasında isim bulundu; değer kopyalanmadı. Ücretsiz sınırsız varsayma. |
| Ücretsiz Perplexity | Kamuya açık kaynak araştırması ve doğrulama | Safari web arayüzü; API veya ücretli MCP planı var sayma. Ücretli plana ihtiyaç çıkarsa durumu bildir. |

## Çalışma sırası

1. Proje AGENTS.md/CLAUDE.md, git status ve ilgili dosyaları oku. Belirsiz hedefi en çok 3 soruyla netleştir. Mevcut kullanıcı değişikliklerini koru.
2. Tek sayfalık görev kartı yaz: hedef, ilgili dosyalar, başarı ölçütü, test, veri sınırı. Tam sohbeti/tüm repoyu her modele aktarma.
3. Rutin görevde bir uygulayıcı yeterlidir. Çok modelli incelemeyi belirsizlik, kritik değişiklik veya inceleme ihtiyacında kullan. Aynı görevi bütün modellere gönderme.
4. Codex uygulayıcı olacaksa ayrı worktree kullan; çalışma dizinini açıkça ver. İkinci model aynı worktree'de eşzamanlı dosya değiştirmesin. Gemini/NIM/Kimi önce öneri/inceleme üretsin. Birleştirme sahibi Claude olsun.
5. Aşağıdaki bounded helper inceleme/araştırma içindir; Codex read-only, Gemini plan modundadır. MCP izinleri bu modlardan bağımsız olabilir: alt göreve tarayıcı/harici yazma işi verme, istemci izinlerini atlatma.
6. Dönen patch/öneriyi oku, ilgili testleri çalıştır. Başarıyı somut kanıtla raporla. Deploy/store release/ad budget değişimi ayrı görev yetkisi gerektirir. AeroTrain tam test paralelliği en çok 2.

## Token ve maliyet

- Başlangıç hedefi: her alt göreve en fazla 24.000 karakter, tek soru, ilgili dosya/satır veya küçük diff. Sınır token ölçümü değildir.
- İlk sonuç kısa bulgular/patch/test özeti olsun. Başarılı işi başka modellere tekrar yaptırma.
- Bütçe/hedef belli değilken pahalı model yükseltmesi veya ücretli fallback açma. 429/kota/ücret uyarısında otomatik tekrar yapma.
- CLI abonelik kotası API kotası değildir. Her sağlayıcının sunduğu usage bilgisini sakla; raporlanmayan token/maliyeti 0 yazma.
- Aynı anda en fazla iki ağır görev; varsayılan sırayla. Her görevde sonuç ve kalan işi kısa handoff olarak kaydet.

## CLI inceleme köprüsü

```sh
python3 ~/Projects/content/ai-dev-toolkit/tools/agent_delegate.py codex --project /absolute/project < task.txt
python3 ~/Projects/content/ai-dev-toolkit/tools/agent_delegate.py gemini --project /absolute/project < task.txt
python3 ~/Projects/content/ai-dev-toolkit/tools/agent_delegate.py nim < public-or-sanitized-task.txt
python3 ~/Projects/content/ai-dev-toolkit/tools/agent_delegate.py kimi-nim < public-or-sanitized-task.txt
```

Önce `--dry-run` ile çağrı planını gör. NIM için anahtar ebeveyn ortamında olmalı; secrets dosyasını komut çıktısına basma, anahtarı görev dosyasına koyma. NIM/Kimi örnekleri bağlantı tarifidir; canlı hesap/model/kota doğrulaması yapılmadı. Otomatik API maliyeti takibi garanti edilmez. CLI timeout alt işlemlerin tümünü sonlandırma garantisi değildir; zaman aşımında süreçleri kontrol et.

Codex'a yazma görevi, Claude tarafından proje özelinde ayrı worktree'de `codex exec --sandbox workspace-write` ile verilir; tehlikeli bypass flag'leri kullanılmaz. Claude Desktop sohbeti shell araçları olmadan CLI orkestrasyonu yapamaz; bu düzen için Claude Code kullan.

## Safari çalışma kuralı

- Chrome yerine `safari` MCP kullan. Kurulu command: `/opt/homebrew/bin/node`; argüman: `~/.local/share/safari-mcp/node_modules/safari-mcp/index.js` (config içinde mutlak yol).
- Claude Code'u yeniden başlat; `/mcp` ile safari durumunu kontrol et. Önce `safari_doctor`, sonra yeni görev sekmesi (`safari_new_tab`). Snapshot/read_page öncelikli; screenshot yalnızca görsel kanıt gerekiyorsa ve 800–1280 px ile.
- App Store Connect, Google Play Console, AdSense, AdMob, Analytics işlerini bu görev sekmelerinde yürüt. Mevcut kişisel sekmeleri otomatik sahiplenme; receipt varsa koru. Aynı anda tek ajan tarayıcıyı kullansın.
- MFA/CAPTCHA/parola veya macOS güvenlik ekranında kullanıcı gerektiğinde devralsın. Cookie/token export etme. Giriş yapılmış sayfaların içeriği modele gidebilir: gerekli bölümü oku, müşteri PII'sini diğer modellere aktarma.
- Reklam bütçesi, ödeme/banka, rol/izin, uygulama yayınlama ve veri silme işlerinde görev kapsamını kontrol et; gerekli son onayı al. Kayıtlı hesaplara erişim genel harcama/yayın izni değildir.
- Uyumsuz site olursa Chrome'a sessizce dönme; engeli bildir. Mevcut yol AppleScript; opsiyonel Safari extension bağlı değil. Bu yüzden bazı SPA/CSP/Shadow DOM işlemleri sınırlı olabilir.

## Doğrulanan durum

12 Kasım: doğrudan safari MCP doctor 6/6. Aynı SDK oturumunda example.com açıldı ve screenshot JPEG çıktısı alındı (59.288 base64 karakter). Tüm mağaza konsolları ve tüm AI uygulamalarının izin zincirleri tek tek denenmedi. Chrome silinmedi/kapatılmadı; tercih talimat olarak değiştirildi.

## Kaynaklar

- https://code.claude.com/docs/en/mcp
- https://geminicli.com/docs/tools/mcp-server/
- https://learn.chatgpt.com/docs/extend/mcp
- https://docs.api.nvidia.com/nim/reference/llm-apis
- https://github.com/achiya-automation/safari-mcp

İçerik fikri: “Claude yönetiminde Codex + Gemini, Chrome açmadan Safari QA”. Portföy kullanımı: B2BLife, RoboCheckIn, TSA ve KredimPlus için Safari QA. Gelir etkisi ölçülmedi; token tasarrufu yüzdesi iddia edilmez.
