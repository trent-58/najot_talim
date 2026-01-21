from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, UsersListSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response(
            {"msg": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class UsersListAPIView(generics.ListAPIView):
    serializer_class = UsersListSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
