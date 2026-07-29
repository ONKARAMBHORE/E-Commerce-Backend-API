from decimal import Decimal
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Coupon
from .serializers import CouponSerializer
from apps.cart.models import Cart
from apps.accounts.permissions import IsAdmin



# coupon crud
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(detail=False, methods=["post"])  # Custom POST API
    def apply(self, request):
        code = request.data.get("code")  # Get coupon code

        coupon = Coupon.objects.filter(
            code=code,
            is_active=True
        ).first()  # Find active coupon

        if not coupon:
            raise ValidationError({"detail": "Invalid Coupon"})  # Invalid coupon

        now = timezone.now()  # Current time

        if not (coupon.valid_from <= now <= coupon.valid_to):
            raise ValidationError({"detail": "Coupon Expired"})  # Check expiry

        cart_items = Cart.objects.filter(user=request.user)  # User cart

        total = sum(item.subtotal for item in cart_items)  # Cart total

        if total < coupon.minimum_amount:
            raise ValidationError({"detail": "Minimum Amount Not Reached"})  # Min amount check

        for item in cart_items:
            item.coupon = coupon  # Apply coupon
            item.save()  # Save changes

        discount = (total * coupon.discount) / Decimal("100")  # Calculate discount

        return Response({
            "coupon": coupon.code,                # Coupon code
            "discount": discount,                 # Discount amount
            "final_amount": total - discount      # Final amount
        })







    @action(detail=False, methods=["delete"])  # Custom DELETE API
    def remove(self, request):
        Cart.objects.filter(user=request.user).update(
        coupon=None  # Remove coupon
        )

        return Response({
            "message": "Coupon Removed"  # Success message
        })