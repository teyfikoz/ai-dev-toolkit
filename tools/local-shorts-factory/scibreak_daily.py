"""SciBreak — "Space & Earth Today": daily data-driven Short from free public feeds (USGS, NOAA SWPC, JPL CNEOS, Open Notify).
Script is templated from the data (no LLM), so every number is traceable. Renders EN + TR, schedules both, deletes media after 3 days.
  scibreak_daily.py            produce + upload today's pair
  scibreak_daily.py --render   produce only"""
import sys, json, math, urllib.request, datetime as dt, shutil, hashlib
from pathlib import Path
from zoneinfo import ZoneInfo
sys.path.insert(0, '/Users/teyfikoz/Desktop/WhatIfLab_Viral_20261120/production')
import whatif_viral as w
v = w.v
from PIL import ImageDraw

BASE = Path(__file__).resolve().parent
IST = ZoneInfo('Europe/Istanbul'); TODAY = dt.datetime.now(IST).date()
DAY = BASE / TODAY.isoformat(); DAY.mkdir(exist_ok=True)
v.ROOT = BASE; v.OUT = DAY; v.CACHE = BASE / 'tts_cache'; v.CACHE.mkdir(exist_ok=True)
for d in ('covers', 'production/beds'): (BASE / d).mkdir(parents=True, exist_ok=True)
if not (BASE / 'fonts').exists(): shutil.copytree('/Users/teyfikoz/Desktop/Selfix_Viral_20261119/fonts', BASE / 'fonts')
CYAN = (80, 200, 255)

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'SciBreak/1.0'}), timeout=25) as r: return json.loads(r.read())

def facts():
    q = get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson')['features']
    top = max(q, key=lambda x: x['properties']['mag']) if q else None
    kp = get('https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json')[-1]
    kp = float(kp['Kp'] if isinstance(kp, dict) else kp[1])
    cad = get('https://ssd-api.jpl.nasa.gov/cad.api?date-min=now&date-max=%2B7&dist-max=0.05&sort=dist')
    ast = dict(zip(cad['fields'], cad['data'][0])) if cad.get('data') else None
    try: iss = get('http://api.open-notify.org/iss-now.json')['iss_position']
    except Exception: iss = None
    return dict(quakes=[(f['properties']['mag'], f['geometry']['coordinates'][0], f['geometry']['coordinates'][1]) for f in q],
                n=len(q), top=(top['properties']['mag'], top['properties']['place']) if top else None, kp=kp, ast=ast,
                iss=(float(iss['latitude']), float(iss['longitude'])) if iss else None)

def size_range(h):
    d = lambda p: 1329 / math.sqrt(p) * 10 ** (-h / 5) * 1000
    lo, hi = d(0.25), d(0.05)
    r = lambda x: int(round(x, -1)) if x >= 20 else max(1, int(round(x)))
    return r(lo), r(hi)

DIRS = {'north': 'kuzeyinde', 'south': 'güneyinde', 'east': 'doğusunda', 'west': 'batısında', 'northeast': 'kuzeydoğusunda', 'northwest': 'kuzeybatısında',
        'southeast': 'güneydoğusunda', 'southwest': 'güneybatısında', 'N': 'kuzeyinde', 'S': 'güneyinde', 'E': 'doğusunda', 'W': 'batısında', 'NE': 'kuzeydoğusunda',
        'NW': 'kuzeybatısında', 'SE': 'güneydoğusunda', 'SW': 'güneybatısında', 'NNE': 'kuzeydoğusunda', 'ENE': 'kuzeydoğusunda', 'ESE': 'güneydoğusunda', 'SSE': 'güneydoğusunda',
        'SSW': 'güneybatısında', 'WSW': 'güneybatısında', 'WNW': 'kuzeybatısında', 'NNW': 'kuzeybatısında'}
def trn(x, nd=1): return f"{x:.{nd}f}".replace('.', ',')
def place_tr(p):
    import re
    m = re.match(r'(\d+) km ([NSEW]{1,3}) of (.+)', p)
    if m: return f"merkez üssü {m.group(3)} bölgesinin yaklaşık {m.group(1)} km {DIRS.get(m.group(2), '')}"
    m = re.match(r'(north|south|east|west|northeast|northwest|southeast|southwest|south southeast|north northeast)\s+of (the )?(.+)', p)
    if m: return f"merkez üssü {m.group(3)} bölgesinin {DIRS.get(m.group(1).split()[-1], '')}"
    return f"merkez üssü {p.replace(' region', '')} bölgesinde"

