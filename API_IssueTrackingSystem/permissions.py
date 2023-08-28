from rest_framework import permissions
from API_IssueTrackingSystem.models import Project, Issue, Comment, Contributor

class CanAccessContributorProjects(permissions.BasePermission):
    """
    Assurez-vous qu'un utilisateur peut accéder aux projets auxquels il contribue.
    """
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user=request.user).exists()

class CanAccessContributorIssues(permissions.BasePermission):
    """
    Assurez-vous qu'un utilisateur peut accéder aux problèmes des projets auxquels il contribue.
    """
    def has_object_permission(self, request, view, obj):
        return obj.project.contributors.filter(user=request.user).exists()

class CanAccessContributorComments(permissions.BasePermission):
    """
    Assurez-vous qu'un utilisateur peut accéder aux commentaires des problèmes des projets auxquels il contribue.
    """
    def has_object_permission(self, request, view, obj):
        return obj.issue.project.contributors.filter(user=request.user).exists()

class CanAccessContributors(permissions.BasePermission):
    """
    Assurez-vous qu'un utilisateur peut accéder aux objets Contributor auxquels il est associé.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CanManageContributorsPermission(permissions.BasePermission):
    """
    Autorisez uniquement l'auteur d'un projet à ajouter ou supprimer des contributeurs.
    """
    def has_object_permission(self, request, view, obj):
        return obj.project.author == request.user

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Autorisez uniquement l'auteur à modifier des objets, tandis que d'autres ne peuvent que lire.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsOwner(permissions.BasePermission):
    """
    Assurez-vous que l'utilisateur est le propriétaire de l'objet.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsContributor(permissions.BasePermission):
    """
    Assurez-vous que l'utilisateur est un contributeur au projet.
    """
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user=request.user).exists()

class CanCreateIssue(permissions.BasePermission):
    """
    Assurez-vous que seuls les contributeurs d'un projet peuvent créer des problèmes pour ce projet.
    """
    def has_permission(self, request, view):
        project_id = request.data.get('project')
        project = Project.objects.get(id=project_id)
        return project.contributors.filter(user=request.user).exists()

class CanCommentOnIssue(permissions.BasePermission):
    """
    Assurez-vous que seuls les contributeurs d'un projet peuvent commenter ses problèmes.
    """
    def has_permission(self, request, view):
        issue_id = request.data.get('issue')
        issue = Issue.objects.get(id=issue_id)
        return issue.project.contributors.filter(user=request.user).exists()
