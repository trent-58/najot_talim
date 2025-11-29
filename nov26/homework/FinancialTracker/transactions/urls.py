from django.urls import path
from .views import index, see_details, see_transactions

urlpatterns = [
    path('', index, name='index'),
    path('see/', see_transactions, name='see'),
    path('details/', see_details, name='details'),
]