def script(F, lang):
    S = []; en = lang == 'en'
    date_s = TODAY.strftime('%B %-d') if en else f"{TODAY.day} {['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'][TODAY.month-1]}"
    S.append(('globe', None, f"Earth and space today, {date_s}." if en else f"Bugün Dünya ve uzay, {date_s}."))
    if F['top']:
        m, place = F['top']
        S.append(('quakes', f"{F['n']} × M4.5+", f"In the last 24 hours, {F['n']} earthquakes of magnitude 4.5 or more were recorded. The strongest, magnitude {m:.1f}, struck {place}."
                  if en else f"Son 24 saatte 4,5 ve üzeri büyüklükte {F['n']} deprem kaydedildi. En güçlüsü {trn(m)} büyüklüğündeydi; {place_tr(place)}."))
    kp = F['kp']; storm = kp >= 5
    lvl_en = 'storm level' if storm else ('active' if kp >= 4 else 'quiet'); lvl_tr = 'fırtına seviyesinde' if storm else ('hareketli' if kp >= 4 else 'sakin')
    S.append(('kp', f"Kp {kp:.1f}", f"Geomagnetic activity is {lvl_en}, with a planetary K index of {kp:.1f}. " + ("Auroras may reach lower latitudes tonight." if storm else "Auroras stay close to the poles.")
              if en else f"Jeomanyetik aktivite {lvl_tr}; gezegensel K endeksi {trn(kp)}. " + ("Kutup ışıkları bu gece daha güneyden görülebilir." if storm else "Kutup ışıkları kutuplara yakın kalıyor.")))
    if F['ast']:
        a = F['ast']; ld = float(a['dist']) * 149597870.7 / 384400; lo, hi = size_range(float(a['h']))
        when = dt.datetime.strptime(a['cd'], '%Y-%b-%d %H:%M')
        wd = when.strftime('%B %-d') if en else f"{when.day} {['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'][when.month-1]}"
        S.append(('asteroid', f"{ld:.1f} × Moon", f"Asteroid {a['des']}, roughly {lo} to {hi} meters across, passes Earth on {wd} at {ld:.1f} times the Moon's distance, moving {float(a['v_rel']):.1f} kilometers per second."
                  if en else f"{a['des']} adlı asteroit, yaklaşık {lo} ila {hi} metre çapında, {wd} günü Ay mesafesinin {trn(ld)} katından saniyede {trn(float(a['v_rel']))} kilometre hızla geçecek."))
    if F['iss']:
        la, lo_ = F['iss']; ns = ('north' if la >= 0 else 'south') if en else ('kuzey' if la >= 0 else 'güney'); ew = ('east' if lo_ >= 0 else 'west') if en else ('doğu' if lo_ >= 0 else 'batı')
        S.append(('iss', '92 min', f"The International Space Station is now above {abs(la):.0f} degrees {ns}, {abs(lo_):.0f} degrees {ew}, circling Earth about every 92 minutes."
                  if en else f"Uluslararası Uzay İstasyonu şu an {abs(la):.0f} derece {ns}, {abs(lo_):.0f} derece {ew} üzerinde; Dünya'nın çevresini yaklaşık 92 dakikada dolaşıyor."))
    S.append(('end', None, "Data from USGS, NOAA and NASA JPL. Follow SciBreak for tomorrow's update." if en else "Veriler USGS, NOAA ve NASA JPL'den. Yarının özeti için SciBreak'i takip et."))
    return S

def sphere(lat, lon, cx, cy, r, lon0):
    la, lo = math.radians(lat), math.radians(lon - lon0)
    x, z = math.cos(la) * math.sin(lo), math.cos(la) * math.cos(lo)
    return (cx + r * x, cy - r * math.sin(la), z > 0)

