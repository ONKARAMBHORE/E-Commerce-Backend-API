from django.db import models
from django.conf import settings
from apps.products.models import Product
from apps.shipping.models import ShippingAddress


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Packed", "Packed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled")
    )

    order_number = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey("coupons.Coupon", on_delete=models.SET_NULL, null=True, blank=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS, default="Pending")

    payment_method = models.CharField(max_length=30, default="COD")
    payment_status = models.CharField(max_length=20, default="Pending")
    invoice_number = models.CharField(max_length=30, blank=True)
    returned = models.BooleanField(default=False)
    refund_status = models.CharField(max_length=20, default="Not Requested")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
    


# order items

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name