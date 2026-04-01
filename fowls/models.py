from django.db import models
from django.utils.text import slugify

class Breed(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Fowl(models.Model):
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='fowls')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.CharField(max_length=50)  # e.g., "4 weeks", "6 months"
    weight = models.CharField(max_length=50, blank=True)
    vaccination_status = models.CharField(max_length=200, default="Fully Vaccinated")
    feeding_type = models.CharField(max_length=200, blank=True)
    availability = models.BooleanField(default=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='fowls/thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.breed.name})"

class FowlImage(models.Model):
    fowl = models.ForeignKey(Fowl, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='fowls/gallery/')

    def __str__(self):
        return f"Image for {self.fowl.name}"
