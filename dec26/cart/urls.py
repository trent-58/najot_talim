from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/<int:pk>/', views.add_to_cart, name='add'),
    path('update/<int:pk>/', views.update_cart, name='update'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove'),
    path('clear/', views.clear_cart, name='clear'),
    path('process-checkout/', views.process_checkout, name='process_checkout'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
]
