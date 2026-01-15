from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import login_view, me_view, register_view

urlpatterns = [
    path("auth/register/", register_view, name="auth-register"),
    path("auth/login/", login_view, name="auth-login"),
    path("auth/me/", me_view, name="auth-me"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
]
