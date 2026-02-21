import json
import os
import requests

def generate_mock_users():
    """Generates a mock user database by sending POST requests to the local API."""
    
    # We will generate roughly 10 recipe IDs each
    users = {
        "md": {
            "user_name": "md",
            "recipe_names": ["Marcus Samuelsson Fried Chicken", "Hudson Breakfast Bagel", "Detroit Brick Pizza"]
        },
        "guest": {
            "user_name": "guest",
            "recipe_names": ["SriPraPhai Thai Special", "Royal Greens Salad Bowl", "Mihir's Special"]
        }
    }
    
    url = "http://localhost:8000/api/select_recipe"
    
    print(f"Sending mock user data to {url}...")
    for user_name, user_data in users.items():
        for recipe_name in user_data["recipe_names"]:
            payload = {
                "user_name": user_name,
                "recipe_name": recipe_name
            }
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    print(f"Successfully posted recipe {recipe_name} for user {user_name}")
                else:
                    print(f"Failed to post recipe {recipe_name} for user {user_name}: Status {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to API. Is post_recipes.py running? Error: {e}")
                return # Exit early if the server isn't running
                
    print("User mock generation script completed.")

if __name__ == "__main__":
    generate_mock_users()
    # Command to run both user_generator.py and post_recipes.py
    # python -m mock_generator.user_generator & python post_recipes.py