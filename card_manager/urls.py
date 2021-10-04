from django.urls import path, include, re_path
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.views.decorators.csrf import csrf_exempt
from graphene_sentry.views import SentryGraphQLView

schema_view = get_schema_view(
    openapi.Info(
        title="card_manager",
        description="Behold My Awesome Project!",
        default_version='v1'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Rota de autenticação (gerar token)
decorated_auth_view = swagger_auto_schema(
    method='post',
    request_body=AuthTokenSerializer,
    responses={200},
)(views.obtain_auth_token)

urlpatterns = [
    # Docs
    re_path(
        r'^(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        '',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'docs/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
    # API
    path("rest-auth/", include("rest_framework.urls")),
    path('api/', include('core.urls'), name='core'),
    # GRAPHQL
    path('graphql/', csrf_exempt(SentryGraphQLView.as_view(graphiql=True))),
]
