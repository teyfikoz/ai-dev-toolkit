"""Instagram native autoposter for emulator-5580 (own accounts only).

  ig_autopost.py run [--dry]      execute due queue items (cron every 10 min)
  ig_autopost.py status           print queue summary
Queue: queue.json  Receipts: receipts.jsonl  Log: autopost.log
Each item: id, account, kind (reel|story|post), due (ISO, Europe/Istanbul), media [paths], caption_file?,
music {mode: auto|catalog|none, query?, rf?}, poll {q,a,b}?, link {url,text}?, status.
Music 'auto' keeps the file's own audio when present, otherwise adds Instagram catalogue music.
"""
import json, sys, time, fcntl, subprocess, base64, traceback, re, os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
sys.path.insert(0, '/Users/teyfikoz/tools')
import emu

ROOT = Path(__file__).resolve().parent
Q = Path(os.environ.get('IGQ', ROOT / 'queue.json')); RCPT = ROOT / 'receipts.jsonl'; LOG = ROOT / 'autopost.log'
IST = ZoneInfo('Europe/Istanbul')
NAMES = {'ciaoariabella': 'Ariabella | Fashion & Lifestyle', 'selfixxapp': 'SelfixApp', 'layoverkit': 'LayOverKit - Travel Companion',
         'scuplancom': None, 'enumaapp': None, 'themr.ozz': None, 'learnlingoz': None, 'sci_break': None}
MAX_LATE = timedelta(hours=6)

def log(*a):
    line = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S ') + ' '.join(str(x) for x in a)
    print(line, flush=True); LOG.open('a').write(line + '\n')
def notify(msg):
    subprocess.run(['osascript', '-e', f'display notification {json.dumps(msg)} with title "IG Autopost"'], capture_output=True)
def sh(*a): return emu.run('shell', *a)
def tapxy(x, y): sh('input', 'tap', str(int(x)), str(int(y)))
def tap(n): tapxy(*n['c'])
def key(k): sh('input', 'keyevent', str(k))
def typ(s): sh('am', 'broadcast', '-a', 'ADB_INPUT_B64', '--es', 'msg', base64.b64encode(s.encode()).decode())
def typ_careful(text):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        chunk = line + ('\n' if i < len(lines) - 1 else '')
        if '#' in line:
            toks = re.split(r'(\s+)', chunk)
            for t in toks:
                if t: typ(t); time.sleep(0.9 if t.startswith('#') else 0.2)
        else:
            typ(chunk); time.sleep(0.4)

def focus(): return sh('dumpsys', 'window').split('mCurrentFocus=')[-1].split('\n')[0]

def wait(pred, timeout=25, every=1.5):
    end = time.time() + timeout
    while time.time() < end:
        if 'Not Responding' in focus(): recover_anr()
        hit = pred(emu.nodes())
        if hit: return hit
        time.sleep(every)
    return None
def by(text=None, rid=None, exact=False, prefix=False):
    def p(ns):
        for n in ns:
            lab = emu.label(n)
            if rid and n['rid'] == rid: return n
            if text is None: continue
            if exact and lab == text: return n
            if prefix and lab.startswith(text): return n
            if not exact and not prefix and text.lower() in lab.lower(): return n
    return p
class Fail(Exception): pass
def need(n, what):
    if not n: raise Fail(what)
    return n

def recover_anr():
    log('ANR -> restart Instagram')
    for n in emu.nodes():
        if emu.label(n) == 'Close app': tap(n)
    sh('am', 'force-stop', 'com.instagram.android'); time.sleep(2)
    emu.run('shell', 'monkey', '-p', 'com.instagram.android', '-c', 'android.intent.category.LAUNCHER', '1'); time.sleep(15)

def bail():
    for _ in range(6):
        ns = emu.nodes(); labs = {emu.label(n): n for n in ns}
        for k in ('Start over', 'Discard', 'Discard post', 'Discard video', 'Close sheet'):
            if k in labs: tap(labs[k]); time.sleep(1.5); break
        else:
            if any(n['rid'].startswith('profile_header_full_name') for n in ns): return
            key(4); time.sleep(1.5)

