from rest_framework import serializers
from electronics import models


class ElectronicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Electronic
        fields = "__all__"

