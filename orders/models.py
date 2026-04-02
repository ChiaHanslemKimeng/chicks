from django.db import models
from fowls.models import Product

class Order(models.Model):
    PAYMENT_METHODS = [
        ('MTN', 'Mobile Money (MTN)'),
        ('ORANGE', 'Mobile Money (Orange)'),
        ('BANK', 'Bank Transfer'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