def emulator_ok():
    out = subprocess.run(['adb', 'devices'], capture_output=True, text=True).stdout
    return 'emulator-5580\tdevice' in out

def home_profile():
    if 'com.instagram.android' not in focus():
        emu.run('shell', 'monkey', '-p', 'com.instagram.android', '-c', 'android.intent.category.LAUNCHER', '1'); time.sleep(12)
    for _ in range(4):
        tapxy(652, 1514); time.sleep(3)
        if wait(by(rid='profile_header_full_name_above_vanity') or by('posts'), 6) or wait(lambda ns: next((n for n in ns if n['rid'].startswith('profile_header_full_name')), None), 4):
            return True
        key(4); time.sleep(1)
    raise Fail('profile tab')

def current_name():
    n = next((n for n in emu.nodes() if n['rid'].startswith('profile_header_full_name')), None)
    return n['text'] if n else None

def post_count():
    n = next((n for n in emu.nodes() if n['rid'] == 'profile_header_post_count_front_familiar'), None)
    if not n:
        n = next((n for n in emu.nodes() if n['rid'].startswith('profile_header_post_count')), None)
    m = re.search(r'(\d+)', emu.label(n) if n else '')
    return int(m.group(1)) if m else None

def switch(account):
    home_profile()
    want = NAMES.get(account)
    if want and current_name() == want: return
    tapxy(360, 90); time.sleep(2.5)
    row = need(wait(by(account, prefix=True), 8), f'account row {account}'); tap(row); time.sleep(8)
    home_profile()
    if want and current_name() != want: raise Fail(f'switch verify {account} got {current_name()}')
    log('account', account)

def push(paths):
    """Push in reverse so paths[0] is newest (auto-selected / first in gallery)."""
    for p in reversed(paths):
        name = f"ap_{int(time.time()*1000)}_{Path(p).name}"
        emu.run('push', p, f'/sdcard/DCIM/Camera/{name}')
        sh('am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', f'file:///sdcard/DCIM/Camera/{name}')
        time.sleep(1.3)

