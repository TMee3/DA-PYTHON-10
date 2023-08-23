from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
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
    CanManageContributorsPermission, IsAuthorOrReadOnly
)

class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

# Pagination standard pour les vues
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# Vue pour gérer les projets
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    serializer_class_full = ProjectSerializerFull
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']

    # Utiliser IsAuthenticated pour exiger l'authentification pour toutes les actions
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Autoriser les contributeurs à accéder aux projets
        if CanAccessContributorProjects().has_permission(self.request, self):
            return Project.objects.filter(contributors__user=self.request.user)
        else:
            return Project.objects.filter(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_class_full
        return super().get_serializer_class()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project, role='auteur')

    # Appliquer la permission CanManageContributorsPermission pour ajouter/supprimer des contributeurs
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CanManageContributorsPermission]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

# Vue pour gérer les contributeurs
class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Contributor.objects.filter(project__author=self.request.user)

# Vue pour gérer les problèmes
class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'tag', 'priority', 'status']

    # Appliquer la permission CanAccessContributorIssues pour accéder uniquement aux problèmes de projets auxquels l'utilisateur contribue
    def get_queryset(self):
        return Issue.objects.filter(project__contributors__user=self.request.user)

# Vue pour gérer les commentaires
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['description']

    # Appliquer la permission CanAccessContributorComments pour accéder uniquement aux commentaires des problèmes de projets auxquels l'utilisateur contribue
    def get_queryset(self):
        return Comment.objects.filter(issue__project__contributors__user=self.request.user)

# Vue pour créer un utilisateur
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

# Vue pour accéder aux projets avec les problèmes et les contributeurs
class FullProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializerFull
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.select_related('author').prefetch_related('issues', 'contributors__user')
