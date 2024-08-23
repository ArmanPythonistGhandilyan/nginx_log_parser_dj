from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from logs.views import NginxLogViewSet
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"logs", NginxLogViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Nginx Log API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@nginx.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"nginxlogs", NginxLogViewSet, basename="nginxlog")

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", include(router.urls)),
]
