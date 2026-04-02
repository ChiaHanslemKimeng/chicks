import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
django.setup()

import requests
from django.core.files.base import ContentFile
from fowls.models import Category, Breed, Product
from core.models import FAQ
from reviews.models import Review

def populate():
    print("Starting population script...")

    # 1. Create Categories
    categories_data = [
        {'name': 'Birds', 'icon': '🐔', 'description': 'Premium poultry for meat and egg production.'},
        {'name': 'Eggs', 'icon': '🥚', 'description': 'Fertilized and table eggs from elite breeds.'},
        {'name': 'Livestock', 'icon': '🐄', 'description': 'Healthy calves, goats, and piglets.'},
        {'name': 'Equipment', 'icon': '🛠️', 'description': 'Modern poultry and farm infrastructure.'},
    ]

    categories = {}
    for cat in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat['name'],
            defaults={'icon': cat['icon'], 'description': cat['description']}
        )
        categories[cat['name']] = category
        print(f"Category: {category.name} ({'Created' if created else 'Exists'})")

    # 2. Create Breeds
    breeds_data = [
        # Birds
        {'name': 'Broiler (Ross 308)', 'category': 'Birds', 'description': 'Fast-growing meat birds.'},
        {'name': 'Layer (ISA Brown)', 'category': 'Birds', 'description': 'High-yield egg producers.'},
        {'name': 'Cockerel (White)', 'category': 'Birds', 'description': 'Hardy dual-purpose birds.'},
        {'name': 'Brahma Rooster', 'category': 'Birds', 'description': 'Majestic large breed for meat and show.'},
        {'name': 'Broad Breasted Turkey', 'category': 'Birds', 'description': 'Premium large birds for meat production.'},
        # Eggs
        {'name': 'Hatching Eggs', 'category': 'Eggs', 'description': 'Fertilized eggs ready for incubation.'},
        {'name': 'Table Eggs', 'category': 'Eggs', 'description': 'Fresh organic consumption eggs.'},
        {'name': 'Duck Eggs', 'category': 'Eggs', 'description': 'Rich, large eggs for specialty baking.'},
        {'name': 'Quail Eggs', 'category': 'Eggs', 'description': 'Nutrient-dense mini eggs.'},
        {'name': 'Ostrich Egg', 'category': 'Eggs', 'description': 'Massive novelty eggs for specialty markets.'},
        # Livestock - Goats
        {'name': 'Boar Goat', 'category': 'Livestock', 'description': 'Elite meat goat breed.'},
        {'name': 'Saanen Goat', 'category': 'Livestock', 'description': 'Top dairy goat breed.'},
        {'name': 'Spanish Goat', 'category': 'Livestock', 'description': 'Hardy meat goat breed.'},
        {'name': 'Alpine Goat', 'category': 'Livestock', 'description': 'High-performance dairy goat.'},
        {'name': 'Kalahari Red Goat', 'category': 'Livestock', 'description': 'Premium meat goat with high resistance.'},
        # Livestock - Calves
        {'name': 'Holstein Calf', 'category': 'Livestock', 'description': 'High-quality dairy/meat calves.'},
        {'name': 'Angus Calf', 'category': 'Livestock', 'description': 'Superior beef-producing calves.'},
        {'name': 'Jersey Calf', 'category': 'Livestock', 'description': 'Compact dairy calves with rich milk.'},
        {'name': 'Hereford Calf', 'category': 'Livestock', 'description': 'Docile beef cattle known for meat quality.'},
        {'name': 'Simmental Calf', 'category': 'Livestock', 'description': 'Dual-purpose beef/dairy calves.'},
        # Livestock - Pigs/Guinea
        {'name': 'Camborough Piglet', 'category': 'Livestock', 'description': 'Fast-growing hybrid piglets.'},
        {'name': 'Large White Piglet', 'category': 'Livestock', 'description': 'Classic high-weight swine breed.'},
        {'name': 'Landrace Piglet', 'category': 'Livestock', 'description': 'Efficient meat production pig breed.'},
        {'name': 'Guinea Pig', 'category': 'Livestock', 'description': 'Healthy pets or research animals.'},
        {'name': 'Dorper Sheep', 'category': 'Livestock', 'description': 'Excellent meat-producing sheep breed.'},
        # Equipment
        {'name': 'Chicken Coop', 'category': 'Equipment', 'description': 'Professional housing solutions.'},
        {'name': 'Standard Coop', 'category': 'Equipment', 'description': 'Affordable 5-8 bird housing.'},
        {'name': 'Mobile Tractor', 'category': 'Equipment', 'description': 'Portable rotatable bird housing.'},
        {'name': 'Commercial Coop', 'category': 'Equipment', 'description': 'Industrial-scale poultry housing.'},
        {'name': 'Automatic Feeder', 'category': 'Equipment', 'description': 'Smart feeding systems.'},
        {'name': 'Digital Incubator', 'category': 'Equipment', 'description': 'Precision egg hatching technology.'},
        {'name': 'Professional Waterer', 'category': 'Equipment', 'description': 'High-capacity hygiene-focused watering.'},
        {'name': 'Brooder Lamp', 'category': 'Equipment', 'description': 'Essential heating for young chicks.'},
    ]

    breeds = {}
    for b in breeds_data:
        breed, created = Breed.objects.get_or_create(
            name=b['name'],
            category=categories[b['category']],
            defaults={'description': b['description']}
        )
        breeds[b['name']] = breed
        print(f"Breed: {breed.name} ({'Created' if created else 'Exists'})")

    # 3. Create Products
    products_data = [
        # Birds (5)
        {'category': 'Birds', 'breed': 'Broiler (Ross 308)', 'name': 'Day-Old Broiler (Pack of 50)', 'price': 45.00, 'age': '1 Day', 'weight': '40g', 'feeding_type': 'Starter Mash', 'description': 'Elite Ross 308 broilers.'},
        {'category': 'Birds', 'breed': 'Layer (ISA Brown)', 'name': 'Point-of-Lay Pullets', 'price': 12.00, 'age': '18 Weeks', 'weight': '1.5kg', 'feeding_type': 'Layer Pellets', 'description': 'Consistent high-quality egg producers.'},
        {'category': 'Birds', 'breed': 'Cockerel (White)', 'name': 'Hardy White Cockerels (10 Pack)', 'price': 15.00, 'age': '4 Weeks', 'weight': '500g', 'feeding_type': 'Grower Mash', 'description': 'Strong, disease-resistant cockerels.'},
        {'category': 'Birds', 'breed': 'Brahma Rooster', 'name': 'Giant Brahma Breeder', 'price': 65.00, 'age': '6 Months', 'weight': '4.5kg', 'feeding_type': 'Organic Grain', 'description': 'Magnificent Brahma rooster.'},
        {'category': 'Birds', 'breed': 'Broad Breasted Turkey', 'name': 'Thanksgiving Turkey Poults', 'price': 40.00, 'age': '2 Weeks', 'weight': '300g', 'feeding_type': 'Turkey Starter', 'description': 'Broad-breasted white turkey poults.'},
        
        # Goats (5)
        {'category': 'Livestock', 'breed': 'Boar Goat', 'name': 'Young Meat Goat (Male)', 'price': 150.00, 'age': '6 Months', 'weight': '25kg', 'feeding_type': 'Forage', 'description': 'Healthy Boer goat offspring.'},
        {'category': 'Livestock', 'breed': 'Saanen Goat', 'name': 'Dairy Saanen Doe', 'price': 220.00, 'age': '1 Year', 'weight': '45kg', 'feeding_type': 'Hay & Grain', 'description': 'Excellent dairy goat with high milk yield.'},
        {'category': 'Livestock', 'breed': 'Spanish Goat', 'name': 'Wild Range Spanish Goat', 'price': 130.00, 'age': '8 Months', 'weight': '30kg', 'feeding_type': 'Natural Forage', 'description': 'Hardy meat goat for rough terrain.'},
        {'category': 'Livestock', 'breed': 'Alpine Goat', 'name': 'French Alpine Buck', 'price': 250.00, 'age': '10 Months', 'weight': '50kg', 'feeding_type': 'Silage', 'description': 'Premium breeding buck for dairy production.'},
        {'category': 'Livestock', 'breed': 'Kalahari Red Goat', 'name': 'Stud Kalahari Red Kid', 'price': 300.00, 'age': '4 Months', 'weight': '20kg', 'feeding_type': 'Milk & Creep', 'description': 'Top genetics Kalahari Red meat goat.'},
        
        # Calves (5)
        {'category': 'Livestock', 'breed': 'Holstein Calf', 'name': 'Premium Dairy Calf', 'price': 350.00, 'age': '3 Months', 'weight': '80kg', 'feeding_type': 'Milk Replacer', 'description': 'Strong Holstein-Friesian calf.'},
        {'category': 'Livestock', 'breed': 'Angus Calf', 'name': 'Black Angus Beef Calf', 'price': 400.00, 'age': '4 Months', 'weight': '120kg', 'feeding_type': 'Creep Feed', 'description': 'Superior beef genetics Angus calf.'},
        {'category': 'Livestock', 'breed': 'Jersey Calf', 'name': 'Purebred Jersey Heifer', 'price': 380.00, 'age': '3 Months', 'weight': '70kg', 'feeding_type': 'Milk', 'description': 'Small-framed dairy calf with rich milk potential.'},
        {'category': 'Livestock', 'breed': 'Hereford Calf', 'name': 'White-Face Hereford Calf', 'price': 370.00, 'age': '5 Months', 'weight': '140kg', 'feeding_type': 'Pasture', 'description': 'Hardy beef calf with excellent foraging skills.'},
        {'category': 'Livestock', 'breed': 'Simmental Calf', 'name': 'Dual-Purpose Simmental Calf', 'price': 420.00, 'age': '3 Months', 'weight': '95kg', 'feeding_type': 'Mixed Feed', 'description': 'Large-framed calf for balanced production.'},
        
        # Pigs / Guinea (5)
        {'category': 'Livestock', 'breed': 'Camborough Piglet', 'name': 'Weaned Piglet (6 Pack)', 'price': 240.00, 'age': '8 Weeks', 'weight': '15kg', 'feeding_type': 'Pig Starter', 'description': 'Camborough hybrid piglets.'},
        {'category': 'Livestock', 'breed': 'Large White Piglet', 'name': 'Commercial Large White Piglet', 'price': 45.00, 'age': '10 Weeks', 'weight': '20kg', 'feeding_type': 'Swine Grower', 'description': 'High-yield bacon pig breed.'},
        {'category': 'Livestock', 'breed': 'Landrace Piglet', 'name': 'Danish Landrace Piglet', 'price': 50.00, 'age': '9 Weeks', 'weight': '18kg', 'feeding_type': 'Organic Pig Feed', 'description': 'Lean meat production specialist swine.'},
        {'category': 'Livestock', 'breed': 'Guinea Pig', 'name': 'Guinea Pig Breeding Pair', 'price': 30.00, 'age': '4 Months', 'weight': '800g', 'feeding_type': 'Pellets', 'description': 'Healthy breeding pair.'},
        {'category': 'Livestock', 'breed': 'Dorper Sheep', 'name': 'Prime Dorper Lamb', 'price': 180.00, 'age': '5 Months', 'weight': '35kg', 'feeding_type': 'Grass', 'description': 'Fast-growing meat sheep.'},

        # Eggs (5)
        {'category': 'Eggs', 'breed': 'Hatching Eggs', 'name': 'Fertilized Broiler Eggs (Crate)', 'price': 25.00, 'age': 'Fresh', 'weight': '60g', 'feeding_type': 'N/A', 'description': 'High fertility broiler eggs.'},
        {'category': 'Eggs', 'breed': 'Table Eggs', 'name': 'Organic Table Eggs (Large Crate)', 'price': 15.00, 'age': 'Fresh', 'weight': '1.8kg', 'feeding_type': 'N/A', 'description': 'Free-range foraging eggs.'},
        {'category': 'Eggs', 'breed': 'Duck Eggs', 'name': 'Premium PEKIN Duck Eggs', 'price': 12.00, 'age': 'Fresh', 'weight': '80g', 'feeding_type': 'N/A', 'description': 'Rich, large duck eggs.'},
        {'category': 'Eggs', 'breed': 'Quail Eggs', 'name': 'Nutrient-Dense Quail Eggs (100 Pack)', 'price': 20.00, 'age': 'Fresh', 'weight': '10g', 'feeding_type': 'N/A', 'description': 'Gourmet quail eggs.'},
        {'category': 'Eggs', 'breed': 'Ostrich Egg', 'name': 'Jumbo Ostrich Egg (Single)', 'price': 50.00, 'age': 'N/A', 'weight': '1.5kg', 'feeding_type': 'N/A', 'description': 'Massive ostrich egg.'},

        # Equipment (5)
        {'category': 'Equipment', 'breed': 'Chicken Coop', 'name': 'Luxury Backyard Coop', 'price': 550.00, 'age': 'New', 'weight': '120kg', 'feeding_type': 'N/A', 'description': 'Premium bird housing.'},
        {'category': 'Equipment', 'breed': 'Standard Coop', 'name': 'Entry-Level Backyard Coop', 'price': 250.00, 'age': 'New', 'weight': '60kg', 'feeding_type': 'N/A', 'description': 'Compact and mobile coop for 5 birds.'},
        {'category': 'Equipment', 'breed': 'Mobile Tractor', 'name': 'Chicken Tractor (Portable)', 'price': 320.00, 'age': 'New', 'weight': '80kg', 'feeding_type': 'N/A', 'description': 'Movable coop for lawn grazing.'},
        {'category': 'Equipment', 'breed': 'Commercial Coop', 'name': 'Industrial Greenhouse Coop', 'price': 1500.00, 'age': 'New', 'weight': '500kg', 'feeding_type': 'N/A', 'description': 'Professional scale poultry farming solution.'},
        {'category': 'Equipment', 'breed': 'Automatic Feeder', 'name': 'Heavy Duty 10kg Feeder', 'price': 35.00, 'age': 'New', 'weight': '2kg', 'feeding_type': 'N/A', 'description': 'Anti-waste smart feeder.'},
    ]

    for p in products_data:
        product, created = Product.objects.get_or_create(
            name=p['name'],
            category=categories[p['category']],
            breed=breeds[p['breed']],
            defaults={
                'price': p['price'],
                'age': p['age'],
                'weight': p['weight'],
                'feeding_type': p['feeding_type'],
                'description': p['description'],
                'availability': True
            }
        )
        print(f"Product: {product.name} ({'Created' if created else 'Exists'})")

    # 4. Handle Images
    breed_images = {
        'Broiler (Ross 308)': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?auto=format&fit=crop&w=800',
        'Layer (ISA Brown)': 'https://images.unsplash.com/photo-1569254994521-ddb54054f918?auto=format&fit=crop&w=800',
        'Cockerel (White)': 'https://images.unsplash.com/photo-1542385151-efd9000785a0?auto=format&fit=crop&w=800',
        'Brahma Rooster': 'https://images.unsplash.com/photo-1594411130704-5f43009d0607?auto=format&fit=crop&w=800',
        'Broad Breasted Turkey': 'https://images.unsplash.com/photo-1529421308418-eab98863cef3?auto=format&fit=crop&w=800',
        'Boar Goat': 'https://images.unsplash.com/photo-1563851512140-7561f558a74e?auto=format&fit=crop&w=800',
        'Saanen Goat': 'https://images.unsplash.com/photo-1524024973431-2ad916746881?auto=format&fit=crop&w=800',
        'Spanish Goat': 'https://images.unsplash.com/photo-1533514114760-4389f5fd440a?auto=format&fit=crop&w=800',
        'Alpine Goat': 'https://images.unsplash.com/photo-1524024973431-2ad916746881?auto=format&fit=crop&w=800',
        'Kalahari Red Goat': 'https://images.unsplash.com/photo-1563851512140-7561f558a74e?auto=format&fit=crop&w=800',
        'Holstein Calf': 'https://images.unsplash.com/photo-1546445317-29f4545e9d53?auto=format&fit=crop&w=800',
        'Angus Calf': 'https://images.unsplash.com/photo-1545468500-2646698129da?auto=format&fit=crop&w=800',
        'Jersey Calf': 'https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?auto=format&fit=crop&w=800',
        'Hereford Calf': 'https://images.unsplash.com/photo-1546445317-29f4545e9d53?auto=format&fit=crop&w=800',
        'Simmental Calf': 'https://images.unsplash.com/photo-1545468500-2646698129da?auto=format&fit=crop&w=800',
        'Camborough Piglet': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?auto=format&fit=crop&w=800',
        'Large White Piglet': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?auto=format&fit=crop&w=800',
        'Landrace Piglet': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?auto=format&fit=crop&w=800',
        'Guinea Pig': 'https://images.unsplash.com/photo-1533514114760-4389f5fd440a?auto=format&fit=crop&w=800',
        'Dorper Sheep': 'https://images.unsplash.com/photo-1484557918186-7b4e571d4b12?auto=format&fit=crop&w=800',
        'Hatching Eggs': 'https://images.unsplash.com/photo-1518562180175-34a163b1a9a6?auto=format&fit=crop&w=800',
        'Table Eggs': 'https://images.unsplash.com/photo-1569254994521-ddb54054f918?auto=format&fit=crop&w=800',
        'Duck Eggs': 'https://images.unsplash.com/photo-1518562180175-34a163b1a9a6?auto=format&fit=crop&w=800',
        'Quail Eggs': 'https://images.unsplash.com/photo-1518562180175-34a163b1a9a6?auto=format&fit=crop&w=800',
        'Ostrich Egg': 'https://images.unsplash.com/photo-1518562180175-34a163b1a9a6?auto=format&fit=crop&w=800',
        'Chicken Coop': 'https://images.unsplash.com/photo-1594411130704-5f43009d0607?auto=format&fit=crop&w=800',
        'Standard Coop': 'https://images.unsplash.com/photo-1594411130704-5f43009d0607?auto=format&fit=crop&w=800',
        'Mobile Tractor': 'https://images.unsplash.com/photo-1594411130704-5f43009d0607?auto=format&fit=crop&w=800',
        'Commercial Coop': 'https://images.unsplash.com/photo-1594411130704-5f43009d0607?auto=format&fit=crop&w=800',
        'Automatic Feeder': 'https://images.unsplash.com/photo-1589139130095-248386389270?auto=format&fit=crop&w=800',
        'Digital Incubator': 'https://images.unsplash.com/photo-1518562180175-34a163b1a9a6?auto=format&fit=crop&w=800',
        'Professional Waterer': 'https://images.unsplash.com/photo-1589139130095-248386389270?auto=format&fit=crop&w=800',
        'Brooder Lamp': 'https://images.unsplash.com/photo-1518562180175-34a163b1a9a6?auto=format&fit=crop&w=800',
    }

    for product in Product.objects.all():
        if not product.thumbnail and product.breed.name in breed_images:
            try:
                print(f"Downloading image for {product.name}...")
                response = requests.get(breed_images[product.breed.name], timeout=10)
                if response.status_code == 200:
                    filename = f"product_{product.id}.jpg"
                    product.thumbnail.save(filename, ContentFile(response.content), save=True)
                    print(f"Image saved for {product.name}")
            except Exception as e:
                print(f"Failed to download image: {e}")

    # 5. Create Reviews
    Review.objects.all().delete()
    review_names = ["John Doe", "Sarah Smith", "Michael Chen", "Emily Brown", "David Wilson", 
                    "Maria Garcia", "James Taylor", "Linda Martinez", "Robert Anderson", "Patricia Taylor",
                    "Thomas Moore", "Nancy White", "William Harris", "Charles Martin", "Karen Thompson"]
    
    review_comments = [
        "Exceptional quality birds! Very healthy.",
        "The delivery was fast and the goats look great.",
        "My ISA Browns are laying like clockwork. 5 stars!",
        "Sturdy chicken coop, easy to assemble.",
        "The calves are robust and growing fast.",
        "Best poultry supplier in the region.",
        "Very professional support and guidance.",
        "The hatching eggs had a great success rate.",
        "Quality equipment that lasts. Highly recommend.",
        "Healthy piglets, no issues since delivery."
    ]

    for i in range(16):
        name = random.choice(review_names)
        comment = random.choice(review_comments)
        rating = random.randint(4, 5)
        days_ago = random.randint(1, 150)
        review = Review.objects.create(
            customer_name=name,
            rating=rating,
            comment=comment,
            is_approved=True
        )
        # Update creation date manually
        date = datetime.now() - timedelta(days=days_ago)
        Review.objects.filter(pk=review.pk).update(created_at=date)

    # 5. Create FAQs
    FAQ.objects.all().delete()
    faqs_data = [
        ("Do you deliver nationwide?", "Yes, we have climate-controlled transport for all livestock and products."),
        ("What is your refund policy?", "We guarantee 100% health upon arrival. Contact us within 24 hours for any issues."),
        ("Do you provide training?", "Yes, we offer expert farm management advisory for all our customers."),
        ("Are the birds vaccinated?", "All our birds follow a strict, certified vaccination schedule."),
    ]
    for q, a in faqs_data:
        FAQ.objects.create(question=q, answer=a)

    print("Population complete!")

if __name__ == '__main__':
    populate()
