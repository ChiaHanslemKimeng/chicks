import os
import django
import requests
from django.core.files.base import ContentFile
from datetime import datetime
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
django.setup()

from fowls.models import Product, ProductImage

def get_wiki_image_url(query):
    print(f"  Searching Wikipedia for: {query}")
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 0,
        "gsrlimit": 3,  # Get top 3 to find one with an image
        "prop": "pageimages",
        "pithumbsize": 800,
        "format": "json"
    }
    headers = {'User-Agent': 'PoultryFarmBot/1.0'}
    
    try:
        r = requests.get(endpoint, params=params, headers=headers, timeout=10)
        data = r.json()
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    except Exception as e:
        print(f"   Notice: fetch failed: {e}")
    return None

def fetch_wiki_image_content(url):
    try:
        r = requests.get(url, headers={'User-Agent': 'PoultryFarmBot/1.0'}, timeout=10)
        if r.status_code == 200:
            return r.content
    except Exception as e:
        print(f"   Download failed: {e}")
    return None

def run():
    print("Fetching authentic Wikipedia images for all products...")
    
    for product in Product.objects.all():
        print(f"Processing Product {product.id}: {product.name}")
        
        breed_n = product.breed.name if product.breed else product.name
        cat_n = product.category.name if product.category else ''
        
        search_query = f"{breed_n} {cat_n}"
        if "Coop" in product.name or "Feeder" in product.name or "Tractor" in product.name:
            search_query = product.name
        elif "Eggs" in cat_n:
            search_query = f"{product.name} egg"
        else:
             search_query = breed_n
             
        img_url = get_wiki_image_url(search_query)
        if not img_url:
            # Fallback search strategy
            img_url = get_wiki_image_url(breed_n.split(' (')[0])
            
        if img_url:
            print(f"   => Found URL: {img_url[:70]}...")
            image_content = fetch_wiki_image_content(img_url)
            
            if image_content:
                filename = f"wiki_{product.id}_{int(datetime.now().timestamp())}.jpg"
                product.thumbnail.save(filename, ContentFile(image_content), save=True)
                print(f"   => Saved main thumbnail!")
                
                # Clear and re-assign sub-image
                product.images.all().delete()
                sub_filename = f"wiki_sub_{product.id}_{int(datetime.now().timestamp())}.jpg"
                ProductImage.objects.create(
                    product=product,
                    image=ContentFile(image_content, name=sub_filename)
                )
                print(f"   => Saved gallery image!")
            else:
                print("   => FAILED to download image binary.")
        else:
            print("   => NO IMAGE FOUND for query.")
            
        time.sleep(0.5)

    print("Finished updating images!")

if __name__ == '__main__':
    run()
