from django.shortcuts import render, redirect
from fowls.models import Fowl
from .models import FAQ
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    featured_fowls = Fowl.objects.filter(availability=True)[:4]
    return render(request, 'core/home.html', {'featured_fowls': featured_fowls})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject_line = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Email Body
        email_body = f"Message from {name} ({email}):\n\nSubject: {subject_line}\n\n{message}"
        
        try:
            send_mail(
                f"Contact Form: {subject_line}",
                email_body,
                email, # From email (user's email)
                [settings.DEFAULT_FROM_EMAIL], # To admin email
                fail_silently=False,
            )
            messages.success(request, "Thank you for your message! We'll get back to you shortly.")
        except Exception as e:
            messages.error(request, "Oops! There was an error sending your message. Please try again later.")
            
        return redirect('contact')
        
    return render(request, 'core/contact.html')

def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'core/faq.html', {'faqs': faqs})
