from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Tour, Booking


class TourListView(ListView):
    model = Tour
    template_name = "tour_agency/tour_list.html"
    context_object_name = "tours"
    paginate_by = 10


class TourDetailView(DetailView):
    model = Tour
    template_name = "tour_agency/tour_detail.html"
    context_object_name = "tour"


class TourCreateView(CreateView):
    model = Tour
    template_name = "tour_agency/tour_form.html"
    fields = [
        "title",
        "destination",
        "description",
        "price",
        "duration_days",
        "available_seats",
        "start_date",
    ]
    success_url = reverse_lazy("tour_list")


class TourUpdateView(UpdateView):
    model = Tour
    template_name = "tour_agency/tour_form.html"
    fields = [
        "title",
        "destination",
        "description",
        "price",
        "duration_days",
        "available_seats",
        "start_date",
    ]
    success_url = reverse_lazy("tour_list")


class TourDeleteView(DeleteView):
    model = Tour
    template_name = "tour_agency/tour_confirm_delete.html"
    success_url = reverse_lazy("tour_list")


class BookingListView(ListView):
    model = Booking
    template_name = "tour_agency/booking_list.html"
    context_object_name = "bookings"
    paginate_by = 10


class BookingDetailView(DetailView):
    model = Booking
    template_name = "tour_agency/booking_detail.html"
    context_object_name = "booking"


class BookingCreateView(CreateView):
    model = Booking
    template_name = "tour_agency/booking_form.html"
    fields = [
        "tour",
        "customer_name",
        "customer_email",
        "phone_number",
        "number_of_people",
        "total_price",
    ]
    success_url = reverse_lazy("booking_list")


class BookingUpdateView(UpdateView):
    model = Booking
    template_name = "tour_agency/booking_form.html"
    fields = [
        "tour",
        "customer_name",
        "customer_email",
        "phone_number",
        "number_of_people",
        "total_price",
    ]
    success_url = reverse_lazy("booking_list")


class BookingDeleteView(DeleteView):
    model = Booking
    template_name = "tour_agency/booking_confirm_delete.html"
    success_url = reverse_lazy("booking_list")
