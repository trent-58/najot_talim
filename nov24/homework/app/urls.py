from django.urls import path, include

from .views import index, hello_world, greet, get_squared, max_func, age

urlpatterns = [
    path('', index, name='index'),
    path('hello/', hello_world, name='hello_world'),
    path('hello/<str:name>/', greet, name='greet'),
    path('kvadrat/', get_squared, name='get_squared'),
    path('max/', max_func, name='max_func'),
    path('age/<int:num>/', age, name='age'),
]