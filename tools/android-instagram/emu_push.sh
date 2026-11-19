#!/bin/zsh
# push a local video into the emulator gallery so it appears first in Recents
f=$1; n=$(basename $f)
adb -s emulator-5580 push "$f" /sdcard/DCIM/Camera/$n >/dev/null && adb -s emulator-5580 shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM/Camera/$n >/dev/null && echo pushed $n
