from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'ecommerce.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('catalog.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^', include('orders.urls')),
    url(r'^menus/', include('menus.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

