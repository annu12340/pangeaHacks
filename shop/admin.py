from django.contrib import admin
from .models import Category, Product, CreditCard


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "rating", "count", "category", "date"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(CreditCard)
