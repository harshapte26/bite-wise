import uvicorn
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from database.db import add_saved_recipe

router = APIRouter()

class RecipeSelection(BaseModel):
    user_name: str
    recipe_name: str

@router.post("/api/select_recipe")
def select_recipe(selection: RecipeSelection):
    success = add_saved_recipe(selection.user_name, selection.recipe_name)
    if success:
        return {"status": "success", "message": f"Recipe {selection.recipe_name} selected and saved."}
    else:
        return {"status": "success", "message": f"Recipe {selection.recipe_name} was already selected or error occurred."}

if __name__ == "__main__":
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router)
    print("Starting standalone post_recipes service on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
