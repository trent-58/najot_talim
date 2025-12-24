from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

app_name = "users"

urlpatterns = [
    path("", views.UserListView.as_view(), name="user_list"),
    path("add/", views.UserCreateView.as_view(), name="user_add"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
    path(
        "password/change/",
        login_required(
            auth_views.PasswordChangeView.as_view(
                template_name="registration/password_change_form.html",
                success_url=reverse_lazy("users:password_change_done"),
            )
        ),
        name="password_change",
    ),
    path(
        "password/change/done/",
        login_required(
            auth_views.PasswordChangeDoneView.as_view(
                template_name="registration/password_change_done.html"
            )
        ),
        name="password_change_done",
    ),
]
