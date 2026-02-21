import time
from fastapi import APIRouter
from pydantic import BaseModel
from agent import run

router = APIRouter()

class RecipeSelection(BaseModel):
    user_name: str
    recipe_name: str

@router.post("/api/select_recipe")
def select_recipe(selection: RecipeSelection):

    recipe_name = run(selection.user_name, selection.recipe_name)
    result = {
        "recipe_name": recipe_name,
        "url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&q=80&w=800"
    }
    return result
