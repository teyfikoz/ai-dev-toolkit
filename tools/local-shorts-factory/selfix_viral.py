"""Selfix viral pack: local Supertonic-3 TTS + Pillow animation + numpy-synth original music. No paid APIs."""
import os, sys, json, math, wave, hashlib, subprocess, argparse
from pathlib import Path
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from content import SKITS, NARRATED, LONG

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'production' / 'tts_cache'; CACHE.mkdir(parents=True, exist_ok=True)
OUT = ROOT / 'videos'; OUT.mkdir(exist_ok=True)
FPS = 24
NAVY = (15, 17, 35); LAV = (194, 172, 255); CORAL = (255, 150, 135); MINT = (130, 225, 195)
WHITE = (244, 244, 252); MUTED = (128, 132, 168); DARK = (22, 20, 40)
ENV = dict(os.environ, OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', VECLIB_MAXIMUM_THREADS='2')
F = {}
FEMALE = {'Ece', 'Zeynep', 'Selin', 'Ayşe', 'Elif', 'Leyla', 'Emma', 'Sophie', 'Lily', 'Anna', 'Mia', 'Chloe'}
UI = {
 'tr': dict(notice='FARK ETTİN Mİ?', foot='Özgün içerik • Sentetik ses • Terapi değildir', sub='KENDİNİ KEŞFET', ch='BÖLÜM'),
 'en': dict(notice='NOTICE THIS?', foot='Original content • Synthetic voice • Not therapy', sub='EXPLORE YOURSELF', ch='PART'),
}

def font(size, w='Bold'):
    k = (size, w)
    if k not in F: F[k] = ImageFont.truetype(str(ROOT / 'fonts' / f'PJS-{w}.ttf'), size)
    return F[k]

def wrap(d, text, size, width, w='Bold'):
    out, line = [], ''
    for word in text.split():
        trial = (line + ' ' + word).strip()
        if line and d.textlength(trial, font=font(size, w)) > width: out.append(line); line = word
        else: line = trial
    if line: out.append(line)
    return out

def center(d, text, cx, y, size, color, width, w='Bold', gap=1.28):
    ls = wrap(d, text, size, width, w)
    for i, l in enumerate(ls):
        d.text((cx - d.textlength(l, font=font(size, w)) / 2, y + i * size * gap), l, font=font(size, w), fill=color)
    return len(ls) * size * gap

def reveal(d, text, cx, y, size, width, u, w='Bold', on=WHITE, off=(92, 96, 132), gap=1.32):
    """Karaoke-style word reveal driven by speech progress u in [0,1]."""
    ls = wrap(d, text, size, width, w); total = max(1, len(text)); shown = u * total * 1.12; seen = 0
    for i, l in enumerate(ls):
        x = cx - d.textlength(l, font=font(size, w)) / 2
        for word in l.split(' '):
            col = on if seen < shown else off
            d.text((x, y + i * size * gap), word, font=font(size, w), fill=col)
            x += d.textlength(word + ' ', font=font(size, w)); seen += len(word) + 1
    return len(ls) * size * gap

def gradient(W, H, top, bottom):
    a = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(top)[None, None, :] * (1 - a) + np.array(bottom)[None, None, :] * a).repeat(W, axis=1)
    return Image.fromarray(arr.astype('uint8'))

