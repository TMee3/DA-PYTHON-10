from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    # Choix pour le champ "type" du projet
    class Type(models.TextChoices):
        BACK_END = "Back-end"
        FRONT_END = "Front-end"
        IOS = "IOS"
        ANDROID = "Android"

    title = models.fields.CharField(max_length=100)
    description = models.fields.CharField(max_length=5000, blank=True)
    type = models.fields.CharField(choices=Type.choices, max_length=15, default="Back-end")
    
    # Relation ManyToManyField pour les contributeurs
    contributor = models.ManyToManyField(User, through="Contributor", related_name="project_contributor")
    
    # Relation ForeignKey pour l'auteur du projet
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_author")

class Contributor(models.Model):
    # Choix pour le champ "permission" du contributeur
    class Permission(models.TextChoices):
        ADMIN = "Admin"
        LIST = "list"
        DELETE = "Delete"
        UPDATE = "Update"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributor_user", null=False, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributor_project", null=False, blank=False)
    permission = models.fields.CharField(choices=Permission.choices, max_length=15, default="Admin")
    role = models.fields.CharField(max_length=50, null=False, blank=False)
    
    class Meta:
        unique_together = ('user', 'project')  # Contrainte unique pour éviter les doublons

class Issue(models.Model):
    # Choix pour les champs "priority", "tag" et "status" des problèmes
    class Priority(models.TextChoices):
        LOW = "Low"
        MEDIUM = "Medium"
        HIGH = "HIGH"

    class Tag(models.TextChoices):
        BUG = "Bug"
        IMPROVEMENT = "Improuvement"
        TASK = "Task"

    class Status(models.TextChoices):
        TO_DO = "To do"
        WIP = "Work in process"
        Done = "Done"

    title = models.fields.CharField(max_length=100)
    description = models.fields.CharField(max_length=5000, blank=True)
    tag = models.fields.CharField(choices=Tag.choices, max_length=15, default="Bug")
    priority = models.fields.CharField(choices=Priority.choices, max_length=10, default="Low")
    status = models.fields.CharField(choices=Status.choices, max_length=50, default="To do")
    creation_date = models.fields.DateTimeField(auto_now_add=True)
    
    # Relation ForeignKey pour le projet et l'auteur du problème
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issue_project")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issue_author")
    
    # Relation ForeignKey pour l'utilisateur assigné au problème
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee")

class Comment(models.Model):
    description = models.fields.CharField(max_length=5000)
    creation_date = models.fields.DateTimeField(auto_now_add=True)
    
    # Relation ForeignKey pour le problème et l'auteur du commentaire
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comment_issue")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
