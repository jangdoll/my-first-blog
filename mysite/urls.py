"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views
from blog.views import SignupView, RegisteredView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    # url(r'^account/', include('allauth.urls')),
    # url(r'^admin/', admin.site.urls),
    url(r'^account/login/$', views.login, name='login'),
    url(r'^account/logout/$', views.logout, name='logout', kwargs={'next_page': '/post'}),
    url(r'^signup/$', SignupView.as_view(), name='signup', kwargs={'next_page': 'account/login/'}),
    url(r'^accounts/login/done$', RegisteredView.as_view(), name='create_user_done')
]
