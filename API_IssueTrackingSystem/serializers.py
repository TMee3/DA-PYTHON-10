from rest_framework import serializers
from API_IssueTrackingSystem.models import Project, Contributor, Issue, Comment
from django.utils import timezone
from django.contrib.auth import get_user_model



# Sérialiseur de base pour les tâches (issues)
class IssueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Issue
        fields = '__all__'
   
    def get_fields(self):
        fields = super().get_fields()
        fields['project'].queryset = Project.objects.filter(contributor__user=self.context['request'].user)
        return fields
 
    def validate_project(self, value):
        user = self.context['request'].user
        if not Contributor.objects.filter(user=user, project=value).exists():
            raise serializers.ValidationError("Vous n'avez pas accès à ce projet ou il n'existe pas.")
        return value
    
    def validate(self, data):
        if Issue.objects.filter(title=data['title'], project=data['project']).exists():
            raise serializers.ValidationError("Une tâche avec ce titre existe déjà pour ce projet.")
        return data
    
    # Valider que l'utilisateur assigné est un contributeur ou un propriétaire du projet et afficher uniquement les contributeurs et les propriétaires
    def validate_assigned_to(self, value):
        project = self.context['request'].data.get('project')
        if project:
            is_contributor_or_owner = Contributor.objects.filter(user_id=value, project_id=project).exists()
            if not is_contributor_or_owner:
                raise serializers.ValidationError("L'utilisateur assigné doit être un contributeur ou un propriétaire du projet.")
        else:
            raise serializers.ValidationError("Le projet doit être spécifié.")
        return value

# Sérialiseur de base pour les commentaires
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True}
        }
    
    # Afficher uniquement les tâches auxquelles l'utilisateur a accès
    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields['issue'].queryset = Issue.objects.filter(project__contributor__user=self.context['request'].user)
        return fields

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
        extra_kwargs = {'author': {'read_only': True}}


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'
        extra_kwargs = {
            'role': {'required': True},
            'user': {'required': True},
            'project': {'required': True}
        }

    # Afficher uniquement les projets auxquels l'utilisateur a accès et les utilisateurs qui ne sont pas déjà contributeurs
    def get_fields(self):
        fields = super(ContributorSerializer, self).get_fields()
        fields['project'].queryset = Project.objects.filter(contributor__user=self.context['request'].user)
        fields['user'].queryset = get_user_model().objects.exclude(contributor__project__contributor__user=self.context['request'].user)
        return fields
