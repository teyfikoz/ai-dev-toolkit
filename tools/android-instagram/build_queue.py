"""Build/extend queue.json: Ariabella days from the iCloud November plan + Selfix daily reels. Idempotent by id."""
import json, re, glob
from pathlib import Path
from datetime import datetime, date, timedelta
ROOT = Path(__file__).resolve().parent
Q = ROOT / 'queue.json'
AB = Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/Ariabella_Instagram'
PLAN = AB / 'KASIM_GUNLUK_YAPILACAKLAR.md'
SV = Path('/Users/teyfikoz/Desktop/Selfix_Viral_20261119')
OLD = Path('/Users/teyfikoz/Desktop/Selfix_Original_20261117')
OLDR = Path('/Users/teyfikoz/Desktop/Shorts_100M_Lab_2026-11-14/selfix_research')
FIRST_COMMENT = 'Full video + more looks on YouTube 👉 link in bio'

def iso(d, hm): return f"{d.isoformat()}T{hm}:00+03:00"

def ariabella(from_day=date(2026, 11, 20), to_day=date(2026, 11, 30)):
    text = PLAN.read_text(); items = []
    blocks = re.split(r'\n## GÜN \d+ — ', text)[1:]
    dance_free = ['reels/loungewear/burgundy_velvet_robe.mp4', 'reels/resort/strapless_lace.mp4', 'reels/loungewear/white_linen_sunrise.mp4',
                  'reels/evening/mini_skirt.mp4', 'reels/loungewear/champagne_silk_robe.mp4']
    post_fill = ['posts/evening/lace_blazer', 'posts/evening/mini_skirt']
    for b in blocks:
        m = re.match(r'(\d{2})\.11', b)
        if not m: continue
        d = date(2026, 11, int(m.group(1)))
        if not (from_day <= d <= to_day): continue
        body = b.split('\n---')[0]
        for n, line in re.findall(r'\n(\d)\. (.+)', body):
            f = re.search(r'`([^`]+)`', line)
            if not f or not (AB / f.group(1)).exists(): continue
            it = dict(id=f'ab_{d:%m%d}_story{n}', account='ciaoariabella', kind='story', due=iso(d, f'18:0{int(n)-1}'),
                      media=[str(AB / f.group(1))], music={'mode': 'auto'}, status='pending')
            p = re.search(r'\*\*Anket\*\* sticker: "([^"]+)" \(([^/]+) / ([^)]+)\)', line)
            if p: it['poll'] = {'q': p.group(1), 'a': p.group(2).strip(), 'b': p.group(3).strip()}
            l = re.search(r'\*\*Bağlantı\*\* sticker: `([^`]+)` \(yazı: ([^)]+)\)', line)
            if l: it['link'] = {'url': 'https://' + l.group(1).replace('https://', ''), 'text': l.group(2).strip()}
            items.append(it)
        r = re.search(r'\*\*20:30 — Reel:\*\* `([^`]+)`(?: · açıklama: `([^`]+)`)?(?:.*?Açıklama: `([^`]+)`)?', body)
        if r:
            path, capf, inline = r.group(1), r.group(2), r.group(3)
            it = dict(id=f'ab_{d:%m%d}_reel', account='ciaoariabella', kind='reel', due=iso(d, '20:30'), music={'mode': 'auto', 'query': 'elegant lounge', 'rf': False}, status='pending')
            if 'Instagram Reels/' in path or not (AB / path).exists():
                alt = dance_free.pop(0) if dance_free else None
                if not alt: continue
                it['media'] = [str(AB / alt)]; it['caption_file'] = str(AB / alt.replace('.mp4', '_caption.txt')); it['note'] = f'dance file missing; replaced with unused {alt}'
            else:
                it['media'] = [str(AB / path)]; it['caption_file'] = str(AB / capf) if capf else None
                if not capf: it['caption'] = inline
            items.append(it)
        c = re.search(r'\*\*13:00 — Carousel:\*\* `([^`]+)`', body)
        folder = c.group(1).rstrip('/') if c else (post_fill.pop(0) if post_fill else None)
        if folder and (AB / folder).exists():
            imgs = sorted(glob.glob(str(AB / folder / '[0-9].jpg')))
            items.append(dict(id=f'ab_{d:%m%d}_post', account='ciaoariabella', kind='post', due=iso(d, '13:00'), media=imgs,
                              caption_file=str(AB / folder / 'caption.txt'), music={'mode': 'auto'}, status='pending', **({} if c else {'note': 'fill set (plan had no carousel)'})))
    return items

