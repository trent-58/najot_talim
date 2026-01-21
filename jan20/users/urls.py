from .views import LoginAPIView, RegisterAPIView, UsersListAPIView
from django.urls import path

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("list/", UsersListAPIView.as_view(), name="list"),
]
