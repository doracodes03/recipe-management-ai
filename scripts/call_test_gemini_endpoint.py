import requests

url = 'http://127.0.0.1:8000/ai/test-gemini'
print('Calling', url)
try:
    r = requests.get(url, timeout=20)
    print('Status:', r.status_code)
    try:
        print('JSON:', r.json())
    except Exception:
        print('Text:', r.text[:1000])
except Exception as e:
    print('Request failed:', repr(e))
