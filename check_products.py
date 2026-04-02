import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
import django
django.setup()

from fowls.models import Product

# Remove the old duplicate names (keep the newer ones)
duplicates = [
    'Thanksgiving Turkey Poults (5 Pack)',   # old name, replaced by 'Thanksgiving Turkey Poults'
    'Luxury Backyard Coop (10-15 Birds)',    # old name, replaced by 'Luxury Backyard Coop'
    'Heavy Duty 10kg Feeder',                # old name, replaced by inline entry
    'Hygienic Nipple System (50 Birds)',     # old: keep 'Hygienic Nipple System'
]

for name in duplicates:
    deleted, _ = Product.objects.filter(name=name).delete()
    print(f"Removed '{name}': {deleted} row(s)")

print(f"\nFinal total: {Product.objects.count()} products")
from fowls.models import Category
for cat in Category.objects.all():
    print(f"  {cat.name}: {Product.objects.filter(category=cat).count()} products")
