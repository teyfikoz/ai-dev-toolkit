"""Selfix app promo Shorts/Reels: real store screenshots in a phone frame, narration, App Store + Google Play QR codes."""
import math, subprocess, sys, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import qrcode
import selfix_viral as v

SHOTS = Path('/Users/teyfikoz/Projects/mobile/personalite/fastlane/screenshots/en-US')
IOS = 'https://apps.apple.com/app/id6760978989'
AND = 'https://play.google.com/store/apps/details?id=com.teyfikoz.personalite'
ROOT = v.ROOT

SCRIPTS = {
 'tr': dict(hook='Kendini 3 dakikada keşfet', scenes=[
   (None, 'Kendini gerçekten ne kadar tanıyorsun? Üç dakikada keşfet.'),
   ('02', 'Selfix içinde MBTI, Big Five, Enneagram, duygusal zekâ ve DISC gibi yedi kişilik testi var.'),
   ('04', 'Testi bitirdiğin anda sonucunu, güçlü yanlarını ve sana uyan kariyer alanlarını görürsün.'),
   ('05', 'Bir arkadaşınla kişilik uyumunuzu karşılaştırabilirsin.'),
   ('01', 'Uygulama on yedi dilde. Kişilik sonuçları klinik tanı değildir; kendini keşfetmek içindir.'),
   ('QR', 'Selfix ücretsiz. Kodu okut ya da profildeki bağlantıdan indir.')]),
 'en': dict(hook='Discover yourself in 3 minutes', scenes=[
   (None, 'How well do you really know yourself? Find out in three minutes.'),
   ('02', 'Selfix has seven personality tests, including MBTI, Big Five, Enneagram, emotional intelligence and DISC.'),
   ('04', 'The moment you finish, you see your result, your strengths and the careers that may suit you.'),
   ('05', 'You can compare your personality compatibility with a friend.'),
   ('01', 'The app speaks seventeen languages. Results are for self discovery, not a clinical diagnosis.'),
   ('QR', 'Selfix is free. Scan the code or use the link in bio.')]),
}
LBL = {'tr': dict(ios='App Store', andr='Google Play', free='Ücretsiz • 17 dil'), 'en': dict(ios='App Store', andr='Google Play', free='Free • 17 languages')}

def qr(url, size):
    q = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M); q.add_data(url); q.make(fit=True)
    return q.make_image(fill_color=(20, 18, 40), back_color='white').convert('RGB').resize((size, size), Image.NEAREST)

SHOT = {}
def phone(name, h=860):
    if name not in SHOT:
        im = Image.open(SHOTS / f'iPhone_6.7_inch_{name}.png').convert('RGB')
        w = int(im.width * h / im.height); im = im.resize((w, h), Image.LANCZOS)
        mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), 56, fill=255)
        frame = Image.new('RGBA', (w + 36, h + 36), (0, 0, 0, 0)); ImageDraw.Draw(frame).rounded_rectangle((0, 0, w + 35, h + 35), 70, fill=(12, 12, 20, 255))
        frame.paste(im, (18, 18), mask)
        sh = Image.new('RGBA', (w + 120, h + 120), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((60, 70, w + 60, h + 70), 70, fill=(0, 0, 0, 150))
        sh = sh.filter(ImageFilter.GaussianBlur(28)); sh.alpha_composite(frame, (42, 42))
        SHOT[name] = sh
    return SHOT[name]

QRS = {}
def frame(job, t):
    im = v.base(job); d = ImageDraw.Draw(im); v.header(d, job, 1080)
    i, s, u = v.active(job, t); lang = job['lang']
    v.center(d, job['hook'], 540, 190, 62, v.WHITE, 940, 'ExtraBold')
    sc = s['scene']
    if sc is None:
        r = 200 + 14 * math.sin(t * 1.3)
        d.ellipse((540 - r, 760 - r, 540 + r, 760 + r), outline=v.LAV, width=6)
        v.center(d, '?', 540, 640, 220, v.CORAL, 400, 'ExtraBold', gap=1)
    elif sc == 'QR':
        if 'q' not in QRS: QRS['q'] = (qr(IOS, 340), qr(AND, 340))
        a, b = QRS['q']
        for k, (img, label, x) in enumerate(((a, LBL[lang]['ios'], 120), (b, LBL[lang]['andr'], 620))):
            pop = min(1, max(0, (t - s['start']) / 0.35 - k * 0.3))
            if pop <= 0: continue
            d.rounded_rectangle((x - 20, 470, x + 360, 900), 36, fill=(255, 255, 255))
            im.paste(img, (x, 490)); v.center(d, label, x + 170, 840, 40, (20, 18, 40), 360, 'ExtraBold')
        v.center(d, LBL[lang]['free'], 540, 940, 44, v.MINT, 900, 'Bold')
    else:
        ph = phone(sc); x = (1080 - ph.width) // 2; slide = max(0, 1 - (t - s['start']) / 0.35)
        im.paste(ph, (x, 330 + int(slide * 120)), ph)
        d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 1250 if sc not in (None, 'QR') else 1060, 1020, 1440 if sc not in (None, 'QR') else 1400), 36, fill=(30, 28, 58))
    v.reveal(d, s['text'], 540, (1285 if sc not in (None, 'QR') else 1100), 44, 880, u)
    v.center(d, 'Selfix', 540, 1490, 30, v.LAV, 900, 'ExtraBold')
    return im

def build(lang):
    c = SCRIPTS[lang]; narr = 'M2' if lang == 'tr' else 'M1'
    segs = [dict(text=tx, voice=narr, role='N', scene=sc, pause=0.5) for sc, tx in c['scenes']]
    segs[-1]['pause'] = 2.2
    return dict(id=f'sv_promo_{lang.upper()}', lang=lang, kind='promo', fmt='short', hook=c['hook'], segs=segs, speed=1.04)

v.frame = lambda job, t: frame(job, t) if job['kind'] == 'promo' else None

if __name__ == '__main__':
    for lang in ('tr', 'en'):
        j = build(lang)
        if '--still' in sys.argv:
            v.make_audio(j)
            for k, s in enumerate(j['segs']): frame(j, s['end'] - 0.1).save(ROOT / 'production' / f'promo_{lang}_{k}.jpg', quality=85)
            continue
        print(v._produce(j))