def selfix(start=date(2026, 11, 20)):
    items = []
    tr = ['cantsayno', 'burden', 'wetalk', 'unshakable', 'luck', 'sorry', 'introvert', 'quietplans']
    en = ['compliment', 'available', 'cantsayno', 'burden', 'wetalk', 'unshakable', 'luck', 'sorry', 'introvert', 'quietplans']
    for i, s in enumerate(tr):
        items.append(dict(id=f'sx_{s}_TR', account='selfixxapp', kind='reel', due=iso(start + timedelta(days=i), '20:00'),
                          media=[str(SV / 'ig' / f'sv_{s}_TR_IG720.mp4')], caption_file=str(SV / 'ig' / f'sv_{s}_TR_caption.txt'),
                          music={'mode': 'catalog', 'query': 'calm piano', 'rf': True, 'volume': 34}, status='pending'))
    for i, s in enumerate(en):
        items.append(dict(id=f'sx_{s}_EN', account='selfixxapp', kind='reel', due=iso(start + timedelta(days=i), '23:30'),
                          media=[str(SV / 'ig' / f'sv_{s}_EN_IG720.mp4')], caption_file=str(SV / 'ig' / f'sv_{s}_EN_caption.txt'),
                          music={'mode': 'catalog', 'query': 'calm piano', 'rf': True, 'volume': 34}, status='pending'))
    d0 = start + timedelta(days=len(tr))
    for j, (slug, lang, vid, cap, mode) in enumerate([
        ('boundary', 'TR', OLD / 'videos/selfix_boundary_TR_IG720.mp4', OLD / 'captions/selfix_boundary_TR_caption.txt', 'catalog'),
        ('repair', 'TR', OLD / 'videos/selfix_repair_TR_IG720.mp4', OLD / 'captions/selfix_repair_TR_caption.txt', 'catalog'),
        ('label', 'TR', OLDR / 'publish/selfix_label_TR.mp4', OLDR / 'publish/selfix_label_TR_caption.txt', 'none'),
        ('roles', 'TR', OLDR / 'publish/selfix_roles_TR.mp4', OLDR / 'publish/selfix_roles_TR_caption.txt', 'none')]):
        items.append(dict(id=f'sx_old_{slug}_{lang}', account='selfixxapp', kind='reel', due=iso(d0 + timedelta(days=j), '20:00'),
                          media=[str(vid)], caption_file=str(cap), music={'mode': mode, 'query': 'calm piano', 'rf': True, 'volume': 34}, status='pending'))
    return items

if __name__ == '__main__':
    q = json.loads(Q.read_text()) if Q.exists() else []
    have = {x['id'] for x in q}; new = [x for x in ariabella() + selfix() if x['id'] not in have]
    for x in new:
        missing = [m for m in x['media'] if not Path(m).exists()] + ([x['caption_file']] if x.get('caption_file') and not Path(x['caption_file']).exists() else [])
        if missing: x['status'] = 'blocked'; x['last_error'] = 'missing: ' + ', '.join(missing)
    q += new; Q.write_text(json.dumps(q, ensure_ascii=False, indent=1))
    from collections import Counter
    print('added', len(new), Counter((x['account'], x['kind']) for x in new), Counter(x['status'] for x in new))
    for x in new:
        if x['status'] != 'pending' or x.get('note'): print(x['id'], x['status'], x.get('note') or x.get('last_error'))