def grid_globe(d, cx, cy, r, lon0):
    d.ellipse((cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), fill=(30, 60, 110))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(22, 70, 140))
    for la in range(-60, 61, 30):
        pts = [sphere(la, lo, cx, cy, r, lon0) for lo in range(-180, 181, 5)]
        seg = [(x, y) for x, y, vz in pts if vz]
        if len(seg) > 1: d.line(seg, fill=(70, 120, 190), width=2)
    for lo in range(-180, 180, 30):
        pts = [sphere(la, lo, cx, cy, r, lon0) for la in range(-90, 91, 5)]
        seg = [(x, y) for x, y, vz in pts if vz]
        if len(seg) > 1: d.line(seg, fill=(70, 120, 190), width=2)

def illus(im, d, vis, t, u, F):
    cx, cy, r = 540, 820, 250
    if vis in ('globe', 'quakes', 'iss', 'kp', 'end'):
        lon0 = (F['iss'][1] if vis == 'iss' and F['iss'] else (F['top'] and F['quakes'] and max(F['quakes'])[1]) or 0) or 0
        if vis in ('quakes', 'iss'): grid_globe(d, cx, cy, r, lon0)
        else: w.earth(d, cx, cy, r, t * 0.3)
        if vis == 'quakes':
            for m, lo, la in F['quakes']:
                x, y, vis_ = sphere(la, lo, cx, cy, r, lon0)
                if vis_:
                    rr = 12 + (m - 4.5) * 14 + 5 * math.sin(t * 4)
                    d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 90, 70), width=4)
        if vis == 'iss' and F['iss']:
            x, y, _ = sphere(F['iss'][0], F['iss'][1], cx, cy, r + 40, lon0)
            d.ellipse((cx - r - 40, cy - (r + 40) * 0.35, cx + r + 40, cy + (r + 40) * 0.35), outline=(120, 140, 190), width=2)
            d.rectangle((x - 18, y - 6, x + 18, y + 6), fill=v.WHITE); d.rectangle((x - 40, y - 3, x - 20, y + 3), fill=CYAN); d.rectangle((x + 20, y - 3, x + 40, y + 3), fill=CYAN)
        if vis == 'kp':
            for k in range(10):
                a = math.radians(200 - k * 22); col = (90, 200, 120) if k < 4 else ((255, 190, 60) if k < 5 else (255, 80, 70))
                x0, y0 = cx + 330 * math.cos(a), cy - 330 * math.sin(a); d.ellipse((x0 - 16, y0 - 16, x0 + 16, y0 + 16), fill=col if k <= F['kp'] else (50, 50, 70))
    elif vis == 'asteroid':
        w.earth(d, 260, cx, 120, t * 0.3)
        ld = float(F['ast']['dist']) * 149597870.7 / 384400 if F['ast'] else 1
        moon_x = 260 + 560 / max(ld, 1) if ld > 1 else 820
        d.ellipse((900 - 34, cx - 34, 900 + 34, cx + 34), fill=(190, 190, 200))
        d.text((860, cx + 50), 'MOON' if True else '', font=v.font(24, 'Bold'), fill=(160, 160, 180))
        ax = 1000 - 640 * u; ay = cx - 220 + 80 * math.sin(u * 3)
        d.line((1060, cx - 300, ax, ay), fill=(110, 110, 150), width=2); d.ellipse((ax - 14, ay - 12, ax + 14, ay + 12), fill=(200, 160, 120))
    return d

def frame(job, t):
    im = w.bg(); d = ImageDraw.Draw(im)
    i, s, u = v.active(job, t)
    d.text((70, 80), 'SCIBREAK', font=v.font(38, 'ExtraBold'), fill=CYAN)
    v.center(d, job['hook'], 540, 190, 60, v.WHITE, 960, 'ExtraBold')
    d = illus(im, d, s['visual'], t, u, job['facts'])
    if s.get('stat'):
        size = 72; wdt = d.textlength(s['stat'], font=v.font(size, 'ExtraBold'))
        d.rounded_rectangle((540 - wdt / 2 - 34, 1120, 540 + wdt / 2 + 34, 1130 + size + 26), 30, fill=CYAN)
        d.text((540 - wdt / 2, 1132), s['stat'], font=v.font(size, 'ExtraBold'), fill=(10, 20, 35))
    d.rounded_rectangle((60, 1250, 1020, 1470), 34, fill=(16, 22, 44)); v.reveal(d, s['text'], 540, 1278, 40, 890, u)
    return im

