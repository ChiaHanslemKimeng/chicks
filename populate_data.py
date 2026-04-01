import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
django.setup()

from django.core.files import File
from fowls.models import Breed, Fowl
from core.models import FAQ
from reviews.models import Review

def populate():
    print("Populating database...")

    # Define base media path for fowls
    media_fowls_path = os.path.join('media', 'fowls')

    # 1. Breeds
    breeds_data = [
        {'name': 'Broilers', 'description': 'Fast-growing chickens raised specifically for meat production.'},
        {'name': 'Layers', 'description': 'Breeds specialized in high egg production.'},
        {'name': 'Cockerels', 'description': 'Young male chickens, often raised for meat or breeding.'},
        {'name': 'Turkeys', 'description': 'Large birds known for their delicious meat, especially during holidays.'},
        {'name': 'Ducks', 'description': 'Waterfowl breeds perfect for eggs and meat.'},
        {'name': 'Indigenous Chickens', 'description': 'Local hardy breeds with unique flavors and resistance.'},
    ]

    breed_objs = {}
    for b_data in breeds_data:
        breed, created = Breed.objects.get_or_create(name=b_data['name'], defaults={'description': b_data['description']})
        breed_objs[b_data['name']] = breed

    # 2. Fowls
    fowls_data = [
        {
            'breed': 'Broilers',
            'name': 'Ross 308 Broiler',
            'price': Decimal('5.50'),
            'age': '4 weeks',
            'weight': '1.5kg',
            'description': 'High-performance broiler with excellent growth rate and feed conversion.',
            'image': 'broiler.jpg'
        },
        {
            'breed': 'Layers',
            'name': 'Isa Brown Layer',
            'price': Decimal('8.00'),
            'age': '16 weeks',
            'weight': '1.8kg',
            'description': 'The world\'s most popular brown egg layer. Highly productive and docile.',
            'image': 'layer.jpg'
        },
        {
            'breed': 'Turkeys',
            'name': 'Broad Breasted White',
            'price': Decimal('25.00'),
            'age': '12 weeks',
            'weight': '5.0kg',
            'description': 'Large turkey breed with high meat yield. Perfect for commercial production.',
            'image': 'turkey.jpg'
        },
        {
            'breed': 'Ducks',
            'name': 'Pekin Duck',
            'price': Decimal('12.00'),
            'age': '8 weeks',
            'weight': '3.0kg',
            'description': 'Fast-growing duck breed known for excellent meat quality and egg production.',
            'image': 'indigenous.jpg' # Duck image failed 404, using indigenous as placeholder
        },
        {
            'breed': 'Indigenous Chickens',
            'name': 'Local Village Chicken',
            'price': Decimal('10.00'),
            'age': '6 months',
            'weight': '1.2kg',
            'description': 'Tough, hardy local birds with rich organic flavor. Raised on free range.',
            'image': 'indigenous.jpg'
        }
    ]

    for f_data in fowls_data:
        fowl, created = Fowl.objects.get_or_create(
            name=f_data['name'],
            defaults={
                'breed': breed_objs[f_data['breed']],
                'price': f_data['price'],
                'age': f_data['age'],
                'weight': f_data['weight'],
                'description': f_data['description'],
                'availability': True
            }
        )
        
        # Add image if it exists and wasn't already set
        if created and 'image' in f_data:
            img_path = os.path.join(media_fowls_path, f_data['image'])
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    fowl.thumbnail.save(f_data['image'], File(f), save=True)
                    print(f"Assigned local image {f_data['image']} to {fowl.name}")

    # 3. FAQs
    faqs_data = [
        {'question': 'How do I order?', 'answer': 'Simply browse our fowls, select the ones you want, and click "Order Now". Fill in your details and select a payment method. Our admin will then contact you with instructions.'},
        {'question': 'What breeds are available?', 'answer': 'We offer Broilers, Layers, Cockerels, Turkeys, Ducks, and Indigenous local chickens.'},
        {'question': 'How is delivery done?', 'answer': 'We use specialized poultry transport vehicles to ensure your birds arrive healthy and stress-free at your location.'},
        {'question': 'Are the birds vaccinated?', 'answer': 'Yes, all our birds undergo a strict vaccination schedule managed by professional veterinarians.'},
    ]

    for faq in faqs_data:
        FAQ.objects.get_or_create(question=faq['question'], defaults={'answer': faq['answer']})

    # 4. Reviews
    print("Adding reviews...")
    from django.utils import timezone
    from datetime import timedelta

    reviews_data = [
        {'name': 'John Doe', 'rating': 5, 'comment': 'Excellent quality broilers! They grew so fast and stayed healthy.', 'approved': True, 'days_ago': 5},
        {'name': 'Sarah Smith', 'rating': 4, 'comment': 'The Isa Brown layers started laying right on time. Highly recommended.', 'approved': True, 'days_ago': 12},
        {'name': 'Michael Jordan', 'rating': 5, 'comment': 'Fast delivery and very professional service. The turkeys were healthy.', 'approved': True, 'days_ago': 20},
        {'name': 'David Bekham', 'rating': 5, 'comment': 'Top notch indigenous chickens. Very resistant and great taste.', 'approved': True, 'days_ago': 35},
        {'name': 'Alice Johnson', 'rating': 5, 'comment': 'Best layers I have ever bought. Very high egg production.', 'approved': True, 'days_ago': 45},
        {'name': 'Robert Wilson', 'rating': 4, 'comment': 'Great ducks! Very healthy and arrived on time.', 'approved': True, 'days_ago': 60},
        {'name': 'Emily Davis', 'rating': 5, 'comment': 'The broilers are massive! Best feed conversion ratio.', 'approved': True, 'days_ago': 75},
        {'name': 'James Miller', 'rating': 5, 'comment': 'Very professional farm. Well vaccinated birds.', 'approved': True, 'days_ago': 90},
        {'name': 'Sophia Brown', 'rating': 4, 'comment': 'Good service, birds are healthy. Will buy again.', 'approved': True, 'days_ago': 105},
        {'name': 'Daniel Taylor', 'rating': 5, 'comment': 'Indigenous breeds are very hardy. Survived the cold season well.', 'approved': True, 'days_ago': 120},
        {'name': 'Olivia Anderson', 'rating': 5, 'comment': 'The turkeys made our holiday special. Giant and healthy.', 'approved': True, 'days_ago': 135},
        {'name': 'Matthew Thomas', 'rating': 4, 'comment': 'Reliable delivery and good quality chicks.', 'approved': True, 'days_ago': 150},
        {'name': 'Isabella Moore', 'rating': 5, 'comment': 'Love the Pekin ducks. Very productive.', 'approved': True, 'days_ago': 165},
        {'name': 'Jackson White', 'rating': 5, 'comment': 'Excellent expertise. Their advice helped my small farm grow.', 'approved': True, 'days_ago': 180},
        {'name': 'Lucas Harris', 'rating': 4, 'comment': 'Best place for broiler chicks. Very low mortality rate.', 'approved': True, 'days_ago': 195},
        {'name': 'Grace Martin', 'rating': 5, 'comment': 'Quality layers and great customer support.', 'approved': True, 'days_ago': 210},
    ]

    for rev in reviews_data:
        review, created = Review.objects.get_or_create(
            customer_name=rev['name'],
            comment=rev['comment'],
            defaults={'rating': rev['rating'], 'is_approved': rev['approved']}
        )
        
        # Override created_at for historical representation
        target_date = timezone.now() - timedelta(days=rev['days_ago'])
        Review.objects.filter(pk=review.pk).update(created_at=target_date)

    print("Population complete!")

if __name__ == '__main__':
    populate()
