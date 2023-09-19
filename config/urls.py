

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from API_IssueTrackingSystem.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('issues', IssueViewSet, basename='issue')
router.register('contributor', ContributorViewSet, basename='contributor')
router.register('comments', CommentViewSet, basename='comment')

router.register('projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', UserViewSet.as_view(), name='users'),
    path('login/', TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_tokens'),
    path('', include(router.urls)),
    
    

]
