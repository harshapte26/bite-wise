import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'user_db.json')

def load_db():
    if not os.path.exists(DB_FILE):
        # Create directory if missing and initialize with empty array
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        save_db([])
        return []
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_user(user_name):
    db = load_db()
    for user in db:
        if user.get("user_name") == str(user_name):
            return user
    return None

def get_all_users():
    return load_db()

def add_saved_recipe(user_name, recipe_name):
    db = load_db()
    user_name_str = str(user_name)
    
    user = next((u for u in db if u.get("user_name") == user_name_str), None)
    if not user:
        user = {"user_name": user_name_str, "recipe_names": []}
        db.append(user)
        
    if recipe_name not in user["recipe_names"]:
        user["recipe_names"].append(recipe_name)
    save_db(db)
    return True

def remove_saved_recipe(user_name, recipe_name):
    db = load_db()
    user_name_str = str(user_name)
    
    user = next((u for u in db if u.get("user_name") == user_name_str), None)
    if user and recipe_name in user["recipe_names"]:
        user["recipe_names"].remove(recipe_name) # Removes first occurrence 
        save_db(db)
        return True
        
    return False
