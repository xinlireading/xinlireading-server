"""xinlireadingsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from xinlireading.views import SignupView, SigninView

urlpatterns = [
	url(r'^', include('xinlireading.urls')),
	url(r'^home/', include('xinlireading.urls')),
    # url(r'^signup/', include('xinlireading.urls')),
    url(r'^signup/', SignupView.as_view()),
    # url(r'^signin/', include('xinlireading.urls')),
    url(r'^signin/', SigninView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^invalid/', include('xinlireading.urls')),
    url(r'^success/', include('xinlireading.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
