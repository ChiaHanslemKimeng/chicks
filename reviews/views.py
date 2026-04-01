from django.shortcuts import render, redirect
from .models import Review

def reviews(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            customer_name=customer_name,
            rating=rating,
            comment=comment
        )
        return redirect('reviews')
        
    approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'reviews/reviews.html', {'reviews': approved_reviews})
