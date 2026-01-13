import sys
sys.path.append(r"d:\Fastapi")
from app.database import SessionLocal
from app import models, schemas

db = SessionLocal()
recipes = db.query(models.Recipe).all()
print(f"Found {len(recipes)} recipes")

errors = []
for i, r in enumerate(recipes, 1):
    try:
        obj = schemas.RecipeResponse.model_validate(r)
    except Exception as e:
        errors.append((i, r.id, str(e)))

if errors:
    print("Errors during serialization:")
    for e in errors:
        print(e)
else:
    print("All recipes serialized successfully")
