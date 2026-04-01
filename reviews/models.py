from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    customer_name = models.CharField(max_length=200)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer_name} - {self.rating}/5"
