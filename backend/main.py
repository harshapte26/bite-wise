import os, yaml, asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.recipe_creator.recipe_creator import create_recipe_creator_agent

load_dotenv()

# ── Build agent ONCE (instruction kept with {placeholders} intact) ────────────
with open("agents/recipe_creator/recipe_creator_prompt.yaml") as f:
    config = yaml.safe_load(f)

agent = create_recipe_creator_agent(config, config["model"])

# ── Invoke: swap state each call to change the prompt ─────────────────────────
async def run(existing_recipes: list[str], nutrition_info: str):
    sessions = InMemorySessionService()

    # State values fill {existing_recipes} and {nutrition_info} in the YAML instruction
    await sessions.create_session(
        app_name="bite-wise",
        user_id="u1",
        session_id="s1",
        state={
            "existing_recipes": "\n".join(f"- {r}" for r in existing_recipes),
            "nutrition_info": nutrition_info,
        },
    )

    runner = Runner(agent=agent, app_name="bite-wise", session_service=sessions)

    async for event in runner.run_async(
        user_id="u1",
        session_id="s1",
        new_message=types.Content(role="user", parts=[types.Part(text="Go.")]),
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)
            break


# ── Change inputs here each time you want a different recipe ──────────────────
asyncio.run(run(
    existing_recipes=[
        "Spicy Miso Ramen",
        "Avocado Toast Bowl",
        "Detroit Brick Pizza",
    ],
    nutrition_info="High protein, under 600 calories, low carb",
))
