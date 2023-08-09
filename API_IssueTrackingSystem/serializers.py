from rest_framework import serializers
from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from django.contrib.auth.models import User

# Serializer pour les commentaires
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# Serializer pour les problèmes (issues)
class IssueSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)  # Utilisation de PrimaryKeyRelatedField

    class Meta:
        model = Issue
        fields = ['id', 'title', 'project']
        
# Serializer pour les contributeurs
class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Utilisation de StringRelatedField pour l'affichage
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']

# Serializer pour les projets sans détails associés
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title']
        extra_kwargs = {'author': {'read_only': True}}

# Serializer pour les projets avec détails associés (problèmes et contributeurs)
class ProjectSerializerFull(serializers.ModelSerializer):
    issues = IssueSerializer(many=True, read_only=True)
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'issues', 'contributors']

# Serializer pour les utilisateurs
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
