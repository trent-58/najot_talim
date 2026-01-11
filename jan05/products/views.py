from django.shortcuts import render
from rest_framework import generics
from products import serializers, models

# Create your views here.


class CarList(generics.ListAPIView):
    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()


class CarDetail(generics.RetrieveAPIView):
    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()
    lookup_field = "pk"

class CarCreate(generics.CreateAPIView):
    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()

class CarUpdate(generics.UpdateAPIView):
    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()
    lookup_field = "pk"

class CarDelete(generics.DestroyAPIView):
    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()
    lookup_field = "pk"


class CarListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()

class CarRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()
    lookup_field = "pk" 

    