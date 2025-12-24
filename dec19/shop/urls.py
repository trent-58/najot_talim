from django.contrib import admin
from django.urls import path, include
from store.views import home
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path(
        "admin/password_change/",
        RedirectView.as_view(pattern_name="users:password_change", permanent=False),
    ),
    path(
        "admin/password_change/done/",
        RedirectView.as_view(
            pattern_name="users:password_change_done", permanent=False
        ),
    ),
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="registration/logged_out.html"),
        name="logout",
    ),
    path("store/", include("store.urls")),
    path("users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
