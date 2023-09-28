from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model

# Sérialiseur pour le profil utilisateur avec validation de l'âge
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
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
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'user_profile')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe déjà.")
        return value

    def create(self, validated_data):
        user_profile_data = validated_data.pop('user_profile', {})
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        get_user_model().objects.create(user=user, **user_profile_data)
        return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Le mot de passe doit contenir au moins 8 caractères.')
        return value
    
