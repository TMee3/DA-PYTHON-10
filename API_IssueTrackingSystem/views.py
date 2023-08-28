from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer, ProjectSerializerFull, ContributorSerializer,
    IssueSerializer, CommentSerializer, UsersSerializer
)
from .permissions import (
    CanAccessContributorProjects, CanAccessContributorIssues,
    CanAccessContributorComments, CanAccessContributors,
    CanManageContributorsPermission, IsAuthorOrReadOnly,
    IsOwner, IsContributor, CanCreateIssue, CanCommentOnIssue
)

class UserViewSet(generics.CreateAPIView):
    """
    Vue pour la création d'utilisateurs.
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination standard pour les vues.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProjectViewSet(ModelViewSet):
    """
    Vue pour gérer les projets.
    """
    serializer_class = ProjectSerializer
    serializer_class_full = ProjectSerializerFull
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticated, CanAccessContributorProjects, IsOwner]

    def get_queryset(self):
        """
        Récupère uniquement les projets auxquels l'utilisateur est contributeur ou auteur.
        """
        return Project.objects.filter(contributors__user=self.request.user)

    def get_serializer_class(self):
        """
        Utilise un serializer différent pour l'action 'retrieve'.
        """
        if self.action == 'retrieve':
            return self.serializer_class_full
        return super().get_serializer_class()

    def perform_create(self, serializer):
        """
        Crée un projet et ajoute l'utilisateur actuel en tant que contributeur.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project, role='auteur')

class ContributorViewSet(ModelViewSet):
    """
    Vue pour gérer les contributeurs.
    """
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, IsContributor]

    def get_queryset(self):
        """
        Récupère uniquement les contributeurs des projets dont l'utilisateur est l'auteur ou contributeur.
        """
        return Contributor.objects.filter(project__contributors__user=self.request.user)

class IssueViewSet(ModelViewSet):
    """
    Vue pour gérer les problèmes.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, CanCreateIssue]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'tag', 'priority', 'status']

    def get_queryset(self):
        """
        Récupère uniquement les problèmes des projets auxquels l'utilisateur est contributeur.
        """
        return Issue.objects.filter(project__contributors__user=self.request.user)

class CommentViewSet(ModelViewSet):
    """
    Vue pour gérer les commentaires.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, CanCommentOnIssue]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['description']

    def get_queryset(self):
        """
        Récupère uniquement les commentaires des problèmes des projets auxquels l'utilisateur est contributeur.
        """
        return Comment.objects.filter(issue__project__contributors__user=self.request.user)

class FullProjectViewSet(viewsets.ModelViewSet):
    """
    Vue pour accéder aux projets avec les problèmes et les contributeurs.
    """
    serializer_class = ProjectSerializerFull
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Project.objects.select_related('author').prefetch_related('issues', 'contributors__user')
