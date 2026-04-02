from django.shortcuts import render, get_object_or_404
from .models import Category, Breed, Product, ProductImage
from django.db.models import Q
from django.core.paginator import Paginator

def product_list(request, category_slug=None):
    products = Product.objects.filter(availability=True).order_by('-created_at')
    categories = Category.objects.all()
    
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
        breeds = current_category.breeds.all()
    else:
        breeds = Breed.objects.all()
    
    # Filtering
    breed_slug = request.GET.get('breed')
    if breed_slug:
        products = products.filter(breed__slug=breed_slug)
        
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(breed__name__icontains=search_query)
        )
        
    price_min = request.GET.get('min_price')
    if price_min:
        products = products.filter(price__gte=price_min)
        
    price_max = request.GET.get('max_price')
    if price_max:
        products = products.filter(price__lte=price_max)
        
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': current_category,
        'breeds': breeds,
        'current_breed': breed_slug,
    }
    return render(request, 'fowls/fowl_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category, availability=True).exclude(pk=pk)[:4]
    return render(request, 'fowls/fowl_detail.html', {
        'product': product,
        'related_products': related_products
    })
