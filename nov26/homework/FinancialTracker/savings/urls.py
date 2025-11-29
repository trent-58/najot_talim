from django.urls import path

from .views import index, see_details, see_savings

urlpatterns = [
    path('', index, name='index'),
    path('see/', see_savings, name='see'),
    path('details/', see_details, name='details'),
]