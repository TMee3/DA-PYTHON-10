from rest_framework import serializers

from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from django.contrib.auth.models import User
import datetime



class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProjectSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author']
        extra_kwargs = {'author': {'read_only': True}}


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'author']
        extra_kwargs = {'author': {'read_only': True}}



class UsersSerializer(serializers.ModelSerializer):
    # Explicitly specifying the fields for the serializer
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'can_be_contacted', 'can_data_be_shared', 'birth_date', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'birth_date': {'write_only': True, 'required': True},
        }

    # Overriding the create method to check for age
    def create(self, validated_data):
        birth_date = validated_data.get('birth_date', None)
        if birth_date:
            today = datetime.date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 15:
                raise serializers.ValidationError('User must be 15 years or older.')
        return super(UsersSerializer, self).create(validated_data)

    # Verify that the password is at least 8 characters long
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        return value

    # Hash the password before saving the user
    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.set_password(user.password)
        user.save()
        return user
 


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']
