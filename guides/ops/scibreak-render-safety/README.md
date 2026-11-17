# SciBreak bounded render and collection guard

Operational patch tools for the user's existing private SciBreak scripts, not a
new content or camera-access service. They do not contain keys, private source
files, historical videos, RTMP endpoints, or account credentials.

`patch_engine.py ORIGINAL OUTPUT` applies the verified FFmpeg output-duration
fix, resource caps, minimum free-space gate and discovery watcher flock. The
58-second output `-t` follows **all** inputs; the old placement only bounded an
audio input and allowed the looping video output to run until timeout.

`patch_collectors.py ORIGINAL OUTPUT` handles `scibreak_monitor.py`,
`scibreak_data_overlay.py` or `scibreak_live_director.py`, adding shared budget
checks and nonoverlap. Install `scibreak_disk_budget.py` beside those scripts.
Below **5.5 GiB usable free space**, new collection, frame capture, cache updates
and rendering pause. Cached streaming functions are unchanged. Gates do not
remove archives, resize disks, alter reserved blocks, contact APIs or start a
broadcast by themselves.

Do not apply over unknown source versions. Back up current sources/config,
record their hashes, generate outputs separately, compile and run tests before
atomically replacing files. Existing long-running collectors must pick up the
new code; do not restart a public broadcaster blindly. No historic output
cleanup is automatic. These scripts require Unix flock and Python 3.10+.

## Verified incident outcome, 17 November 2026

- Five renderer checks passed, including a real synthetic two-second FFmpeg
  render inspected by ffprobe; seven collector checks passed against actual
  private source copies and again on the server.
- One specifically approved malformed generated MP4 was recorded and truncated;
  valid archives and all other outputs were preserved. Only regenerable caches,
  old archived journals and unused dangling Docker images were otherwise cleaned.
- Discovery watcher rejects duplicates; fresh real monitor invocation below the
  budget emitted LOW_DISK and skipped source calls. New work is intentionally
  paused while capacity remains below the floor.
- No active public broadcaster existed in the prepatch inventory. This work did
  not create a new broadcast. Rights and source suitability must be checked before
  public rebroadcast.

Storage is still constrained. Approve explicit archive offload/retention or more
capacity before resuming production. A gate prevents recurrence from these
collectors; it is not a guarantee against every other process filling the disk.
