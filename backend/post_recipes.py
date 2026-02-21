import time
from fastapi import APIRouter
from pydantic import BaseModel
from agent import run

router = APIRouter()

class RecipeSelection(BaseModel):
    user_name: str
    recipe_name: str

@router.post("/api/select_recipe")
async def select_recipe(selection: RecipeSelection):

    result = await run(selection.user_name, selection.recipe_name)
    """
    {
        "recipe_name": "Mihir's Special",
        "url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&q=80&w=800"
    }
    """
    return result
