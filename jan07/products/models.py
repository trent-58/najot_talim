from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.IntegerField()
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} {self.color} - ${self.price} "
