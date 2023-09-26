from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import UserProfile
from django.utils import timezone

# Sérialiseur pour le profil utilisateur avec validation de l'âge
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('can_be_contacted', 'can_data_be_shared', 'birth_date')

    def validate_birth_date(self, value):
        if value is None:
            raise serializers.ValidationError('La date de naissance est requise.')

        today = timezone.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError('L\'utilisateur doit avoir au moins 15 ans.')
        return value

# Sérialiseur pour les utilisateurs avec profil intégré
class UsersSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_profile')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe déjà.")
        return value

    def create(self, validated_data):
        user_profile_data = validated_data.pop('user_profile', {})
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        UserProfile.objects.create(user=user, **user_profile_data)
        return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Le mot de passe doit contenir au moins 8 caractères.')
        return value
    
