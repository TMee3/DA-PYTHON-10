from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

# Sérialiseur pour le modèle Project
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'contributor']

# Sérialiseur pour le modèle Contributor
class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role']

# Sérialiseur pour le modèle Issue
class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'project', 'author', 'assignee']

# Sérialiseur pour le modèle Comment
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author']
