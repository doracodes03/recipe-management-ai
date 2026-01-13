# Recipe Explorer — FastAPI + Flask UI 🍽️

A small recipe manager with search, filters, a lightweight Flask UI, and AI-assisted recipe suggestions. This README explains features, configuration, step-by-step installation, and troubleshooting with helpful emojis. ✅

---

## What this project provides

- Backend: FastAPI + SQLAlchemy (SQLite) for recipe CRUD and search. 🔁
- Frontend: Simple Flask-rendered UI at `flask_ui/` to search/add/edit/delete recipes. 🎛️
- AI Assistant: Hugging Face router integration to `HF_MODEL` for generation (suggest recipe, make healthier, explain steps). 🤖
- Tokenized multi-field search and diet inference (veg / non-veg / vegan). 🔍
- Small list of scripts in `scripts/` for testing HF/Gemini and probing available models. 🧪

> Note: Gemini support was previously present but the current backend is configured to use Hugging Face only.

---

## Quick Start — Windows (step-by-step) 🪄

1) Clone / open this repository in your workspace (you already have it). 📂

2) Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# or for cmd.exe:
# .\.venv\Scripts\activate.bat
```

3) Install dependencies:

```powershell
pip install -r requirements.txt
```

4) Create a `.env` file in the project root (there is an example in the repository). Required variables:

```
HF_API_KEY=hf_xxx
HF_MODEL=gpt2                 # change to the HF model you can access
HF_API_URL=https://router.huggingface.co/models
# GEMINI entries removed from the agent — no Gemini config required
```

5) Start the FastAPI backend (development mode):

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

6) In another terminal, start the Flask UI (views that call the backend):

```powershell
python flask_ui/app.py
```

Open the UI: http://127.0.0.1:5000 ✅

---

## Endpoints & scripts

- API routes (FastAPI):
  - `POST /recipes/add` — Add a recipe
  - `GET /recipes/all` — List recipes
  - `GET /recipes/search` — Search recipes (query, cuisine, diet_type, max_prep_time)
  - `PUT /recipes/update/{id}` — Update recipe
  - `DELETE /recipes/delete/{id}` — Delete recipe
  - `POST /ai/suggest-recipe` — Suggest recipe (query param `query`) — checks DB then AI
  - `POST /ai/make-healthier` — Make recipe healthier (body: `recipe_id` or `recipe_text`)
  - `POST /ai/explain-steps` — Explain steps (body: `recipe_id` or `recipe_text`)
  - `GET /ai/list-hf-models` — List models from Hugging Face Hub (helpful to find usable models)
  - `POST /ai/test-hf` — Test a specific HF model via router: JSON `{"model":"<id>","prompt":"..."}`

- Useful scripts (in `scripts/`):
  - `test_gemini_direct.py` — legacy/test Gemini (may not be used)
  - `test_call_hf_direct.py` — call `call_hf_model` locally
  - `find_working_hf_model.py` — probe HF hub locally
  - `test_ai_suggest.py` — test `ai/suggest-recipe` endpoint
  - `probe_hf_hub_then_backend.py` — list Hub models and test each via backend `/ai/test-hf`

---

## UI Additions & Images 🖼️

The Flask UI (`flask_ui/templates/index.html`) maps a set of common recipe names to image URLs (provided in the templates). If a recipe doesn't match a known name, a small placeholder image is shown.

If you'd like persistent recipe images stored per recipe, I can:
- Add an `image_url` field to the `Recipe` model and the forms (recommended), or
- Allow uploading images to a storage bucket and save the link.

Tell me which option you prefer and I will implement it.

---

## AI Configuration & Troubleshooting 🤖

- The current code uses the Hugging Face Router API. Ensure your `HF_API_KEY` is set in `.env` and `HF_MODEL` is set to a model you *have access to* on Hugging Face.

- Common problems & solutions:
  - 404 from HF router: your token doesn't have access to the model or model name is incorrect. Use `GET /ai/list-hf-models` or `scripts/find_working_hf_model.py` to discover available models.
  - 429 from Gemini (if used earlier): quota or billing issue — enable billing or use a different model.
  - Backend returns fallback text: the AI call failed (check backend logs or use the `scripts/` helpers to inspect raw responses).

---

## How to test AI flows locally 🧪

- Suggest recipe (curl):

```bash
# query as query param
curl -X POST "http://127.0.0.1:8000/ai/suggest-recipe?query=healthy+quinoa+dinner"
```

- Test a specific HF model (backend will call the router):

```bash
curl -X POST http://127.0.0.1:8000/ai/test-hf -H "Content-Type: application/json" -d '{"model":"gpt2","prompt":"Write a friendly one-line cooking tip."}'
```

- Use the Flask UI for a friendly web UX: http://127.0.0.1:5000

---

## Development notes & safety 🔧

- Pydantic v2: models use `model_config = {"from_attributes": True}` where needed for SQLAlchemy ORM conversion.
- Diet normalization validator: `RecipeCreate` normalizes synonyms (e.g., `vegetarian` → `veg`, `nonveg` → `non-veg`) so legacy DB rows don't fail validation.
- AI orchestration: the backend uses HF as the primary generator and falls back to a safe textual fallback if no provider responds.

---

## Deploying / Production hints 🚀

- Use a production-ready ASGI server (e.g., Gunicorn + Uvicorn workers) for FastAPI and a WSGI server (or static hosting) for the UI if separated.
- Store secrets in a secure secrets manager (Azure Key Vault, AWS Secrets Manager, or GCP Secret Manager) — don't keep production keys in `.env` in source control.
- Rate-limit AI calls and add caching if you expect high traffic.

---

## Troubleshooting checklist 🔎

- If UI shows fallback AI text:
  1. Confirm FastAPI is running (http://127.0.0.1:8000).
  2. Run `python scripts/test_call_hf_direct.py` to inspect HF router behavior.
  3. Try `GET /ai/list-hf-models` to see which models are available to your token.

- If HF calls return 404:
  - Confirm `HF_API_KEY` has model access and the `HF_MODEL` string is exactly correct (case-sensitive). Use Hub model id (owner/name).

---

## Next steps I can take (choose one) 🛠️

- Add `image_url` to the recipe model and UI so images persist per recipe.
- Wire an upload route to accept images and store them in a storage bucket.
- Harden AI error reporting: return raw provider error in a debug-only endpoint.

---

If you'd like, I can now: (pick one)
- Add `image_url` support and update the DB/UI.
- Implement a debug endpoint that returns raw HF router responses for a model.
- Walk you through setting an HF model that your token can access.

Happy to continue — tell me which next step you want. 😊
