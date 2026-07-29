from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "minimum_amount", "valid_to", "is_active")
    search_fields = ("code",)