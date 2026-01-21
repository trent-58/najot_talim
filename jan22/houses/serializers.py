from rest_framework import serializers
from .models import House

class HouseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = House
        fields = ("id", "owner", "title", "description", "price", "created_at")
