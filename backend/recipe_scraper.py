import os
import json
import requests
from dotenv import load_dotenv
from recipe_scrapers import scrape_me
from google.cloud import storage

load_dotenv()
# GCP Configuration
BUCKET_NAME = "bitewise-recipe-images"
# Ensure GOOGLE_APPLICATION_CREDENTIALS env var is set to your service account key path

def upload_to_gcp(local_file_path, destination_blob_name):
    """Uploads a file to the GCP bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    return blob.public_url

def scrape_and_store_recipe(url):
    try:
        # 1. Scrape Recipe
        scraper = scrape_me(url)
        title = scraper.title()
        
        # 2. Get Nutritional Info (if available on the site)
        nutrients = scraper.nutrients()
        
        # 3. Handle Image
        image_url = scraper.image()
        image_extension = image_url.split('.')[-1].split('?')[0] # Basic extension cleaner
        safe_title = "".join([c for c in title if c.isalnum() or c==' ']).rstrip().replace(' ', '_').lower()
        image_name = f"{safe_title}.{image_extension}"
        
        # Download image temporarily
        img_data = requests.get(image_url).content
        with open(image_name, 'wb') as handler:
            handler.write(img_data)
        
        # # 4. Upload to Cloud
        cloud_image_url = upload_to_gcp(image_name, f"seed_recipes/{image_name}")
        
        # 5. Prepare Metadata
        recipe_data = {
            "title": title,
            "nutrients": nutrients,
            "ingredients": scraper.ingredients(),
            "directions": scraper.instructions(),
            "image_name": image_name,
            "cloud_image_url": cloud_image_url,
            "metadata": {
                "source_url": url,
                "total_time": scraper.total_time(),
                "yields": scraper.yields()
            }
        }
        
        # Clean up local image
        os.remove(image_name)
        return recipe_data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def seed_recipes():
    # if seed_recipes.json exists, skip
    if os.path.exists('database/seed_recipes.json'):
        return

    urls = [
        "https://www.allrecipes.com/recipe/240652/paneer-tikka-masala/",
        "https://www.allrecipes.com/recipe/91499/general-tsaos-chicken-ii/",
        "https://www.allrecipes.com/recipe/8300592/perfect-chicken-piccata/",
        "https://www.allrecipes.com/mexican-street-corn-chicken-chili-recipe-11850006",
        "https://www.allrecipes.com/michigan-olive-burger-recipe-11732096",
        "https://www.allrecipes.com/recipe/246123/panang-curry-with-tofu-and-vegetables/"
    ]
    
    results = []
    for url in urls:
        data = scrape_and_store_recipe(url)
        if data:
            results.append(data)
    
    # Save to JSON
    with open('database/seed_recipes.json', 'w') as f:
        json.dump(results, f, indent=4)
