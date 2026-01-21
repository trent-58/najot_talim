from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import House
from .serializers import HouseSerializer


class HouseListCreateAPIView(GenericAPIView):
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return House.objects.filter(owner=self.request.user).order_by("-created_at")

    def get(self, request):
        houses = self.get_queryset()
        serializer = self.get_serializer(houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HouseDetailAPIView(GenericAPIView):
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return House.objects.filter(owner=self.request.user)

    def get(self, request, pk):
        house = self.get_object()
        serializer = self.get_serializer(house)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        house = self.get_object()
        serializer = self.get_serializer(house, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        house = self.get_object()
        serializer = self.get_serializer(house, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        house = self.get_object()
        house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
