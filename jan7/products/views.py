from django.shortcuts import render
from rest_framework import generics, status, response
from rest_framework.views import APIView

from products import serializers, models



# Create your views here.


# class CarList(generics.ListAPIView):
#     serializer_class = serializers.CarSerializer
#     queryset = models.Car.objects.all()


# class CarDetail(generics.RetrieveAPIView):
#     serializer_class = serializers.CarSerializer
#     queryset = models.Car.objects.all()
#     lookup_field = "pk"

# class CarCreate(generics.CreateAPIView):
#     serializer_class = serializers.CarSerializer
#     queryset = models.Car.objects.all()

# class CarUpdate(generics.UpdateAPIView):
#     serializer_class = serializers.CarSerializer
#     queryset = models.Car.objects.all()
#     lookup_field = "pk"

# class CarDelete(generics.DestroyAPIView):
#     serializer_class = serializers.CarSerializer
#     queryset = models.Car.objects.all()
#     lookup_field = "pk"


# class CarListCreate(generics.ListCreateAPIView):
#     serializer_class = serializers.CarSerializer
#     queryset = models.Car.objects.all()

# class CarRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.CarSerializer
#     queryset = models.Car.objects.all()
#     lookup_field = "pk"



class CarListView(generics.ListAPIView):
    def get(self, request):
        cars = models.Car.objects.all()
        serializer_class = serializers.CarSerializer(cars, many=True)



        if not cars:
            data = {
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'No cars available.'
            }
            return response.Response(data)
        
        data = {'status': status.HTTP_200_OK,
                'message': 'Cars retrieved successfully.',
                'data': serializer_class.data}
        return response.Response(data)


class CarDetailView(APIView):
    def get(self, request, pk):
        car = models.Car.objects.filter(pk=pk).first()
        serializer = serializers.CarSerializer(car)
        if not car:
            data = { 
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Specified car not found'
            }
            return response.Response(data)
            
        data = {
            'status': status.HTTP_200_OK,
            'message': 'specified car found',
            'data': serializer.data}
        return response.Response(data)


class CarCreateView(APIView):
    def post(self, request):
        serializer = serializers.CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Car created successfully',
                'data': serializer.data
            }
            return response.Response(data)
        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Car creation failed',
            'errors': serializer.errors
        }
        return response.Response(data)


class CarUpdateView(APIView):
    def put(self, request, pk):
        car = models.Car.objects.filter(pk=pk).first()
        serializer = serializers.CarSerializer(car, data=request.data)
        if not car:
            data = {
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Specified car not found'
            }
            return response.Response(data)

        if serializer.is_valid():
            serializer.save()
            data = {
                'status': status.HTTP_200_OK,
                'message': 'Car updated successfully',
                'data': serializer.data
            }
            return response.Response(data)


    def patch(self, request, pk):
        car = models.Car.objects.filter(pk=pk).first()
        serializer = serializers.CarSerializer(car, data=request.data)
        if not car:
            data = {
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Specified car not found'
            }
            return response.Response(data)

        if serializer.is_valid():
            serializer.save()
            data = {
                'status': status.HTTP_200_OK,
                'message': 'Car updated successfully',
                'data': serializer.data
            }
            return response.Response(data)


class CarDeleteView(APIView):
    def delete(self, request, pk):
        car = models.Car.objects.filter(pk=pk).first()
        if not car:
            data = {
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Specified car not found'
            }

            return response.Response(data)

        car.delete()
        data = {
            'status': status.HTTP_200_OK,
            'message': 'Car deleted successfully'
        }
        return response.Response(data)


