"""Translate Selfix YouTube titles + short descriptions into the app's 17 languages (Groq, free tier). Cached in translations.json."""
import json, os, re, sys, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'translations.json'
LANGS = {'en': 'English', 'tr': 'Turkish', 'de': 'German', 'es': 'Spanish', 'fr': 'French', 'it': 'Italian', 'pt': 'Portuguese (Brazil)', 'nl': 'Dutch',
         'pl': 'Polish', 'ru': 'Russian', 'sv': 'Swedish', 'no': 'Norwegian Bokmål', 'da': 'Danish', 'fi': 'Finnish', 'ja': 'Japanese', 'ko': 'Korean', 'zh': 'Simplified Chinese'}
KEY = next(l.split('=', 1)[1].strip().strip('"') for l in open(os.path.expanduser('~/.claude/projects/-Users-teyfikoz/memory/secrets.env')) if l.startswith('GROQ_API_KEY='))

def groq(prompt):
    body = {'model': 'openai/gpt-oss-120b', 'temperature': 0.2, 'response_format': {'type': 'json_object'},
            'messages': [{'role': 'system', 'content': 'You are a professional app-store and YouTube localizer. Natural, concise, culturally fluent. Return strict JSON only.'},
                         {'role': 'user', 'content': prompt}]}
    req = urllib.request.Request('https://api.groq.com/openai/v1/chat/completions', data=json.dumps(body).encode(),
                                 headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json', 'User-Agent': 'OpenAI/Python 1.0.0'})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r: return json.loads(json.loads(r.read())['choices'][0]['message']['content'])
        except Exception as e:
            time.sleep(8 * (i + 1)); err = e
    raise err

def main():
    plan = json.loads((ROOT / 'plan.json').read_text()); cache = json.loads(OUT.read_text()) if OUT.exists() else {}
    for j in plan['jobs']:
        if j['id'] in cache and len(cache[j['id']]) >= 16: continue
        src_lang = j['language']; title = re.sub(r'\s*#shorts$', '', j['title'])
        summary = j['description'].split('\n\n')[1] if j['kind'] == 'short' else j['description'].split('\n\n')[0]
        targets = {k: v for k, v in LANGS.items() if k != src_lang}
        prompt = (f"Source language: {LANGS[src_lang]}. Translate for a self-discovery app's YouTube video.\n"
                  f"TITLE (max 90 chars, keep it a curiosity hook, no hashtags): {title}\nSUMMARY (1-3 short lines): {summary}\n"
                  f"Return JSON: {{\"<code>\": {{\"title\": \"...\", \"summary\": \"...\"}}}} for codes: {', '.join(targets)}. "
                  "Do not add claims, diagnoses or emojis.")
        res = groq(prompt)
        cache[j['id']] = {k: res[k] for k in targets if k in res and res[k].get('title')}
        OUT.write_text(json.dumps(cache, ensure_ascii=False, indent=1)); print(j['id'], len(cache[j['id']]), flush=True)
        time.sleep(2)

if __name__ == '__main__': main()
