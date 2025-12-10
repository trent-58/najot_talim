from django.urls import path
from .views import (
    TourListView,
    TourDetailView,
    TourCreateView,
    TourUpdateView,
    TourDeleteView,
    BookingListView,
    BookingDetailView,
    BookingCreateView,
    BookingUpdateView,
    BookingDeleteView,
)

urlpatterns = [
    path("tours/", TourListView.as_view(), name="tour_list"),
    path("tours/<int:pk>/", TourDetailView.as_view(), name="tour_detail"),
    path("tours/create/", TourCreateView.as_view(), name="tour_create"),
    path("tours/<int:pk>/update/", TourUpdateView.as_view(), name="tour_update"),
    path("tours/<int:pk>/delete/", TourDeleteView.as_view(), name="tour_delete"),
    path("bookings/", BookingListView.as_view(), name="booking_list"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking_detail"),
    path("bookings/create/", BookingCreateView.as_view(), name="booking_create"),
    path(
        "bookings/<int:pk>/update/", BookingUpdateView.as_view(), name="booking_update"
    ),
    path(
        "bookings/<int:pk>/delete/", BookingDeleteView.as_view(), name="booking_delete"
    ),
]
