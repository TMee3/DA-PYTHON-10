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


    

class UserDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "Votre compte a bien été supprimé."}, status=status.HTTP_200_OK)

