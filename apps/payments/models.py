from django.db import models
from apps.orders.models import Order



class Payment(models.Model):
    METHOD = (
        ("COD", "Cash On Delivery"),
        ("RAZORPAY", "Razorpay")
    )
    STATUS = (
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded")
    )
    # Linked order

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")

    payment_method = models.CharField(max_length=20, choices=METHOD)
    transaction_id = models.CharField(max_length=150, blank=True)
    razorpay_order_id = models.CharField(max_length=150, blank=True)
    razorpay_payment_id = models.CharField(max_length=150, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS, default="Pending")

    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now = True)

    def __str__ (self):
        return self.order.order_number
