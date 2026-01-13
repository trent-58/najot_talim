from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "id",
            "brand",
            "model",
            "year",
            "price",
            "color",
            "mileage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
