import os
import yaml
from google.adk.agents import Agent
from pydantic import BaseModel, Field


class RecipeScrapedOutput(BaseModel):
    title: str = Field(description="The title of the recipe.")
    ingredients: list[str] = Field(description="A list of ingredients required for the recipe.")
    instructions: list[str] = Field(description="A list of instructions or steps to prepare the recipe.")


# ─── Load prompt config from YAML ─────────────────────────────────────────────
_PROMPT_FILE = os.path.join(os.path.dirname(__file__), "recipe_scraping_agent_prompt.yaml")

with open(_PROMPT_FILE, "r") as f:
    _config = yaml.safe_load(f)

MODEL = _config.get("model", "gemini-2.0-flash")


# ───  Agent: RecipeScrapingAgent ───────────────────────────────────────────
recipe_scraping_agent = Agent(
    name=_config["name"],
    model=MODEL,
    description=_config["description"],
    instruction=_config["instruction"],
    output_schema=RecipeScrapedOutput,
    output_key="scraped_recipe",
)
