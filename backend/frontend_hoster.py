from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from get_recipes import router as get_recipes_router
from post_recipes import router as post_recipes_router

app.include_router(get_recipes_router)
app.include_router(post_recipes_router)

@app.get("/api/nutrition_summary")
def get_nutrition_summary(user_name: str = "md"):
    # This would eventually call the NutritionAnalysisAgent.
    # For now, returning mock data that matches the output schema.
    return {
        "summary": "Your current meal plan is rich in protein but slightly low in fiber. Great for muscle building, but consider adding more greens.",
        "total_nutrients": {
            "calories": "2450 kcal",
            "proteinContent": "125 g",
            "carbsContent": "210 g",
            "fatContent": "85 g",
            "fiberContent": "12 g",
            "sodiumContent": "2100 mg"
        },
        "chart_path": "agents/nutrition_analysis/nutrition_chart.png",
        "suggestions": [
            "Add 1 cup of spinach to your breakfast bagel for vitamin K and iron.",
            "Sprinkle 2 tablespoons of chia seeds onto your pizza for a fiber boost.",
            "Swap one rice portion for quinoa to increase your magnesium intake."
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("frontend_hoster:app", host="0.0.0.0", port=8000, reload=True)
