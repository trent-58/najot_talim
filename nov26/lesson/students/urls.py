from django.urls import path, include

from .views import about, my_group, students

urlpatterns = [
    path('', students, name='student'),
    path('about/', about, name='about'),
    path('my_group/', my_group, name='my_group'),
]