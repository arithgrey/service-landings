from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LandingTemplateViewSet, LandingViewSet

router = DefaultRouter()
router.register(r'templates', LandingTemplateViewSet)
router.register(r'pages', LandingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
