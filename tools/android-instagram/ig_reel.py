"""Instagram native Reel helper for emulator-5580 (catalog music, AI label, caption, optional schedule).
Usage: ig_reel.py prepare --music "query" [--track-index 0] --caption-file F [--volume 34]
       Leaves the app on the share screen; scheduling/sharing is a separate, verified step."""
import argparse, subprocess, time, sys, base64
sys.path.insert(0, '/Users/teyfikoz/tools')
import emu

def wait(pred, timeout=25, every=1.5):
    end = time.time() + timeout
    while time.time() < end:
        ns = emu.nodes()
        hit = pred(ns)
        if hit: return hit
        time.sleep(every)
    return None

def find(text, exact=False, rid=None):
    def p(ns):
        for n in ns:
            lab = emu.label(n)
            if rid and n['rid'] == rid: return n
            if text and ((lab == text) if exact else (text.lower() in lab.lower())): return n
    return p

def tap(n): emu.run('shell', 'input', 'tap', str(n['c'][0]), str(n['c'][1]))
def tapxy(x, y): emu.run('shell', 'input', 'tap', str(x), str(y))
def typ(s):
    emu.run('shell', 'am', 'broadcast', '-a', 'ADB_INPUT_B64', '--es', 'msg', base64.b64encode(s.encode()).decode())
def need(n, what):
    if not n: print('FAIL', what); sys.exit(3)
    return n

def prepare(a):
    if a.start == 'edit': return after_music(a)
    emu.run('shell', 'ime', 'set', 'com.android.adbkeyboard/.AdbIME')
    tapxy(652, 1514); time.sleep(4)
    tap(need(wait(find('Create New', exact=True), 20), 'create new')); time.sleep(2)
    tap(need(wait(find('Create new reel', exact=True), 10), 'create reel')); time.sleep(3)
    keep = wait(find('Keep editing'), 4)
    if keep: tap(need(wait(find('Start new video')), 'start new'))
    g = need(wait(lambda ns: next((n for n in ns if n['rid'] == 'gallery_grid_item_thumbnail' and 'Video' in emu.label(n)), None), 20), 'gallery video')
    print('VIDEO', emu.label(g)); tap(g)
    if a.no_music:
        time.sleep(10); nx = wait(find('Next', exact=True), 20)
        tap(nx) if nx else tapxy(630, 1518)
        return caption_step(a)
    tap(need(wait(find('Add audio', rid='clips_action_bar_add_music_button'), 30), 'add audio'))
    tap(need(wait(find('Search...'), 15), 'search')); time.sleep(1); typ(a.music); emu.run('shell', 'input', 'keyevent', '66')
    tracks = need(wait(lambda ns: [n for n in ns if emu.label(n).startswith('Select track')] or None, 20), 'tracks')
    rf = [t for t in tracks if 'royalty-free' in emu.label(t)] if a.rf else tracks
    t = need((rf or tracks)[a.track_index] if len(rf or tracks) > a.track_index else None, 'track index')
    print('TRACK', emu.label(t)); tap(t); time.sleep(4)
    tapxy(652, 1470); time.sleep(5); tapxy(652, 126); time.sleep(4)          # confirm track, done trimming
    after_music(a)

def after_music(a):
    ev = wait(find('Edit video'), 8)
    tap(ev) if ev else tapxy(108, 1518); time.sleep(4)
    au = need(wait(lambda ns: next((n for n in ns if emu.label(n).startswith('Audio:')), None), 15), 'audio clip'); tap(au); time.sleep(2)
    tap(need(wait(find('Volume', exact=True), 10), 'volume btn')); time.sleep(2)
    for _ in range(4):
        v = wait(lambda ns: next((n for n in ns if n['text'].isdigit() and n['c'][1] > 1300), None), 6)
        cur = int(v['text']);
        if abs(cur - a.volume) <= 4: break
        x = 96 + cur / 100 * 492; tx = 96 + a.volume / 100 * 492
        emu.run('shell', 'input', 'swipe', str(int(x)), '1388', str(int(tx)), '1388', '800'); time.sleep(1.5)
    print('VOLUME', cur)
    tap(need(wait(find('Done', exact=True), 8), 'done vol')); time.sleep(2)
    tapxy(70, 1495); time.sleep(1); tapxy(652, 52)
    caption_step(a)

def caption_step(a):
    cap = need(wait(find(None, rid='caption_input_text_view'), 40), 'share screen'); time.sleep(2)
    tap(cap); time.sleep(1.5); typ(open(a.caption_file).read()); time.sleep(2.5)
    tapxy(656, 92); time.sleep(2)
    ns = emu.nodes(); c = next(n for n in ns if n['rid'] == 'caption_input_text_view')
    want = open(a.caption_file).read()
    print('CAPTION_OK', c['text'].strip() == want.strip(), len(c['text']), len(want))
    lab = need(wait(find('Add AI label', exact=True), 8), 'ai label')
    tapxy(646, lab['c'][1] + 18); time.sleep(1.5)
    print('READY_ON_SHARE_SCREEN — verify AI toggle visually before share/schedule')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('--music'); ap.add_argument('--track-index', type=int, default=0)
    ap.add_argument('--caption-file'); ap.add_argument('--volume', type=int, default=34); ap.add_argument('--rf', action='store_true'); ap.add_argument('--start', default=''); ap.add_argument('--no-music', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'prepare': prepare(a)
