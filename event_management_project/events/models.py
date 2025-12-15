from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings # To get AUTH_USER_MODEL

# --- 1. Custom User Model ---

class CustomUser(AbstractUser):
    """Extends Django's AbstractUser for custom user fields."""
    pass 

# --- 2. Category Model ---

class Category(models.Model):
    """Model to categorize events (e.g., Music, Sport, Tech)."""
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name 

# --- 3. Event Model ---

class Event(models.Model):
    """Model to store event details."""
    # Functional Requirements Fields (Fields are grouped at the top)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_and_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_events')
    capacity = models.PositiveBigIntegerField(help_text="Maximum number of attendees.")
    created_date = models.DateTimeField(auto_now_add=True)
    
    # Event capacity management
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attending_events', blank=True)
    waitlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='waitlisted_events', blank=True)
    
    # Event Category (Foreign Key field)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Model Methods (Placed after fields)
    def __str__(self):
        return self.title
    
# --- 4. Comment Model ---
        
class Comment(models.Model):
    '''Model for storing comments and feedback related to an event.'''
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments', help_text="The event this comment relates to.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_comments', help_text="The user who submitted the comment.")
    content = models.TextField(help_text="The text of the comment or feedback.")
    rating = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        choices=[(i, i) for i in range(1, 6)], 
        help_text="Optional numerical rating (1-5)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.title}"