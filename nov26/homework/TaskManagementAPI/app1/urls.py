from django.urls import path
from .views import index, see, details

urlpatterns = [
    path('', index, name='index'),
    path('see/', see, name='items'),
    path('details/', details, name='info'),
]
