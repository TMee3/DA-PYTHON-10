from API_IssueTrackingSystem.models import Project, Contributor, Comment, Issue
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsContributor(BasePermission):
    message = "The user is not a contributor of the project or does not have the required profile settings."

    def _get_project_id(self, obj):
        # Get project id based on the type of the object
        if isinstance(obj, Comment):
            return obj.issue.project.id
        elif isinstance(obj, Issue):
            return obj.project.id
        elif isinstance(obj, Project):
            return obj.id
        elif isinstance(obj, Contributor):
            return obj.project.id
        return None

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False      
        
        # Get the project_id from the object
        project_id = self._get_project_id(obj)
        if not project_id:
            return False

        # Check if the user is a contributor for the project
        return Contributor.objects.filter(user=request.user, project_id=project_id).exists()

class IsAuthorOrReadOnly(BasePermission):
    # Custom permission to only allow authors of a project to edit it
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions are determined based on the object type
        if isinstance(obj, Project):
            return obj.author == request.user
        elif isinstance(obj, Issue):
            return obj.assigned_to == request.user
        elif isinstance(obj, Comment):
            return obj.author == request.user
        elif isinstance(obj, Contributor):
            return obj.user == request.user
        return False  # Default case if obj type isn't handled
