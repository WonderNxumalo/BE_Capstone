from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organiser of an event to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        #  Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the organiser of the event
        return obj.organizer == request.user
    
    
class IsAuthenticatedAndSelf(permissions.BasePermission):
    """
    Custom permission to only allow a user to update/delete their own account.
    """
    def has_object_permission(self, request, view, obj):
        # Read permisssions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        
        # Write permissions are only allowed to the user editing their own object
        return obj == request.user
    
    