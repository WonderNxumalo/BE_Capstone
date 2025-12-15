from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import EventViewSet, CommentViewSet

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')

# Nested Router for Comment
comments_router = routers.NestedDefaultRouter(router, 'events', lookup='event')
comments_router.register('comments', CommentViewSet, basename='event-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
]