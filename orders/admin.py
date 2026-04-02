from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'product', 'quantity', 'payment_method', 'created_at', 'is_processed')
    list_filter = ('payment_method', 'is_processed', 'created_at')
    search_fields = ('customer_name', 'email', 'phone', 'location')
    list_editable = ('is_processed',)
