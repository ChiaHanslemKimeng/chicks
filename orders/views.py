from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from fowls.models import Product
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .cart import Cart
from django.views.decorators.http import require_POST

# Cart Views
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # We will enforce quantities during checkout, but can enforce here if needed.
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart_view')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'Removed {product.name} from your cart.')
    return redirect('cart_view')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            cart.add(product=product, quantity=quantity, update_quantity=True)
            messages.success(request, f'Updated {product.name} quantity.')
        else:
            cart.remove(product)
            messages.success(request, f'Removed {product.name} from your cart.')
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity.')
    return redirect('cart_view')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

def checkout(request, product_pk=None):
    cart = Cart(request)
    
    if len(cart) == 0:
        return redirect('cart_view')
        
    if request.method == 'POST':
        # Validations!
        total_price = cart.get_total_price()
        if total_price < 100:
            messages.error(request, "Minimum order total (including shipping) must be at least $100 to proceed.")
            return redirect('cart_view')
            
        egg_qty = sum(item['quantity'] for item in cart if item['product'].category and item['product'].category.name.lower() == 'eggs')
        has_eggs = any(item['product'].category and item['product'].category.name.lower() == 'eggs' for item in cart)
        if has_eggs and egg_qty < 1:
            messages.error(request, "Minimum order for eggs is 1 tray.")
            return redirect('cart_view')
            
        customer_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        payment_method = request.POST.get('payment_method')
        
        # Save order
        order = Order.objects.create(
            customer_name=customer_name,
            email=email,
            phone=phone,
            location=location,
            payment_method=payment_method
        )
        
        items_string = ""
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
            items_string += f"            - {item['quantity']} x {item['product'].name} (${item['total_price']:.2f})\n"
            
        subtotal = cart.get_subtotal()
        shipping_fee = 30
        total_price = cart.get_total_price()
        
        # Prepare email data
        cart_items_for_email = []
        for item in cart:
            cart_items_for_email.append({
                'product': item['product'],
                'quantity': item['quantity'],
                'total_price': item['total_price']
            })
            
        context = {
            'customer_name': customer_name,
            'customer_email': email,
            'customer_phone': phone,
            'customer_location': location,
            'payment_method': order.get_payment_method_display(),
            'items': cart_items_for_email,
            'subtotal': cart.get_subtotal(),
            'total_price': cart.get_total_price(),
            'order_pk': order.pk,
        }
        
        try:
            from django.core.mail import EmailMultiAlternatives
            
            # 1. Send Confirmation to Customer
            customer_subject = 'Order Confirmation - Universal Poultry Farm'
            customer_html = render_to_string('orders/emails/customer_order.html', context)
            customer_text = f"Dear {customer_name}, thank you for your order. Total: ${cart.get_total_price():.2f}"
            
            msg_customer = EmailMultiAlternatives(
                customer_subject,
                customer_text,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            msg_customer.attach_alternative(customer_html, "text/html")
            msg_customer.send(fail_silently=False)
            
            # 2. Send Notification to Admin
            admin_subject = f'NEW ORDER #{order.id} - {customer_name}'
            admin_html = render_to_string('orders/emails/admin_notification.html', context)
            admin_text = f"New order received from {customer_name}. Total: ${cart.get_total_price():.2f}"
            
            msg_admin = EmailMultiAlternatives(
                admin_subject,
                admin_text,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER]
            )
            msg_admin.attach_alternative(admin_html, "text/html")
            msg_admin.reply_to = [email] # So admin can just click reply
            msg_admin.send(fail_silently=False)
            
        except Exception as e:
            print(f"Email error: {e}")
            
        cart.clear()
        return redirect('order_success', order_id=order.id)
        
    return render(request, 'orders/checkout.html', {'cart': cart})

def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    subtotal = sum(item.price * item.quantity for item in order.items.all())
    shipping_fee = 30
    total_amount = subtotal + shipping_fee
    
    context = {
        'order': order,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total_amount': total_amount
    }
    return render(request, 'orders/order_success.html', context)
