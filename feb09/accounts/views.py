from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, CodeVerificationSerializer, RegisterDetailsSerializer, UserChangePhotoSerializer, RetrieveUserDetailsSerializer, LoginSerializer, LogoutSerializer
from .models import CustomUser


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Code is sent. Enter the code."},
            status=status.HTTP_201_CREATED
        )


class CodeVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CodeVerificationSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.save()
        tokens["message"] = "Code is verified"
        return Response(tokens, status=status.HTTP_200_OK)


class RegisterDetailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegisterDetailsSerializer
    queryset = CustomUser.objects.all()

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Details are saved"}, status=status.HTTP_200_OK)


class UserChangePhotoView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserChangePhotoSerializer
    queryset = CustomUser.objects.all()

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Picture is updated"}, status=status.HTTP_200_OK)


class UserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetrieveUserDetailsSerializer
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)



class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.save()
        tokens.update(message="Successfull Login")
        return Response(tokens, status=status.HTTP_202_ACCEPTED)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



