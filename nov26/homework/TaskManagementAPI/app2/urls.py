from django.urls import path
from .views import index, see, details

urlpatterns = [
    path('', index, name='index'),
    path('view/', see, name='items'),
    path('info/', details, name='info'),
]
