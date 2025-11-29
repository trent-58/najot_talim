"""
URL configuration for BlogCMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path


def landing_page(request):
    from django.http import HttpResponse
    text = "<a href='posts/'>Posts</a>  | <a href='users/'>Users</a> | <a href='videos/'>Videos</a>"
    return HttpResponse(text)


urlpatterns = [
    path('', landing_page, name='landing'),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('users/', include('users.urls')),
    path('videos/', include('videos.urls')),
]
