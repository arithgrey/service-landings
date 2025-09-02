from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.landing.views import LandingTemplateViewSet, ProductLandingViewSet
from django.http import JsonResponse
from django.db import connection
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'templates', LandingTemplateViewSet)
router.register(r'product-landings', ProductLandingViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Service Landings API",
        default_version='v1',
        description="API para gestión de plantillas y landings de productos",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def health_view(request):
    return JsonResponse({"status": "ok"}, status=200)


def liveness_view(request):
    return JsonResponse({"status": "alive"}, status=200)


def readiness_view(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse({"status": "ready"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "not ready", "error": str(e)}, status=503)


urlpatterns = [
    path('api/landings/', include(router.urls)),
    path('health', health_view),
    path('liveness', liveness_view),
    path('readiness', readiness_view),
    # Swagger/OpenAPI
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
