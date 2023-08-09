from django.contrib import admin
from API_IssueTrackingSystem.models import Comment, Contributor, Project, Issue


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Contributor)
class ContributorsAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    pass


@admin.register(Issue)
class IssuesAdmin(admin.ModelAdmin):
    pass
