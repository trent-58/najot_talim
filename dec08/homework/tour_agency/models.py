from django.db import models


class Tour(models.Model):
    title = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    available_seats = models.IntegerField()
    start_date = models.DateField()

    def __str__(self):
        return self.title


class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    number_of_people = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer_name} - {self.tour.title}"
