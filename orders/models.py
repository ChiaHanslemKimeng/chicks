from django.db import models
from fowls.models import Product

class Order(models.Model):
    PAYMENT_METHODS = [
        ('BANK', 'E Transfer/paypal'),
        ('PAYPAL', 'PayPal Checkout'),
        ('CHIME', 'Chime'),
        ('ZELLE', 'Zelle'),
        ('VENMO', 'Venmo'),
        ('CASHAPP', 'Cash App'),
        ('APPLE', 'Apple Card'),
        ('WIRE', 'Wire Transfer'),
        ('CRYPTO', 'Cryptocurrency'),
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

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
