from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Software engineering lab",
        default_version="v1",
        description="API documentation for the lab",
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
path('admin/', admin.site.urls),
path('', include('myapp.urls')),
path('api/token/', TokenObtainPairView.as_view(),
name='token_obtain_pair'),
path('api/token/refresh/', TokenRefreshView.as_view(),
name='token_refresh'),
path('swagger/', schema_view.with_ui('swagger',
cache_timeout=0), name='schema-swagger-ui'),

]


