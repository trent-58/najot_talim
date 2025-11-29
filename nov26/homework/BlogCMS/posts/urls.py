from django.urls import path
from .views import see_detail, see_post, index

urlpatterns = [
    path('', index, name='index'),
    path('see/', see_post, name='see'),
    path('details/', see_detail, name='detail'),
]
