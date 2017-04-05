import os
from PIL import Image
from django.db import models
from ecommerce.settings import MEDIA_ROOT


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='catalog/')
    thumb = models.ImageField(upload_to='catalog/thumb/', blank=True)
    brand = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name = '商品'
        verbose_name_plural = '商品'

    @models.permalink
    def get_absolute_url(self):
        return ('product', (), {'product_id': self.id})

    @staticmethod
    def make_thumb(path, size=220):
        img = Image.open(path)
        thumb = img.resize((size, size))
        return thumb

    def save(self):
        super().save()
        img_name = self.image.name
        img_path = os.path.join(MEDIA_ROOT, img_name)
        thumb = Image.open(img_path).resize((220, 220))
        thumb_path = os.path.join(MEDIA_ROOT, 'catalog\\thumb\\')
        thumb_name = os.path.join(thumb_path, str(self.id)+'.jpg')
        thumb.save(thumb_name)
        self.thumb = 'catalog/thumb/%s.jpg' % self.id
        super().save()

    def __str__(self):
        return self.name

