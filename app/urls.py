from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.landing.views import LandingTemplateViewSet, ProductLandingViewSet

router = DefaultRouter()
router.register(r'templates', LandingTemplateViewSet)
router.register(r'product-landings', ProductLandingViewSet)

urlpatterns = [
    path('api/landings/', include(router.urls)),
]
