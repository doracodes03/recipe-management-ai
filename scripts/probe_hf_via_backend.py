import requests, time, json

BASE = "http://127.0.0.1:8000"
LIST_URL = f"{BASE}/ai/list-hf-models"
TEST_URL = f"{BASE}/ai/test-hf"

print('Fetching HF models from backend...')
resp = requests.get(LIST_URL, params={'limit': 200}, timeout=30)
if resp.status_code != 200:
    print('Failed to fetch list:', resp.status_code, resp.text[:500])
    raise SystemExit(1)

models = resp.json()
if isinstance(models, dict):
    # earlier list_hf_models returns a list; handle dict wrapping
    if 'models' in models:
        models_list = models['models']
    else:
        # could be list directly
        models_list = models
else:
    models_list = models

print('Total models returned:', len(models_list))

prompt = 'Write a friendly one-line cooking tip.'

for i, m in enumerate(models_list[:200], start=1):
    # m may be dict with 'id' or a string
    if isinstance(m, dict):
        mid = m.get('id') or m.get('modelId') or m.get('model')
    else:
        mid = str(m)
    if not mid:
        continue
    print(f"[{i}] Testing: {mid}")
    try:
        r = requests.post(TEST_URL, json={'model': mid, 'prompt': prompt}, timeout=30)
    except Exception as e:
        print('  Request error:', e)
        time.sleep(0.2)
        continue
    if r.status_code == 200:
        try:
            data = r.json()
        except Exception:
            print('  Non-JSON success response')
            print(r.text[:1000])
            with open('d:/Fastapi/scripts/working_hf_model_backend.txt','w',encoding='utf-8') as f:
                f.write(mid)
            print('Saved working model:', mid)
            break
        # check if result exists
        if 'result' in data and data['result']:
            print('  SUCCESS:', mid)
            print('  Sample:', str(data['result'])[:500])
            with open('d:/Fastapi/scripts/working_hf_model_backend.txt','w',encoding='utf-8') as f:
                f.write(mid)
            break
        else:
            print('  No result in response or model returned empty. Status:', r.status_code)
    else:
        print('  Status', r.status_code, 'Response:', r.text[:500])
    time.sleep(0.3)
else:
    print('No working model found in the first 200 models.')

print('Done.')
