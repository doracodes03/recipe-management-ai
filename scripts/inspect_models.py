import sys
sys.path.append(r"d:\Fastapi")
from app import schemas, models
from app.database import SessionLocal

print('RecipeResponse attrs:', [a for a in dir(schemas.RecipeResponse) if not a.startswith('_')])
print('has from_orm:', hasattr(schemas.RecipeResponse, 'from_orm'))
print('has model_validate:', hasattr(schemas.RecipeResponse, 'model_validate'))

# attempt to serialize first recipe
db = SessionLocal()
recipe = db.query(models.Recipe).first()
print('sample recipe:', recipe)

try:
    # try from_orm if available
    if hasattr(schemas.RecipeResponse, 'from_orm'):
        obj = schemas.RecipeResponse.from_orm(recipe)
        print('from_orm ok:', obj)
    elif hasattr(schemas.RecipeResponse, 'model_validate'):
        obj = schemas.RecipeResponse.model_validate(recipe)
        print('model_validate ok:', obj)
    else:
        print('no compatible pydantic create method')
except Exception as e:
    import traceback
    traceback.print_exc()
    print('error:', e)
