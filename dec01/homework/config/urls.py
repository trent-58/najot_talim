"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h3><a href='watches/'>Watches</a></h3>  <h3><a href='news/'>News</a></h3>  <h3><a href='menu/'>Menu</a></h3>   <h3><a href='admin/'>Adminka</a></h3>")


urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('menu/', include('menu.urls')),
    path('news/', include('news.urls')),
    path('watches/', include('watches.urls')),
]
