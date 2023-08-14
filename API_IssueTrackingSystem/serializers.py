from rest_framework import serializers
from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'project']
        depth = 1

class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title']
        extra_kwargs = {'author': {'read_only': True}}

class ProjectSerializerFull(ProjectSerializer):
    issues = IssueSerializer(many=True, read_only=True)
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['description', 'type', 'author', 'issues', 'contributors']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = super(UsersSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
