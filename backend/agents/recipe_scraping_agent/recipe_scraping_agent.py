from google.adk.agents import Agent
from pydantic import BaseModel, Field


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
    
class RecipeScrapedOutput(BaseModel):
    title: str = Field(description="The name of the recipe")
    nutrients: Nutrients
    ingredients: list[str] = Field(description="List of ingredients")
    image_url: str = Field(description="Local image filename")
    source_url: str | None = Field(default=None, description="Original URL from where the recipe was scraped")
    total_time: int | None = Field(default=None, description="Total time to prepare recipe in minutes")


# ───  Agent: RecipeScrapingAgent ───────────────────────────────────────────
def create_recipe_scraping_agent(_config, MODEL):
    return Agent(
        name=_config["name"],
        model=MODEL,
        description=_config["description"],
        instruction=_config["instruction"],
        output_schema=RecipeScrapedOutput,
        output_key="scraped_recipe",
    )

