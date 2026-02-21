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
        "summary": "Your plan is slightly high in sodium and low in certain micronutrients. To optimize your health, consider the following targeted adjustments.",
        "total_nutrients": {
            "Calories": "2,450 kcal",
            "Protein": "125 g",
            "Carbs": "210 g",
            "Fat": "85 g",
            "Fiber": "12 g",
            "Sodium": "2,100 mg"
        },
        "chart_path": "agents/nutrition_analysis/nutrition_chart.png",
        "suggestions": [
            "Add spinach or kale to your breakfast bagel to boost Vitamin K and Iron.",
            "Mix in chia seeds or flax seeds with your pizza toppings for extra Fiber.",
            "Incorporate a side of greek yogurt to increase Protein and Probiotics."
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("frontend_hoster:app", host="0.0.0.0", port=8000, reload=True)
