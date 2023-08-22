from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from API_IssueTrackingSystem.models import Project, Issue, Comment, Contributor

# Permission pour vérifier si l'utilisateur peut accéder aux projets sur lesquels il est contributeur
class CanAccessContributorProjects(permissions.BasePermission):
    def has_permission(self, request, view):
        return Project.objects.filter(contributors__user=request.user).exists()

# Permission pour vérifier si l'utilisateur peut accéder aux problèmes sur lesquels il est contributeur
class CanAccessContributorIssues(permissions.BasePermission):
    def has_permission(self, request, view):
        return Issue.objects.filter(project__contributors__user=request.user).exists()

# Permission pour vérifier si l'utilisateur peut accéder aux commentaires sur lesquels il est contributeur
class CanAccessContributorComments(permissions.BasePermission):
    def has_permission(self, request, view):
        return Comment.objects.filter(issue__project__contributors__user=request.user).exists()

# Permission pour vérifier si l'utilisateur peut accéder aux contributeurs
class CanAccessContributors(permissions.BasePermission):
    def has_permission(self, request, view):
        return Contributor.objects.filter(user=request.user).exists()

# Permission pour gérer les contributeurs (ajouter, supprimer) dans un projet
class CanManageContributorsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            project_id = request.data.get('project')  # Assurez-vous d'adapter cela à votre logique
            if Contributor.objects.filter(project_id=project_id, user=request.user, role='auteur').exists():
                return True
        return False

# Permission pour autoriser uniquement l'auteur à modifier les objets
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Méthodes sûres comme GET, HEAD, OPTIONS
            return True
        return obj.author == request.user
