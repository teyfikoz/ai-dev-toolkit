"""Selfix multi-video release worker. Dry run by default.

Guards: live channel identity, asset hashes, shared Grim/Selfix local daily cap (6) with a
Selfix sub-limit (4), private upload -> processing -> thumbnail readback -> publishAt readback.
Interrupted uploads without an ID are held for owner reconciliation (no blind re-upload).
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import argparse, fcntl, hashlib, json, sys, time

ROOT = Path(__file__).resolve().parent
PLAN = ROOT / 'plan.json'; STATE = ROOT / 'receipts.json'
GRIM = Path('/Users/teyfikoz/Desktop/Grimfiles_2026-11-16')
OLD = Path('/Users/teyfikoz/Desktop/Selfix_Original_20261117')
TOKEN = Path('/Users/teyfikoz/Projects/content/youtube/scripts/token_selfixxapp.json')
EXPECTED = 'UCsPhsanizD_dZUJGMj-TdKQ'
PT = ZoneInfo('America/Los_Angeles')
sys.path.insert(0, str(OLD / 'production'))

def read(p, d): return json.loads(p.read_text()) if p.exists() else d
def save(p, data):
    tmp = p.with_suffix('.tmp'); tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1)); tmp.replace(p)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now(): return datetime.now(timezone.utc)

def validate(job):
    if job['channel_id'] != EXPECTED: raise ValueError('WRONG_TARGET_CHANNEL')
    if sha(job['video']) != job['sha256'] or sha(job['thumbnail']) != job['thumbnail_sha256']: raise ValueError('ASSET_HASH_MISMATCH')
    from PIL import Image
    with Image.open(job['thumbnail']) as im:
        want = 9 / 16 if job['kind'] == 'short' else 16 / 9
        if abs(im.width / im.height - want) > .02: raise ValueError('THUMBNAIL_ASPECT')

def uploads_today(state):
    day = now().astimezone(PT).date().isoformat()
    own = state.get('quota_days', {}).get(day, {}).get('uploads', 0)
    grim = read(GRIM / 'youtube_upload_receipts.json', {}).get('quota_days', {}).get(day, {}).get('uploads', 0)
    pilots = read(OLD / 'youtube/upload_receipts.json', {}).get('quota_days', {}).get(day, {}).get('uploads', 0)
    return day, own, grim + pilots

def client():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_httplib2 import AuthorizedHttp
    from googleapiclient.discovery import build
    import httplib2
    c = Credentials.from_authorized_user_file(str(TOKEN))
    if not c.valid: c.refresh(Request())
    return build('youtube', 'v3', http=AuthorizedHttp(c, http=httplib2.Http(timeout=60)), cache_discovery=False)

def identity(y):
    rows = y.channels().list(part='id,snippet', mine=True).execute().get('items', [])
    if len(rows) != 1 or rows[0]['id'] != EXPECTED: raise ValueError('LIVE_ACCOUNT_IDENTITY_MISMATCH')
    return {'channel_id': rows[0]['id'], 'title': rows[0]['snippet']['title'], 'checked_at': now().isoformat()}

def process(y, job, ev, state, limit):
    from googleapiclient.http import MediaFileUpload
    from shorts_thumbnail_readback import verify
    validate(job)
    target = datetime.fromisoformat(job['publish_at'])
    if not ev.get('video_id'):
        if ev.get('phase') == 'UPLOAD_STARTED': raise RuntimeError('AMBIGUOUS_UPLOAD_REQUIRES_OWNER_RECONCILIATION')
        if target < now() + timedelta(hours=2): ev['phase'] = 'SKIPPED_TOO_LATE'; save(STATE, state); return 'late'
        day, own, other = uploads_today(state)
        if own >= limit or own + other >= 6: return 'cap'
        ev.update(phase='UPLOAD_STARTED', started_at=now().isoformat()); save(STATE, state)
        body = {'snippet': {'title': job['title'], 'description': job['description'], 'categoryId': '27',
                            'defaultLanguage': job['language'], 'defaultAudioLanguage': job['language']},
                'status': {'privacyStatus': 'private', 'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}}
        req = y.videos().insert(part='snippet,status', notifySubscribers=False, body=body,
                                media_body=MediaFileUpload(job['video'], mimetype='video/mp4', chunksize=8 * 1024 * 1024, resumable=True))
        resp = None
        try:
            while resp is None: _, resp = req.next_chunk(num_retries=3)
        except Exception as e:
            st = getattr(getattr(e, 'resp', None), 'status', None)
            if st in (400, 403) and resp is None:
                ev.update(phase='PREPARED', rejected_before_upload=str(e)[:200]); save(STATE, state)
            raise
        if not resp.get('id'): raise RuntimeError('MISSING_UPLOAD_ID')
        ev.update(video_id=resp['id'], phase='UPLOADED_PRIVATE', uploaded_at=now().isoformat())
        state.setdefault('quota_days', {}).setdefault(day, {'uploads': 0})['uploads'] += 1; save(STATE, state)
    vid = ev['video_id']; row = None
    for _ in range(40):
        rows = y.videos().list(part='snippet,status,processingDetails', id=vid).execute().get('items', [])
        if len(rows) != 1 or rows[0]['snippet']['channelId'] != EXPECTED: raise RuntimeError('VIDEO_IDENTITY_MISMATCH')
        row = rows[0]; st = row.get('processingDetails', {}).get('processingStatus')
        if st == 'succeeded': break
        if st in ('failed', 'terminated'): raise RuntimeError('VIDEO_PROCESSING_FAILED')
        time.sleep(6)
    if row.get('processingDetails', {}).get('processingStatus') != 'succeeded':
        ev['phase'] = 'WAITING_PROCESSING'; save(STATE, state); return 'wait'
    if not ev.get('thumbnail_set'):
        y.thumbnails().set(videoId=vid, media_body=MediaFileUpload(job['thumbnail'], mimetype='image/jpeg')).execute()
        ev['thumbnail_set'] = now().isoformat(); save(STATE, state)
    if job['kind'] == 'short' and not ev.get('thumbnail_readback', {}).get('match'):
        for _ in range(5):
            ev['thumbnail_readback'] = verify(y, vid, job['thumbnail'], ROOT); save(STATE, state)
            if ev['thumbnail_readback'].get('match'): break
            time.sleep(8)
        if not ev['thumbnail_readback'].get('match'):
            ev['phase'] = 'PRIVATE_THUMBNAIL_REVIEW'; save(STATE, state); return 'thumb'
    if target < now() + timedelta(minutes=20): ev['phase'] = 'PRIVATE_SCHEDULE_TOO_LATE'; save(STATE, state); return 'late'
    y.videos().update(part='status', body={'id': vid, 'status': {'privacyStatus': 'private', 'publishAt': target.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
                                                               'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}}).execute()
    for _ in range(6):
        r = y.videos().list(part='snippet,status', id=vid).execute()['items'][0]
        at = r['status'].get('publishAt')
        if at and datetime.fromisoformat(at.replace('Z', '+00:00')) == target and r['status']['privacyStatus'] == 'private':
            ev.update(phase='COMPLETE', publish_at_readback=at, verified_at=now().isoformat(), url=f'https://www.youtube.com/watch?v={vid}'); save(STATE, state); return 'ok'
        time.sleep(4)
    ev['phase'] = 'SCHEDULE_READBACK_PENDING'; save(STATE, state); return 'pending'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--execute', action='store_true'); a = ap.parse_args()
    plan = read(PLAN, {})
    if plan.get('channel_id') != EXPECTED: raise ValueError('UNEXPECTED_PLAN')
    for j in plan['jobs']: validate(j)
    state = read(STATE, {'channel_id': EXPECTED, 'assets': {}, 'quota_days': {}})
    pending = [j for j in plan['jobs'] if state['assets'].get(j['sha256'], {}).get('phase') != 'COMPLETE']
    if not a.execute:
        day, own, other = uploads_today(state)
        print(json.dumps({'status': 'DRY_RUN', 'jobs': len(plan['jobs']), 'pending': len(pending), 'today_pt': day, 'own_uploads': own, 'other_uploads': other})); return
    if not pending: print('NOOP_ALL_COMPLETE'); return
    with (GRIM / '.longform_upload.lock').open('a') as g, (ROOT / '.upload.lock').open('a') as o:
        try: fcntl.flock(g, fcntl.LOCK_EX | fcntl.LOCK_NB); fcntl.flock(o, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: print('NOOP_UPLOAD_WORKER_BUSY'); return
        y = client(); state['identity'] = identity(y); save(STATE, state)
        results = {}
        for j in sorted(pending, key=lambda x: x['publish_at']):
            ev = state['assets'].setdefault(j['sha256'], {'id': j['id'], 'phase': 'PREPARED'})
            if ev.get('phase') == 'SKIPPED_TOO_LATE': continue
            try: r = process(y, j, ev, state, plan.get('selfix_daily_upload_limit', 4))
            except Exception as e:
                ev['last_error'] = {'type': type(e).__name__, 'msg': str(e)[:300], 'status': getattr(getattr(e, 'resp', None), 'status', None), 'at': now().isoformat()}
                save(STATE, state); r = 'error'
                if getattr(getattr(e, 'resp', None), 'status', None) in (403, 429): results[j['id']] = r; break
            results[j['id']] = r
            if r == 'cap': break
        done = sum(v.get('phase') == 'COMPLETE' for v in state['assets'].values())
        print(json.dumps({'complete': done, 'total': len(plan['jobs']), 'this_run': results}, ensure_ascii=False))

if __name__ == '__main__':
    try: main()
    except Exception as e: print('SELFIX_VIRAL_QUEUE_HELD', type(e).__name__, str(e)[:200]); sys.exit(1)
