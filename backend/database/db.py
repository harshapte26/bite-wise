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

def get_user(user_id):
    db = load_db()
    for user in db:
        if user["user_id"] == str(user_id):
            return user
    return None

def get_all_users():
    return load_db()

def add_saved_recipe(user_id, recipe_id):
    db = load_db()
    user_id_str = str(user_id)
    
    user = next((u for u in db if u["user_id"] == user_id_str), None)
    if not user:
        user = {"user_id": user_id_str, "recipe_ids": []}
        db.append(user)
        
    user["recipe_ids"].append(recipe_id)
    save_db(db)
    return True

def remove_saved_recipe(user_id, recipe_id):
    db = load_db()
    user_id_str = str(user_id)
    
    user = next((u for u in db if u["user_id"] == user_id_str), None)
    if user and recipe_id in user["recipe_ids"]:
        user["recipe_ids"].remove(recipe_id) # Removes first occurrence 
        save_db(db)
        return True
        
    return False
