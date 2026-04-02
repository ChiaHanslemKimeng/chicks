from django.urls import path
from . import views

urlpatterns = [
    # Visitor API (called by floating chat widget)
    path('api/init/', views.init_chat, name='chat_init'),
    path('api/send/', views.send_message, name='chat_send'),
    path('api/poll/', views.poll_messages, name='chat_poll'),

    # Admin panel views
    path('admin-chat/', views.admin_chat_list, name='admin_chat_list'),
    path('admin-chat/<int:room_id>/', views.admin_chat_detail, name='admin_chat_detail'),
    path('admin-chat/<int:room_id>/reply/', views.admin_reply, name='admin_reply'),
    path('admin-chat/<int:room_id>/poll/', views.admin_poll, name='admin_poll'),
]
