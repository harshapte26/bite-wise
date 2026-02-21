from fastapi import APIRouter

router = APIRouter()

MOCK_RECIPES = [
    {
        "recipe_id": 1,
        "recipe_name": "Marcus Samuelsson Fried Chicken",
        "url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&q=80&w=800"
    },
    {
        "recipe_id": 2,
        "recipe_name": "SriPraPhai Thai Special",
        "url": "https://images.unsplash.com/photo-1559314809-0d155014e29e?auto=format&fit=crop&q=80&w=800"
    },
    {
        "recipe_id": 3,
        "recipe_name": "Hudson Breakfast Bagel",
        "url": "https://images.unsplash.com/photo-1549488344-1f9b8d2bd1f3?auto=format&fit=crop&q=80&w=800"
    },
    {
        "recipe_id": 4,
        "recipe_name": "Royal Greens Salad Bowl",
        "url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&q=80&w=800"
    },
    {
        "recipe_id": 5,
        "recipe_name": "Detroit Brick Pizza",
        "url": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&q=80&w=800"
    },
    {
        "recipe_id": 6,
        "recipe_name": "Mihir's Special",
        "url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&q=80&w=800"
    }
]

@router.get("/api/recipes")
def get_recipes():
    return MOCK_RECIPES
