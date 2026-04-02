from django.contrib import admin
from .models import ChatRoom, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    readonly_fields = ['timestamp', 'is_from_admin', 'is_read']
    fields = ['content', 'is_from_admin', 'is_read', 'timestamp']


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'visitor_email', 'last_message_at', 'unread_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['visitor_name', 'visitor_email', 'session_key']
    readonly_fields = ['session_key', 'created_at', 'last_message_at']
    inlines = [MessageInline]

    def unread_count(self, obj):
        count = obj.unread_admin_count()
        if count > 0:
            return f"🔴 {count} unread"
        return "✅ All read"
    unread_count.short_description = "Unread"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender_label', 'short_content', 'timestamp', 'is_read']
    list_filter = ['is_from_admin', 'is_read', 'timestamp']
    search_fields = ['content', 'room__visitor_name']

    def sender_label(self, obj):
        return "Admin" if obj.is_from_admin else obj.room.visitor_name
    sender_label.short_description = "From"

    def short_content(self, obj):
        return obj.content[:60] + "..." if len(obj.content) > 60 else obj.content
    short_content.short_description = "Message"
