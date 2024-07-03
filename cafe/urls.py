from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cafe.views import (
    CafeViewSet,
    CafeLunchMenuViewSet,
)


router = DefaultRouter()

router.register('cafes', CafeViewSet)
router.register('lunches', CafeLunchMenuViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "cafe"
