from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from django.contrib.auth.models import User
from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from API_IssueTrackingSystem.serializers import (
    ProjectSerializer, ProjectSerializerFull, ContributorSerializer,
    IssueSerializer, CommentSerializer, UsersSerializer
)

# Permission personnalisée
class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    serializer_class_full = ProjectSerializerFull
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_class_full
        return super().get_serializer_class()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project, role='auteur')

class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Contributor.objects.filter(project__author=self.request.user)

class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'tag', 'priority', 'status']

    def get_queryset(self):
        return Issue.objects.filter(project__author=self.request.user)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['description']

    def get_queryset(self):
        return Comment.objects.filter(issue__project__author=self.request.user)

class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializerFull  # Utilisation de la version complète pour inclure les problèmes et les contributeurs
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.select_related('author').prefetch_related('issues', 'contributors__user')