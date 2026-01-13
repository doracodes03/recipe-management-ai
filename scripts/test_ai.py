import requests

BASE = "http://127.0.0.1:8000"

endpoints = [
    ("/ai/suggest-recipe", {"query": "vegan salad"}),
    ("/ai/make-healthier", {"recipe_id": 1}),
    ("/ai/explain-steps", {"recipe_id": 1}),
]

for path, params in endpoints:
    url = BASE + path
    try:
        r = requests.post(url, params=params, timeout=10)
        print("REQUEST:", url, params)
        print("STATUS:", r.status_code)
        try:
            print("JSON:", r.json())
        except Exception:
            print("TEXT:", r.text[:1000])
    except Exception as e:
        print("ERROR calling", url, e)
    print("---")
