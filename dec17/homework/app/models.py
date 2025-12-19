from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os


def product_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{instance.name}-{uuid.uuid4()}.{ext}"
    return os.path.join("products", filename)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        to="Category", on_delete=models.CASCADE, related_name="products"
    )
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)

    class Meta:
        db_table = "products"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/default.webp"


class User(AbstractUser):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField()

    class Meta:
        db_table = "users"
        ordering = ["id"]

    def __str__(self):
        return self.username
