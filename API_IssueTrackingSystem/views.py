from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User

from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from API_IssueTrackingSystem.serializers import ProjectSerializer, ProjectSerializerFull,\
    ContributorSerializer, IssueSerializer, CommentSerializer, UsersSerializer

# Définition d'une classe pour la pagination standard
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# Vue pour les opérations CRUD liées aux projets
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    serializer_class_full = ProjectSerializerFull
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']

    # Choix du sérialiseur en fonction de l'action de la vue
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_class_full
        return super().get_serializer_class()

    # Création d'un projet avec un contributeur initial (auteur)
    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        contributor = Contributor(user=self.request.user, project=project, role='auteur')
        contributor.save()
        return Response({"message": "Project created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

# Vue pour les opérations CRUD liées aux contributeurs
class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer

    # Filtrer les contributeurs en fonction du projet donné
    def get_queryset(self):
        contributors = Contributor.objects.filter(project=self.kwargs.get('project_pk'))
        return contributors

    # Récupérer la liste des contributeurs pour un projet
    def list(self, request, *args, **kwargs):
        contributors = self.get_queryset()
        serializer = self.get_serializer(contributors, many=True)
        return Response({"message": "Contributors retrieved successfully", "data": serializer.data})

# Vue pour les opérations CRUD liées aux problèmes (issues)
class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'tag', 'priority', 'status']

    # Filtrer les problèmes en fonction du projet donné
    def get_queryset(self):
        queryset = Issue.objects.filter(project=self.kwargs.get('project_pk'))
        return queryset

    # Récupérer la liste des problèmes pour un projet
    def list(self, request, *args, **kwargs):
        issues = self.get_queryset()
        serializer = self.get_serializer(issues, many=True)
        return Response({"message": "Issues retrieved successfully", "data": serializer.data})

# Vue pour les opérations CRUD liées aux commentaires
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['description']

    # Récupérer la liste des commentaires pour un problème donné
    def list(self, request, *args, **kwargs):
        comments = self.queryset.filter(issue=self.kwargs.get('issue_pk'))
        serializer = self.get_serializer(comments, many=True)
        return Response({"message": "Comments retrieved successfully", "data": serializer.data})

# Vue pour la création d'utilisateurs
class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    # Créer un utilisateur
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
