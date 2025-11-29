from django.urls import path
from .views import see_users, see_info, index

urlpatterns = [
    path('', index, name='index'),
    path('see/', see_users, name='see'),
    path('info/', see_info, name='info'),
]
