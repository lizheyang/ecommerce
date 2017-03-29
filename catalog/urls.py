from django.conf.urls import url
from . import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'ecommerce.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url('^product/(?P<product_id>[0-9]+)/$', views.show_product, name='product'),
    url(r'^category/(?P<category_id>[0-9]+)/$', views.show_categories, name='category')
]