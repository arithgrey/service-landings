from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.landing.views import LandingTemplateViewSet, ProductLandingViewSet
from django.http import JsonResponse
from django.db import connection

router = DefaultRouter()
router.register(r'templates', LandingTemplateViewSet)
router.register(r'product-landings', ProductLandingViewSet)


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
]
