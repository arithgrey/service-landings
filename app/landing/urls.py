from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LandingTemplateViewSet, LandingViewSet, ProductLandingViewSet

router = DefaultRouter()
router.register(r"templates", LandingTemplateViewSet)
router.register(r"pages", LandingViewSet)
router.register(r"product-landings", ProductLandingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
