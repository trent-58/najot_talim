from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='news_index'),
    path('category/<int:category_id>/', views.category_news, name='category_news'),
]
