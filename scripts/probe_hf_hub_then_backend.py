import os, sys, time
sys.path.append(r"d:\Fastapi")
from app.ai_agent import list_hf_models
import requests

BACKEND_TEST_URL = 'http://127.0.0.1:8000/ai/test-hf'

print('Listing models from HF Hub (using local helper)...')
models = list_hf_models(limit=500)
if not models:
    print('No models returned from Hub list or request failed.')
    raise SystemExit(1)

# models is a list of dicts
candidates = []
for m in models:
    if isinstance(m, dict):
        mid = m.get('id')
    else:
        mid = str(m)
    if not mid:
        continue
    lid = mid.lower()
    # skip obvious non-text models
    if any(x in lid for x in ['image', 'speech', 'whisper', 'clip', 'segmentation']):
        continue
    candidates.append(mid)

print(f'Total candidates after filtering: {len(candidates)}')

prompt = 'Write a friendly one-line cooking tip.'

for i, model in enumerate(candidates[:300], start=1):
    print(f'[{i}] Testing model via backend: {model}')
    try:
        r = requests.post(BACKEND_TEST_URL, json={'model': model, 'prompt': prompt}, timeout=30)
    except Exception as e:
        print('  Request failed:', e)
        time.sleep(0.2)
        continue

    if r.status_code == 200:
        try:
            data = r.json()
        except Exception:
            print('  Non-JSON 200 response; likely success. Saving model:', model)
            with open('d:/Fastapi/scripts/working_hf_model_backend.txt','w',encoding='utf-8') as f:
                f.write(model)
            break
        if data.get('result'):
            print('  SUCCESS:', model)
            print('  Sample:', str(data['result'])[:400])
            with open('d:/Fastapi/scripts/working_hf_model_backend.txt','w',encoding='utf-8') as f:
                f.write(model)
            break
        else:
            print('  200 but empty result field.')
    else:
        print('  Status', r.status_code)
    time.sleep(0.25)
else:
    print('No working model found in probed candidates.')

print('Done.')
