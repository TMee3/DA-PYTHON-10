from .permissions import IsContributor, IsAuthorOrReadOnly
from rest_framework import generics, exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from API_IssueTrackingSystem.serializers import ProjectSerializer, ProjectSerializerFull, ContributorSerializer, IssueSerializer, CommentSerializer, UsersSerializer

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    serializer_class_full = ProjectSerializerFull
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user).distinct()

    def perform_create(self, serializer):
        if Project.objects.filter(title=serializer.validated_data['title']).exists():
            raise exceptions.ValidationError("A project with this title already exists.")
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project, role='auteur')

class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Contributor.objects.select_related('project', 'user').filter(project__contributor__user=self.request.user)

    def perform_create(self, serializer):
        user = serializer.validated_data['user']
        project = serializer.validated_data['project']
        role = serializer.validated_data.get('role', '')
        if role not in ['auteur', 'contributeur']:
            raise exceptions.ValidationError("Invalid role for contributor.")
        if Contributor.objects.filter(user=user, project=project).exists():
            raise exceptions.ValidationError("This user is already a contributor for the project.")
        serializer.save()

class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Issue.objects.select_related('project', 'assigned_to').filter(project__contributor__user=self.request.user)

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        
        # Validate that the project specified exists and current user has access to it
        if not Project.objects.filter(id=project_id, contributor__user=self.request.user).exists():
            raise exceptions.ValidationError("The specified project does not exist or you do not have access to it.")
        
        # Validate that the issue title is unique for the given project
        issue_title = serializer.validated_data['title']
        if Issue.objects.filter(title=issue_title, project_id=project_id).exists():
            raise exceptions.ValidationError("An issue with this title already exists for the specified project.")
        
        # Validate that the assigned_to user (if provided) is a contributor or owner of the project
        assigned_to = self.request.data.get('assigned_to')
        if assigned_to:
            is_contributor_or_owner = Contributor.objects.filter(user_id=assigned_to, project_id=project_id).exists()
            if not is_contributor_or_owner:
                raise exceptions.ValidationError("Assigned user must be a contributor or owner of the project.")
        
        serializer.save(author=self.request.user)

class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.select_related('issue').filter(issue__project__contributor__user=self.request.user)

    def perform_create(self, serializer):
        comment = serializer.validated_data.get('description', '').strip()
        if not comment:
            raise exceptions.ValidationError("Comment cannot be empty.")
        serializer.save(author=self.request.user)

class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
