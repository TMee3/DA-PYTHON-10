from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UserCreate(generics.CreateAPIView):
    """
    Vue pour la création d'utilisateurs via API.
    """

    queryset = User.objects.all()  # Récupération de tous les utilisateurs (non utilisé ici)
    serializer_class = UserSerializer  # Utilisation du sérialiseur pour la création d'utilisateurs

    def perform_create(self, serializer):
        """Sauvegarde de l'utilisateur nouvellement créé."""
        serializer.save()

    

class UserDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:  # Check if the user is authenticated
            user.delete()
            # reutrn a success message if the user is deleted
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)