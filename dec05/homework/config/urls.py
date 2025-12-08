from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static


apps = [
    {
        "name": "markaz",
        "path": "markaz/",
        "image_url": "media/markaz.jpg"
    },
    {
        "name": "texnika",
        "path": "texnika/",
        "image_url": "media/texnika.png"
    },
]



urlpatterns = [
    path("", lambda request: render(request, "home.html", {"apps": apps}), name="home"),
    path("admin/", admin.site.urls),
    path("markaz/", include("markaz.urls")),
    path("texnika/", include("texnika.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
