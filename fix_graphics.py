import os
import django
import requests
from django.core.files.base import ContentFile
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
django.setup()

from fowls.models import Product, ProductImage

fixes = {
    'Thanksgiving Turkey Poults': 'https://loremflickr.com/800/800/turkey,animal,bird',
    'Entry-Level Backyard Coop': 'https://loremflickr.com/800/800/chicken,coop,wooden',
    'Luxury Backyard Coop': 'https://loremflickr.com/800/800/chicken,pen,large',
    'Stud Kalahari Red Kid': 'https://loremflickr.com/800/800/goat,farm,animal'
}

def run():
    for product_name, img_url in fixes.items():
        try:
            products = Product.objects.filter(name__icontains=product_name)
            if not products.exists():
                print(f"Product '{product_name}' not found.")
                continue

            product = products.first()
            print(f"Fixing {product.name}...")

            r = requests.get(img_url, timeout=10, allow_redirects=True)
            if r.status_code == 200:
                filename = f"fixed_{product.id}_{int(datetime.now().timestamp())}.jpg"
                product.thumbnail.save(filename, ContentFile(r.content), save=True)
                
                product.images.all().delete()
                sub_filename = f"fixed_sub_{product.id}_{int(datetime.now().timestamp())}.jpg"
                ProductImage.objects.create(
                    product=product,
                    image=ContentFile(r.content, name=sub_filename)
                )
                print("  => Image replaced using LoremFlickr!")
            else:
                print(f"  => Failed to fetch image (status {r.status_code})")
        except Exception as e:
            print(f"Error on {product_name}: {e}")

if __name__ == '__main__':
    run()
