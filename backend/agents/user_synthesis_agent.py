import os
from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

class UserSynthesisAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

    def get_agent(self):
        return Agent(
            role="User Culinary Profiler",
            goal="Analyze a user's selected recipes to synthesize their culinary and dietary preferences.",
            backstory=(
                "You are an expert culinary analyst with deep knowledge of global cuisines, "
                "dietary restrictions, and flavor profiles. Your specialty is understanding "
                "user tastes based on their food choices to provide a personalized experience."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def get_task(self, user_name, selected_recipes, agent):
        recipe_names = ", ".join([r.get("recipe_name", "Unknown Recipe") for r in selected_recipes])
        description = (
            f"Analyze the following data for user '{user_name}':\n"
            f"Selected Recipes: {recipe_names}\n\n"
            "Synthesize a profile for this user including:\n"
            "1. Cuisine Preferences: Identify dominant cuisines or regional styles.\n"
            "2. Dietary Tendencies: Note if the choices lean towards vegetarian, keto, spicy, etc.\n"
            "3. Flavor Profile: Describe the types of flavors the user likely enjoys (e.g., savory, sweet, bold, mild).\n"
            "4. Overall Persona: A brief summary of the user's culinary identity."
        )
        expected_output = (
            "A concise markdown report summarizing the user's cuisine preferences, "
            "dietary tendencies, flavor profile, and overall culinary persona."
        )
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output
        )

if __name__ == "__main__":
    # Example usage
    agent = UserSynthesisAgent()
    mock_recipes = [
        {"recipe_id": 1, "recipe_name": "Marcus Samuelsson Fried Chicken"},
        {"recipe_id": 2, "recipe_name": "SriPraPhai Thai Special"},
        {"recipe_id": 5, "recipe_name": "Detroit Brick Pizza"}
    ]
    user_agent = agent.get_agent()
    result = agent.get_task("Harsh", mock_recipes, user_agent)
    print("\n--- User Synthesis Task ---")
    print(result)
