from django.urls import path
from .views import see_videos, see_video_info, index

urlpatterns = [
    path('', index, name='index'),
    path('see/', see_videos, name='see'),
    path('info/', see_video_info, name='info'),
]
