# Android emulator helpers for native Instagram publishing

Used on a dedicated, authorised test emulator to publish your own accounts' Reels and Stories with Instagram catalogue music (the Graph API cannot add catalogue music).

- `emu.py` — `shot`, `ui [filter]`, `tap x y`, `tapt TEXT`, `swipe`, `launch`. uiautomator dump with password fields redacted.
- `ig_reel.py prepare` — pick newest gallery video, search catalogue music (optionally royalty-free only), set music volume, type caption, enable the AI label. Stops on the share screen for a visual check. `--no-music` keeps the file's own audio.
- `ig_type.py` — Unicode caption entry through ADBKeyboard (`com.android.adbkeyboard/.AdbIME` must be the active IME).
- `emu_push.sh` — push media into `/sdcard/DCIM/Camera` and trigger a media scan.

## Lessons

- uiautomator cannot dump while video autoplays; start flows from the profile tab and keep coordinate fallbacks.
- Instagram may show an "Edits" promo sheet on Next; close it with `Close sheet`.
- Long-pressing Share publishes immediately. In some app builds the schedule option is missing even after switching to a Creator profile.
- Music around 32–37 with narration at 100 stays audible; 19 was reported as inaudible.
- An emulator with ~2.5 GB RAM triggers Instagram ANRs; force-stop and relaunch, nothing is lost before Share.
