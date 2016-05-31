from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^signup/$', views.signup, name='signup'),
	# url(r'^signin/$', views.signin, name='signin'),
]
