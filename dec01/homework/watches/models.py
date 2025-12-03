from django.db import models

# Create your models here.


class company(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    

class watch(models.Model):
    name = models.CharField(max_length=50)
    company_fk = models.ForeignKey(company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}  |   {self.company_fk.name}"

class order(models.Model):
    name = models.CharField(max_length=40)
    watch_fk = models.ForeignKey(watch, on_delete=models.CASCADE)