from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from API_IssueTrackingSystem.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet, UserViewSet


# Routeur principal
router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')

# Routeurs imbriqués pour les vues basées sur IssueViewSet et ContributorViewSet
project_nested_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
project_nested_router.register(r'issues', IssueViewSet, basename='project-issues')
project_nested_router.register(r'users', ContributorViewSet, basename='project-users')

# Routeur imbriqué pour les vues basées sur CommentViewSet
issue_nested_router = routers.NestedDefaultRouter(project_nested_router, r'issues', lookup='issue')
issue_nested_router.register(r'comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserViewSet.as_view(), name='users'),
    path('login/', TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_tokens'),
    path('', include(router.urls)),
    path('', include(project_nested_router.urls)),
    path('', include(issue_nested_router.urls)),
]
