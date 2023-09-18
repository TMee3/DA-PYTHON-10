from rest_framework import serializers
from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone


# Sérialiseur de base pour les tâches (issues)
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

    def validate_project(self, value):
        user = self.context['request'].user
        if not Contributor.objects.filter(user=user, project=value).exists():
            raise serializers.ValidationError("Vous n'avez pas accès à ce projet ou il n'existe pas.")
        return value

# Sérialiseur de base pour les commentaires
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate_issue(self, value):
        user = self.context['request'].user
        if not Issue.objects.filter(id=value.id, project__contributor__user=user).exists():
            raise serializers.ValidationError("Vous n'avez pas accès à cette tâche ou elle n'existe pas.")
        return value

# Sérialiseurs pour les projets (version complète et simplifiée)
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'author']
        extra_kwargs = {'author': {'read_only': True}}

class ProjectSerializerFull(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        fields = ['id', 'title', 'description', 'type', 'author']

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

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'