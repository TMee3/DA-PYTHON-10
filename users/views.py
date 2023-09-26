from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from API_IssueTrackingSystem.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .serializers import UsersSerializer


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

    @action(detail=False, methods=['DELETE'])
    def forget_me(self, request):
        """Supprimer l'utilisateur et toutes les données associées."""
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
