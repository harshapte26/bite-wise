import os
import json
import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Dict, List

# ─── Schema Definition ────────────────────────────────────────────────────────
class NutritionOutput(BaseModel):
    summary: str = Field(description="A brief summary of the aggregated nutritional information.")
    total_nutrients: Dict[str, str] = Field(description="The total aggregated values for each nutrient.")
    chart_path: str = Field(description="The file path where the nutrition bar plot is saved.")

# ─── Tool: Calculate and Plot Nutrients ────────────────────────────────────────
# ─── Tool 1: Get User Selected Recipes ────────────────────────────────────────
def get_user_selected_recipes(user_name: str) -> List[str]:
    """
    Reads the user database and returns a list of recipe titles selected by the given user.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    user_db_path = os.path.join(base_dir, "database", "user_db.json")

    try:
        with open(user_db_path, "r") as f:
            user_data = json.load(f)
        
        if isinstance(user_data, list):
            for user in user_data:
                if user.get("user_name") == user_name:
                    return user.get("recipe_names", [])
        elif isinstance(user_data, dict):
            if user_data.get("user_name") == user_name:
                return user_data.get("recipe_names", [])

        return []
    except Exception as e:
        print(f"Error loading user recipes: {e}")
        return []

# ─── Tool 2: Get Recipe Nutrients ─────────────────────────────────────────────
def get_recipe_nutrients(recipe_names: List[str]) -> List[Dict]:
    """
    Fetches detailed nutrient data for a list of recipe names from the seed database.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    seed_recipes_path = os.path.join(base_dir, "recipe_db", "seed_recipes.json")

    try:
        with open(seed_recipes_path, "r") as f:
            seed_recipes = json.load(f)
        
        matching_nutrients = []
        for recipe in seed_recipes:
            if recipe.get("title") in recipe_names:
                matching_nutrients.append(recipe.get("nutrients", {}))
        
        return matching_nutrients
    except Exception as e:
        print(f"Error loading recipe nutrients: {e}")
        return []

# ─── Tool 3: Calculate and Plot Aggregated Nutrition ─────────────────────────
def calculate_and_plot_aggregated_nutrition(recipe_nutrients: List[Dict]) -> str:
    """
    Aggregates nutritional data from a list of nutrient dictionaries and generates a bar plot.
    """
    output_chart_path = os.path.join(os.path.dirname(__file__), "nutrition_chart.png")

    try:
        if not recipe_nutrients:
            return "No nutrient data provided to analyze."

        totals = {}
        
        def parse_value(val_str):
            if not val_str or not isinstance(val_str, str):
                return 0.0
            return float(''.join(c for c in val_str if c.isdigit() or c == '.'))

        for nutrients in recipe_nutrients:
            for key, value in nutrients.items():
                numeric_val = parse_value(value)
                unit = ''.join(c for c in value if c.isalpha()) if isinstance(value, str) else ""
                
                if key not in totals:
                    totals[key] = {"value": 0.0, "unit": unit}
                totals[key]["value"] += numeric_val

        # Generate Visualization
        plot_data = []
        for key, info in totals.items():
            plot_data.append({"Nutrient": key, "Value": info["value"], "Unit": info["unit"]})

        df = pd.DataFrame(plot_data)
        df = df.sort_values(by="Value", ascending=False)

        plt.figure(figsize=(12, 6))
        sns.set_theme(style="whitegrid")
        palette = sns.color_palette("muted", len(df))
        
        ax = sns.barplot(x="Value", y="Nutrient", data=df, palette=palette)
        
        # Add values on the bars
        for i, (idx, row) in enumerate(df.iterrows()):
            ax.text(row.Value + 0.1, i, f'{row.Value:.1f} {row.Unit}', va='center')

        plt.title(f"Total Nutritional Content for {len(recipe_nutrients)} Selected Recipes", fontsize=16, pad=20)
        plt.xlabel("Aggregated Value", fontsize=12)
        plt.ylabel("Nutrient", fontsize=12)
        plt.tight_layout()
        plt.savefig(output_chart_path)
        plt.close()

        result_totals = {k: f"{v['value']:.1f} {v['unit']}" for k, v in totals.items()}
        return json.dumps({
            "status": "success",
            "processed_recipes": len(recipe_nutrients),
            "totals": result_totals,
            "chart_path": output_chart_path
        })

    except Exception as e:
        return f"Error during nutritional analysis: {str(e)}"

# ─── Tool 4: Recommend Nutritional Additions ──────────────────────────────────
# ─── Load prompt config from YAML ─────────────────────────────────────────────
_PROMPT_FILE = os.path.join(os.path.dirname(__file__), "nutrition_analysis_prompt.yaml")

with open(_PROMPT_FILE, "r") as f:
    _config = yaml.safe_load(f)

MODEL = _config.get("model", "gemini-2.0-flash")

# ─── Agent: NutritionAnalysisAgent ──────────────────────────────────────────
nutrition_analysis_agent = Agent(
    name=_config["name"],
    model=MODEL,
    description=_config["description"],
    instruction=_config["instruction"],
    tools=[
        get_user_selected_recipes, 
        get_recipe_nutrients, 
        calculate_and_plot_aggregated_nutrition
    ],
    output_schema=NutritionOutput,
    output_key="nutrition_summary",
)

if __name__ == "__main__":
    # Test script to verify the decomposed tool chain
    user = "guest"
    print(f"1. Fetching recipes for user: {user}...")
    recipes = get_user_selected_recipes(user)
    print(f"   Recipes: {recipes}")
    
    if recipes:
        print(f"\n2. Fetching nutrients for recipes...")
        nutrients = get_recipe_nutrients(recipes)
        print(f"   Fetched data for {len(nutrients)} recipes.")
        
        if nutrients:
            print(f"\n3. Aggregating and plotting...")
            tool_result = calculate_and_plot_aggregated_nutrition(nutrients)
            result_json = json.loads(tool_result)
            print(f"   Aggregated Totals: {result_json.get('totals')}")
            print("\nVerification complete. The agent will now use its LLM reasoning to suggest additions based on these totals.")
    
    # We can't easily run the full agent without session state/mocks here, 
    # but we can verify the instantiation.
    print(f"\nAgent '{nutrition_analysis_agent.name}' instantiated successfully.")
