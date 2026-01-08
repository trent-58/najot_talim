from products import views
from django.urls import path


urlpatterns = [
    path("cars/", views.CarList.as_view(), name="car-list"),
    path("cars/<int:pk>/", views.CarDetail.as_view(), name="car-detail"),
    path("cars/create/", views.CarCreate.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", views.CarUpdate.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", views.CarDelete.as_view(), name="car-delete"),
    path("cars/list-create/", views.CarListCreate.as_view(), name="car-list-create"),
    path(
        "cars/<int:pk>/rud/", views.CarRetrieveUpdateDestroy.as_view(), name="car-rud"
    ),
]
