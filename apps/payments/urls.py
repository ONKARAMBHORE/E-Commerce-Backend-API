from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, webhook

router = DefaultRouter()
router.register("", PaymentViewSet, basename="payments")

urlpatterns = router.urls + [
    path("webhook/", webhook)
]