import os
import django
import requests
from django.core.files.base import ContentFile
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
django.setup()

from fowls.models import Category, Breed, Product, ProductImage

def run():
    print("Starting custom breeds population...")

    # Ensure Birds category exists
    category, created = Category.objects.get_or_create(
        name='Birds',
        defaults={'icon': '🐔', 'description': 'Premium poultry for meat and egg production.'}
    )

    new_breeds_data = [
        {
            'name': 'Copper Marans',
            'desc': 'Famous for laying some of the darkest, chocolate-brown eggs of any chicken breed.',
            'product_name': 'Copper Marans Point-of-Lay',
            'price': 25.00,
            'age': '16 Weeks',
            'weight': '1.2kg',
            'feeding_type': 'Layer Grower',
            'img_url': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?auto=format&fit=crop&w=800'
        },
        {
            'name': 'Buff Orpington',
            'desc': 'Golden retrievers of the chicken world. Large, fluffy, docile, and lay light brown eggs.',
            'product_name': 'Buff Orpington Full Grown',
            'price': 30.00,
            'age': '24 Weeks',
            'weight': '2.5kg',
            'feeding_type': 'Organic Grain',
            'img_url': 'https://images.unsplash.com/photo-1569254994521-ddb54054f918?auto=format&fit=crop&w=800'
        },
        {
            'name': 'Silkie',
            'desc': 'Small ornamental bantam breed. Fluffy feathers, black skin, very broody.',
            'product_name': 'Silkie Bantam Chick',
            'price': 15.00,
            'age': '3 Weeks',
            'weight': '150g',
            'feeding_type': 'Starter Mash',
            'img_url': 'https://images.unsplash.com/photo-1542385151-efd9000785a0?auto=format&fit=crop&w=800'
        },
        {
            'name': 'Rhode Island Red',
            'desc': 'Hardy, independent, and lay a lot of brown eggs. A classic dual-purpose breed.',
            'product_name': 'Rhode Island Red Pullet',
            'price': 18.00,
            'age': '18 Weeks',
            'weight': '1.6kg',
            'feeding_type': 'Layer Pellets',
            'img_url': 'https://images.unsplash.com/photo-1594411130704-5f43009d0607?auto=format&fit=crop&w=800'
        },
        {
            'name': 'Black Australorp',
            'desc': 'Incredible egg layers (they hold records for egg production) that lay brown eggs.',
            'product_name': 'Black Australorp Layer',
            'price': 22.00,
            'age': '20 Weeks',
            'weight': '2.0kg',
            'feeding_type': 'Layer Mash',
            'img_url': 'https://images.unsplash.com/photo-1569254994521-ddb54054f918?auto=format&fit=crop&w=800'
        },
        {
            'name': 'Barred Rock',
            'desc': 'Classic, very friendly American heritage farm chicken with a black-and-white striped pattern.',
            'product_name': 'Barred Plymouth Rock Cockerel',
            'price': 20.00,
            'age': '12 Weeks',
            'weight': '1.8kg',
            'feeding_type': 'Grower Mash',
            'img_url': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?auto=format&fit=crop&w=800'
        },
        {
            'name': 'Leghorn',
            'desc': 'Famous for laying copious amounts of large white eggs. Very active breed.',
            'product_name': 'White Leghorn Layer',
            'price': 16.00,
            'age': '20 Weeks',
            'weight': '1.5kg',
            'feeding_type': 'Layer Pellets',
            'img_url': 'https://images.unsplash.com/photo-1542385151-efd9000785a0?auto=format&fit=crop&w=800'
        }
    ]

    for data in new_breeds_data:
        # Create Breed
        breed, b_created = Breed.objects.get_or_create(
            name=data['name'],
            category=category,
            defaults={'description': data['desc']}
        )
        print(f"Breed: {breed.name} ({'Created' if b_created else 'Exists'})")

        # Create Product
        product, p_created = Product.objects.get_or_create(
            name=data['product_name'],
            category=category,
            breed=breed,
            defaults={
                'price': data['price'],
                'age': data['age'],
                'weight': data['weight'],
                'feeding_type': data['feeding_type'],
                'description': data['desc'],
                'availability': True
            }
        )
        print(f"Product: {product.name} ({'Created' if p_created else 'Exists'})")

        # Download main thumbnail if it doesn't have one
        if not product.thumbnail:
            try:
                print(f"  Downloading main image for {product.name}...")
                response = requests.get(data['img_url'], timeout=10)
                if response.status_code == 200:
                    filename = f"product_{product.id}_{int(datetime.now().timestamp())}.jpg"
                    product.thumbnail.save(filename, ContentFile(response.content), save=True)
                    print(f"  Main Image saved!")
            except Exception as e:
                print(f"  Failed to download main image: {e}")

        # Ensure they have sub-images (gallery images)
        if product.images.count() == 0:
            try:
                print(f"  Downloading sub-image for {product.name}...")
                sub_response = requests.get(data['img_url'] + '&ixlib=rb-1.2.1', timeout=10) # slightly altered url to reuse image gracefully
                if sub_response.status_code == 200:
                    sub_filename = f"gallery_{product.id}_{int(datetime.now().timestamp())}.jpg"
                    prod_img = ProductImage(product=product)
                    prod_img.image.save(sub_filename, ContentFile(sub_response.content), save=True)
                    print(f"  Sub-image saved!")
            except Exception as e:
                print(f"  Failed to download sub-image: {e}")

    print("Custom breeds population complete!")

if __name__ == '__main__':
    run()
