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


class ProjectViewSet(viewsets.ModelViewSet):
    """Viewset for CRUD operations on Project model."""
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user).distinct()

    def perform_create(self, serializer):
        if Project.objects.filter(title=serializer.validated_data['title']).exists():
            raise exceptions.ValidationError("A project with this title already exists.")
        serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=serializer.instance, role='auteur')

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
            raise exceptions.ValidationError("Invalid role for contributor.")
        if Contributor.objects.filter(user=user, project=project).exists():
            raise exceptions.ValidationError("This user is already a contributor for the project.")
        serializer.save()

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Issue.objects.select_related('project', 'assigned_to').filter(project__contributor__user=self.request.user)

    # Show only projects that the user has access to
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'].user = self.request.user
        return context
    
    # Validate that the project exists and that the user has access to it
    def validate_project(self, value):
        user = self.request.user
        if not Contributor.objects.filter(user=user, project=value).exists():
            raise exceptions.ValidationError("The specified project does not exist or you do not have access to it.")
        return value
    
    # Show only assigned users that are contributors or owners of the project
    def get_fields(self):
        fields = super().get_fields()
        fields['project'].queryset = Project.objects.filter(contributor__user=self.request.user)
        fields['assigned_to'].queryset = Contributor.objects.filter(project__contributor__user=self.request.user)
        return fields
    
    # Validate that the assigned user is a contributor or owner of the project
    def validate_assigned_to(self, value):
        project = self.request.data.get('project')
        if project:
            is_contributor_or_owner = Contributor.objects.filter(user_id=value, project_id=project).exists()
            if not is_contributor_or_owner:
                raise exceptions.ValidationError("Assigned user must be a contributor or owner of the project.")
        else:
            raise exceptions.ValidationError("The project must be specified.")
        return value
    
    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        if not Project.objects.filter(id=project_id, contributor__user=self.request.user).exists():
            raise exceptions.ValidationError("The specified project does not exist or you do not have access to it.")
        issue_title = serializer.validated_data['title']
        if Issue.objects.filter(title=issue_title, project_id=project_id).exists():
            raise exceptions.ValidationError("An issue with this title already exists for the specified project.")
        assigned_to = self.request.data.get('assigned_to')
        if assigned_to:
            is_contributor_or_owner = Contributor.objects.filter(user_id=assigned_to, project_id=project_id).exists()
            if not is_contributor_or_owner:
                raise exceptions.ValidationError("Assigned user must be a contributor or owner of the project.")
        serializer.save()

class CommentViewSet(viewsets.ModelViewSet):
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


class UserDataViewSet(viewsets.ViewSet):
    """ViewSet for user's RGPD rights."""
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        """Retrieve user data."""
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "projects": [project.title for project in Project.objects.filter(contributor__user=request.user)],
            "issues": [issue.title for issue in Issue.objects.filter(project__contributor__user=request.user)],
            "comments": [comment.description for comment in Comment.objects.filter(issue__project__contributor__user=request.user)],
            "contributors": [contributor.user.username for contributor in Contributor.objects.filter(project__contributor__user=request.user)]
        }
        return Response(user_data)

    @action(detail=False, methods=['GET'])
    def export_data(self, request):
        """Export user data in JSON format."""
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "projects": [project.title for project in Project.objects.filter(contributor__user=request.user)],
            "issues": [issue.title for issue in Issue.objects.filter(project__contributor__user=request.user)],
            "comments": [comment.description for comment in Comment.objects.filter(issue__project__contributor__user=request.user)],
            "contributors": [contributor.user.username for contributor in Contributor.objects.filter(project__contributor__user=request.user)]
        }
        return JsonResponse(user_data)

    @action(detail=False, methods=['DELETE'])
    def forget_me(self, request):
        """Delete user and all associated data."""
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
