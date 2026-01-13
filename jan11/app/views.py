from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from django_filters import rest_framework as django_filters
from .models import Car
from .serializers import CarSerializer
from .filters import CarFilter


class CarPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    pagination_class = CarPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = CarFilter
    search_fields = ["brand", "model", "color"]
    ordering_fields = ["year", "price", "mileage", "created_at"]
    ordering = ["-created_at"]
