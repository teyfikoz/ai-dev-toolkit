"""Builds the Selfix YouTube release plan (new viral pack + 8 finished older originals)."""
import json, hashlib, subprocess, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'production'))
from content import SKITS, NARRATED, LONG

IST = ZoneInfo('Europe/Istanbul')
CH = 'UCsPhsanizD_dZUJGMj-TdKQ'
OLD = Path('/Users/teyfikoz/Desktop/Shorts_100M_Lab_2026-11-14/selfix_research')
IOS = 'https://apps.apple.com/app/id6760978989'
AND = 'https://play.google.com/store/apps/details?id=com.teyfikoz.personalite'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

TAGS = {'tr': '#Shorts #Psikoloji #ÖzFarkındalık #KişiselGelişim #Selfix', 'en': '#Shorts #Psychology #SelfAwareness #SelfGrowth #Selfix'}
FOOT = {
 'tr': 'Özgün senaryo ve animasyon; yerel sentetik ses ve özgün fon müziği. Genel farkındalık içeriğidir; tanı veya tedavi değildir. Popüler psikoloji videolarındaki konulardan esinlenen özgün metin; alıntı veya çeviri yoktur.',
 'en': 'Original script and animation; local synthetic voice and original music. General self-awareness content, not diagnosis or treatment. Original writing inspired by popular psychology topics; no quotes or translations.'}
APP = {'tr': f'Kendini keşfetmek için Selfix:\niOS: {IOS}\nAndroid: {AND}\nInstagram: https://www.instagram.com/selfixxapp/',
       'en': f'Explore yourself with Selfix:\niOS: {IOS}\nAndroid: {AND}\nInstagram: https://www.instagram.com/selfixxapp/'}

def font(n, w='ExtraBold'): return ImageFont.truetype(str(ROOT / 'fonts' / f'PJS-{w}.ttf'), n)

def long_thumb(title, lang, dest):
    W, H = 1280, 720
    im = Image.new('RGB', (W, H), (16, 16, 38)); d = ImageDraw.Draw(im)
    for r in range(380, 120, -40): d.ellipse((980 - r, 360 - r, 980 + r, 360 + r), outline=(70 + (380 - r) // 4, 60, 140), width=3)
    d.text((980 - d.textlength('9', font=font(380)) / 2, 120), '9', font=font(380), fill=(255, 150, 135))
    big = 'HEP MÜSAİT OLMAYI BIRAK' if lang == 'tr' else 'STOP BEING ALWAYS AVAILABLE'
    words, lines, line = big.split(), [], ''
    for w in words:
        t = (line + ' ' + w).strip()
        if line and d.textlength(t, font=font(82)) > 700: lines.append(line); line = w
        else: line = t
    lines.append(line)
    for i, l in enumerate(lines): d.text((60, 150 + i * 100), l, font=font(82), fill=(244, 244, 252))
    d.text((62, 150 + len(lines) * 100 + 20), 'değişen 9 şey' if lang == 'tr' else '9 things that change', font=font(44, 'Bold'), fill=(194, 172, 255))
    d.text((60, 640), 'SELFIX', font=font(40), fill=(194, 172, 255))
    im.save(dest, quality=92)

def portrait_cover(video, dest, at=0.4):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(at), '-i', str(video), '-frames:v', '1', '-q:v', '2', str(dest)], check=True)

