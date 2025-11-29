from django.urls import path

from .views import index, see, details


urlpatterns = [
    path('', index, name='index'),
    path('see/', see, name='see'),
    path('details/', details, name='details'),
]