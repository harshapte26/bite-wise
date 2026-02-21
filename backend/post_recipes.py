from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RecipeSelection(BaseModel):
    user_id: str
    recipe_id: int

@router.post("/api/select_recipe")
def select_recipe(selection: RecipeSelection):
    print(f"User {selection.user_id} selected recipe {selection.recipe_id}")
    return {"status": "success", "message": f"Recipe {selection.recipe_id} selected"}
