#!/usr/bin/env python3
"""Bounded, serial delegation. Prompts via stdin; no prompt/key logging."""
import argparse, json, os, shutil, subprocess, sys, urllib.request, urllib.error
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('provider',choices=['codex','gemini','nim','kimi-nim'])
    p.add_argument('--project',type=Path,default=Path.cwd())
    p.add_argument('--model')
    p.add_argument('--timeout',type=int,default=180)
    p.add_argument('--dry-run',action='store_true')
    a=p.parse_args()
    if not a.project.is_dir(): p.error('Project directory does not exist')
    if not 1 <= a.timeout <= 900: p.error('Timeout must be 1..900 seconds')
    if a.provider=='codex':
        cmd=['codex','exec','--sandbox','read-only','--skip-git-repo-check','-']
        if a.model: cmd[2:2]=['--model',a.model]
    elif a.provider=='gemini':
        cmd=['gemini','--approval-mode','plan','--output-format','text','--prompt','Read the task from stdin. Return findings only; do not modify files or call external write tools.']
        if a.model: cmd+=['--model',a.model]
    else: cmd=None
    model=a.model or ('moonshotai/kimi-k3' if a.provider=='kimi-nim' else 'nvidia/llama-3.3-nemotron-super-49b-v1.5')
    if a.dry_run:
        print(json.dumps({'provider':a.provider,'command':cmd,'model':model if cmd is None else a.model,'project':str(a.project.resolve()),'timeout':a.timeout,'max_input_chars':24000,'max_api_output_tokens':1200,'network_call':False},ensure_ascii=False));return 0
    prompt=sys.stdin.read(24001)
    if not prompt.strip() or len(prompt)>24000: p.error('Provide 1..24000 characters on stdin; send a bounded task, not the whole repository')
    if cmd:
        if not shutil.which(cmd[0]): p.error('CLI not installed: '+cmd[0])
        try: return subprocess.run(cmd,input=prompt,text=True,cwd=a.project,timeout=a.timeout).returncode
        except subprocess.TimeoutExpired: print('Delegation timed out; no automatic retry.',file=sys.stderr);return 124
    key=os.environ.get('NVIDIA_NIM_API_KEY') or os.environ.get('NVIDIA_API_KEY')
    if not key: p.error('Set NVIDIA_NIM_API_KEY in the parent environment; no key is read from disk or logged')
    body={'model':model,'messages':[{'role':'user','content':prompt}],'max_tokens':1200,'stream':False}
    req=urllib.request.Request('https://integrate.api.nvidia.com/v1/chat/completions',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=a.timeout) as response: data=json.load(response)
        print(data['choices'][0]['message'].get('content') or '')
        print(json.dumps({'usage':data.get('usage'),'model':data.get('model'),'cost':'not supplied by endpoint; do not infer zero'},ensure_ascii=False),file=sys.stderr)
        return 0
    except urllib.error.HTTPError as e:
        print('NIM HTTP '+str(e.code)+'; no automatic retry or paid fallback.',file=sys.stderr);return 1
    except (urllib.error.URLError,TimeoutError,KeyError,ValueError):
        print('NIM request failed; no automatic retry or paid fallback.',file=sys.stderr);return 1

if __name__=='__main__': sys.exit(main())
