from pydantic import BaseModel, validator


class RecipeCreate(BaseModel):
    name: str
    ingredients: str
    instructions: str
    cuisine: str
    prep_time: int
    diet_type: str

    @validator("diet_type")
    def normalize_diet(cls, v: str):
        if v is None:
            return v
        v = v.lower().strip()

        if v in ("vegetarian",):
            return "veg"
        if v in ("nonveg", "non veg"):
            return "non-veg"

        allowed = ["veg", "non-veg", "vegan"]
        if v not in allowed:
            raise ValueError("diet_type must be veg, non-veg, or vegan")
        return v


class RecipeResponse(RecipeCreate):
    id: int
    model_config = {"from_attributes": True}



class AIQuery(BaseModel):
    query: str
