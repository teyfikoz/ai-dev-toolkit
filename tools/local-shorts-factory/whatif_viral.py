"""What If Lab Scope Shorts renderer: procedural space/physics illustrations + local TTS (reuses the Selfix engine)."""
import sys, math, random, shutil
from pathlib import Path
sys.path.insert(0, '/Users/teyfikoz/Desktop/Selfix_Viral_20261119/production')
import selfix_viral as v
from PIL import Image, ImageDraw, ImageFilter
from multiprocessing import Pool
from whatif_content import TOPICS

ROOT = Path(__file__).resolve().parents[1]
for d in ('videos', 'covers', 'production/tts_cache', 'production/beds'): (ROOT / d).mkdir(parents=True, exist_ok=True)
if not (ROOT / 'fonts').exists(): shutil.copytree('/Users/teyfikoz/Desktop/Selfix_Viral_20261119/fonts', ROOT / 'fonts')
v.ROOT = ROOT; v.OUT = ROOT / 'videos'; v.CACHE = ROOT / 'production' / 'tts_cache'
ORANGE = (255, 156, 66); CYAN = (90, 210, 255); WHITE = v.WHITE; MUT = (140, 150, 185)
random.seed(7); STARS = [(random.randint(0, 1079), random.randint(0, 1919), random.random()) for _ in range(260)]
BG = None
def bg():
    global BG
    if BG is None:
        im = v.gradient(1080, 1920, (6, 8, 22), (18, 12, 40)); d = ImageDraw.Draw(im)
        for x, y, b in STARS: r = 1 if b < .8 else 2; d.ellipse((x - r, y - r, x + r, y + r), fill=(int(150 + 100 * b),) * 3)
        BG = im
    return BG.copy()

def earth(d, cx, cy, r, t, shade=0.0, ice=0.0):
    d.ellipse((cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), fill=(40, 90, 160))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(30, 110, 200))
    for k in range(5):
        a = (t * 0.6 + k * 1.3) % (2 * math.pi); x = cx + r * 0.75 * math.sin(a)
        if math.cos(a) > -0.1:
            w = r * 0.28 * max(0.2, math.cos(a)); h = r * (0.22 + 0.08 * k % 3)
            d.ellipse((x - w, cy - r * 0.55 + k * r * 0.22 - h / 2, x + w, cy - r * 0.55 + k * r * 0.22 + h / 2), fill=(70, 160, 90))
    if ice: d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(230, 245, 255), width=int(4 + ice * 30))
    if shade: d.pieslice((cx - r, cy - r, cx + r, cy + r), 270, 90, fill=(8, 14, 34))

def illus(im, d, vis, t, u, line_i):
    cx, cy = 540, 820
    if vis in ('earth', 'wind', 'ocean', 'daynight', 'cold'):
        earth(d, cx, cy, 250, 0 if vis in ('wind', 'ocean') else t, shade=1 if vis == 'daynight' else 0, ice=u if vis == 'cold' else 0)
        if vis == 'wind':
            for k in range(14):
                y = cy - 220 + k * 32; x0 = ((t * 900 + k * 137) % 1300) - 300
                d.line((x0, y, x0 + 160, y), fill=(230, 240, 255), width=5)
        if vis == 'ocean':
            for k in range(3):
                rr = 250 + 25 + k * 22 + 10 * math.sin(t * 3 + k)
                d.arc((cx - rr, cy - rr * 1.08, cx + rr, cy + rr * 1.08), 200, 340, fill=CYAN, width=6)
        if vis == 'cold':
            d.rounded_rectangle((900, 560, 950, 1060), 25, outline=WHITE, width=5)
            h = int(420 * (1 - u)); d.rounded_rectangle((912, 1040 - h, 938, 1048), 13, fill=(120, 190, 255))
    elif vis == 'tunnel':
        for rr, col in ((300, (120, 80, 50)), (250, (210, 100, 40)), (160, (240, 150, 40)), (80, (255, 220, 90))):
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col)
        d.rectangle((cx - 9, cy - 300, cx + 9, cy + 300), fill=(15, 15, 30))
        y = cy - 280 * math.cos(t * 1.1); d.ellipse((cx - 22, y - 22, cx + 22, y + 22), fill=WHITE, outline=ORANGE, width=5)
    elif vis in ('sun', 'orbit'):
        fade = 1.0 if vis == 'sun' and line_i == 0 else (max(0, 1 - u * 1.4) if vis == 'sun' else 0)
        if fade > 0:
            glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
            g.ellipse((cx - 330, cy - 330, cx + 330, cy + 330), fill=(255, 190, 60, int(110 * fade))); glow = glow.filter(ImageFilter.GaussianBlur(40))
            im.paste(glow, (0, 0), glow); d = ImageDraw.Draw(im)
            d.ellipse((cx - 220, cy - 220, cx + 220, cy + 220), fill=(255, int(200 * fade + 40), int(70 * fade)))
        else:
            d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), outline=MUT, width=2)
            d.ellipse((cx - 380, cy - 380, cx + 380, cy + 380), outline=(60, 60, 90), width=2)
            ex = cx + 380 + u * 260; ey = cy - u * 520; d.line((cx + 380, cy, cx + 380 + 300, cy - 600), fill=(90, 90, 130), width=2)
            earth(d, int(ex), int(ey), 60, t)
    elif vis == 'astronaut':
        a = math.sin(t * 0.8) * 0.25; x, y = cx + 30 * math.sin(t * 0.5), cy + 20 * math.cos(t * 0.6)
        def rot(px, py): return (x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a))
        d.ellipse((rot(0, -170)[0] - 60, rot(0, -170)[1] - 60, rot(0, -170)[0] + 60, rot(0, -170)[1] + 60), fill=(240, 205, 170))
        d.polygon([rot(-70, -100), rot(70, -100), rot(60, 80), rot(-60, 80)], fill=(70, 110, 200))
        for sx in (-1, 1):
            d.line([rot(sx * 70, -90), rot(sx * 150, -10 + 20 * math.sin(t))], fill=(70, 110, 200), width=34)
            d.line([rot(sx * 35, 80), rot(sx * 55, 230)], fill=(50, 60, 90), width=38)
        if u > 0.3:
            for k in range(6): d.ellipse((x + 40 + k * 18, y - 230 - k * 22, x + 50 + k * 18, y - 220 - k * 22), outline=CYAN, width=2)
    elif vis == 'ant':
        d.line((80, 1080, 1000, 1080), fill=(90, 70, 50), width=8)
        d.ellipse((560, 760, 860, 1080), fill=(110, 190, 255), outline=WHITE, width=4); d.ellipse((620, 800, 690, 870), fill=(220, 240, 255))
        d.ellipse((150, 980, 330, 1060), fill=(40, 25, 20)); d.ellipse((300, 990, 380, 1050), fill=(40, 25, 20)); d.ellipse((90, 995, 170, 1045), fill=(40, 25, 20))
        hx = 460 + 10 * math.sin(t * 2)
        d.ellipse((hx - 9, 1000, hx + 9, 1018), fill=(240, 205, 170)); d.line((hx, 1018, hx, 1050), fill=ORANGE, width=6)
        d.line((hx, 1050, hx - 8, 1076), fill=WHITE, width=4); d.line((hx, 1050, hx + 8, 1076), fill=WHITE, width=4)
        d.text((hx - 22, 950), 'YOU', font=v.font(24, 'ExtraBold'), fill=ORANGE)
    elif vis in ('moon', 'ring'):
        earth(d, cx, cy, 200, t)
        if vis == 'moon':
            dist = 420 - 230 * u if line_i else 420
            mx = cx + dist; d.ellipse((mx - 60, cy - 60, mx + 60, cy + 60), fill=(190, 190, 200)); d.ellipse((mx - 30, cy - 20, mx - 5, cy + 5), fill=(150, 150, 160))
        else:
            for k in range(320):
                a = k / 320 * 2 * math.pi + t * 0.15; rr = 300 + (k * 37 % 60)
                x = cx + rr * math.cos(a); y = cy + rr * 0.28 * math.sin(a)
                if math.sin(a) < 0 and abs(x - cx) < 200: continue
                d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(200, 200, 215))
    elif vis == 'end':
        r = 210 + 12 * math.sin(t * 2); d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ORANGE, width=8)
        v.center(d, '?', cx, cy - 150, 260, ORANGE, 400, 'ExtraBold', gap=1)
    return d

