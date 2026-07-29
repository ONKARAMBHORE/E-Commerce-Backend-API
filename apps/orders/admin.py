from django.contrib import admin

from .models import *

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "total", "created_at")
    list_filter = ("status",)
    search_fields = ("order_number", "user__email")

    
admin.site.register(OrderItem)