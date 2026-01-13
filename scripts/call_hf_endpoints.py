import requests

print('list-hf-models status:')
try:
    r = requests.get('http://127.0.0.1:8000/ai/list-hf-models?limit=5', timeout=30)
    print(r.status_code)
    print(r.text[:1000])
except Exception as e:
    print('error', e)

print('\ncall test-hf gpt2:')
try:
    r = requests.post('http://127.0.0.1:8000/ai/test-hf', params={'model':'gpt2','prompt':'Hello from test'})
    print(r.status_code)
    print(r.text[:2000])
except Exception as e:
    print('error', e)
