from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .models import Project, Contributor, User, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import ProjectPermission, ContributorPermission, IssuePermission, CommentPermission
from rest_framework.generics import get_object_or_404


class ProjectCreateAndList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    """
    Méthode création de projet ➡ POST
    Permission ➡ N'importe quel utilisateur connecté
    """
    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Méthode affichage de tous les projets rattachés à l'utilisateur connecté ➡ GET
    Permission ➡ Auteur et Contributeur
    """
    def get(self, request):
        user = request.user
        projects = Project.objects.filter(author=user) | Project.objects.filter(contributor=user)

        if projects:
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({"message": "Aucun projet relié à cet utilisateur."}, status=status.HTTP_404_NOT_FOUND)


class ProjectDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, ProjectPermission]

    def get_project(self, project_pk):
        try:
            return Project.objects.get(id=project_pk)
        except Project.DoesNotExist:
            raise Http404()

    """
    Méthode affichage de tous les détails d'un projet ➡ GET
    Permission ➡ N'importe quel utilisateur connecté
    """
    def get(self, request, project_pk):
        project = self.get_project(project_pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Méthode de mise à jour d'un projet ➡ PUT
    Permission ➡ Auteur uniquement
    """
    def put(self, request, project_pk):
        project = self.get_project(project_pk)

        data = request.data.copy()
        data['author'] = request.user.id

        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    """
    Méthode de suppression d'un projet ➡ DELETE
    Permission ➡ Auteur uniquement
    """
    def delete(self, request, project_pk):
        project = self.get_project(project_pk)
        project.delete()
        return Response({"message": "Le projet à bien été supprimé."}, status=status.HTTP_204_NO_CONTENT)


class ContributorCreateandList(APIView):

    permission_classes = [permissions.IsAuthenticated, ContributorPermission]

    """
    Méthode affichage de tous les contributeurs rattachés à un projet ➡ GET
    Permission ➡ N'importe quel utilisateur connecté
    """
    def get(self, request, project_pk):
        project = get_object_or_404(Project, id=project_pk)
        contributor = Contributor.objects.filter(project=project)
        serializer = ContributorSerializer(contributor, many=True)
        return Response(serializer.data)

    """
    Méthode d'ajout d'un contributeur à un projet ➡ POST
    Permission ➡ Auteur uniquement
    """
    def post(self, request, project_pk):
        project = get_object_or_404(Project, id=project_pk)
        data = request.data
        data['project'] = project.id
        try:
            print(request.data)
            Contributor.objects.get(user=data['user'], project=project.id)
            return Response({"message": "Ce contributeur existe déjà !"}, status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            try:
                User.objects.get(id=data['user'])
                serializer = ContributorSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message": "Cet utilisateur est introuvable !"}, status=status.HTTP_404_NOT_FOUND)


class ContributorDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, ContributorPermission]

    """
    Méthode de suppression d'un contributeur à un projet ➡ DELETE
    Permission ➡ Auteur uniquement
    """
    def delete(self, request, project_pk, contributor_pk):
        contributor = get_object_or_404(Contributor, id=contributor_pk)
        contributor.delete()
        return Response({"message": "Le contributeur à bien été supprimé"}, status=status.HTTP_204_NO_CONTENT)


class IssueCreateAndList(APIView):

    permission_classes = [permissions.IsAuthenticated, IssuePermission]

    """
    Méthode d'affichage des problèmes d'un projet ➡ GET
    Permission ➡ Auteur et Contributeur
    """
    def get(self, request, project_pk):
        project = get_object_or_404(Project, id=project_pk)
        issue = Issue.objects.filter(project=project)
        serializer = IssueSerializer(issue, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Méthode de création d'un problème dans un projet ➡ POST
    Permission ➡ Auteur et Contributeur
    """
    def post(self, request, project_pk):
        data = request.data.copy()
        data['author'] = request.user.id
        data['project'] = project_pk

        serializer = IssueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, IssuePermission]

    """
    Méthode d'actualisation d'un problème dans un projet ➡ PUT
    Permission ➡ Auteur uniquement
    """
    def put(self, request, project_pk, issue_pk):
        issue = get_object_or_404(Issue, id=issue_pk)
        data = request.data.copy()
        data['author'] = request.user.id
        data['project'] = project_pk

        serializer = IssueSerializer(issue, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    """
    Méthode de suppression d'un problème dans un projet ➡ DELETE
    Permission ➡ Auteur uniquement
    """
    def delete(self, request, project_pk, issue_pk):
        issue = get_object_or_404(Issue, id=issue_pk)
        issue.delete()
        return Response({"message": "Problème supprimé !"}, status=status.HTTP_204_NO_CONTENT)


class CommentCreateAndList(APIView):

    permission_classes = [permissions.IsAuthenticated, CommentPermission]

    """
    Méthode de création d'un commentaire à un problème ➡ POST
    Permission ➡ Auteur et Contributeur
    """
    def post(self, request, project_pk, issue_pk):
        data = request.data.copy()
        data['author'] = request.user.id
        data['project'] = project_pk
        data['issue'] = issue_pk

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Méthode d'affichage de tous les commentaires d'un problème ➡ GET
    Permission ➡ Auteur et Contributeur
    """
    def get(self, request, project_pk, issue_pk):
        issue = get_object_or_404(Issue, id=issue_pk)
        comment = Comment.objects.filter(issue=issue)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, CommentPermission]

    """
    Méthode d'affichage d'un commentaire d'un problème ➡ GET
    Permission ➡ Auteur et Contributeur
    """
    def get(self, request, project_pk, issue_pk, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Méthode d'actualisation  d'un commentaire d'un problème ➡ PUT
    Permission ➡ Auteur et Contributeur
    """
    def put(self, request, project_pk, issue_pk, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)
        data = request.data.copy()
        data['author'] = request.user.id
        data['project'] = project_pk
        data['issue'] = issue_pk

        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Méthode de supression d'un commentaire d'un problème ➡ DELETE
    Permission ➡ Auteur et Contributeur
    """
    def delete(self, request, project_pk, issue_pk, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)
        comment.delete()
        return Response({"message": "Commentaire supprimé ! "}, status=status.HTTP_204_NO_CONTENT)