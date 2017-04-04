from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^$', views.show_cart, name='show_cart')
]
