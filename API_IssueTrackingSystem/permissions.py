from django.contrib.auth.models import User
from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment, UserProfile
from rest_framework.permissions import BasePermission
from rest_framework import permissions
 

class IsContributor(BasePermission):
    message = "The user is not a contributor of the project or does not have the required profile settings."

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False      
        # Get the project_id based on the type of obj
        if isinstance(obj, Comment):
            project_id = obj.issue.project.id
        elif isinstance(obj, Issue):
            project_id = obj.project.id
        elif isinstance(obj, Project):
            project_id = obj.id
        elif isinstance(obj, Contributor):
            project_id = obj.project.id
        else:
            return False

        # Check if the user is a contributor for the project
        return Contributor.objects.filter(user=request.user, project_id=project_id).exists()

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors of a project to edit it."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of a project
        return obj.author == request.user
    
