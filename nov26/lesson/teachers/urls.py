from django.urls import path, include

from .views import teacher, teacher2, index

urlpatterns = [
    path('', index, name='teacher'),
    path('teacher/', teacher, name='teacher'),
    path('teacher2/', teacher2, name='teacher2'),
]