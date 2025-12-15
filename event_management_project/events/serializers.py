from rest_framework import serializers
from .models import Event, CustomUser, Category, Comment

# User Registration Serialiser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
# Event Serializer 
class EventSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField(source='organizer.username', read_only=True)
    attendees_count = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        allow_null=True
    )
    class Meta:
        model = Event
        # Includes all fields but make 'organiser' read-only for API input
        fields = (
            'id', 'title', 'description', 'date_and_time', 'location', 'capacity', 'created_date', 'organizer',
            'organizer_username', 'attendees', 'waitlist', 'attendees_count', 'category'
        )
        read_only_fields = ('organizer', 'created_date', 'attendees', 'waitlist')
        
    def get_attendees_count(self, obj):
        return obj.attendees.count()
    
    # Validation: Ensure future event date (Requirement)
    def validate_date_and_time(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Events must be in the future.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    # The event ID is typically passed via the URL, so it's read-only here
    event_id = serializers.PrimaryKeyRelatedField(source='event', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id', 'event_id', 'user', 'user_username', 'content', 
            'rating', 'created_at'
        )
        # We need 'user' to be read-only as it will be set by the viewset based on the logged-in user.
        read_only_fields = ('user', 'event_id', 'created_at')

    # Validation to ensure rating is within the 1-5 range if provided
    def validate_rating(self, value):
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value    
    