def frame(job, t):
    im = bg(); d = ImageDraw.Draw(im)
    i, s, u = v.active(job, t)
    d.text((70, 80), 'WHAT IF LAB', font=v.font(38, 'ExtraBold'), fill=ORANGE)
    v.center(d, job['hook'], 540, 190, 60, WHITE, 960, 'ExtraBold')
    d = illus(im, d, s['visual'], t, u, i)
    if s.get('stat'):
        pop = min(1, (t - s['start']) / 0.3); size = int(70 + 30 * pop)
        w = d.textlength(s['stat'], font=v.font(size, 'ExtraBold'))
        d.rounded_rectangle((540 - w / 2 - 34, 1120, 540 + w / 2 + 34, 1130 + size + 26), 30, fill=ORANGE)
        d.text((540 - w / 2, 1132), s['stat'], font=v.font(size, 'ExtraBold'), fill=(20, 12, 30))
    d.rounded_rectangle((60, 1250, 1020, 1470), 34, fill=(20, 18, 46))
    v.reveal(d, s['text'], 540, 1278, 42, 890, u)
    n = len(job['segs'])
    for k in range(n): d.rounded_rectangle((540 - n * 30 + k * 60, 1500, 540 - n * 30 + k * 60 + 44, 1508), 4, fill=ORANGE if k <= i else (60, 58, 90))
    return im

def jobs():
    out = []
    for tp in TOPICS:
        for lang in ('en', 'tr'):
            c = tp[lang]; narr = 'M1' if lang == 'en' else 'M2'
            segs = [dict(text=tx, voice=narr, role='N', visual=vis, stat=st, pause=0.35) for vis, st, tx in c['lines']]
            out.append(dict(id=f"wi_{tp['slug']}_{lang.upper()}", lang=lang, kind='whatif', fmt='short', hook=c['hook'], segs=segs, speed=1.06, src=tp['src']))
    return out

v.frame = lambda job, t: frame(job, t)
def produce(j):
    v.frame = lambda job, t: frame(job, t)
    return v.produce(j)

if __name__ == '__main__':
    if not (ROOT / 'production/beds/warm.wav').exists(): v.synth_bed(ROOT / 'production/beds/warm.wav'); v.synth_bed(ROOT / 'production/beds/calm.wav', 120, calm=True)
    js = jobs()
    if '--still' in sys.argv:
        for j in js[:4]:
            v.make_audio(j)
            for k, s in enumerate(j['segs']): frame(j, (s['start'] + s['end']) / 2).save(ROOT / 'production' / f"still_{j['id']}_{k}.jpg", quality=80)
        sys.exit()
    with Pool(3) as p:
        for r in p.imap_unordered(produce, js): print(r, flush=True)
