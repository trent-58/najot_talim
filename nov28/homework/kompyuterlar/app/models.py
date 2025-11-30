from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100, blank = True)

class laptop(models.Model):
    model_name = models.CharField(max_length = 100)
    model_number = models.CharField(max_length = 100)

class order(models.Model):
    order =models.CharField(max_length = 100)
    order_details = models.CharField(max_length = 200)

