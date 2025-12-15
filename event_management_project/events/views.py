from rest_framework import viewsets, mixins, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly 
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Event, CustomUser, Comment
from .serializers import EventSerializer, UserRegistrationSerializer, CommentSerializer
from .permissions import IsOrganizerOrReadOnly, IsAuthenticatedAndSelf
from .filters import EventFilter 
from rest_framework.pagination import PageNumberPagination

# --- Pagination Class ---

class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination settings for list views."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
# --- 1. User Management ViewSet (CRUD for Users) ---

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Allows retrieval, update, and deletion of user accounts.
    Only allows access to the authenticated user's own profile.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer 
    permission_classes = [IsAuthenticated, IsAuthenticatedAndSelf]

# --- 2. Event CRUD and Viewing Events ViewSet ---

class EventViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Events, including filtering, registration, and waitlist management.
    """
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    pagination_class = StandardResultsSetPagination

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
        """Allows an authenticated user to register for or unregister from an event."""
        event = self.get_object()
        user = request.user

        # Unregister logic
        if user in event.attendees.all():
            event.attendees.remove(user)
            return Response({'status': 'unregistered'}, status=status.HTTP_200_OK)

        # Register logic
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
        """Allows an authenticated user to join or leave the waitlist."""
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
    
# --- 3. Comment Permissions ---

class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of a comment to edit or delete it."""
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the comment
        return obj.user == request.user

# --- 4. Comment ViewSet ---

class CommentViewSet(viewsets.ModelViewSet):
    """CRUD operations for Comments, typically nested under an Event."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]

    def get_queryset(self):
        # Retrieve the event_pk from the URL kwargs provided by the nested router
        event_id = self.kwargs.get('event_pk')
        if event_id:
            # Filter comments to only show those belonging to the specified event
            return Comment.objects.filter(event_id=event_id)
        return Comment.objects.none()

    def perform_create(self, serializer):
        # Automatically set the 'event' and 'user' fields upon creation
        event = Event.objects.get(pk=self.kwargs['event_pk'])
        serializer.save(user=self.request.user, event=event)