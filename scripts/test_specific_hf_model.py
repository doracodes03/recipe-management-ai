import os, sys, time
sys.path.append(r"d:\Fastapi")
from app.ai_agent import call_hf_model, list_hf_models

models_to_test = [
    "google/gemma-2-2b",
    "stabilityai/stable-code-3b",
    "HuggingFaceTB/SmolLM3-3B",
    "meta-llama/Llama-3.2-1B",
    "mistralai/Mistral-7B-v0.1"
]

prompt = "Write a friendly one-line cooking tip."

print('HF_API_KEY present:', bool(os.getenv('HF_API_KEY')))
print('Testing models:')
for m in models_to_test:
    print('\n---')
    print('Model:', m)
    try:
        out = call_hf_model(m, prompt)
    except Exception as e:
        print('Exception:', repr(e))
        out = None
    if out:
        print('SUCCESS: model responded. Sample:', out[:500])
    else:
        print('NO RESPONSE / 404 or other error')
    time.sleep(0.5)

print('\nDone.')
