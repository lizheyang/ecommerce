from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'ecommerce.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^register/$', views.register, name='register'),
    url('^login/$', auth_views.login,
        {'template_name': 'accounts/login.html'}),
    url('^changepw/$', auth_views.password_change,
        {'template_name': 'accounts/change_password.html'}, name='my_change_password'),
    url('^password_change/done/', views.my_password_change_done, name='my_password_change_done',),
    url('^my_account/$', views.my_account, name='my_account'),
    url('^logout/$', auth_views.logout, {'next_page': 'index'}),
    url('^edit_profile/$', views.edit_profile, name='edit_profile'),
    url('^show_profile/$', views.show_profile, name='show_profile'),
    url('^show_address/$', views.show_address, name='show_address'),
    url('^add_address/$', views.add_address, name='add_address'),
    ]