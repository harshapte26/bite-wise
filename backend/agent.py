import yaml
import asyncio
from typing import Dict
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.recipe_creator.recipe_creator import create_recipe_creator_agent
from database.db import add_saved_recipe, get_user

# ── Build agent once at module load ───────────────────────────────────────────
with open("agents/recipe_creator/recipe_creator_prompt.yaml") as f:
    _config = yaml.safe_load(f)

_agent = create_recipe_creator_agent(_config, _config["model"])

# ── Public function ────────────────────────────────────────────────────────────
async def suggest_recipe(existing_recipes: list, nutrition_info: dict) -> str:
    """Run the RecipeCreatorAgent and return a suggested recipe name."""
    nutrition_str = (
        f"{nutrition_info.get('calories', '?')} cal, "
        f"{nutrition_info.get('protein', '?')}g protein, "
        f"{nutrition_info.get('carbs', '?')}g carbs, "
        f"{nutrition_info.get('fat', '?')}g fat"
    )

    sessions = InMemorySessionService()
    await sessions.create_session(
        app_name="bite-wise",
        user_id="system",
        session_id="suggest",
        state={
            "existing_recipes": "\n".join(f"- {r}" for r in existing_recipes),
            "nutrition_info": nutrition_str,
        },
    )

    runner = Runner(agent=_agent, app_name="bite-wise", session_service=sessions)

    async for event in runner.run_async(
        user_id="system",
        session_id="suggest",
        new_message=types.Content(role="user", parts=[types.Part(text="Go.")]),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            return event.content.parts[0].text

    return None


def run(user_name: str, recipe_name: str) -> Dict:
    # 1. Save the selected recipe
    add_saved_recipe(user_name, recipe_name)

    # 2. Load updated user data
    user = get_user(user_name)

    # 3. Ask agent for next suggestion
    recipe_name = asyncio.run(suggest_recipe(
        existing_recipes=user.get("recipe_names", []),
        nutrition_info=user.get("nutrition_info", {}),
    ))
    if recipe_name is None:
        return {
            "status": "error",
            "message": "Failed to get recipe suggestion.",
        }
    # 4. Call for  New Recipe getter & attribute generator: 
    ## Place holder for now & change return object 
    # TODO: @savani 
    return recipe_name