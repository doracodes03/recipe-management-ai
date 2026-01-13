import os, sys
sys.path.append(r"d:\Fastapi")
from app.ai_agent import list_gemini_models, generate_with_gemini

print('GEMINI_API_KEY present:', bool(os.getenv('GEMINI_API_KEY')))
print('GEMINI_BASE:', os.getenv('GEMINI_BASE'))
print('GEMINI_MODEL:', os.getenv('GEMINI_MODEL'))

print('\nListing Gemini models...')
try:
    lm = list_gemini_models()
    print('List models returned type:', type(lm))
    if isinstance(lm, dict):
        print('Models keys:', list(lm.keys())[:5])
    else:
        print(lm)
except Exception as e:
    print('List models error:', repr(e))

print('\nAttempting a simple generate...')
prompt = 'Write a friendly, one-line cooking tip.'
try:
    out = generate_with_gemini(prompt)
    print('Generate output:', out)
except Exception as e:
    print('Generate error:', repr(e))
