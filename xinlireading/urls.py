from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
from xinlireading.views import TestCreateStudentView, SignupView, SigninView, DashboardView, EditProfileView

urlpatterns = [
	# url(r'^/', views.home, name='home'),
	url(r'^home/', views.home, name='home'),
	url(r'^account/signup/', SignupView.as_view(), name='signup'),
	url(r'^account/signin/', SigninView.as_view(), name='signin'),
	url(r'^account/logout/', DashboardView.as_view(), name='logout'),
	url(r'^invalid/', views.invalid, name='invalid'),
	# url(r'^account/', DashboardView.as_view(), name='dashboard'),
	url(r'^account/dashboard/', DashboardView.as_view(), name='dashboard'),
	url(r'^test/', TestCreateStudentView.as_view(), name='test'),
	url(r'^settings/profile/', EditProfileView.as_view(), name='edit-profile')
]
