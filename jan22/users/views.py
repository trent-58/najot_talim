from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import SignUpSerializer


class SignUpView(CreateAPIView):
  permission_classes = [ AllowAny ]
  queryset = User.objects.all()
  serializer_class = SignUpSerializer
