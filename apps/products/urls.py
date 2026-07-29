from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

router.register("categories", CategoryViewSet)

router.register("brand", BrandViewSet)

router.register("products", ProductViewSet)

router.register("images", ProductImageViewSet)

urlpatterns = router.urls