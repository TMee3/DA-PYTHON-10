from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

PRIORITY_CHOICES = [
    ('back_end', _('Back-end')),
    ('front_end', _('Front-end')),
    ('IOS', _('iOS')),
    ('Android', _('Android'))
]

ROLE_CHOICES = [
    ('auteur', _('Auteur')),
    ('collaborateur', _('Collaborateur'))
]

TAG_CHOICES = [
    ('bug', _('Bug')),
    ('amélioration', _('Amélioration')),
    ('tâche', _('Tâche'))
]

STATUS_CHOICES = [
    ('en_attente', _('En attente')),
    ('en_cours', _('En cours')),
    ('termine', _('Terminé'))
]

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    project_type = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title

class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributions")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributors")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('project', 'user')

class Issue(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    tag = models.CharField(max_length=50, choices=TAG_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reported_issues")
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']  # Tri par date de création
