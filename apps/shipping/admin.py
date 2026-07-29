from django.contrib import admin
from .models import ShippingAddress


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "city", "state", "is_default")
    search_fields = ("user__email", "city", "postal_code")