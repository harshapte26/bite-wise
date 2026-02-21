import os
import yaml
from google.adk.agents import Agent
from google.adk.tools import google_search
from pydantic import BaseModel, Field


class RecipeOutput(BaseModel):
    recipe_name: str = Field(description="A catchy, SEO-friendly name for the trending recipe.")

# ─── Load prompt config from YAML ─────────────────────────────────────────────
_PROMPT_FILE = os.path.join(os.path.dirname(__file__), "recipe_creator_prompt.yaml")

with open(_PROMPT_FILE, "r") as f:
    _config = yaml.safe_load(f)

MODEL = _config.get("model", "gemini-2.0-flash")


# ───  Agent: RecipeCreatorAgent ───────────────────────────────────────────
# Receives trend results from TrendSearcherAgent via session state,
# then produces a validated, structured recipe JSON.
recipe_creator_agent = Agent(
    name=_config["name"],
    model=MODEL,
    description=_config["description"],
    instruction=_config["instruction"],
    output_schema=RecipeOutput,
    output_key="generated_recipe",
)
