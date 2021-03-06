from django.db import models
from catalog.models import Product


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, unique=False)

    class Meta:
        db_table = 'cart_items'
        ordering = ['created_at']

    def total(self):
        return self.quantity * self.product.discount_price

    def name(self):
        return self.product.name

    def price(self):
        return self.product.discount_price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        self.quantity += int(quantity)
        self.save()




