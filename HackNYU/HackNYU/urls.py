from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Django Default User Authentication
    # https://docs.djangoproject.com/en/1.10/topics/auth/default/
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    #url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),
    url(r'^detail/(?P<pk>\d+)/$', views.LabReportDetail.as_view(), name='detail'),
    url(r'^history/', views.HistoryView.as_view(), name='history'),
    url(r'^doctor/', views.DoctorView.as_view(), name='doctor'),
    url(r'^faq/', views.FaqView.as_view(), name='faq'),
    url(r'^help/', views.HelpView.as_view(), name='help'),
    url(r'^security/', views.SecurityView.as_view(), name='security'),
    url(r'^about/', views.AboutView.as_view(), name='about'),
    url(r'^contact/', views.ContactView.as_view(), name='contact'),
]