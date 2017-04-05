from django.contrib import admin
from .models import Category, Product
from django.apps import AppConfig

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)


class CatalogConfig(AppConfig):
    name = 'catalog'
    verbose_name = "商品目录"
