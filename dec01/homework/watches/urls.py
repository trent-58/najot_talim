from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='watches_index'),
    path('company/<int:company_id>/', views.company_watches, name='company_watches'),
    path('watch/<int:watch_id>/orders/', views.watch_orders, name='watch_orders'),
]
