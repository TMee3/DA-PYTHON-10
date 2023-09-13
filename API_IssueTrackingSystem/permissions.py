
from django.contrib.auth.models import User
from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsContributor(BasePermission):
    message = "The user is not a contributor of the project."

    def has_object_permission(self, request, view, obj):
        # If the object is an instance of Comment, use select_related to fetch the related issue and project
        if isinstance(obj, Comment):
            obj = Comment.objects.select_related('issue__project').get(pk=obj.pk)
            return Contributor.objects.filter(user=request.user, project=obj.issue.project).exists()

        # If the object is an instance of Issue, use select_related to fetch the related project
        elif isinstance(obj, Issue):
            obj = Issue.objects.select_related('project').get(pk=obj.pk)
            return Contributor.objects.filter(user=request.user, project=obj.project).exists()

        # For Project and Contributor, the previous checks are sufficient
        elif isinstance(obj, Project):
            return Contributor.objects.filter(user=request.user, project=obj).exists()
        
        elif isinstance(obj, Contributor):
            return Contributor.objects.filter(user=request.user, project=obj.project).exists()

        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a project to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only the author of the project can edit
        return obj.author == request.user
