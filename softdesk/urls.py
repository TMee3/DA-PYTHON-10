from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import UserCreate , UserDelete
from project.views import (
    ProjectCreateAndList, ProjectDetail,
    ContributorCreateandList, ContributorDetail,
    IssueCreateAndList, IssueDetail,
    CommentCreateAndList, CommentDetail
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentification
    path('api/signup/', UserCreate.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Gestion des projets
    path('api/project/', ProjectCreateAndList.as_view(), name='create_list_project'),
    path('api/project/<int:project_pk>/', ProjectDetail.as_view(), name='detail_project'),

    # Gestion des contributeurs d'un projet
    path('api/project/<int:project_pk>/user/', ContributorCreateandList.as_view(), name='create_list_contributor'),
    path('api/project/<int:project_pk>/user/<int:contributor_pk>/', ContributorDetail.as_view(), name='detail_contributor'),

    # Gestion des problèmes (issues) d'un projet
    path('api/project/<int:project_pk>/issue/', IssueCreateAndList.as_view(), name='create_list_issue'),
    path('api/project/<int:project_pk>/issue/<int:issue_pk>/', IssueDetail.as_view(), name='detail_issue'),

    # Gestion des commentaires sur un problème
    path('api/project/<int:project_pk>/issue/<int:issue_pk>/comment/', CommentCreateAndList.as_view(), name='create_list_comment'),
    path('api/project/<int:project_pk>/issue/<int:issue_pk>/comment/<int:comment_pk>/', CommentDetail.as_view(), name='create_list_comment'),

    # Suprimer son compte
    path('api/user/delete/', UserDelete.as_view(), name='delete_user'),

    # Swagger documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
