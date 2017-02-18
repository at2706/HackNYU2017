from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Django Default User Authentication
    # https://docs.djangoproject.com/en/1.10/topics/auth/default/
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^$', views.IndexView.as_view(), name='index'),
]
