from django.contrib import admin
from django.apps import AppConfig
from django import forms
from .models import Order


class OrdersConfig(AppConfig):
    name = 'orders'
    verbose_name = "订单管理"


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('created_at', 'updated_at',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    fields = ('id', 'user', 'address', 'status', 'express_company', 'express_number')
    readonly_fields = ('id', 'user')
    form = OrderAdminForm

admin.site.register(Order, OrderAdmin)
