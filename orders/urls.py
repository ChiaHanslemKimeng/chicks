from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:fowl_pk>/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
]
