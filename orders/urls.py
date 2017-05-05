from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^order/(?P<order_id>[\d]+)/$', views.order_page, name='order_page'),
    url(r'^payment/(?P<order_id>[\d]+)/$', views.payment, name='payment'),
    url(r'^confirm/payment/(?P<order_id>[\d]+)/$', views.confirm_payment, name='confirm_payment'),
    url(r'^cancel_order/(?P<order_id>[\d]+)/$', views.cancel_order, name='cancel_order'),
]