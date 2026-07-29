from django.contrib import admin
from .models import Category, Brand, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","is_active")
    search_fields = ("name",)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id","name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","price","stock","is_available")
    search_fields = ("name","sku")


admin.site.register(ProductImage)




