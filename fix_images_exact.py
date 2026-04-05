import os
import django
import requests
from django.core.files.base import ContentFile
from datetime import datetime
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
django.setup()

from fowls.models import Product, ProductImage

WIKI_MAPPING = {
    # Birds
    'Broiler (Ross 308)': 'Broiler',
    'Layer (ISA Brown)': 'ISA_Brown',
    'Cockerel (White)': 'Chicken',
    'Brahma Rooster': 'Brahma_chicken',
    'Broad Breasted Turkey': 'Broad_Breasted_White_turkey',
    
    # Custom
    'Copper Marans': 'Marans',
    'Buff Orpington': 'Orpington_chicken',
    'Silkie': 'Silkie',
    'Rhode Island Red': 'Rhode_Island_Red',
    'Black Australorp': 'Australorp',
    'Barred Rock': 'Plymouth_Rock_chicken',
    'Leghorn': 'Leghorn_chicken',
    
    # Goats
    'Boar Goat': 'Boer_goat',
    'Saanen Goat': 'Saanen_goat',
    'Spanish Goat': 'Spanish_goat',
    'Alpine Goat': 'Alpine_goat',
    'Kalahari Red Goat': 'Kalahari_Red',
    
    # Calves
    'Holstein Calf': 'Holstein_Friesian_cattle',
    'Angus Calf': 'Angus_cattle',
    'Jersey Calf': 'Jersey_cattle',
    'Hereford Calf': 'Hereford_cattle',
    'Simmental Calf': 'Simmental_cattle',
    
    # Pigs/Others
    'Camborough Piglet': 'Pig',
    'Large White Piglet': 'Large_White_pig',
    'Landrace Piglet': 'Danish_Landrace_pig',
    'Guinea Pig': 'Guinea_pig',
    'Dorper Sheep': 'Dorper',
    
    # Eggs
    'Hatching Eggs': 'Egg_(food)',
    'Table Eggs': 'Egg_yolk',
    'Duck Eggs': 'Duck',
    'Quail Eggs': 'Quail_eggs',
    'Ostrich Egg': 'Ostrich_egg',
    
    # Equipment
    'Chicken Coop': 'Chicken_coop',
    'Standard Coop': 'Chicken_tractor',
    'Mobile Tractor': 'Chicken_tractor',
    'Commercial Coop': 'Poultry_farming',
    'Automatic Feeder': 'Bird_feeder',
    'Digital Incubator': 'Incubator_(egg)',
    'Professional Waterer': 'Poultry_farming',
    'Brooder Lamp': 'Infrared_heater',
}

def get_exact_wiki_image(title):
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "pageimages",
        "pithumbsize": 800,
        "format": "json"
    }
    headers = {'User-Agent': 'PoultryFarmBot/2.0'}
    try:
        r = requests.get(endpoint, params=params, headers=headers, timeout=10)
        data = r.json()
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    except Exception as e:
        pass
    return None

def fetch_wiki_image_content(url):
    try:
        r = requests.get(url, headers={'User-Agent': 'PoultryFarmBot/2.0'}, timeout=10)
        if r.status_code == 200:
            return r.content
    except:
        pass
    return None

def run():
    print("Fixing images with exact Wikipedia matches...")
    for product in Product.objects.all():
        breed_name = product.breed.name if product.breed else product.name
        wiki_title = WIKI_MAPPING.get(breed_name)
        
        if wiki_title:
            print(f"[{breed_name}] -> fetching '{wiki_title}'")
            img_url = get_exact_wiki_image(wiki_title)
            
            if img_url:
                image_content = fetch_wiki_image_content(img_url)
                if image_content:
                    filename = f"exact_{product.id}_{int(datetime.now().timestamp())}.jpg"
                    product.thumbnail.save(filename, ContentFile(image_content), save=True)
                    
                    product.images.all().delete()
                    sub_filename = f"exact_sub_{product.id}_{int(datetime.now().timestamp())}.jpg"
                    ProductImage.objects.create(
                        product=product,
                        image=ContentFile(image_content, name=sub_filename)
                    )
                    print("  => Success!")
                else:
                    print("  => Failed to download binary.")
            else:
                print("  => No thumbnail found on that Wikipedia page.")
        else:
            print(f"[{breed_name}] -> No mapping defined.")
            
        time.sleep(0.3)
        
    print("Image fixing complete.")

if __name__ == '__main__':
    run()
