from API_IssueTrackingSystem.models import Project, Contributor, Comment, Issue
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsContributor(BasePermission):
    message = "L'utilisateur n'est pas un contributeur du projet ou n'a pas les paramètres de profil requis."

    def _get_project_id(self, obj):
        # Obtenir l'identifiant du projet en fonction du type d'objet
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
        # Vérifier si l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return False      
        
        # Obtenir l'identifiant du projet depuis l'objet
        project_id = self._get_project_id(obj)
        if not project_id:
            return False

        # Vérifier si l'utilisateur est un contributeur du projet
        return Contributor.objects.filter(user=request.user, project_id=project_id).exists()

class IsAuthorOrReadOnly(BasePermission):
    # Permission personnalisée pour autoriser uniquement les auteurs d'un projet à le modifier
    def has_object_permission(self, request, view, obj):
        # Les permissions de lecture sont autorisées pour toutes les requêtes GET, HEAD et OPTIONS (SAFE_METHODS)
        if request.method in SAFE_METHODS:
            return True
        
        # Les permissions d'écriture sont déterminées en fonction du type d'objet
        if isinstance(obj, Project):
            return obj.author == request.user
        elif isinstance(obj, Issue):
            return obj.assigned_to == request.user
        elif isinstance(obj, Comment):
            return obj.author == request.user
        elif isinstance(obj, Contributor):
            return obj.user == request.user
        return False  # Cas par défaut si le type d'objet n'est pas géré
