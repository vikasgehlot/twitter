"""users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.shortcuts import render
from django.urls import path,include
from django.http import HttpResponse
from django.contrib.auth.models import User


def home(request):
	return HttpResponse("<div><h3>Create User at /api/user/</h3></div><div><h3> Already a user Login /api/auth/login/</h3></div>")

def profile(request):
	if request.user not in User.objects.all():
		return HttpResponse("<h3>NOT a Authenticated user<h3>")
	print(request.user)
	return HttpResponse("<h3>Login Successful<h3>")


urlpatterns = [
	path('',home),
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
	path('accounts/profile/',profile)
]
