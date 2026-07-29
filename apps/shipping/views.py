from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ShippingAddress
from .serializers import ShippingAddressSerializer


class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(
            user=self.request.user  # Current user addresses
        )

    def perform_create(self, serializer):
        if serializer.validated_data.get("is_default"):  # Default selected
            ShippingAddress.objects.filter(
                user=self.request.user,
                is_default=True
            ).update(
                is_default=False  # Remove old default
            )

        serializer.save(
            user=self.request.user  # Save current user
        )



# Update Default Address
    def perform_update(self, serializer):
        if serializer.validated_data.get("is_default"):  # Update default
            ShippingAddress.objects.filter(
                user=self.request.user,
                is_default=True
            ).exclude(
                pk=serializer.instance.pk  # Exclude current address
            ).update(
                is_default=False  # Remove old default
            )

        serializer.save()  # Save changes




# set default address
    @action(detail=True, methods=["post"])  # Custom POST API
    def set_default(self, request, pk=None):
        ShippingAddress.objects.filter(
            user=request.user,
            is_default=True
        ).update(
            is_default=False  # Remove old default
        )

        address = self.get_object()  # Get selected address
        address.is_default = True    # Make default
        address.save()               # Save address

        return Response({
            "message": "Default Address Updated"  # Success message
        })



# default address

    @action(detail=False, methods=["get"])  # Custom GET API
    def default(self, request):
        address = ShippingAddress.objects.filter(
            user=request.user,
            is_default=True
        ).first()  # Get default address

        if not address:
            return Response({
                "message": "No Default Address"  # No address found
            })

        return Response(
            ShippingAddressSerializer(address).data  # Return address
        )