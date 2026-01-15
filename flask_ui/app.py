from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

# Configure the FastAPI backend base URL
FASTAPI_BASE = os.environ.get("FASTAPI_BASE", "http://127.0.0.1:8000")


def fetch_recipes(params=None):
    try:
        resp = requests.get(f"{FASTAPI_BASE}/recipes/search", params=params or {})
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return []


@app.route("/", methods=["GET"])
def index():
    # Read search/filter params from querystring
    query = request.args.get("query")
    diet_type = request.args.get("diet_type")
    cuisine = request.args.get("cuisine")
    max_prep_time = request.args.get("max_prep_time")

    params = {}
    if query:
        params["query"] = query
    if diet_type:
        params["diet_type"] = diet_type
    if cuisine:
        params["cuisine"] = cuisine
    if max_prep_time:
        params["max_prep_time"] = max_prep_time

    recipes = fetch_recipes(params)

    return render_template("index.html", recipes=recipes, query=query, diet_type=diet_type, cuisine=cuisine, max_prep_time=max_prep_time)


@app.route("/add", methods=["POST"])
def add_recipe():
    data = {
        "name": request.form.get("name"),
        "ingredients": request.form.get("ingredients"),
        "instructions": request.form.get("instructions"),
        "cuisine": request.form.get("cuisine"),
        "prep_time": int(request.form.get("prep_time") or 0),
        "diet_type": request.form.get("diet_type") or "veg"
    }

    try:
        resp = requests.post(f"{FASTAPI_BASE}/recipes/add", json=data)
        resp.raise_for_status()
        flash("Recipe added successfully", "success")
    except requests.HTTPError as e:
        flash(f"Failed to add recipe: {e}", "danger")

    return redirect(url_for("index"))


@app.route("/ai/suggest", methods=["POST"])
def ai_suggest():
    q = request.form.get("ai_query")
    if not q:
        flash("Please enter a query for the AI assistant", "warning")
        return redirect(url_for("index"))

    try:
        resp = requests.post(f"{FASTAPI_BASE}/ai/suggest-recipe", params={"query": q})
        resp.raise_for_status()
        data = resp.json()
        ai_text = data.get("recipe") or data.get("recipes") or data
    except Exception as e:
        ai_text = f"AI request failed: {e}"

    # Render index with ai_result shown in a banner
    recipes = fetch_recipes()
    return render_template("index.html", recipes=recipes, ai_result=ai_text)


@app.route("/ai/make-healthier", methods=["POST"])
def ai_make_healthier():
    recipe_id = request.form.get("ai_recipe_id")
    payload = {}
    if recipe_id:
        payload["recipe_id"] = int(recipe_id)

    try:
        resp = requests.post(f"{FASTAPI_BASE}/ai/make-healthier", params=payload)
        resp.raise_for_status()
        data = resp.json()
        ai_text = data.get("result")
    except Exception as e:
        ai_text = f"AI request failed: {e}"

    recipes = fetch_recipes()
    return render_template("index.html", recipes=recipes, ai_result=ai_text)


@app.route("/ai/explain", methods=["POST"])
def ai_explain():
    recipe_id = request.form.get("ai_recipe_id")
    payload = {}
    if recipe_id:
        payload["recipe_id"] = int(recipe_id)

    try:
        resp = requests.post(f"{FASTAPI_BASE}/ai/explain-steps", params=payload)
        resp.raise_for_status()
        data = resp.json()
        ai_text = data.get("result")
    except Exception as e:
        ai_text = f"AI request failed: {e}"

    recipes = fetch_recipes()
    return render_template("index.html", recipes=recipes, ai_result=ai_text)


@app.route("/delete/<int:recipe_id>")
def delete_recipe(recipe_id: int):
    try:
        resp = requests.delete(f"{FASTAPI_BASE}/recipes/delete/{recipe_id}")
        if resp.status_code == 200:
            flash("Recipe deleted", "success")
        else:
            flash(f"Delete failed: {resp.status_code}", "danger")
    except Exception as e:
        flash(f"Delete error: {e}", "danger")

    return redirect(url_for("index"))


@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id: int):
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "ingredients": request.form.get("ingredients"),
            "instructions": request.form.get("instructions"),
            "cuisine": request.form.get("cuisine"),
            "prep_time": int(request.form.get("prep_time") or 0),
            "diet_type": request.form.get("diet_type") or "veg"
        }

        try:
            resp = requests.put(f"{FASTAPI_BASE}/recipes/update/{recipe_id}", json=data)
            if resp.status_code == 200:
                flash("Recipe updated", "success")
            else:
                flash(f"Update failed: {resp.status_code}", "danger")
        except Exception as e:
            flash(f"Update error: {e}", "danger")

        return redirect(url_for("index"))

    # GET -> fetch recipe data by pulling all and finding the id
    try:
        resp = requests.get(f"{FASTAPI_BASE}/recipes/all")
        resp.raise_for_status()
        all_recipes = resp.json()
        recipe = next((r for r in all_recipes if r.get("id") == recipe_id), None)
    except Exception:
        recipe = None

    if not recipe:
        flash("Recipe not found", "danger")
        return redirect(url_for("index"))

    return render_template("edit.html", recipe=recipe)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



