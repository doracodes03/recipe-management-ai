from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_
import re
from . import models, schemas
from typing import Optional


def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_all_recipes(db: Session):
    return db.query(models.Recipe).all()

def update_recipe(db: Session, recipe_id: int, recipe: schemas.RecipeCreate):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        return None

    for key, value in recipe.dict().items():
        setattr(db_recipe, key, value)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        return None

    db.delete(db_recipe)
    db.commit()
    return db_recipe


def search_recipes(
    db,
    ingredient: Optional[str] = None,
    cuisine: Optional[str] = None,
    diet_type: Optional[str] = None,
    max_prep_time: Optional[int] = None
):
    query = db.query(models.Recipe)

    # If a free-text query was provided, search across name, ingredients and instructions.
    # Tokenize the query and match any token (OR) so entering any word from
    # "Mediterranean Quinoa Salad" will match the recipe.
    if ingredient:
        tokens = [t for t in re.findall(r"\w+", ingredient) if t]
        if tokens:
            token_clauses = []
            for t in tokens:
                pattern = f"%{t}%"
                token_clauses.append(models.Recipe.name.ilike(pattern))
                token_clauses.append(models.Recipe.ingredients.ilike(pattern))
                token_clauses.append(models.Recipe.instructions.ilike(pattern))

            # match if any token appears in any of the fields
            query = query.filter(or_(*token_clauses))

    if cuisine:
        query = query.filter(models.Recipe.cuisine.ilike(f"%{cuisine}%"))

    # Use case-insensitive exact match for normalized diet types to avoid
    # matching 'veg' inside 'non-veg'. We compare lower(diet_type) == diet_type
    if diet_type:
        query = query.filter(func.lower(models.Recipe.diet_type) == diet_type.lower())

    if max_prep_time:
        query = query.filter(models.Recipe.prep_time <= max_prep_time)

    return query.all()


def extract_diet_from_query(query: str) -> Optional[str]:
    if not query:
        return None

    q = query.lower()

    if "vegan" in q:
        return "vegan"
    if "non veg" in q or "non-veg" in q or "nonveg" in q:
        return "non-veg"
    # check ' veg ' or startswith/endswith to avoid matching 'non-veg'
    if " veg " in f" {q} " or q.strip().endswith(" veg") or q.strip().startswith("veg "):
        return "veg"

    return None
