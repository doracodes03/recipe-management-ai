import sys
import os
sys.path.append(r"d:\Fastapi")

from app import ai_agent

print('GEMINI_API_KEY present:', bool(os.getenv('GEMINI_API_KEY')))
print('HF_API_KEY present:', bool(os.getenv('HF_API_KEY')))

prompt = 'Give a one-line friendly test response: Hello from API.'

print('\n--- Testing Gemini (may be None if no key) ---')
try:
    res = ai_agent.generate_with_gemini(prompt)
    print('Gemini result:', repr(res))
except Exception as e:
    print('Gemini exception:', e)

print('\n--- Testing Hugging Face (may be None if no key) ---')
try:
    res2 = ai_agent.generate_with_hf(prompt)
    print('HF result:', repr(res2))
except Exception as e:
    print('HF exception:', e)
