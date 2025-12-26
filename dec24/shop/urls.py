from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('shop_single_product/<int:pk>', views.shop_single_product, name='shop_single_product'),
    path('shop-checkout', views.shop_checkout, name='shop_checkout'),
]