def has_audio(path):
    r = subprocess.run(['ffmpeg', '-i', path, '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
    m = re.search(r'mean_volume: (-?[\d.]+) dB', r.stderr)
    return bool(m) and float(m.group(1)) > -45

def open_create(which):
    home_profile()
    tap(need(wait(by('Create New', exact=True), 15), 'create new')); time.sleep(2)
    tap(need(wait(by(which, exact=True), 10), which)); time.sleep(4)
    k = wait(by('Keep editing'), 3)
    if k: tap(need(wait(by('Start new video'), 5), 'start new'))

def close_edits_promo():
    s = wait(by('Close sheet', exact=True), 2)
    if s: tap(s); time.sleep(1.5)

def pick_catalog(query, rf=True):
    s = need(wait(by('Search...'), 15), 'music search'); tap(s); time.sleep(1); typ(query); key(66)
    tracks = need(wait(lambda ns: [n for n in ns if emu.label(n).startswith('Select track')] or None, 20), 'tracks')
    pool = [t for t in tracks if 'royalty-free' in emu.label(t)] if rf else []
    t = (pool or tracks)[0]; tap(t); time.sleep(4)
    return emu.label(t).replace('Select track ', '')

def set_music_volume(target):
    ev = wait(by('Edit video'), 8); tap(ev) if ev else tapxy(108, 1518); time.sleep(4)
    au = wait(lambda ns: next((n for n in ns if emu.label(n).startswith('Audio:')), None), 15)
    if not au: return None
    tap(au); time.sleep(2); tap(need(wait(by('Volume', exact=True), 10), 'volume')); time.sleep(2)
    cur = None
    for _ in range(4):
        v = wait(lambda ns: next((n for n in ns if n['text'].isdigit() and n['c'][1] > 1300), None), 6)
        if not v: break
        cur = int(v['text'])
        if abs(cur - target) <= 5: break
        sh('input', 'swipe', str(int(96 + cur / 100 * 492)), '1388', str(int(96 + target / 100 * 492)), '1388', '800'); time.sleep(1.5)
    tap(need(wait(by('Done', exact=True), 8), 'vol done')); time.sleep(2)
    tapxy(70, 1495); time.sleep(1); tapxy(652, 52)
    return cur

def five_tags(caption):
    seen = 0
    def keep(m):
        nonlocal seen
        seen += 1
        return m.group(0) if seen <= 5 else ''
    out = re.sub(r'(?<!\w)#\w+', keep, caption)
    out = re.sub(r'[ \t]+\n', '\n', re.sub(r'[ \t]{2,}', ' ', out))
    return re.sub(r'\n{3,}', '\n\n', out).strip()

def caption_and_ai(caption, share_rid='share_button'):
    caption = five_tags(caption)
    cap = need(wait(by(rid='caption_input_text_view'), 45), 'share screen'); time.sleep(1.5)
    if caption:
        core = lambda t: re.sub(r'[^0-9a-zçğıöşüâîû#@]+', '', t.lower())
        for attempt in range(2):
            tap(cap); time.sleep(1.5)
            if attempt: sh('am', 'broadcast', '-a', 'ADB_CLEAR_TEXT'); time.sleep(1)
            typ(caption) if '#' not in caption or attempt == 0 and caption.count('#') <= 6 else typ_careful(caption)
            time.sleep(2.5); tapxy(656, 92); time.sleep(2)
            got = next((n['text'] for n in emu.nodes() if n['rid'] == 'caption_input_text_view'), '')
            if core(got) == core(caption): break
            cap = need(wait(by(rid='caption_input_text_view'), 8), 'caption field')
        if core(got) != core(caption):
            import difflib
            d = [x for x in difflib.ndiff(caption.splitlines(), got.splitlines()) if x[:1] in '+-']
            raise Fail(f'caption mismatch {len(got)} vs {len(caption)} diff={d[:6]}')
    lab = need(wait(by('Add AI label', exact=True), 8), 'ai label row')
    tapxy(646, lab['c'][1] + 18); time.sleep(1.5)
    # verify toggle: the Switch near the label must be checked
    sw = [n for n in emu.nodes() if n['cls'] in ('Switch', 'SwitchCompat', 'CompoundButton') and abs(n['c'][1] - lab['c'][1]) < 80]
    if sw and not sw[0]['chk']:
        tap(sw[0]); time.sleep(1)
    fb = [n for n in emu.nodes() if 'Facebook' in emu.label(n)]
    return True

def do_reel(it, dry):
    media = it['media'][0]; push([media]); open_create('Create new reel')
    g = need(wait(lambda ns: next((n for n in ns if n['rid'] == 'gallery_grid_item_thumbnail' and 'Video' in emu.label(n)), None), 20), 'gallery video'); tap(g)
    mode = it.get('music', {}).get('mode', 'auto'); track = None; vol = None
    if mode == 'catalog' or (mode == 'auto' and not has_audio(media)):
        for attempt in range(3):
            b = wait(by(rid='clips_action_bar_add_music_button'), 20)
            tap(b) if b else tapxy(84, 1210)
            if wait(by('Search...'), 10): break
            key(4); time.sleep(2)
        track = pick_catalog(it['music'].get('query', 'calm piano'), it['music'].get('rf', True))
        tapxy(652, 1470); time.sleep(5); tapxy(652, 126); time.sleep(4)
        vol = set_music_volume(it['music'].get('volume', 34))
    else:
        time.sleep(8); close_edits_promo()
        nx = need(wait(by(rid='clips_right_action_button'), 20), 'next'); tap(nx); time.sleep(3); close_edits_promo()
        if not wait(by(rid='caption_input_text_view'), 6): tap(nx)
    caption_and_ai(Path(it['caption_file']).read_text() if it.get('caption_file') else it.get('caption', ''))
    return finish_share(it, dry, by(rid='share_button'), {'track': track, 'music_volume': vol})

def do_post(it, dry):
    push(it['media']); open_create('Create new post')
    if len(it['media']) > 1:
        tap(need(wait(by(rid='multi_select_slide_button_all'), 8) or wait(by('Select multiple button'), 4), 'multi select')); time.sleep(2)
        grid = [n for n in emu.nodes() if n['rid'] == 'gallery_grid_item_thumbnail']
        for n in grid[1:len(it['media'])]: tap(n); time.sleep(2.2)
        sel = [n for n in emu.nodes() if n['rid'] == 'gallery_grid_item_thumbnail' and emu.label(n).startswith('Selected')]
        if len(sel) != len(it['media']): raise Fail(f'selected {len(sel)} of {len(it["media"])}')
    tap(need(wait(by(rid='next_button_textview'), 8), 'next1')); time.sleep(5)
    tap(need(wait(by(rid='media_thumbnail_tray_button'), 20), 'next2')); time.sleep(6)
    cap = need(wait(by(rid='caption_input_text_view'), 40), 'post share screen')
    track = None
    if it.get('music', {}).get('mode', 'auto') != 'none':
        chip = wait(lambda ns: next((n for n in ns if n['rid'] == 'suggestion_text' and '·' in n['text']), None), 6)
        if chip: track = chip['text']; tap(chip); time.sleep(4)
        if not wait(by(rid='caption_input_text_view'), 4): key(4); time.sleep(2)
    caption_and_ai(Path(it['caption_file']).read_text() if it.get('caption_file') else it.get('caption', ''))
    return finish_share(it, dry, by(rid='share_footer_button'), {'track': track})

def story_more_ai():
    tapxy(661, 410); time.sleep(2)
    more = wait(lambda ns: next((n for n in ns if emu.label(n) == 'More' and n['cls'] == 'View'), None), 6)
    if not more: tapxy(660, 494); time.sleep(2); more = wait(lambda ns: next((n for n in ns if emu.label(n) == 'More' and n['cls'] == 'View'), None), 6)
    tap(need(more, 'story more')); time.sleep(2)
    tap(need(wait(by('Label AI', exact=True), 6), 'label ai')); time.sleep(2)
    tapxy(646, 1444); time.sleep(1.5); tapxy(360, 300); time.sleep(1.5)

def do_story(it, dry):
    media = it['media'][0]; push([media]); open_create('Create new story')
    g = need(wait(lambda ns: next((n for n in ns if n['rid'] == 'gallery_grid_item_thumbnail'), None), 20), 'story gallery'); tap(g); time.sleep(6)
    extra = {}
    if it.get('poll'):
        tapxy(660, 150); time.sleep(3); tapxy(606, 784); time.sleep(3); typ(it['poll']['q']); time.sleep(1.5)
        tapxy(360, 156); time.sleep(1); typ(it['poll']['a']); tapxy(360, 254); time.sleep(1); typ(it['poll']['b']); time.sleep(1.5)
        tapxy(652, 46); time.sleep(3); extra['poll'] = it['poll']['q']
    if it.get('link'):
        tapxy(660, 150); time.sleep(3); tapxy(548, 878); time.sleep(4)
        tapxy(360, 444); time.sleep(1); typ(it['link']['url']); time.sleep(1); tapxy(220, 604); time.sleep(2)
        tapxy(360, 640); time.sleep(1); typ(it['link']['text']); time.sleep(1); tapxy(670, 352); time.sleep(2); tapxy(670, 352); time.sleep(3)
        tapxy(652, 46); time.sleep(2)
        sh('input motionevent DOWN 360 640; sleep 0.4; input motionevent MOVE 360 800; input motionevent MOVE 360 1000; input motionevent MOVE 360 1080; sleep 0.2; input motionevent UP 360 1080')
        time.sleep(2); extra['link'] = it['link']['url']
    is_video = media.lower().endswith(('.mp4', '.mov'))
    if it.get('music', {}).get('mode', 'auto') != 'none' and not (is_video and has_audio(media)):
        tapxy(660, 241); time.sleep(4)
        tr = wait(lambda ns: [n for n in ns if emu.label(n).startswith('Select track')] or None, 12)
        if it['music'].get('query') or not tr: extra['track'] = pick_catalog(it['music'].get('query', 'soft acoustic'), False)
        else: extra['track'] = emu.label(tr[0]).replace('Select track ', ''); tap(tr[0]); time.sleep(4)
        tapxy(652, 1470); time.sleep(4); tapxy(652, 46); time.sleep(3)
    story_more_ai()
    if dry: log('DRY story ready', it['id']); return {'status': 'DRY_READY', **extra}
    tap(need(wait(by('Your story', exact=True), 10), 'your story')); time.sleep(20)
    return {'status': 'SHARED_STORY', **extra}

def finish_share(it, dry, share_pred, extra):
    if dry:
        log('DRY ready on share screen', it['id']); return {'status': 'DRY_READY', **extra}
    before = None
    tap(need(wait(share_pred, 10), 'share')); time.sleep(10)
    # verify: post count increases within 8 minutes
    home_profile(); before = it.get('_count_before')
    for _ in range(16):
        c = post_count()
        if before is not None and c is not None and c > before: return {'status': 'PUBLISHED_COUNT_VERIFIED', 'count': c, **extra}
        time.sleep(30); tapxy(652, 1514); time.sleep(2)
    return {'status': 'SHARED_COUNT_NOT_CONFIRMED', **extra}

def run(dry=False):
    if not emulator_ok(): log('emulator offline'); notify('Emulator offline — paylaşım yapılamadı'); return
    q = json.loads(Q.read_text()); now = datetime.now(IST)
    due = [it for it in q if it['status'] == 'pending' and datetime.fromisoformat(it['due']) <= now]
    if not due: return
    sh('ime', 'set', 'com.android.adbkeyboard/.AdbIME')
    for it in sorted(due, key=lambda x: x['due']):
        if now - datetime.fromisoformat(it['due']) > MAX_LATE:
            it['status'] = 'expired'; log('expired', it['id']); continue
        log('START', it['id'], it['kind'], it['account'])
        try:
            switch(it['account'])
            if it['kind'] in ('reel', 'post'): home_profile(); it['_count_before'] = post_count()
            res = {'reel': do_reel, 'post': do_post, 'story': do_story}[it['kind']](it, dry)
            it.pop('_count_before', None)
            it['status'] = 'pending' if dry else 'done'; it['result'] = res
            log('OK', it['id'], res)
        except Exception as e:
            it['attempts'] = it.get('attempts', 0) + 1; it.pop('_count_before', None)
            it['last_error'] = f'{type(e).__name__}: {e}'[:300]
            log('FAIL', it['id'], it['last_error']); traceback.print_exc(file=LOG.open('a'))
            if it['attempts'] >= 3: it['status'] = 'failed'; notify(f"Başarısız: {it['id']} — {it['last_error'][:80]}")
            bail()
            if 'Not Responding' in focus(): recover_anr()
        RCPT.open('a').write(json.dumps({'at': datetime.now(IST).isoformat(), 'id': it['id'], 'status': it['status'], 'result': it.get('result'), 'error': it.get('last_error')}, ensure_ascii=False) + '\n')
        Q.write_text(json.dumps(q, ensure_ascii=False, indent=1))
        if dry: bail(); break

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        q = json.loads(Q.read_text()); from collections import Counter
        print(Counter(x['status'] for x in q)); [print(x['due'][:16], x['status'], x['id']) for x in sorted(q, key=lambda x: x['due']) if x['status'] != 'done'][:15]
        sys.exit()
    with open(ROOT / '.lock', 'w') as lk:
        try: fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: sys.exit(0)
        busy = Path('/Users/teyfikoz/tools/.emulator_busy')
        if busy.exists(): log('emulator reserved by another job'); sys.exit(0)
        run(dry='--dry' in sys.argv)
