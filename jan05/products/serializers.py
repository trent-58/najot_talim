from products import models
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Car
        fields = "__all__"
