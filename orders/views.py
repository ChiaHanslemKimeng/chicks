from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from fowls.models import Product
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def checkout(request, product_pk=None):
    product = None
    if product_pk:
        product = get_object_or_404(Product, pk=product_pk)
        
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        
        customer_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        quantity = int(request.POST.get('quantity', 1))
        payment_method = request.POST.get('payment_method')
        
        # Save order
        order = Order.objects.create(
            product=product,
            customer_name=customer_name,
            email=email,
            phone=phone,
            location=location,
            quantity=quantity,
            payment_method=payment_method
        )
        
        # Send Email
        subject = 'Payment Instructions for Your Poultry Order'
        context = {
            'customer_name': customer_name,
            'fowl_name': product.name,
            'quantity': quantity,
            'payment_method': order.get_payment_method_display(),
            'farm_name': 'PoultryElite Farm',
            'phone': '+123 456 7890',
            'email_address': 'info@poultryelite.com'
        }
        
        # Try to send email (won't crash if fails in dev)
        try:
            email_body = f"""
            Dear {customer_name},
            
            Thank you for your order from our poultry farm.
            
            Order Details:
            Fowl: {product.name}
            Quantity: {quantity}
            Selected Payment Method: {order.get_payment_method_display()}
            
            Based on your selected payment method, our admin will contact you shortly with the appropriate payment account details.
            
            Please wait for the payment instructions before proceeding.
            
            If you have any questions, feel free to contact us.
            
            Best regards,
            PoultryElite Farm
            📞 +123 456 7890
            📧 info@poultryelite.com
            """
            send_mail(
                subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Email error: {e}")
            
        return redirect('order_success', order_id=order.id)
        
    return render(request, 'orders/checkout.html', {'selected_product': product})

def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/order_success.html', {'order': order})
