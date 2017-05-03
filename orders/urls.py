from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^order/(?P<order_id>[\w\-]+)/$', views.order_page, name='order_page'),
]