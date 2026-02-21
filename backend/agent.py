import yaml
import asyncio
from typing import Dict
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.recipe_creator.recipe_creator import create_recipe_creator_agent
from agents.recipe_scraping_agent.recipe_scraping_agent import create_recipe_scraping_agent, RecipeScrapedOutput
from database.db import add_saved_recipe, get_user
from dotenv import load_dotenv
import json
import uuid

load_dotenv()

# ── Build agents once at module load ───────────────────────────────────────────
with open("agents/recipe_creator/recipe_creator_prompt.yaml") as f:
    _creator_config = yaml.safe_load(f)

_creator_agent = create_recipe_creator_agent(_creator_config, _creator_config.get("model", "gemini-2.5-flash"))

with open("agents/recipe_scraping_agent/recipe_scraping_agent_prompt.yaml") as f:
    _scraper_config = yaml.safe_load(f)

_scraper_agent = create_recipe_scraping_agent(_scraper_config, _scraper_config.get("model", "gemini-2.5-flash"))


# ── Public functions ────────────────────────────────────────────────────────────
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

    runner = Runner(agent=_creator_agent, app_name="bite-wise", session_service=sessions)

    async for event in runner.run_async(
        user_id="system",
        session_id="suggest",
        new_message=types.Content(role="user", parts=[types.Part(text="Go.")]),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            return event.content.parts[0].text

    return None

async def scrape_recipe(recipe_name: str) -> dict:
    """Run the RecipeScrapingAgent and return the scraped recipe data."""
    sessions = InMemorySessionService()
    session_id = f"scrape_{uuid.uuid4().hex}"
    
    # Get the raw schema as a string to pass into the template
    try:
        schema_json = RecipeScrapedOutput.model_json_schema()
    except AttributeError:
        # Fallback for v1/v2 pydantic differences
        schema_json = RecipeScrapedOutput.schema_json()

    await sessions.create_session(
        app_name="bite-wise",
        user_id="system",
        session_id=session_id,
        state={
            "recipe_name": recipe_name,
            "recipe_schema": json.dumps(schema_json),
        },
    )

    runner = Runner(agent=_scraper_agent, app_name="bite-wise", session_service=sessions)

    async for event in runner.run_async(
        user_id="system",
        session_id=session_id,
        new_message=types.Content(role="user", parts=[types.Part(text="Go.")]),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            # If the output is wrapped in markdown json block, strip it
            if text.startswith("```json"):
                text = text.split("```json", 1)[1].rsplit("```", 1)[0].strip()
            elif text.startswith("```"):
                text = text.split("```", 1)[1].rsplit("```", 1)[0].strip()
                
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON scraped data: {e}")
                return {"error": "Failed to parse JSON", "raw_text": text}

    return None

async def run(user_name: str, recipe_name: str) -> Dict:
    # 1. Save the selected recipe
    add_saved_recipe(user_name, recipe_name)

    # 2. Load updated user data
    user = get_user(user_name)

    # 3. Ask agent for next suggestion
    recipe_name_obj = await suggest_recipe(
        existing_recipes=user.get("recipe_names", []),
        nutrition_info=user.get("nutrition_info", {}),
    )
    # Load as json object 
    try:
        recipe_name_obj = json.loads(recipe_name_obj)
        suggested_recipe_name = recipe_name_obj.get("recipe_name")
    except Exception:
        suggested_recipe_name = None
        
    if suggested_recipe_name is None:
        return {
            "status": "error",
            "message": "Failed to get recipe suggestion.",
        }
        
    # 4. Call for New Recipe getter & attribute generator
    scraped_recipe_details = await scrape_recipe(suggested_recipe_name)
    print(scraped_recipe_details)
    print("------")
    # 5. Save the scraped recipe details
    add_saved_recipe(user_name, scraped_recipe_details)
    
    # 
    result = {
    "recipe_name": suggested_recipe_name,
    "url": scraped_recipe_details.get("image_url") ,
    "status": "success",
    "nutrients": scraped_recipe_details.get("nutrients"),
    "ingredients": scraped_recipe_details.get("ingredients"),  
}
    return result

if __name__ == "__main__":
    # Run the function locally
    print(asyncio.run(run("md", "Spaghetti Carbonara")))