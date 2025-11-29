from django.urls import path
from .views import index, view_items, view_info

urlpatterns = [
    path('', index, name='index'),
    path('items/', view_items, name='view_items'),
    path('info/', view_info, name='view_info'),
]
