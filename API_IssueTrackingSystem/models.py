from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

class Project(models.Model):
    """Model representing a project."""
    title = models.CharField(max_length=50)
    description = models.TextField()
    choices_priority = [('back_end', 'back_end'), ('front_end', 'front_end'), ('IOS', 'IOS'), ('Android', 'Android')]
    type = models.CharField(max_length=50, choices=choices_priority)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Contributor(models.Model):
    """Model representing a contributor of a project."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    choices = [('auteur', 'auteur'), ('collaborateur', 'collaborateur')]
    role = models.CharField(max_length=50, choices=choices)

    class Meta:
        unique_together = ('project', 'user')

class Issue(models.Model):
    """Model representing an issue related to a project."""
    title = models.CharField(max_length=50)
    description = models.TextField()
    choices_tag = [('bug', 'bug'), ('amélioration', 'amélioration'), ('tâche', 'tâche')]
    tag = models.CharField(max_length=50, choices=choices_tag)
    choices_priority = [('faible', 'faible'), ('moyenne', 'moyenne'), ('élevé', 'élevé')]
    priority = models.CharField(max_length=50, choices=choices_priority)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    choices_status = [('en attende', 'en attende'), ('en cours', 'en cours'), ('terminé', 'terminé')]
    status = models.CharField(max_length=50, choices=choices_status)
    assigned_to = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """Model representing a comment on an issue."""
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
