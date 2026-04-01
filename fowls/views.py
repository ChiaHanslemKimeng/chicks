from django.shortcuts import render, get_object_or_404
from .models import Fowl, Breed, FowlImage
from django.db.models import Q
from django.core.paginator import Paginator

def fowl_list(request):
    fowls = Fowl.objects.filter(availability=True).order_by('-created_at')
    breeds = Breed.objects.all()
    
    # Filtering
    breed_slug = request.GET.get('breed')
    if breed_slug:
        fowls = fowls.filter(breed__slug=breed_slug)
        
    search_query = request.GET.get('search')
    if search_query:
        fowls = fowls.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(breed__name__icontains=search_query)
        )
        
    price_min = request.GET.get('min_price')
    if price_min:
        fowls = fowls.filter(price__gte=price_min)
        
    price_max = request.GET.get('max_price')
    if price_max:
        fowls = fowls.filter(price__lte=price_max)
        
    # Pagination
    paginator = Paginator(fowls, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'breeds': breeds,
        'current_breed': breed_slug,
    }
    return render(request, 'fowls/fowl_list.html', context)

def fowl_detail(request, pk):
    fowl = get_object_or_404(Fowl, pk=pk)
    related_fowls = Fowl.objects.filter(breed=fowl.breed, availability=True).exclude(pk=pk)[:4]
    return render(request, 'fowls/fowl_detail.html', {
        'fowl': fowl,
        'related_fowls': related_fowls
    })
