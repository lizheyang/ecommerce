from django.db import models
from django import forms
from django.contrib.auth.models import User
from catalog.models import Product
from accounts.models import UserAddress
import decimal
import uuid


class Order(models.Model):
    ODER_STATUS = (
        (1, '未支付'),
        (2, '已支付'),
        (3, '已发货'),
        (4, '已完成'),
        (5, '已取消'),
    )

    order_id = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    address = models.ForeignKey(UserAddress)
    status = models.IntegerField(choices=ODER_STATUS, default=1)

    def __str__(self):
        return 'Order #' + str(self.id)

    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order)

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    @property
    def product_id(self):
        return self.product.id

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return self.product.get_absolute_url
