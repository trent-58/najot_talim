from django.urls import path
from .views import HouseListCreateAPIView, HouseDetailAPIView

urlpatterns = [
    path("houses/", HouseListCreateAPIView.as_view(), name="house-list-create"),
    path("houses/<int:pk>/", HouseDetailAPIView.as_view(), name="house-detail"),
]
