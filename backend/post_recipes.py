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

    # result = run(selection.user_name, selection.recipe_name)
    result = {
        "recipe_name": "Mihir's Special",
        "url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&q=80&w=800"
    }
    time.sleep(3)
    return result
