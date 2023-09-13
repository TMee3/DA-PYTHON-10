
from .permissions import IsContributor, IsAuthorOrReadOnly

from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response

from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from API_IssueTrackingSystem.serializers import ProjectSerializer, ProjectSerializerFull,\
    ContributorSerializer, IssueSerializer, CommentSerializer, UsersSerializer


class ProjectViewSet(ModelViewSet):
    """Viewset to handle CRUD operations for projects."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    serializer_class_full = ProjectSerializerFull

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_class_full
        return super().get_serializer_class()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        contributor = Contributor(user=self.request.user, project=project, role= 'auteur' )
        contributor.save()


class ContributorViewSet(ModelViewSet):
    """Viewset to handle CRUD operations for project contributors."""
    serializer_class = ContributorSerializer
    permissions_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        contributors = Contributor.objects.filter(project=self.kwargs.get('project_pk'))
        return contributors


class IssueViewSet(ModelViewSet):
    """Viewset to handle CRUD operations for project issues."""
    serializer_class = IssueSerializer
    permissions_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Issue.objects.filter(project=self.kwargs.get('project_pk'))
        return queryset


class CommentViewSet(ModelViewSet):
    """Viewset to handle CRUD operations for issue comments."""
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    


class UserViewSet(generics.CreateAPIView):
    """View to handle user creation."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer



