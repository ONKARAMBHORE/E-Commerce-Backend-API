from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = ("id", "order", "payment_method", "amount", "status", "created_at")
    list_filter = ("payment_method", "status")
    search_fields = ("transaction_id", "razorpay_payment_id", "order__order_number")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "paid_at")