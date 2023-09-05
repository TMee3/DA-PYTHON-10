from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User

class UserCreate(generics.CreateAPIView):
    """
    Vue pour la création d'utilisateurs via API.
    """

    queryset = User.objects.all()  # Récupération de tous les utilisateurs (non utilisé ici)
    serializer_class = UserSerializer  # Utilisation du sérialiseur pour la création d'utilisateurs
