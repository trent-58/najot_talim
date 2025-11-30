from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=200)

    def __str__(self):
        return self.name

