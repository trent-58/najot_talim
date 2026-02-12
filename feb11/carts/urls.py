from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartDetailAPIView.as_view(), name="cart_detail"),
    path("add/", views.CartAddAPIView.as_view(), name="cart_add"),
    path("remove/", views.CartRemoveAPIView.as_view(), name="cart_remove"),
    path("clear/", views.CartClearAPIView.as_view(), name="cart_clear"),
    path("update/", views.CartUpdateAPIView.as_view(), name="cart_update"),
]
