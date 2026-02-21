import json
import os
import requests

def generate_mock_users():
    """Generates a mock user database by sending POST requests to the local API."""
    
    # We will generate roughly 10 recipe IDs each
    users = {
        "1337": {
            "user_id": "1337",
            "recipe_ids": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        },
        "404": {
            "user_id": "404",
            "recipe_ids": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        }
    }
    
    url = "http://localhost:8000/api/select_recipe"
    
    print(f"Sending mock user data to {url}...")
    for user_id, user_data in users.items():
        for recipe_id in user_data["recipe_ids"]:
            payload = {
                "user_id": user_id,
                "recipe_id": recipe_id
            }
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    print(f"Successfully posted recipe {recipe_id} for user {user_id}")
                else:
                    print(f"Failed to post recipe {recipe_id} for user {user_id}: Status {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to API. Is post_recipes.py running? Error: {e}")
                return # Exit early if the server isn't running
                
    print("User mock generation script completed.")

if __name__ == "__main__":
    generate_mock_users()
    # Command to run both user_generator.py and post_recipes.py
    # python -m mock_generator.user_generator & python post_recipes.py