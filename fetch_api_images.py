import os
import django
import requests
from django.core.files.base import ContentFile
from datetime import datetime
from duckduckgo_search import DDGS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
django.setup()

from fowls.models import Product, ProductImage
from duckduckgo_search.exceptions import RatelimitException, TimeoutException
import time

def fetch_image_with_retry(query, attempt=1):
    print(f"Searching duckduckgo for: {query}")
    try:
        results = DDGS().images(query, max_results=5)
        for res in results:
            url = res.get('image')
            if not url: continue
            print(f"  Attempting URL: {url[:60]}...")
            try:
                r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200 and 'image' in r.headers.get('Content-Type', ''):
                    return r.content
            except Exception as e:
                print(f"  Fetch failed: {e}")
                continue
    except Exception as search_err:
        print(f"Search API error: {search_err}")
        if attempt < 3:
            time.sleep(2)
            return fetch_image_with_retry(query, attempt + 1)
        
    return None

def run():
    print("Fetching authentic images for all products...")
    
    for product in Product.objects.all():
        print(f"Processing Product {product.id}: {product.name}")
        
        breed_n = product.breed.name if product.breed else product.name
        cat_n = product.category.name if product.category else ''
        
        # refine query context
        search_query = f"{breed_n} {cat_n}"
        if "Coop" in product.name or "Feeder" in product.name or "Tractor" in product.name:
            search_query = product.name
        elif "Eggs" in cat_n:
            search_query = f"{product.name}"
            
        print(f" => Query context: {search_query}")
        
        image_content = fetch_image_with_retry(search_query)

        if image_content:
            filename = f"real_{product.id}_{int(datetime.now().timestamp())}.jpg"
            # Update thumbnail
            product.thumbnail.save(filename, ContentFile(image_content), save=True)
            print(f"  => Saved main thumbnail!")
            
            # Clear old subimages and add a fresh one (we can optionally fetch a second, but DDGS is slow)
            # For simplicity, we just save this as the sub image too, or try to get a second one from DDGS.
            product.images.all().delete()
            
            # Try fetching a SECOND image for the gallery
            image_content_2 = fetch_image_with_retry(search_query + " subpicture")
            sub_file_content = image_content_2 if image_content_2 else image_content
            
            sub_filename = f"real_sub_{product.id}_{int(datetime.now().timestamp())}.jpg"
            ProductImage.objects.create(
                product=product,
                image=ContentFile(sub_file_content, name=sub_filename)
            )
            print(f"  => Saved gallery sub-image!")
        else:
            print(f"  => FAILED to fetch a reliable image for {product.name}")
            
    print("Finished updating images!")

if __name__ == '__main__':
    run()
