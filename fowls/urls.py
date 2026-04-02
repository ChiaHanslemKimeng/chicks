from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='fowl_list'),
    path('category/<slug:category_slug>/', views.product_list, name='category_list'),
    path('<int:pk>/', views.product_detail, name='fowl_detail'),
]
