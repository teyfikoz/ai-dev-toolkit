# Local Shorts Factory (zero paid APIs)

Produces vertical Shorts/Reels and 16:9 long-form videos entirely on a laptop, then schedules them on YouTube with read-back verification.

- `selfix_viral.py` — renderer. Supertonic-3 local TTS (multi-voice dialogue skits), Pillow animation (chat bubbles, karaoke word reveal, numbered lists, chaptered long-form), numpy-synthesised original music bed. Writes two masters per job: `_IG` (voice only, so Instagram catalogue music can be added natively) and `_YT` (voice + original music).
- `content.py` — scripts (original writing; research supplied topics/hooks/format only).
- `build_plan.py` — release plan with titles, descriptions, chapters and 9:16 / 16:9 thumbnails.
- `viral_queue.py` — YouTube uploader: live channel identity check, asset hashes, shared daily cap, private upload → processing → thumbnail CDN read-back (pHash) → `publishAt` read-back. Quota rejections reset the job instead of locking it.

## Lessons

- A memory watchdog that kills `ffmpeg` above 50 % pressure will break long renders. The renderer pipes 20-second chunks with retries, then concatenates.
- All channels using one Google Cloud OAuth client share one 10,000-unit daily quota (~6 uploads). Cap each channel locally.
- Copying high-view transcripts sentence by sentence risks YouTube "reused content" and copyright claims. Use them for topic, hook and structure only.
- Shorts covers must be 9:16; verify the `shortsAspectRatio` CDN image, not the 16:9 proxy (`../youtube/shorts_thumbnail_readback.py`).

Usage: `python3 selfix_viral.py --workers 4` then `python3 build_plan.py` then `python3 viral_queue.py` (dry run) / `--execute`.

## Added 20 Nov 2026
- `whatif_viral.py` + `whatif_content.py` — science "What if" Shorts: procedural space/physics illustrations, stat badges, karaoke captions; scripts fact-checked against public sources.
- `promo.py` — app promo Short from real store screenshots in a phone frame, plus App Store / Google Play QR codes.
- `translate_meta.py` — localizes YouTube titles/descriptions into 17 languages (free Groq tier); `viral_queue.py` applies them via `localizations` and verifies by read-back.