def produce(F):
    jobs = []
    for lang in ('en', 'tr'):
        segs = [dict(text=tx, voice='M1' if lang == 'en' else 'M2', role='N', visual=vis, stat=st, pause=0.3) for vis, st, tx in script(F, lang)]
        hook = 'Space & Earth Today' if lang == 'en' else 'Bugün Uzay ve Dünya'
        jobs.append(dict(id=f"sb_{TODAY:%Y%m%d}_{lang.upper()}", lang=lang, kind='sb', fmt='short', hook=hook, segs=segs, speed=1.05, facts=F))
    if not (BASE / 'production/beds/warm.wav').exists(): v.synth_bed(BASE / 'production/beds/warm.wav'); v.synth_bed(BASE / 'production/beds/calm.wav', 120, calm=True)
    v.frame = frame
    for j in jobs: print(v._produce(j), flush=True)
    return jobs

def upload(jobs):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    c = Credentials.from_authorized_user_file('/Users/teyfikoz/Projects/content/youtube/scripts/token_curiousuniverse.json')
    if not c.valid: c.refresh(Request())
    y = build('youtube', 'v3', credentials=c, cache_discovery=False)
    ch = y.channels().list(part='snippet', mine=True).execute()['items'][0]['snippet']['title']
    assert ch == 'SciBreak', ch
    rec_p = BASE / 'receipts.json'; rec = json.loads(rec_p.read_text()) if rec_p.exists() else {}
    for j, hm in zip(jobs, ((18, 0), (19, 30))):
        if rec.get(j['id'], {}).get('video_id'): continue
        vid_path = DAY / f"{j['id']}_YT.mp4"
        when = dt.datetime.combine(TODAY, dt.time(*hm), IST)
        if when < dt.datetime.now(IST) + dt.timedelta(minutes=90): when += dt.timedelta(days=1)
        text = '\n'.join(s['text'] for s in j['segs'])
        title = (('Space & Earth Today — ' + TODAY.strftime('%b %-d, %Y')) if j['lang'] == 'en' else ('Bugün Uzay ve Dünya — ' + TODAY.strftime('%d.%m.%Y'))) + ' #shorts'
        desc = text + ('\n\nSources: USGS Earthquake Hazards Program, NOAA SWPC planetary K index, NASA JPL CNEOS close approaches, Open Notify ISS position. Automated data summary; synthetic voice.\n\n#Shorts #Space #Earthquake #Asteroid #Science'
                       if j['lang'] == 'en' else '\n\nKaynaklar: USGS deprem programı, NOAA SWPC K endeksi, NASA JPL CNEOS yakın geçişler, Open Notify ISS konumu. Otomatik veri özeti; sentetik ses.\n\n#Shorts #Uzay #Deprem #Asteroit #Bilim')
        body = {'snippet': {'title': title[:100], 'description': desc, 'categoryId': '28', 'defaultLanguage': j['lang'], 'defaultAudioLanguage': j['lang']},
                'status': {'privacyStatus': 'private', 'publishAt': when.astimezone(dt.timezone.utc).isoformat().replace('+00:00', 'Z'), 'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}}
        req = y.videos().insert(part='snippet,status', body=body, notifySubscribers=False, media_body=MediaFileUpload(str(vid_path), mimetype='video/mp4', resumable=True))
        resp = None
        while resp is None: _, resp = req.next_chunk(num_retries=3)
        got = y.videos().list(part='status', id=resp['id']).execute()['items'][0]['status']
        rec[j['id']] = {'video_id': resp['id'], 'publishAt': got.get('publishAt'), 'sha256': hashlib.sha256(vid_path.read_bytes()).hexdigest()}
        rec_p.write_text(json.dumps(rec, indent=1)); print('UPLOADED', j['id'], resp['id'], got.get('publishAt'), flush=True)

def cleanup():
    for d in BASE.glob('20??-??-??'):
        try:
            if (TODAY - dt.date.fromisoformat(d.name)).days > 3: shutil.rmtree(d)
        except ValueError: pass
    shutil.rmtree(BASE / 'production', ignore_errors=True) if False else None

if __name__ == '__main__':
    F = facts(); (DAY / 'facts.json').write_text(json.dumps(F, indent=1, default=str))
    jobs = produce(F)
    if '--render' not in sys.argv: upload(jobs)
    cleanup()
