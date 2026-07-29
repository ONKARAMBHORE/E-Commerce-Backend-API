import uuid
from decimal import Decimal

from django.db import transaction

from django.db.models.functions import TruncMonth
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.accounts.models import User
from apps.cart.models import Cart
from apps.payments.models import Payment
from apps.products.models import Product
from apps.shipping.models import ShippingAddress

from .models import *
from .serializers import *
from django.utils import timezone

from django.db import transaction
from django.core.mail import send_mail

from apps.notifications.models import Notification
from apps.notifications.utils import send_notification_email


from django.db.models import Sum, Count
from rest_framework.permissions import IsAdminUser



class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).select_related(
            "shipping_address",
            "coupon"
        ).prefetch_related(
            "items",
            "items__product"
        )







    @action(detail=False, methods=["post"])  # Custom POST API
    @transaction.atomic  # Atomic transaction
    def checkout(self, request):

        cart = Cart.objects.filter(
            user=request.user
        ).select_related(
            "product",
            "coupon"
        )  # User cart

        if not cart.exists():
            raise ValidationError({
                "detail": "Cart Empty"  # Empty cart
            })

        address = ShippingAddress.objects.filter(
            user=request.user,
            is_default=True
        ).first()  # Default address

        if not address:
            raise ValidationError({
                "detail": "Default Address Required"  # Address required
            })

        subtotal = Decimal("0")  # Initial subtotal
        discount = Decimal("0")  # Initial discount
        coupon = None            # No coupon

        for item in cart:
            if item.quantity > item.product.stock:
                raise ValidationError({
                    "detail": f"{item.product.name} Out Of Stock"  # Stock check
                })

            subtotal += item.subtotal  # Add subtotal

            if item.coupon:
                coupon = item.coupon  # Save coupon

        if coupon:
            discount = (
                subtotal * coupon.discount
            ) / 100  # Calculate discount

        total = subtotal - discount  # Final amount

        order = Order.objects.create(
            order_number=str(uuid.uuid4())[:10].upper(),  # Unique order ID
            user=request.user,
            shipping_address=address,
            coupon=coupon,
            subtotal=subtotal,
            discount=discount,
            total=total
        )
        send_mail(
            "Order Placed",
            f"Your Order {order.order_number} has been placed successfully.",
            None,
            [request.user.email]
        )

#   Order Confirmation    notification   
        Notification.objects.create(
            user=request.user,
            title="Order Placed",
            message=f"Your order {order.order_number} has been placed successfully."
        )

        send_notification_email(
            "Order Confirmation",
            f"Your order {order.order_number} has been placed successfully.",
        request.user.email
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                subtotal=item.subtotal
            )  # Create order item

            item.product.stock -= item.quantity  # Reduce stock
            item.product.save()                  # Save product

        cart.delete()  # Clear cart

        return Response(
            OrderSerializer(order).data  # Return order
        )





#   cancel order

    @action(detail=True, methods=["post"])  # Cancel order
    @transaction.atomic  # Atomic transaction
    def cancel(self, request, pk=None):
        order = self.get_object()  # Get order

        if order.status in ["Delivered", "Cancelled"]:
            raise ValidationError({
            "detail": "Cannot Cancel"  # Invalid status
        })

        order.status = "Cancelled"  # Update status
        order.save()  # Save order

        for item in order.items.all():
            item.product.stock += item.quantity  # Restore stock
            item.product.save()  # Save product

        return Response({
            "message": "Order Cancelled"  # Success message
        })

# buy now order

    @action(detail=False, methods=["post"])  # Buy now API
    @transaction.atomic  # Atomic transaction
    def buy_now(self, request):
        product = Product.objects.get(
            pk=request.data["product"]  # Get product
        )

        quantity = int(
            request.data.get("quantity", 1)  # Default quantity
        )

        address = ShippingAddress.objects.get(
            user=request.user,
            is_default=True
        )  # Default address

        if quantity > product.stock:
            raise ValidationError({
                "detail": "Out Of Stock"  # Stock check
            })

        subtotal = product.price * quantity  # Calculate total

        order = Order.objects.create(
            order_number=str(uuid.uuid4())[:10].upper(),  # Order ID
            invoice_number=str(uuid.uuid4())[:8].upper(),  # Invoice ID
            user=request.user,
            shipping_address=address,
            subtotal=subtotal,
            total=subtotal
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
            subtotal=subtotal
        )  # Create order item

        product.stock -= quantity  # Reduce stock
        product.save()  # Save product

        return Response(
            OrderSerializer(order).data  # Return order
        )



# update status


    @action(detail=True, methods=["patch"])  # Update status
    def update_status(self, request, pk=None):
        order = self.get_object()  # Get order

        order.status = request.data.get("status")  # New status
        order.save()  # Save status

        return Response(
            OrderSerializer(order).data  # Return updated order
        )


# retuen order 

    @action(detail=True, methods=["post"])  # Return order
    def return_order(self, request, pk=None):
        order = self.get_object()  # Get order

        if order.status != "Delivered":
            raise ValidationError({
                "detail": "Only Delivered Orders Can Be Returned"  # Check delivery
            })

        order.returned = True  # Mark returned
        order.refund_status = "Requested"  # Request refund
        order.save()  # Save order

        return Response({
            "message": "Return Request Submitted"  # Success message
        })


# Refund Approved


    @action(detail=True, methods=["patch"])  # Refund API
    def refund(self, request, pk=None):
        order = self.get_object()  # Get order

        order.refund_status = "Completed"  # Complete refund
        order.save()  # Save order

        return Response({
            "message": "Refund Completed"  # Success message
        })



# invoice 

    @action(detail=True, methods=["get"])  # Invoice API
    def invoice(self, request, pk=None):
        order = self.get_object()  # Get order

        return Response({
            "invoice": order.invoice_number,      # Invoice number
            "order": OrderSerializer(order).data  # Order details
        })





   # Dashboard API
    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def dashboard(self, request):

        return Response({
            "total_orders": Order.objects.count(),
            "total_users": User.objects.count(),
            "total_products": Product.objects.count(),
            "total_revenue": Payment.objects.filter(status="Success").aggregate(total=Sum("amount"))["total"] or 0
    })


# Recent Orders
    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def recent_orders(self, request):

        orders = Order.objects.select_related("user").order_by("-created_at")[:10]

        return Response(OrderSerializer(orders, many=True).data)


# Top Selling Products
    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def top_products(self, request):

        products = Product.objects.annotate(
            sold=Sum("orderitem__quantity")
        ).order_by("-sold")[:10]

        return Response([
            {"id": p.id, "name": p.name, "sold": p.sold or 0}
            for p in products
        ])


# Low Stock
    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def low_stock(self, request):

        products = Product.objects.filter(stock__lt=10)

        return Response([
            {"id": p.id, "name": p.name, "stock": p.stock}
            for p in products
        ])



# Monthly Sales
    from django.db.models.functions import TruncMonth
    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def monthly_sales(self, request):

        data = Payment.objects.filter(status="Success").annotate(
            month=TruncMonth("created_at")
        ).values("month").annotate(
            revenue=Sum("amount")
        ).order_by("month")

        return Response(data)
