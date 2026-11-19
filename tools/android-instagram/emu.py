"""Tiny ADB helper for emulator-5580: shot | ui [filter...] | tap x y | tapt TEXT [n] | type TEXT | key CODE | swipe x1 y1 x2 y2 [ms]"""
import subprocess, sys, re, time, xml.etree.ElementTree as ET
D = ['adb', '-s', 'emulator-5580']
SHOT = '/private/tmp/claude-501/-Users-teyfikoz/emu_shot.png'

def run(*a, text=True):
    return subprocess.run(D + list(a), capture_output=True, text=text, timeout=40).stdout

def nodes():
    path = f'/sdcard/ui-{time.time_ns()}.xml'
    run('shell', 'uiautomator', 'dump', '--compressed', path)
    raw = run('shell', 'cat', path); run('shell', 'rm', path)
    try: root = ET.fromstring(raw)
    except ET.ParseError: return []
    out = []
    for e in root.iter('node'):
        b = re.findall(r'\d+', e.get('bounds', '0,0,0,0'))
        x1, y1, x2, y2 = map(int, b) if len(b) == 4 else (0, 0, 0, 0)
        out.append(dict(text=e.get('text') or '', desc=e.get('content-desc') or '', rid=(e.get('resource-id') or '').split('/')[-1],
                        cls=(e.get('class') or '').split('.')[-1], click=e.get('clickable') == 'true', sel=e.get('selected') == 'true',
                        chk=e.get('checked') == 'true', pw=e.get('password') == 'true', c=((x1 + x2) // 2, (y1 + y2) // 2), b=(x1, y1, x2, y2)))
    return out

def label(n): return '[PASSWORD]' if n['pw'] else (n['text'] or n['desc'])

def main():
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'shot':
        png = subprocess.run(D + ['exec-out', 'screencap', '-p'], capture_output=True, timeout=40).stdout
        open(SHOT, 'wb').write(png)
        from PIL import Image
        im = Image.open(SHOT); im.convert('RGB').resize((im.width // 2, im.height // 2)).save(SHOT.replace('.png', '_s.jpg'), quality=80)
        print(SHOT.replace('.png', '_s.jpg'), '(half scale: multiply by 2)')
    elif cmd == 'ui':
        for n in nodes():
            s = label(n)
            if not (s or n['rid']): continue
            if args and not any(q.lower() in (s + ' ' + n['rid'] + ' ' + n['cls']).lower() for q in args): continue
            print(f"{n['c'][0]:4d},{n['c'][1]:4d} {'C' if n['click'] else ' '}{'S' if n['sel'] or n['chk'] else ' '} {n['cls'][:12]:12s} {n['rid'][:28]:28s} {s[:70]!r}")
    elif cmd == 'tap': run('shell', 'input', 'tap', args[0], args[1])
    elif cmd == 'tapt':
        q = args[0].lower(); k = int(args[1]) if len(args) > 1 else 0
        hits = [n for n in nodes() if q == label(n).lower() or q == n['rid'].lower()] or [n for n in nodes() if q in label(n).lower()]
        if len(hits) <= k: print('NOT_FOUND', args[0]); sys.exit(2)
        x, y = hits[k]['c']; run('shell', 'input', 'tap', str(x), str(y)); print('TAPPED', label(hits[k])[:60], x, y)
    elif cmd == 'type':
        t = ' '.join(args).replace(' ', '%s')
        run('shell', 'input', 'text', t)
    elif cmd == 'key': run('shell', 'input', 'keyevent', args[0])
    elif cmd == 'swipe': run('shell', 'input', 'swipe', *args[:4], args[4] if len(args) > 4 else '300')
    elif cmd == 'launch': run('shell', 'monkey', '-p', args[0], '-c', 'android.intent.category.LAUNCHER', '1')

if __name__ == '__main__': main()
