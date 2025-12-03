from django.db import models

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class meal(models.Model):
    name = models.CharField(max_length=50)
    category_fk = models.ForeignKey(category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name