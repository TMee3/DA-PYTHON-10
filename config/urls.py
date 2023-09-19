

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from API_IssueTrackingSystem.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet, UserViewSet, UserDataViewSet


# API URLs

# RGPD URLs
user_data_viewset = UserDataViewSet.as_view({
    'get': 'retrieve',
    'delete': 'forget_me'
})
user_data_export_view = UserDataViewSet.as_view({
    'get': 'export_data'
})



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
    path('user_data/', user_data_viewset, name='user_data'),
    path('user_data/export/', user_data_export_view, name='user_data_export'),
    path('user_data/forget_me/', user_data_viewset, name='forget_me')
    
    

]
