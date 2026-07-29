from rest_framework.routers import DefaultRouter
from .views import CouponViewSet

router = DefaultRouter()
router.register("", CouponViewSet, basename="coupon")  # Register API

urlpatterns = router.urls     # Generate URLs