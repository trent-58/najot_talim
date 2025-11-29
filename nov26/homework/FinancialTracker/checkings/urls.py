from django.urls import path

from .views import index, see_details, see_checkings

urlpatterns = [
    path('', index, name='index'),
    path('see/', see_checkings, name='see'),
    path('details/', see_details, name='details'),
]