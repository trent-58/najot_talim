from django.urls import path
from .views import (
    ProductListView,
    CartView, CartAddItemView, CartUpdateItemView, CartClearView,
    CheckoutCreateOrderView,
    MyOrdersView,
)

urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("cart/", CartView.as_view()),
    path("cart/items/add/", CartAddItemView.as_view()),
    path("cart/items/<int:item_id>/", CartUpdateItemView.as_view()),
    path("cart/clear/", CartClearView.as_view()),
    path("checkout/", CheckoutCreateOrderView.as_view()),
    path("orders/", MyOrdersView.as_view()),
]
