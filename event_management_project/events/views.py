from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Event, CustomUser
from .serializers import EventSerializer, UserRegistrationSerializer
from .permissions import IsOrganizerOrReadOnly, IsAuthenticatedAndSelf
from .filters import EventFilter 

# 1. User Management ViewSet (CRUD for Users)
class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    # Only allow retrieving/updating/deleting the logged-in user's account
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer # Using registration serializer for updates
    permission_classes = [IsAuthenticated, IsAuthenticatedAndSelf]

# 2. Event CRUD and Viewing Events ViewSet
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    pagination_class = None 

    def get_queryset(self):
        # View Upcoming Events: Filter events where date_and_time is in the future
        return Event.objects.filter(date_and_time__gte=timezone.now()).order_by('date_and_time')

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create', 'register', 'waitlist_toggle']: # Create & custom actions need auth
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']: # Update/Delete needs IsOrganizer
            self.permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]
        else: # list, retrieve (Read operations)
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Set the organizer to the current logged-in user
        serializer.save(organizer=self.request.user)

    # Event Capacity Management (Enroll/Unenroll)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if user in event.attendees.all():
            event.attendees.remove(user)
            return Response({'status': 'unregistered'}, status=status.HTTP_200_OK)

        if event.attendees.count() < event.capacity:
            event.attendees.add(user)
            # Remove from waitlist if applicable
            if user in event.waitlist.all():
                event.waitlist.remove(user)
            return Response({'status': 'registered'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'event is full'}, status=status.HTTP_400_BAD_REQUEST)

    # Optional Waitlist Toggle
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def waitlist_toggle(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if user in event.attendees.all():
            return Response({'status': 'already registered'}, status=status.HTTP_400_BAD_REQUEST)

        if user in event.waitlist.all():
            event.waitlist.remove(user)
            return Response({'status': 'removed from waitlist'}, status=status.HTTP_200_OK)
        else:
            event.waitlist.add(user)
            return Response({'status': 'added to waitlist'}, status=status.HTTP_201_CREATED)