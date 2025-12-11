from rest_framework import serializers
from .models import Event, CustomUser, Category

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
    
    