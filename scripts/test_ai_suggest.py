import requests, json

url = 'http://127.0.0.1:8000/ai/suggest-recipe'
query = 'ultraviolet kumquat nebula'  # intentionally unique to avoid DB matches

print('POST', url)
try:
    # `ai_suggest_recipe` expects `query` as a query parameter (not JSON body)
    r = requests.post(url, params={'query': query}, timeout=60)
    print('Status:', r.status_code)
    try:
        data = r.json()
    except Exception:
        print('Non-JSON response:', r.text[:200])
        raise
    print('\nFull response JSON:')
    print(json.dumps(data, indent=2, ensure_ascii=False))

    src = data.get('source')
    if src == 'ai_generated':
        print('\nResult: AI-generated response (no DB fallback).')
        if 'recipe' in data:
            print('\nAI recipe preview:')
            print(data['recipe'][:1000])
    elif src == 'database':
        print('\nResult: Database fallback — recipes found in DB for that query.')
        if 'recipes' in data:
            print('Number of recipes returned:', len(data['recipes']))
    else:
        print('\nResult: Unknown response format; check server logs.')

except Exception as e:
    print('Request failed:', repr(e))
