from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

# Create your models here.

class User(AbstractUser):
    """
    User model that extends the Django AbstractUser.
    Contains additional fields for user profile information.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Note: email, username, password, first_name, last_name are already included in AbstractUser
    email = models.EmailField(unique=True)  # Override to make email required and unique
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    last_seen = models.DateTimeField(default=timezone.now)
    is_online = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Model representing a conversation between users.
    A conversation can have multiple participants.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    
    def __str__(self):
        if self.is_group and self.title:
            return f"Group: {self.title}"
        return f"Conversation: {', '.join([user.username for user in self.participants.all()[:3]])}"
    
    class Meta:
        ordering = ['-updated_at']


class Message(models.Model):
    """
    Model representing a message sent in a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()  # Renamed from content to message_body
    sent_at = models.DateTimeField(auto_now_add=True)  # Renamed from created_at to sent_at
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.sender.username}: {self.message_body[:50]}"
    
    def mark_as_read(self):
        """Mark message as read and set read timestamp"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    class Meta:
        ordering = ['sent_at']
