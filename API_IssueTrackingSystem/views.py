from rest_framework import generics, exceptions, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import action
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer, UsersSerializer
from .permissions import IsContributor, IsAuthorOrReadOnly

# VueSet pour les opérations CRUD sur le modèle Project
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user).distinct()

    def perform_create(self, serializer):
        if Project.objects.filter(title=serializer.validated_data['title']).exists():
            raise exceptions.ValidationError("Un projet avec ce titre existe déjà.")
        serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=serializer.instance, role='auteur')

# VueSet pour les contributeurs
class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Contributor.objects.select_related('project', 'user').filter(project__contributor__user=self.request.user)

    def perform_create(self, serializer):
        user = serializer.validated_data['user']
        project = serializer.validated_data['project']
        role = serializer.validated_data.get('role', '')
        if role not in ['auteur', 'collaborateur']:
            raise exceptions.ValidationError("Rôle invalide pour le contributeur.")
        if Contributor.objects.filter(user=user, project=project).exists():
            raise exceptions.ValidationError("Cet utilisateur est déjà un contributeur du projet.")
        serializer.save()

# VueSet pour les tâches (issues)
class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Issue.objects.select_related('project', 'assigned_to').filter(project__contributor__user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'].user = self.request.user
        return context

    def validate_project(self, value):
        user = self.request.user
        if not Contributor.objects.filter(user=user, project=value).exists():
            raise exceptions.ValidationError("Le projet spécifié n'existe pas ou vous n'y avez pas accès.")
        return value

    def get_fields(self):
        fields = super().get_fields()
        fields['project'].queryset = Project.objects.filter(contributor__user=self.request.user)
        fields['assigned_to'].queryset = Contributor.objects.filter(project__contributor__user=self.request.user)
        return fields

    def validate_assigned_to(self, value):
        project = self.request.data.get('project')
        if project:
            is_contributor_or_owner = Contributor.objects.filter(user_id=value, project_id=project).exists()
            if not is_contributor_or_owner:
                raise exceptions.ValidationError("L'utilisateur assigné doit être un contributeur ou un propriétaire du projet.")
        else:
            raise exceptions.ValidationError("Le projet doit être spécifié.")
        return value

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        if not Project.objects.filter(id=project_id, contributor__user=self.request.user).exists():
            raise exceptions.ValidationError("Le projet spécifié n'existe pas ou vous n'y avez pas accès.")
        issue_title = serializer.validated_data['title']
        if Issue.objects.filter(title=issue_title, project_id=project_id).exists():
            raise exceptions.ValidationError("Un problème avec ce titre existe déjà pour le projet spécifié.")
        assigned_to = self.request.data.get('assigned_to')
        if assigned_to:
            is_contributor_or_owner = Contributor.objects.filter(user_id=assigned_to, project_id=project_id).exists()
            if not is_contributor_or_owner:
                raise exceptions.ValidationError("L'utilisateur assigné doit être un contributeur ou un propriétaire du projet.")
        serializer.save()

# VueSet pour les commentaires
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.select_related('issue').filter(issue__project__contributor__user=self.request.user)

    def perform_create(self, serializer):
        comment = serializer.validated_data.get('description', '').strip()
        if not comment:
            raise exceptions.ValidationError("Le commentaire ne peut pas être vide.")
        serializer.save(author=self.request.user)

# VueSet pour la création d'utilisateurs
class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

# VueSet pour les droits RGPD de l'utilisateur
class UserDataViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        """Récupérer les données de l'utilisateur."""
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "projets": [project.title for project in Project.objects.filter(contributor__user=request.user)],
            "problèmes": [issue.title for issue in Issue.objects.filter(project__contributor__user=request.user)],
            "commentaires": [comment.description for comment in Comment.objects.filter(issue__project__contributor__user=request.user)],
            "contributeurs": [contributor.user.username for contributor in Contributor.objects.filter(project__contributor__user=request.user)]
        }
        return Response(user_data)

    @action(detail=False, methods=['GET'])
    def export_data(self, request):
        """Exporter les données de l'utilisateur au format JSON."""
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "projets": [project.title for project in Project.objects.filter(contributor__user=request.user)],
            "problèmes": [issue.title for issue in Issue.objects.filter(project__contributor__user=request.user)],
            "commentaires": [comment.description for comment in Comment.objects.filter(issue__project__contributor__user=request.user)],
            "contributeurs": [contributor.user.username for contributor in Contributor.objects.filter(project__contributor__user=request.user)]
        }
        return JsonResponse(user_data)

    @action(detail=False, methods=['DELETE'])
    def forget_me(self, request):
        """Supprimer l'utilisateur et toutes les données associées."""
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
