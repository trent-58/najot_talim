from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import (
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def me_view(request):
    if request.method == "DELETE":
        # delete account + revoke token
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == "GET":
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PATCH
    serializer = UserSerializer(
        request.user,
        data=request.data,
        partial=True,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_view(request):
    # require password here
    password = request.data.get("password")
    if not password or len(password) < 8:
        return Response(
            {"password": ["Password is required (min 8 chars)."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {"user": UserSerializer(user).data, "token": token.key},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    old_password = serializer.validated_data["old_password"]
    new_password = serializer.validated_data["new_password"]

    if not request.user.check_password(old_password):
        return Response({"old_password": ["Old password is incorrect."]}, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(new_password)
    request.user.save()

    # revoke token so user must login again
    try:
        request.user.auth_token.delete()
    except Exception:
        pass

    return Response({"detail": "Password updated. Please login again."}, status=status.HTTP_200_OK)
