from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from .serializers import SignUpSerializers
from rest_framework import permissions

class SignUpView(generics.CreateAPIView):
  permission_classes = [permissions.AllowAny]
  queryset = CustomUser.objects.all()
  serializer_class = SignUpSerializers
