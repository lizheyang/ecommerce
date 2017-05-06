from django.conf.urls import url
from . import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'ecommerce.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.show_menus, name='show_menus'),
    url(r'^spide_menus/$', views.spide_menus, name='spide_menus'),
    url(r'^menu_page/(?P<menu_folder>[a-z_0-9]+)/$', views.menu_page, name='menu_page'),
]
