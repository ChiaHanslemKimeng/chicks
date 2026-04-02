from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or Icon class")

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Breed(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='breeds', null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name if self.category else 'No Category'})"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.CharField(max_length=50, blank=True)  # Still useful for livestock
    weight = models.CharField(max_length=50, blank=True)
    vaccination_status = models.CharField(max_length=200, default="Fully Vaccinated")
    feeding_type = models.CharField(max_length=200, blank=True)
    availability = models.BooleanField(default=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='products/thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category.name if self.category else 'No Category'})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"
