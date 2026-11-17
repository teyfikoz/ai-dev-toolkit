"""Apply narrow collection guards, keeping the live broadcast functions intact."""
import ast
from pathlib import Path
import sys


def insert_guard(source,name,body):
 tree=ast.parse(source)
 function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
 first=function.body[0]
 after=(first.end_lineno if isinstance(first,ast.Expr) and isinstance(first.value,ast.Constant) and isinstance(first.value.value,str) else function.lineno)
 lines=source.splitlines(keepends=True)
 lines[after:after]=[line+'\n' for line in body.splitlines()]
 return ''.join(lines)


def patch(source,name):
 original_source = source
 if 'from scibreak_disk_budget import' in source:raise ValueError('Already patched')
 source=source.replace('from pathlib import Path','from pathlib import Path\nfrom scibreak_disk_budget import collection_allowed, single_collector',1)
 if name=='scibreak_monitor.py':
  source=source.replace('def run_once(only:', '@single_collector("monitor")\ndef run_once(only:',1)
  source=insert_guard(source,'run_once','    if not collection_allowed():\n        log("LOW_DISK: new collections paused below 5.5 GiB; cached state retained")\n        return')
  source=source.replace('    for name, fn in ALL_SOURCES.items():','    for name, fn in ALL_SOURCES.items():\n        if not collection_allowed():\n            log("LOW_DISK: remaining collections paused")\n            return',1)
  source=insert_guard(source,'save_img','    if not collection_allowed():\n        raise RuntimeError("LOW_DISK: image collection paused")')
  source=insert_guard(source,'enqueue','    if not collection_allowed():\n        return')
 elif name=='scibreak_data_overlay.py':
  source=source.replace('def watch_loop():','@single_collector("overlay")\ndef watch_loop():',1)
  source=source.replace('    while True:\n        try:', '    while True:\n        if not collection_allowed():\n            log("LOW_DISK: overlay collection paused; cached overlay retained")\n            time.sleep(60)\n            continue\n        try:',1)
  source=insert_guard(source,'update_cache','    if not collection_allowed():\n        try:\n            return json.loads(DATA_CACHE.read_text())\n        except (OSError, ValueError):\n            return {}')
  for function in ('render_overlay_card','push_data_discovery'):
   source=insert_guard(source,function,'    if not collection_allowed():\n        return None')
 elif name=='scibreak_live_director.py':
  source=insert_guard(source,'fetch_goes_frame','    if not collection_allowed():\n        return out_path.is_file() and out_path.stat().st_size > 0')
  source=source.replace('        if ok:\n            dest = FRAME_DIR / f"goes_{i:03d}.jpg"','        if ok and not collection_allowed():\n            collected.append(str(img_path))\n        elif ok:\n            dest = FRAME_DIR / f"goes_{i:03d}.jpg"',1)
  source=insert_guard(source,'_frame_capture_loop','    if not collection_allowed():\n        log("LOW_DISK: discovery frame capture paused; live stream unchanged")\n        return')
  source=source.replace('        f"SECONDS=0\\n"', '''        f"exec 9>'{FRAME_DIR}/.capture.lock'\\n"
        f"flock -n 9 || exit 0\\n"
        f"SECONDS=0\\n"''',1)
  source=source.replace('        f"  TS=$(date -u +%Y%m%d_%H%M%S)\\n"', '''        f"  if ! python3 '{Path(__file__).parent}/scibreak_disk_budget.py' --check >/dev/null 2>&1; then sleep 60; continue; fi\\n"
        f"  TS=$(date -u +%Y%m%d_%H%M%S)\\n"''',1)
  source=source.replace('f"  ffmpeg -y -i', 'f"  timeout 20 ffmpeg -nostdin -y -i',1)
  # Verify broadcast and fallback functions were not changed by this patch.
  before={n.name:ast.dump(n) for n in ast.parse(original_source).body if isinstance(n,ast.FunctionDef)}
  after={n.name:ast.dump(n) for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)}
  for function in ('stream_hls_to_rtmp', '_stream_fallback_card', 'stream_category', 'main_stream'):
   assert before[function] == after[function], 'Broadcast function changed: ' + function
 else:raise ValueError(name)
 ast.parse(source)
 return source


if __name__=='__main__':
 source,output=map(Path,sys.argv[1:]);output.write_text(patch(source.read_text(),source.name))
