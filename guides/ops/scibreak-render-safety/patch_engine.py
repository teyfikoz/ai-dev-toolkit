"""Bound discovery rendering without changing streaming or deleting old outputs."""
from pathlib import Path
import sys

HELPERS = '''
# Bounded offline rendering. No cleanup of historical outputs is automatic.
MIN_RENDER_FREE = 5 * 1024 ** 3
MAX_RENDER_BYTES = 512 * 1024 ** 2
MAX_SHORTS_BYTES = 150 * 1024 ** 2

def render_budget_available() -> bool:
    # Reserve enough for the whole capped next file, not just current free bytes.
    return shutil.disk_usage(OUT).free >= MIN_RENDER_FREE + MAX_RENDER_BYTES


def _shorts_command(overlay: Path, output: Path, duration: int = 58) -> list[str]:
    return [
        "ffmpeg", "-nostdin", "-y", "-loop", "1", "-i", str(overlay),
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        # Output options MUST follow all inputs. Input-only -t leaves video infinite.
        "-t", str(duration), "-fs", str(MAX_SHORTS_BYTES),
        "-c:v", "libx264", "-threads", "2", "-preset", "veryfast", "-b:v", "2000k",
        "-c:a", "aac", "-b:a", "64k", "-pix_fmt", "yuv420p", "-vf", "fps=30",
        "-movflags", "+faststart", str(output),
    ]


def _acquire_discovery_lock():
    handle = (ROOT / ".discovery-engine.lock").open("a")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return None
    return handle

'''

def patch(source: str) -> str:
    if 'def render_budget_available' in source:
        raise ValueError('Already patched')
    source=source.replace('import argparse, base64, json, os, subprocess, sys, time, textwrap, urllib.request, urllib.error',
        'import argparse, base64, json, os, subprocess, sys, time, textwrap, urllib.request, urllib.error\nimport shutil\nimport fcntl')
    at=source.index('def make_shorts_clip(')
    source=source[:at]+HELPERS+'\n'+source[at:]
    source=source.replace('    if not PIL_OK:\n        return None\n    ts      = frame_path.stem',
        '    if not PIL_OK or not render_budget_available():\n        return None\n    ts      = frame_path.stem',1)
    start=source.index('    cmd = [',source.index('def make_shorts_clip('))
    end=source.index('    r = subprocess.run(',start)
    source=source[:start]+'    cmd = _shorts_command(overlay, out)\n'+source[end:]
    source=source.replace('    ts  = frame_path.stem\n    out = CLIPS_DIR / f"longform_{ts}.mp4"',
        '    if not render_budget_available():\n        return None\n    ts  = frame_path.stem\n    out = CLIPS_DIR / f"longform_{ts}.mp4"',1)
    # Bound existing long-form commands too. Preserve their existing output duration.
    a=source.index('def make_longform_video(');b=source.index('# ─── Tier 3:',a)
    section=source[a:b].replace('"ffmpeg", "-y",','"ffmpeg", "-nostdin", "-y",').replace('"-c:v", "libx264", "-preset",','"-fs", str(MAX_RENDER_BYTES), "-c:v", "libx264", "-threads", "2", "-preset",')
    source=source[:a]+section+source[b:]
    source=source.replace('def process_queue():\n', 'def process_queue():\n    if not render_budget_available():\n        log("Discovery rendering paused: less than 5 GiB plus next-file budget available")\n        return\n',1)
    # A queue iteration may contain many entries; recheck before each expensive task.
    source=source.replace('    for line in DISC_QUEUE.read_text().splitlines():\n',
        '    for line in DISC_QUEUE.read_text().splitlines():\n        if not render_budget_available():\n            log("Discovery rendering paused: disk budget exhausted")\n            return\n',1)
    source=source.replace('    if a.watch:\n        watch_loop()',
        '    if a.watch:\n        _discovery_lock = _acquire_discovery_lock()\n        if _discovery_lock is None:\n            log("Discovery engine already running; duplicate watcher exits")\n            sys.exit(0)\n        watch_loop()',1)
    return source

if __name__ == '__main__':
    origin, output = map(Path, sys.argv[1:])
    output.write_text(patch(origin.read_text()))
