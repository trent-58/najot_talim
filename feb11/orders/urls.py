from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrderListAPIView.as_view(), name="order_list"),
    path("create/", views.OrderCreateAPIView.as_view(), name="order_create"),
    path("<int:pk>/", views.OrderDetailAPIView.as_view(), name="order_detail"),
    path("<int:pk>/status/", views.OrderStatusUpdateAPIView.as_view(), name="order_status_update"),
    path("<int:pk>/cancel/", views.OrderCancelAPIView.as_view(), name="order_cancel"),
]