# ---------- music: original numpy synthesis ----------
def synth_bed(path, seconds=96, calm=False):
    sr = 48000; t = np.arange(int(sr * seconds)) / sr
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]] if calm else [[48, 52, 55], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
    bar = 6.0 if calm else 4.0
    out = np.zeros((len(t), 2))
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    for b in range(int(seconds / bar)):
        s, e = int(b * bar * sr), int((b + 1) * bar * sr); seg = t[s:e] - t[s]
        env = np.minimum(1, seg / 1.2) * np.minimum(1, (bar - seg) / 1.2)
        chord = prog[b % 4]
        for i, m in enumerate(chord + [chord[0] - 12]):
            for det, pan in ((-0.6, 0.35), (0.6, 0.65)):
                wv = np.sin(2 * np.pi * (hz(m) + det) * seg) * 0.05 * env
                out[s:e, 0] += wv * (1 - pan); out[s:e, 1] += wv * pan
        if not calm:
            for k, m in enumerate([chord[0] + 12, chord[2] + 12, chord[1] + 12, chord[2] + 12]):
                ps = s + int(k * bar / 4 * sr); n = int(1.6 * sr); pt = np.arange(n) / sr
                pl = (np.sin(2 * np.pi * hz(m) * pt) + 0.3 * np.sin(4 * np.pi * hz(m) * pt)) * np.exp(-pt * 3.2) * 0.045
                end = min(len(out), ps + n); out[ps:end] += pl[:end - ps, None]
    k = 40; out = np.apply_along_axis(lambda c: np.convolve(c, np.ones(k) / k, 'same'), 0, out)
    out /= np.abs(out).max() / 0.6
    with wave.open(str(path), 'wb') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(sr); f.writeframes((out * 32767).astype('<i2').tobytes())

# ---------- jobs ----------
def build_jobs():
    jobs = []
    for s in SKITS:
        for lang in ('tr', 'en'):
            c = s[lang]; narr = 'M2' if lang == 'tr' else 'M1'
            vo = {r: ('F2' if c['names'][i] in FEMALE else 'M3') for i, r in enumerate('AB')}
            segs = [dict(text=c['hook'], voice=narr, role='hook', pause=0.25)]
            segs += [dict(text=t, voice=vo[r], role=r, pause=0.35) for r, t in c['lines']]
            segs += [dict(text=t, voice=narr, role='N', pause=0.5) for t in c['insight']]
            jobs.append(dict(id=f"sv_{s['slug']}_{lang.upper()}", lang=lang, kind='skit', fmt='short', hook=c['hook'], names=c['names'], segs=segs, src=s['src'], speed=1.05))
    for s in NARRATED:
        for lang in ('tr', 'en'):
            c = s[lang]; narr = 'M2' if lang == 'tr' else 'M1'
            segs = [dict(text=t, voice=narr, role='N', pause=0.45) for t in c['lines']]
            jobs.append(dict(id=f"sv_{s['slug']}_{lang.upper()}", lang=lang, kind='narr', fmt='short', hook=c['hook'], items=c['items'], segs=segs, src=s['src'], speed=1.04))
    for s in LONG:
        for lang in ('tr', 'en'):
            c = s[lang]; narr = 'M2' if lang == 'tr' else 'M1'
            segs = [dict(text=t, voice=narr, role='intro', ch=0, pause=0.6) for t in c['intro']]
            for i, (title, body) in enumerate(c['chapters'], 1):
                segs.append(dict(text=f"{['Bir','İki','Üç','Dört','Beş','Altı','Yedi','Sekiz','Dokuz'][i-1] if lang=='tr' else ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine'][i-1]}: {title}.", voice=narr, role='chtitle', ch=i, title=title, pause=0.9))
                segs += [dict(text=t, voice=narr, role='body', ch=i, title=title, pause=0.7) for t in body]
            segs += [dict(text=t, voice=narr, role='outro', ch=10, pause=0.7) for t in c['outro']]
            jobs.append(dict(id=f"sv_{s['slug']}_{lang.upper()}_LONG", lang=lang, kind='long', fmt='long', title=c['title'], nch=len(c['chapters']), segs=segs, src=s['src'], speed=1.0))
    return jobs

def tts(text, voice, lang, speed):
    key = hashlib.sha1(f'{text}|{voice}|{lang}|{speed}'.encode()).hexdigest()[:16]
    raw = CACHE / f'{key}.wav'
    if not raw.exists():
        subprocess.run(['supertonic', 'tts', text, '--model', 'supertonic-3', '--lang', lang, '--voice', voice, '--steps', '8', '--speed', str(speed), '-o', str(raw)],
                       check=True, env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return raw

def make_audio(job):
    folder = ROOT / 'production' / job['id']; folder.mkdir(exist_ok=True)
    sr = 48000; pcm = []; at = 0.0
    for s in job['segs']:
        raw = tts(s['text'], s['voice'], job['lang'], job['speed'])
        mono = folder / (raw.stem + '_48k.wav')
        if not mono.exists():
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-ar', str(sr), '-ac', '1', str(mono)], check=True)
        with wave.open(str(mono)) as w: data = np.frombuffer(w.readframes(w.getnframes()), '<i2')
        dur = len(data) / sr
        s['start'], s['end'] = at, at + dur
        pcm.append(data); pcm.append(np.zeros(int(s['pause'] * sr), '<i2')); at += dur + s['pause']
        s['hold'] = at
    voice = folder / 'narration.wav'
    with wave.open(str(voice), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.concatenate(pcm).tobytes())
    job['total'] = at + (0.6 if job['fmt'] == 'short' else 1.5)
    return voice

def active(job, t):
    for i, s in enumerate(job['segs']):
        if t < s['hold']: return i, s, max(0.0, min(1.0, (t - s['start']) / max(0.01, s['end'] - s['start'])))
    s = job['segs'][-1]; return len(job['segs']) - 1, s, 1.0

# ---------- frames ----------
BASES = {}
def base(job):
    if job['id'] not in BASES:
        if job['fmt'] == 'long': BASES[job['id']] = gradient(1920, 1080, (14, 16, 36), (36, 24, 62))
        else: BASES[job['id']] = gradient(1080, 1920, (14, 16, 36), (40, 26, 66))
    return BASES[job['id']].copy()

def header(d, job, W):
    d.text((80, 78), 'SELFIX', font=font(40, 'ExtraBold'), fill=LAV)
    d.text((82, 128), UI[job['lang']]['sub'], font=font(22, 'Medium'), fill=MUTED)

def bubble(d, x, y, text, name, left, hl, dy=0, W=1080):
    size = 46; maxw = 720
    ls = wrap(d, text, size, maxw, 'Medium'); tw = max(d.textlength(l, font=font(size, 'Medium')) for l in ls)
    bw, bh = tw + 64, len(ls) * size * 1.3 + 44
    bx = 80 if left else W - 80 - bw; by = y + dy
    fill = LAV if left else WHITE
    d.text((bx + (6 if left else bw - d.textlength(name, font=font(26, 'Bold')) - 6), by - 38), name, font=font(26, 'Bold'), fill=LAV if left else (210, 210, 228))
    d.rounded_rectangle((bx, by, bx + bw, by + bh), 34, fill=fill, outline=CORAL if hl else None, width=5 if hl else 0)
    for i, l in enumerate(ls): d.text((bx + 32, by + 22 + i * size * 1.3), l, font=font(size, 'Medium'), fill=DARK)
    return bh + 70

def bubble_h(d, text):
    return len(wrap(d, text, 46, 720, 'Medium')) * 46 * 1.3 + 44 + 70

def frame_skit(job, t):
    im = base(job); d = ImageDraw.Draw(im); header(d, job, 1080)
    i, s, u = active(job, t)
    lines = [x for x in job['segs'] if x['role'] in 'AB']
    if t < lines[0]['start'] - 0.05:
        d.ellipse((290, 560, 790, 1060), outline=LAV, width=6); d.ellipse((370, 640, 710, 980), outline=(90, 80, 150), width=3)
        center(d, '“...”', 540, 700, 150, CORAL, 400, 'ExtraBold', gap=1)
        center(d, job['hook'], 540, 1130, 82, WHITE, 940, 'ExtraBold')
        center(d, UI[job['lang']]['foot'], 540, 1800, 24, MUTED, 960, 'Medium')
        return im
    center(d, job['hook'], 540, 220, 64, WHITE, 940, 'ExtraBold')
    started = [x for x in lines if t >= x['start'] - 0.05]
    heights = [bubble_h(d, x['text']) for x in started]
    top, bottom = 540, 1440
    off = max(0, sum(heights) - (bottom - top)); y = top - off
    for x, h in zip(started, heights):
        pop = min(1, (t - x['start'] + 0.05) / 0.22)
        if y + h > top - 40:
            bubble(d, 0, y, x['text'], job['names'][0 if x['role'] == 'A' else 1], x['role'] == 'A', x is s, dy=int((1 - pop) * 40))
        y += h
    if s['role'] == 'N' or (i > 0 and job['segs'][i - 1]['role'] == 'N'):
        first_n = next(x for x in job['segs'] if x['role'] == 'N')
        a = min(1, max(0, (t - first_n['start'] + 0.3) / 0.45))
        ov = Image.new('RGB', im.size, (10, 10, 24)); im = Image.blend(im, ov, 0.78 * a); d = ImageDraw.Draw(im); header(d, job, 1080)
        if a > 0.2:
            d.rounded_rectangle((70, 560, 1010, 1420), 44, fill=(30, 28, 58), outline=LAV, width=3)
            center(d, UI[job['lang']]['notice'], 540, 630, 44, CORAL, 860, 'ExtraBold')
            reveal(d, s['text'], 540, 760, 62, 820, u if s['role'] == 'N' else 1.0)
    elif s['role'] == 'hook':
        pass
    n = len(job['segs']); d.rounded_rectangle((80, 1640, 1000, 1648), 4, fill=(48, 46, 80)); d.rounded_rectangle((80, 1640, 80 + 920 * min(1, t / job['total']), 1648), 4, fill=LAV)
    center(d, UI[job['lang']]['foot'], 540, 1800, 24, MUTED, 960, 'Medium')
    return im

def frame_narr(job, t):
    im = base(job); d = ImageDraw.Draw(im); header(d, job, 1080)
    i, s, u = active(job, t)
    center(d, job['hook'], 540, 220, 60, WHITE, 940, 'ExtraBold')
    cy = 720; r = 180 + 14 * math.sin(t * 1.4)
    d.ellipse((540 - r, cy - r, 540 + r, cy + r), outline=LAV, width=6)
    r2 = r * 0.72 + 10 * math.sin(t * 2.1 + 1); d.ellipse((540 - r2, cy - r2, 540 + r2, cy + r2), outline=(90, 80, 150), width=3)
    label = str(i) if job['items'] and 0 < i < len(job['segs']) - 1 else ('?' if i == len(job['segs']) - 1 else '•')
    if i == 0: label = '5' if job['items'] else '!'
    center(d, label, 540, cy - 95, 150, CORAL if i else LAV, 400, 'ExtraBold', gap=1)
    d.rounded_rectangle((70, 990, 1010, 1420), 40, fill=(30, 28, 58))
    reveal(d, s['text'], 540, 1040, 54, 840, u)
    n = len(job['segs'])
    for k in range(n): d.rounded_rectangle((540 - n * 30 + k * 60, 1470, 540 - n * 30 + k * 60 + 44, 1480), 5, fill=LAV if k <= i else (56, 54, 90))
    center(d, UI[job['lang']]['foot'], 540, 1800, 24, MUTED, 960, 'Medium')
    return im

def frame_long(job, t):
    im = base(job); d = ImageDraw.Draw(im)
    d.text((80, 64), 'SELFIX', font=font(40, 'ExtraBold'), fill=LAV); d.text((82, 114), UI[job['lang']]['sub'], font=font(22, 'Medium'), fill=MUTED)
    i, s, u = active(job, t); ch = s['ch']
    for k in range(3):
        rr = 160 + 70 * k + 12 * math.sin(t * 0.7 + k)
        cx, cy = (1560, 260) if ch in (0, 10) else (430, 560)
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(60 + 20 * k, 52 + 16 * k, 110 + 20 * k), width=2)
    if ch == 0:
        center(d, job['title'], 960, 300, 76, WHITE, 1500, 'ExtraBold')
        d.rounded_rectangle((260, 640, 1660, 930), 40, fill=(30, 28, 58)); reveal(d, s['text'], 960, 680, 44, 1280, u)
    elif ch == 10:
        center(d, '?', 960, 150, 180, CORAL, 400, 'ExtraBold', gap=1)
        d.rounded_rectangle((260, 560, 1660, 900), 40, fill=(30, 28, 58)); reveal(d, s['text'], 960, 600, 46, 1280, u)
    else:
        d.text((430 - d.textlength(f'{ch:02d}', font=font(260, 'ExtraBold')) / 2, 330), f'{ch:02d}', font=font(260, 'ExtraBold'), fill=LAV)
        d.text((130, 250), f"{UI[job['lang']]['ch']} {ch}/{job['nch']}", font=font(28, 'Bold'), fill=MUTED)
        center(d, s['title'], 430, 700, 46, WHITE, 640, 'ExtraBold')
        d.rounded_rectangle((850, 250, 1830, 880), 40, fill=(30, 28, 58))
        if s['role'] == 'chtitle': center(d, s['title'], 1340, 470, 62, CORAL, 860, 'ExtraBold')
        else: reveal(d, s['text'], 1340, 310, 46, 860, u)
    n = job['nch']
    for k in range(1, n + 1):
        x0 = 280 + (k - 1) * (1360 / n); d.rounded_rectangle((x0, 975, x0 + 1360 / n - 18, 985), 5, fill=LAV if 0 < k <= ch else (56, 54, 90))
    d.text((1920 - 80 - d.textlength(UI[job['lang']]['foot'], font=font(22, 'Medium')), 1025), UI[job['lang']]['foot'], font=font(22, 'Medium'), fill=MUTED)
    return im

def frame(job, t):
    return {'skit': frame_skit, 'narr': frame_narr, 'long': frame_long}[job['kind']](job, t)

def ts(x):
    m = round(x * 1000); return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def produce(job):
    for attempt in range(2):
        try: return _produce(job)
        except Exception as e:
            err = f'{type(e).__name__}: {e}'
    return f"FAILED {job['id']} {err}"

def _produce(job):
    if (OUT / f"{job['id']}_YT.mp4").exists() and (ROOT / 'production' / job['id'] / 'meta.json').exists(): return f"SKIP {job['id']}"
    beds = ROOT / 'production' / 'beds'; beds.mkdir(exist_ok=True)
    bed = beds / ('calm.wav' if job['fmt'] == 'long' else 'warm.wav')
    voice = make_audio(job)
    W, H = (1920, 1080) if job['fmt'] == 'long' else (1080, 1920)
    folder = ROOT / 'production' / job['id']; silent = folder / 'silent.mp4'
    n = math.ceil(job['total'] * FPS); CH = FPS * 20; parts = []
    for c, lo in enumerate(range(0, n, CH)):
        hi = min(n, lo + CH); part = folder / f'chunk_{c:03d}.mp4'; parts.append(part)
        if part.exists():
            try:
                got = int(subprocess.check_output(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', str(part)]).strip())
                if got == hi - lo: continue
            except Exception: pass
        for attempt in range(6):
            p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
                                  '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-threads', '2', str(part)], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            try:
                for f in range(lo, hi): p.stdin.write(frame(job, f / FPS).tobytes())
                p.stdin.close()
            except BrokenPipeError: pass
            if p.wait() == 0: break
            import time; time.sleep(20)
        else: raise RuntimeError(f'chunk {c} failed')
    (folder / 'chunks.txt').write_text('\n'.join(f"file '{x}'" for x in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(folder / 'chunks.txt'), '-c', 'copy', str(silent)], check=True)
    ig = OUT / f"{job['id']}_IG.mp4"; yt = OUT / f"{job['id']}_YT.mp4"
    common = ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(silent), '-i', str(voice), '-filter_complex', '[1:a]apad,loudnorm=I=-15:TP=-1.5:LRA=11[a]',
                    '-map', '0:v', '-map', '[a]', '-shortest', *common, str(ig)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(silent), '-i', str(voice), '-stream_loop', '-1', '-i', str(bed), '-filter_complex',
                    '[1:a]apad,loudnorm=I=-15:TP=-1.5:LRA=11[v];[2:a]volume=0.16,afade=t=in:d=1.5[m];[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]',
                    '-map', '0:v', '-map', '[a]', '-shortest', *common, str(yt)], check=True)
    srt = '\n'.join(f"{k+1}\n{ts(s['start'])} --> {ts(s['end'])}\n{s['text']}\n" for k, s in enumerate(job['segs']))
    (OUT / f"{job['id']}.srt").write_text(srt)
    cov = frame(job, 0.0 if job['fmt'] == 'short' else 2.0).convert('RGB'); cov.save(ROOT / 'covers' / f"{job['id']}_cover.jpg", quality=93)
    for fpath in (ig, yt):
        r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(fpath), '-f', 'null', '-'], capture_output=True, text=True)
        assert r.returncode == 0 and not r.stderr.strip(), r.stderr
    meta = {k: v for k, v in job.items() if k != 'segs'}
    meta.update(segs=[{k: s[k] for k in ('text', 'voice', 'role', 'start', 'end')} for s in job['segs']], ig=str(ig), yt=str(yt),
                sha_ig=hashlib.sha256(ig.read_bytes()).hexdigest(), sha_yt=hashlib.sha256(yt.read_bytes()).hexdigest(), decode='PASS')
    (ROOT / 'production' / job['id'] / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    return f"DONE {job['id']} {job['total']:.1f}s"

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--only', nargs='*'); ap.add_argument('--workers', type=int, default=5); ap.add_argument('--still', action='store_true')
    a = ap.parse_args()
    beds = ROOT / 'production' / 'beds'; beds.mkdir(exist_ok=True)
    if not (beds / 'warm.wav').exists(): synth_bed(beds / 'warm.wav')
    if not (beds / 'calm.wav').exists(): synth_bed(beds / 'calm.wav', 120, calm=True)
    jobs = build_jobs()
    if a.only: jobs = [j for j in jobs if j['id'] in a.only]
    if a.still:
        for j in jobs:
            make_audio(j)
            for k, s in enumerate(j['segs'][:8]):
                frame(j, (s['start'] + s['end']) / 2).save(ROOT / 'production' / f"still_{j['id']}_{k}.jpg", quality=85)
        print('stills ok'); sys.exit()
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(produce, jobs): print(r, flush=True)
