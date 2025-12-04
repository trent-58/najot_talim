from django.db import models

    
class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category_fk = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    manufacturer_fk = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name