def main():
    jobs = []
    order_tr = ['compliment', 'available', 'cantsayno', 'burden', 'wetalk', 'unshakable', 'luck', 'sorry', 'introvert', 'quietplans', 'boundary', 'repair', 'label', 'roles']
    meta = {}
    for s in SKITS:
        for lang in ('tr', 'en'):
            c = s[lang]; meta[(s['slug'], lang)] = (c['hook'], c['insight'][:2])
    for s in NARRATED:
        for lang in ('tr', 'en'):
            c = s[lang]; meta[(s['slug'], lang)] = (c['hook'], c['lines'][1:3])
    start = datetime(2026, 11, 21, tzinfo=IST)
    for i, slug in enumerate(order_tr):
        for lang in ('tr', 'en'):
            when = (start + timedelta(days=i)).replace(hour=19) if lang == 'tr' else (start + timedelta(days=i + 1)).replace(hour=2)
            if slug in ('boundary', 'repair', 'label', 'roles'):
                video = OLD / 'publish' / f'selfix_{slug}_{lang.upper()}.mp4'
                m = next(x for x in json.loads((OLD / 'manifest.json').read_text()) if x['job_id'] == f'selfix_{slug}_{lang.upper()}')
                title = m['title']; body = [s['text'] for s in m['scenes'][1:3]]
                cover = ROOT / 'covers' / f'old_{slug}_{lang.upper()}_cover.jpg'; portrait_cover(video, cover)
                jid = f'old_{slug}_{lang.upper()}'
            else:
                jid = f'sv_{slug}_{lang.upper()}'
                video = ROOT / 'videos' / f'{jid}_YT.mp4'; cover = ROOT / 'covers' / f'{jid}_cover.jpg'
                title, body = meta[(slug, lang)]
            desc = f"{title}\n\n" + '\n'.join(body) + f"\n\n{APP[lang]}\n\n{FOOT[lang]}\n\n{TAGS[lang]}"
            yt_title = (title.rstrip('.') + ' #shorts')[:100]
            jobs.append(dict(id=jid, kind='short', language=lang, title=yt_title, description=desc, video=str(video), sha256=sha(video),
                             thumbnail=str(cover), thumbnail_sha256=sha(cover), publish_at=when.isoformat(), channel_id=CH))
    for s in LONG:
        for lang, when in (('tr', datetime(2026, 11, 28, 20, tzinfo=IST)), ('en', datetime(2026, 11, 29, 3, tzinfo=IST))):
            c = s[lang]; jid = f"sv_{s['slug']}_{lang.upper()}_LONG"
            video = ROOT / 'videos' / f'{jid}_YT.mp4'; thumb = ROOT / 'covers' / f'{jid}_thumb_1280.jpg'; long_thumb(c['title'], lang, thumb)
            m = json.loads((ROOT / 'production' / jid / 'meta.json').read_text())
            chap, idx = [], 0
            for seg in m['segs']:
                if seg['role'] == 'chtitle':
                    idx += 1; t = int(seg['start']); chap.append(f"{t//60:02d}:{t%60:02d} {idx}. {c['chapters'][idx-1][0]}")
            chap.insert(0, '00:00 ' + ('Giriş' if lang == 'tr' else 'Intro'))
            desc = c['intro'][0] + '\n\n' + ('Bölümler' if lang == 'tr' else 'Chapters') + ':\n' + '\n'.join(chap) + f"\n\n{APP[lang]}\n\n{FOOT[lang]}\n\n" + ('#Psikoloji #Sınırlar #ÖzFarkındalık #KişiselGelişim #Selfix' if lang == 'tr' else '#Psychology #Boundaries #SelfAwareness #SelfGrowth #Selfix')
            jobs.append(dict(id=jid, kind='long', language=lang, title=c['title'], description=desc, video=str(video), sha256=sha(video),
                             thumbnail=str(thumb), thumbnail_sha256=sha(thumb), publish_at=when.isoformat(), channel_id=CH))
    jobs.sort(key=lambda j: j['publish_at'])
    assert len({j['sha256'] for j in jobs}) == len(jobs), 'DUPLICATE_VIDEO'
    plan = dict(channel_id=CH, created_at=datetime.now(IST).isoformat(), selfix_daily_upload_limit=3, shared_grim_selfix_daily_cap=6, paid_api_calls=0, jobs=jobs)
    (ROOT / 'youtube' / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    for j in jobs: print(j['publish_at'][:16], j['id'], '|', j['title'])
    print(len(jobs), 'jobs')

if __name__ == '__main__': main()
