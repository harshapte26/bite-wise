import os
import yaml
from google.adk.agents import Agent
from google.adk.tools import google_search
from pydantic import BaseModel, Field


class RecipeOutput(BaseModel):
    recipe_name: str = Field(description="A catchy, SEO-friendly name for the trending recipe.")

# ───  Agent: RecipeCreatorAgent ───────────────────────────────────────────
def create_recipe_creator_agent(_config, MODEL):
    return Agent(
        name=_config["name"],
        model=MODEL,
        description=_config["description"],
        instruction=_config["instruction"],
        output_schema=RecipeOutput,
        output_key="generated_recipe",
    )
