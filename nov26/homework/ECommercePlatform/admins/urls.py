from django.urls import path
from .views import index, view_admins, add_admin

urlpatterns = [
    path('', index, name='index'),
    path('view/', view_admins, name='view_admins'),
    path('add/', add_admin, name='add_admin'),
]
