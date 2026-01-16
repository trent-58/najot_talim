from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    me_view,
    change_password_view,
)

urlpatterns = [
    path("auth/register/", register_view),
    path("auth/login/", login_view, name="auth-login"),
    path("auth/logout/", logout_view, name="auth-logout"),
    path("auth/me/", me_view, name="auth-me"),
    path("auth/change-password/", change_password_view, name="auth-change-password"),
]
