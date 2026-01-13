import os, sys, time
sys.path.append(r"d:\Fastapi")
from app.ai_agent import list_hf_models, call_hf_model

API_KEY = os.getenv('HF_API_KEY')
if not API_KEY:
    print('HF_API_KEY not set in environment. Aborting.')
    raise SystemExit(1)

print('Fetching model list...')
models = list_hf_models(limit=50)
if not models:
    print('No models returned from list_hf_models')
    raise SystemExit(1)

# Filter likely text models by skipping obvious image/audio-only models
candidates = []
for m in models:
    if isinstance(m, dict):
        mid = m.get('id','')
    else:
        mid = str(m)
    lid = mid.lower()
    if any(skip in lid for skip in ['-image', 'image', 'speech', 'audio', 'wav', 'whisper', 'tts', 'voice', 'clip', 'segmentation', 'detect']):
        continue
    candidates.append(mid)

print(f'Probing up to {min(20,len(candidates))} candidate models...')
prompt = 'Write a friendly one-line cooking tip.'

for i, model in enumerate(candidates[:20], start=1):
    print(f'[{i}] Trying model: {model}')
    try:
        out = call_hf_model(model, prompt)
    except Exception as e:
        print('  Exception calling model:', repr(e))
        out = None
    if out:
        print('\nSUCCESS: model responded ->', model)
        print('Response:', out)
        with open('d:/Fastapi/scripts/working_hf_model.txt', 'w', encoding='utf-8') as f:
            f.write(model)
        break
    else:
        print('  No response or model not available (404/busy).')
        time.sleep(0.5)
else:
    print('\nNo working model found in the probed candidates.')
    print('You can run the script again or call /ai/list-hf-models for a broader list.')
