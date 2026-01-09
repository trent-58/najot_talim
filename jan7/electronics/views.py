from rest_framework.views import APIView
from rest_framework import status, response
from electronics import models, serializers


class ElectronicListCreateView(APIView):
    def get(self, request):
        electronics = models.Electronic.objects.all()
        serializer = serializers.ElectronicSerializer(electronics, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = serializers.ElectronicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElectronicUpdateDeleteRetrieveView(APIView):
    def get(self, request, pk):
        electronic = models.Electronic.objects.filter(pk=pk).first()
        if not electronic:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ElectronicSerializer(electronic)
        return response.Response(serializer.data)

    def put(self, request, pk):
        electronic = models.Electronic.objects.filter(pk=pk).first()
        if not electronic:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ElectronicSerializer(electronic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        electronic = models.Electronic.objects.filter(pk=pk).first()
        if not electronic:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ElectronicSerializer(electronic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        electronic = models.Electronic.objects.filter(pk=pk).first()
        if not electronic:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        electronic.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

