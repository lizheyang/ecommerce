from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from accounts.models import UserAddress
import decimal


class Order(models.Model):
    ODER_STATUS = (
        (1, '未支付'),
        (2, '已支付'),
        (3, '已发货'),
        (4, '已完成'),
        (5, '已取消'),
    )

    id = models.CharField(max_length=50, default='', primary_key=True, verbose_name='订单号')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='用户')
    address = models.ForeignKey(UserAddress, verbose_name='配送地址')
    status = models.IntegerField(choices=ODER_STATUS, default=1, verbose_name='订单状态')
    express_company = models.CharField(blank=True, null=True, max_length=50, verbose_name='快递公司')
    express_number = models.CharField(blank=True, null=True, max_length=50, verbose_name='快递单号')

    class Meta:
        app_label = 'orders'
        db_table = 'orders'
        ordering = ['-created_at']
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return '订单 #' + str(self.id) + self.ODER_STATUS[int(self.status)-1][1]

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

    class Meta:
        app_label = 'orders'

    @property
    def total(self):
        return self.quantity * self.price

    # @property
    # def name(self):
    #     return self.product.name
    #
    # @property
    # def product_id(self):
    #     return self.product.id

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return self.product.get_absolute_url
