import sys, os
sys.path.append(r"d:\Fastapi")
from app.ai_agent import call_hf_model, list_hf_models

print('HF_API_KEY present:', bool(os.getenv('HF_API_KEY')))
print('\nListing first 5 HF hub models (may be large):')
models = list_hf_models(limit=5)
print('list_hf_models returned type:', type(models))
if models:
    for m in models[:5]:
        print('-', m.get('id') if isinstance(m, dict) else str(m))

print('\nTrying call_hf_model with gpt2:')
res = call_hf_model('gpt2', 'Write a friendly one-line greeting for a cooking assistant.')
print('Result:', res)

print('\nTrying call_hf_model with distilbart-cnn-12-6:')
res2 = call_hf_model('sshleifer/distilbart-cnn-12-6', 'Summarize: This is a test.')
print('Result2:', res2)
