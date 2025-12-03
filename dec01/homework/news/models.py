from django.db import models

# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class news(models.Model):
    category_fk = models.ForeignKey(category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=2000)

    def __str__(self):
        return self.title
