from fastapi import APIRouter
from pydantic import BaseModel
from agent import run

router = APIRouter()

class RecipeSelection(BaseModel):
    user_name: str
    recipe_name: str

@router.post("/api/select_recipe")
def select_recipe(selection: RecipeSelection):

    result = run(selection.user_name, selection.recipe_name)
    return result
