from django import forms
from redactor.widgets import RedactorEditor
from django.contrib import admin
from catalog.models import Category, Product
from django.apps import AppConfig

# Register your models here.



class CatalogConfig(AppConfig):
    name = 'catalog'
    verbose_name = "商品目录"


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {
            'description': RedactorEditor(),
        }
        exclude = ('thumb', 'created_at', 'updated_at',)


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)