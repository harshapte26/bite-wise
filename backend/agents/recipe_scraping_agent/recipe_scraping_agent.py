import os
import yaml
from dotenv import load_dotenv
from google.adk.agents import Agent
from pydantic import BaseModel, Field

# Load environment variables from .env
load_dotenv()


class Nutrients(BaseModel):
    calories: str | None = None
    carbohydrateContent: str | None = None
    cholesterolContent: str | None = None
    fiberContent: str | None = None
    proteinContent: str | None = None
    saturatedFatContent: str | None = None
    sodiumContent: str | None = None
    sugarContent: str | None = None
    fatContent: str | None = None
    unsaturatedFatContent: str | None = None


class Metadata(BaseModel):
    source_url: str | None = Field(default=None, description="Original URL from where the recipe was scraped")
    total_time: int | None = Field(default=None, description="Total time to prepare recipe in minutes")
    yields: str | None = Field(default=None, description="Number of servings")


class RecipeScrapedOutput(BaseModel):
    title: str = Field(description="The name of the recipe")
    nutrients: Nutrients
    ingredients: list[str] = Field(description="List of ingredients")
    directions: str = Field(description="Instructions for preparing the recipe")
    image_name: str = Field(description="Local image filename")
    cloud_image_url: str = Field(description="URL of the image hosted in the cloud")
    metadata: Metadata


# ─── Load prompt config from YAML ─────────────────────────────────────────────
_PROMPT_FILE = os.path.join(os.path.dirname(__file__), "recipe_scraping_agent_prompt.yaml")

with open(_PROMPT_FILE, "r") as f:
    _config = yaml.safe_load(f)

MODEL = _config.get("model", "gemini-2.5-flash")


# ───  Agent: RecipeScrapingAgent ───────────────────────────────────────────
recipe_scraping_agent = Agent(
    name=_config["name"],
    model=MODEL,
    description=_config["description"],
    instruction=_config["instruction"],
    output_schema=RecipeScrapedOutput,
    output_key="scraped_recipe",
)

# ─── Run the agent ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    from pprint import pprint
    from google.adk import Runner
    from google.adk.sessions import InMemorySessionService

    # Initialize the session service
    session_service = InMemorySessionService()
    
    # Create a runner for our agent
    runner = Runner(
        app_name="recipe_scraper_app",
        agent=recipe_scraping_agent,
        session_service=session_service
    )
    
    print("Running agent...")
    result = runner.run("scrape the recipe details for the following text or URL: https://www.allrecipes.com/recipe/11973/spaghetti-carbonara-ii/")
    
    print("Agent Output:")
    pprint(result)