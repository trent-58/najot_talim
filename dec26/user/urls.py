from . import views
from django.urls import path, include

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('detail/', views.detail, name='detail'),
    path('orders/', views.orders, name='orders'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),
]