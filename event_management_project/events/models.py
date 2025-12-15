from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings # To get AUTH_USER_MODEL

class CustomUser(AbstractUser):
    # AbstractUser provides username, email, and password (custom fields can be added)
    pass 

class Event(models.Model):
    # Functional Requirements
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_and_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_events')
    capacity = models.PositiveBigIntegerField(help_text="Maximum number of attendees.")
    created_date = models.DateTimeField(auto_now_add=True)
    
    # Event capacity management
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='attending_events',blank=True)
    waitlist = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='waitlisted_events',blank=True)
    
    def __str__(self):
        return self.title
    
# Stretch Goal: Event Categories
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name 

# Stretch Goal: Event Comments
        
class Comment(models.Model):
    '''
    Model for storing comments and feedback related to an event.
    '''
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments', help_text="The event this comment relates to.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_comments', help_text="The user who submitted the comment.")
    content = models.TextField(help_text="The text of the comment or feedback.")
    rating = models.PositiveIntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)], help_text="Optional numerical rating (1-5)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.title}"
    
    