from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from .database import SessionLocal, engine
from . import models, schemas, crud
from .crud import extract_diet_from_query
from .ai_agent import generate_recipe

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe Management API")

# ---------------- DB DEPENDENCY ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- RECIPE CRUD ----------------

@app.post("/recipes/add", response_model=schemas.RecipeResponse)
def add_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)

@app.get("/recipes/all", response_model=list[schemas.RecipeResponse])
def get_recipes(db: Session = Depends(get_db)):
    return crud.get_all_recipes(db)

@app.put("/recipes/update/{recipe_id}", response_model=schemas.RecipeResponse)
def update_recipe(recipe_id: int, recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    updated = crud.update_recipe(db, recipe_id, recipe)
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated

@app.delete("/recipes/delete/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_recipe(db, recipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}

# ---------------- SEARCH & FILTER ----------------

@app.get("/recipes/search", response_model=list[schemas.RecipeResponse])
def search_recipes(
    query: Optional[str] = None,
    cuisine: Optional[str] = None,
    diet_type: Optional[str] = None,
    max_prep_time: Optional[int] = None,
    db: Session = Depends(get_db)
):
    inferred_diet = extract_diet_from_query(query) if query else None
    final_diet = diet_type or inferred_diet

    return crud.search_recipes(
        db=db,
        ingredient=query,
        cuisine=cuisine,
        diet_type=final_diet,
        max_prep_time=max_prep_time
    )

# ---------------- AI FEATURES ----------------

@app.post("/ai/suggest-recipe")
def ai_suggest_recipe(
    payload: schemas.AIQuery,
    db: Session = Depends(get_db)
):
    query = payload.query

    # 1️ Search database first
    recipes = crud.search_recipes(db, ingredient=query)

    if recipes:
        return {
            "source": "database",
            "recipes": recipes
        }

    # 2️ Build prompt
    prompt = f"""
    You are a cooking assistant.

    Create a healthy recipe using: {query}

    Return the response in this format:
    - Recipe Name
    - Ingredients
    - Steps
    - Cuisine
    - Preparation Time
    """

    ai_response = generate_recipe(prompt)

    return {
        "source": "ai_generated",
        "recipe": ai_response
    }


@app.post("/ai/make-healthier")
def ai_make_healthier(
    recipe_id: Optional[int] = None,
    recipe_text: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if recipe_id:
        recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        source = f"{recipe.name}. Ingredients: {recipe.ingredients}. Instructions: {recipe.instructions}"
    elif recipe_text:
        source = recipe_text
    else:
        raise HTTPException(status_code=400, detail="Provide recipe_id or recipe_text")

    prompt = f"Make this recipe healthier:\n{source}"
    return {"result": generate_recipe(prompt)}

@app.post("/ai/explain-steps")
def ai_explain_steps(
    recipe_id: Optional[int] = None,
    recipe_text: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if recipe_id:
        recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        source = f"{recipe.name}. Ingredients: {recipe.ingredients}. Instructions: {recipe.instructions}"
    elif recipe_text:
        source = recipe_text
    else:
        raise HTTPException(status_code=400, detail="Provide recipe_id or recipe_text")

    prompt = f"Explain this recipe step-by-step for beginners:\n{source}"
    return {"result": generate_recipe(prompt)}
