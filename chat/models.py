from django.db import models
import uuid


class ChatRoom(models.Model):
    """Represents a unique chat session for a visitor."""
    session_key = models.CharField(max_length=40, unique=True)
    visitor_name = models.CharField(max_length=100, default='Guest')
    visitor_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-last_message_at']

    def __str__(self):
        return f"Chat with {self.visitor_name} ({self.session_key[:8]}...)"

    def unread_admin_count(self):
        """Messages from visitors that admin hasn't seen."""
        return self.messages.filter(is_from_admin=False, is_read=False).count()


class Message(models.Model):
    """A single chat message in a room."""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_from_admin = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        sender = "Admin" if self.is_from_admin else self.room.visitor_name
        return f"{sender}: {self.content[:50]}"
