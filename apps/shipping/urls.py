from rest_framework.routers import DefaultRouter
from .views import ShippingAddressViewSet

router = DefaultRouter()
router.register("", ShippingAddressViewSet, basename="shipping")

urlpatterns = router.urls