from django.urls import path
from .views import index, view_info, view_items

urlpatterns = [
    path('', index, name='index'),
    path('items/', view_items, name='items'),
    path('info/', view_info, name='info'),
]
