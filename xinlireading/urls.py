from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
from xinlireading.views import SignupView, SigninView, DashboardView

urlpatterns = [
	url(r'^/', views.home, name='home'),
	url(r'^home/', views.home, name='home'),
	url(r'^signup/', SignupView.as_view(), name='signup'),
	url(r'^signin/', SignupView.as_view(), name='signin'),
	url(r'^invalid/', views.invalid, name='invalid'),
    # url(r'^success/', views.success, name='success'),
	url(r'^dashboard/', DashboardView.as_view(), name='dashboard')
]
