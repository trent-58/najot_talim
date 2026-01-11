from django.urls import path
from electronics import views

urlpatterns = [
    path("electronics/", views.ElectronicListCreateView.as_view(), name="electronic-list-create"),
    path("electronics/<int:pk>/", views.ElectronicUpdateDeleteRetrieveView.as_view(), name="electronic-rud"),
]

