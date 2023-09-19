from django.conf import settings
from django.db import models


# Constants for choices
PRIORITY_CHOICES = [
    ('faible', 'faible'),
    ('moyenne', 'moyenne'),
    ('élevé', 'élevé')
]

PROJECT_TYPE_CHOICES = [
    ('back_end', 'back_end'),
    ('front_end', 'front_end'),
    ('IOS', 'IOS'),
    ('Android', 'Android')
]

CONTRIBUTOR_ROLE_CHOICES = [
    ('auteur', 'auteur'),
    ('collaborateur', 'collaborateur')
]

ISSUE_TAG_CHOICES = [
    ('bug', 'bug'),
    ('amélioration', 'amélioration'),
    ('tâche', 'tâche')
]

ISSUE_STATUS_CHOICES = [
    ('en attende', 'en attende'),
    ('en cours', 'en cours'),
    ('terminé', 'terminé')
]

class UserProfile(models.Model):
    """Model representing user's additional profile information."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

class Project(models.Model):
    """Model representing a project."""
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Contributor(models.Model):
    """Model representing a contributor of a project."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=CONTRIBUTOR_ROLE_CHOICES)

    class Meta:
        unique_together = ('project', 'user')

class Issue(models.Model):
    """Model representing an issue related to a project."""
    title = models.CharField(max_length=50)
    description = models.TextField()
    tag = models.CharField(max_length=50, choices=ISSUE_TAG_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ISSUE_STATUS_CHOICES)
    assigned_to = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """Model representing a comment on an issue."""
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
