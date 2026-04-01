from django.urls import path
from . import views

urlpatterns = [
    path('', views.fowl_list, name='fowl_list'),
    path('<int:pk>/', views.fowl_detail, name='fowl_detail'),
]
